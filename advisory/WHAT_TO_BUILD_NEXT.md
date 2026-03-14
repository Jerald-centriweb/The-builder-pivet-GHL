# What to Build Next — PreBuild Autopilot Feature Roadmap

> Ranked by: value to builder clients × ease to build in GHL × impact on sellability.
> Everything in Tier 1 can be built natively in GHL with no code. Tiers 2–3 require external tools.

---

## Tier 1 — High Value, Build in GHL Now

### 1.1 After-Hours AI Response (Missed Call Text-Back)
**What:** GHL's native "Missed Call Text-Back" feature + an after-hours SMS that acknowledges the lead when the builder can't respond.
**Why:** 40% of builder enquiries come in evenings/weekends. A lead who gets an immediate response — even an automated one — is 3× more likely to book. A builder who goes silent until Monday loses to the first competitor who responds.
**Build:** Enable Missed Call Text-Back in GHL settings. Add a time-based condition to WF-01 that sends a different SMS when it's after 6pm or weekend: *"Hi [name], thanks for reaching out! We're not in the office right now but we'll be in touch first thing tomorrow. In the meantime, complete our quick project questionnaire and we'll have your results ready when we call: [survey_link]"*
**Effort:** 1 hour

### 1.2 Builder Weekly Performance Report
**What:** Automated email to the builder every Monday morning with their pipeline KPIs from the past 7 days.
**Content:**
- New enquiries received
- Surveys completed vs sent
- Hot / warm / cold breakdown
- Discovery calls booked
- Proposals sent
- Payments received
- Leads that went cold (moved to Not Now this week)

**Why:** Builders who see their pipeline every week stay subscribed. Builders who don't interact with the system cancel within 90 days. A weekly report makes the system feel alive even in quiet weeks.
**Build:** GHL workflow + GHL reporting + email template. Can be built natively.
**Effort:** 3 hours

### 1.3 Pre-Call Brief (Builder Prep)
**What:** 30 minutes before every discovery call, WF-05 sends the builder a formatted brief on who they're about to call.
**Content:**
- Contact name, phone
- Qualification score + temperature
- Their survey answers (project type, budget, timeline, land status, finance status)
- How they heard about the builder
- Any notes from reminders/replies

**Why:** Builders currently walk into intro calls blind. This makes them look prepared and professional. It also reduces no-shows because the builder actually values the call enough to prepare for it.
**Build:** GHL internal notification template using custom field merge fields.
**Effort:** 2 hours

### 1.4 No-Show Recovery Sequence
**What:** If a discovery call is marked as no-show, automatically trigger a 3-step recovery:
- Immediate SMS: "Hi [name], we missed you at our call today. No worries — here's a link to rebook at a time that works: [calendar_link]"
- 24hr email: Empathetic, asks if everything is OK, reiterates value of the call
- 72hr final SMS: Last attempt before moving to Nurture

**Why:** 20–30% of booked calls are no-shows. Most of those leads are still interested — they just got busy. A no-show recovery sequence converts 30–40% of them.
**Build:** WF-05 extension with no-show branch.
**Effort:** 2 hours

### 1.5 Proposal Expiry Nudge
**What:** If a proposal is sent but not signed after 5 days, send a direct builder notification: "Time-sensitive: [name]'s proposal has been sitting unsigned for 5 days. Consider calling them directly."
**Why:** Proposals that aren't followed up within 5 days drop from ~60% acceptance to ~20%. Most builders forget to follow up. This reminder catches it.
**Build:** WF-06 time delay + internal notification.
**Effort:** 1 hour

### 1.6 Lost Lead Exit Survey
**What:** When a lead is moved to Lost, automatically send a 2-question SMS: "Hi [name], sorry it didn't work out this time. Mind if I ask — what was the main reason? [link to 2-question form]"
**Questions:** (1) Why did you choose a different builder? (2) Would you consider us in future?
**Why:** Builder gets real market intelligence. Builds the lost lead database for future re-engagement. Some respond and re-engage immediately.
**Build:** WF trigger on Lost stage + FRM-Exit-Survey form + follow-up logic.
**Effort:** 3 hours

