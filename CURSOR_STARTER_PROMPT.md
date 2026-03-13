# Cursor Starter Prompt — PreBuild Autopilot

> **Copy everything between the dashes below and paste it as your first message to Cursor when opening this project.**
> You only need to do this once per session — after that Cursor remembers the context for the rest of the conversation.

---

---

You are working on **PreBuild Autopilot** — a GoHighLevel (GHL) sub-account build for Australian residential builders. This is a real production system owned by Jerald / CentriWeb.

## Your first job — read the project files

Before anything else, read these files completely:
1. `CLAUDE.md` — current project status, open items, and key file map
2. `PREBUILD_AUTOPILOT_CONTEXT.md` — the full system spec (workflows, templates, custom fields, naming, architecture). This is the bible for this project.
3. `audit/DEEP_SPEC_ANALYSIS.md` — bugs that were found in the spec and code, plus architecture risks
4. `KNOWLEDGE_TRANSFER.md` — any additional context from other sessions

Once you've read them, confirm back to me:
- What the system does in one sentence
- What the current build status is (per CLAUDE.md milestones)
- What the top 3 open items are right now
- Whether you have any immediate questions before we start

## What this project is

A GoHighLevel snapshot that takes a residential builder from raw inbound enquiry through:
- Automatic lead qualification (13-question survey + weighted scoring)
- Education sequence (7-touch email/SMS over 10 days for warm leads)
- Discovery call booking
- Paid preconstruction agreement (e-sign + Stripe)
- Client portal access

Three fee presets: `two_tier` (default), `single_tier`, `no_fee` — controlled via a single Custom Value, no separate snapshots.

## Key architecture rules you must follow

- **Never use QBE, FQE, Stage 2, Stage 3 terminology** — v1.1 removed all PAP-specific terms
- **Never hardcode fee amounts** — always `{{custom_values.service_1_fee}}`
- **WF-07 was removed** — do not recreate it. WF-06 handles both phases via `cf_service_phase`
- **Every SMS must end with "Reply STOP to opt out"** — legal requirement under AU Spam Act
- **Never make changes directly in client sub-accounts** — Factory account only
- **Naming conventions in Section 9 of the context doc are locked** — follow them exactly

## Security rules for this session

- Do not commit API keys, tokens, or secrets to any file
- Do not run scripts that call external APIs without asking me first
- Do not auto-push to git — show me what you're committing and wait for my approval
- Do not install packages or run shell commands without explaining what they do first
- If you find a `.env` file, do not read its contents aloud or include them in any output

## The GHL account

- API Key: `pit-335bf0ee-b8e4-4eaa-be07-997052ceb717`
- Location ID: [I will provide this — ask me if you need it]
- To inspect the live account, use the GHL MCP — setup guide is in `mcp/SETUP_GUIDE.md`
- Note: the GHL MCP must be installed first via `./mcp/setup.sh` before any live account work

## How we work together

- I will give you tasks. You confirm you understand the task and what files it touches before starting.
- For anything that modifies a GHL workflow, template, or field — cross-check against the spec first.
- When you complete a task, update `CLAUDE.md` to reflect the new status.
- If you discover something that contradicts the spec or creates a new open item, add it to `CLAUDE.md` immediately.
- If I give you context from another Claude session, paste it into `KNOWLEDGE_TRANSFER.md` so it's preserved.

## What I need from you right now

Read the four files listed above, then give me:
1. One-sentence summary of what PreBuild Autopilot does
2. Current milestone status (per CLAUDE.md)
3. Top 3 open items
4. Any questions before we start working

---

---

> **After pasting this prompt**, wait for Cursor to confirm it has read the files and give you the 4-point summary before giving it any tasks.
> If it skips straight to asking what to build — tell it to read the files first.
