# CLAUDE.md — PreBuild Autopilot / GHL Sub-Account

> **Read this first, every session.** This is the shared memory layer for all Claude instances working on this project — terminal, Cursor, Claude Code, any environment.

---

## What This Project Is

**PreBuild Autopilot** — a done-for-you GoHighLevel snapshot that automates the preconstruction sales funnel for Australian residential builders (5–30 homes/year). Built and operated by Jerald / CentriWeb.

It takes a builder from raw inbound enquiry → lead qualification → education → discovery call → paid preconstruction agreement → client portal. No manual sorting of leads. Only pre-qualified, deposit-paying clients reach the builder.

**Business model:** ~$2,500 setup + $297/month per builder client. Installed from a Factory snapshot. One sub-account per builder, customised via Custom Values (no forks).

---

## Who Is Working On This

| Role | Claude Instance | Knows About |
|------|----------------|-------------|
| Repo/code work | Claude Code (this instance, any terminal) | Everything in this repo |
| GHL live account | Claude Code + GHL MCP (once set up) | Live account state |
| Strategy/context | Other Claude account (web or API) | Additional business context not yet in this repo |

**If you have context from another Claude session or account that's not in this repo — paste it into `KNOWLEDGE_TRANSFER.md` in this directory so all instances can read it.**

---

## Current Build Status (Update This When Things Change)

| Milestone | Status | Notes |
|-----------|--------|-------|
| M1 — Factory Baseline | Likely complete | Pipeline + Custom Values + naming conventions locked |
| M2 — Core Workflows Live | Unknown | WF-03 scoring unverified — see open items |
| M3 — Demo Ready | Unknown | Seeded demo contacts not confirmed |
| M4 — Snapshot v1.1 Export | Unknown | |
| M5 — Pilot Install | Unknown | |

**Last verified:** March 2026 (spec review only — live account not yet inspected)

---

## Open Items Right Now (Ranked)

1. **WF-03 scoring is unverified** — the scoring engine exists (`audit/wf03_scoring_engine.py`) but whether WF-03 in GHL actually calls it is unknown. This is the #1 risk. If scoring isn't working, nothing routes correctly.
2. **GHL MCP not yet set up** — needed to inspect the live account from terminal. See `mcp/SETUP_GUIDE.md`.
3. **Location ID not yet provided** — required for both the collector script and the MCP.
4. **Dynamic Custom Values architecture flaw** — `current_service_fee` etc. are location-level in GHL. Will break when multiple clients are in different phases simultaneously. Fix: convert to contact-level custom fields.
5. **n8n outreach bugs** — 5 known bugs in the cold outreach system (Section 19 of context doc). Not yet fixed.
6. **ET-BOOK-Confirmation** — template copy was missing from spec, now added to context doc but not yet built in GHL.

---

## Key Files In This Repo

| File | What It Is |
|------|-----------|
| `PREBUILD_AUTOPILOT_CONTEXT.md` | **THE SPEC** — read this in full before any GHL work. Single source of truth for all architecture, naming, workflows, templates, custom fields. |
| `audit/DEEP_SPEC_ANALYSIS.md` | Bugs found, architecture risks, improvement priorities. Start here to understand what needs fixing. |
| `audit/GHL_VERIFICATION_CHECKLIST.md` | Section-by-section checklist to verify live GHL account state against spec. |
| `audit/wf03_scoring_engine.py` | The external scoring engine for WF-03. Deploy to n8n/Cloud Function/Lambda. Fixed bugs: MAX_RAW_SCORE, tag removal, referral scoring. |
| `audit/ghl_audit_collector.py` | Script to pull live data from GHL. Run locally with `--api-key` + `--location-id`. |
| `audit/PREBUILD_AUTOPILOT_AUDIT_REPORT.md` | Full architecture audit report (spec-based, not live account). |
| `audit/PRIORITY_ACTION_MATRIX.md` | Execution order for all known tasks. |
| `audit/SELLABILITY_STRATEGY.md` | Productisation and demo strategy. |
| `audit/SRV_QUALIFICATION_FULL_SPEC.md` | Full survey spec with all 15 questions. |
| `mcp/SETUP_GUIDE.md` | How to install GHL MCP for live account access from terminal. |
| `mcp/setup.sh` | One-command MCP install script. |
| `mcp/claude_mcp_config.json` | Claude Code settings entry for GHL MCP. |

---

## Critical Rules (Never Violate These)

1. **Never use QBE, FQE, Stage 2, Stage 3 terminology** — generic refactor removed PAP dependency
2. **Never hardcode fee amounts** — always `{{custom_values.service_1_fee}}`
3. **Never reference WF-07** — removed in v1.1, merged into WF-06
4. **Never make changes directly in client sub-accounts** — Factory only → snapshot → installs
5. **Never fork the snapshot per builder** — use `fee_structure` Custom Value instead
6. **Always include "Reply STOP to opt out" in every SMS template**
7. **Always use `{{custom_values.google_review_link}}`** — never hardcode review placeholders

---

## GHL Account Access

**API Key:** `pit-335bf0ee-b8e4-4eaa-be07-997052ceb717`
**Location ID:** *(not yet provided — get from GHL → Settings → Company → Locations)*

### To access live account from terminal:
```bash
# Option 1 — run data collector locally:
python3 audit/ghl_audit_collector.py \
  --api-key "pit-335bf0ee-b8e4-4eaa-be07-997052ceb717" \
  --location-id "YOUR_LOCATION_ID"

# Option 2 — install MCP for full tool access:
./mcp/setup.sh
# then add location ID to ~/.claude/settings.json and ~/.claude/mcp/ghl-mcp/.env
```

> Note: The Claude Code cloud environment (GitHub/web sessions) blocks outbound HTTPS to GHL. Run these on your local machine or VPS where there's direct internet access.

---

## Architecture Quick Reference

**Pipeline:** `PreBuild Pipeline` — 8 active stages + 2 non-active (Not Now, Lost)

**Workflows:** WF-01 through WF-12 (WF-07 removed). Key ones:
- WF-01: Speed-to-Lead (fires <60s on any new contact)
- WF-03: Scoring + Routing (THE critical workflow — requires external scorer)
- WF-04: Education sequence (7 touches over 10 days for warm leads)
- WF-06: Proposal + E-Sign + Payment (handles Phase 1 AND Phase 2 via `cf_service_phase`)

**Fee structures:** `two_tier` (default) / `single_tier` / `no_fee` — set via `fee_structure` Custom Value

**Scoring bands:** Hot ≥80 | Warm 50–79 | Cold <50 | Disqualified (budget <$300K OR fee rejection)

**External dependencies:**
- Stripe (builder's own account) — payment processing
- n8n — cold outreach system (separate from GHL funnel, has known bugs)
- External scoring endpoint — required for WF-03 (n8n Code Node or Cloud Function)

---

## Bringing Context From Another Claude Session

If you have notes, decisions, or context from another Claude account or session:

1. Copy the relevant content
2. Paste it into `KNOWLEDGE_TRANSFER.md` in this directory
3. Commit and push it
4. Every Claude instance will then have it on next read

This repo is the shared brain. If it's not in the repo, it doesn't exist for other Claude instances.

---

*Maintained by Jerald / CentriWeb. Update this file whenever the project status changes or new decisions are made.*
*Last updated: March 2026*
