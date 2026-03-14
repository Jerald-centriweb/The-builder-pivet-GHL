# Live Build Tracker — PreBuild Autopilot GHL Account

> **Living document.** Update this whenever something is built, fixed, or published in GHL.
> Every detail of the live account captured at the field/option/ID level.
>
> **Last full data pull:** March 14, 2026
> **Account:** MASTER FACTORY — PREBUILD ENGINE | `cVCso4OlgGoOoXMpbxxA`
> **Pipeline ID:** `KRZs6JZq3qKVnJyvTmZh`
>
> To refresh: run `audit/ghl_audit_collector.py` from the VPS and commit the new `audit_data.json`.

---

## Build Progress Summary

| Section | Total Required | Built | % Done | Blocking |
|---------|---------------|-------|--------|----------|
| Pipeline stages | 10 active | 7 correct / 3 wrong names | 70% | Yes — workflows won't route |
| Workflows | 11 | 10 draft / 0 published / 1 missing | 0% live | Yes |
| Custom fields | 22 | 15 built / 2 wrong names / 7 missing | 59% | Yes — WF-03 can't write scores |
| Custom values | 14 | 11 shells (all blank) / 3 missing | ~0% useful | Yes — all templates render blank |
| SMS templates | 9 | 5 shells (all blank) / 4 missing | 0% useful | Yes |
| Email templates | 14 | 0 | 0% | Yes |
| Tags | 17+ | 5 exist / 14 missing | 29% | Yes — workflows can't tag/route |
| Calendar | 1 | 1 (inactive, no team) | 0% functional | Yes — can't receive bookings |
| Survey | 1 | 1 (mapping unverified) | partial | Partial |
| Scoring engine | 1 | Code only — not deployed | 0% live | Yes — WF-03 is stub |

---

## 1. Pipeline Stages

**Pipeline name:** `Prebuild Pipeline`
**Pipeline ID:** `KRZs6JZq3qKVnJyvTmZh`

| # | Current Name | Required Name | Stage ID | Status |
|---|-------------|--------------|----------|--------|
| 0 | New Enquiry | New Enquiry | `66dfc3ca-9268-4210-8b5e-4a1e4d6e40b7` | ✅ Correct |
| 1 | Survey Completed | **DELETE** | `0e125a91-9bad-4807-8f5c-9459f9c7bd18` | ❌ Delete — contacts shouldn't sit here |
| 2 | Qualified - Hot | **Qualified** | `8883cbd1-098e-4829-bfa2-1bd558653e28` | ❌ Rename |
| 3 | Nurture - Warm | **Nurture** | `333e7953-2cea-472e-875e-33d14dd286a8` | ❌ Rename |
| 4 | Intro Call Booked | **Discovery Booked** | `91b6d5c4-2337-40e1-80ea-bbf01e93c8a7` | ❌ Rename |
| 5 | Proposal Sent | Proposal Sent | `b35dabb7-d871-4b3c-945a-0a3ad26129a7` | ✅ Correct |
| 6 | Engaged | Engaged | `c0a80e7f-6347-4f9b-87ad-f9062cbc4ca7` | ✅ Correct |
| 7 | Delivered | Delivered | `617535ae-a933-440c-96c6-06bf25675d9e` | ✅ Correct |
| 8 | Won | Won | `448d8524-9d58-41f7-b6eb-c8f048d4cb28` | ✅ Correct |
| 9 | Not Now | Not Now | `a82b6def-f219-468b-b45c-2ef1032785d3` | ✅ Correct |
| 10 | Lost | Lost | `e2bd3aa2-0f5d-42e3-843f-fb63fd1070df` | ✅ Correct |

**Fix:** Rename 3 stages. Delete 1. (Do before publishing any workflow.)

---

## 2. Custom Fields

All fields are contact-level. Parent group ID: `9J5apjY7yE5DoT87ovOS`

### Fields That Exist

