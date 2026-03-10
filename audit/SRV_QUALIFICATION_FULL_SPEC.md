# SRV-Qualification — Full Survey Specification

> **Purpose:** This is the single most important asset in the PreBuild Autopilot system. Every lead's journey — hot/warm/cold routing, education vs fast-track, proposal timing — flows from this survey. A well-designed survey does three things simultaneously:
> 1. **Qualifies** — separates serious builders from tyre-kickers using weighted scoring
> 2. **Educates** — the questions themselves prime the homeowner to understand the process
> 3. **Collects** — populates custom fields that personalise every downstream touchpoint

---

## Survey Design Principles

- **Under 4 minutes** — 15 questions max. Every question that doesn't score or inform a downstream action gets cut.
- **Progressive disclosure** — Easy questions first (project type, location), confronting questions last (budget, fees).
- **Psychologically sequenced** — By the time they reach "Are you open to a preconstruction fee?", they've already answered 9 questions and are mentally committed to completing. This is deliberate.
- **Mobile-first** — 70%+ of homeowners will complete this on their phone from the SMS link. Every question must work with thumb taps, not typing.
- **No jargon** — "Do you have finance sorted?" not "What is your financing status?"

---

## GHL Survey Configuration

**Survey Name:** `SRV-Qualification`
**Survey URL slug:** `/project-questionnaire` (or use Custom Value `{{custom_values.survey_link}}`)
**Thank You redirect:** Calendar booking page (for Hot leads) or custom thank-you page with "We'll be in touch within 24 hours"

---

## Question-by-Question Specification

### Page 1: About Your Project (Easy, Low-Friction Start)

---

#### Q1: What type of project are you planning?

| Setting | Value |
|---------|-------|
| **Type** | Single-select (radio buttons) |
| **Required** | Yes |
| **Maps to** | `cf_project_type` |
| **Options** | New Home Build / Knockdown & Rebuild / Extension / Renovation |

**Scoring:**
| Answer | Points | Rationale |
|--------|--------|-----------|
| New Home Build | 10 | Highest margin, best system fit |
| Knockdown & Rebuild | 10 | Same as new build in complexity and margin |
| Extension | 8 | Good fit, slightly smaller scope |
| Renovation | 6 | Lower margin, more variable scope |

**Why this question is first:** It's the easiest to answer and immediately gets the homeowner thinking about their project. Zero friction.

---

#### Q2: Where will this project be located?

| Setting | Value |
|---------|-------|
| **Type** | Text input (single line) |
| **Required** | Yes |
| **Maps to** | `cf_site_address` |
| **Placeholder text** | "Suburb or full address" |

**Scoring:** 0 points — informational only. Used in proposal merge fields, builder task context, and potential future suburb-based cost enrichment (Perplexity Sonar integration).

**Why it's here:** Captures location early while engagement is high. This field personalises the proposal ("your project at [address]") which dramatically increases perceived effort and trust.

---

#### Q3: Do you already have land or a property for this project?

| Setting | Value |
|---------|-------|
| **Type** | Single-select (radio buttons) |
| **Required** | Yes |
| **Maps to** | `cf_land_status` |
| **Options** | Yes, I own the land/property / Under contract (settlement pending) / Still looking for land |

**Scoring:**
| Answer | Points | Rationale |
|--------|--------|-----------|
| Yes, I own the land/property | 15 | Ready to proceed — no land dependency |
| Under contract (settlement pending) | 12 | Nearly ready — can start prelim work during settlement |
| Still looking for land | 5 | Months away from being ready. May circle back later. |

---

### Page 2: Your Plans & Timeline

---

#### Q4: How far along are your design plans?

| Setting | Value |
|---------|-------|
| **Type** | Single-select (radio buttons) |
| **Required** | Yes |
| **Maps to** | `cf_design_status` |
| **Options** | I have detailed plans or drawings ready / I have a rough concept or sketch / I haven't started on plans yet |

**Scoring:**
| Answer | Points | Rationale |
|--------|--------|-----------|
| I have detailed plans or drawings ready | 15 | Can price immediately — fastest path to revenue |
| I have a rough concept or sketch | 10 | Needs design consultation but is actively progressing |
| I haven't started on plans yet | 5 | Early stage — needs more education before they're ready to pay |

