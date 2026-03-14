# GHL Written Content Dump — Every Word, Label, and Message

> **For Claude:** This file contains every piece of written content in the PreBuild Autopilot system — templates, survey questions, form labels, and inline copy. Source: `PREBUILD_AUTOPILOT_CONTEXT.md` Section 8 + `SRV_QUALIFICATION_FULL_SPEC.md`.
>
> **Note:** The GHL API does not return this content (forms/surveys return 401; templates return empty body). This dump is the spec source of truth.

---

## SMS Templates (9)

### SMS-STL-Welcome
```
Hi {{contact.first_name}}, thanks for reaching out to {{custom_values.builder_name}}! We'd love to help with your building project. To get started, please take our quick project questionnaire (about 3 mins): {{custom_values.survey_link}} — The {{custom_values.builder_name}} Team. Reply STOP to opt out.
```

### SMS-SRV-Reminder-1 (72hrs)
```
Hey {{contact.first_name}}, just checking in — have you had a chance to complete our quick project questionnaire? Here's the link: {{custom_values.survey_link}} — {{custom_values.builder_name}}. Reply STOP to opt out.
```

### SMS-SRV-Final (192hrs)
```
Hi {{contact.first_name}}, last nudge from us! We'd love to help with your building project. Complete our 3-min questionnaire here: {{custom_values.survey_link}} — or reply CALL and we'll ring you. — {{custom_values.builder_name}}. Reply STOP to opt out.
```

### SMS-QUAL-Hot-BookCall
```
Great news {{contact.first_name}}! Based on your project details, we'd love to chat. Book a quick call here: {{custom_values.calendar_link}} — {{custom_values.builder_name}}. Reply STOP to opt out.
```

### SMS-EDU-01-Checkin
```
Hey {{contact.first_name}}, did you get a chance to read about our process? Any questions, just reply to this message — we're here to help. — {{custom_values.builder_name}}. Reply STOP to opt out.
```

### SMS-EDU-02-CTA
```
Hey {{contact.first_name}}, we've shared everything about our process over the past week. Ready to chat? Book a quick call: {{custom_values.calendar_link}} — {{custom_values.builder_name}}. Reply STOP to opt out.
```

### SMS-PROP-Sent
```
Hi {{contact.first_name}}, we've just sent through your {{custom_values.agreement_title}} for your project. Please check your email to review and sign. Any questions, just reply here! — {{custom_values.builder_name}}. Reply STOP to opt out.
```

### SMS-PAY-Confirmation
```
Payment received — thank you! Your {{custom_values.builder_name}} project portal is now live: {{custom_values.portal_link}}. Reply STOP to opt out.
```

### SMS-WIN-ReviewRequest (14 days after Won)
```
Hi {{contact.first_name}}, it's been great working with you on your project. If you're happy with the process, we'd love it if you could leave us a quick Google review — it helps other homeowners find us: {{custom_values.google_review_link}}. Thanks so much! — {{custom_values.builder_name}}. Reply STOP to opt out.
```

---

## Inline SMS (Workflow Actions — Not Stored as Templates)

### WF-05 Booking Confirmation (immediate)
```
Confirmed! Your call with {{custom_values.builder_name}} is on {{appointment.date}} at {{appointment.time}}. We'll call you on {{contact.phone}}.
```

### WF-05 24hr Reminder
```
Reminder: your call with {{custom_values.builder_name}} is tomorrow at {{appointment.time}}. Looking forward to chatting!
```

### WF-05 No-Show
```
Hi {{contact.first_name}}, we missed you on today's call. No worries — would you like to reschedule? {{custom_values.calendar_link}} — {{custom_values.builder_name}}. Reply STOP to opt out.
```

### WF-10 Stale Lead (builder internal)
```
Heads up — {{contact.name}} hasn't had a pipeline update in 7 days. Review their contact and take action.
```

---

## Email Templates (14)

### ET-STL-01-Welcome
**Subject:** Thanks for your enquiry, {{contact.first_name}} — here's what happens next

**Body:**
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

### ET-SRV-Reminder-2 (120hrs)
**Subject:** Quick reminder — your project questionnaire

**Body:**
```
Hi {{contact.first_name}},

We noticed you haven't had a chance to complete our project questionnaire yet. No worries — it only takes about 3 minutes, and it helps us understand your project so we can give you the most relevant advice.

→ Complete it here: {{custom_values.survey_link}}

Prefer to chat instead? You can book a quick call with us here: {{custom_values.calendar_link}}

{{custom_values.builder_name}}
```

### ET-QUAL-Hot-BookCall
**Subject:** Your project looks like a great fit — let's talk

**Body:**
```
Hi {{contact.first_name}},

Thanks for completing our questionnaire. Based on your answers, your project sounds like a great fit for what we do.

The next step is a quick intro call — just 30 minutes to talk through your plans and see how we can help.

→ Book your call here: {{custom_values.calendar_link}}

Talk soon,
{{custom_values.builder_name}}
{{custom_values.builder_phone}}
```

