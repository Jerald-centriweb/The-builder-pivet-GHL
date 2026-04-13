#!/usr/bin/env python3
"""
GHL Sub-Account Audit Data Collector — PreBuild Autopilot
=========================================================
Run this script locally where you have network access to the GHL API.

Usage:
    python3 ghl_audit_collector.py \
        --api-key "YOUR_PIT_KEY" \
        --location-id "YOUR_LOCATION_ID" \
        --output audit/audit_data.json

Optional — **thorough capture** (every asset the API exposes; active/inactive is
just metadata, not filtered):

    python3 ghl_audit_collector.py \
        --api-key "YOUR_PIT_KEY" \
        --location-id "YOUR_LOCATION_ID" \
        --output audit/audit_data.json \
        --deep \
        --markdown audit/GHL_THOROUGH_ACCOUNT_EXPORT.md

`--deep` calls per-ID endpoints for workflows, forms, surveys, and calendars so
Claude can see builder payloads when GHL returns them. Unknown or restricted
endpoints are stored as `{ "error": ... }` — still useful for a full picture.

Then (or alone on an existing JSON):

    python3 audit/ghl_audit_to_markdown.py audit/audit_data.json -o audit/GHL_THOROUGH_ACCOUNT_EXPORT.md

Find your Location ID: GHL → Settings → Company → Locations → copy the ID
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


def _list_from_section(data, key_candidates=("workflows", "forms", "surveys", "calendars", "templates")):
    """Normalize list responses: { "forms": [...] } or raw list."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in key_candidates:
            v = data.get(k)
            if isinstance(v, list):
                return v
    return []


