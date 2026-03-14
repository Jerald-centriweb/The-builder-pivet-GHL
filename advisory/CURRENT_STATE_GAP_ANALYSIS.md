# Live Account Gap Analysis — What's Built vs What's Needed

> Based on the GHL live account dump (March 2026) vs PREBUILD_AUTOPILOT_CONTEXT.md spec.
> Use this as a build checklist. Work top to bottom.

**Account:** MASTER FACTORY — PREBUILD ENGINE | `cVCso4OlgGoOoXMpbxxA`

---

## Status Summary

| Category | Spec Requires | Live Has | Gap |
|----------|-------------|---------|-----|
| Pipeline stages | 10 | 11 (4 wrong names) | Rename 4, remove 1 |
| Workflows | 11 | 10 (all Draft) | Publish 10, create 1 |
| Custom fields | 22 | 15 (2 wrong names) | Create 7, rename 2 |
| Custom values | 14 required | 11 (all blank) | Create 3, populate all 14 |
| SMS templates | 9 | 5 | Create 4 |
| Email templates | 14 | 0 | Create all 14 |
| Tags | 16 | 5 | Create 11 |
| Survey | 1 | 1 (unverified mapping) | Verify field mappings |
| Calendar | 1 | 1 | Verify booking link |
| Portal | 5 pages | Unconfirmed | Build/verify |
| Scoring engine | Deployed + wired | Code only | Deploy + wire WF-03 |

---

## Fix 1 — Pipeline Stage Names (Do This First)

Workflow "Move to Stage" actions use exact text matching. Wrong names = silent failures.

| Current Name | Change To | Why |
|-------------|----------|-----|
| Survey Completed | **Delete this stage** | Not a pipeline stage — it's a tag. Contacts shouldn't sit here. |
| Qualified - Hot | **Qualified** | Spec name. Workflows reference "Qualified". |
| Nurture - Warm | **Nurture** | Spec name. Workflows reference "Nurture". |
| Intro Call Booked | **Discovery Booked** | Spec name. WF-05 moves to "Discovery Booked". |
| New Enquiry | Keep | ✅ Matches |
| Proposal Sent | Keep | ✅ Matches |
| Engaged | Keep | ✅ Matches |
| Delivered | Keep | ✅ Matches |
| Won | Keep | ✅ Matches |
| Not Now | Keep | ✅ Matches |
| Lost | Keep | ✅ Matches |

---

## Fix 2 — Custom Field Names

| Current Key | Change To | Type | Notes |
|------------|----------|------|-------|
| `cf_lead_score` | `cf_qualification_score` | NUMERICAL | Scoring engine writes to this key |
| `cf_finance_status` | `cf_financing_status` | SINGLE_OPTIONS | Survey maps to this key |

---

## Fix 3 — Missing Custom Fields (Create These)

| Field Name | Key | Type | Set By |
|-----------|-----|------|-------|
| Lead Temperature | `cf_lead_temperature` | SINGLE_OPTIONS (hot/warm/cold) | WF-03 |
| Design Status | `cf_design_status` | SINGLE_OPTIONS | Survey |
| Decision Maker | `cf_decision_maker` | SINGLE_OPTIONS (Yes/Shared/Other) | Survey |
| Communication Preference | `cf_communication_preference` | SINGLE_OPTIONS | Survey |
| Lost Reason | `cf_lost_reason` | SINGLE_OPTIONS | Builder (manual) |
| Site Address | `cf_site_address` | TEXT | Survey |
| Prior Quotes | `cf_prior_quotes` | SINGLE_OPTIONS | Survey |

Note: `cf_suburb` currently exists — decide if this replaces `cf_site_address` or if both are needed.

---

## Fix 4 — Missing Custom Values (Create + Populate)

All current 11 custom values are **blank** — they need real values for even the demo to work.

| Key | What to populate | Notes |
|-----|-----------------|-------|
| `builder_name` | Smith Building Co (demo) | Required in every template |
| `builder_phone` | 0412 345 678 (demo) | |
| `builder_email` | info@smithbuilding.com.au (demo) | |
| `builder_abn` | 12 345 678 901 (demo) | Needed for proposal |
| `service_1_name` | Budget Estimate | |
| `service_1_fee` | $550 inc GST | |
| `service_2_name` | Detailed Quote | |
| `service_2_fee` | $6,600 inc GST | |
| `calendar_link` | [actual GHL calendar URL] | |
| `survey_link` | [actual GHL survey URL] | Critical — in WF-01 |
| `portal_link` | [actual GHL portal URL] | |
| `google_review_link` | [Google Business review URL] | |
| `refund_policy` | Fees are fully refunded if we proceed to a building contract together. | |
| `agreement_title` | Pre-Construction Services Agreement | |

---

## Fix 5 — Missing Tags (Create All)

Tags that workflows add/remove/check must exist before workflows can use them.

Create these tags in GHL (Settings → Tags):
- `survey-pending`
- `survey-completed`
- `survey-abandoned`
- `call-booked`
- `proposal-sent`
- `payment-received`
- `portal-active`
- `review-requested`
- `stage-won`
- `stage-lost`
- `fee-tier-two`
- `fee-tier-single`
- `fee-tier-none`
- `payment-manual`
- `lead-cold` ✅ exists
- `lead-hot` ✅ exists
- `lead-warm` ✅ exists

