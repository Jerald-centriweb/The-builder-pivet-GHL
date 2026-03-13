# GHL MCP Setup — Connect Claude to Your GHL Account

This gives Claude Code (in your terminal) direct live access to your GHL sub-account.
Once set up, Claude can inspect workflows, custom fields, contacts, surveys, pipelines, and templates — and make changes if you ask it to.

---

## What You Need

1. Your **GHL Location ID** — find it at: GHL → Settings → Company → Locations → copy the ID string (looks like `abc123XYZ...`)
2. **Node.js v18+** — check with `node --version`
3. **Git** — check with `git --version`

The API key is already in the setup script: `pit-335bf0ee-b8e4-4eaa-be07-997052ceb717`

---

## Setup (One Time)

```bash
# From the repo root:
chmod +x mcp/setup.sh
./mcp/setup.sh
```

The script will:
1. Clone the GoHighLevel MCP server to `~/.claude/mcp/ghl-mcp/`
2. Install Node.js dependencies
3. Build the TypeScript
4. Create the `.env` file with your API key
5. Print instructions to update `~/.claude/settings.json`

---

## After Running the Script

### Step 1 — Find your Location ID
In GHL: **Settings → Company → Locations** → copy the ID from the URL or the table.

### Step 2 — Add it in two places

**In `~/.claude/mcp/ghl-mcp/.env`:**
```
GHL_LOCATION_ID=your_actual_location_id_here
```

**In `~/.claude/settings.json`** (create if it doesn't exist):
```json
{
  "mcpServers": {
    "ghl": {
      "command": "node",
      "args": ["/Users/YOUR_USERNAME/.claude/mcp/ghl-mcp/dist/index.js"],
      "env": {
        "GHL_API_KEY": "pit-335bf0ee-b8e4-4eaa-be07-997052ceb717",
        "GHL_LOCATION_ID": "your_actual_location_id_here",
        "GHL_BASE_URL": "https://services.leadconnectorhq.com",
        "NODE_ENV": "production"
      }
    }
  }
}
```

Replace `YOUR_USERNAME` with your actual Mac/Linux username.

### Step 3 — Restart Claude Code
```bash
claude
```

### Step 4 — Verify it works
Ask Claude: *"List my GHL workflows"* — you should see your workflow names.

---

## What Claude Can Do Once Connected

| Task | Example prompt |
|------|---------------|
| List all workflows + status | "Show me all workflows and whether they're published or draft" |
| Check custom fields | "List all contact custom fields — do all the cf_ fields from the spec exist?" |
| Inspect a workflow | "Show me what WF-03 does — what triggers it and what actions does it have?" |
| Check survey | "Get SRV-Qualification and show me all questions and their field mappings" |
| Check pipeline stages | "List all pipeline stages in PreBuild Pipeline" |
| Check custom values | "Are all required custom values populated or do any have placeholder text?" |
| Test a contact | "Find the contact named Test Lead and show their custom field values" |
| Check templates | "List all SMS templates and show me their body text — do they all have STOP opt-out?" |
| Fix a field | "Update the google_review_link custom value to [URL]" |
| Run the live audit | "Check every item in audit/GHL_VERIFICATION_CHECKLIST.md against the live account" |

---

## If the MCP Doesn't Connect

1. Check Node.js version: `node --version` — must be v18+
2. Check the built file exists: `ls ~/.claude/mcp/ghl-mcp/dist/index.js`
3. Check settings.json path is correct for your OS (tilde `~` may need expanding on some systems)
4. Try running the server manually to see errors: `node ~/.claude/mcp/ghl-mcp/dist/index.js`

---

## Using with Cursor

If you're using Cursor IDE:
1. Open Cursor settings → Extensions → Claude Code (or similar MCP config panel)
2. Add the MCP server entry from `mcp/claude_mcp_config.json`
3. The GHL tools will be available in your Cursor chat panel

---

## Security Note

The API key in this repo is a **Private Integration key** scoped to the Factory sub-account only. It cannot access other GHL accounts. Do not commit additional API keys or Stripe credentials to this repo.
