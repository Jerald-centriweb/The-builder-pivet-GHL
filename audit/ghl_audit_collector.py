#!/usr/bin/env python3
"""
GHL Sub-Account Audit Data Collector — PreBuild Autopilot
=========================================================
Run this script locally where you have network access to the GHL API.

Usage:
    python3 ghl_audit_collector.py \
        --api-key "pit-335bf0ee-b8e4-4eaa-be07-997052ceb717" \
        --location-id "YOUR_LOCATION_ID"

Find your Location ID: GHL → Settings → Company → Locations → copy the ID

Output: audit_data.json (comprehensive dump of all GHL sub-account data)
"""

import argparse
import json
import time
import sys
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"


def api_post(path, api_key, body):
    """Make authenticated POST request to GHL API."""
    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Version": API_VERSION,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "PreBuildAudit/1.0 (https://github.com/Jerald-centriweb/The-builder-pivet-GHL)",
    }
    data = json.dumps(body).encode("utf-8")
    try:
        req = Request(url, data=data, headers=headers, method="POST")
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        body_err = e.read().decode() if hasattr(e, "read") else ""
        return {"error": e.code, "message": body_err, "url": url}
    except URLError as e:
        return {"error": "urlerror", "message": str(e), "url": url}


def api_get(path, api_key, params=None):
    """Make authenticated GET request to GHL API with retry."""
    url = f"{BASE_URL}{path}"
    if params:
        qs = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{qs}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Version": API_VERSION,
        "Accept": "application/json",
        "User-Agent": "PreBuildAudit/1.0 (https://github.com/Jerald-centriweb/The-builder-pivet-GHL)",
    }

    for attempt in range(4):
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except HTTPError as e:
            if e.code == 429:
                wait = 2 ** (attempt + 1)
                print(f"  Rate limited. Waiting {wait}s...")
                time.sleep(wait)
                continue
            body = e.read().decode() if hasattr(e, 'read') else ""
            return {"error": e.code, "message": body, "url": url}
        except URLError as e:
            wait = 2 ** (attempt + 1)
            print(f"  Network error: {e}. Retrying in {wait}s...")
            time.sleep(wait)
    return {"error": "timeout", "message": "Failed after 4 retries", "url": url}


def paginate(path, api_key, key, params=None):
    """Paginate through GHL API results."""
    all_items = []
    params = params or {}
    params.setdefault("limit", "100")

    while True:
        data = api_get(path, api_key, params)
        if "error" in data:
            return data
        items = data.get(key, [])
        all_items.extend(items)
        meta = data.get("meta", data.get("traceData", {}))
        next_page = meta.get("nextPageUrl") or meta.get("startAfterId") or meta.get("startAfter")
        if not next_page or not items:
            break
        if "startAfterId" in meta:
            params["startAfterId"] = meta["startAfterId"]
        elif "startAfter" in meta:
            params["startAfter"] = str(meta["startAfter"])
        else:
            break
        time.sleep(0.3)

    return all_items


def collect_all(api_key, location_id):
    audit = {"collected_at": datetime.utcnow().isoformat(), "location_id": location_id, "sections": {}}

    # 1. Custom Fields
    print("[1/17] Fetching custom fields...")
    audit["sections"]["custom_fields"] = api_get(f"/locations/{location_id}/customFields", api_key)
    time.sleep(0.3)

    # 2. Contacts (via search - GET /contacts/ often returns empty, POST /contacts/search works)
    print("[2/17] Fetching contacts (sample)...")
    contacts_resp = api_post("/contacts/search", api_key, {
        "locationId": location_id,
        "pageLimit": 100,
        "query": ""  # Empty query returns recent contacts
    })
    if isinstance(contacts_resp, dict) and "error" in contacts_resp:
        audit["sections"]["contacts"] = contacts_resp
    else:
        audit["sections"]["contacts"] = contacts_resp
    time.sleep(0.3)

    # 3. Pipelines
    print("[3/17] Fetching pipelines...")
    audit["sections"]["pipelines"] = api_get("/opportunities/pipelines", api_key, {"locationId": location_id})
    time.sleep(0.3)

    # 4. Opportunities (sample)
    print("[4/17] Fetching opportunities...")
    pipelines = audit["sections"].get("pipelines", {})
    if isinstance(pipelines, dict) and "pipelines" in pipelines:
        for p in pipelines["pipelines"][:3]:
            pid = p.get("id", "")
            opps = api_get("/opportunities/search", api_key, {
                "location_id": location_id, "pipeline_id": pid, "limit": "50"
            })
            audit["sections"][f"opportunities_{pid}"] = opps
            time.sleep(0.3)
    time.sleep(0.3)

    # 5. Workflows
    print("[5/17] Fetching workflows...")
    audit["sections"]["workflows"] = api_get("/workflows/", api_key, {"locationId": location_id})
    time.sleep(0.3)

    # 6. Forms
    print("[6/17] Fetching forms...")
    audit["sections"]["forms"] = api_get("/forms/", api_key, {"locationId": location_id})
    time.sleep(0.3)

    # 7. Surveys
    print("[7/17] Fetching surveys...")
    audit["sections"]["surveys"] = api_get("/surveys/", api_key, {"locationId": location_id})
    time.sleep(0.3)

    # 8. Calendars
    print("[8/17] Fetching calendars...")
    audit["sections"]["calendars"] = api_get("/calendars/", api_key, {"locationId": location_id})
    time.sleep(0.3)

    # 9. Tags
    print("[9/17] Fetching tags...")
    audit["sections"]["tags"] = api_get(f"/locations/{location_id}/tags", api_key)
    time.sleep(0.3)

    # 10. Custom Objects
    print("[10/17] Fetching custom objects...")
    audit["sections"]["custom_objects"] = api_get(f"/locations/{location_id}/customObjects", api_key)
    time.sleep(0.3)

    # 11. Custom Values
    print("[11/17] Fetching custom values...")
    audit["sections"]["custom_values"] = api_get(f"/locations/{location_id}/customValues", api_key)
    time.sleep(0.3)

    # 12. Location info
    print("[12/17] Fetching location info...")
    audit["sections"]["location"] = api_get(f"/locations/{location_id}", api_key)
    time.sleep(0.3)

    # 13. Campaigns / Email Templates (if available)
    print("[13/17] Fetching campaigns...")
    audit["sections"]["campaigns"] = api_get("/campaigns/", api_key, {"locationId": location_id})
    time.sleep(0.3)

    # 14. Payments / Transactions
    print("[14/17] Fetching payments...")
    audit["sections"]["payments"] = api_get("/payments/orders", api_key, {"locationId": location_id, "limit": "50"})

    # 15. Email & SMS Templates
    print("[15/17] Fetching templates...")
    audit["sections"]["templates"] = api_get(f"/locations/{location_id}/templates", api_key)

    # 16. Brand Boards (colors, fonts)
    print("[16/17] Fetching brand boards...")
    audit["sections"]["brand_boards"] = api_get(f"/brand-boards/{location_id}", api_key)

    # 17. Funnels (may contain styling)
    print("[17/17] Fetching funnels...")
    audit["sections"]["funnels"] = api_get("/funnels/funnel/list", api_key, {"locationId": location_id})

    return audit


