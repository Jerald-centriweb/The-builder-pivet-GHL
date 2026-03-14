# Terminal Setup Complete — PreBuild Autopilot

Setup has been run successfully. Here's what was done and what you need to do next.

---

## What Was Installed

| Component | Location | Status |
|-----------|----------|--------|
| GHL MCP Server | `~/.claude/mcp/ghl-mcp/` | ✅ Cloned, built |
| Claude Code settings | `~/.claude/settings.json` | ✅ Created |
| Cursor MCP config | `~/.cursor/mcp.json` | ✅ GHL server added |

---

## Required: Add Your GHL Location ID

The GHL API needs your **Location ID** to connect. Without it, the MCP will not work.

### 1. Find your Location ID

1. Log into GoHighLevel
2. Go to **Settings → Company → Locations**
3. Copy the ID string (looks like `abc123XYZ...`)

### 2. Update it in three places

Replace `REPLACE_WITH_YOUR_LOCATION_ID` with your actual ID in:

| File | What to edit |
|------|--------------|
| `~/.claude/mcp/ghl-mcp/.env` | `GHL_LOCATION_ID=your_actual_id` |
| `~/.claude/settings.json` | `"GHL_LOCATION_ID": "your_actual_id"` |
| `~/.cursor/mcp.json` | `"GHL_LOCATION_ID": "your_actual_id"` |

### Quick edit (replace YOUR_ID with your real ID):

```bash
# Edit all three at once (macOS):
LOCATION_ID="YOUR_ID"
sed -i '' "s/REPLACE_WITH_YOUR_LOCATION_ID/$LOCATION_ID/g" ~/.claude/mcp/ghl-mcp/.env
sed -i '' "s/REPLACE_WITH_YOUR_LOCATION_ID/$LOCATION_ID/g" ~/.claude/settings.json
sed -i '' "s/REPLACE_WITH_YOUR_LOCATION_ID/$LOCATION_ID/g" ~/.cursor/mcp.json
```

---

## Using the Setup

### In Cursor (this IDE)

1. **Restart Cursor** after adding your Location ID (or reload the window: Cmd+Shift+P → "Developer: Reload Window")
2. The GHL MCP tools will appear when you use the AI chat
3. Try: *"List my GHL workflows"* to verify the connection

### In Terminal (Claude Code CLI)

Claude Code is **not installed** yet. To use it:

```bash
npm install -g @anthropic-ai/claude-code
```

Then:

```bash
cd "/Users/jeraldimmanuel/Documents/Cursor projects/The-builder-pivet-GHL"
claude
```

Claude Code will read `CLAUDE.md` and have GHL MCP access (once Location ID is set).

### Run the GHL Audit Collector

To pull live data from your GHL account into `audit/audit_data.json`:

```bash
cd "/Users/jeraldimmanuel/Documents/Cursor projects/The-builder-pivet-GHL"
python3 audit/ghl_audit_collector.py \
  --api-key "pit-335bf0ee-b8e4-4eaa-be07-997052ceb717" \
  --location-id "YOUR_LOCATION_ID"
```

---

## VPS Setup (Optional)

If you want to run everything on your remote server (76.13.212.238), use `CURSOR_VPS_PROMPT.md`. Fill in your credentials and follow the steps there. The VPS setup is separate from this local setup.

---

## Verify Everything Works

1. Add your Location ID (see above)
2. Restart Cursor
3. In Cursor chat, ask: *"List my GHL workflows"*
4. If you see workflow names, the setup is working

---

*Generated after running `mcp/setup.sh` — March 2026*
