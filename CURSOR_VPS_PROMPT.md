# Cursor VPS Setup Prompt

> **How to use this:**
> 1. Fill in your GHL Location ID where marked below (the only blank you need to fill)
> 2. Copy everything between the === lines
> 3. Paste it as your first message to Cursor
> 4. Cursor will SSH into the VPS and run the full setup automatically

---

===========================================================================

I need you to SSH into my VPS and set up the PreBuild Autopilot project environment. Follow these instructions exactly, step by step.

## VPS Connection Details

- **Host:** 76.13.212.238
- **User:** root
- **Password:** [PASTE YOUR PASSWORD HERE — do not save this file after adding it]
- **OS:** Ubuntu 24.04

## GHL Location ID

- **Location ID:** [PASTE YOUR GHL LOCATION ID HERE — find it at GHL → Settings → Company → Locations]

## What to do

### Step 1 — Connect to the VPS
SSH into the server:
```
ssh root@76.13.212.238
```
Use the password above when prompted. Accept the host key fingerprint if asked.

### Step 2 — Run the setup script
Once connected, run this single command (replace YOUR_LOCATION_ID with the Location ID above):
```bash
curl -fsSL https://raw.githubusercontent.com/Jerald-centriweb/The-builder-pivet-GHL/claude/review-autopilot-architecture-ZT2lu/vps/setup_vps.sh | GHL_LOCATION_ID=YOUR_LOCATION_ID bash
```

This script will automatically:
- Update Ubuntu packages
- Install Node.js 20
- Install Claude Code (`@anthropic-ai/claude-code`)
- Clone the project repo to `/root/prebuild-autopilot`
- Install and build the GoHighLevel MCP server
- Write the MCP config with the API key and Location ID
- Write Claude Code settings so MCP loads automatically
- Test the live GHL API connection
- Configure the firewall (SSH only, everything else blocked)

### Step 3 — Watch the output
Let the script run to completion. Report back to me:
- Whether Step 8 (GHL API test) succeeded or failed
- The final summary output
- Any errors that occurred

### Step 4 — If Step 8 (GHL API) failed
Tell me the exact error message and I will diagnose it.

### Step 5 — If everything succeeded
Run:
```bash
cd /root/prebuild-autopilot && claude
```
Then tell me what Claude Code says — it should read CLAUDE.md and give you a project summary.

## Rules for this session

- Do not print the SSH password in your responses
- Do not save the password anywhere on this machine
- Do not commit anything to git unless I explicitly ask
- Do not run any commands I haven't listed here without asking first
- If any step fails, stop and tell me what failed before continuing

===========================================================================

---

> **After filling in your password and Location ID:**
> - Copy from `===` to `===`
> - Paste into Cursor
> - Delete the password from this file immediately after (or don't save the file)
>
> **The password and Location ID should never be committed to git.**
> They go into Cursor's chat only — not into any file in this repo.
