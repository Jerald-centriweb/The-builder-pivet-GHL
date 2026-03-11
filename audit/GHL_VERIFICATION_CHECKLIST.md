# PreBuild Autopilot — GHL Live Verification Checklist

> **Purpose:** This document separates what was *designed/specified* from what *actually exists and works* inside your GHL sub-account. The previous audit report was an architecture review conducted against the spec — not a confirmed live inspection of the account. Use this checklist to close that gap.

**How to use it:**
- Go into your GHL sub-account and work through each section
- Mark each item ✅ CONFIRMED, ❌ MISSING/BROKEN, or ⚠️ EXISTS BUT NEEDS FIX
- Items marked **[CRITICAL]** will cause the system to fail if not resolved

---

## HONEST VERDICT: What the Audit Actually Did

| What It Did Well | What It Did NOT Do |
|-----------------|-------------------|
| Reviewed the architecture against the spec | Pulled live data from your GHL account |
| Identified the real technical bottleneck (WF-03 scoring) | Confirmed workflows are active and correctly wired |
| Found compliance gaps (SMS opt-out, review link) | Verified survey fields map to the right custom fields |
| Turned problems into an execution order | Confirmed e-sign → Stripe chain actually works |
| Framed a sellable product narrative | Verified templates render correctly in live GHL |

**Bottom line:** The output is a strong implementation review and risk map — use it as a verification checklist and build queue, not as confirmed truth.

---

## Section 1: Custom Fields
*Navigate to: Settings → Custom Fields → Contacts*

| # | Field Name | Key | Expected Type | Status |
|---|-----------|-----|---------------|--------|
| 1 | Qualification Score | `cf_qualification_score` | Number | |
| 2 | Lead Temperature | `cf_lead_temperature` | Dropdown (hot/warm/cold) | |
| 3 | Budget Range | `cf_budget_range` | Dropdown | |
| 4 | Project Type | `cf_project_type` | Dropdown | |
| 5 | Land Status | `cf_land_status` | Dropdown | |
| 6 | Site Address | `cf_site_address` | Text | |
| 7 | Timeline | `cf_timeline` | Dropdown | |
| 8 | Financing Status | `cf_financing_status` | Dropdown | |
| 9 | Decision Maker | `cf_decision_maker` | Dropdown | |
| 10 | Open to Fee | `cf_open_to_fee` | Dropdown (yes/needs_info/no) | |
| 11 | Communication Preference | `cf_communication_preference` | Dropdown | |
| 12 | Service Phase | `cf_service_phase` | Dropdown | |
| 13 | Service 1 Fee | `cf_service_1_fee` | Number/Currency | |
| 14 | Service 2 Fee | `cf_service_2_fee` | Number/Currency | |
| 15 | Lost Reason | `cf_lost_reason` | Dropdown | |
| 16 | How Heard / Source | `cf_how_heard` | Dropdown | *(Added in updated spec — may not exist yet)* |
| 17 | Partner Name | `cf_partner_name` | Text | *(Added in updated spec — may not exist yet)* |
| 18 | Partner Email | `cf_partner_email` | Email | *(Added in updated spec — may not exist yet)* |

**What to check:**
- [ ] All fields exist with the exact key names above
- [ ] Dropdown options match what the survey sends (exact text string match required)
- [ ] `cf_qualification_score` is a Number field, not Text (scoring engine writes numbers)

---

## Section 2: Custom Values (Merge Fields)
*Navigate to: Settings → Custom Values*

| # | Custom Value | Expected Alias | Status |
|---|-------------|---------------|--------|
| 1 | Builder name | `{{custom_values.builder_name}}` | |
| 2 | Builder phone | `{{custom_values.builder_phone}}` | |
| 3 | Builder email | `{{custom_values.builder_email}}` | |
| 4 | Company name | `{{custom_values.company_name}}` | |
| 5 | Service 1 fee label | `{{custom_values.service_1_fee_label}}` | |
| 6 | Service 2 fee label | `{{custom_values.service_2_fee_label}}` | |
| 7 | Intro call link | `{{custom_values.intro_call_link}}` | |
| 8 | Client portal URL | `{{custom_values.portal_url}}` | |
| 9 | Google review link | `{{custom_values.google_review_link}}` | *(Must be a real URL, not a placeholder)* |
| 10 | Fee tier preset | `{{custom_values.fee_tier}}` | |