---

## Fix 6 — Missing Workflows (Create 1)

| Workflow | Status | Action |
|---------|--------|--------|
| WF-01-Speed-to-Lead | Draft | Fix, then publish |
| WF-02-Survey-Reminders | Draft | Fix, then publish |
| WF-03-Scoring-and-Routing | Draft | Fix + wire external scorer, then publish |
| WF-04-Education-Sequence | Draft | Fix, then publish |
| WF-05-Booking-Flow | Draft | Fix, then publish |
| WF-06-Proposal-and-Payment | Draft | Fix, then publish |
| **WF-08-Portal-Welcome** | **Missing** | **Create from spec, then publish** |
| WF-09-Stage-Notifications | Draft | Fix, then publish |
| WF-10-Stale-Lead-Reminders | Draft | Fix, then publish |
| WF-11-Partner-Notifications | Draft | Rename to WF-11-Builder-Tasks per spec, restructure |
| WF-12-Review-Request | Draft | Fix, then publish |

**Publish order matters:** Fix field names + stage names BEFORE publishing workflows. Otherwise they'll fire and fail silently.

---

## Fix 7 — Missing Email Templates (Create All 14)

All copy is in `PREBUILD_AUTOPILOT_CONTEXT.md` Section 8. Copy-paste from there.

| Template ID | Type | When It Fires |
|------------|------|--------------|
| ET-STL-01-Welcome | Email | WF-01 immediately on new contact |
| ET-SRV-Reminder-2 | Email | WF-02 at 120hrs if no survey |
| ET-QUAL-Hot-BookCall | Email | WF-03 on hot lead routing |
| ET-EDU-01-Process-Overview | Email | WF-04 Day 0 |
| ET-EDU-02-Service-1-Explainer | Email | WF-04 Day 3 |
| ET-EDU-03-Service-2-Explainer | Email | WF-04 Day 5 |
| ET-EDU-04-Testimonial | Email | WF-04 Day 7 |
| ET-EDU-05-CTA-Next-Step | Email | WF-04 Day 10 |
| ET-BOOK-Confirmation | Email | WF-05 on calendar booking |
| ET-PROP-Agreement-Sent | Email | WF-06 on Proposal Sent stage |
| ET-PROP-Reminder-48hr | Email | WF-06 48hrs after proposal if unsigned |
| ET-PAY-Confirmation | Email | WF-06 on payment confirmed |
| ET-PORTAL-Welcome | Email | WF-08 on Engaged stage |
| ET-WIN-ReviewRequest | Email | WF-12 (optional — SMS is primary) |

---

## Fix 8 — Missing SMS Templates (Create 4)

| Template | When |
|---------|------|
| SMS-SRV-Final | WF-02 Day 8 final survey nudge |
| SMS-QUAL-Hot-BookCall | WF-03 hot lead → calendar link |
| SMS-PAY-Confirmation | WF-06 payment confirmed |
| SMS-WIN-ReviewRequest | WF-12 14 days after Won |

All copy in `PREBUILD_AUTOPILOT_CONTEXT.md` Section 8.

**Check compliance on all SMS:** Every SMS must end with "Reply STOP to opt out."

---

## Fix 9 — Deploy Scoring Engine + Wire WF-03

This is the most technical fix and must happen before the system is useful.

**Option A — n8n (if Jerald already uses n8n):**
1. Create new n8n workflow with HTTP webhook trigger
2. Add Code node — paste the `score_lead()` function from `audit/wf03_scoring_engine.py`
3. Add HTTP Request node — POST result back to GHL contacts API
4. Copy webhook URL
5. In GHL WF-03 → add HTTP Request action → POST survey data to that URL

**Option B — No code at all (workaround):**
Use GHL's native If/Then branches with hard-coded score ranges. It won't be as precise but it works without external tools:
- If budget = "Under $300K" → disqualify
- If budget = "$800K+" AND land = "Own Land" AND timeline = "ASAP" → hot
- Everything else → warm or cold
Not recommended for production but usable to demo the routing.

---

## Fix 10 — Publish Workflows (Last Step)

Only publish after Fixes 1–9 are done. Publishing order:

1. WF-03-Scoring-and-Routing (test first with a dummy survey submission)
2. WF-01-Speed-to-Lead
3. WF-02-Survey-Reminders
4. WF-05-Booking-Flow
5. WF-04-Education-Sequence
6. WF-06-Proposal-and-Payment
7. WF-08-Portal-Welcome
8. WF-09-Stage-Notifications
9. WF-10-Stale-Lead-Reminders
10. WF-11-Builder-Tasks
11. WF-12-Review-Request

---

## QA Tests (Run After Publishing)

From `PREBUILD_AUTOPILOT_CONTEXT.md` Section 13 — all 18 tests must pass before demoing.

Critical ones to run first:
1. Submit test form → SMS received < 60 sec → email received → builder notification
2. Complete survey (hot answers) → score ≥80 → tag lead-hot → stage = Qualified → calendar SMS sent
3. Hard disqualifier: budget under $300K → Not Now regardless of other scores
4. Hard disqualifier: "No" to fee → Not Now
5. Move to Proposal Sent → proposal email fires with correct phase content
6. Test payment path → pipeline moves to Engaged