def analyze_contacts(contacts_data):
    """Quick analysis of contact data quality."""
    analysis = {
        "total_sampled": 0,
        "with_qualification_score": 0,
        "with_budget_range": 0,
        "with_lead_temperature": 0,
        "with_service_phase": 0,
        "with_email": 0,
        "with_phone": 0,
        "tag_distribution": {},
    }

    contacts = contacts_data.get("contacts", []) if isinstance(contacts_data, dict) else []
    analysis["total_sampled"] = len(contacts)

    for c in contacts:
        cf = c.get("customFields", c.get("customField", []))
        tags = c.get("tags", [])

        if c.get("email"):
            analysis["with_email"] += 1
        if c.get("phone"):
            analysis["with_phone"] += 1

        for tag in tags:
            t = tag if isinstance(tag, str) else tag.get("name", str(tag))
            analysis["tag_distribution"][t] = analysis["tag_distribution"].get(t, 0) + 1

        if isinstance(cf, list):
            for field in cf:
                key = field.get("key", field.get("id", ""))
                val = field.get("value", field.get("field_value", ""))
                if "qualification_score" in str(key) and val:
                    analysis["with_qualification_score"] += 1
                if "budget_range" in str(key) and val:
                    analysis["with_budget_range"] += 1
                if "lead_temperature" in str(key) and val:
                    analysis["with_lead_temperature"] += 1
                if "service_phase" in str(key) and val:
                    analysis["with_service_phase"] += 1
        elif isinstance(cf, dict):
            for key, val in cf.items():
                if "qualification_score" in key and val:
                    analysis["with_qualification_score"] += 1
                if "budget_range" in key and val:
                    analysis["with_budget_range"] += 1
                if "lead_temperature" in key and val:
                    analysis["with_lead_temperature"] += 1
                if "service_phase" in key and val:
                    analysis["with_service_phase"] += 1

    return analysis


def main():
    parser = argparse.ArgumentParser(description="GHL Sub-Account Audit Collector")
    parser.add_argument("--api-key", required=True, help="GHL Private Integration API Key")
    parser.add_argument("--location-id", required=True, help="GHL Location ID (Settings → Company → Locations)")
    parser.add_argument("--output", default="audit_data.json", help="Output file path")
    args = parser.parse_args()

    print("=" * 60)
    print("GHL Sub-Account Audit Collector — PreBuild Autopilot")
    print("=" * 60)
    print(f"API Key: {args.api_key[:10]}...{args.api_key[-4:]}")
    print(f"Location ID: {args.location_id}")
    print(f"Output: {args.output}")
    print()

    audit = collect_all(args.api_key, args.location_id)

    # Run contact analysis
    if "contacts" in audit["sections"]:
        print("\nAnalyzing contact data quality...")
        audit["analysis"] = {
            "contacts": analyze_contacts(audit["sections"]["contacts"])
        }

    with open(args.output, "w") as f:
        json.dump(audit, f, indent=2, default=str)

    print(f"\nAudit data saved to {args.output}")
    print(f"Total sections collected: {len(audit['sections'])}")

    # Print quick summary
    print("\n--- Quick Summary ---")
    for section, data in audit["sections"].items():
        if isinstance(data, dict) and "error" in data:
            print(f"  {section}: ERROR {data['error']} - {data.get('message', '')[:80]}")
        elif isinstance(data, list):
            print(f"  {section}: {len(data)} items")
        elif isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, list):
                    print(f"  {section}.{k}: {len(v)} items")
                    break
            else:
                print(f"  {section}: retrieved")

    if "analysis" in audit:
        ca = audit["analysis"]["contacts"]
        print(f"\n--- Contact Analysis ({ca['total_sampled']} sampled) ---")
        print(f"  With qualification score: {ca['with_qualification_score']}")
        print(f"  With budget range: {ca['with_budget_range']}")
        print(f"  With lead temperature: {ca['with_lead_temperature']}")
        print(f"  With service phase: {ca['with_service_phase']}")
        print(f"  With email: {ca['with_email']}")
        print(f"  With phone: {ca['with_phone']}")
        if ca["tag_distribution"]:
            print(f"  Tag distribution: {json.dumps(ca['tag_distribution'], indent=4)}")


if __name__ == "__main__":
    main()
