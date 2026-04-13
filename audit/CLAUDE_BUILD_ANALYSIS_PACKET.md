# Claude — Build analysis packet (new chat)

Use this file as the **primary** context. Add **exactly one** companion file (see below) so the model can compare **intent vs reality**.

---

## Companion file (pick one — second attachment)

| You want Claude to focus on… | Attach this second file |
|------------------------------|-------------------------|
| **Full product spec** — every workflow, template, field, rule, naming lock | `PREBUILD_AUTOPILOT_CONTEXT.md` *(repo root; long but complete)* |
| **Live Factory vs that spec** — gaps, stage-name mismatches, inventory | `audit/SUBACCOUNT_BUILD_STATUS_FULL_AUDIT.md` |
| **Raw live inventory** (forms, calendars, tags, deep workflow JSON if you ran `--deep`) | `audit/GHL_THOROUGH_ACCOUNT_EXPORT.md` — *regenerate first:* `python3 audit/ghl_audit_collector.py --api-key … --location-id … --output audit/audit_data.json --deep --markdown audit/GHL_THOROUGH_ACCOUNT_EXPORT.md` |

**Recommended default pair for “everything about the build”:** **this packet + `PREBUILD_AUTOPILOT_CONTEXT.md`.**

---

## What you’re building (one paragraph)

**PreBuild Autopilot** — a GoHighLevel Factory snapshot for Australian residential builders: enquiry → qualification survey → scoring/routing → education → intro call → proposal / e-sign / payment → portal. One sub-account per builder; customise via Custom Values; no per-client forks. Critical rules: no hardcoded fees (`{{custom_values.service_1_fee}}`), no WF-07, SMS ends with “Reply STOP to opt out”, `{{custom_values.google_review_link}}` for reviews.

---

## Remaining work (ranked — do these in order)

1. **Prove WF-03** — External scorer (`audit/wf03_scoring_engine.py`) deployed and wired; contact fields updated; routing matches **live** pipeline stage **names** (e.g. `Qualified - Hot` vs spec “Qualified”).
2. **Reconcile field keys** — e.g. `cf_lead_score` vs `cf_qualification_score`; `cf_finance_status` vs `cf_financing_status`; survey option strings vs scorer (`wf03_scoring_engine.py`).
3. **Find or build WF-08** (Portal Welcome) — Not on workflow list in last API export; confirm in UI.
4. **Clarify WF-11** — Live `WF-11-Partner-Notifications` vs spec “Builder Internal Tasks”.
5. **Custom values** — Ensure `fee_structure`, `survey_link`, `google_review_link`, portal/calendar links exist and are populated (API list alone may hide values).
6. **Tags** — Spec expects many tags (`survey-pending`, `call-booked`, etc.); only a subset appeared in last export — confirm created by workflows or pre-created.
7. **Publish + test** — Workflows were **draft** in last export; calendar **inactive**; run end-to-end test contacts after publish.
8. **Templates** — API often returns empty bodies; verify in GHL; add **ET-BOOK-Confirmation** per open items.
9. **Architecture** — Move fee/phase-sensitive logic off location-level Custom Values where concurrent clients would clash (`CLAUDE.md` open item).
10. **n8n cold outreach** — Separate system; known bugs in spec §19.

---

## “What can we do better?” (themes for Claude to stress-test)

- **Demo readiness:** Seeded contacts + recorded happy-path vs cold/warm/hot/disqualified.
- **Single source of truth:** Spec vs live naming (pipeline stages, templates, WF names).
- **Observability:** Builder-facing weekly summary / dashboard (even lightweight).
- **Compliance:** Every SMS opt-out; real review URL; Australian context copy.
- **Sellability:** ROI story, onboarding checklist, snapshot export process (M4/M5).
- **Code vs GHL:** `audit/DEEP_SPEC_ANALYSIS.md` for scoring-engine and spec contradictions.

---

## Suggested prompts (paste after attachments)

1. “Given the spec and this packet, list **spec vs live** mismatches and whether to change GHL or the spec.”
2. “Produce a **2-week execution plan** with owners, verification steps, and ‘done’ definitions.”
3. “Identify **single points of failure** in the funnel and mitigations.”
4. “What would you **cut or defer** for a credible v1 pilot?”

---

## Other repo files (only if Claude needs depth)

| Path | Use |
|------|-----|
| `audit/audit_data.json` | Latest API JSON (refresh with collector) |
| `audit/wf03_scoring_engine.py` | Scoring logic for WF-03 |
| `audit/DEEP_SPEC_ANALYSIS.md` | Spec/code bugs and risks |
| `audit/GHL_VERIFICATION_CHECKLIST.md` | Manual UI checklist |
| `CLAUDE.md` | Milestones + current open items |

---

*This packet is a router + prioritised backlog. Numbers above align with `CLAUDE.md` and `audit/SUBACCOUNT_BUILD_STATUS_FULL_AUDIT.md`; refresh those sources after you change GHL.*