### 1.7 Partner Coordination Workflow (Couple Handler)
**What:** When `cf_partner_name` and `cf_partner_email` are populated, create a second contact record for the partner linked via `cf_household_id`. Send the partner a separate (lighter) education sequence: "Hi [partner_name], [primary_name] told us you're exploring a building project together. Here's a quick overview of how our process works — [link]"
**Why:** The partner who hasn't seen the education content is the #1 reason deals die at discovery call. The "I need to discuss with my wife" objection is almost always "my wife doesn't understand why we'd pay a fee." This pre-empts it.
**Build:** WF-11 expanded with contact creation action + separate email sequence.
**Effort:** 4 hours

---

## Tier 2 — High Value, Needs Minor External Tool

### 2.1 Instant Lead Scoring Without External Server (n8n Code Node)
**What:** Deploy `audit/wf03_scoring_engine.py` as an n8n Code Node. WF-03 POSTs survey data to n8n → n8n runs the scoring → POSTs back to GHL.
**Why:** This is THE critical gap. Without working scoring, routing doesn't work, hot leads don't get the calendar link, warm leads don't start education. Everything downstream depends on this.
**Build:** n8n workflow with HTTP trigger → Code node (paste the score_lead function) → HTTP request back to GHL. ~15 lines of config.
**Effort:** 2 hours if n8n is already running

