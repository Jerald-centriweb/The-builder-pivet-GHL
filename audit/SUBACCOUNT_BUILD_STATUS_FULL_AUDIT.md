# PreBuild Autopilot — Full Sub-Account Build Status Audit

> **Purpose:** Single handoff document for Claude Code (or any assistant) to understand **where the Factory sub-account stands vs the spec**, what is verified from the API, what must be verified manually, and **prioritised next steps**.  
> **Data snapshot:** `audit/audit_data.json` collected **2026-03-14T01:24:30Z** (Location ID in that file). Refresh with `audit/ghl_audit_collector.py` before major decisions.  
> **Spec source of truth:** `PREBUILD_AUTOPILOT_CONTEXT.md`  
> **Naming locks:** Pipeline `PreBuild Pipeline` (live: `Prebuild Pipeline`), workflows `WF-[##]-[Description]`, templates `ET-` / `SMS-`, custom fields `cf_snake_case`.

---

## Executive summary

| Area | Verdict |
|------|---------|
| **Factory shell** | Location, pipeline, core workflow *names*, forms, survey, calendar object, and a subset of custom fields/custom values exist. |
| **Go-live readiness** | **Not production-ready.** All sampled workflows are **draft**; intro calendar is **inactive**; API cannot confirm template bodies, payments, or workflow internals. |
| **Highest risks** | (1) **WF-03** — scoring + routing must match spec and any external scorer; field keys must align with `wf03_scoring_engine.py`. (2) **Pipeline stage names** in GHL differ from spec labels — any workflow “move to stage” actions must use **exact** live strings. (3) **Custom field / tag gaps** vs Section 5 of the spec. |
| **Demo / sell** | No contacts in sampled data; end-to-end journey not proven in this export. |

---

## 1. Location & account context

| Item | Live (from `audit_data.json`) |
|------|-------------------------------|
| **Location name** | MASTER FACTORY — PREBUILD ENGINE |
| **Location ID** | `cVCso4OlgGoOoXMpbxxA` (from collector output) |
| **Address** | 3 ocean street, New Castle, NSW 2290, AU |
| **Website** | centriweb.com |
| **Timezone** | Pacific/Auckland *(verify vs Australian builder default)* |
| **Logo URL** | Empty in API response |
| **Currency** | Empty in API response |
| **Contacts (search sample)** | **0** total returned |
| **Opportunities (main pipeline sample)** | **0** |

**Implication:** The account reads as an empty Factory — good for a clean template, but **no behavioural proof** (scoring, stage moves, sends) from live traffic in this dataset.

---

## 2. Pipeline — spec vs live

**Spec (`PREBUILD_AUTOPILOT_CONTEXT.md` §4):** Pipeline name **`PreBuild Pipeline`**; stages: New Enquiry → **Qualified** → **Nurture** → **Discovery Booked** → Proposal Sent → Engaged → Delivered → Won; non-active: Not Now, Lost.

**Live (`audit_data.json`):** Pipeline name **`Prebuild Pipeline`** (ID `KRZs6JZq3qKVnJyvTmZh`). Stages:

| # | Live stage name | Spec equivalent | Notes |
|---|-----------------|-----------------|--------|
| 0 | New Enquiry | New Enquiry | Aligns |
| 1 | **Survey Completed** | *(not a separate named stage in spec table)* | Extra stage — workflows must be checked so they do not expect “survey completed” as only a tag |
| 2 | **Qualified - Hot** | **Qualified** | **String mismatch** — any action “move to Qualified” may fail if GHL requires exact name |
| 3 | **Nurture - Warm** | **Nurture** | **String mismatch** |
| 4 | **Intro Call Booked** | **Discovery Booked** | **String mismatch** |
| 5 | Proposal Sent | Proposal Sent | Aligns |
| 6 | Engaged | Engaged | Aligns |
| 7 | Delivered | Delivered | Aligns |
| 8 | Won | Won | Aligns |
| 9 | Not Now | Not Now | Aligns |
| 10 | Lost | Lost | Aligns |

**Action for next steps:** Search every workflow for **Move Opportunity / Change Pipeline Stage** actions and confirm targets match **live** stage names above, not prose from the spec alone.

---

## 3. Workflows — inventory vs spec

