# PreBuild Autopilot — Priority Action Matrix

> Use this to decide what to tackle next. Items are ranked by a combination of **revenue impact**, **risk severity**, and **effort required**.

---

## Priority Tier 1: DO IMMEDIATELY (This Week)
*These items are either compliance risks, broken functionality, or high-impact quick wins.*

| # | Action | Why It's Tier 1 | Effort | Who | Revenue Impact |
|---|--------|-----------------|--------|-----|----------------|
| 1 | **SMS opt-out compliance** | Legal risk. ACMA penalties up to $2.22M/day. Telcos can suspend your sending number. | 30 min | OM | Protective — prevents account shutdown |
| 2 | **Fix Google Review link placeholder** | SMS-WIN-ReviewRequest sends literal `[Google Review Link]` text to paying clients. Broken last impression. | 15 min | OM | Low direct, high reputation |
| 3 | **Add manual payment override (`payment-manual` tag)** | Clients paying by bank transfer get stuck at Proposal Sent forever. Builder has to manually run every downstream step. | 1 hr | OM | HIGH — any builder not using Stripe exclusively hits this wall |
| 4 | **Resolve WF-03 scoring implementation** | If scoring doesn't work, every lead gets misrouted. The entire value proposition collapses. | 4-8 hrs | Dev | CRITICAL — system is non-functional without this |

**Changes already applied to context doc:** Items 1, 2, 3 are reflected in the updated PREBUILD_AUTOPILOT_CONTEXT.md.

---

## Priority Tier 2: DO THIS SPRINT (Next 2 Weeks)
*High-impact improvements that require moderate effort.*

| # | Action | Why It's Tier 2 | Effort | Who | Revenue Impact |
|---|--------|-----------------|--------|-----|----------------|
| 5 | **Fix ET-EDU-01 Handlebars conditional** | `{{#if}}` doesn't render in GHL. First education email looks broken for single_tier/no_fee builders. | 1 hr | OM | MEDIUM — affects first impression of nurture sequence |
| 6 | **Add lead source attribution (`cf_how_heard`)** | Can't measure marketing ROI. Builder can't justify ad spend. You can't prove system value. | 2 hrs | OM | HIGH — data that drives all future marketing decisions |
| 7 | **Enable missed-call text-back** | Every missed call is a lead potentially lost to a competitor who answers. | 15 min | OM | MEDIUM-HIGH — captures phone-first leads |
| 8 | **Add calendar cancel/reschedule handling** | Cancelled calls leave leads in limbo with no re-engagement path. | 2 hrs | OM | MEDIUM — prevents lead leakage at discovery stage |
| 9 | **Add partner fields to survey** | Partner "veto vote" kills 20-30% of deals at discovery. Pre-educating partners converts more. | 1.5 hrs | OM | HIGH — directly increases discovery→proposal conversion |

**Changes already applied to context doc:** Items 5, 6, 8, 9 are reflected in the updated PREBUILD_AUTOPILOT_CONTEXT.md.

---

## Priority Tier 3: PLAN FOR NEXT MONTH
*Important but can wait. Either requires external tools or longer dev time.*

| # | Action | Why It's Tier 3 | Effort | Who | Revenue Impact |
|---|--------|-----------------|--------|-----|----------------|
| 10 | **Build long-term nurture workflow (WF-13)** | "Not Now" = 40-60% of leads. Without quarterly re-engagement, they're permanently lost. | 4 hrs | OM | MEDIUM-HIGH (long-term) |
| 11 | **Add video to education sequence** | Text-only emails have 2-3x lower engagement than video. Builder's face builds trust. | 2 hrs embed + builder records | OM + Builder | HIGH — best education sequence upgrade available |
| 12 | **Deploy AI voice agent (Vapi)** | After-hours leads (30-50% of enquiries) get no real engagement. | 12-20 hrs | Dev | HIGH — could capture 2+ extra conversions/month |
| 13 | **Build analytics dashboard (Looker Studio)** | "Show me the ROI" question comes within 30 days. Without dashboard, builders churn. | 8-12 hrs | Dev | HIGH (retention) — proves value, prevents churn |
| 14 | **Portal login engagement check** | Paying clients who never log in may have buyer's remorse. | 1 hr | OM | LOW-MEDIUM |

