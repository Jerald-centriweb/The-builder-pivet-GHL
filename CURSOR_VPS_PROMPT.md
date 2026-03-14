# Cursor VPS Setup Prompt

> **How to use this file:**
> 1. Fill in the three values marked **[YOU FILL THIS]** below
> 2. Copy the entire block between the `=====` lines
> 3. Paste it as your first message to Cursor
> 4. Cursor SSHes into the VPS and runs the full setup — do not save this file with real values in it

---

**What you need before starting:**
- Your **VPS root password** (you know this)
- Your **Anthropic API key** — get it from `console.anthropic.com` → API Keys → Create new key (starts with `sk-ant-`)
- Your **GHL Location ID** — in GHL go to Settings → Company → Locations, copy the ID string

---

==========================================================================

I need you to SSH into my VPS and fully set up the PreBuild Autopilot environment. Work through this exactly, step by step. Do not skip steps. Do not run extra commands I haven't listed.

## Credentials (use these, do not print them in your responses)

- **VPS:** `root@76.13.212.238` (Hostinger KVM, Ubuntu 24.04)
- **SSH Password:** [YOU FILL THIS — your VPS root password]
- **Anthropic API Key:** [YOU FILL THIS — from console.anthropic.com, starts with sk-ant-]
- **GHL Location ID:** [YOU FILL THIS — from GHL → Settings → Company → Locations]

## Step 1 — SSH into the VPS

```bash
ssh root@76.13.212.238
```

Accept the host fingerprint if prompted. Use the SSH password above.

## Step 2 — Run the one-command setup

Once connected, run this exactly (replace the two placeholder values with the real credentials above):

```bash
curl -fsSL https://raw.githubusercontent.com/Jerald-centriweb/The-builder-pivet-GHL/claude/review-autopilot-architecture-ZT2lu/vps/setup_vps.sh \
  | GHL_LOCATION_ID="REPLACE_WITH_LOCATION_ID" \
    ANTHROPIC_API_KEY="REPLACE_WITH_ANTHROPIC_KEY" \
    bash
```

**What this script does automatically:**
1. Updates Ubuntu packages
2. Installs Node.js 20
3. Installs Claude Code (`@anthropic-ai/claude-code`)
4. Writes the Anthropic API key to `/etc/environment` (persists across reboots)
5. Clones the project repo to `/root/prebuild-autopilot`
6. Clones and builds the GoHighLevel MCP server
7. Writes MCP credentials (GHL API key + Location ID)
8. Writes Claude Code settings so the GHL MCP loads automatically
9. Tests the live GHL API connection
10. Configures the UFW firewall (SSH inbound only)

## Step 3 — Report the results

Let the script run fully. Then tell me:
- Did Step 9 (GHL API test) show success or errors?
- Paste the final summary block from the output
- Paste any error lines if they appeared

## Step 4 — If the GHL API test failed

Tell me the exact error and I will fix it before continuing.

## Step 5 — If everything succeeded, launch Claude Code

```bash
cd /root/prebuild-autopilot && claude
```

Claude Code will auto-read `CLAUDE.md` and immediately know the full project context. The GHL MCP will load automatically, giving it live account access.

Tell me what Claude says when it starts — it should give a project summary.

## Step 6 — First task for Claude once it's running

Once Claude Code is running in the VPS terminal, paste this to it:

```
Read CLAUDE.md, then read audit/audit_data.json if it exists.

Tell me:
1. What is the live state of the GHL account — what's actually built vs what the spec requires?
2. Which workflows exist and are they published or draft?
3. Which custom fields exist?
4. What's the most urgent thing to fix?
```

Paste Claude's full response back to me.

## Rules for this session

- Do not print the SSH password, Anthropic key, or GHL Location ID in any response
- Do not save any credentials to files in the repo
- Do not commit or push to git without my explicit instruction
- Do not run any commands beyond what's listed here without asking first
- If any step fails, stop immediately and tell me what failed

==========================================================================

---

> **Security reminder:** Delete the credentials from this file immediately after copying to Cursor (or close without saving).
> None of these values should ever be committed to git.