**Spec:** WF-01 … WF-12 with **WF-07 removed** (merged into WF-06). Expect **11** active workflow *slots* (WF-08 Portal Welcome, WF-11 Builder Internal Tasks per spec naming).

**Live (10 workflows, all `status: draft`):**

| Live name | ID | Version | Spec note |
|-----------|-----|---------|-----------|
| WF-01-Speed-to-Lead | `9f2b93e5-9662-4749-b9d0-6b40c5c1b6a2` | 2 | Core |
| WF-02-Survey-Reminders | `17891e4d-c278-4895-a3f7-357c3178fb6b` | 2 | Core |
| WF-03-Scoring-and-Routing | `d52e3147-c48a-44d3-af52-6680e5573b47` | **95** | Heavily iterated — verify logic + external HTTP |
| WF-04-Education-Sequence | `bbfe1ca0-14a6-4452-baea-7128661642b4` | 2 | Core |
| WF-05-Booking-Flow | `5408bfe2-e1c0-4220-aae5-81c673113183` | 2 | Core |
| WF-06-Proposal-and-Payment | `2fc5067c-be83-46d3-9a8c-550ce02e4a4e` | 2 | Core |
| WF-09-Stage-Notifications | `bd849e9f-9361-4526-a3b6-98b976c85d17` | 2 | Core |
| WF-10-Stale-Lead-Reminders | `c7241790-4b89-4995-b7fa-a1dba97d24db` | 2 | Core |
| WF-11-Partner-Notifications | `d06709cc-f1fc-4736-8f5b-391682f4c1cc` | 2 | Spec §7 names this **WF-11: Builder Internal Tasks** — **verify** this is intentional rename vs missing builder-task workflow |
| WF-12-Review-Request | `1c1a6318-4ff8-41f1-9a49-ea2176c9576f` | 2 | Core |

**Missing from workflow list API response:**

| Spec workflow | Risk |
|---------------|------|
| **WF-08 — Portal Welcome** | **Not listed** — confirm in GHL UI under another name, nested, or not built |
| **WF-07** | Must remain **absent** (merged into WF-06) |

**Critical:** GHL **GET `/workflows/`** returns metadata only (name, id, status, version). **Triggers, branches, HTTP calls, and template wiring are not in `audit_data.json`.** Manual UI review or MCP deep tools are required for “what happens inside” each workflow.

**All workflows are draft:** Nothing in this export proves automations **publish** or fire on real events.

---

## 4. Custom fields — live vs spec (Section 5)

**Live count:** 15 custom fields (API). Several use **long question text as the GHL “name”** instead of short `cf_*` labels — acceptable in GHL but harder to audit at a glance.

### Present in live (by `fieldKey` / name)

| fieldKey / identifier | Notes |
|-------------------------|--------|
| `contact.cf_finance_status` | Aligns with financing concept; spec uses `cf_financing_status` — **key name differs** |
| `contact.cf_budget_how` | Extra vs core spec table (useful) |
| `contact.cf_partner_email` | Spec |
| `contact.cf_open_to_fee` | Spec |
| `contact.cf_lead_score` | Spec expects **`cf_qualification_score`** for WF-03 — **critical naming mismatch** if workflows/engine write to different keys |
| `contact.cf_service_phase` | Present; picklist values are **“Phase 1 - Budget Assessment” / “Phase 2 - Detailed Estimate”** — spec also describes `not_started` / `phase_1` / `phase_2` / `complete` — **verify** WF-06 branches match **actual** option strings |
| `contact.cf_contact_role` | Related to partner handling |
| `contact.cf_budget_range` | Spec |
| `contact.cf_partner_phone` | Spec |
| `contact.cf_land_status` | Spec |
| `contact.cf_household_id` | Spec / household |
| `contact.cf_project_type` | Spec |
| `contact.cf_partner_name` | Spec |
| `contact.cf_timeline` | Spec (option wording may differ from scorer — verify) |
| `contact.cf_suburb` | Extra vs minimal spec table |

### Missing or not seen in live API list (spec expects)

| Spec key | Used for |
|----------|----------|
| `cf_qualification_score` | Primary score field in spec + checklist |
| `cf_lead_temperature` | Reporting / branching |
| `cf_site_address` | Proposal merge |
| `cf_decision_maker` | Scoring rubric |
| `cf_communication_preference` | Spec |
| `cf_service_1_fee`, `cf_service_2_fee` | Stripe / proposal amounts per contact |
| `cf_lost_reason` | Lost stage |
| `cf_how_heard` | Attribution |
| `cf_design_status`, `cf_prior_quotes`, `cf_site_challenges` | Scoring in `wf03_scoring_engine.py` |
| `cf_additional_notes` | Free text |