| Field Key | Display Name | Type | Field ID | Status | Notes |
|-----------|-------------|------|----------|--------|-------|
| `cf_finance_status` | cf_finance_status | SINGLE_OPTIONS | `4sz70FQcItdNAYWypP75` | ❌ Rename → `cf_financing_status` | Wrong key — WF-03 writes to `cf_financing_status` |
| `cf_budget_how` | How did you arrive at that budget figure? | SINGLE_OPTIONS | `65TbdMo6scjMuTjJkqpw` | ✅ | Not scored but useful for context |
| `cf_partner_email` | cf_partner_email | TEXT | `BnhU18zxb5FTowoII5Bv` | ✅ | Partner workflow uses this |
| `cf_open_to_fee` | "Our process involves a paid preconstruction consultation…" | SINGLE_OPTIONS | `GvDfWDn1fVXi7zzeAhIq` | ⚠️ | Hard disqualifier field. "I'm not sure, it depends on the cost" option not in scoring engine — treat as warm |
| `cf_lead_score` | cf_lead_score | NUMERICAL | `Q3J4eIjb6jBNWShBassD` | ❌ Rename → `cf_qualification_score` | Scoring engine writes to `cf_qualification_score` |
| `cf_service_phase` | cf_service_phase | SINGLE_OPTIONS | `Qrl9ArsqpOoTJLwaEm3Z` | ⚠️ | Picklist values differ from spec |
| `cf_contact_role` | cf_contact_role | SINGLE_OPTIONS | `aaxgKaLrDXpu3WkUEBDG` | ✅ | Primary/Partner |
| `cf_budget_range` | cf_budget_range | SINGLE_OPTIONS | `agfjXtjPV85k1yIIxNAt` | ⚠️ | Has extra option "I'm not sure yet" — not scored, route as cold |
| `cf_partner_phone` | cf_partner_phone | PHONE | `j4VfskwKJcjzjx1EhaI8` | ✅ | |
| `cf_land_status` | cf_land_status | SINGLE_OPTIONS | `mI294jc8bR3ocPSUyyaZ` | ✅ | |
| `cf_household_id` | cf_household_id | TEXT | `o5VzkmKKYAKbobEtgk0E` | ✅ | Partner linking |
| `cf_project_type` | cf_project_type | SINGLE_OPTIONS | `o8Mmf8PKrWkhyMgFNsxC` | ✅ | |
| `cf_partner_name` | cf_partner_name | TEXT | `pL3PpzFrHXXaYhymuGx5` | ✅ | |
| `cf_timeline` | When are you hoping to start construction? | SINGLE_OPTIONS | `rhqrfzfvIDV3IpN3VnMm` | ✅ | Has "I'm just exploring" — soft disqualifier, scores 0 |
| `cf_suburb` | cf_suburb | TEXT | `rnRryJlMEJF6R7GczxmQ` | ✅ | Decide: use as `cf_site_address` or keep separate |

### Picklist Options — Every Field

**`cf_finance_status` (rename → `cf_financing_status`):**
- Yes, fully approved
- Yes, pre-approval in place
- We're in the process of arranging finance
- We're using cash / equity
- Not yet, still researching costs first

**`cf_budget_how`:**
- I spoke to a bank or broker and got a borrowing figure
- I researched build costs online / got rough quotes
- A family member or friend built recently and gave me a figure
- It's a rough number — I'm not sure if it's realistic

**`cf_open_to_fee`:**
- Yes, I understand professional advice has a cost ← scores 15pts (hot)
- I'd like to understand more about what's included first ← scores 8pts (warm)
- I'm not sure, it depends on the cost ← **NOT IN SCORING ENGINE** — add as 5pts
- No, I expect quotes and consultations to be free ← HARD DISQUALIFIER

**`cf_service_phase`:**
- Phase 1 - Budget Assessment ← spec says `phase_1` (picklist value mismatch — check WF-06)
- Phase 2 - Detailed Estimate ← spec says `phase_2` (same issue)

**`cf_contact_role`:**
- Primary
- Partner

**`cf_budget_range`:**
- Under $300K ← HARD DISQUALIFIER
- $300K–$500K ← scores 5pts
- $500K–$800K ← scores 10pts
- $800,000 – $1,200,000 ← scores 15pts
- $1,200,000+ ← scores 15pts
- I'm not sure yet, I need help understanding costs ← **NOT IN SCORING ENGINE** — add as cold (5pts)

**`cf_land_status`:**
- Yes, I own the land/property ← scores 15pts
- We're under contract to purchase ← scores 10pts
- We're actively looking for land ← scores 5pts
- Not applicable — I'm renovating my existing home ← scores 5pts

