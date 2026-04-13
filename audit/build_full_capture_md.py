#!/usr/bin/env python3
"""Emit audit/GHL_PREBUILD_DEMO_FULL_CAPTURE.md — run after updating MCP_* blobs below."""
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
AUDIT_JSON = ROOT / "audit_data.json"
OUT = ROOT / "GHL_PREBUILD_DEMO_FULL_CAPTURE.md"

# --- Paste fresh MCP `data` payloads here when re-running capture ---
MCP_LOCATION = {
    "location": {
        "id": "cVCso4OlgGoOoXMpbxxA",
        "name": "MASTER FACTORY — PREBUILD ENGINE",
        "address": "3 ocean street",
        "city": "New Castle",
        "state": "NSW",
        "country": "AU",
        "postalCode": "2290",
        "website": "centriweb.com",
        "timezone": "Pacific/Auckland",
        "firstName": "Jerald",
        "lastName": "Immanuel",
        "email": "jerald@centriweb.com",
        "phone": "+61 466 046 109",
        "logoUrl": "",
        "currency": "",
        "business": {
            "name": "MASTER FACTORY — PREBUILD ENGINE",
            "address": "3 ocean street",
            "city": "New Castle",
            "state": "NSW",
            "country": "AU",
            "postalCode": "2290",
            "website": "centriweb.com",
            "timezone": "Pacific/Auckland",
            "email": "",
        },
        "settings": {"allowDuplicateContact": False, "allowDuplicateOpportunity": False},
    }
}

# Summary rows from live `locations_get-custom-fields` (add picklist counts in col 4)
MCP_CF_ROWS = [
    ("cf_prelim_fee_s2", "contact.cf_prelim_fee_s2", "NUMERICAL", "—"),
    ("Business Name", "contact.business_name", "TEXT", "—"),
    ("cf_lost_reason", "contact.cf_lost_reason", "TEXT", "—"),
    ("cf_finance_status", "contact.cf_finance_status", "SINGLE_OPTIONS", "5"),
    ("How did you arrive at that budget figure?", "contact.cf_budget_how", "SINGLE_OPTIONS", "5"),
    ("How did you hear about us?", "contact.cf_how_heard", "SINGLE_OPTIONS", "5"),
    ("State", "contact.state_dropdown", "SINGLE_OPTIONS", "5"),
    ("Engagement Phase", "contact.contactcf_engagement_phase", "SINGLE_OPTIONS", "2"),
    ("cf_partner_email", "contact.cf_partner_email", "TEXT", "—"),
    ("cf_lead_temperature", "contact.cf_lead_temperature", "SINGLE_OPTIONS", "3"),
    ("cf_finance_contingency", "contact.cf_finance_contingency", "SINGLE_OPTIONS", "5"),
    ("cf_open_to_fee (long label)", "contact.cf_open_to_fee", "SINGLE_OPTIONS", "4"),
    ("cf_council_contingency", "contact.cf_council_contingency", "SINGLE_OPTIONS", "5"),
    ("What are the two most important things…", "contact.cf_top_priorities", "MULTIPLE_OPTIONS", "6"),
    ("cf_land_contingency", "contact.cf_land_contingency", "SINGLE_OPTIONS", "4"),
    ("cf_delivery_status", "contact.cf_delivery_status", "SINGLE_OPTIONS", "5"),
    ("Is there anything else we should know before the call?", "contact.cf_precall_additional_notes", "TEXT", "—"),
    ("cf_delivery_due_date", "contact.cf_delivery_due_date", "DATE", "—"),
    ("cf_design_contingency", "contact.cf_design_contingency", "SINGLE_OPTIONS", "5"),
    ("cf_lead_score", "contact.cf_lead_score", "NUMERICAL", "—"),
    ("cf_service_phase", "contact.cf_service_phase", "SINGLE_OPTIONS", "2"),
    ("What's your #1 priority in a builder?", "contact.cf_top_priority_1", "SINGLE_OPTIONS", "5"),
    ("cf_prelim_fee_s3", "contact.cf_prelim_fee_s3", "NUMERICAL", "—"),
    ("Are you the main decision-maker…", "contact.cf_decision_maker", "RADIO", "3"),
    ("What's the most important thing on our call?", "contact.cf_precall_main_topic", "TEXT", "—"),
    ("cf_contact_role", "contact.cf_contact_role", "SINGLE_OPTIONS", "2"),
    ("cf_budget_range", "contact.cf_budget_range", "SINGLE_OPTIONS", "7"),
    ("cf_delivery_completed_date", "contact.cf_delivery_completed_date", "DATE", "—"),
    ("How would you prefer we stay in touch?", "contact.cf_communication_pref", "RADIO", "4"),
    ("cf_qualification_score", "contact.cf_qualification_score", "NUMERICAL", "—"),
    ("Do you have plans or drawings?", "contact.cf_precall_has_plans", "RADIO", "3"),
    ("cf_delivery_start_date", "contact.cf_delivery_start_date", "DATE", "—"),
    ("cf_partner_phone", "contact.cf_partner_phone", "PHONE", "—"),
    ("Decline Sent Date", "contact.cf_decline_sent_date", "DATE", "—"),
    ("Have you spoken to any other builders?", "contact.cf_other_builders", "RADIO", "3"),
    ("cf_land_status", "contact.cf_land_status", "SINGLE_OPTIONS", "4"),
    ("cf_household_id", "contact.cf_household_id", "TEXT", "—"),
    ("cf_project_type", "contact.cf_project_type", "SINGLE_OPTIONS", "5"),
    ("cf_partner_name", "contact.cf_partner_name", "TEXT", "—"),
    ("Have you received any other quotes?", "contact.cf_precall_other_quotes", "RADIO", "2"),
    ("cf_timeline", "contact.cf_timeline", "SINGLE_OPTIONS", "5"),
    ("cf_suburb", "contact.cf_suburb", "TEXT", "—"),
    ("What's your #2 priority?", "contact.cf_top_priority_2", "SINGLE_OPTIONS", "5"),
    ("cf_estimator_status", "contact.cf_estimator_status", "SINGLE_OPTIONS", "5"),
    ("Is there a specific timeline driving your project?", "contact.cf_precall_timeline_driver", "TEXT", "—"),
]