**Note:** Add `cf_design_status` to Custom Fields schema if not already present. Values: `Plans Ready` / `Concept Only` / `Nothing Yet`

---

#### Q5: When would you ideally like to start construction?

| Setting | Value |
|---------|-------|
| **Type** | Single-select (radio buttons) |
| **Required** | Yes |
| **Maps to** | `cf_timeline` |
| **Options** | As soon as possible / Within 3–6 months / 6–12 months from now / More than 12 months away |

**Scoring:**
| Answer | Points | Rationale |
|--------|--------|-----------|
| As soon as possible | 15 | Highest urgency = highest conversion probability |
| Within 3–6 months | 12 | Solid timeline — preconstruction work fits perfectly |
| 6–12 months from now | 8 | Planning phase — good for nurture, may convert later |
| More than 12 months away | 3 | Too far out for most builders to invest time now |

---

#### Q6: Have you spoken with any other builders about this project?

| Setting | Value |
|---------|-------|
| **Type** | Single-select (radio buttons) |
| **Required** | Yes |
| **Maps to** | `cf_prior_quotes` |
| **Options** | No, you're my first point of contact / Yes, 1–2 other builders / Yes, 3 or more builders |

**Scoring:**
| Answer | Points | Rationale |
|--------|--------|-----------|
| No, you're my first point of contact | 10 | First mover advantage — no competitor comparison yet |
| Yes, 1–2 other builders | 10 | Normal shopping behaviour — still winnable |
| Yes, 3 or more builders | 5 | Quote-shopping behaviour — higher risk of tyre-kicking |

**Why this matters:** Homeowners who've already spoken to 3+ builders are often in "free quote collection" mode. They're the least likely to pay a preconstruction fee. This question flags them early.

---

### Page 3: Budget & Finances (The Confronting Section)

> **Page intro text (shown at top of page):**
> "These next few questions help us understand your project budget so we can give you the most accurate and relevant advice. There are no wrong answers — we work with projects of all sizes."

This framing reduces drop-off on the budget question by 20-30%. Without it, homeowners feel judged.

---

#### Q7: What's your approximate budget range for this project?

| Setting | Value |
|---------|-------|
| **Type** | Single-select (radio buttons) |
| **Required** | Yes |
| **Maps to** | `cf_budget_range` |
| **Options** | Under $300,000 / $300,000 – $500,000 / $500,000 – $800,000 / $800,000 – $1,200,000 / Over $1,200,000 |

**Scoring:**
| Answer | Points | Rationale |
|--------|--------|-----------|
| Under $300,000 | **HARD DISQUALIFIER** | Below minimum viable project cost for custom builders. Auto-routes to Not Now with polite decline. |
| $300,000 – $500,000 | 5 | Entry-level custom build — viable but tight margins |
| $500,000 – $800,000 | 10 | Sweet spot for most custom builders |
| $800,000 – $1,200,000 | 15 | Premium project — high margin, high engagement |
| Over $1,200,000 | 15 | Top tier — builder will prioritise this lead |

**Hard disqualifier behaviour:** If selected, score is overridden to 0 regardless of all other answers. Contact routes to Not Now with a specific polite decline: "Based on your budget, our preconstruction services may not be the best fit right now. We recommend [alternative resource]."

---

#### Q8: Where are you at with financing?

| Setting | Value |
|---------|-------|
| **Type** | Single-select (radio buttons) |
| **Required** | Yes |
| **Maps to** | `cf_financing_status` |
| **Options** | Pre-approved by a lender / Working with a broker (in progress) / Haven't started the finance process yet / Cash buyer (no finance needed) |

**Scoring:**
| Answer | Points | Rationale |
|--------|--------|-----------|
| Pre-approved by a lender | 15 | Ready to commit — finance is not a blocker |
| Cash buyer (no finance needed) | 15 | Same — no finance dependency |
| Working with a broker (in progress) | 12 | Active — will likely be approved soon |
| Haven't started the finance process yet | 6 | Risk — may discover they can't afford the project |

---