**Action:** Reconcile **`cf_lead_score` vs `cf_qualification_score`** across survey mappings, WF-03, and `wf03_scoring_engine.py` (`update_ghl_contact` payload). Align or migrate before trusting scores.

---

## 5. Custom values — live keys vs spec (Section 6)

**API behaviour:** List returns **keys / fieldKey**; **values are not audited here** from JSON (confirm in GHL: no placeholders).

**Present (11 keys in export):**  
`meeting_location`, `calendar_link`, `service_2_fee`, `builder_email`, `refund_policy`, `service_1_name`, `service_2_name`, `builder_logo_url`, `builder_phone`, `service_1_fee`, `builder_name`.

**Spec-required / common — verify existence and populated values in GHL UI:**

| Typical spec key | Status in key list |
|------------------|--------------------|
| `fee_structure` | **Not in exported list** — **critical** for two_tier / single_tier / no_fee |
| `survey_link` | **Not in exported list** |
| `google_review_link` | **Not in exported list** |
| `portal_link` / `portal_url` | **Not in exported list** |
| `builder_abn`, `service_*_fee_label`, `current_service_fee`, etc. | Verify per §6 |

---

## 6. Tags — live vs spec (Section 5)

**Live (5 tags):** `lead-cold`, `lead-hot`, `lead-warm`, `role-partner`, `role-primary`.

**Spec additionally expects (non-exhaustive):**  
`survey-pending`, `survey-completed`, `survey-abandoned`, `call-booked`, `proposal-sent`, `payment-received`, `portal-active`, `review-requested`, `stage-won`, `stage-lost`, `fee-tier-single`, `fee-tier-two`, `fee-tier-none`, `payment-manual`.

**Implication:** Tags may be created on first use by workflows, or workflows may reference tags that **do not exist yet** — confirm in GHL.

---

## 7. Forms, survey, calendar

| Asset | Live |
|-------|------|
| **Forms** | `FRM-Lead-Intake`, `Book a demo`, `SRV-Qualification-Survey` (IDs in `audit_data.json`) |
| **Survey** | `SRV-Qualification-Survey` — ID `J30zhHTAz8daVE7wZP7P` |
| **Calendar** | `CAL-Intro-Call` — ID `b4uPmlCoYV7J96XJZBsD`, **round robin**, **`isActive`: false** |

**Critical:** **`isActive: false`** means booking may be blocked or hidden until activated in GHL.

**Survey field mapping:** Not available via this audit JSON. Cross-check every question → custom field against `audit/SRV_QUALIFICATION_FULL_SPEC.md` and `audit/wf03_scoring_engine.py` option strings.

---

## 8. Templates (API limitations)

**Live SMS templates (5):**  
`SMS-BOOK-Confirmation`, `SMS-BOOK-Reminder-24hr`, `SMS-PROP-Agreement-Sent`, `SMS-STL-Survey-Link`, `SMS-STL-Survey-Reminder`.

**API template `body`:** Returned as **whitespace / empty** in export — do **not** assume blank; open in GHL UI.

**Spec gap (from project open items):** **`ET-BOOK-Confirmation`** — copy in spec; confirm built and linked in WF-05.

**Naming:** Spec uses names like `SMS-STL-Welcome`, `ET-STL-01-Welcome` — **live names differ** (`SMS-STL-Survey-Link`, etc.). Workflows must reference **actual** template IDs/names in GHL.

**Compliance:** Every SMS must end with **“Reply STOP to opt out”** (verify in UI).

**Email templates:** Not enumerated in this `audit_data.json` slice the same way as SMS; confirm full **ET-*** set from spec §8 exists.

---

## 9. Other API sections (from collector)

| Section | Result |
|---------|--------|
| **Campaigns** | Empty list |
| **Payments** | **403 Forbidden** — scope or product not exposed to this token |
| **Custom objects** | **404** on collected path — endpoint/version may differ |
| **Brand boards** | 0 |
| **Funnels** | 0 |

---

## 10. External systems & code (not GHL UI, but build-critical)