MCP_CONTACTS_SUMMARY = [
    ("rak4VWhq1U6JRdZJ3qO7", "trixy testing", "FRM-Lead-Intake", "form-lead-intake-completed, survey-completed, lead-hot"),
    ("jKFMsgKs6eDnjERcu2iH", "karen white", "—", "—"),
    ("EhNjYGOZwzy32fxX2znO", "steve harris", "—", "—"),
    ("R9eeWJFGvyZBWWfECPsA", "rachel cooper", "—", "—"),
    ("m8nuGqQRuzkLEcPGwvhP", "mark anderson", "—", "—"),
    ("2FSHZmIAub2zJmyZ91uA", "lisa taylor", "—", "—"),
    ("0dhewvmcmLqP6ZArqxT7", "david brown", "—", "—"),
    ("oGhQ70aLAPCtYPF2mLYN", "emily chen", "—", "—"),
    ("2jcgipjVLeYzuWovyj8p", "james wilson", "—", "—"),
    ("RDbX3pqB1LG4MxF2aDBF", "trixy macaraeg", "—", "—"),
    ("OWmlyS0bGRvNJZPb9lmJ", "tom mitchell", "—", "—"),
    ("wDGAd6lYnAJrQ3zHiuKw", "sarah johnson", "—", "—"),
    ("u7thPj7XGpKCvE83oMSl", "test test", "FRM-Lead-Intake", "form-lead-intake-completed"),
]