**`cf_project_type`:**
- New build ← scores 10pts
- Knockdown rebuild ← scores 10pts
- Major renovation ← scores 5pts
- Extension or addition ← scores 3pts
- Not sure yet ← scores 0pts

**`cf_timeline`:**
- As soon as possible ← scores 15pts
- Within 3-6 months ← scores 10pts
- In 6-12 months ← scores 5pts
- 12+ months away ← scores 0pts
- I'm just exploring at this stage ← scores 0pts (soft disqualifier — route to Not Now)

### Missing Custom Fields (Create These)

| Field Key | Type | Options | Set By | Priority |
|-----------|------|---------|--------|----------|
| `cf_lead_temperature` | SINGLE_OPTIONS | hot / warm / cold | WF-03 | 🔴 Critical |
| `cf_design_status` | SINGLE_OPTIONS | (check spec Section 5 for options) | Survey | 🔴 Critical |
| `cf_decision_maker` | SINGLE_OPTIONS | Yes / Shared / Other | Survey | 🔴 Critical |
| `cf_communication_preference` | SINGLE_OPTIONS | SMS / Email / Either | Survey | 🟡 High |
| `cf_lost_reason` | SINGLE_OPTIONS | Chose another builder / Budget / Timing / Other | Builder manual | 🟡 High |
| `cf_site_address` | TEXT | n/a | Survey | 🟡 High |
| `cf_prior_quotes` | SINGLE_OPTIONS | (check spec — scored field) | Survey | 🔴 Critical |
| `cf_qualification_score` | NUMERICAL | n/a | WF-03 (scoring engine) | 🔴 Critical (after rename) |

**Note:** `cf_qualification_score` is created by renaming `cf_lead_score`. After rename, the scoring engine endpoint already writes to the correct key.

**Decision needed on `cf_suburb` vs `cf_site_address`:** Both capture location. Options: (a) rename `cf_suburb` to `cf_site_address`, (b) keep both for different purposes (suburb = searchable/filterable, site_address = full address for site visit planning).

### Scoring Engine Gaps (Add to `audit/wf03_scoring_engine.py`)

Two live picklist options not in the scoring engine:
1. `cf_open_to_fee`: "I'm not sure, it depends on the cost" → recommended: 5pts (same as warm-leaning)
2. `cf_budget_range`: "I'm not sure yet, I need help understanding costs" → recommended: 5pts (cold)

---

## 3. Custom Values

All values under parent ID: `D9N3rxMFBkF7LyzBVoVn` (except `meeting_location` which has no parent)

### Current Custom Values (11 — all blank)

| Key | Template Syntax | Custom Value ID | Status |
|-----|----------------|----------------|--------|
| `builder_name` | `{{custom_values.builder_name}}` | `pS7Pziv6TlCv6CR2wNeJ` | ❌ Blank |
| `builder_phone` | `{{custom_values.builder_phone}}` | `jhu1RHj3eMpAEzJjBeaD` | ❌ Blank |
| `builder_email` | `{{custom_values.builder_email}}` | `wlGZP6ZjVUVBJ6BINPn8` | ❌ Blank |
| `builder_logo_url` | `{{custom_values.builder_logo_url}}` | `pfd60g17qledTetUmbn4` | ❌ Blank |
| `service_1_name` | `{{custom_values.service_1_name}}` | `C4fROtgclp1luF56hvej` | ❌ Blank |
| `service_1_fee` | `{{custom_values.service_1_fee}}` | `d3pLVQwE0CIOWYVAwnlh` | ❌ Blank |
| `service_2_name` | `{{custom_values.service_2_name}}` | `8YFzb8p0PgzdVh1AR1tq` | ❌ Blank |
| `service_2_fee` | `{{custom_values.service_2_fee}}` | `3rf7KPRgEEMsbbkNaMu9` | ❌ Blank |
| `calendar_link` | `{{custom_values.calendar_link}}` | `vvaTgPGV8GKr55qeZd0H` | ❌ Blank |
| `refund_policy` | `{{custom_values.refund_policy}}` | `oLX1uWnN5sYxIqCqFTE2` | ❌ Blank |
| `meeting_location` | `{{custom_values.meeting_location}}` | `W1PIwsKG6ei5r6GhDxTm` | ❌ Blank (not in spec — may be leftover) |

### Missing Custom Values (Create + Populate)

