#!/bin/bash
# GHL MCP Server Setup — PreBuild Autopilot
# Installs the GoHighLevel MCP server so Claude Code (CLI) can talk to your GHL account.
#
# Usage:
#   chmod +x mcp/setup.sh
#   ./mcp/setup.sh

set -e

echo "=============================================="
echo "  GoHighLevel MCP Server Setup"
echo "=============================================="
echo ""

# --- Check dependencies ---
if ! command -v node &>/dev/null; then
    echo "ERROR: Node.js is required. Install from https://nodejs.org (v18+)"
    exit 1
fi

NODE_VER=$(node -e "process.exit(parseInt(process.versions.node) < 18 ? 1 : 0)" 2>/dev/null && echo "ok" || echo "old")
if [ "$NODE_VER" = "old" ]; then
    echo "ERROR: Node.js v18+ required. Current: $(node --version)"
    exit 1
fi

if ! command -v git &>/dev/null; then
    echo "ERROR: git is required"
    exit 1
fi

echo "[1/5] Cloning GoHighLevel MCP server..."
MCP_DIR="$HOME/.claude/mcp/ghl-mcp"
if [ -d "$MCP_DIR" ]; then
    echo "  Already cloned — pulling latest..."
    git -C "$MCP_DIR" pull origin main
else
    git clone https://github.com/mastanley13/GoHighLevel-MCP.git "$MCP_DIR"
fi

echo ""
echo "[2/5] Installing dependencies..."
cd "$MCP_DIR"
npm install

echo ""
echo "[3/5] Building TypeScript..."
npm run build

echo ""
echo "[4/5] Creating .env file..."
ENV_FILE="$MCP_DIR/.env"
if [ -f "$ENV_FILE" ]; then
    echo "  .env already exists — skipping (edit manually if needed)"
else
    cat > "$ENV_FILE" <<'ENVEOF'
GHL_API_KEY=pit-335bf0ee-b8e4-4eaa-be07-997052ceb717
GHL_LOCATION_ID=REPLACE_WITH_YOUR_LOCATION_ID
GHL_BASE_URL=https://services.leadconnectorhq.com
NODE_ENV=production
ENVEOF
    echo "  Created $ENV_FILE"
    echo ""
    echo "  *** ACTION REQUIRED ***"
    echo "  Edit $ENV_FILE and replace REPLACE_WITH_YOUR_LOCATION_ID"
    echo "  Find it in: GHL → Settings → Company → Locations → copy the ID string"
    echo ""
fi

echo "[5/5] Updating Claude Code MCP config..."
CLAUDE_SETTINGS="$HOME/.claude/settings.json"
GHL_MCP_ENTRY=$(cat <<JSONEOF
{
  "command": "node",
  "args": ["$MCP_DIR/dist/index.js"],
  "env": {
    "GHL_API_KEY": "pit-335bf0ee-b8e4-4eaa-be07-997052ceb717",
    "GHL_LOCATION_ID": "REPLACE_WITH_YOUR_LOCATION_ID",
    "GHL_BASE_URL": "https://services.leadconnectorhq.com",
    "NODE_ENV": "production"
  }
}
JSONEOF
)

if [ -f "$CLAUDE_SETTINGS" ]; then
    echo ""
    echo "  Claude settings file exists at $CLAUDE_SETTINGS"
    echo "  Manually add the following under \"mcpServers\":"
    echo ""
    echo "    \"ghl\": $GHL_MCP_ENTRY"
    echo ""
    echo "  Then replace REPLACE_WITH_YOUR_LOCATION_ID with your actual Location ID."
else
    mkdir -p "$HOME/.claude"
    cat > "$CLAUDE_SETTINGS" <<SETTINGSEOF
{
  "mcpServers": {
    "ghl": $GHL_MCP_ENTRY
  }
}
SETTINGSEOF
    echo "  Created $CLAUDE_SETTINGS"
fi

echo ""
echo "=============================================="
echo "  Setup complete."
echo "=============================================="
echo ""
echo "NEXT STEPS:"
echo "  1. Find your GHL Location ID:"
echo "     GHL → Settings → Company → Locations → copy the ID"
echo ""
echo "  2. Update the Location ID in:"
echo "     $MCP_DIR/.env"
echo "     $CLAUDE_SETTINGS  (under mcpServers.ghl.env.GHL_LOCATION_ID)"
echo ""
echo "  3. Restart Claude Code:"
echo "     claude  (in terminal)"
echo ""
echo "  4. Verify MCP is connected:"
echo "     In Claude, ask: 'List my GHL workflows'"
echo "     If it works, you'll see your workflow names."
echo ""