MCP_OPPORTUNITIES = [
    {
        "id": "Ki59EK9y3l672pjaLpc8",
        "name": "Trixy Testing",
        "pipelineStageId": "8883cbd1-098e-4829-bfa2-1bd558653e28",
        "stageName": "Qualified - Hot",
        "status": "open",
        "contactId": "rak4VWhq1U6JRdZJ3qO7",
        "source": "FRM-Lead-Intake",
    },
    {
        "id": "3E9nYtTtmNvbq1Ne243v",
        "name": "Trixy Macaraeg",
        "pipelineStageId": "333e7953-2cea-472e-875e-33d14dd286a8",
        "stageName": "Nurture - Warm",
        "status": "open",
        "contactId": "RDbX3pqB1LG4MxF2aDBF",
        "source": None,
    },
    {
        "id": "UEsbmTWDYm1u2dQq1qpG",
        "name": "TEST TEST",
        "pipelineStageId": "66dfc3ca-9268-4210-8b5e-4a1e4d6e40b7",
        "stageName": "New Enquiry",
        "status": "open",
        "contactId": "u7thPj7XGpKCvE83oMSl",
        "source": "FRM-Lead-Intake",
    },
]

MCP_CONVERSATIONS = [
    {"id": "eSy7c8ztSQi44quZBp3c", "contactId": "RDbX3pqB1LG4MxF2aDBF", "lastMessageType": "TYPE_EMAIL", "unreadCount": 0},
    {"id": "yzlkhm8MIpGfj5i8kQal", "contactId": "rak4VWhq1U6JRdZJ3qO7", "lastMessageType": "TYPE_EMAIL", "unreadCount": 0},
    {"id": "LXLPzV6na258qwqpxuL3", "contactId": "u7thPj7XGpKCvE83oMSl", "lastMessageType": "TYPE_NO_SHOW", "unreadCount": 0},
]

EMAIL_BUILDERS = [
    ("ET-PROP: Unsigned Reminder", "69cda3631af4b43499b82feb", "builder", "—"),
    ("Phase 1 Agreement Email", "69cda5a039671024b5878bd7", "builder", "—"),
    ("Phase 1 Agreement Email (dup)", "69cda690c1eecde4acd267b4", "builder", "—"),
    ("1. Speed-to-Lead + Survey Emails", "69cbcdd39f2cc51cf68ebf18", "folder", "3"),
    ("2. Proposal, Payment + Portal Emails", "69cbcde59baa1b24edf06525", "folder", "4"),
    ("4. Education Sequence", "69cba80744ec869b8d66fde6", "folder", "6"),
    ("3. Nurture Re-engagement", "69cbce0044ec8692cd68ba34", "folder", "3"),
    ("5. Post-Payment Delivery (WF-13)", "69cbce0841aaf0c198d5b3b8", "folder", "13"),
    ("6. ET-BOOK-PRECALL", "69cbce119baa1b63a8f06838", "folder", "1"),
    ("8. ET-NFE-NEXT-STEPS", "69cbce1daed86939bcf3ecd5", "folder", "1"),
    ("7. NFE-BUILDER-INTRO", "69cbce1898caf347567e98f2", "folder", "1"),
]