| Key | Template Syntax | Demo Value | Notes |
|-----|----------------|-----------|-------|
| `survey_link` | `{{custom_values.survey_link}}` | [GHL survey URL] | Critical — used in WF-01 first SMS |
| `portal_link` | `{{custom_values.portal_link}}` | [GHL membership portal URL] | WF-08 |
| `google_review_link` | `{{custom_values.google_review_link}}` | [Google Business URL] | WF-12 |
| `builder_abn` | `{{custom_values.builder_abn}}` | 12 345 678 901 | Proposal template |
| `agreement_title` | `{{custom_values.agreement_title}}` | Pre-Construction Services Agreement | Proposal template |

### Demo Values to Populate (For Sales Demos)

| Key | Demo Value |
|-----|-----------|
| `builder_name` | Smith Building Co |
| `builder_phone` | 0412 345 678 |
| `builder_email` | info@smithbuilding.com.au |
| `builder_abn` | 12 345 678 901 |
| `service_1_name` | Budget Estimate |
| `service_1_fee` | $550 inc GST |
| `service_2_name` | Detailed Quote |
| `service_2_fee` | $6,600 inc GST |
| `refund_policy` | Fees are fully refunded if we proceed to a building contract together. |
| `agreement_title` | Pre-Construction Services Agreement |
| `calendar_link` | [copy from GHL Settings → Calendars → CAL-Intro-Call → copy booking link] |
| `survey_link` | [copy from GHL → Sites → Surveys → SRV-Qualification-Survey → share link] |
| `portal_link` | [GHL Memberships → client portal → share link] |
| `google_review_link` | [Google Business profile → Write a review → copy URL] |

---

## 4. Workflows

| Workflow | ID | Status | Version | Action Needed |
|---------|----|--------|---------|---------------|
| WF-01-Speed-to-Lead | `9f2b93e5-9662-4749-b9d0-6b40c5c1b6a2` | Draft | 2 | Fix then publish |
| WF-02-Survey-Reminders | `17891e4d-c278-4895-a3f7-357c3178fb6b` | Draft | 2 | Fix then publish |
| WF-03-Scoring-and-Routing | `d52e3147-c48a-44d3-af52-6680e5573b47` | Draft | **95** | Wire scoring endpoint then publish |
| WF-04-Education-Sequence | `bbfe1ca0-14a6-4452-baea-7128661642b4` | Draft | 2 | Fix then publish |
| WF-05-Booking-Flow | `5408bfe2-e1c0-4220-aae5-81c673113183` | Draft | 2 | Fix then publish |
| WF-06-Proposal-and-Payment | `2fc5067c-be83-46d3-9a8c-550ce02e4a4e` | Draft | 2 | Fix then publish |
| WF-07 | — | — | — | Removed in v1.1 — do not recreate |
| **WF-08-Portal-Welcome** | **MISSING** | — | — | **Create from scratch** |
| WF-09-Stage-Notifications | `bd849e9f-9361-4526-a3b6-98b976c85d17` | Draft | 2 | Fix then publish |
| WF-10-Stale-Lead-Reminders | `c7241790-4b89-4995-b7fa-a1dba97d24db` | Draft | 2 | Fix then publish |
| WF-11-Partner-Notifications | `d06709cc-f1fc-4736-8f5b-391682f4c1cc` | Draft | 2 | Rename to WF-11-Builder-Tasks, restructure |
| WF-12-Review-Request | `1c1a6318-4ff8-41f1-9a49-ea2176c9576f` | Draft | 2 | Fix then publish |

**WF-03 note:** Version 95 means Jerald has been actively building this out. It's the most developed workflow. Still needs the external scoring endpoint wired before it can be tested.

**Publish order (after all other fixes done):**
1. WF-03 (test with dummy submission first)
2. WF-01
3. WF-02
4. WF-05
5. WF-04
6. WF-06
7. WF-08
8. WF-09
9. WF-10
10. WF-11
11. WF-12

---

## 5. Tags

### Existing Tags (5)

| Tag Name | Tag ID | Status |
|----------|--------|--------|
| `lead-cold` | `MXOLGdGZbJieXmd94skG` | ✅ |
| `lead-hot` | `tKwww2XKloLqXK8q7CvL` | ✅ |
| `lead-warm` | `Dj7zf3vRSdlS1gc6ad3u` | ✅ |
| `role-partner` | `qZEvg5CBpDK2bCPGVUTd` | ✅ (extra — not in spec but useful) |
| `role-primary` | `Vqpcvxmm3P8PGBkSY6BJ` | ✅ (extra — not in spec but useful) |

