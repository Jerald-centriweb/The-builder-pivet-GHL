"""
WF-03 Scoring Engine — PreBuild Autopilot
==========================================
Deploy as:
  - n8n Code Node (paste the score_lead function)
  - Google Cloud Function (use the Flask handler)
  - AWS Lambda (use the lambda_handler)

This receives survey data from a GHL webhook and returns:
  - qualification_score (0-100)
  - lead_temperature (hot/warm/cold)
  - tags to apply
  - pipeline stage to move to
  - is_disqualified (boolean)
  - disqualifier_reason (if applicable)

Then POST the result back to GHL to update the contact.
"""

import json
import math

# --- SCORING CONFIGURATION ---

SCORING_RUBRIC = {
    "project_type": {
        "New Home Build": 10,
        "New Build": 10,
        "Knockdown & Rebuild": 10,
        "Knockdown Rebuild": 10,
        "Extension": 8,
        "Renovation": 6,
    },
    "land_status": {
        "Yes, I own the land/property": 15,
        "Own Land": 15,
        "Under contract (settlement pending)": 12,
        "Under Contract": 12,
        "Still looking for land": 5,
        "Looking": 5,
    },
    "design_status": {
        "I have detailed plans or drawings ready": 15,
        "Plans Ready": 15,
        "Plans ready": 15,
        "I have a rough concept or sketch": 10,
        "Concept Only": 10,
        "Concept only": 10,
        "I haven't started on plans yet": 5,
        "Nothing Yet": 5,
        "Nothing yet": 5,
    },
    "timeline": {
        "As soon as possible": 15,
        "ASAP": 15,
        "Within 3-6 months": 12,
        "Within 3\u20136 months": 12,
        "3-6 months": 12,
        "3\u20136 months": 12,
        "6-12 months from now": 8,
        "6\u201312 months": 8,
        "6-12 months": 8,
        "More than 12 months away": 3,
        "12+ months": 3,
        "12 months+": 3,
    },
    "prior_quotes": {
        "No, you're my first point of contact": 10,
        "First Contact": 10,
        "First contact": 10,
        "Yes, 1-2 other builders": 10,
        "Yes, 1\u20132 other builders": 10,
        "1-2 Builders": 10,
        "1-2 builders": 10,
        "Yes, 3 or more builders": 5,
        "3+ Builders": 5,
        "3+ builders": 5,
    },
    "budget_range": {
        "Under $300,000": "DISQUALIFY",
        "Under $300K": "DISQUALIFY",
        "$300,000 - $500,000": 5,
        "$300,000 \u2013 $500,000": 5,
        "$300-500K": 5,
        "$300\u2013500K": 5,
        "$500,000 - $800,000": 10,
        "$500,000 \u2013 $800,000": 10,
        "$500-800K": 10,
        "$500\u2013800K": 10,
        "$800,000 - $1,200,000": 15,
        "$800,000 \u2013 $1,200,000": 15,
        "$800K-1.2M": 15,
        "$800K\u20131.2M": 15,
        "Over $1,200,000": 15,
        "$1.2M+": 15,
    },
    "financing_status": {
        "Pre-approved by a lender": 15,
        "Pre-approved": 15,
        "Cash buyer (no finance needed)": 15,
        "Cash buyer": 15,
        "Cash Buyer": 15,
        "Working with a broker (in progress)": 12,
        "In progress": 12,
        "Using broker": 12,
        "Haven't started the finance process yet": 6,
        "Not started": 6,
    },
    "decision_maker": {
        "Yes, I'm the sole decision-maker": 10,
        "Yes": 10,
        "It's a shared decision (with partner/spouse)": 8,
        "Shared": 8,
        "Someone else will make the final call": 3,
        "Other": 3,
    },
    "site_challenges": {
        "No significant challenges that I'm aware of": 10,
        "No challenges": 10,
        "None": 10,
        "Some potential issues (slope, flooding, heritage, bushfire zone)": 7,
        "Some": 7,
        "Significant challenges (steep site, difficult access, contamination, etc.)": 3,
        "Significant": 3,
    },
    "open_to_fee": {
        "Yes, that makes sense": 15,
        "Yes": 15,
        "I'd need to understand more about what's included": 8,
        "Needs more info": 8,
        "Need more info": 8,
        "No, I'm only looking for free quotes": "DISQUALIFY",
        "No": "DISQUALIFY",
    },
}

MAX_RAW_SCORE = 145  # Sum of all max points

# Score bands (on normalised 0-100 scale)
HOT_THRESHOLD = 80
WARM_THRESHOLD = 50


