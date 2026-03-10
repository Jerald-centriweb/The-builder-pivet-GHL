# PreBuild Autopilot — Sellability Strategy

> How to make this sub-account so good that building companies buy it within 5 minutes of seeing a demo.

---

## The Core Insight: Builders Don't Buy Software. They Buy Fewer Wasted Hours.

Every improvement below is evaluated against one question: **"Does this make the builder say YES faster on the sales call?"**

---

## 1. INSTANT-WIN IMPROVEMENTS (Do Before Next Sales Demo)

### 1.1 Add a "ROI Calculator" to the Demo Script

**What:** Before showing the system, show the builder their own numbers.

Ask on the sales call:
- "How many quotes do you do per month?" → e.g., 8
- "How many hours per quote?" → e.g., 12
- "What's your win rate?" → e.g., 15%
- "What's your hourly rate if you charged?" → e.g., $120

Then show them:
```
You spend: 8 quotes × 12 hrs × $120 = $11,520/month quoting for free
You win: 1.2 projects (15% of 8)
Cost per won project: $9,600 in free labour
With PreBuild Autopilot:
- 60% of tyre-kickers filtered before you speak to anyone
- Remaining leads are pre-educated and deposit-ready
- You recover $550-$6,600 per engaged lead in preconstruction fees
```

**Implementation:** Build this as a simple calculator in the demo sub-account. Can be a GHL custom page with embedded form that calculates instantly. Takes 2 hours to build.

**Why it sells:** Builders think in hours, not conversion rates. Showing them "$11,520/month wasted" is an emotional gut punch. Then showing them the system that fixes it is the relief.

### 1.2 Add Real-Time Pipeline Dashboard to Demo

**What:** The demo needs a visual dashboard the builder can see immediately:
- Colour-coded pipeline (red/amber/green)
- Lead count per stage
- Revenue collected (Phase 1 + Phase 2 fees)
- Survey completion rate
- Average time from enquiry to paid engagement

**Implementation:** Use GHL's native dashboard widgets. Pre-seed the demo account with 15-20 contacts at various stages so the dashboard looks alive and active, not empty.

**Why it sells:** Builders are visual. An empty pipeline looks like vaporware. A populated one with real numbers looks like a system that's already working.

### 1.3 Mobile Preview During Demo

**What:** Show the builder what their CLIENT sees on their phone. Open the SMS-STL-Welcome on a phone screen. Show the survey loading on mobile. Show the calendar booking experience.

**Implementation:** Have a test phone (or phone simulator) ready during demos. Send a real test lead through the system live.

**Why it sells:** Builders have never seen automation from the client's perspective. When they see how fast and professional it looks, they immediately think "my competitors don't have this."

---

## 2. PRODUCT IMPROVEMENTS THAT INCREASE CLOSE RATE

### 2.1 Builder Dashboard Page (Add to Snapshot)

**What:** A dedicated "Builder Dashboard" page inside GHL that shows:
- This month's pipeline summary (new leads / qualified / booked / paid)
- Revenue collected
- Next actions required (stale leads, upcoming calls, proposals awaiting signature)
- Recent activity feed

**Implementation:** GHL Custom Page with embedded dashboard widgets. 4-6 hours to build.

**Why it sells:** This is the "command centre" slide in the demo. Builders see ONE screen that tells them everything. They immediately imagine opening this every morning with their coffee.

### 2.2 Automated "Weekly Report" Email to Builder

**What:** Every Monday morning, the builder gets an email:
```
Subject: Your PreBuild Autopilot Weekly Report

This week:
- 5 new enquiries received
- 3 surveys completed (60% completion rate)
- 2 leads qualified as Hot
- 1 discovery call booked
- $550 collected in preconstruction fees

Action items:
- Michael Chen has been in Nurture for 8 days — consider manual follow-up
- Sarah Johnson's proposal has been unsigned for 3 days — send a reminder
```