**What to check:**
- [ ] All values are populated with real data (not placeholder text)
- [ ] `google_review_link` is a real Google Maps review URL
- [ ] `intro_call_link` opens the correct Calendly/GHL calendar

---

## Section 3: Pipeline Stages
*Navigate to: CRM → Pipelines → PreBuild Autopilot Pipeline*

| # | Stage Name | Expected Purpose | Status |
|---|-----------|-----------------|--------|
| 1 | New Enquiry | Unprocessed inbound lead | |
| 2 | Survey Sent | Survey dispatched, awaiting completion | |
| 3 | Qualified | Score ≥ 80, hot lead | |
| 4 | Nurture | Score 50–79, warm lead | |
| 5 | Not Now | Score < 50 or disqualified | |
| 6 | Discovery Booked | Call scheduled | |
| 7 | Discovery Complete | Call held | |
| 8 | Proposal Sent | Engagement agreement out | |
| 9 | Client — Active | Paid, in preconstruction | |
| 10 | Lost | Dead deal, reason captured | |

**What to check:**
- [ ] Stages exist with the exact names above (workflow stage-move actions use exact text)
- [ ] Two separate pipelines exist if using two_tier (Phase 1 + Phase 2) OR one pipeline with `cf_service_phase` to track which phase
- [ ] Stage order is logical (no stage-move going backwards by accident)

---

## Section 4: Workflows — Existence & Status
*Navigate to: Automation → Workflows*

**[CRITICAL]** This is the most important section to verify.

| # | Workflow ID | Name | Expected Trigger | Status (Published/Draft/Missing) |
|---|------------|------|-----------------|----------------------------------|
| WF-01 | Speed-to-Lead | New Enquiry Response | Contact created OR form submitted | |
| WF-02 | Survey Delivery | Survey Delivery | Tag added: `survey-pending` | |
| WF-03 | **Lead Scoring & Routing** | **CRITICAL** | Survey form submitted | |
| WF-04 | Hot Lead Nurture | Hot Lead Education | Tag added: `lead-hot` | |
| WF-05 | Discovery Call | Discovery Call Handler | Calendar booked (CAL-Intro-Call) | |
| WF-06 | Proposal & Payment | Proposal & Activation | Stage moved to `Proposal Sent` | |
| WF-07 | Client Onboarding | Client Onboarding | Tag added: `client-active` | |
| WF-08 | Project Delivery | In-Project Touchpoints | Tag added: `project-delivery` | |
| WF-09 | Completion & Handoff | Project Completion | Tag added: `project-complete` | |
| WF-10 | Win-Back & Reviews | Win-Back & Review | Tag added: `project-handoff` | |
| WF-11 | Cold/Warm Nurture | Warm Lead Nurture | Tag added: `lead-warm` | |
| WF-12 | Disqualified | Disqualified Handling | Tag added: `lead-cold` | |
| WF-13 | Long-Term Nurture | Not Now Re-engagement | *(To be built — not in snapshot)* | |

**For WF-03 specifically — the engine of the whole system:**
- [ ] Does WF-03 actually compute a score? (GHL cannot do this natively — it requires an external scoring endpoint)
- [ ] Is there a webhook call to an external scorer (n8n / Cloud Function / Lambda)?
- [ ] If no external scorer exists yet, WF-03 scoring is **not working** — this is the #1 build priority

---

## Section 5: WF-03 Scoring — Live State Check

This is the single most important verification in the entire checklist.

**The problem:** GHL workflows cannot do weighted math across 10 fields with hard disqualifier overrides. There is no native "if answer = X add Y points" accumulator in GHL.

**What *should* exist:**
1. Survey submits → GHL webhook fires to external endpoint
2. External endpoint (n8n / Cloud Function) runs `score_lead()` from `wf03_scoring_engine.py`
3. Scorer POSTs result back to GHL: updates `cf_qualification_score`, `cf_lead_temperature`, adds tags
4. WF-03 branches on `cf_lead_temperature` value to route lead