### 2.2 Budget Reality Check Widget
**What:** A simple single-page web app (embeddable on the builder's website) that asks: "What are you thinking of building?" and "What's your rough budget?" and returns: "Based on current Newcastle construction costs, a [project type] of [size] typically costs between $X and $Y. Your stated budget of $Z is [on track / 15% below market / 40% below market]."
**Why:** Homeowners with unrealistic budgets are the #1 source of wasted quoting time. If someone can self-qualify against real cost data before they even enquire, the inbound quality improves dramatically. Also a powerful trust-builder — the builder looks knowledgeable and transparent.
**Build:** Static HTML/JS page with a simple cost table lookup. No backend needed. Embed on builder's website before the enquiry form.
**Effort:** 1 day to build v1

### 2.3 ROI Calculator for Sales Calls
**What:** A one-page interactive calculator the operator (Jerald) shows on sales calls. Builder inputs: enquiries/month, hours/quote, win rate, hourly rate. Calculator outputs: current cost of quoting, projected savings with PreBuild Autopilot, payback period on setup fee.
**Why:** Removes price objection entirely. When a builder sees "you're spending $4,200/month on unqualified quoting and this system costs $297/month", the $297 is a no-brainer.
**Build:** Single HTML page with JavaScript. No backend.
**Effort:** Half a day

### 2.4 Review Automation (Google + Facebook)
**What:** After the 14-day review request SMS fires, if the client hasn't left a review in 7 days, send a second SMS with a direct link specifically to Google review submission (not just the Google Business profile). After review is left, trigger a gratitude SMS.
**Why:** Most builders have 3–8 Google reviews. 20+ reviews changes how homeowners perceive them. Each review also improves Google Maps ranking. One review request SMS is easy to ignore — a second with a friction-free direct link converts far better.
**Build:** WF-12 extension + Zapier/n8n to detect review submission (or time-based fallback).
**Effort:** 2 hours for the SMS sequence; review detection requires API

### 2.5 Facebook Lead Ad Direct Integration
**What:** Connect GHL to the builder's Facebook Business Manager so Facebook Lead Ads pipe directly into the GHL pipeline as New Enquiry contacts, triggering WF-01 immediately.
**Why:** Facebook Lead Ads are the fastest way for builders to generate volume enquiries. Without direct integration, leads go cold while waiting for someone to manually import them. Speed-to-lead drops from <60 seconds to hours.
**Build:** Native GHL Facebook integration (already supported). Requires builder's FB Business page access.
**Effort:** 30 minutes per builder

---

## Tier 3 — Game-Changers for V2

### 3.1 AI Voice Agent for After-Hours Inbound Calls (Vapi or Bland.ai)
**What:** When a lead calls the builder's number after hours and nobody answers, an AI voice agent picks up: "Hi, thanks for calling Smith Building Co! I'm the virtual assistant. I can take your project details right now so we can have everything ready for when our team calls you back tomorrow. Can I get your name?"
The agent collects: name, project type, suburb, budget range, timeline. Creates or updates a GHL contact. Tags it appropriately.
**Why:** 15–25% of builder leads come via phone, not web forms. After-hours callers who hit voicemail rarely leave a message. An AI that actually collects project info converts these completely lost leads.
**Integration:** Vapi.ai → GHL webhook → WF-01 trigger
**Effort:** 1–2 days to build and test

### 3.2 Buildxact Integration (Status Sync)
**What:** When a lead progresses to a real construction contract in Buildxact (the most common estimating tool for custom builders), sync their status back to GHL. Move to Won. Trigger review request timer.
**Why:** Currently the "Won" stage is moved manually by the builder. Builders forget to update GHL. Win rate reporting is always understated. Automatic sync means the system's reporting reflects reality.
**Integration:** Buildxact API → n8n → GHL
**Effort:** 3–5 days

### 3.3 Smart Re-Engagement (Long-Term Nurture)
**What:** Contacts in "Not Now" get a quarterly re-engagement sequence triggered by their original timeline. If someone said "12+ months" and it's now been 9 months, they get: "Hi [name], it's been a while since we connected. If your building plans are getting closer, we'd love to help. [book a call / re-do survey]"
**Why:** Builder funnels have a long tail. "Not Now" is not "Never". A builder with 200 Not Now contacts from the past year has $2M+ in potential fee revenue sitting dormant. This activates it.
**Build:** GHL workflow with date-based conditional triggers.
**Effort:** 3 hours

### 3.4 Client Progress Portal (Enhanced)
**What:** The existing portal gets enhanced with:
- Live project milestone tracker (visual progress bar)
- Document upload area for homeowner to submit plans/site photos
- Weekly progress update from builder (1-paragraph text update)
- Q&A section (homeowner asks, builder responds)
**Why:** Currently the portal is static. A portal that's genuinely useful (homeowner checks it weekly) creates daily engagement, reduces calls to the builder ("where are we at?"), and makes the prelim fee feel well worth it.
**Build:** GHL Memberships + custom pages + workflow to trigger updates
**Effort:** 2–3 days

### 3.5 Competitor Benchmarking Report (Lead Gen for Operator)
**What:** Jerald builds a free "Builder Sales Efficiency Report" that pulls data from a short survey: enquiries/month, quotes/month, win rate, average quote time. Benchmarks against industry average. Sends a personalised PDF showing where the builder is leaking money.
**Why:** This is a lead generation tool for CentriWeb. Builders who complete the audit see their own pain quantified. Conversion from "interested" to "ready to buy" is dramatically higher when they've done their own calculation.
**Build:** Typeform or GHL survey → n8n → personalised PDF generation → email delivery
**Effort:** 2–3 days

---

## GHL Native Features Not Yet Activated

These are already available in GHL but not yet set up:

| Feature | How to use it | Effort |
|---------|--------------|--------|
| Reputation Management | Auto-request reviews + monitor Google/Facebook | 1 hour |
| Live Chat Widget | Qualify website visitors before they complete the form | 2 hours |
| Email Marketing | Monthly builder newsletter template | 3 hours |
| Social Planner | Schedule builder's social posts from GHL | 1 hour |
| Proposals (DocuSign alternative) | Already planned — ensure Stripe link fires on sign | Verify only |
| Memberships (Portal) | Already planned — activate and brand it | 4 hours |
| Conversation AI (GHL native) | Basic chatbot on builder's website | 2 hours |
| Affiliate Manager | Referral program for builders to refer other builders | 3 hours |
| Invoicing | Send invoices from GHL instead of Stripe only | 2 hours |
| Communities | Private community for builder clients (peer network) | 1 day |