def score_lead(survey_data: dict) -> dict:
    """
    Calculate qualification score from survey responses.

    Args:
        survey_data: dict with keys matching SCORING_RUBRIC categories.
            Expected keys: project_type, land_status, design_status, timeline,
            prior_quotes, budget_range, financing_status, decision_maker,
            site_challenges, open_to_fee

    Returns:
        dict with: raw_score, qualification_score (0-100), lead_temperature,
        tags, pipeline_stage, is_disqualified, disqualifier_reason
    """
    raw_score = 0
    disqualified = False
    disqualifier_reasons = []
    scoring_breakdown = {}

    for field, rubric in SCORING_RUBRIC.items():
        answer = survey_data.get(field, "")
        if not answer:
            scoring_breakdown[field] = {"answer": "(blank)", "points": 0}
            continue

        answer = str(answer).strip()
        points = rubric.get(answer, 0)

        if points == "DISQUALIFY":
            disqualified = True
            disqualifier_reasons.append(f"{field}: {answer}")
            scoring_breakdown[field] = {"answer": answer, "points": "DISQUALIFIED"}
        elif isinstance(points, (int, float)):
            raw_score += points
            scoring_breakdown[field] = {"answer": answer, "points": points}
        else:
            # No matching answer found - try fuzzy match
            matched = False
            for key, val in rubric.items():
                if answer.lower() in key.lower() or key.lower() in answer.lower():
                    if val == "DISQUALIFY":
                        disqualified = True
                        disqualifier_reasons.append(f"{field}: {answer}")
                        scoring_breakdown[field] = {"answer": answer, "points": "DISQUALIFIED"}
                    else:
                        raw_score += val
                        scoring_breakdown[field] = {"answer": answer, "points": val}
                    matched = True
                    break
            if not matched:
                scoring_breakdown[field] = {"answer": answer, "points": 0, "note": "unrecognised answer"}

    # Normalise to 0-100
    normalised_score = round((raw_score / MAX_RAW_SCORE) * 100) if not disqualified else 0

    # Determine temperature and routing
    if disqualified:
        lead_temperature = "cold"
        pipeline_stage = "Not Now"
        tags = ["lead-cold"]
    elif normalised_score >= HOT_THRESHOLD:
        lead_temperature = "hot"
        pipeline_stage = "Qualified"
        tags = ["lead-hot"]
    elif normalised_score >= WARM_THRESHOLD:
        lead_temperature = "warm"
        pipeline_stage = "Nurture"
        tags = ["lead-warm"]
    else:
        lead_temperature = "cold"
        pipeline_stage = "Not Now"
        tags = ["lead-cold"]

    # Always add survey-completed, remove survey-pending
    tags.append("survey-completed")

    return {
        "raw_score": raw_score,
        "max_raw_score": MAX_RAW_SCORE,
        "qualification_score": normalised_score,
        "lead_temperature": lead_temperature,
        "pipeline_stage": pipeline_stage,
        "tags_to_add": tags,
        "tags_to_remove": ["survey-pending"],
        "is_disqualified": disqualified,
        "disqualifier_reasons": disqualifier_reasons if disqualified else [],
        "scoring_breakdown": scoring_breakdown,
    }


# --- GHL API INTEGRATION ---