### Page 4: Working Together

---

#### Q9: Are you the main decision-maker for this project?

| Setting | Value |
|---------|-------|
| **Type** | Single-select (radio buttons) |
| **Required** | Yes |
| **Maps to** | `cf_decision_maker` |
| **Options** | Yes, I'm the sole decision-maker / It's a shared decision (with partner/spouse) / Someone else will make the final call |

**Scoring:**
| Answer | Points | Rationale |
|--------|--------|-----------|
| Yes, I'm the sole decision-maker | 10 | No partner veto risk |
| It's a shared decision (with partner/spouse) | 8 | Common — triggers partner coordination flow |
| Someone else will make the final call | 3 | Red flag — person filling out form may not have authority |

---

#### Q10: *(Conditional — only shows if Q9 = "Shared decision")*
What's your partner's name and best contact?

| Setting | Value |
|---------|-------|
| **Type** | Two text fields: Name + Email or Phone |
| **Required** | No (but encouraged) |
| **Maps to** | `cf_partner_name`, `cf_partner_email` |
| **Helper text** | "We'll send them a brief overview of what we discussed, so you're both on the same page." |

**Scoring:** 0 points — informational only. Triggers partner notification micro-workflow in WF-03.

**Why this is critical for profit:** The partner who hasn't seen the education content is the #1 deal-killer at discovery calls. Getting their contact info HERE means we can educate them in parallel. This single question can increase discovery-to-proposal conversion by 20-30%.

---

#### Q11: Are there any specific challenges with your site?

| Setting | Value |
|---------|-------|
| **Type** | Single-select (radio buttons) |
| **Required** | Yes |
| **Maps to** | `cf_site_challenges` |
| **Options** | No significant challenges that I'm aware of / Some potential issues (slope, flooding, heritage, bushfire zone) / Significant challenges (steep site, difficult access, contamination, etc.) |

**Scoring:**
| Answer | Points | Rationale |
|--------|--------|-----------|
| No significant challenges | 10 | Straightforward project |
| Some potential issues | 7 | Needs investigation but not a dealbreaker |
| Significant challenges | 3 | Higher cost, higher risk, longer timeline |

**Note:** Add `cf_site_challenges` to Custom Fields if not present. Values: `None` / `Some` / `Significant`

---

#### Q12: How did you hear about us?

| Setting | Value |
|---------|-------|
| **Type** | Single-select (dropdown) |
| **Required** | Yes |
| **Maps to** | `cf_how_heard` |
| **Options** | Google search / Facebook or Instagram / Referred by a friend or family member / Referred by a professional (architect, broker, etc.) / Builder website / House & Land marketplace / Other |

**Scoring:** 0 points — informational only. **But this is the most valuable data point for the builder's marketing budget.**

| Answer | Hidden value (for attribution reporting) |
|--------|------------------------------------------|
| Google search | `google_search` |
| Facebook or Instagram | `social_media` |
| Referred by a friend or family | `referral_personal` |
| Referred by a professional | `referral_professional` |
| Builder website | `website_organic` |
| House & Land marketplace | `house_and_land` |
| Other | `other` |

---

### Page 5: The Close (Commitment Questions)

> **Page intro text:**
> "Last couple of questions — almost done!"

---

#### Q13: Our process involves a professional preconstruction service to give you accurate costing before any construction commitment. There's a fee for this work. Is that something you'd be open to?

| Setting | Value |
|---------|-------|
| **Type** | Single-select (radio buttons) |
| **Required** | Yes |
| **Maps to** | `cf_open_to_fee` |
| **Options** | Yes, that makes sense / I'd need to understand more about what's included / No, I'm only looking for free quotes |

**Scoring:**
| Answer | Points | Rationale |
|--------|--------|-----------|
| Yes, that makes sense | 15 | Ideal client — understands value of paid preconstruction work |
| I'd need to understand more about what's included | 8 | Needs education — perfect for the nurture sequence |
| No, I'm only looking for free quotes | **HARD DISQUALIFIER** | Will never convert to a paid engagement. Routes to Not Now. |