### Missing Tags (Create in GHL → Settings → Tags)

| Tag | Used By | Priority |
|-----|---------|----------|
| `survey-pending` | WF-01 (adds), WF-03 (removes) | 🔴 Critical |
| `survey-completed` | WF-03 (adds on complete survey) | 🔴 Critical |
| `survey-abandoned` | WF-02 (adds on Day 8 no response) | 🔴 Critical |
| `call-booked` | WF-05 (adds on calendar booking) | 🔴 Critical |
| `proposal-sent` | WF-06 (adds) | 🟡 High |
| `payment-received` | WF-06 (adds on payment) | 🟡 High |
| `portal-active` | WF-08 (adds on portal welcome sent) | 🟡 High |
| `review-requested` | WF-12 (adds) | 🟡 High |
| `stage-won` | WF-09 (adds on Won stage) | 🟡 High |
| `stage-lost` | WF-09 (adds on Lost stage) | 🟡 High |
| `fee-tier-two` | WF-06 (adds when two_tier fee structure) | 🟡 High |
| `fee-tier-single` | WF-06 (adds when single_tier) | 🟡 High |
| `fee-tier-none` | WF-06 (adds when no_fee) | 🟡 High |
| `payment-manual` | WF-06 (adds when payment is outside Stripe) | 🟡 High |

---

## 6. SMS Templates

All 5 existing templates have **blank bodies** — they exist as named shells only.

### Existing SMS Templates (5 — all need content written)

| Template Name | Template ID | Origin ID | Status | Copy Source |
|--------------|-------------|-----------|--------|-------------|
| SMS-BOOK-Confirmation | `NJRMCgbDfy5I7CgJYeOw` | `rKmL23eyEP8oR2in7sRc` | ❌ Blank body | Spec Section 8 |
| SMS-BOOK-Reminder-24hr | `HagMETiAlknBPzX5f8O7` | `yLMfHriPsNzpHQQUBGNl` | ❌ Blank body | Spec Section 8 |
| SMS-PROP-Agreement-Sent | `j69tNcYHetz36cQmwVBq` | `rg4VIFfBZ3GNzp2pu9wg` | ❌ Blank body | Spec Section 8 |
| SMS-STL-Survey-Link | `bDXUKR51AfVU1iRrNQ1G` | `njG9CDduIZQiJj3181jA` | ❌ Blank body | Spec Section 8 |
| SMS-STL-Survey-Reminder | `oSg6lXwcNAXEJeVkSYQV` | `tfzjlxmT4nhYRVefXAmL` | ❌ Blank body | Spec Section 8 |

### Missing SMS Templates (4 — Create + Write)

| Template | When It Fires | Copy Source |
|---------|--------------|-------------|
| SMS-SRV-Final | WF-02 Day 8 — final survey nudge | Spec Section 8 |
| SMS-QUAL-Hot-BookCall | WF-03 — hot lead → calendar link | Spec Section 8 |
| SMS-PAY-Confirmation | WF-06 — payment confirmed | Spec Section 8 |
| SMS-WIN-ReviewRequest | WF-12 — 14 days after Won | Spec Section 8 |

**Compliance rule:** Every SMS must end with: `Reply STOP to opt out.`

---

## 7. Email Templates

**Count: 0 exist.** All 14 need to be created. Copy for all is in `PREBUILD_AUTOPILOT_CONTEXT.md` Section 8.

| Template ID | Trigger | Workflow |
|------------|---------|----------|
| ET-STL-01-Welcome | New contact (immediate) | WF-01 |
| ET-SRV-Reminder-2 | No survey at 120hrs | WF-02 |
| ET-QUAL-Hot-BookCall | Hot lead routing | WF-03 |
| ET-EDU-01-Process-Overview | Education Day 0 | WF-04 |
| ET-EDU-02-Service-1-Explainer | Education Day 3 | WF-04 |
| ET-EDU-03-Service-2-Explainer | Education Day 5 | WF-04 |
| ET-EDU-04-Testimonial | Education Day 7 | WF-04 |
| ET-EDU-05-CTA-Next-Step | Education Day 10 | WF-04 |
| ET-BOOK-Confirmation | Calendar booking | WF-05 |
| ET-PROP-Agreement-Sent | Proposal Sent stage | WF-06 |
| ET-PROP-Reminder-48hr | 48hrs after proposal if unsigned | WF-06 |
| ET-PAY-Confirmation | Payment confirmed | WF-06 |
| ET-PORTAL-Welcome | Engaged stage | WF-08 |
| ET-WIN-ReviewRequest | 14 days after Won | WF-12 |