| Item | Location | Notes |
|------|----------|--------|
| **Scoring engine** | `audit/wf03_scoring_engine.py` | Deploy to n8n / Cloud Function / Lambda; wire webhook from GHL on survey submit |
| **Known code issues** | `audit/DEEP_SPEC_ANALYSIS.md` | Includes MAX_RAW_SCORE / unreachable branches — **read before production** |
| **n8n outreach** | Spec §19 | Separate cold outreach; known bugs — do not conflate with core GHL funnel |

---

## 11. Milestone checklist (mapped to your spec)

| Milestone | Evidence in this audit | Likely next action |
|-----------|-------------------------|-------------------|
| **M1 — Factory baseline** | Pipeline + many assets exist | Resolve naming: pipeline casing; stage strings; template names |
| **M2 — Core workflows live** | 10 workflows exist, **all draft**; WF-08 missing from list | Publish after QA; build/locate WF-08; verify WF-03 HTTP + field keys |
| **M3 — Demo ready** | 0 contacts | Seed demo contacts; run full journey |
| **M4 — Snapshot export** | Not verifiable from JSON | Export after M2+M3 stable |
| **M5 — Pilot** | N/A | After snapshot + install playbook |

---

## 12. Prioritised next-step backlog (for Claude Code)

Use this as an ordered work queue. Each item should end in **evidence** (screenshot, test contact state, or refreshed JSON).

1. **Publish + smoke-test** — Turn **CAL-Intro-Call** active; publish workflows one-by-one with test contacts.
2. **WF-03 end-to-end** — Confirm webhook (if any), scorer deployment, **score field key** (`cf_qualification_score` vs `cf_lead_score`), tags, and **exact** pipeline stage names on move.
3. **Stage name audit** — Grep/export workflow actions for “Qualified”, “Nurture”, “Discovery Booked” vs live **Qualified - Hot**, **Nurture - Warm**, **Intro Call Booked**.
4. **WF-08** — Confirm Portal Welcome workflow exists or add per §7.
5. **WF-11 naming** — Confirm **Partner-Notifications** vs **Builder Internal Tasks** intent.
6. **Custom fields** — Add missing spec fields OR update spec/workflows to match Factory; fix `cf_financing_status` vs `cf_finance_status` if scorer expects one key.
7. **Custom values** — Add `fee_structure`, `survey_link`, `google_review_link`, portal URL; remove placeholders.
8. **Tags** — Create spec tags or verify workflows create them before first run.
9. **Templates** — Align names with workflows or vice versa; add **ET-BOOK-Confirmation**; SMS opt-out on all SMS.
10. **Payments** — Fix API scope or verify in UI: Stripe, e-sign, `payment-manual` path per WF-06.
11. **Re-run collector** — `python3 audit/ghl_audit_collector.py --api-key "…" --location-id "…" --output audit/audit_data.json` after major changes.
12. **Branding** — Complete `audit/GHL_BRANDING_AND_UI_SPEC.md` checklist; optional `audit/ghl_branding_captured.json` (gitignored by default).

---

## 13. Files to attach in Claude Code for deeper work

| File | Why |
|------|-----|
| `PREBUILD_AUTOPILOT_CONTEXT.md` | Full spec |
| `audit/audit_data.json` | Latest structured live metadata |
| `audit/SRV_QUALIFICATION_FULL_SPEC.md` | Survey ↔ field mapping |
| `audit/wf03_scoring_engine.py` | Scoring logic |
| `audit/DEEP_SPEC_ANALYSIS.md` | Known spec/code gaps |
| `audit/GHL_VERIFICATION_CHECKLIST.md` | Manual UI checklist (note: some row labels are older naming — cross-check §7 of context) |
| `audit/GHL_WRITTEN_CONTENT_DUMP.md` | Copy library where API bodies are empty |
| `CLAUDE.md` | Project status and open items |

---

## 14. Disclaimer

This document merges **API snapshot** (partial, no workflow internals) with **spec** and **static analysis**. It is not a substitute for: (a) opening each workflow in GHL, (b) sending test leads, (c) confirming Stripe and legal SMS footers, or (d) a lawyer’s review of agreements and spam compliance.

---

*Generated for PreBuild Autopilot / CentriWeb. Refresh `audit_data.json` and update this file’s snapshot date when the account changes materially.*
