# PreBuild Autopilot — Advisory Briefing
### For Claude: Read this entire folder before making any recommendations.

---

## What This Is

**PreBuild Autopilot** is a GoHighLevel (GHL) sub-account snapshot built by Jerald Immanuel / CentriWeb (Newcastle, NSW, Australia) that automates the preconstruction sales funnel for Australian residential builders.

**The problem it solves:** Australian custom builders (5–30 homes/year) spend 10–40 unpaid hours per quote with only a 10–20% win rate. Most lose money on the quoting process. Homeowners arrive with unrealistic budgets, shop 4–5 builders simultaneously, and ghost after getting their free quote.

**The solution:** A done-for-you system that:
1. Captures inbound enquiries automatically
2. Qualifies leads through a 15-question weighted survey (scores 0–100)
3. Educates warm leads over 7–10 days (why paid preconstruction fees are client-beneficial)
4. Routes hot leads directly to a booking calendar
5. Sends a paid engagement agreement + Stripe payment link
6. Gives paying clients a branded portal with project status
7. Filters out tyre-kickers before the builder ever speaks to them

**Business model:**
- ~$2,500 setup fee per builder client
- ~$297/month recurring per builder
- Installed from a Factory snapshot → customised via Custom Values → live in 5 days
- Operator: CentriWeb / Jerald (agency model — he builds and manages it for builders)

**Three product presets:**
- `two_tier` — Phase 1 (Budget Estimate ~$550) + Phase 2 (Detailed Quote ~$6,600)
- `single_tier` — One paid service only
- `no_fee` — Qualification + education only, no payment (for builders not ready to charge)

---

## The Industry Context

### Australian Residential Builders — Who They Are

The target market is **5–30 homes/year custom builders** across Australia. Key characteristics:

- **Revenue:** $2M–$20M/year
- **Team size:** 1–10 office staff, rest are subcontractors
- **Pain:** Free quoting culture is deeply entrenched but quietly resented
- **Win rate:** 10–20% on tender — spend $3K–$8K of time per lost job
- **Typical prelim agreement:** HIA-standard contract exists but most builders can't sell the concept
- **Fee acceptance:** Builders who DO charge prelim fees report 80%+ acceptance from qualified leads
- **Key associations:** HIA (Housing Industry Association), MBA (Master Builders Australia)
- **Estimating tools:** Buildxact, Databuild, Cheops — most still use Excel
- **Lead sources:** Website, Facebook ads, referrals, House & Land portals

### The Emotional Hook (Why They Buy)

Builders don't buy software. They buy relief from a specific pain:

> "I just spent 3 days quoting for a couple who said they had $800K but actually had $350K. They went with a volume builder. I'll never get that time back."

The pitch is not "here is a CRM." The pitch is:
**"Stop doing unpaid work for people who were never going to hire you."**

The ROI is immediate and concrete:
- 10 enquiries/month × 3 hours each = 30 hours of quoting time
- If the system filters 70% to tyre-kickers = 9 hours saved per month
- At a builder's effective rate of $150–$250/hr = $1,350–$2,250/month saved just in time
- Plus: the 3 who ARE qualified now pay $550–$6,600 before you quote them

### What Builders Care About (in order)
1. Less wasted time on bad leads
2. Getting paid before doing detailed work
3. Looking more professional than competitors
4. Knowing which leads are serious before calling them
5. Not having to chase people

### What They Don't Care About
- Database architecture
- Workflow logic
- CRM terminology
- API integrations
- "Automation"

---

## Current Live Account State (March 2026)