**Implementation:** New workflow WF-14-Weekly-Report. Fires every Monday at 7am. Aggregates pipeline data using GHL's internal reporting. 3-4 hours to build.

**Why it sells:** This is a "set and forget" proof point. The builder doesn't need to log into the system — the system comes to them. During the demo, say: "Every Monday you'll get this in your inbox. You don't even need to log in."

### 2.3 "Speed-to-Lead Guarantee" Positioning

**What:** Rebrand the speed-to-lead feature as a competitive advantage the builder can market:

"Every enquiry gets a personal response within 60 seconds — 24/7, even on weekends."

**Implementation:** Already built (WF-01). Just needs positioning. Create a badge/graphic the builder can put on their website: "60-Second Response Guarantee."

**Why it sells:** Builders know they lose leads by being slow. Giving them a marketable promise they can put on their website is something they can immediately see value in.

### 2.4 Branded Client Portal with Stage Tracker

**What:** Upgrade the portal beyond basic pages. Add:
- Visual stage tracker (Step 1 → Step 2 → Step 3, with current step highlighted)
- Document upload area (for plans, site photos)
- FAQ section customised per builder
- "What to expect next" section that updates per stage

**Implementation:** GHL Membership pages with conditional visibility based on `cf_service_phase`. 6-8 hours.

**Why it sells:** Show this in the demo. Say: "Your client has their own portal. They can see exactly where their project is. How many builders do you know that offer this?" Zero. That's the answer. Zero.

---

## 3. FEATURES THAT REDUCE CHURN (Keep Builders Paying $297/month)

### 3.1 Monthly ROI Report

**What:** Automated monthly report showing:
- Total leads received
- Qualification breakdown (Hot/Warm/Cold)
- Conversion rate (enquiry → paid engagement)
- Revenue collected in preconstruction fees
- Hours saved (estimated: filtered leads × avg hours per unqualified conversation)
- ROI: "(Revenue collected + Hours saved value) vs $297 subscription"

**Implementation:** Monthly workflow + email template. Can use GHL reporting data or external Looker Studio dashboard.

**Why this prevents churn:** The #1 reason builders cancel is "I don't know if it's working." A monthly ROI report that shows "$3,300 collected in fees this month vs $297 subscription = 11x ROI" makes cancellation unthinkable.

### 3.2 Continuous Education Content Library

**What:** Provide builders with pre-written content they can use in their marketing:
- Blog posts about preconstruction process
- Social media posts about their qualification process
- Email templates for manual follow-up with warm leads
- Scripts for discovery calls

**Implementation:** Google Drive shared folder or a dedicated portal page in the builder's account. Content produced once, delivered to all builders.

**Why this prevents churn:** Builders feel supported, not just sold to. It also generates more inbound leads for the system to process, creating a positive feedback loop.

---

## 4. PRICING & PACKAGING STRATEGY

### Current: $2,500 setup + $297/month

### Recommended Upgrade Path:

| Tier | Price | What's Included | Target |
|------|-------|-----------------|--------|
| **Starter** | $1,500 setup + $197/month | No-fee preset only. Survey + qualification + calendar booking + basic education. No proposals, no portal, no Stripe. | Small builders testing the concept |
| **Professional** | $2,500 setup + $297/month | Full two_tier or single_tier. Proposals + Stripe + Portal + full education sequence. | Primary ICP (Custom/Design-Build) |
| **Premium** | $4,000 setup + $497/month | Professional + AI voice agent + budget calculator widget + analytics dashboard + video education content + priority support | Builders doing 15+ homes/year who want everything automated |

**Why tiered pricing works:**
- Starter reduces friction for first-time buyers. They upgrade when they see results.
- Premium captures maximum value from serious builders. The AI voice agent alone could save them 10+ hours/month.
- The jump from $197 to $297 is where most builders convert. The jump from $297 to $497 happens after 2-3 months of seeing ROI.

---

## 5. SALES OBJECTION HANDLERS (Build Into Demo)