---

## Priority Tier 4: V2.0 ROADMAP
*Nice-to-have, requires significant development, or depends on Tier 1-3 completion.*

| # | Action | Why It's Tier 4 | Effort | Who | Revenue Impact |
|---|--------|-----------------|--------|-----|----------------|
| 15 | **Budget calculator widget** | Pre-qualifies leads before survey. Reduces tyre-kicker volume. | 12-16 hrs | Dev | MEDIUM-HIGH |
| 16 | **Professional document generation (DocuSeal)** | GHL proposals work but look generic. Matters more for $6,600 Phase 2 fee. | 16-24 hrs | Dev | MEDIUM |
| 17 | **Pre-personalisation with Perplexity Sonar** | Auto-research suburb data before survey. Advanced but powerful. | 2-4 hrs | Dev (n8n) | LOW-MEDIUM |
| 18 | **Review automation platform (NiceJob)** | Multi-channel review requests get 3-4x more reviews than single SMS. | 2-4 hrs | Dev/OM | LOW-MEDIUM |
| 19 | **Partner notification workflow** | Full couple coordination flow. | 4-6 hrs | Dev | MEDIUM |
| 20 | **Custom Object "Project" implementation** | Multi-project support. Richer reporting. | 6-8 hrs | Dev | LOW (until builder has multi-project clients) |

---

## Decision Framework

When choosing what to work on next, ask:

1. **Is it broken?** Fix it first (Tier 1).
2. **Does it lose leads or money?** Fix it second (Tier 2).
3. **Does it improve conversion or prove ROI?** Plan it (Tier 3).
4. **Does it add new capability?** Roadmap it (Tier 4).

### The One Question That Matters Most Right Now

> **Has WF-03 scoring actually been implemented and tested?**

If the answer is "no" or "I'm not sure" — that's the only priority. Everything else is polishing a car with no engine. The scoring workflow determines whether every single lead gets routed correctly. Without it, Hot leads get lost in education sequences, Cold leads get invited to calls, and builders lose trust in the system within the first week.

Run the audit collector script locally to verify workflow status:
```bash
python3 audit/ghl_audit_collector.py --api-key "pit-335bf0ee-b8e4-4eaa-be07-997052ceb717"
```

---

## Summary of Changes Already Applied to PREBUILD_AUTOPILOT_CONTEXT.md

| Change | What Was Done |
|--------|---------------|
| SMS opt-out compliance | Added "Reply STOP to opt out" to all 9 SMS templates |
| Google Review link fix | Replaced `[Google Review Link]` placeholder with `{{custom_values.google_review_link}}` merge field |
| google_review_link Custom Value | Added to Required Custom Values registry |
| google_review_link in onboarding | Added to onboarding checklist (item #18) |
| google_review_link in merge syntax | Added to Merge Field Syntax table |
| Manual payment override | Added `payment-manual` tag to Tags Schema + added manual payment override spec to WF-06 |
| fee-tier-two tag | Added explicit tag for default two_tier preset (for reporting clarity) |
| ET-EDU-01 Handlebars fix | Replaced broken `{{#if}}` conditional with implementation note for workflow-level branching |
| Lead source attribution | Added `cf_how_heard` to Custom Fields schema + survey question #14 |
| Partner fields | Added `cf_partner_name` and `cf_partner_email` to Custom Fields schema + survey question #15 |
| Calendar cancel/reschedule | Added cancel and reschedule handling specs to WF-05 |
| No-show follow-up | Updated WF-05 no-show handling to include homeowner SMS (not just builder task) |
| SMS compliance rule | Added to Critical Rules "Always Do" table |
| Review link rule | Added to Critical Rules "Always Do" table |