def update_ghl_contact(contact_id: str, score_result: dict, api_key: str, location_id: str = None):
    """
    POST score results back to GHL to update contact fields and tags.
    Uses urllib to avoid external dependencies.
    """
    import urllib.request
    import urllib.error

    base_url = "https://services.leadconnectorhq.com"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Version": "2021-07-28",
    }

    # 1. Update custom fields
    update_data = {
        "customFields": [
            {"key": "cf_qualification_score", "field_value": str(score_result["qualification_score"])},
            {"key": "cf_lead_temperature", "field_value": score_result["lead_temperature"]},
        ],
    }

    # Add tags
    if score_result["tags_to_add"]:
        update_data["tags"] = score_result["tags_to_add"]

    req = urllib.request.Request(
        f"{base_url}/contacts/{contact_id}",
        data=json.dumps(update_data).encode(),
        headers=headers,
        method="PUT",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
            print(f"Contact {contact_id} updated: score={score_result['qualification_score']}, temp={score_result['lead_temperature']}")
            return result
    except urllib.error.HTTPError as e:
        print(f"Error updating contact: {e.code} - {e.read().decode()}")
        return None

    # 2. Remove tags (separate API call)
    for tag in score_result.get("tags_to_remove", []):
        try:
            remove_req = urllib.request.Request(
                f"{base_url}/contacts/{contact_id}/tags",
                data=json.dumps({"tags": [tag]}).encode(),
                headers=headers,
                method="DELETE",
            )
            urllib.request.urlopen(remove_req, timeout=15)
        except Exception:
            pass


# --- DEPLOYMENT HANDLERS ---

def n8n_handler(items):
    """
    For use as an n8n Code node.
    Input: items[0].json should contain survey fields + contact_id
    Output: scoring result
    """
    data = items[0]["json"] if isinstance(items, list) else items
    contact_id = data.pop("contact_id", data.pop("contactId", None))

    result = score_lead(data)
    result["contact_id"] = contact_id

    return [{"json": result}]


def flask_handler():
    """For Google Cloud Function or any Flask-based deployment."""
    from flask import Flask, request, jsonify

    app = Flask(__name__)

    @app.route("/score", methods=["POST"])
    def score():
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        contact_id = data.pop("contact_id", data.pop("contactId", None))
        api_key = data.pop("api_key", data.pop("apiKey", None))

        result = score_lead(data)
        result["contact_id"] = contact_id

        # If API key provided, update GHL directly
        if api_key and contact_id:
            update_ghl_contact(contact_id, result, api_key)

        return jsonify(result)

    return app


def lambda_handler(event, context):
    """For AWS Lambda deployment."""
    body = json.loads(event.get("body", "{}"))
    contact_id = body.pop("contact_id", body.pop("contactId", None))
    api_key = body.pop("api_key", body.pop("apiKey", None))

    result = score_lead(body)
    result["contact_id"] = contact_id

    if api_key and contact_id:
        update_ghl_contact(contact_id, result, api_key)

    return {
        "statusCode": 200,
        "body": json.dumps(result),
        "headers": {"Content-Type": "application/json"},
    }


# --- CLI TESTING ---

if __name__ == "__main__":
    # Test with a Hot lead profile
    hot_lead = {
        "project_type": "New Home Build",
        "land_status": "Yes, I own the land/property",
        "design_status": "I have detailed plans or drawings ready",
        "timeline": "As soon as possible",
        "prior_quotes": "No, you're my first point of contact",
        "budget_range": "$800,000 - $1,200,000",
        "financing_status": "Pre-approved by a lender",
        "decision_maker": "Yes, I'm the sole decision-maker",
        "site_challenges": "No significant challenges that I'm aware of",
        "open_to_fee": "Yes, that makes sense",
    }

    warm_lead = {
        "project_type": "Extension",
        "land_status": "Yes, I own the land/property",
        "design_status": "I have a rough concept or sketch",
        "timeline": "Within 3-6 months",
        "prior_quotes": "Yes, 1-2 other builders",
        "budget_range": "$300,000 - $500,000",
        "financing_status": "Working with a broker (in progress)",
        "decision_maker": "It's a shared decision (with partner/spouse)",
        "site_challenges": "No significant challenges that I'm aware of",
        "open_to_fee": "I'd need to understand more about what's included",
    }

    cold_lead = {
        "project_type": "Renovation",
        "land_status": "Still looking for land",
        "design_status": "I haven't started on plans yet",
        "timeline": "More than 12 months away",
        "prior_quotes": "Yes, 3 or more builders",
        "budget_range": "$300,000 - $500,000",
        "financing_status": "Haven't started the finance process yet",
        "decision_maker": "Someone else will make the final call",
        "site_challenges": "Significant challenges (steep site, difficult access, contamination, etc.)",
        "open_to_fee": "I'd need to understand more about what's included",
    }

    disqualified_budget = {
        "project_type": "New Home Build",
        "land_status": "Yes, I own the land/property",
        "design_status": "I have detailed plans or drawings ready",
        "timeline": "As soon as possible",
        "budget_range": "Under $300,000",
        "open_to_fee": "Yes, that makes sense",
    }

    disqualified_fee = {
        "project_type": "New Home Build",
        "budget_range": "$500,000 - $800,000",
        "open_to_fee": "No, I'm only looking for free quotes",
    }

    print("=" * 60)
    print("WF-03 SCORING ENGINE — TEST RESULTS")
    print("=" * 60)

    for name, lead in [
        ("HOT LEAD", hot_lead),
        ("WARM LEAD", warm_lead),
        ("COLD LEAD", cold_lead),
        ("DISQUALIFIED (Budget)", disqualified_budget),
        ("DISQUALIFIED (Fee)", disqualified_fee),
    ]:
        result = score_lead(lead)
        print(f"\n--- {name} ---")
        print(f"  Raw score: {result['raw_score']}/{result['max_raw_score']}")
        print(f"  Normalised: {result['qualification_score']}/100")
        print(f"  Temperature: {result['lead_temperature']}")
        print(f"  Pipeline: {result['pipeline_stage']}")
        print(f"  Tags: {result['tags_to_add']}")
        if result['is_disqualified']:
            print(f"  DISQUALIFIED: {result['disqualifier_reasons']}")
        print(f"  Breakdown:")
        for field, detail in result['scoring_breakdown'].items():
            print(f"    {field}: {detail['answer']} → {detail['points']} pts")
