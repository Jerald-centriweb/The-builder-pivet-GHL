# GHL Sub-Account Live Dump — PreBuild Autopilot

> **For Claude:** This file summarizes the live GoHighLevel sub-account state. Full JSON is in `audit/audit_data.json`. Use this for context when working on the PreBuild Autopilot spec.

**Location ID:** `cVCso4OlgGoOoXMpbxxA`  
**Collected:** March 2026  
**Source:** `audit/ghl_audit_collector.py` → `audit/audit_data.json`

---

## Location

| Field | Value |
|-------|-------|
| Name | MASTER FACTORY — PREBUILD ENGINE |
| Address | 3 ocean street, New Castle, NSW 2290, AU |
| Website | centriweb.com |
| Timezone | Pacific/Auckland |
| Contact | Jerald Immanuel, jerald@centriweb.com, +61 466 046 109 |

---

## Pipeline: Prebuild Pipeline

**ID:** `KRZs6JZq3qKVnJyvTmZh`

| Stage | Position |
|-------|----------|
| New Enquiry | 0 |
| Survey Completed | 1 |
| Qualified - Hot | 2 |
| Nurture - Warm | 3 |
| Intro Call Booked | 4 |
| Proposal Sent | 5 |
| Engaged | 6 |
| Delivered | 7 |
| Won | 8 |
| Not Now | 9 |
| Lost | 10 |

---

## Workflows (10 total, all draft)

| Name | ID | Status |
|------|-----|--------|
| WF-01-Speed-to-Lead | 9f2b93e5-9662-4749-b9d0-6b40c5c1b6a2 | draft |
| WF-02-Survey-Reminders | 17891e4d-c278-4895-a3f7-357c3178fb6b | draft |
| WF-03-Scoring-and-Routing | d52e3147-c48a-44d3-af52-6680e5573b47 | draft |
| WF-04-Education-Sequence | bbfe1ca0-14a6-4452-baea-7128661642b4 | draft |
| WF-05-Booking-Flow | 5408bfe2-e1c0-4220-aae5-81c673113183 | draft |
| WF-06-Proposal-and-Payment | 2fc5067c-be83-46d3-9a8c-550ce02e4a4e | draft |
| WF-09-Stage-Notifications | bd849e9f-9361-4526-a3b6-98b976c85d17 | draft |
| WF-10-Stale-Lead-Reminders | c7241790-4b89-4995-b7fa-a1dba97d24db | draft |
| WF-11-Partner-Notifications | d06709cc-f1fc-4736-8f5b-391682f4c1cc | draft |
| WF-12-Review-Request | 1c1a6318-4ff8-41f1-9a49-ea2176c9576f | draft |

---

## Custom Fields (15)

| Name | Type | Purpose |
|------|------|---------|
| cf_finance_status | SINGLE_OPTIONS | Finance approval status |
| cf_budget_how | SINGLE_OPTIONS | How budget figure was arrived at |
| cf_partner_email | TEXT | Partner email |
| cf_open_to_fee | SINGLE_OPTIONS | Open to paid preconstruction |
| cf_lead_score | NUMERICAL | Lead score |
| cf_service_phase | SINGLE_OPTIONS | Phase 1 / Phase 2 |
| cf_contact_role | SINGLE_OPTIONS | Primary / Partner |
| cf_budget_range | SINGLE_OPTIONS | Budget bands |
| cf_partner_phone | PHONE | Partner phone |
| cf_land_status | SINGLE_OPTIONS | Land ownership status |
| cf_household_id | TEXT | Household grouping |
| cf_project_type | SINGLE_OPTIONS | New build, knockdown, etc. |
| cf_partner_name | TEXT | Partner name |
| cf_timeline | SINGLE_OPTIONS | Construction start timeline |
| cf_suburb | TEXT | Suburb |

---

## Custom Values (11)

| Name | Use |
|------|-----|
| meeting_location | Meeting location |
| calendar_link | `{{ custom_values.calendar_link }}` |
| service_2_fee | Phase 2 fee |
| builder_email | Builder email |
| refund_policy | Refund policy text |
| service_1_name | Phase 1 service name |
| service_2_name | Phase 2 service name |
| builder_logo_url | Builder logo |
| builder_phone | Builder phone |
| service_1_fee | Phase 1 fee |
| builder_name | Builder name |

---

## Forms (3)

| Name | ID |
|------|-----|
| FRM-Lead-Intake | x1jLoeSHaBKZXm8Gm0gu |
| Book a demo | GbemuaflhwNAilmnqgEf |
| SRV-Qualification-Survey | ugnDa7Hh1lQNb52GUypu |

---

## Surveys (1)

| Name | ID |
|------|-----|
| SRV-Qualification-Survey | J30zhHTAz8daVE7wZP7P |

---

## Calendars (1)

| Name | ID | Type |
|------|-----|------|
| CAL-Intro-Call | b4uPmlCoYV7J96XJZBsD | round_robin |

---

## Tags (5)

- lead-cold, lead-hot, lead-warm  
- role-partner, role-primary  

---

## Templates (5 SMS)

| Name | Type |
|------|------|
| SMS-BOOK-Confirmation | sms |
| SMS-BOOK-Reminder-24hr | sms |
| SMS-PROP-Agreement-Sent | sms |
| SMS-STL-Survey-Link | sms |
| SMS-STL-Survey-Reminder | sms |

*(Template bodies in audit_data.json — some may be placeholder)*

---

## Known Gaps (from collector)

- **Contacts:** 0 (subaccount may have no contacts yet, or search returns empty)
- **Custom objects:** 404 (endpoint may differ)
- **Payments:** 403 (API key may need payments.readonly scope)
- **Campaigns:** 0

---

## How to Refresh This Dump

```bash
cd "/path/to/The-builder-pivet-GHL"
python3 audit/ghl_audit_collector.py \
  --api-key "YOUR_PIT_KEY" \
  --location-id "cVCso4OlgGoOoXMpbxxA" \
  --output audit/audit_data.json
```

Then regenerate this summary or use `audit_data.json` directly.

---

## Related: Written Content

**`audit/GHL_WRITTEN_CONTENT_DUMP.md`** — Every piece of written content: SMS/email templates, survey questions, form labels, inline copy. The GHL API doesn't return this; the dump is extracted from the spec.

---

## GoHighLevel MCP

For live API access from Claude/Cursor, use the [GoHighLevel-MCP](https://github.com/mastanley13/GoHighLevel-MCP) server. It provides 269+ tools for contacts, workflows, opportunities, templates, etc. Configure in `~/.cursor/mcp.json` with your API key and Location ID.