def collect_all(api_key, location_id, deep=False):
    audit = {
        "collected_at": datetime.utcnow().isoformat(),
        "location_id": location_id,
        "collector_version": 2,
        "deep_mode": deep,
        "sections": {},
    }
    s = audit["sections"]
    step = [0]
    total = 25 + (1 if deep else 0)

    def tick(label):
        step[0] += 1
        print(f"[{step[0]}/{total}] {label}")

    tick("Fetching custom fields...")
    s["custom_fields"] = api_get(f"/locations/{location_id}/customFields", api_key)
    time.sleep(0.25)

    tick("Fetching contacts (sample)...")
    contacts_resp = api_post(
        "/contacts/search",
        api_key,
        {"locationId": location_id, "pageLimit": 100, "query": ""},
    )
    if isinstance(contacts_resp, dict):
        s["contacts"] = contacts_resp
    else:
        s["contacts"] = {"error": "invalid_response", "raw": str(contacts_resp)[:500]}
    time.sleep(0.25)

    tick("Fetching pipelines...")
    s["pipelines"] = api_get("/opportunities/pipelines", api_key, {"locationId": location_id})
    time.sleep(0.25)

    tick("Fetching opportunities (per pipeline sample)...")
    pipelines = s.get("pipelines", {})
    if isinstance(pipelines, dict) and "pipelines" in pipelines:
        for p in pipelines["pipelines"][:5]:
            pid = p.get("id", "")
            if not pid:
                continue
            s[f"opportunities_{pid}"] = api_get(
                "/opportunities/search",
                api_key,
                {"location_id": location_id, "pipeline_id": pid, "limit": "50"},
            )
            time.sleep(0.2)

    tick("Fetching workflows (list)...")
    s["workflows"] = api_get("/workflows/", api_key, {"locationId": location_id})
    time.sleep(0.25)

    tick("Fetching forms (list)...")
    s["forms"] = api_get("/forms/", api_key, {"locationId": location_id})
    time.sleep(0.25)

    tick("Fetching surveys (list)...")
    s["surveys"] = api_get("/surveys/", api_key, {"locationId": location_id})
    time.sleep(0.25)

    tick("Fetching calendars (list)...")
    s["calendars"] = api_get("/calendars/", api_key, {"locationId": location_id})
    time.sleep(0.25)

    tick("Fetching calendar groups...")
    s["calendar_groups"] = api_get("/calendars/groups", api_key, {"locationId": location_id})
    time.sleep(0.25)

    tick("Fetching tags...")
    s["tags"] = api_get(f"/locations/{location_id}/tags", api_key)
    time.sleep(0.25)

    tick("Fetching custom objects (multiple paths)...")
    s["custom_objects"] = {
        "get_locations_customObjects": api_get(f"/locations/{location_id}/customObjects", api_key),
        "get_objects": api_get("/objects/", api_key, {"locationId": location_id}),
        "get_locations_custom_objects_snake": api_get(f"/locations/{location_id}/custom-objects", api_key),
    }
    time.sleep(0.25)

    tick("Fetching custom values...")
    s["custom_values"] = api_get(f"/locations/{location_id}/customValues", api_key)
    time.sleep(0.25)

    tick("Fetching location (full record)...")
    s["location"] = api_get(f"/locations/{location_id}", api_key)
    time.sleep(0.25)

    tick("Fetching campaigns...")
    s["campaigns"] = api_get("/campaigns/", api_key, {"locationId": location_id})
    time.sleep(0.25)

    tick("Fetching payments orders...")
    s["payments"] = api_get("/payments/orders", api_key, {"locationId": location_id, "limit": "50"})
    time.sleep(0.25)

    tick("Fetching SMS/email templates...")
    s["templates"] = api_get(f"/locations/{location_id}/templates", api_key)
    time.sleep(0.25)

    tick("Fetching brand boards...")
    s["brand_boards"] = api_get(f"/brand-boards/{location_id}", api_key)
    time.sleep(0.25)

    tick("Fetching funnels list...")
    s["funnels"] = api_get("/funnels/funnel/list", api_key, {"locationId": location_id})
    time.sleep(0.25)

    tick("Fetching products...")
    s["products"] = api_get("/products/", api_key, {"locationId": location_id})
    time.sleep(0.25)

    tick("Fetching blogs...")
    s["blogs"] = api_get("/blogs/", api_key, {"locationId": location_id})
    time.sleep(0.25)

    tick("Fetching users for location...")
    s["users"] = api_get("/users/", api_key, {"locationId": location_id})
    time.sleep(0.25)

    tick("Fetching form submissions (recent sample)...")
    s["forms_submissions"] = api_get(
        "/forms/submissions",
        api_key,
        {"locationId": location_id, "limit": "50"},
    )
    time.sleep(0.25)

    tick("Fetching survey submissions (recent sample)...")
    s["surveys_submissions"] = api_get(
        f"/locations/{location_id}/surveys/submissions",
        api_key,
        {"limit": "50"},
    )
    time.sleep(0.25)

    tick("Fetching invoices (sample)...")
    s["invoices"] = api_get("/invoices/", api_key, {"locationId": location_id, "limit": "50"})
    time.sleep(0.25)

    tick("Fetching estimates (sample)...")
    s["estimates"] = api_get("/estimates/", api_key, {"locationId": location_id, "limit": "50"})
    time.sleep(0.25)

    if deep:
        tick("DEEP: per-workflow, form, survey, calendar payloads...")
        deep_blob = {
            "workflows_by_id": {},
            "forms_by_id": {},
            "surveys_by_id": {},
            "calendars_by_id": {},
            "templates_by_id": {},
        }
        wf_items = _list_from_section(s["workflows"], ("workflows",))
        for item in wf_items:
            if not isinstance(item, dict) or not item.get("id"):
                continue
            wid = item["id"]
            deep_blob["workflows_by_id"][str(wid)] = api_get(f"/workflows/{wid}", api_key, {"locationId": location_id})
            time.sleep(0.22)

        form_items = _list_from_section(s["forms"], ("forms",))
        for item in form_items:
            if not isinstance(item, dict) or not item.get("id"):
                continue
            fid = item["id"]
            deep_blob["forms_by_id"][str(fid)] = api_get(f"/forms/{fid}", api_key, {"locationId": location_id})
            time.sleep(0.22)

        survey_items = _list_from_section(s["surveys"], ("surveys",))
        for item in survey_items:
            if not isinstance(item, dict) or not item.get("id"):
                continue
            sid = item["id"]
            deep_blob["surveys_by_id"][str(sid)] = api_get(f"/surveys/{sid}", api_key, {"locationId": location_id})
            time.sleep(0.22)

        cal_items = _list_from_section(s["calendars"], ("calendars",))
        for item in cal_items:
            if not isinstance(item, dict) or not item.get("id"):
                continue
            cid = item["id"]
            # Single-calendar GET often works without duplicating locationId in query
            r = api_get(f"/calendars/{cid}", api_key, {"locationId": location_id})
            if isinstance(r, dict) and r.get("error") == 400:
                r = api_get(f"/calendars/{cid}", api_key, {})
            deep_blob["calendars_by_id"][str(cid)] = r
            time.sleep(0.22)

        tmpl_items = _list_from_section(s["templates"], ("templates",))
        for item in tmpl_items:
            if not isinstance(item, dict) or not item.get("id"):
                continue
            tid = item["id"]
            deep_blob["templates_by_id"][str(tid)] = api_get(
                f"/locations/{location_id}/templates/{tid}",
                api_key,
                {},
            )
            time.sleep(0.22)

        s["deep"] = deep_blob

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

    if not isinstance(contacts_data, dict) or "error" in contacts_data:
        analysis["note"] = "contacts section missing or API error — analysis skipped"
        return analysis

    contacts = contacts_data.get("contacts", [])
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
                if ("qualification_score" in str(key) or "lead_score" in str(key)) and val:
                    analysis["with_qualification_score"] += 1
                if "budget_range" in str(key) and val:
                    analysis["with_budget_range"] += 1
                if "lead_temperature" in str(key) and val:
                    analysis["with_lead_temperature"] += 1
                if "service_phase" in str(key) and val:
                    analysis["with_service_phase"] += 1
        elif isinstance(cf, dict):
            for key, val in cf.items():
                if ("qualification_score" in key or "lead_score" in key) and val:
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
    parser.add_argument("--output", default="audit_data.json", help="Output JSON path")
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Fetch per-ID workflow, form, survey, calendar, and template payloads (slower; best for Claude)",
    )
    parser.add_argument(
        "--markdown",
        metavar="PATH",
        help="After JSON is written, also write a thorough Markdown export to PATH (imports ghl_audit_to_markdown)",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("GHL Sub-Account Audit Collector — PreBuild Autopilot")
    print("=" * 60)
    print(f"API Key: {args.api_key[:10]}...{args.api_key[-4:]}")
    print(f"Location ID: {args.location_id}")
    print(f"Output: {args.output}")
    print(f"Deep mode: {args.deep}")
    print()

    audit = collect_all(args.api_key, args.location_id, deep=args.deep)

    # Run contact analysis (skip if contacts call failed)
    if "contacts" in audit["sections"]:
        csec = audit["sections"]["contacts"]
        if isinstance(csec, dict) and "error" not in csec:
            print("\nAnalyzing contact data quality...")
            audit["analysis"] = {"contacts": analyze_contacts(csec)}
        elif isinstance(csec, dict) and "error" in csec:
            audit["analysis"] = {"contacts": {"skipped": True, "reason": "contacts API error", "detail": csec}}

    with open(args.output, "w", encoding="utf-8") as f:
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
        if ca.get("skipped"):
            print("\n--- Contact Analysis: skipped (API error) ---")
        else:
            print(f"\n--- Contact Analysis ({ca.get('total_sampled', 0)} sampled) ---")
            print(f"  With qualification/lead score: {ca.get('with_qualification_score', 0)}")
            print(f"  With budget range: {ca.get('with_budget_range', 0)}")
            print(f"  With lead temperature: {ca.get('with_lead_temperature', 0)}")
            print(f"  With service phase: {ca.get('with_service_phase', 0)}")
            print(f"  With email: {ca.get('with_email', 0)}")
            print(f"  With phone: {ca.get('with_phone', 0)}")
            if ca.get("tag_distribution"):
                print(f"  Tag distribution: {json.dumps(ca['tag_distribution'], indent=4)}")

    if args.markdown:
        import os
        _here = os.path.dirname(os.path.abspath(__file__))
        if _here not in sys.path:
            sys.path.insert(0, _here)
        try:
            from ghl_audit_to_markdown import build_markdown
        except ImportError as e:
            print(f"\nWarning: could not import ghl_audit_to_markdown ({e}).")
        else:
            md = build_markdown(audit, args.output)
            with open(args.markdown, "w", encoding="utf-8") as mf:
                mf.write(md)
            print(f"\nMarkdown export written to {args.markdown}")


if __name__ == "__main__":
    main()