---

## 8. Forms + Survey + Calendar

### Forms (3)

| Form Name | Form ID | Status |
|-----------|---------|--------|
| FRM-Lead-Intake | `x1jLoeSHaBKZXm8Gm0gu` | ⚠️ Built — field mapping to custom fields unverified |
| SRV-Qualification-Survey (form version) | `ugnDa7Hh1lQNb52GUypu` | ⚠️ Built — same as survey below |
| Book a demo | `GbemuaflhwNAilmnqgEf` | ⚠️ Extra form — not in spec, may be leftover or Jerald's use |

### Survey (1)

| Survey Name | Survey ID | Status |
|------------|-----------|--------|
| SRV-Qualification-Survey | `J30zhHTAz8daVE7wZP7P` | ⚠️ Built — field-to-custom-field mapping unverified |

**Action needed:** Verify each survey question maps to the correct custom field key. See `audit/SRV_QUALIFICATION_FULL_SPEC.md` for the expected 15 questions and their mappings.

### Calendar (1)

| Calendar Name | Calendar ID | Status | Issues |
|--------------|-------------|--------|--------|
| CAL-Intro-Call | `b4uPmlCoYV7J96XJZBsD` | ❌ Inactive | `isActive: false`, no team members, no open hours |

**Fix needed:**
1. Add builder (Jerald or demo user) as team member
2. Set availability/open hours
3. Set `isActive: true`
4. Copy the booking URL → paste into `calendar_link` custom value

**Calendar config (current):**
- Type: Round Robin (OptimizeForAvailability)
- Slot duration: 30 mins
- Slot interval: 30 mins
- Auto-confirm: true
- Allow reschedule/cancel: true
- Widget slug: `cal-intro-call-demo-9faa41b6-a29d-4ec6-8d79-cd88d220fe46`
- Event title template: `{{contact.name}}`

---

## 9. Location Settings

| Setting | Current Value | Correct Value |
|---------|--------------|---------------|
| Name | MASTER FACTORY — PREBUILD ENGINE | ✅ |
| Address | 3 ocean street, New Castle NSW 2290 | ✅ |
| Website | centriweb.com | ✅ |
| Timezone | **Pacific/Auckland** | **Australia/Sydney** ← Fix this |
| Logo URL | (blank) | Upload CentriWeb or demo logo |
| Currency | (blank) | AUD |
| Default email service | (blank) | Set up SMTP or GHL email |
| Social links | All blank | Set Facebook at minimum for builder demos |

**Fix timezone first** — all workflow time-based delays and the after-hours logic (feature 1.1) will fire at wrong times if timezone is wrong.

---

## 10. Scoring Engine Status

**File:** `audit/wf03_scoring_engine.py`
**Deployment:** NOT deployed — code only

### Current Score Rubric

| Field | Max Points | Key Options |
|-------|-----------|-------------|
| `project_type` | 10 | New build/KDR=10, Reno=5, Extension=3, Not sure=0 |
| `land_status` | 15 | Own land=15, Under contract=10, Looking=5, Renovating=5 |
| `design_status` | 15 | Full plans=15, Rough concept=10, Early stages=5, Not started=0 |
| `timeline` | 15 | ASAP=15, 3-6mo=10, 6-12mo=5, 12+/exploring=0 |
| `prior_quotes` | 10 | None yet=10, 1-2 others=8, 3+=5, Over-shopped=0 |
| `budget_range` | 15 | $800K+=15, $500-800K=10, $300-500K=5, <$300K=DISQUALIFY |
| `financing_status` | 15 | Fully approved=15, Pre-approved=12, In process=8, Cash=15, Not yet=3 |
| `decision_maker` | 10 | Yes=10, Shared=7, Other=3, No=0 |
| `site_challenges` | 10 | No major challenges=10, Minor=7, Moderate=5, Significant=0 |
| `open_to_fee` | 15 | Yes=15, Learn more=8, **Not sure=5 (add this)**, No=DISQUALIFY |
| `referral_source` | 15 | Referral=15, Website=8, Google/Social=5, Other=5 |
| **MAX RAW** | **145** | |