def main():
    audit = json.loads(AUDIT_JSON.read_text(encoding="utf-8"))
    sec = audit.get("sections", {})
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = []
    lines.append("# PreBuild Factory — full live capture (MCP + REST)\n\n")
    lines.append(f"> **Generated (UTC):** {ts}  \n")
    lines.append("> **Location ID:** `cVCso4OlgGoOoXMpbxxA`  \n")
    lines.append(
        "> **Sources:** Cursor MCP **`user-ghl-prebuild-demo`** (live API) + "
        "`audit/audit_data.json` for workflows/forms/survey/SMS/calendar list not in MCP toolset.  \n"
    )
    lines.append(
        "> **Workflow internals / form fields:** run `python3 audit/ghl_audit_collector.py --deep …` and/or GHL UI.  \n\n"
    )
    lines.append("---\n\n")

    lines.append("## A. MCP — `locations_get-location`\n\n```json\n")
    lines.append(json.dumps(MCP_LOCATION, indent=2))
    lines.append("\n```\n\n")

    lines.append("## B. MCP — `locations_get-custom-fields` (model=all)\n\n")
    lines.append("| GHL name | fieldKey | Data type | Picklist size |\n|---|---|---|---|\n")
    for name, fk, dt, pc in MCP_CF_ROWS:
        lines.append(f"| {name} | `{fk}` | {dt} | {pc} |\n")
    lines.append("\n*Full picklists: call MCP or GHL UI.*\n\n")

    lines.append("## C. MCP — `opportunities_get-pipelines`\n\n```json\n")
    lines.append(json.dumps(sec.get("pipelines"), indent=2)[:12000])
    lines.append("\n```\n\n")

    lines.append("## D. MCP — `contacts_get-contacts` (limit 100)\n\n")
    lines.append("**meta.total:** 13. *PII: real emails/phones exist on records — table omits email/phone; fetch via GHL/MCP as needed.*\n\n")
    lines.append("| Contact ID | Name | source | tags (comma) |\n|---|---|---|---|\n")
    for cid, nm, src, tg in MCP_CONTACTS_SUMMARY:
        lines.append(f"| `{cid}` | {nm} | {src or '—'} | {tg or '—'} |\n")
    lines.append("\n")

    lines.append("## E. MCP — `opportunities_search-opportunity` (Prebuild Pipeline)\n\n```json\n")
    lines.append(json.dumps({"meta": {"total": 3}, "opportunities": MCP_OPPORTUNITIES}, indent=2))
    lines.append("\n```\n\n")

    lines.append("## F. MCP — `conversations_search-conversation` (summary)\n\n```json\n")
    lines.append(json.dumps({"total": 3, "conversations": MCP_CONVERSATIONS}, indent=2))
    lines.append("\n```\n\n")

    lines.append("## G. MCP — `calendars_get-calendar-events` (CAL-Intro-Call, 2024–2027)\n\n")
    lines.append("Returned **0** events for range `1704067200000`–`1893456000000`.\n\n")

    lines.append("## H. MCP — `payments_list-transactions`\n\n**0** transactions (empty `data`).\n\n")

    lines.append("## I. MCP — blogs + categories + authors\n\n")
    lines.append("- `blogs_get-blogs`: **0** sites.  \n")
    lines.append("- `blogs_get-all-categories-by-location`: **0** categories.  \n")
    lines.append("- `blogs_get-all-blog-authors-by-location`: **0** authors.  \n\n")

    lines.append("## J. MCP — `emails_fetch-template` (builder + folders)\n\n")
    lines.append("| Name | ID | Type | childCount |\n|---|---|---|---|\n")
    for n, i, t, c in EMAIL_BUILDERS:
        lines.append(f"| {n} | `{i}` | {t} | {c} |\n")
    lines.append("\n")

    lines.append("## K. MCP — `social-media-posting_get-account`\n\n")
    lines.append("`accounts`: **[]**, `groups`: **[]**.\n\n")

    lines.append("## L. REST — `audit/audit_data.json` (collector snapshot)\n\n")
    rest = {
        "audit_collected_at": audit.get("collected_at"),
        "workflows": sec.get("workflows", {}).get("workflows"),
        "forms": sec.get("forms", {}).get("forms"),
        "surveys": sec.get("surveys", {}).get("surveys"),
        "tags": sec.get("tags", {}).get("tags"),
        "custom_value_names": [x.get("name") for x in sec.get("custom_values", {}).get("customValues", [])],
        "sms_templates": sec.get("templates", {}).get("templates"),
        "calendar": sec.get("calendars", {}).get("calendars", [{}])[0],
    }
    lines.append("```json\n")
    lines.append(json.dumps(rest, indent=2)[:28000])
    lines.append("\n```\n\n")

    lines.append("## M. MCP tool coverage note\n\n")
    lines.append(
        "The **`user-ghl-prebuild-demo`** server exposes ~36 tools (contacts, pipelines, blogs, calendars events, "
        "conversations, payments, email builder list, social). It does **not** include workflow definition export, "
        "form schema, or survey schema — use **`ghl_audit_collector.py --deep`** for those."
    )
    lines.append("\n")

    OUT.write_text("".join(lines), encoding="utf-8")
    print("Wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
