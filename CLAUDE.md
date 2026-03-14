# CLAUDE.md — PreBuild Autopilot / GHL Sub-Account

> **Read this first, every session.** This is the shared memory layer for all Claude instances working on this project — terminal, Cursor, Claude Code, any environment.

---

## What This Project Is

**PreBuild Autopilot** — a done-for-you GoHighLevel snapshot that automates the preconstruction sales funnel for Australian residential builders (5–30 homes/year). Built and operated by Jerald / CentriWeb.

It takes a builder from raw inbound enquiry → lead qualification → education → discovery call → paid preconstruction agreement → client portal. No manual sorting of leads. Only pre-qualified, deposit-paying clients reach the builder.

**Business model:** ~$2,500 setup + $297/month per builder client. Installed from a Factory snapshot. One sub-account per builder, customised via Custom Values (no forks).

---

## Who Is Working On This

| Role | Claude Instance | Location | Knows About |
|------|----------------|----------|-------------|
| Repo/code work | Claude Code (GitHub env) | Cloud (this session) | Everything in this repo |
| Live GHL work | Claude Code + GHL MCP | VPS: root@76.13.212.238 | Live account + this repo |
| Strategy/context | Other Claude account | Web/API | Additional business context |

**VPS:** Hostinger KVM, Ubuntu 24.04, `srv1420954.hstgr.cloud` — `76.13.212.238`
**Project dir on VPS:** `/root/prebuild-autopilot`
**Claude Code on VPS:** Installed via `npm install -g @anthropic-ai/claude-code`

**If you have context from another Claude session or account that's not in this repo — paste it into `KNOWLEDGE_TRANSFER.md` so all instances can read it.**

---

## Current Build Status (Updated March 2026 — Live Account Inspected)

| Milestone | Status | Notes |
|-----------|--------|-------|
| M1 — Factory Baseline | ⚠️ Partial | Pipeline exists but 4 stage names wrong. Fields exist but 2 misnamed, 7 missing. All custom values blank. |
| M2 — Core Workflows Live | ❌ Blocked | All 10 workflows DRAFT. WF-08 missing. Scoring engine not deployed. |
| M3 — Demo Ready | ❌ Not started | No seeded contacts. Custom values blank. Email templates missing. |
| M4 — Snapshot v1.1 Export | ❌ Blocked | Can't export until M2 complete |
| M5 — Pilot Install | ❌ Blocked | |

**Last verified:** March 2026 — live account data pulled via GHL API (see `audit/audit_data.json`)

---

## Open Items Right Now (Ranked by Impact)

### Blockers — fix before anything else works
1. **Rename 4 pipeline stages** — "Qualified - Hot"→"Qualified", "Nurture - Warm"→"Nurture", "Intro Call Booked"→"Discovery Booked", delete "Survey Completed" stage
2. **Rename 2 custom fields** — `cf_lead_score`→`cf_qualification_score`, `cf_finance_status`→`cf_financing_status`
3. **Create 7 missing custom fields** — cf_lead_temperature, cf_design_status, cf_decision_maker, cf_communication_preference, cf_lost_reason, cf_site_address, cf_prior_quotes
4. **Populate all 14 custom values** — all currently blank, nothing in templates will render
5. **Create 11 missing tags** — survey-pending, survey-completed, call-booked, payment-received, etc.
6. **Build 14 email templates** — none exist in GHL (copy in context doc Section 8)
7. **Build 4 missing SMS templates** — SMS-SRV-Final, SMS-QUAL-Hot-BookCall, SMS-PAY-Confirmation, SMS-WIN-ReviewRequest
8. **Create WF-08-Portal-Welcome** — not in account at all
9. **Deploy scoring engine** — code in `audit/wf03_scoring_engine.py`, needs n8n deployment + WF-03 webhook
10. **Publish all workflows** — only after 1–9 done. ALL 10 are Draft.

### Architecture risks (fix before first client)
11. **Dynamic Custom Values flaw** — current_service_fee etc. are location-level, break with concurrent clients
12. **n8n outreach bugs** — 5 documented bugs in Section 19 of context doc