**Hard disqualifiers (override score → Not Now regardless):**
- `budget_range` = "Under $300K"
- `open_to_fee` = "No, I expect quotes and consultations to be free"

**Score bands:**
- Hot: ≥80 → Stage: Qualified, Tag: lead-hot, SMS: calendar link
- Warm: 50–79 → Stage: Nurture, Tag: lead-warm, Start: WF-04 education
- Cold: <50 → Stage: Not Now, Tag: lead-cold

### Deployment Options

**Option A (n8n) — recommended:**
1. Create n8n workflow: HTTP trigger → Code node (paste `score_lead()`) → HTTP POST back to GHL
2. Copy webhook URL
3. In WF-03: add HTTP Request action → POST survey field values to that URL

**Option B (GHL native) — no-code fallback for demo:**
- If/Then branches: `cf_budget_range` = "Under $300K" → Not Now
- If `cf_open_to_fee` = "No" → Not Now
- If `cf_budget_range` = "$800K+" AND `cf_land_status` = "own" AND `cf_timeline` = "ASAP" → Qualified
- Everything else → Nurture

---

## 11. Additional Issues Discovered in Audit

| Issue | Severity | Action |
|-------|----------|--------|
| `cf_service_phase` picklist values don't match spec (uses "Phase 1 - Budget Assessment" not `phase_1`) | 🟡 | Verify WF-06 `If/Else` conditions match actual picklist text |
| `cf_open_to_fee` has 4th option "I'm not sure" not in scoring engine | 🔴 | Add to scoring engine: 5pts |
| `cf_budget_range` has extra option "I'm not sure yet" not in scoring engine | 🟡 | Add: 5pts (cold routing) |
| `cf_timeline` has "I'm just exploring" — should this be a hard disqualifier? | 🟡 | Current: scores 0 + routes cold. Consider making soft-disqualifier to Not Now if also 12+ months |
| Calendar `isActive: false` | 🔴 | Activate + add team member before WF-05 is published |
| Timezone `Pacific/Auckland` | 🟡 | Change to `Australia/Sydney` before publishing time-based workflows |
| All 5 SMS template bodies blank | 🔴 | Write content before publishing WF-01/02/05/06 |
| `payments` API returns 403 | ℹ️ | Needs `payments.readonly` OAuth scope. Not critical unless you want payment reporting |
| `snapshotId` is empty string | ℹ️ | Factory account hasn't been snapshotted yet — expected at this stage |
| No contacts in account | ℹ️ | Expected — Factory account. Seed demo contacts when ready to demo |
| `currency` is blank | 🟡 | Set to AUD — may affect Stripe integration and proposal display |
| `logoUrl` is blank | 🟡 | Upload a logo for email template header |

---

## 12. Change Log

Track every change made to the live account here. Newest at top.

| Date | Changed By | What Changed | Status |
|------|-----------|-------------|--------|
| 2026-03-14 | Claude Code | Created this tracker document | Done |
| 2026-03-14 | ghl_audit_collector.py | Full account data pulled to audit_data.json | Done |

*(Add rows as things are built in GHL. This is how you keep all Claude instances in sync.)*

---

## 13. Next 3 Actions

Based on current state, the highest-leverage moves right now:

**Action 1 — Fix blocking infrastructure (30 mins in GHL):**
- Rename 4 pipeline stages
- Rename 2 custom fields
- Fix timezone (Pacific/Auckland → Australia/Sydney)
- Activate calendar + add team member

**Action 2 — Populate custom values for demo (20 mins):**
- Fill all 11 existing values with Smith Building Co demo data
- Get the 3 missing URLs (survey link, calendar link, portal link) and create + populate those

**Action 3 — Write all SMS template content (1 hour):**
- Open each of the 5 blank SMS shells in GHL
- Copy content from PREBUILD_AUTOPILOT_CONTEXT.md Section 8
- Create the 4 missing SMS templates

After those 3 actions: WF-01, WF-02, WF-05 can be tested end-to-end. The account will be functional enough to show a basic demo.