**Why this question wording matters:**
- It says "professional preconstruction service" not "fee" — frames it as a deliverable, not a cost
- It says "accurate costing before any construction commitment" — frames the fee as protecting the homeowner, not the builder
- The "No" option says "free quotes" which subtly frames free-quote-seekers as less serious

**Hard disqualifier behaviour:** Same as Q7 — overrides to 0, routes to Not Now with specific polite decline messaging.

---

#### Q14: How would you prefer we get in touch?

| Setting | Value |
|---------|-------|
| **Type** | Single-select (radio buttons) |
| **Required** | Yes |
| **Maps to** | `cf_communication_preference` |
| **Options** | Email / Phone call / SMS / Any of the above |

**Scoring:** 0 points — informational only. Informs which channel WF-03/WF-04 should prioritise for outreach.

---

#### Q15: Is there anything else you'd like us to know about your project?

| Setting | Value |
|---------|-------|
| **Type** | Multi-line text (textarea) |
| **Required** | No |
| **Maps to** | `cf_additional_notes` |
| **Placeholder** | "Optional — anything you'd like to share about your vision, concerns, or questions" |

**Scoring:** 0 points — informational only. Gives the builder context for the discovery call. Often contains gold: "We've been planning this for 3 years" (very serious) or "Just exploring options" (tyre-kicker).

**Note:** Add `cf_additional_notes` to Custom Fields as a Text (multi-line) field.

---

## Scoring Summary

### Maximum possible score: 145 points

| Question | Max Points | Weight |
|----------|-----------|--------|
| Q1: Project type | 10 | 6.9% |
| Q2: Location | 0 | — |
| Q3: Land status | 15 | 10.3% |
| Q4: Design status | 15 | 10.3% |
| Q5: Timeline | 15 | 10.3% |
| Q6: Prior quotes | 10 | 6.9% |
| Q7: Budget range | 15 | 10.3% |
| Q8: Financing | 15 | 10.3% |
| Q9: Decision maker | 10 | 6.9% |
| Q10: Partner info | 0 | — |
| Q11: Site challenges | 10 | 6.9% |
| Q12: How heard | 0 | — |
| Q13: Open to fee | 15 | 10.3% |
| Q14: Communication pref | 0 | — |
| Q15: Additional notes | 0 | — |
| **TOTAL** | **145** | **100%** |

### Score Normalisation

Raw score (0-145) is normalised to 0-100 for `cf_qualification_score`:

```
cf_qualification_score = ROUND((raw_score / 145) * 100)
```

### Routing Bands (on normalised 0-100 scale)

| Band | Normalised Score | Raw Score (approx) | Tag | Pipeline Stage | What Happens |
|------|-----------------|-------------------|-----|----------------|--------------|
| **Hot** | 80-100 | 116-145 | `lead-hot` | Qualified | Immediate calendar link + builder notification |
| **Warm** | 50-79 | 73-115 | `lead-warm` | Nurture | 7-touch education sequence over 10 days |
| **Cold** | 0-49 | 0-72 | `lead-cold` | Not Now | Polite decline + quarterly re-engagement |

### Hard Disqualifiers (Override All Scoring)

| Trigger | Result |
|---------|--------|
| Q7 = "Under $300,000" | Score → 0, route to Not Now regardless |
| Q13 = "No, I'm only looking for free quotes" | Score → 0, route to Not Now regardless |

---

## Typical Score Profiles

### Hot Lead Example (Score: 88/100 = 127/145)
- New Build (10) + Own Land (15) + Plans Ready (15) + ASAP (15) + Pre-approved (15) + First contact (10) + $500-800K (10) + Yes to fee (15) + Sole decision-maker (10) + No site challenges (10) + Using broker (12) = **137** → normalised **94**

### Warm Lead Example (Score: 62/100 = 90/145)
- Extension (8) + Own Land (15) + Concept only (10) + 3-6 months (12) + Using broker (12) + 1-2 builders (10) + $300-500K (5) + Need more info (8) + Shared decision (8) + No challenges (10) = **98** → normalised **68**

### Cold Lead Example (Score: 35/100 = 51/145)
- Renovation (6) + Still looking (5) + Nothing yet (5) + 12+ months (3) + Not started finance (6) + 3+ builders (5) + $300-500K (5) + Need more info (8) + Other decides (3) + Significant challenges (3) = **49** → normalised **34**