**Verification steps:**
- [ ] Open WF-03 — does it contain a **Webhook** action or **HTTP Request** step?
- [ ] If yes: what URL does it POST to? Is that endpoint deployed and running?
- [ ] Send a test lead through the survey — does `cf_qualification_score` get populated with a number?
- [ ] Does the lead move to the correct pipeline stage based on score?
- [ ] Submit a lead with budget "Under $300,000" — does it get tagged `lead-cold` and go to Not Now?
- [ ] Submit a lead answering "No, I'm only looking for free quotes" — same result?

**If scoring is not working:** The `wf03_scoring_engine.py` in this repo is ready to deploy. See deployment options in that file (n8n Code Node, Google Cloud Function, AWS Lambda).

---

## Section 6: Survey — Field Mapping Verification
*Navigate to: Sites → Surveys → SRV-Qualification*

**[CRITICAL]** Survey answers must write to the exact custom field keys. If mapping is wrong, scoring engine gets blank data.

| # | Survey Question | Writes To Field | Status |
|---|----------------|----------------|--------|
| 1 | Project type | `cf_project_type` | |
| 2 | Land/property status | `cf_land_status` | |
| 3 | Design / plans status | `cf_design_status` | |
| 4 | Timeline | `cf_timeline` | |
| 5 | Prior builder quotes | `cf_prior_quotes` | |
| 6 | Budget range | `cf_budget_range` | |
| 7 | Finance status | `cf_financing_status` | |
| 8 | Decision maker | `cf_decision_maker` | |
| 9 | Site challenges | `cf_site_challenges` | |
| 10 | Open to fee | `cf_open_to_fee` | |
| 11 | Site address | `cf_site_address` | |
| 12 | Communication preference | `cf_communication_preference` | |
| 13 | How did you hear about us | `cf_how_heard` | |
| 14 | Partner name | `cf_partner_name` | |

**What to check:**
- [ ] Every question has a field mapping (not just a label)
- [ ] Answer option text *exactly* matches what `wf03_scoring_engine.py` expects (e.g. "Under $300,000" not "under 300k")
- [ ] Survey fires a trigger tag or webhook on completion

---

## Section 7: Email & SMS Templates
*Navigate to: Marketing → Emails / SMS*

**Compliance check (do these before anything else):**
- [ ] Every SMS template ends with: *"Reply STOP to opt out"* or *"Reply STOP to unsubscribe"*
- [ ] SMS-WIN-ReviewRequest: replace `[Google Review Link]` with `{{custom_values.google_review_link}}`
- [ ] ET-EDU-01: remove any `{{#if fee_tier == "single_tier"}}` Handlebars conditionals — they don't render in GHL's email builder. Replace with workflow branching.

**Template existence check:**

| # | Template ID | Expected Content | Exists? |
|---|------------|-----------------|---------|
| 1 | ET-SPEED-01 | Immediate inbound acknowledgement | |
| 2 | ET-EDU-01 | Education email 1 (fee concept intro) | |
| 3 | ET-EDU-02 | Education email 2 (preconstruction value) | |
| 4 | ET-EDU-03 | Education email 3 (builder selection) | |
| 5 | ET-DISC-01 | Discovery call confirmation | |
| 6 | ET-DISC-02 | Discovery call reminder | |
| 7 | ET-PROP-01 | Proposal sent / sign here | |
| 8 | ET-ONBOARD-01 | Welcome to preconstruction | |
| 9 | SMS-SPEED-01 | Immediate SMS acknowledgement | |
| 10 | SMS-SURVEY-01 | Survey link SMS | |
| 11 | SMS-WIN-ReviewRequest | Review request (post-completion) | |

---

## Section 8: Payment & E-Sign Chain
*Navigate to: Payments → Products, and check WF-06*