### ET-EDU-01-Process-Overview
**Subject:** Here's how {{custom_values.builder_name}} turns your vision into reality

**Body:**
```
Hi {{contact.first_name}},

Building a home is one of the biggest decisions you'll make. That's why we've developed {{custom_values.process_description}} to make sure every dollar is accounted for before construction begins.

Here's how it works:

Stage 1 — Getting to Know Each Other
We learn about your project, priorities, and budget through a quick questionnaire and an intro call. No obligations, no surprises.

Stage 2 — {{custom_values.service_1_name}}
We prepare a {{custom_values.service_1_name}} — a professional estimate of your project cost based on your design brief. This gives you a realistic number to work with before spending money on detailed drawings.

Stage 3 — {{custom_values.service_2_name}} *(Include only for two_tier — use workflow If/Then on fee_structure)*
Once the budget checks out, we move into a {{custom_values.service_2_name}} — a fully itemised estimate with subcontractor and supplier pricing. This is what you need to sign a construction contract.

We've attached a one-page overview so you can see exactly what's included at each stage.

→ Ready to take the next step? Book a call: {{custom_values.calendar_link}}

{{custom_values.builder_name}}
```

### ET-EDU-02-Service-1-Explainer
**Subject:** What's included in a {{custom_values.service_1_name}}?

**Body:**
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

### ET-EDU-03-Service-2-Explainer
**Subject:** From budget range to fixed price — here's what the next stage involves

**Body:**
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

### ET-EDU-04-Testimonial
**Subject:** What our clients say about working with us

**Body:**
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

### ET-EDU-05-CTA-Next-Step
**Subject:** Ready when you are, {{contact.first_name}}

**Body:**
```
Hi {{contact.first_name}},

Over the past week, we've shared how our process works, what's included in our {{custom_values.service_1_name}} and {{custom_values.service_2_name}}, and what our clients think.

If you're ready to explore whether we're the right fit for your project, the next step is a conversation — no pressure, no commitment.

→ Book a call: {{custom_values.calendar_link}}

Or simply reply to this email with your questions.

{{custom_values.builder_name}}
```

### ET-BOOK-Confirmation
**Subject:** Your call with {{custom_values.builder_name}} is confirmed

**Body:**
```
Hi {{contact.first_name}},

Your intro call with {{custom_values.builder_name}} is confirmed.

Date: {{appointment.date}}
Time: {{appointment.time}}
Format: We'll call you on {{contact.phone}}

Before the call, it helps to have these things in mind:
— Your rough build budget or budget range
— Whether you've started on plans or have a designer in mind
— Your preferred start timeline

If you need to reschedule, you can do so here: {{custom_values.calendar_link}}

Looking forward to chatting.

{{custom_values.builder_name}}
{{custom_values.builder_phone}}
```

### ET-PROP-Agreement-Sent
**Subject:** Your {{custom_values.agreement_title}} — {{custom_values.builder_name}}

**Body:**
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

### ET-PROP-Reminder-48hr
**Subject:** Just checking in — your agreement is waiting

**Body:**
```
Hi {{contact.first_name}},

Just a quick reminder that your {{custom_values.agreement_title}} is still waiting for your signature.

→ Sign here: {{proposal.link}}

Any questions before signing? Reply to this email and we'll get back to you quickly.

{{custom_values.builder_name}}
```

### ET-PAY-Confirmation
**Subject:** Payment confirmed — we're getting started on your project

**Body:**
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

### ET-PORTAL-Welcome
**Subject:** Welcome to your {{custom_values.builder_name}} project portal

**Body:**
```
Hi {{contact.first_name}},

Your personal project portal is now live.

→ Log in here: {{custom_values.portal_link}}

You'll see your current project status and what's coming next. We'll keep your portal updated as things progress.

Questions at any time? Reply to this email or call {{custom_values.builder_phone}}.

{{custom_values.builder_name}}
```

---

## Survey: SRV-Qualification (15 Questions)

**Survey Name:** SRV-Qualification  
**URL slug:** `/project-questionnaire`  
**Thank You (Hot):** Redirect to calendar  
**Thank You (Warm/Cold):** "We'll be in touch within 24 hours"

### Page 1: About Your Project

**Page intro:** *(none)*

| Q | Question Text | Type | Maps To | Options / Placeholder |
|---|---------------|------|---------|----------------------|
| 1 | What type of project are you planning? | Single-select | cf_project_type | New Home Build / Knockdown & Rebuild / Extension / Renovation |
| 2 | Where will this project be located? | Text | cf_site_address | Placeholder: "Suburb or full address" |
| 3 | Do you already have land or a property for this project? | Single-select | cf_land_status | Yes, I own the land/property / Under contract (settlement pending) / Still looking for land |

### Page 2: Your Plans & Timeline