---

## GHL Implementation Notes

### Survey-to-Field Mapping Checklist

Every survey answer MUST auto-populate the corresponding custom field on submission. Verify each mapping in GHL:

| Survey Question | Maps To | Field Type | Verify |
|-----------------|---------|-----------|--------|
| Q1 | `cf_project_type` | Dropdown | [ ] |
| Q2 | `cf_site_address` | Text | [ ] |
| Q3 | `cf_land_status` | Dropdown | [ ] |
| Q4 | `cf_design_status` | Dropdown | [ ] |
| Q5 | `cf_timeline` | Dropdown | [ ] |
| Q6 | `cf_prior_quotes` | Dropdown | [ ] |
| Q7 | `cf_budget_range` | Dropdown | [ ] |
| Q8 | `cf_financing_status` | Dropdown | [ ] |
| Q9 | `cf_decision_maker` | Dropdown | [ ] |
| Q10 | `cf_partner_name` + `cf_partner_email` | Text + Email | [ ] |
| Q11 | `cf_site_challenges` | Dropdown | [ ] |
| Q12 | `cf_how_heard` | Dropdown | [ ] |
| Q13 | `cf_open_to_fee` | Dropdown | [ ] |
| Q14 | `cf_communication_preference` | Dropdown | [ ] |
| Q15 | `cf_additional_notes` | Text (multi-line) | [ ] |

### New Custom Fields Required

These fields are referenced in the survey but were not in the original PREBUILD_AUTOPILOT_CONTEXT.md:

| Field | Key | Type | Values |
|-------|-----|------|--------|
| Design Status | `cf_design_status` | Dropdown | Plans Ready / Concept Only / Nothing Yet |
| Prior Quotes | `cf_prior_quotes` | Dropdown | First Contact / 1-2 Builders / 3+ Builders |
| Site Challenges | `cf_site_challenges` | Dropdown | None / Some / Significant |
| Additional Notes | `cf_additional_notes` | Text (multi-line) | Free text |

### Survey Completion Trigger

On submission, GHL should fire the `SRV-Qualification` submitted trigger which starts WF-03. WF-03 then:

1. Removes `survey-pending` tag
2. Adds `survey-completed` tag
3. Sends survey data to scoring endpoint (webhook to n8n or Cloud Function)
4. Receives score back
5. Sets `cf_qualification_score`, `cf_lead_temperature`
6. Applies tags and routes to correct pipeline stage

### Thank You Page Strategy

**For Hot leads (score >=80):** Redirect to calendar booking page immediately. The homeowner is motivated right now — don't make them wait for an email. CTA: "Your project looks like a great fit! Book your intro call now."

**For all others:** Show a simple "Thanks! We'll review your answers and be in touch within 24 hours." Don't show the calendar — let the education sequence warm them up first.

GHL can't conditionally redirect based on score (score isn't calculated until after redirect). Two options:
1. **Simple:** Generic thank-you page for all. Calendar link arrives via SMS/email seconds later for Hot leads.
2. **Advanced:** Redirect all to a thank-you page that includes the calendar embed. Hot leads book immediately, warm leads ignore it and get nurtured. No downside to showing it.

**Recommendation:** Option 2. Include the calendar on the thank-you page. Warm leads who are actually more ready than their score suggests will self-select by booking.

---

## Survey UX Best Practices for Residential Builders

1. **Builder's branding on every page** — Logo, colours, font. This is the homeowner's first interaction with the builder's "system." It must feel professional, not like a generic survey tool.

2. **Progress bar visible** — Shows "Page 2 of 5" or percentage. Reduces abandonment.

3. **Mobile-optimised** — Large tap targets, no horizontal scrolling, auto-advance on single-select.

4. **No "Back" button anxiety** — Make it easy to go back and change answers. Homeowners second-guess themselves on budget questions.

5. **Social proof on budget page** — Consider adding a small note: "Most of our clients invest between $500K–$1.2M in their custom home." This anchors expectations and normalises the higher budget ranges.