- [ ] Stripe is connected under Settings → Integrations → Stripe
- [ ] At least one Payment Product exists matching `cf_service_1_fee` / `cf_service_2_fee` values
- [ ] E-sign (PROP-Engagement-Agreement) has a trigger: "Document Signed" → moves to `Client — Active`, fires onboarding
- [ ] Manual payment override exists: tag `payment-manual` triggers the same onboarding path as Stripe webhook
- [ ] Test the chain: sign a test document → confirm it moves pipeline stage → confirm WF-07 fires

---

## Section 9: Calendar
*Navigate to: Calendars → CAL-Intro-Call*

- [ ] Calendar exists and is linked in `{{custom_values.intro_call_link}}`
- [ ] Booking confirmation email is set (not blank)
- [ ] No-show trigger is configured (tag or stage move)
- [ ] Cancel trigger: lead goes back to Qualified or Nurture (not lost)
- [ ] Reschedule trigger: confirmation sent, stage stays at Discovery Booked

---

## Section 10: Client Portal
*Navigate to: Sites → Client Portal*

- [ ] Portal is enabled and accessible at the URL in `{{custom_values.portal_url}}`
- [ ] At least these pages exist: Welcome, Project Brief, Timeline, Documents, Milestones
- [ ] Phase-conditional content is working (Phase 1 clients see Phase 1 docs, not Phase 2)
- [ ] Portal invite is sent automatically on `client-active` tag (WF-07)

---

## The 5 Things That Must Work Before Demoing or Selling

Rank these in order. Do not demo until #1–3 are confirmed.

### #1 — WF-03 Scoring is actually running
**How to verify:** Submit a test survey with a hot lead profile. Check if `cf_qualification_score` gets a number and the lead moves to Qualified stage.
**If it doesn't work:** Deploy `wf03_scoring_engine.py` as an n8n Code Node or Cloud Function. Wire WF-03 to POST survey data to it on form submit.

### #2 — Survey field mappings are correct
**How to verify:** Submit test survey → open the contact record → check all 10+ custom fields are populated with the exact answer text.
**If mappings are wrong:** Edit each survey question → Field Mapping → select the correct custom field.

### #3 — Pipeline routing works end-to-end
**How to verify:** Submit three test leads: one hot, one warm, one disqualified. Confirm each lands in the correct stage.
**If routing is wrong:** Check WF-03 branching conditions against the tag/field values the scorer writes.

### #4 — Payment override path works
**How to verify:** Add tag `payment-manual` to a test contact at Proposal Sent stage — confirm it triggers the same onboarding steps as a Stripe payment.
**If it doesn't exist:** Add the manual payment trigger branch to WF-06.

### #5 — SMS opt-out is on every template
**How to verify:** Open each SMS template. Check it ends with "Reply STOP to opt out."
**If missing:** Add it now. This is the only item on this list that is a legal risk, not just a product risk.

---

## Things That Must Work Before Selling to Multiple Builders

Once the above 5 are confirmed, move to these:

1. **Seeded demo account** — a "fake builder" contact with a journey that shows hot/warm/cold routing, a signed proposal, and a report card. Buyers need to see it working, not hear about it.
2. **ROI calculator** — a simple worksheet showing: X leads/month × Y% saved from pre-qualifying = Z hours saved × builder hourly rate = $ saved. Put a number on it.
3. **Weekly builder report** — an automated email showing: leads in, qualified vs cold, calls booked, proposals sent, fees collected. Even a basic version. Retention depends on builders seeing value every week.
4. **Dashboard page** — even 3 pipeline-count widgets. Builders who see their pipeline daily stay on the system.
5. **Branded proposal experience** — the fee acceptance email/document is the moment of truth. It should look polished, not like a default GHL template.

---

## Running the Data Collector Script

The `ghl_audit_collector.py` script can pull live data directly from your account for most of Section 1–4:

```bash
python3 audit/ghl_audit_collector.py --api-key "YOUR-API-KEY" --location-id "YOUR-LOCATION-ID"
```

This will output a JSON file with: all custom fields, workflow list + statuses, pipeline stages, and contact counts per stage. It won't replace manual checking of template content or survey mappings, but it eliminates the guesswork on field existence and workflow status.

---

*Last updated: March 2026 — created to bridge the gap between the architecture audit and live account verification.*
