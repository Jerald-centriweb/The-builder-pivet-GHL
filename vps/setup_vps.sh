#!/bin/bash
# =============================================================
# PreBuild Autopilot — VPS Full Setup Script
# Ubuntu 24.04 / Hostinger KVM
# Run as root on the VPS
# =============================================================
set -e

# Colours for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
info() { echo -e "${YELLOW}[..] $1${NC}"; }
fail() { echo -e "${RED}[!!] $1${NC}"; exit 1; }

echo ""
echo "============================================================"
echo "  PreBuild Autopilot — VPS Setup"
echo "  Ubuntu 24.04 / Hostinger"
echo "============================================================"
echo ""

# --- Require Location ID argument ---
if [ -z "$GHL_LOCATION_ID" ]; then
    echo "Usage: GHL_LOCATION_ID=your_location_id bash setup_vps.sh"
    echo ""
    echo "Find your Location ID: GHL → Settings → Company → Locations"
    exit 1
fi

GHL_API_KEY="pit-335bf0ee-b8e4-4eaa-be07-997052ceb717"
REPO_URL="https://github.com/Jerald-centriweb/The-builder-pivet-GHL.git"
REPO_BRANCH="claude/review-autopilot-architecture-ZT2lu"
REPO_DIR="/root/prebuild-autopilot"
MCP_DIR="/root/.claude/mcp/ghl-mcp"

# =============================================================
# STEP 1 — System update
# =============================================================
info "Step 1/9 — Updating system packages..."
apt-get update -qq && apt-get upgrade -y -qq
apt-get install -y -qq git curl python3 python3-pip ufw
ok "System updated"

# =============================================================
# STEP 2 — Node.js 20
# =============================================================
info "Step 2/9 — Installing Node.js 20..."
if ! command -v node &>/dev/null || [ "$(node -e 'process.exit(parseInt(process.versions.node) < 18 ? 1 : 0)' 2>/dev/null; echo $?)" = "1" ]; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - -qq
    apt-get install -y -qq nodejs
fi
ok "Node.js $(node --version) installed"

# =============================================================
# STEP 3 — Claude Code
# =============================================================
info "Step 3/9 — Installing Claude Code..."
npm install -g @anthropic-ai/claude-code --quiet 2>/dev/null || \
npm install -g @anthropic-ai/claude-code
ok "Claude Code $(claude --version 2>/dev/null || echo 'installed') ready"

# =============================================================
# STEP 4 — Clone repo
# =============================================================
info "Step 4/9 — Cloning project repo..."
if [ -d "$REPO_DIR" ]; then
    info "Repo exists — pulling latest..."
    git -C "$REPO_DIR" fetch origin
    git -C "$REPO_DIR" checkout "$REPO_BRANCH"
    git -C "$REPO_DIR" pull origin "$REPO_BRANCH"
else
    git clone "$REPO_URL" "$REPO_DIR"
    git -C "$REPO_DIR" checkout "$REPO_BRANCH"
fi
ok "Repo ready at $REPO_DIR"

# =============================================================
# STEP 5 — GHL MCP Server
# =============================================================
info "Step 5/9 — Installing GHL MCP server..."
mkdir -p "$MCP_DIR"
if [ ! -d "$MCP_DIR/.git" ]; then
    git clone https://github.com/mastanley13/GoHighLevel-MCP.git "$MCP_DIR"
else
    git -C "$MCP_DIR" pull origin main 2>/dev/null || true
fi

cd "$MCP_DIR"
npm install --quiet
npm run build
ok "GHL MCP server built"

# =============================================================
# STEP 6 — MCP environment config
# =============================================================
info "Step 6/9 — Configuring MCP credentials..."
cat > "$MCP_DIR/.env" <<ENVEOF
GHL_API_KEY=$GHL_API_KEY
GHL_LOCATION_ID=$GHL_LOCATION_ID
GHL_BASE_URL=https://services.leadconnectorhq.com
NODE_ENV=production
ENVEOF
ok "MCP .env written"

# =============================================================
# STEP 7 — Claude Code settings (auto-load MCP on start)
# =============================================================
info "Step 7/9 — Configuring Claude Code settings..."
mkdir -p /root/.claude
cat > /root/.claude/settings.json <<SETTINGSEOF
{
  "mcpServers": {
    "ghl": {
      "command": "node",
      "args": ["$MCP_DIR/dist/index.js"],
      "env": {
        "GHL_API_KEY": "$GHL_API_KEY",
        "GHL_LOCATION_ID": "$GHL_LOCATION_ID",
        "GHL_BASE_URL": "https://services.leadconnectorhq.com",
        "NODE_ENV": "production"
      }
    }
  }
}
SETTINGSEOF
ok "Claude Code settings written"

# =============================================================
# STEP 8 — Test GHL API connection
# =============================================================
info "Step 8/9 — Testing GHL API connection..."
cd "$REPO_DIR"
TEST_OUTPUT=$(python3 audit/ghl_audit_collector.py \
    --api-key "$GHL_API_KEY" \
    --location-id "$GHL_LOCATION_ID" \
    --output /tmp/ghl_test.json 2>&1 | tail -20)

if echo "$TEST_OUTPUT" | grep -q "ERROR timeout"; then
    echo -e "${RED}[!!] GHL API connection failed — check API key and Location ID${NC}"
    echo "$TEST_OUTPUT"
else
    ok "GHL API connected — live account data pulled"
    echo "$TEST_OUTPUT"
fi

# =============================================================
# STEP 9 — Firewall
# =============================================================
info "Step 9/9 — Configuring firewall..."
ufw --force reset > /dev/null
ufw default deny incoming > /dev/null
ufw default allow outgoing > /dev/null
ufw allow OpenSSH > /dev/null
ufw --force enable > /dev/null
ok "Firewall enabled — SSH only inbound"

# =============================================================
# DONE
# =============================================================
echo ""
echo "============================================================"
echo -e "${GREEN}  Setup complete.${NC}"
echo "============================================================"
echo ""
echo "  Project directory : $REPO_DIR"
echo "  GHL MCP server    : $MCP_DIR"
echo "  Claude settings   : /root/.claude/settings.json"
echo ""
echo "  To start working:"
echo "    cd $REPO_DIR && claude"
echo ""
echo "  Claude Code will auto-read CLAUDE.md and have full"
echo "  project context + live GHL account access via MCP."
echo ""

# If GHL test data was pulled, copy it to repo for analysis
if [ -f /tmp/ghl_test.json ] && ! grep -q '"error"' /tmp/ghl_test.json; then
    cp /tmp/ghl_test.json "$REPO_DIR/audit/audit_data.json"
    echo "  Live GHL data saved to audit/audit_data.json"
    echo "  Open Claude Code and say: 'Analyse audit/audit_data.json"
    echo "  against the verification checklist'"
    echo ""
fi