Full gap analysis: `advisory/CURRENT_STATE_GAP_ANALYSIS.md`

---

## Key Files In This Repo

| File | What It Is |
|------|-----------|
| `CLAUDE.md` | **THIS FILE** — shared memory for all Claude instances. Update it when status changes. |
| `KNOWLEDGE_TRANSFER.md` | Paste context from other Claude sessions here so all instances share it. |
| `PREBUILD_AUTOPILOT_CONTEXT.md` | **THE SPEC** — read before any GHL work. Architecture, workflows, templates, naming, custom fields. |
| `audit/DEEP_SPEC_ANALYSIS.md` | Bugs found in spec + code, architecture risks, what to fix and in what order. |
| `audit/GHL_VERIFICATION_CHECKLIST.md` | Section-by-section checklist to verify live GHL account against the spec. |
| `audit/wf03_scoring_engine.py` | External scoring engine for WF-03. Bugs fixed. Deploy to n8n/Cloud Function/Lambda. |
| `audit/ghl_audit_collector.py` | Pulls live data from GHL. Run on VPS with `--api-key` + `--location-id`. |
| `audit/audit_data.json` | Live GHL account data (full JSON dump from collector). |
| `audit/GHL_SUBACCOUNT_DUMP.md` | Human-readable summary of live sub-account for Claude context. |
| `audit/PREBUILD_AUTOPILOT_AUDIT_REPORT.md` | Full architecture audit (spec-based, not live account). |
| `audit/PRIORITY_ACTION_MATRIX.md` | Execution order for all known tasks. |
| `audit/SELLABILITY_STRATEGY.md` | Productisation and demo strategy. |
| `audit/SRV_QUALIFICATION_FULL_SPEC.md` | Full survey spec with all 15 questions and field mappings. |
| `mcp/SETUP_GUIDE.md` | How to install GHL MCP for live account access. |
| `mcp/setup.sh` | MCP-only install script (VPS full setup uses `vps/setup_vps.sh` instead). |
| `mcp/claude_mcp_config.json` | Claude Code settings entry for GHL MCP. |
| `vps/setup_vps.sh` | **Full VPS setup** — installs everything in one command. |
| `CURSOR_VPS_PROMPT.md` | Ready-to-paste Cursor prompt to run VPS setup. Fill in 3 values then give to Cursor. |
| `CURSOR_STARTER_PROMPT.md` | First-message prompt for any new Cursor session on this project. |
| `.cursorrules` | Auto-read by Cursor — project rules, safety rules, naming conventions. |

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

**GHL API Key:** `pit-335bf0ee-b8e4-4eaa-be07-997052ceb717`
**GHL Location ID:** `cVCso4OlgGoOoXMpbxxA`
**Account name:** MASTER FACTORY — PREBUILD ENGINE (Newcastle NSW — Factory account, not a client)
**Anthropic API Key:** *(owner's key from console.anthropic.com — stored in VPS /etc/environment, never in repo)*

### From the VPS (works — no proxy blocking):
```bash
# Run data collector:
python3 /root/prebuild-autopilot/audit/ghl_audit_collector.py \
  --api-key "pit-335bf0ee-b8e4-4eaa-be07-997052ceb717" \
  --location-id "YOUR_LOCATION_ID"

# Launch Claude Code with GHL MCP:
cd /root/prebuild-autopilot && claude
```

### First-time VPS setup:
```bash
# Cursor runs this — see CURSOR_VPS_PROMPT.md for the full prompt
curl -fsSL https://raw.githubusercontent.com/Jerald-centriweb/The-builder-pivet-GHL/claude/review-autopilot-architecture-ZT2lu/vps/setup_vps.sh \
  | GHL_LOCATION_ID="xxx" ANTHROPIC_API_KEY="sk-ant-xxx" bash
```

> Note: The GitHub/cloud Claude Code environment blocks outbound HTTPS to GHL. All live GHL work must run from the VPS.

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
