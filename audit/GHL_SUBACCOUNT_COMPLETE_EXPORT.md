# GHL Subaccount Complete Export — Cross-Platform Reference

> **Purpose:** A single entry point for any platform (AI, docs, migration tools, other CRMs) to fully understand the PreBuild Autopilot subaccount **without logging into GHL**. This document indexes everything we've captured and what requires manual capture.

---

## Export Index

| File | Content | API Source |
|------|---------|------------|
| `audit/audit_data.json` | Pipelines, workflows, custom fields, tags, forms, surveys, calendars, templates, location, brand boards, funnels | ✅ API |
| `audit/GHL_SUBACCOUNT_DUMP.md` | Human-readable structure summary | From audit_data.json |
| `audit/GHL_WRITTEN_CONTENT_DUMP.md` | Every SMS/email template, survey question, form label, inline copy | Spec (API returns empty) |
| `audit/GHL_BRANDING_AND_UI_SPEC.md` | Schema for colors, fonts, logos, styling + manual capture checklist | Manual (API limited) |
| `audit/ghl_branding_captured.json` | *(Create after manual capture)* Actual color/font values | Manual |
| `PREBUILD_AUTOPILOT_CONTEXT.md` | Full system spec, workflows, Custom Values registry | Spec |

---

## What's Fully Captured (No GHL Login Needed)

- **Structure:** Pipelines, stages, workflows, forms, surveys, calendars, tags
- **Data model:** Custom fields (names, types, options), Custom Values (keys)
- **Written content:** All template copy, survey questions, labels, inline messages
- **Location:** Name, address, contact, settings
- **Brand Boards:** Structure (if any) — currently empty
- **Funnels:** List (if API returns them)

---

## What Requires Manual Capture

| Asset | Why | Where in GHL |
|-------|-----|--------------|
| **Colors** | Brand Boards empty; forms/surveys 401 | Marketing → Brand Boards; Form/Survey Style |
| **Fonts** | Not in API | Funnels → Design; Forms; Email Builder |
| **Custom Value actual values** | API returns keys only, not values | Settings → Custom Values |
| **Logo URL** | `location.logoUrl` empty | Settings → Company; or Custom Value `builder_logo_url` |
| **Form/Survey styling** | 401 on form/survey detail | Marketing → Forms/Surveys → Design |
| **Email template HTML** | API returns empty body | Marketing → Email Templates |
| **Portal page design** | No API | Memberships → Portal |

---

## Recommended Workflow for Full Export

1. **Run audit collector** (gets all API data):
   ```bash
   python3 audit/ghl_audit_collector.py --api-key "YOUR_KEY" --location-id "YOUR_ID" --output audit/audit_data.json
   ```

2. **Follow branding capture checklist** in `audit/GHL_BRANDING_AND_UI_SPEC.md`

3. **Create `audit/ghl_branding_captured.json`** with colors, fonts, logo URLs

4. **Optional: Add branding Custom Values** in GHL (`primary_color`, `heading_font`, etc.) so future exports can reference them

---

## For Other Platforms

To fully understand this subaccount:

1. Read `audit/audit_data.json` for structure and metadata
2. Read `audit/GHL_WRITTEN_CONTENT_DUMP.md` for all copy
3. Read `audit/GHL_BRANDING_AND_UI_SPEC.md` for visual schema
4. If `audit/ghl_branding_captured.json` exists, read it for actual colors/fonts
5. Read `PREBUILD_AUTOPILOT_CONTEXT.md` for business logic and rules

---

## API Limitations Summary

| Endpoint | Status | Notes |
|----------|--------|-------|
| Brand Boards | 200, empty | No boards configured |
| Forms detail | 401 | Route not supported |
| Surveys detail | 401 | Route not supported |
| Template body | 200, empty | Returns `"  "` |
| Custom Values | 200, keys only | No `value` field in response |
| Funnels | TBD | Added to collector |