### "I already have a CRM"
> "This isn't a CRM replacement — it's a preconstruction sales system that sits on top of your CRM. It does one thing your CRM can't: it qualifies, educates, and gets homeowners to pay a preconstruction fee before you ever speak to them."

### "My leads are all referrals, I don't need this"
> "Referrals are your best leads — and they'll score highest in our system. But even referrals need to understand your process and agree to a paid engagement. How many referrals have you quoted for free and lost? This system makes sure even referrals go through the proper process."

### "I don't want to charge a fee"
> "You don't have to. Our no-fee option still qualifies and educates leads automatically. But here's what builders find: once homeowners go through the education sequence and understand the value, 70%+ are willing to pay for a professional estimate. The system sells the fee for you."

### "$297/month is expensive"
> "You spend $11,000/month quoting for free. If this system saves you even ONE wasted quote per month, it's paid for itself 4x over. And every preconstruction fee you collect is pure profit on top of that."

### "Can I see it working for a real builder?"
> Have 1-2 pilot builder case studies ready. Even if they're only 30 days in, show: "Builder X installed this 30 days ago. They received 12 enquiries. 4 qualified as Hot. 3 booked calls. 2 signed proposals. $1,100 collected in Phase 1 fees. Their subscription is $297. That's 3.7x ROI in month one."

---

## 6. GO-TO-MARKET QUICK WINS

### 6.1 Facebook Group Strategy
Join Australian builder Facebook groups (HIA members, MBA members, builder business owner groups). Don't sell. Share educational content about the "free quoting problem." Position Jerald/CentriWeb as the expert. Drop the demo link when asked.

### 6.2 HIA / MBA Partnership
Approach HIA (Housing Industry Association) and MBA (Master Builders Association) about partnering. Their members are the exact ICP. Offer to present at their events or contribute to their member newsletter.

### 6.3 Referral Program for Existing Builders
First 3 pilot builders get a referral bonus: $500 credit per referred builder who signs up. Builders know other builders. One happy customer can bring 3-5 referrals.

### 6.4 "Free Audit" Lead Magnet
Offer builders a free "Preconstruction Sales Audit" — review their current quoting process, estimate time/money wasted, and show them what automation could look like. Use this as the top-of-funnel for PreBuild Autopilot sales. (This is literally what we just did in the audit report — productise it.)

---

## 7. WHAT MAKES THIS UNSELLABLE (Fix These First)

| Blocker | Why It Kills Sales | Fix |
|---------|-------------------|-----|
| WF-03 scoring not working | Builder tests the system in demo → lead doesn't route correctly → "this is broken" | Deploy scoring engine (wf03_scoring_engine.py) |
| Empty demo pipeline | Dashboard looks dead → "is anyone actually using this?" | Seed 15-20 demo contacts across all stages |
| No weekly report | Builder pays for 2 months, never logs in, cancels because "it wasn't doing anything" | Build WF-14 weekly report |
| No mobile preview in demo | Builder can't visualise the client experience | Prepare phone demo setup |
| Generic GHL proposal PDF | Looks like every other GHL proposal → "this doesn't look professional" | Add builder branding to proposal template, or upgrade to DocuSeal for v2 |

---

## Summary: Top 5 Actions to Increase Sales

1. **Fix WF-03 scoring** — Deploy `wf03_scoring_engine.py` via n8n webhook. Without this, the product doesn't work. (Dev: 4 hours)

2. **Add ROI calculator to demo** — Build a simple "how much do you waste quoting?" page. Show it BEFORE the system demo. (OM: 2 hours)

3. **Seed demo account properly** — 15-20 contacts across all stages with realistic data. Dashboard must look alive. (OM: 2 hours)

4. **Build weekly report workflow** — WF-14 sends Monday morning summary. Proves value passively. Prevents churn. (OM: 4 hours)

5. **Add builder dashboard page** — One screen showing everything. This is the "I need this" moment in the demo. (OM: 4 hours)

**Total time to sales-ready:** ~16 hours of OM/dev work.