| Q | Question Text | Type | Maps To | Options / Placeholder |
|---|---------------|------|---------|----------------------|
| 4 | How far along are your design plans? | Single-select | cf_design_status | I have detailed plans or drawings ready / I have a rough concept or sketch / I haven't started on plans yet |
| 5 | When would you ideally like to start construction? | Single-select | cf_timeline | As soon as possible / Within 3–6 months / 6–12 months from now / More than 12 months away |
| 6 | Have you spoken with any other builders about this project? | Single-select | cf_prior_quotes | No, you're my first point of contact / Yes, 1–2 other builders / Yes, 3 or more builders |

### Page 3: Budget & Finances

**Page intro:** "These next few questions help us understand your project budget so we can give you the most accurate and relevant advice. There are no wrong answers — we work with projects of all sizes."

| Q | Question Text | Type | Maps To | Options / Placeholder |
|---|---------------|------|---------|----------------------|
| 7 | What's your approximate budget range for this project? | Single-select | cf_budget_range | Under $300,000 / $300,000 – $500,000 / $500,000 – $800,000 / $800,000 – $1,200,000 / Over $1,200,000 |
| 8 | Where are you at with financing? | Single-select | cf_financing_status | Pre-approved by a lender / Working with a broker (in progress) / Haven't started the finance process yet / Cash buyer (no finance needed) |

### Page 4: Working Together

| Q | Question Text | Type | Maps To | Options / Placeholder |
|---|---------------|------|---------|----------------------|
| 9 | Are you the main decision-maker for this project? | Single-select | cf_decision_maker | Yes, I'm the sole decision-maker / It's a shared decision (with partner/spouse) / Someone else will make the final call |
| 10 | What's your partner's name and best contact? *(Conditional: only if Q9 = Shared decision)* | Two text fields | cf_partner_name, cf_partner_email | Helper: "We'll send them a brief overview of what we discussed, so you're both on the same page." |
| 11 | Are there any specific challenges with your site? | Single-select | cf_site_challenges | No significant challenges that I'm aware of / Some potential issues (slope, flooding, heritage, bushfire zone) / Significant challenges (steep site, difficult access, contamination, etc.) |
| 12 | How did you hear about us? | Single-select | cf_how_heard | Google search / Facebook or Instagram / Referred by a friend or family member / Referred by a professional (architect, broker, etc.) / Builder website / House & Land marketplace / Other |

### Page 5: The Close

**Page intro:** "Last couple of questions — almost done!"

| Q | Question Text | Type | Maps To | Options / Placeholder |
|---|---------------|------|---------|----------------------|
| 13 | Our process involves a professional preconstruction service to give you accurate costing before any construction commitment. There's a fee for this work. Is that something you'd be open to? | Single-select | cf_open_to_fee | Yes, that makes sense / I'd need to understand more about what's included / No, I'm only looking for free quotes |
| 14 | How would you prefer we get in touch? | Single-select | cf_communication_preference | Email / Phone call / SMS / Any of the above |
| 15 | Is there anything else you'd like us to know about your project? | Multi-line text | cf_additional_notes | Placeholder: "Optional — anything you'd like to share about your vision, concerns, or questions" |

---

## Hard Disqualifier Messages

**Q7 = Under $300,000:**
> Based on your budget, our preconstruction services may not be the best fit right now. We recommend [alternative resource].

**Q13 = No, I'm only looking for free quotes:**
> *(Same polite decline — routes to Not Now)*

---

## Forms (Spec Reference)

| Form | Purpose | Full field spec |
|------|---------|-----------------|
| FRM-Lead-Intake | Initial lead capture | Minimal — typically name, email, phone. May redirect to survey. |
| FRM-Pre-Call | Pre-discovery call prep | *(Spec does not detail field-by-field)* |
| SRV-Qualification-Survey | Main qualification | See Survey section above — this is the primary form |

---

## Builder Task Copy (Internal)

| Trigger | Task Text |
|---------|-----------|
| Survey completed | "Review {{contact.name}}'s survey answers (score: {{cf_qualification_score}})" |
| Call booked | "Prep for call with {{contact.name}} — review their survey answers before the call" |
| Call no-show | "{{contact.name}} may not have shown — confirm what happened and update pipeline" |
| Call cancelled | "{{contact.name}} cancelled their intro call — follow up" |
| Payment received | "{{contact.name}} has paid their {{custom_values.current_service_fee_label}} — project is active." |
| Survey reply | "{{contact.name}} replied to survey reminder — follow up manually" |

---

## Calendar Notes (CAL-Intro-Call)

```
Phone:- {{contact.phone}}
Email:- {{contact.email}}

Need to make a change to this event?
Reschedule:-
{{reschedule_link}}

Cancel:-
{{cancellation_link}}
```

---

*Generated from PREBUILD_AUTOPILOT_CONTEXT.md + SRV_QUALIFICATION_FULL_SPEC.md. This is the canonical written content for the PreBuild Autopilot system.*
