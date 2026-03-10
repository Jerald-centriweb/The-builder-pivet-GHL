# PreBuild Autopilot — Full Project Context
## For Claude Code: Read This Before Every Session

> **What this file is:** The single source of truth for the PreBuild Autopilot GHL build. Every architectural decision, naming convention, workflow spec, template, and strategic principle lives here. Read it in full before making any changes, building anything new, or auditing the existing subaccount.
>
> **What you're working on:** A GoHighLevel (GHL) subaccount that automates the preconstruction sales funnel for Australian residential builders. It runs as a snapshot-based, single-tenant system — one GHL subaccount per builder client, cloned from a master Factory account.

---

## Table of Contents

1. [Product Overview & Strategy](#1-product-overview--strategy)
2. [Critical Rules — Read First](#2-critical-rules--read-first)
3. [System Architecture](#3-system-architecture)
4. [Pipeline Spec](#4-pipeline-spec)
5. [Data Model — Custom Fields & Tags](#5-data-model--custom-fields--tags)
6. [Custom Values Registry](#6-custom-values-registry)
7. [Workflow Specs (WF-01 to WF-12)](#7-workflow-specs-wf-01-to-wf-12)
8. [Full Template Copy Library](#8-full-template-copy-library)
9. [Naming Conventions](#9-naming-conventions)
10. [GHL Folder Structure](#10-ghl-folder-structure)
11. [Builder Presets (fee_structure)](#11-builder-presets-fee_structure)
12. [Builder Archetypes](#12-builder-archetypes)
13. [QA Checklist](#13-qa-checklist)
14. [Onboarding Process](#14-onboarding-process)
15. [Demo Build Spec](#15-demo-build-spec)
16. [Change Control Rules](#16-change-control-rules)
17. [Strategic Context](#17-strategic-context)
18. [What Changed in the Generic Refactor (v1.1)](#18-what-changed-in-the-generic-refactor-v11)
19. [Open Questions & Known Issues](#19-open-questions--known-issues)

---

## 1. Product Overview & Strategy

### What It Does

PreBuild Autopilot is a done-for-you automated preconstruction sales funnel for Australian residential builders (5–30 homes/year). It automates the journey from raw enquiry through qualification, education, discovery call booking, and paid preliminary agreements — so builders only engage with pre-qualified, deposit-paying clients.

### The Problem It Solves

- Builders spend 10–40 hours quoting for free with low win rates (~10–20%)
- Homeowner budget expectations are chronically unrealistic
- HIA preliminary agreements exist but builders can't sell the value proposition — they come across as demanding money for nothing
- The system educates homeowners first, charges a feasibility fee second — framed as client-beneficial ("Feasibility & Vision Package"), not builder-protective

### Business Model

- Delivered as a GHL subaccount snapshot installed by operator (CentriWeb/Jerald's agency)
- Pricing model (not hardcoded in system): ~$2,500 setup + $297/month per builder
- Operator installs from Factory snapshot → configures Custom Values for each builder → goes live in 5 business days

### Key Partners (Context Only — Not Hardcoded)

- **Price A Plan (PAP):** Preconstruction estimating service. Their 3-stage process and qualifying questions informed the system design. The system is now fully generic and does NOT require PAP.
- **House & Land (HnL):** Builder marketplace providing lead gen. Optional integration, not a hard dependency.

---

## 2. Critical Rules — Read First

These rules govern every action you take in this codebase and GHL account.

### NEVER Do These

| Rule | Why |
|---|---|
| Never use QBE, FQE, Stage 2, Stage 3 terminology | PAP-specific terms. System is now generic. |
| Never hardcode fee amounts | Always use `{{custom_values.service_1_fee}}` syntax |
| Never reference WF-07 as an active workflow | It was removed. WF-06 handles both phases. |
| Never put more than 7 client-facing touchpoints per lead journey | Reduces spam, increases quality |
| Never fork the snapshot per builder | Use `fee_structure` + Custom Values alias layer instead |
| Never make changes directly in a client subaccount | Changes go: Factory → QA → snapshot export → installs |
| Never assume PAP or House & Land partnerships are confirmed | Treat as optional, not required |

### Always Do These

| Rule | Why |
|---|---|
| Use `{{custom_values.xxx}}` syntax for ALL client-facing copy | Builder-configurable alias layer |
| Check `cf_service_phase` before routing proposal/payment logic | Determines Phase 1 vs Phase 2 behaviour |
| Keep internal asset names stable across all builds | Only Custom Values change per builder |
| Exit education sequences when `call-booked` tag is added | Prevents over-messaging |
| Exclude Won / Not Now / Lost from stale reminders | Only active pipeline stages get reminders |
| Include "Reply STOP to opt out" in every SMS template | Required under Australian Spam Act 2003 / ACMA regulations. GHL handles STOP keyword natively. |
| Use `{{custom_values.google_review_link}}` in review SMS, never hardcode placeholders | Prevents broken links in client-facing messages |

### GHL Merge Field Syntax

| Reference | Correct Syntax |
|---|---|
| Contact first name | `{{contact.first_name}}` |
| Contact full name | `{{contact.name}}` |
| Contact phone | `{{contact.phone}}` |
| Builder name | `{{custom_values.builder_name}}` |
| Service 1 name | `{{custom_values.service_1_name}}` |
| Service 1 fee | `{{custom_values.service_1_fee}}` |
| Service 2 name | `{{custom_values.service_2_name}}` |
| Service 2 fee | `{{custom_values.service_2_fee}}` |
| Current phase label | `{{custom_values.current_phase_label}}` |
| Current service fee | `{{custom_values.current_service_fee}}` |
| Agreement title | `{{custom_values.agreement_title}}` |
| Survey link | `{{custom_values.survey_link}}` |
| Calendar link | `{{custom_values.calendar_link}}` |
| Portal link | `{{custom_values.portal_link}}` |
| Testimonial 1 | `{{custom_values.testimonial_1}}` |
| Appointment date | `{{appointment.date}}` |
| Appointment time | `{{appointment.time}}` |
| Proposal link | `{{proposal.link}}` |
| Google review link | `{{custom_values.google_review_link}}` |

---

## 3. System Architecture

### The Two-Account Model

| Account | Purpose | Who Uses It |
|---|---|---|
| **Factory Sub-Account** | Clean canonical build. All new features built here first. Used to export snapshots. | OM/operator only |
| **Demo Sub-Account** | Sales demo showing 2 presets (Paid + No-Fee). Used on sales calls. | Jerald / CentriWeb |
| **Client Sub-Accounts** | Installed from snapshot. Customised via Custom Values during onboarding. | Each builder client |

**Rule:** Changes are NEVER made directly in client subaccounts. All changes go Factory → QA → snapshot export → push to installs.

### Tech Stack

| Component | Tool | Notes |
|---|---|---|
| CRM + Automation | GoHighLevel (GHL) | Core platform — pipeline, workflows, forms, surveys, email/SMS, proposals, portal |
| Payment | Stripe (via GHL) | Each builder uses their own Stripe account |
| Calendar | GHL Calendar | `CAL-Intro-Call` (30-min slots) |
| Client Portal | GHL Memberships | Stage tracker, FAQs, documents |
| Lead Gen Outreach | n8n + Google Sheets | Separate system — cold outreach pipeline, NOT the GHL funnel |
| Lead Research | Perplexity Sonar (in n8n) | Enriches leads before outreach emails |
| Email Sending (outreach) | Gmail + Outlook (4 each) | Round-robin sender rotation in n8n |
| Estimating | Price A Plan (external, optional) | Produces the Budget Estimate/Detailed Quote deliverable. NOT inside GHL. |

### Architecture Principle

GHL handles 85%+ of Phase 1 natively. No custom app, no middleware, no external database in Phase 1. Everything lives in GHL until Phase 2+ limits are hit.

### Snapshot Versioning

| Version | Description |
|---|---|
| v1.0 | First pilot builder installed and functional |
| v1.1 | Bug fixes + generic refactor (no QBE/FQE) + optimisations |
| v1.2 | Review request workflow + missed call text-back (planned) |
| v2.0 | AI chat widget, enhanced portal, Buildxact status sync (Phase 2) |

---

## 4. Pipeline Spec

**Pipeline name in GHL:** `PreBuild Pipeline`

### Active Stages

| # | Stage Name | Moved By | Trigger | What Fires |
|---|---|---|---|---|
| 1 | **New Enquiry** | System (auto) | Form submission / FB Lead Ad / manual entry | WF-01: SMS + email <60 seconds; survey link sent |
| 2 | **Qualified** | System (auto) | WF-03: score ≥80 | Calendar link sent to client; builder internal notification + task |
| 3 | **Nurture** | System (auto) | WF-03: score 50–79 | WF-04: Education sequence starts (7 touches over 10 days) |
| 4 | **Discovery Booked** | System (auto) | Calendar event created | WF-05: Confirmation SMS/email; 24hr reminder; builder task |
| 5 | **Proposal Sent** | Builder (manual) | Builder moves after discovery call | WF-06: PROP-Engagement-Agreement email sent; e-sign + Stripe link |
| 6 | **Engaged** | System (auto) | Stripe payment confirmed | WF-08: Portal access granted; welcome email/SMS; `portal-active` tag |
| 7 | **Delivered** | Builder (manual) | Builder marks when service is delivered | WF-11: Task for builder — "Follow up: does client want Phase 2?" |
| 8 | **Won** | Builder (manual) | Builder marks when contract signed | WF-12: Review request queued for 14 days |

### Non-Active Stages

| Stage | Entry | What Fires | Re-entry |
|---|---|---|---|
| **Not Now** | Auto: score <50 (WF-03). Auto: survey abandoned after 10 days (WF-02). Manual: builder parks. | Polite decline email. Tag: `lead-cold`. Quarterly long-term nurture. No stale reminders. | Builder manually re-opens to any active stage. |
| **Lost** | Builder moves manually only. | Optional exit survey. Tag: `stage-lost`. `cf_lost_reason` populated. No further automation. | Can be re-opened; requires manual move + removal of `stage-lost` tag. |

### Two-Tier Fee Cycle (How the Pipeline is Traversed Twice)

For builders with `fee_structure = two_tier`, the pipeline runs twice:

**Round 1 — Phase 1 (e.g., Budget Estimate):**
```
New Enquiry → Qualified/Nurture → Discovery Booked → Proposal Sent → Engaged → Delivered
```

**Round 2 — Phase 2 (e.g., Detailed Quote):**
```
Delivered → Proposal Sent (builder manually cycles back) → Engaged → Delivered → Won
```

The `cf_service_phase` field on Contact tracks which pass:
- `not_started` → `phase_1` → `phase_2` → `complete`

WF-06 reads this field to determine which proposal template content, which fee amount, and which portal content to use. There is **one** proposal template (`PROP-Engagement-Agreement`) that conditionally renders for either phase.

### Single-Tier and No-Fee Flows

- **single_tier:** Same pipeline, one pass only through Proposal Sent → Engaged → Delivered → Won. WF-06 Phase 2 conditional branch disabled.
- **no_fee:** Proposal Sent and Engaged stages are skipped. Pipeline goes Qualified/Nurture → Discovery Booked → Delivered (repurposed as "Quote Sent") → Won. No Stripe, no portal, no proposal.

---

## 5. Data Model — Custom Fields & Tags

### Contact Custom Fields

All fields prefixed `cf_` — stored on GHL Contact record.

| Field Name | Key | Type | Values | Set By | Notes |
|---|---|---|---|---|---|
| Qualification Score | `cf_qualification_score` | Number | 0–100 | WF-03 (auto) | Calculated from survey. Drives routing. |
| Lead Temperature | `cf_lead_temperature` | Dropdown | `hot` / `warm` / `cold` | WF-03 (auto) | Mirror of tag for reporting |
| Budget Range | `cf_budget_range` | Dropdown | Under $300K / $300–500K / $500–800K / $800K–1.2M / $1.2M+ | Survey (auto) | Under $300K is a hard disqualifier |
| Project Type | `cf_project_type` | Dropdown | New Build / Renovation / Extension / Knockdown Rebuild | Survey (auto) | |
| Land Status | `cf_land_status` | Dropdown | Own Land / Under Contract / Looking | Survey (auto) | Own Land = highest score |
| Site Address | `cf_site_address` | Text | Free text | Survey (auto) | Used in proposal merge fields |
| Timeline | `cf_timeline` | Dropdown | ASAP / 3–6 months / 6–12 months / 12+ months | Survey (auto) | |
| Financing Status | `cf_financing_status` | Dropdown | Pre-approved / In progress / Not started / Cash buyer | Survey (auto) | |
| Decision Maker | `cf_decision_maker` | Dropdown | Yes / Shared / Other | Survey (auto) | |
| Open to Fee | `cf_open_to_fee` | Dropdown | Yes / Needs more info / No | Survey (auto) | "No" = hard disqualifier |
| Communication Preference | `cf_communication_preference` | Dropdown | Email / SMS / Phone / Any | Survey (auto) | 0 pts — informational only |
| Service Phase | `cf_service_phase` | Dropdown | `not_started` / `phase_1` / `phase_2` / `complete` | WF-06 (auto) | Critical: drives WF-06 conditional logic |
| Service 1 Fee | `cf_service_1_fee` | Number | e.g., 600 | Onboarding (manual) | Mirrors `custom_values.service_1_fee`. Used in Stripe. |
| Service 2 Fee | `cf_service_2_fee` | Number | e.g., 6600 | Onboarding (manual) | Same for Phase 2 |
| Lost Reason | `cf_lost_reason` | Dropdown | Budget too low / Chose competitor / Timeline changed / No response / Scope mismatch / Other | Builder (manual) | Set when moving to Lost |
| How Heard | `cf_how_heard` | Dropdown | Google Search / Facebook / Instagram / Referral (friend/family) / Referral (professional) / Builder Website / House & Land / Other | Survey (auto) | Lead source attribution — 0 pts, informational only |
| Partner Name | `cf_partner_name` | Text | Free text | Survey (auto) | For couple coordination workflow |
| Partner Email | `cf_partner_email` | Email | Free text | Survey (auto) | For partner notification |
| Design Status | `cf_design_status` | Dropdown | Plans Ready / Concept Only / Nothing Yet | Survey (auto) | Informs builder prep for discovery call |
| Prior Quotes | `cf_prior_quotes` | Dropdown | First Contact / 1-2 Builders / 3+ Builders | Survey (auto) | Competitive landscape signal |
| Site Challenges | `cf_site_challenges` | Dropdown | None / Some / Significant | Survey (auto) | Risk factor for project complexity |
| Additional Notes | `cf_additional_notes` | Text (multi-line) | Free text | Survey (auto) | Open-ended project context from homeowner |

### Custom Object: Project (Optional)

Available on all GHL plans as of Oct 2025. Use when builder expects multi-project clients or needs richer dashboard KPIs. Linked to Contact (one-to-many).

**Fields on Project object:**
- Project Name, Site Address, Budget Range, Plan Type, Land Status, Timeline, Qualification Score
- Service Phase: `Phase 1 Active` / `Phase 1 Delivered` / `Phase 2 Active` / `Phase 2 Delivered`

**Graceful degradation rule:** All 12 core workflows must function using Contact fields only. Project object is additive, not required.

### Tags Schema

| Tag | Set By | Meaning |
|---|---|---|
| `lead-hot` | WF-03 (auto) | Score ≥80 |
| `lead-warm` | WF-03 (auto) | Score 50–79 |
| `lead-cold` | WF-03 (auto) | Score <50 |
| `survey-pending` | WF-01 (auto) | Survey link sent, awaiting completion |
| `survey-completed` | WF-03 (auto) | Survey submitted |
| `survey-abandoned` | WF-02 (auto) | No completion after 10 days |
| `call-booked` | WF-05 (auto) | Calendar event created — exits education sequence |
| `proposal-sent` | WF-06 (auto) | Engagement proposal delivered |
| `payment-received` | WF-06 (auto) | Stripe payment confirmed |
| `portal-active` | WF-08 (auto) | Portal access granted |
| `review-requested` | WF-12 (auto) | Review request sent — prevents duplicates |
| `stage-won` | WF (auto on Won) | Contact reached Won stage |
| `stage-lost` | Builder (manual) | Contact moved to Lost |
| `fee-tier-single` | Onboarding (manual) | Builder uses single-tier fee structure |
| `fee-tier-two` | Onboarding (manual) | Builder uses two-tier fee structure (default, explicit for reporting) |
| `fee-tier-none` | Onboarding (manual) | Builder uses no-fee structure |
| `payment-manual` | Builder/OM (manual) | Off-platform payment confirmed — triggers same automation as Stripe webhook |

---

## 6. Custom Values Registry

> Custom Values = the alias layer. Internal asset names never change. These values power ALL client-facing copy in emails, SMS, proposals, and the portal. Every value is set during builder onboarding.

### Required (No Defaults — Must Be Set Per Builder)

| Key | Example | Used In |
|---|---|---|
| `builder_name` | Smith Building Co | All templates, portal, proposals |
| `builder_phone` | 0412 345 678 | Email footers, proposals |
| `builder_abn` | 12 345 678 901 | Proposals/agreements |
| `service_1_fee` | $550 inc GST | PROP-Engagement-Agreement, Stripe |
| `service_2_fee` | $6,600 inc GST | PROP-Engagement-Agreement, Stripe (Phase 2) |
| `survey_link` | GHL survey URL | WF-01, WF-02 templates |
| `calendar_link` | GHL calendar URL | Hot lead routing, survey reminders, education CTAs |
| `portal_link` | GHL portal URL | WF-08 welcome email/SMS |
| `google_review_link` | Google Business Profile review URL | WF-12 SMS-WIN-ReviewRequest |

### Configurable (Have Defaults — Override Per Builder)

| Key | Default Value | Notes |
|---|---|---|
| `fee_structure` | `two_tier` | `two_tier` / `single_tier` / `no_fee` — drives workflow branching |
| `service_1_name` | `Budget Estimate` | Builder alternatives: "Concept Estimate", "Preliminary Pricing", "Feasibility Report" |
| `service_1_fee_label` | `Budget Estimate fee` | Used in proposals and emails |
| `service_2_name` | `Detailed Quote` | Builder alternatives: "Construction Tender", "Fixed-Price Quote", "Full Quantity Estimate" |
| `service_2_fee_label` | `Detailed Quote fee` | Used in proposals and emails |
| `phase_1_label` | `Phase 1 – Budget Assessment` | Portal and email display |
| `phase_2_label` | `Phase 2 – Detailed Pricing` | Portal and email display |
| `process_description` | `our structured two-stage pre-construction process` | Used in intro emails/SMS |
| `process_stage_count` | `2` | `2` for two_tier, `1` for single_tier, `0` for no_fee |
| `agreement_title` | `Pre-Construction Services Agreement` | Proposal header |
| `refund_policy` | `Fees are fully refunded if we proceed to a building contract together.` | Optional — not all builders offer this |
| `refund_clause` | ` (fully refundable if we proceed to contract)` | Inline in proposal copy |
| `sample_doc_1_label` | `Sample Budget Estimate` | Education email attachment label |
| `sample_doc_2_label` | `Sample Detailed Quote` | Education email attachment label |
| `testimonial_1` | (builder provides) | ET-EDU-04-Testimonial |
| `testimonial_1_name` | (builder provides) | ET-EDU-04-Testimonial |
| `testimonial_2` | (builder provides) | ET-EDU-04-Testimonial |
| `testimonial_2_name` | (builder provides) | ET-EDU-04-Testimonial |

### Dynamic (Set by Workflow Based on cf_service_phase)

These are NOT manually configured — workflows update them based on `cf_service_phase`.

| Key | Phase 1 Value | Phase 2 Value |
|---|---|---|
| `current_phase_label` | value of `phase_1_label` | value of `phase_2_label` |
| `current_service_description` | Phase 1 scope description | Phase 2 scope description |
| `current_service_fee` | value of `service_1_fee` | value of `service_2_fee` |
| `current_service_scope` | "Introductory call, preliminary consultation, budget estimate report." | "Site visits, detailed design consultation, subcontractor engagement, itemised estimate, delivery meeting, revision meeting, documentation preparation." |
| `current_phase_next_steps` | "We'll schedule your preliminary design consultation, then prepare your {{service_1_name}}." | "We'll schedule your site visit, then begin work on your {{service_2_name}}." |

---

## 7. Workflow Specs (WF-01 to WF-12)

> WF-07 was **removed** in v1.1. It has been merged into WF-06 via `cf_service_phase` conditional logic. Do not recreate it.

### WF-01: Speed-to-Lead

| Element | Detail |
|---|---|
| **Trigger** | Contact created (any source: form submission, FB Lead Ad, manual entry) |
| **Action 1** | Send SMS: `SMS-STL-Welcome` (immediate, <60 seconds) |
| **Action 2** | Send Email: `ET-STL-01-Welcome` (immediate, <60 seconds) |
| **Action 3** | Add tag: `survey-pending` |
| **Action 4** | Internal notification to builder (inline — not a template) |
| **Edge case** | If no email → send SMS only. If no phone → send email only. If neither → create task for builder: "Contact {{contact.name}} manually — no email or phone on file." |
| **QA test** | Submit test form → SMS received <60 sec → email received → builder notification visible in dashboard |

---

### WF-02: Survey Invitation + Reminders

| Element | Detail |
|---|---|
| **Trigger** | Tag `survey-pending` added AND time elapsed (see sequence below) |
| **Condition** | Tag `survey-completed` NOT present |
| **Sequence** | Day 3 (72hrs): SMS `SMS-SRV-Reminder-1` → Day 5 (120hrs): Email `ET-SRV-Reminder-2` → Day 8 (192hrs): SMS `SMS-SRV-Final` → Day 10: If still incomplete → remove `survey-pending`, add `survey-abandoned`, move to **Not Now** |
| **Edge case** | If contact replies to any SMS with a question → create task for builder: "{{contact.name}} replied to survey reminder — follow up manually" |
| **Exit** | Tag `survey-completed` added at any point stops the sequence |
| **QA test** | Create contact with `survey-pending` → verify first reminder fires at 72hrs → verify sequence stops on survey completion mid-sequence |

---

### WF-03: Scoring + Routing

| Element | Detail |
|---|---|
| **Trigger** | Survey `SRV-Qualification` submitted |
| **Action 1** | Remove `survey-pending`; add `survey-completed` |
| **Action 2** | Calculate score using workflow math (see scoring rubric below) |
| **Action 3** | Set `cf_qualification_score` = calculated total |
| **Action 4** | Apply hard disqualifier overrides (see below) |
| **Action 5a** | Score ≥80 AND no disqualifier → tag `lead-hot`, move to **Qualified**, send `SMS-QUAL-Hot-BookCall` + `ET-QUAL-Hot-BookCall`, builder notification + task |
| **Action 5b** | Score 50–79 AND no disqualifier → tag `lead-warm`, move to **Nurture**, start education sequence |
| **Action 5c** | Score <50 OR disqualifier triggered → tag `lead-cold`, move to **Not Now**, send polite decline |
| **Action 6** | Internal notification to builder: "{{contact.name}} scored {{cf_qualification_score}} — tagged {{cf_lead_temperature}}" |
| **Edge case** | Survey submitted with incomplete required fields → create task: "Review incomplete survey from {{contact.name}}" |
| **QA test** | Submit survey for Hot (≥80) → verify correct tag + stage. Repeat for Warm and Cold. Test each hard disqualifier. |

#### Scoring Rubric

| # | Question | Scoring |
|---|---|---|
| 1 | Project type | New Build=10, Knockdown Rebuild=10, Extension=8, Renovation=6 |
| 2 | Budget range | Under $300K=**HARD DISQUALIFIER**, $300–500K=5, $500–800K=10, $800K–1.2M=15, $1.2M+=15 |
| 3 | Land status | Own Land=15, Under Contract=12, Looking=5 |
| 4 | Timeline | ASAP=15, 3–6 months=12, 6–12 months=8, 12+ months=3 |
| 5 | Financing | Pre-approved=15, Cash buyer=15, Using broker=12, Not started=6 |
| 6 | Prior quotes | First contact=10, 1–2 builders=10, 3+ builders=5 |
| 7 | Design status | Plans ready=15, Concept only=10, Nothing yet=5 |
| 8 | Referred by | Existing client=15, Professional=12, Other=8, Online ad=5 |
| 9 | Decision maker? | Yes=10, Shared=8, Other=3 |
| 10 | Open to fee? | Yes=15, Need more info=8, **No=HARD DISQUALIFIER** |
| 11 | Site challenges | No challenges=10, Some=7, Significant=3 |
| 12 | Number of builders | 1–2=10, First=10, 3+=5 |
| 13 | Communication preference | 0 pts — informational only, maps to `cf_communication_preference` |
| 14 | How did you hear about us? | 0 pts — informational only, maps to `cf_how_heard`. Used for lead source attribution and marketing ROI analysis. |
| 15 | Will you be making this decision with a partner/spouse? | 0 pts — if Yes, collect partner name + email/phone. Maps to `cf_partner_name`, `cf_partner_email`. Used for couple coordination. |

**Hard Disqualifiers:** Budget under $300K OR "No" to preconstruction fee → routes to Not Now regardless of all other scores.

**Score bands:** Hot ≥80 | Warm 50–79 | Cold <50

---

### WF-04: Education Sequence

| Element | Detail |
|---|---|
| **Trigger** | Tag `lead-warm` added (or manually enrolled by builder for any lead) |
| **Condition** | Pipeline stage = Nurture |
| **Exit condition** | Tag `call-booked` added OR pipeline moves past Nurture |
| **Sequence** | Touch 1 (Day 0): Email `ET-EDU-01-Process-Overview` → Touch 2 (Day 1): SMS `SMS-EDU-01-Checkin` → Touch 3 (Day 3): Email `ET-EDU-02-Service-1-Explainer` → Touch 4 (Day 5): Email `ET-EDU-03-Service-2-Explainer` → Touch 5 (Day 7): Email `ET-EDU-04-Testimonial` → Touch 6 (Day 9): SMS `SMS-EDU-02-CTA` → Touch 7 (Day 10): Email `ET-EDU-05-CTA-Next-Step` |
| **Post-sequence** | If no engagement after Day 10 → remains in Nurture for builder manual follow-up. No auto-move. |
| **QA test** | Enrol test contact → verify all 7 touches fire on schedule → book a call mid-sequence → verify remaining emails do NOT send |

---

### WF-05: Booking Flow

| Element | Detail |
|---|---|
| **Trigger** | Calendar event created (`CAL-Intro-Call`) |
| **Action 1** | Add tag `call-booked`; remove contact from education sequence (WF-04 exit condition) |
| **Action 2** | Move pipeline to **Discovery Booked** |
| **Action 3** | Send confirmation SMS: "Confirmed! Your call with {{custom_values.builder_name}} is on {{appointment.date}} at {{appointment.time}}. We'll call you on {{contact.phone}}." |
| **Action 4** | Send confirmation email: `ET-BOOK-Confirmation` |
| **Action 5** | Create builder task: "Prep for call with {{contact.name}} — review their survey answers before the call" |
| **Wait** | 24 hours before appointment |
| **Action 6** | Send reminder SMS: "Reminder: your call with {{custom_values.builder_name}} is tomorrow at {{appointment.time}}. Looking forward to chatting!" |
| **No-show handling** | If appointment time passes with no status update → send SMS to homeowner: "Hi {{contact.first_name}}, we missed you on today's call. No worries — would you like to reschedule? {{custom_values.calendar_link}} — {{custom_values.builder_name}}. Reply STOP to opt out." + create task for builder: "{{contact.name}} may not have shown — confirm what happened and update pipeline" |
| **Cancel handling** | Calendar event cancelled → remove `call-booked` tag (re-enables education sequence if still in Nurture) → create builder task: "{{contact.name}} cancelled their intro call — follow up" → if pipeline = Discovery Booked, consider moving back to previous stage |
| **Reschedule handling** | Calendar event rescheduled → send updated confirmation SMS with new date/time → update builder task with new appointment details |
| **QA test** | Book test calendar event → verify confirmation SMS + email → verify 24hr reminder fires → verify builder task created |

---

### WF-06: Proposal + E-Sign + Payment

> **This is the most complex workflow.** It handles BOTH Phase 1 and Phase 2 via `cf_service_phase` conditional logic. WF-07 was merged into this workflow — do not recreate WF-07.

| Element | Detail |
|---|---|
| **Trigger** | Pipeline stage = **Proposal Sent** (builder moves manually after discovery call) |
| **Action 1** | Check `cf_service_phase`: if `not_started` → set to `phase_1`. If `phase_1` already complete → set to `phase_2`. |
| **Action 2** | Send email `ET-PROP-Agreement-Sent` (single template — reads `current_service_description` and `current_service_fee` which are set from `cf_service_phase`) |
| **Action 3** | Send SMS `SMS-PROP-Sent` |
| **Action 4** | Add tag `proposal-sent` |
| **Wait** | For e-signature event |
| **Action 5** | On signature received → trigger Stripe payment link for amount `cf_service_1_fee` (Phase 1) or `cf_service_2_fee` (Phase 2) |
| **Action 6** | Send 48hr payment reminder if not yet paid: `ET-PROP-Reminder-48hr` |
| **Wait** | For Stripe payment confirmed webhook |
| **Action 7** | On payment confirmed → add tag `payment-received` → move pipeline to **Engaged** |
| **Action 8** | Send payment confirmation email `ET-PAY-Confirmation` + SMS `SMS-PAY-Confirmation` |
| **Action 9** | Builder internal notification: "{{contact.name}} has paid their {{custom_values.current_service_fee_label}} — project is active." |
| **Payment failure** | If Stripe payment fails → send retry email → create builder task |
| **Manual payment override** | If tag `payment-manual` is added by builder/OM (for bank transfer, cheque, cash payments) → execute same actions as Stripe confirmation: add `payment-received` tag → move pipeline to Engaged → send confirmation email/SMS → trigger WF-08 portal access. This ensures automation works regardless of payment method. |
| **QA test** | Move contact to Proposal Sent with `cf_service_phase = not_started` → verify Phase 1 proposal sends. Repeat with `cf_service_phase = phase_1` → verify Phase 2 content. Sign → verify Stripe link. Pay → verify pipeline moves to Engaged. |

---

### WF-07: REMOVED

WF-07 (formerly "Stage 3 — Proposal + E-Sign + Payment") was removed in v1.1. Its functionality is entirely covered by WF-06's `cf_service_phase` conditional logic. **Do not recreate this workflow.**

---

### WF-08: Portal Welcome

| Element | Detail |
|---|---|
| **Trigger** | Pipeline stage = **Engaged** |
| **Action 1** | Add tag `portal-active` |
| **Action 2** | Grant GHL Membership/Portal access to contact |
| **Action 3** | Send email `ET-PORTAL-Welcome` |
| **Action 4** | Send SMS `SMS-PAY-Confirmation` (if not already sent by WF-06) |
| **Action 5** | If Custom Object "Project" is enabled → update Project.Service Phase to match `cf_service_phase` |
| **QA test** | Move contact to Engaged → verify portal access granted → verify welcome email/SMS sent → verify Portal-Welcome page renders |

---

### WF-09: Stage Update Notifications

| Element | Detail |
|---|---|
| **Trigger** | Any pipeline stage change |
| **Action** | Internal notification to builder for every stage move. All copy uses Custom Values — no QBE/FQE terms. |
| **Examples** | "{{contact.name}} has moved to Qualified — they're a hot lead. Book a call now." / "{{contact.name}} paid their {{custom_values.current_service_fee_label}} — project is active." |

---

### WF-10: Stale Lead Reminders

| Element | Detail |
|---|---|
| **Trigger** | 7 days with no pipeline stage update |
| **Condition** | Pipeline stage is NOT Won / Not Now / Lost |
| **Action** | SMS to builder: "Heads up — {{contact.name}} hasn't had a pipeline update in 7 days. Review their contact and take action." |
| **QA test** | Create contact, set stage, wait 7 days without update → verify SMS fires. Confirm it does NOT fire for Won/Not Now/Lost. |

---

### WF-11: Builder Internal Tasks

| Element | Detail |
|---|---|
| **Trigger** | Key pipeline stage transitions |
| **Actions** | Creates manual action tasks for builder at critical junctures: after survey (review scores), after discovery call (trigger proposal), after Delivered (ask client about Phase 2), after Won (handover to construction team) |
| **Task examples** | "Review {{contact.name}}'s survey answers (score: {{cf_qualification_score}})" / "Follow up with {{contact.name}} — do they want to proceed to {{custom_values.service_2_name}}?" |

---

### WF-12: Review Request

| Element | Detail |
|---|---|
| **Trigger** | Pipeline stage = **Won** AND 14 days elapsed |
| **Condition** | Tag `review-requested` NOT present |
| **Action 1** | Add tag `review-requested` (prevents duplicate sends) |
| **Action 2** | Send SMS `SMS-WIN-ReviewRequest` |
| **QA test** | Move contact to Won → wait 14 days → verify review SMS fires once → move another contact to Won → verify second SMS also fires |

---

## 8. Full Template Copy Library

All templates use `{{custom_values.xxx}}` merge fields. No hardcoded builder names, fees, or terminology.

---

### Speed-to-Lead Templates

**`SMS-STL-Welcome`**
```
Hi {{contact.first_name}}, thanks for reaching out to {{custom_values.builder_name}}! We'd love to help with your building project. To get started, please take our quick project questionnaire (about 3 mins): {{custom_values.survey_link}} — The {{custom_values.builder_name}} Team. Reply STOP to opt out.
```

**`ET-STL-01-Welcome`**
Subject: `Thanks for your enquiry, {{contact.first_name}} — here's what happens next`
```
Hi {{contact.first_name}},

Thank you for reaching out to {{custom_values.builder_name}}. We're excited about the possibility of bringing your project to life.

To make sure we're the right fit for each other, we start with a quick project questionnaire. It takes about 3 minutes and helps us understand your plans, priorities, and timeline.

→ Complete your project questionnaire here: {{custom_values.survey_link}}

Once we review your answers, we'll be in touch with next steps tailored to your project.

Looking forward to learning more about what you're planning.

Warm regards,
{{custom_values.builder_name}}
{{custom_values.builder_phone}}
```

---

### Survey Reminder Templates

**`SMS-SRV-Reminder-1`** (72hrs)
```
Hey {{contact.first_name}}, just checking in — have you had a chance to complete our quick project questionnaire? Here's the link: {{custom_values.survey_link}} — {{custom_values.builder_name}}. Reply STOP to opt out.
```

**`ET-SRV-Reminder-2`** (120hrs)
Subject: `Quick reminder — your project questionnaire`
```
Hi {{contact.first_name}},

We noticed you haven't had a chance to complete our project questionnaire yet. No worries — it only takes about 3 minutes, and it helps us understand your project so we can give you the most relevant advice.

→ Complete it here: {{custom_values.survey_link}}

Prefer to chat instead? You can book a quick call with us here: {{custom_values.calendar_link}}

{{custom_values.builder_name}}
```

**`SMS-SRV-Final`** (192hrs)
```
Hi {{contact.first_name}}, last nudge from us! We'd love to help with your building project. Complete our 3-min questionnaire here: {{custom_values.survey_link}} — or reply CALL and we'll ring you. — {{custom_values.builder_name}}. Reply STOP to opt out.
```

---

### Qualification Routing Templates

**`SMS-QUAL-Hot-BookCall`** (fires immediately on score ≥80)
```
Great news {{contact.first_name}}! Based on your project details, we'd love to chat. Book a quick call here: {{custom_values.calendar_link}} — {{custom_values.builder_name}}. Reply STOP to opt out.
```

**`ET-QUAL-Hot-BookCall`** (fires immediately on score ≥80)
Subject: `Your project looks like a great fit — let's talk`
```
Hi {{contact.first_name}},

Thanks for completing our questionnaire. Based on your answers, your project sounds like a great fit for what we do.

The next step is a quick intro call — just 30 minutes to talk through your plans and see how we can help.

→ Book your call here: {{custom_values.calendar_link}}

Talk soon,
{{custom_values.builder_name}}
{{custom_values.builder_phone}}
```

---

### Education Sequence Templates

**`ET-EDU-01-Process-Overview`** (Day 0 — Touch 1)
Subject: `Here's how {{custom_values.builder_name}} turns your vision into reality`
```
Hi {{contact.first_name}},

Building a home is one of the biggest decisions you'll make. That's why we've developed {{custom_values.process_description}} to make sure every dollar is accounted for before construction begins.

Here's how it works:

Stage 1 — Getting to Know Each Other
We learn about your project, priorities, and budget through a quick questionnaire and an intro call. No obligations, no surprises.

Stage 2 — {{custom_values.service_1_name}}
We prepare a {{custom_values.service_1_name}} — a professional estimate of your project cost based on your design brief. This gives you a realistic number to work with before spending money on detailed drawings.

Stage 3 — {{custom_values.service_2_name}} *(Include this section only for two_tier builders — use workflow If/Then branch on fee_structure tag to send variant without this section for single_tier/no_fee)*
Once the budget checks out, we move into a {{custom_values.service_2_name}} — a fully itemised estimate with subcontractor and supplier pricing. This is what you need to sign a construction contract.

We've attached a one-page overview so you can see exactly what's included at each stage.

→ Ready to take the next step? Book a call: {{custom_values.calendar_link}}

{{custom_values.builder_name}}
```

**`SMS-EDU-01-Checkin`** (Day 1 — Touch 2)
```
Hey {{contact.first_name}}, did you get a chance to read about our process? Any questions, just reply to this message — we're here to help. — {{custom_values.builder_name}}. Reply STOP to opt out.
```

**`ET-EDU-02-Service-1-Explainer`** (Day 3 — Touch 3)
Subject: `What's included in a {{custom_values.service_1_name}}?`
```
Hi {{contact.first_name}},

One question we hear often: "What exactly do I get for the {{custom_values.service_1_fee_label}}?"

Here's what's included in our {{custom_values.service_1_name}}:
— A preliminary design consultation (introductory call or meeting)
— Review of your plans, site, and design brief
— Professional cost estimate based on current market pricing
— Written report covering: overall budget range, key cost drivers, value-engineering options
— Delivery meeting to walk you through the numbers

The {{custom_values.service_1_fee_label}} is {{custom_values.service_1_fee}} (inc. GST){{custom_values.refund_clause}}.

We've attached a sample {{custom_values.sample_doc_1_label}} so you can see exactly what you'll receive.

→ Ready to get started? Book your intro call: {{custom_values.calendar_link}}

{{custom_values.builder_name}}
```

**`ET-EDU-03-Service-2-Explainer`** (Day 5 — Touch 4)
Subject: `From budget range to fixed price — here's what the next stage involves`
```
Hi {{contact.first_name}},

Once your {{custom_values.service_1_name}} confirms the budget is in the right range, the next step is our {{custom_values.service_2_name}}. This is where we go into full detail.

Here's what's included:
— Site visit and detailed design consultation (1–2 hours)
— Consultation with architects and designers as needed
— Engaging consultants (soil tests, energy reports, etc.) if required
— A fully itemised estimate covering every element of your build
— Pricing from subcontractors and suppliers
— A face-to-face delivery meeting to walk through every line
— A revision meeting for design and cost-saving suggestions if needed
— Preparation of all documentation to proceed to contract

We've attached a sample {{custom_values.sample_doc_2_label}} so you can see the level of detail involved.

The {{custom_values.service_2_fee_label}} is {{custom_values.service_2_fee}} (inc. GST){{custom_values.refund_clause}}.

{{custom_values.builder_name}}
```

**`ET-EDU-04-Testimonial`** (Day 7 — Touch 5)
Subject: `What our clients say about working with us`
```
Hi {{contact.first_name}},

Don't just take our word for it. Here's what recent clients have said:

"{{custom_values.testimonial_1}}"
— {{custom_values.testimonial_1_name}}

"{{custom_values.testimonial_2}}"
— {{custom_values.testimonial_2_name}}

Our process is designed to give you confidence and clarity before you commit to building. Ready to take the next step?

→ Book a call with us here: {{custom_values.calendar_link}}

{{custom_values.builder_name}}
```

**`SMS-EDU-02-CTA`** (Day 9 — Touch 6)
```
Hey {{contact.first_name}}, we've shared everything about our process over the past week. Ready to chat? Book a quick call: {{custom_values.calendar_link}} — {{custom_values.builder_name}}. Reply STOP to opt out.
```

**`ET-EDU-05-CTA-Next-Step`** (Day 10 — Touch 7)
Subject: `Ready when you are, {{contact.first_name}}`
```
Hi {{contact.first_name}},

Over the past week, we've shared how our process works, what's included in our {{custom_values.service_1_name}} and {{custom_values.service_2_name}}, and what our clients think.

If you're ready to explore whether we're the right fit for your project, the next step is a conversation — no pressure, no commitment.

→ Book a call: {{custom_values.calendar_link}}

Or simply reply to this email with your questions.

{{custom_values.builder_name}}
```

---

### Proposal Templates

**`ET-PROP-Agreement-Sent`** (triggered by WF-06 when pipeline = Proposal Sent)
Subject: `Your {{custom_values.agreement_title}} — {{custom_values.builder_name}}`
```
Hi {{contact.first_name}},

Great news — based on our conversation, we'd love to move forward with your project at {{cf_site_address}}.

Please review and sign the attached {{custom_values.agreement_title}}. Once signed, you'll be directed to our secure payment page.

What you're getting:
{{custom_values.current_service_description}}

Fee: {{custom_values.current_service_fee}} (inc. GST){{custom_values.refund_clause}}

→ Review and sign your agreement here: {{proposal.link}}

Once your payment is confirmed, we'll set up your personal project portal and get started.

{{custom_values.builder_name}}
```

> **Note:** This is ONE template that handles BOTH Phase 1 and Phase 2. The `current_service_description` and `current_service_fee` merge fields are set by WF-06 based on `cf_service_phase`. Do not create a second proposal template.

**`SMS-PROP-Sent`**
```
Hi {{contact.first_name}}, we've just sent through your {{custom_values.agreement_title}} for your project. Please check your email to review and sign. Any questions, just reply here! — {{custom_values.builder_name}}. Reply STOP to opt out.
```

**`ET-PROP-Reminder-48hr`** (if unsigned after 48hrs)
Subject: `Just checking in — your agreement is waiting`
```
Hi {{contact.first_name}},

Just a quick reminder that your {{custom_values.agreement_title}} is still waiting for your signature.

→ Sign here: {{proposal.link}}

Any questions before signing? Reply to this email and we'll get back to you quickly.

{{custom_values.builder_name}}
```

---

### Payment Confirmation Templates

**`ET-PAY-Confirmation`**
Subject: `Payment confirmed — we're getting started on your project`
```
Hi {{contact.first_name}},

We've received your payment of {{custom_values.current_service_fee}} — thank you for choosing {{custom_values.builder_name}}.

Here's what happens next:
{{custom_values.current_phase_next_steps}}

You now have access to your personal project portal:
→ Access your portal here: {{custom_values.portal_link}}

We're excited to get started.

{{custom_values.builder_name}}
```

**`SMS-PAY-Confirmation`**
```
Payment received — thank you! Your {{custom_values.builder_name}} project portal is now live: {{custom_values.portal_link}}. Reply STOP to opt out.
```

---

### Portal Welcome Templates

**`ET-PORTAL-Welcome`**
Subject: `Welcome to your {{custom_values.builder_name}} project portal`
```
Hi {{contact.first_name}},

Your personal project portal is now live.

→ Log in here: {{custom_values.portal_link}}

You'll see your current project status and what's coming next. We'll keep your portal updated as things progress.

Questions at any time? Reply to this email or call {{custom_values.builder_phone}}.

{{custom_values.builder_name}}
```

---

### Review Request Template

**`SMS-WIN-ReviewRequest`** (fires 14 days after Won stage)
```
Hi {{contact.first_name}}, it's been great working with you on your project. If you're happy with the process, we'd love it if you could leave us a quick Google review — it helps other homeowners find us: {{custom_values.google_review_link}}. Thanks so much! — {{custom_values.builder_name}}. Reply STOP to opt out.
```

---

## 9. Naming Conventions

> These names are LOCKED. Never change internal asset names in client installs. Only Custom Values change per builder.

| Asset Type | Convention | Examples |
|---|---|---|
| Pipeline | `PreBuild Pipeline` | `PreBuild Pipeline` |
| Workflows | `WF-[##]-[Description]` | `WF-01-Speed-to-Lead`, `WF-03-Scoring-Routing` |
| Forms | `FRM-[Description]` | `FRM-Lead-Intake`, `FRM-Pre-Call` |
| Surveys | `SRV-[Description]` | `SRV-Qualification` |
| Email Templates | `ET-[Stage]-[##]-[Description]` | `ET-STL-01-Welcome`, `ET-EDU-01-Process-Overview`, `ET-EDU-02-Service-1-Explainer` |
| SMS Templates | `SMS-[Stage]-[Description]` | `SMS-STL-Welcome`, `SMS-SRV-Reminder-1`, `SMS-EDU-01-Checkin` |
| Proposals | `PROP-[Description]` | `PROP-Engagement-Agreement` — single template only |
| Portal Pages | `Portal-[Description]` | `Portal-Welcome`, `Portal-Phase-1`, `Portal-Phase-2`, `Portal-Documents`, `Portal-FAQ` |
| Tags | `[category]-[value]` | `lead-hot`, `survey-pending`, `stage-won`, `fee-tier-none` |
| Custom Fields | `cf_[snake_case]` | `cf_qualification_score`, `cf_service_phase`, `cf_budget_range` |
| Custom Values | `[snake_case]` | `service_1_name`, `builder_name`, `fee_structure` |
| Custom Object | `Project` | `Project` |
| Calendar | `CAL-[Description]` | `CAL-Intro-Call` |

### Stage Abbreviations (for Template Names)

| Abbreviation | Stage / Context |
|---|---|
| `STL` | Speed-to-Lead (initial enquiry) |
| `SRV` | Survey reminders |
| `QUAL` | Qualification routing |
| `EDU` | Education sequence |
| `BOOK` | Booking / discovery call |
| `PROP` | Proposal / agreement |
| `PAY` | Payment confirmation |
| `PORTAL` | Portal welcome |
| `STALE` | Stale lead reminders |
| `DEL` | Delivery (service delivered) |
| `WIN` | Won / review request |

---

## 10. GHL Folder Structure

```
📁 Forms
   ├── FRM-Lead-Intake
   └── FRM-Pre-Call

📁 Surveys
   └── SRV-Qualification

📁 Email Templates
   ├── ET-STL-01-Welcome
   ├── ET-SRV-Reminder-2
   ├── ET-QUAL-Hot-BookCall
   ├── ET-EDU-01-Process-Overview
   ├── ET-EDU-02-Service-1-Explainer
   ├── ET-EDU-03-Service-2-Explainer
   ├── ET-EDU-04-Testimonial
   ├── ET-EDU-05-CTA-Next-Step
   ├── ET-BOOK-Confirmation
   ├── ET-PROP-Agreement-Sent
   ├── ET-PROP-Reminder-48hr
   ├── ET-PAY-Confirmation
   ├── ET-PORTAL-Welcome
   └── ET-WIN-ReviewRequest (optional email variant)

📁 SMS Templates
   ├── SMS-STL-Welcome
   ├── SMS-SRV-Reminder-1
   ├── SMS-SRV-Final
   ├── SMS-QUAL-Hot-BookCall
   ├── SMS-EDU-01-Checkin
   ├── SMS-EDU-02-CTA
   ├── SMS-PROP-Sent
   ├── SMS-PAY-Confirmation
   └── SMS-WIN-ReviewRequest

📁 Workflows
   ├── WF-01-Speed-to-Lead
   ├── WF-02-Survey-Reminders
   ├── WF-03-Scoring-Routing
   ├── WF-04-Education-Sequence
   ├── WF-05-Booking-Flow
   ├── WF-06-Proposal-Payment
   ├── WF-08-Portal-Welcome
   ├── WF-09-Stage-Notifications
   ├── WF-10-Stale-Reminders
   ├── WF-11-Builder-Tasks
   └── WF-12-Review-Request
   ⚠️  WF-07 — DOES NOT EXIST. Was removed. Do not create.

📁 Proposals / Documents
   └── PROP-Engagement-Agreement (one template — handles Phase 1 + Phase 2)

📁 Memberships / Portal
   ├── Portal-Welcome
   ├── Portal-Phase-1 (shows when cf_service_phase = phase_1)
   ├── Portal-Phase-2 (shows when cf_service_phase = phase_2)
   ├── Portal-Documents
   └── Portal-FAQ

📁 Calendars
   └── CAL-Intro-Call (30-min slots)

📁 Pipelines
   └── PreBuild Pipeline
```

---

## 11. Builder Presets (fee_structure)

The `fee_structure` Custom Value drives which workflows, templates, and pipeline stages are active. Set during onboarding. Never hardcoded in workflow logic — always read from `custom_values.fee_structure`.

### Preset A — Two-Tier (Default)

**`fee_structure = two_tier`**
Target: Custom Builder, Design-Build

| What's Active | Detail |
|---|---|
| Pipeline stages | All 10 (8 active + 2 non-active) |
| Templates | All 18 |
| Workflows | All 11 (WF-07 removed, all others active) |
| Stripe/payment | ✅ Required — both Phase 1 and Phase 2 |
| Portal | ✅ Required |
| Education sequence | Full 7 touches |
| Pipeline passes | 2 (Phase 1 then Phase 2) |
| Onboarding complexity | High |

**Custom Values defaults for Preset A:**
- `process_stage_count` = `2`
- `service_1_name` = `Budget Estimate`
- `service_2_name` = `Detailed Quote`
- `service_1_fee` = `$550 inc GST`
- `service_2_fee` = `$6,600 inc GST`
- `phase_1_label` = `Budget Assessment`
- `phase_2_label` = `Detailed Pricing`
- `agreement_title` = `Pre-Construction Services Agreement`
- `refund_policy` = `Fees are fully refunded if we proceed to a building contract together.`

### Preset B — Single-Tier

**`fee_structure = single_tier`**
Target: Renovation Specialist, Extension Builder

| What's Active | Detail |
|---|---|
| Pipeline stages | All 10 (one pass only) |
| Templates | 16 (ET-EDU-03-Service-2-Explainer disabled) |
| Workflows | 11 (WF-06 Phase 2 conditional branch disabled) |
| Stripe/payment | ✅ Required — Phase 1 only |
| Portal | ✅ Required |
| Education sequence | Medium — 5 touches (Service-2-Explainer disabled) |
| Pipeline passes | 1 |
| Onboarding complexity | Medium |

**Custom Values defaults for Preset B:**
- `process_stage_count` = `1`
- `service_1_name` = `Detailed Quote` (or "Scoping Report", "Project Assessment")
- `service_2_name` = (not used)
- `service_1_fee` = `$1,200 inc GST` (typical for renovation/extension)

### Preset C — No-Fee

**`fee_structure = no_fee`**
Target: Small Builder (sole trader), builders testing the system

| What's Active | Detail |
|---|---|
| Pipeline stages | 7 (Proposal Sent + Engaged disabled) |
| Templates | 10 |
| Workflows | 8 (WF-06, WF-08 disabled) |
| Stripe/payment | ❌ Not required |
| Portal | ❌ Not required |
| Education sequence | Minimal — 3 touches max |
| Pipeline passes | 1 (skips to Delivered = "Quote Sent") |
| Onboarding complexity | Low |

**Disabled when `fee_structure = no_fee`:**
- WF-06 (Proposal + Payment)
- WF-08 (Portal Welcome)
- ET-PROP-Agreement-Sent
- ET-PROP-Reminder-48hr
- ET-PAY-Confirmation
- ET-PORTAL-Welcome
- SMS-PROP-Sent
- SMS-PAY-Confirmation

### Preset Comparison

| Feature | Preset A (Two-Tier) | Preset B (Single-Tier) | Preset C (No-Fee) |
|---|---|---|---|
| Paid services | 2 | 1 | 0 |
| Pipeline stages active | 10 | 10 | 7 |
| Templates active | 18 | 16 | 10 |
| Workflows active | 11 | 11 | 8 |
| Stripe required | ✅ | ✅ | ❌ |
| Portal required | ✅ | ✅ | ❌ |
| Education sequence | Full (7 touches) | Medium (5 touches) | Minimal (3 touches) |
| Onboarding complexity | High | Medium | Low |
| Best for | Custom, Design-Build | Renovation, Extension | Small Builder, Sole Trader |

---

## 12. Builder Archetypes

Validated against AU/NZ market research. Determines which preset to recommend during sales.

| # | Archetype | System Fit | Preset | v1 Priority |
|---|---|---|---|---|
| 1 | Custom / Architectural Builder | ★★★★★ Excellent | two_tier | v1 Primary ICP |
| 2 | Renovation / Extension Specialist | ★★★★☆ Strong | single_tier or two_tier | v1 Primary ICP |
| 3 | Volume / Production Builder | ★★☆☆☆ Poor | no_fee (with deposit) | v2 — defer |
| 4 | Design-Build Firm | ★★★★★ Excellent | two_tier | v1 Primary ICP |
| 5 | Small Builder / Sole Trader (free quotes) | ★★★☆☆ Moderate | no_fee | v1 Secondary |
| 6 | Specialist / Trade Contractor | ★★☆☆☆ Poor | no_fee or single_tier | v2 — defer |

**v1 ICP:** Focus sales on Archetypes 1, 2, 4. Archetype 5 works but most features are unused. Archetypes 3 and 6 should wait for v2.

---

## 13. QA Checklist

Run this before every go-live. All 18 tests must pass.

| # | Test | Expected Result |
|---|---|---|
| 1 | Submit lead capture form (FRM-Lead-Intake) | Contact created in GHL; SMS received <60 sec; email received; builder notification fires |
| 2 | Complete survey — Hot answers | Score ≥80; tag `lead-hot`; pipeline = Qualified; calendar link sent; builder task created |
| 3 | Complete survey — Warm answers | Score 50–79; tag `lead-warm`; pipeline = Nurture; education sequence starts |
| 4 | Complete survey — Cold answers | Score <50; tag `lead-cold`; pipeline = Not Now; polite decline sent |
| 5 | Hard disqualifier: budget under $300K | Routes to Not Now regardless of other scores |
| 6 | Hard disqualifier: "No" to fee | Routes to Not Now regardless of other scores |
| 7 | Book intro call | Calendar event created; confirmation SMS + email sent; builder task created; `call-booked` tag added; education sequence exits |
| 8 | Move to Proposal Sent (Phase 1) | `cf_service_phase` = `phase_1`; PROP-Engagement-Agreement email sent with Phase 1 content and fee |
| 9 | Sign proposal | E-signature captured; Stripe payment link triggered |
| 10 | Complete Stripe payment | Payment confirmed; pipeline moves to Engaged; confirmation email/SMS sent; `payment-received` tag added |
| 11 | Portal access | Client can log in; Portal-Welcome page displays; Portal-Phase-1 shows Phase 1 content |
| 12 | Cycle back for Phase 2 | Move contact from Delivered to Proposal Sent; `cf_service_phase` = `phase_2`; proposal fires with Phase 2 content and `service_2_fee` |
| 13 | Stale reminder fires | After 7 days no update → builder SMS fires |
| 14 | Stale reminder does NOT fire for Won/Not Now/Lost | Confirm WF-10 condition excludes these stages |
| 15 | Education sequence exits on call booked | Book a call mid-sequence → remaining emails stop |
| 16 | Survey reminder sequence | No completion after 72hrs → first reminder SMS fires; sequence stops when survey completed |
| 17 | No-fee preset | `fee_structure = no_fee`; Proposal Sent + Engaged stages skipped; no Stripe, no portal |
| 18 | Review request fires once | 14 days after Won stage → SMS-WIN-ReviewRequest sends; `review-requested` tag prevents duplicate |

---

## 14. Onboarding Process

**Target:** Builder live in 5 business days. Operator time: ~15 hours total.

### What Builder Provides (Collect at Discovery Call)

1. Trading name + ABN
2. Logo (PNG/SVG, high-res)
3. Brand colours (hex codes)
4. 2–3 past project photos
5. Service area(s)
6. Fee amounts: Service 1 and Service 2 (or confirm no-fee)
7. Existing preliminary agreement template (if any)
8. Sample Budget Estimate PDF (if two_tier or single_tier)
9. Sample Detailed Quote PDF (if two_tier)
10. 2–3 client testimonials (text + client first name)
11. Google Calendar access (or Calendly if they already use it)
12. Stripe account (builder's own — CentriWeb does not handle payments)
13. Facebook Business page access (if using FB Lead Ads)
14. Google Business Profile link (for review requests)
15. Intro call duration preference (default: 30 min)
16. Specific qualifying criteria (if any deviations from default scoring)
17. `fee_structure` preference: `two_tier` / `single_tier` / `no_fee`
18. Google Business Profile review link (for review request automation)

### 5-Day Build Schedule

| Day | Tasks | Hours |
|---|---|---|
| Day 1 | Create sub-account from snapshot. Apply branding. Configure all Custom Values. Connect Stripe. Connect Calendar. | ~3 hrs |
| Day 2 | Customise survey scoring (if builder has specific criteria). Customise PROP-Engagement-Agreement with builder's wording, ABN, fee amounts. Upload sample service PDFs. | ~3 hrs |
| Day 3 | Customise all email/SMS templates with builder's name, testimonials, project photos. Configure education sequence attachments. Set up portal branding + content. | ~4 hrs |
| Day 4 | Connect Facebook Lead Ad (if applicable). Embed FRM-Lead-Intake on builder's website. Run full end-to-end QA test. | ~3 hrs |
| Day 5 | Fix any issues from Day 4. Builder review call (30 min) — walk through full system. Get approval on all messaging. Final adjustments. | ~2 hrs |

### What's Pre-Built in Snapshot (Operator Doesn't Rebuild Per Client)

| Asset | Pre-Built? | Builder Provides |
|---|---|---|
| Pipeline stages | ✅ | — |
| Workflow logic + triggers | ✅ | — |
| Education sequence structure | ✅ | Testimonials, project photos, sample PDFs |
| Qualification survey questions | ✅ | Scoring adjustments only |
| Proposal template structure | ✅ | Fee amounts, ABN, specific terms |
| Portal pages layout + copy | ✅ | Branding, colours, builder-specific FAQ |
| Dashboard widgets | ✅ | — |
| Stripe connection | — | ✅ Builder's own Stripe |
| Calendar availability | — | ✅ Builder's schedule |
| Facebook Lead Ad | — | ✅ Builder's FB Business page |

---

## 15. Demo Build Spec

The Demo sub-account is used for sales calls only. Shows two presets side-by-side.

### Two Presets in Demo

| Preset | fee_structure | Seeded Contacts | Purpose |
|---|---|---|---|
| Preset A — Paid (Two-Tier) | `two_tier` | "Sarah Johnson" (Hot lead), "Michael Chen" (Warm — mid-education), "David & Lisa Park" (Engaged — portal active) | Show full hero journey from form to portal |
| Preset C — No-Fee | `no_fee` | "Tom Richards" (Qualified), "Emma Walsh" (Discovery Booked) | Show simplified flow for small builders |

### 5-Minute Demo Script

**Opening (30 sec):**
> "Let me show you exactly what this looks like from your client's perspective first — because if the experience is great for them, they'll pay your prelim fees without hesitation."

**Step 1 — Form submission (60 sec):**
- Show FRM-Lead-Intake on a mock builder website
- Submit form → show SMS arriving on phone within 60 seconds
- Show contact appearing in pipeline at New Enquiry

**Step 2 — Survey + Routing (60 sec):**
- Open survey link from SMS → complete as Hot lead
- Show pipeline move to Qualified; calendar link auto-sent
- **AHA line:** "This is the part where you normally spend 3–5 hours manually explaining your process. That's gone."

**Step 3 — Education sequence (30 sec):**
- Switch to Warm lead demo contact
- Show education sequence queued; preview ET-EDU-01-Process-Overview
- "While they're reading, you're doing nothing. The system is nurturing them for you."

**Step 4 — Proposal + Payment (60 sec):**
- Show PROP-Engagement-Agreement with builder's name and fee auto-populated
- Sign → Stripe payment link appears → pay test amount → pipeline moves to Engaged
- **AHA line:** "How many of your competitors have something like this? None. This is what separates a $300K builder from a $1M builder in a client's mind."

**Step 5 — Portal (60 sec):**
- Log in as client → show Welcome page + Phase 1 stage tracker
- "Your client always knows exactly where they are in the process. No chasing, no confusion."
- Show builder dashboard → pipeline KPIs → colour-coded leads

**Close (30 sec):**
> "This is running 24/7 for you. Every lead gets a response in under a minute. Every tire-kicker gets educated or filtered out automatically. The only leads that reach you are pre-qualified and ready to pay. We build this for you in 5 business days."

---

## 16. Change Control Rules

### How Changes Flow

```
Identify change → Document in Change Request log → Build in Factory only →
QA in Factory → Export new snapshot → Apply to new installs →
Update existing client installs manually (workflow exports/imports)
```

### Rules

1. **Never make changes directly in client subaccounts.** Factory is the only place changes are made.
2. **Every change to pipeline stages, field schema, or workflow triggers requires a Decision Log entry:** what changed, why, who decided, date.
3. **No bespoke forks per builder.** If a builder needs something different, use Custom Values + `fee_structure` toggle first. Only create a new variant if it can't be handled by the alias layer.
4. **Snapshot versioning:** v1.0 → v1.1 → v1.2 (minor) → v2.0 (major). Increment the version number on every snapshot export.
5. **Existing client installs:** Until GHL supports snapshot versioning natively, existing clients get manual updates via workflow exports/imports. Document which clients are on which version.

### Build Milestones

| Milestone | Outcome | Acceptance Criteria |
|---|---|---|
| M1 — Factory Baseline | Factory account created with naming conventions locked | Pipeline created. Custom Values dictionary created. All naming conventions confirmed. |
| M2 — Core Workflows Live | WF-01/02/03/04/05/06/08/09/10/11/12 implemented + templates connected | Each workflow passes individual QA test. |
| M3 — Demo Ready | Demo sub-account with 2 presets + seeded contacts | Full hero journey demo passes for both presets. Deliverable in under 5 minutes. |
| M4 — Snapshot v1.1 Export | Fresh snapshot exported from Factory, test-installed in blank sub-account | Fresh install + Custom Values config = functional in <1 day. |
| M5 — Pilot Install | 1–3 builder clients installed from snapshot | Issues logged. v1.2 improvements queued. |

---

## 17. Strategic Context

### Why This System Exists

Residential builders in Australia lose significant money quoting for free. The average custom builder spends 10–40 hours per quote with a 10–20% win rate. The root cause: homeowners have unrealistic budget expectations, and builders have no system to educate or qualify them before investing time.

The HIA preliminary agreements exist but builders can't sell them. The framing is wrong — it sounds like the builder is charging for their own protection. PreBuild Autopilot reframes it: the preliminary fee buys a professional deliverable (Budget Estimate or Detailed Quote) that helps the homeowner understand their project before any construction commitment.

### Strategic Wedge: Sales Pain, Not Operational Pain

Research confirmed that free quoting and tire-kicker frustration generates far higher emotional intensity among builders than operational/compliance pain. The sales funnel angle — eliminating unqualified leads and getting paid for preliminary work — resonates immediately. Operational efficiency (time tracking, site management) is a weaker opening argument.

### Key Principles

- **Education over filtering:** The system sets homeowner expectations through a 7-touch education sequence rather than just gatekeeping them
- **Remove the "extortion vibe":** Preliminary fees must be framed as delivering client value, not protecting the builder
- **Generic over PAP-specific:** The system serves all builder archetypes without requiring the Price A Plan partnership
- **Partner-dependency is a risk:** Architecture decisions must never hard-depend on PAP or House & Land

---

## 18. What Changed in the Generic Refactor (v1.1)

This section exists so you understand WHY things are named the way they are and don't accidentally revert to old patterns.

| What Changed | Old (v1.0) | New (v1.1) | Why |
|---|---|---|---|
| Service terminology | QBE, FQE | Service 1, Service 2 (configurable) | Remove PAP dependency |
| Pipeline stage names | S2 Paid (QBE Active), etc. | Engaged, Delivered | Generic; snapshot-portable |
| Proposal templates | PROP-S2-QBE-Agreement + PROP-S3-FQE-Agreement (two templates) | PROP-Engagement-Agreement (one template) | Simpler; WF-06 conditional handles both phases |
| WF-06 + WF-07 | Two separate proposal workflows | WF-06 only, with cf_service_phase conditional | Eliminates duplicate maintenance |
| Custom Values | qbe_fee, fqe_fee hardcoded | service_1_fee, service_2_fee + full alias layer | All client-facing language configurable |
| Portal pages | Portal-Stage-2-Budget-Assessment, Portal-Stage-3-Detailed-Estimate | Portal-Phase-1, Portal-Phase-2 | Generic names |
| Email templates | ET-EDU-02-QBE-Explainer, ET-EDU-03-FQE-Explainer | ET-EDU-02-Service-1-Explainer, ET-EDU-03-Service-2-Explainer | Remove PAP terms |
| Internal notifications | "paid their QBE fee", "FQE is ready" | Uses `{{custom_values.current_service_fee_label}}`, `{{custom_values.service_2_name}}` | All via Custom Values |
| cf_prelim_fee_s2 | `cf_prelim_fee_s2` | `cf_service_1_fee` | Remove "prelim" and "S2" references |
| cf_prelim_fee_s3 | `cf_prelim_fee_s3` | `cf_service_2_fee` | Remove "S3" reference |
| New field added | (missing) | `cf_service_phase` | Critical: drives WF-06 conditional logic for Phase 1/2 |
| New field added | (missing) | `cf_lost_reason` | Pipeline analytics |
| Stage count | 13 stages | 10 stages (8 active + 2 non-active) | Cleaner without losing flexibility |

---

## 19. Open Questions & Known Issues

### Open Architecture Questions (Confirm Before Building)

| Question | Status | Impact |
|---|---|---|
| Region: AU only vs AU+NZ? | Unconfirmed | Affects terminology defaults and compliance references |
| PAP partnership confirmed? | Unconfirmed | Treat as optional throughout — no hard dependencies |
| House & Land partnership confirmed? | Unconfirmed | Treat as optional throughout |
| Custom Object "Project" — in-scope for MVP? | Unconfirmed | Graceful degradation design means it can be added later without reworking workflows |
| Household/partner handling (couples) | Unconfirmed | Design decision: both partners as separate Contacts linked by household ID, coordinated via a Partner Notification reusable workflow |

### n8n Outreach System Known Issues (Separate to GHL)

The n8n cold outreach system (used for lead generation before leads enter GHL) has documented bugs:

| Issue | Detail |
|---|---|
| Column name capitalisation mismatch | `Email 1 Body` vs `Email 1 body` — causes silent blank email sends |
| Trailing spaces on column names | e.g., `Email 1 sent ` — must be replicated exactly in scraper output |
| Two different Google Spreadsheet IDs | Copywriter workflow vs sending workflow use different IDs — possible missing transfer workflow |
| Missing default column initialisation | Scraper missing defaults for: `Analysed`, `Replied`, `Opted Out`, `Bounced`, `W1-2` |
| W1-2 type mismatch | Must be written as strings `"1"` and `"2"`, not integers, for Google Sheets filter compatibility |

These issues are in the n8n system, NOT in GHL. Resolve before scaling outreach.

---

*End of document — PreBuild Autopilot Project Context v1.1 — March 2026*
*Maintained by Jerald / CentriWeb. Update this file whenever architecture decisions change.*