**Account:** MASTER FACTORY — PREBUILD ENGINE
**Location ID:** `cVCso4OlgGoOoXMpbxxA`
**Address:** Newcastle, NSW (Jerald's own agency address — not a client account)

### What's Actually Built

| Component | Built | Working | Notes |
|-----------|-------|---------|-------|
| Pipeline | ✅ | ⚠️ | 11 stages exist but 4 names don't match spec |
| Workflows | ✅ | ❌ | All 10 exist but ALL are Draft — nothing fires |
| Survey | ✅ | ⚠️ | Exists but field mappings unverified |
| Forms | ✅ | ⚠️ | FRM-Lead-Intake exists |
| Custom Fields | ⚠️ | ⚠️ | 15 exist, 7 missing, 2 with wrong names |
| Custom Values | ⚠️ | ❌ | 11 exist but all blank — not populated |
| SMS Templates | ⚠️ | ⚠️ | 5 of 9 exist |
| Email Templates | ❌ | ❌ | 0 of 14 found |
| Calendar | ✅ | ⚠️ | CAL-Intro-Call exists |
| Tags | ⚠️ | ⚠️ | 5 of 16 exist |
| Portal | ❓ | ❓ | Not confirmed |
| Stripe | ❓ | ❓ | Not confirmed |
| Scoring engine | ✅ | ❌ | Code exists in repo but not deployed anywhere |

### The Three Things Stopping It Working Right Now

**1. Every workflow is Draft.**
GHL workflows only fire when Published. Nothing in this system can trigger. This is a single toggle per workflow but must be done after fixing the issues below.

**2. Custom field names don't match what the scoring engine expects.**
- Live account has `cf_lead_score` → spec + scoring engine expects `cf_qualification_score`
- Live account has `cf_finance_status` → spec expects `cf_financing_status`
The scoring engine writes to `cf_qualification_score`. If that field doesn't exist, scores are lost silently.

**3. Pipeline stage names don't match what workflows expect.**
Workflow "Move to Stage" actions use exact text. Four stages have wrong names:
- Live: "Survey Completed" — should not be a stage at all (it's a tag in the spec)
- Live: "Qualified - Hot" — workflows expect "Qualified"
- Live: "Nurture - Warm" — workflows expect "Nurture"
- Live: "Intro Call Booked" — workflows expect "Discovery Booked"

Any workflow that moves a contact to a stage will fail silently with these mismatches.

### What's Missing Entirely
- WF-08-Portal-Welcome (not created)
- 14 email templates (none exist)
- 4 SMS templates (SMS-SRV-Final, SMS-QUAL-Hot-BookCall, SMS-EDU-01-Checkin, SMS-EDU-02-CTA, SMS-PAY-Confirmation, SMS-WIN-ReviewRequest)
- 11 tags (survey-pending, survey-completed, call-booked, payment-received, portal-active, review-requested, stage-won, stage-lost, fee-tier-*, payment-manual)
- 4 custom values (builder_abn, survey_link, portal_link, google_review_link)
- 7 custom fields (cf_lead_temperature, cf_design_status, cf_decision_maker, cf_communication_preference, cf_lost_reason, cf_site_address, cf_prior_quotes)
- External scoring endpoint (the WF-03 engine is coded but not deployed)

---

## The Fix List (Before Any Builder Can Go Live)

### Must fix first (breaks everything if not done)
1. Rename pipeline stages to match spec exactly
2. Rename `cf_lead_score` → `cf_qualification_score`
3. Rename `cf_finance_status` → `cf_financing_status`
4. Create the 7 missing custom fields
5. Create the 11 missing tags
6. Populate all custom values (at least the required 14)
7. Build all 14 email templates
8. Build the 4 missing SMS templates
9. Create WF-08-Portal-Welcome
10. Deploy the scoring engine to n8n or a cloud function
11. Wire WF-03 to call the external scorer via webhook
12. Publish all 10 workflows (only after 1–11 done)

### Fix before demo (makes it look broken)
13. Seed demo contacts (hot/warm/cold journey)
14. Populate demo custom values with "Smith Building Co" example data

---

## Key Files in This Repo

| File | Read for |
|------|---------|
| `PREBUILD_AUTOPILOT_CONTEXT.md` | Full spec — architecture, all workflows, all templates, naming rules |
| `audit/GHL_SUBACCOUNT_DUMP.md` | Live account snapshot — what's actually in GHL |
| `audit/DEEP_SPEC_ANALYSIS.md` | All bugs found, architecture risks |
| `audit/GHL_VERIFICATION_CHECKLIST.md` | Item-by-item verification guide |
| `audit/wf03_scoring_engine.py` | The scoring engine code (Python) |
| `audit/SELLABILITY_STRATEGY.md` | Existing sellability notes |
| `advisory/WHAT_TO_BUILD_NEXT.md` | New features and GHL additions |
| `advisory/SELLABILITY_PLAYBOOK.md` | How to position and sell this |
| `advisory/BUILDER_VALUE_MAP.md` | Builder pain points and value propositions |

---

## Who You're Helping

**Jerald Immanuel** — founder of CentriWeb, a small digital agency based in Newcastle, NSW. He's building PreBuild Autopilot as a productised service to sell to residential builders across Australia (and potentially NZ). He is the operator — he installs, configures, and supports the system for each builder client.

**His current situation:** The Factory account is 70–80% built but not yet live with any paying builder clients. The spec is excellent. The code/structure is mostly right. The gaps are mostly execution — missing templates, wrong field names, workflows in Draft.

**What he needs:**
- Get the Factory account to a working state he can demo
- Get his first 1–3 builder clients installed and paying
- Have a clear roadmap of what to add to make it more valuable
- A commercial narrative that resonates with builders instantly
