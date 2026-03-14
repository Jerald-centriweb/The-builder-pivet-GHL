#!/bin/bash
# =============================================================
# PreBuild Autopilot — VPS Full Setup Script
# Ubuntu 24.04 / Hostinger KVM — srv1420954.hstgr.cloud
# Run as root on the VPS
#
# Usage:
#   GHL_LOCATION_ID=xxx ANTHROPIC_API_KEY=xxx bash setup_vps.sh
# =============================================================
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ok()   { echo -e "${GREEN}  [✓]${NC} $1"; }
info() { echo -e "${YELLOW}  [→]${NC} $1"; }
fail() { echo -e "${RED}  [✗] $1${NC}"; exit 1; }
head() { echo -e "\n${CYAN}━━━ $1 ━━━${NC}"; }

echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${CYAN}  PreBuild Autopilot — Full VPS Setup${NC}"
echo -e "${CYAN}  Hostinger KVM / Ubuntu 24.04${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""

# --- Validate required args ---
if [ -z "$GHL_LOCATION_ID" ]; then
    fail "GHL_LOCATION_ID is required.\nUsage: GHL_LOCATION_ID=xxx ANTHROPIC_API_KEY=xxx bash setup_vps.sh\nFind Location ID: GHL → Settings → Company → Locations"
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
    fail "ANTHROPIC_API_KEY is required for Claude Code to authenticate.\nGet yours at: https://console.anthropic.com → API Keys\nUsage: GHL_LOCATION_ID=xxx ANTHROPIC_API_KEY=sk-ant-xxx bash setup_vps.sh"
fi

# Validate Anthropic key format
if [[ ! "$ANTHROPIC_API_KEY" == sk-ant-* ]]; then
    fail "ANTHROPIC_API_KEY looks wrong — it should start with 'sk-ant-'\nGet yours at: https://console.anthropic.com → API Keys"
fi

GHL_API_KEY="pit-335bf0ee-b8e4-4eaa-be07-997052ceb717"
REPO_URL="https://github.com/Jerald-centriweb/The-builder-pivet-GHL.git"
REPO_BRANCH="claude/review-autopilot-architecture-ZT2lu"
REPO_DIR="/root/prebuild-autopilot"
MCP_DIR="/root/.claude/mcp/ghl-mcp"
CLAUDE_DIR="/root/.claude"

echo "  GHL Location ID : ${GHL_LOCATION_ID:0:8}..."
echo "  Anthropic Key   : ${ANTHROPIC_API_KEY:0:14}..."
echo "  GHL API Key     : ${GHL_API_KEY:0:14}..."
echo ""

# =============================================================
# STEP 1 — System update
# =============================================================
head "Step 1/10 — System update"
info "Updating packages..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get upgrade -y -qq
apt-get install -y -qq git curl python3 python3-pip ufw jq
ok "System packages updated"

# =============================================================
# STEP 2 — Node.js 20
# =============================================================
head "Step 2/10 — Node.js 20"
if node --version 2>/dev/null | grep -q "v2[0-9]"; then
    ok "Node.js $(node --version) already installed"
else
    info "Installing Node.js 20..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - >/dev/null 2>&1
    apt-get install -y -qq nodejs
    ok "Node.js $(node --version) installed"
fi

# =============================================================
# STEP 3 — Claude Code CLI
# =============================================================
head "Step 3/10 — Claude Code CLI"
info "Installing @anthropic-ai/claude-code..."
npm install -g @anthropic-ai/claude-code 2>/dev/null || npm install -g @anthropic-ai/claude-code
ok "Claude Code installed"

# =============================================================
# STEP 4 — Anthropic API key (persisted for all sessions)
# =============================================================
head "Step 4/10 — Anthropic API key"
info "Writing API key to shell environment..."
mkdir -p "$CLAUDE_DIR"

# Write to /etc/environment so it persists across reboots and all sessions
if grep -q "ANTHROPIC_API_KEY" /etc/environment 2>/dev/null; then
    sed -i "s|ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY|" /etc/environment
else
    echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" >> /etc/environment
fi

# Also write to root's .bashrc and .profile for interactive sessions
for RC_FILE in /root/.bashrc /root/.profile; do
    if grep -q "ANTHROPIC_API_KEY" "$RC_FILE" 2>/dev/null; then
        sed -i "s|export ANTHROPIC_API_KEY=.*|export ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY|" "$RC_FILE"
    else
        echo "export ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" >> "$RC_FILE"
    fi
done

# Load it for this session
export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
ok "Anthropic API key configured (persists across reboots)"

# =============================================================
# STEP 5 — Clone project repo
# =============================================================
head "Step 5/10 — Project repo"
if [ -d "$REPO_DIR/.git" ]; then
    info "Repo exists — pulling latest..."
    git -C "$REPO_DIR" fetch origin -q
    git -C "$REPO_DIR" checkout "$REPO_BRANCH" -q
    git -C "$REPO_DIR" pull origin "$REPO_BRANCH" -q
    ok "Repo updated to latest"
else
    info "Cloning repo..."
    git clone -q "$REPO_URL" "$REPO_DIR"
    git -C "$REPO_DIR" checkout -q "$REPO_BRANCH"
    ok "Repo cloned to $REPO_DIR"
fi

# =============================================================
# STEP 6 — GHL MCP Server
# =============================================================
head "Step 6/10 — GoHighLevel MCP Server"
if [ -d "$MCP_DIR/.git" ]; then
    info "MCP repo exists — pulling latest..."
    git -C "$MCP_DIR" pull origin main -q 2>/dev/null || true
else
    info "Cloning GHL MCP server..."
    git clone -q https://github.com/mastanley13/GoHighLevel-MCP.git "$MCP_DIR"
fi

info "Installing MCP dependencies..."
cd "$MCP_DIR"
npm install --silent
info "Building MCP server..."
npm run build
ok "GHL MCP server built at $MCP_DIR"

# =============================================================
# STEP 7 — MCP credentials
# =============================================================
head "Step 7/10 — MCP credentials"
cat > "$MCP_DIR/.env" <<ENVEOF
GHL_API_KEY=$GHL_API_KEY
GHL_LOCATION_ID=$GHL_LOCATION_ID
GHL_BASE_URL=https://services.leadconnectorhq.com
NODE_ENV=production
ENVEOF
ok "MCP .env written"

# =============================================================
# STEP 8 — Claude Code settings (MCP auto-loads on start)
# =============================================================
head "Step 8/10 — Claude Code settings"
cat > "$CLAUDE_DIR/settings.json" <<SETTINGSEOF
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
ok "Claude Code settings written — GHL MCP will load automatically"

# =============================================================
# STEP 9 — Test GHL API connection
# =============================================================
head "Step 9/10 — GHL API connection test"
info "Calling live GHL account..."
cd "$REPO_DIR"

python3 audit/ghl_audit_collector.py \
    --api-key "$GHL_API_KEY" \
    --location-id "$GHL_LOCATION_ID" \
    --output /tmp/ghl_test.json 2>&1

if [ -f /tmp/ghl_test.json ]; then
    ERRORS=$(python3 -c "import json; d=json.load(open('/tmp/ghl_test.json')); errs=[k for k,v in d.get('sections',{}).items() if isinstance(v,dict) and 'error' in v]; print(len(errs))" 2>/dev/null || echo "0")
    if [ "$ERRORS" = "0" ]; then
        ok "GHL API connected — live account data pulled successfully"
        cp /tmp/ghl_test.json "$REPO_DIR/audit/audit_data.json"
        ok "Data saved to audit/audit_data.json"
    else
        echo -e "${RED}  [✗] GHL API returned $ERRORS errors — check Location ID${NC}"
        echo "      Sections with errors:"
        python3 -c "
import json
d = json.load(open('/tmp/ghl_test.json'))
for k,v in d.get('sections',{}).items():
    if isinstance(v,dict) and 'error' in v:
        print(f'        {k}: {v.get(\"error\")} — {str(v.get(\"message\",\"\"))[:60]}')
" 2>/dev/null || true
    fi
else
    echo -e "${RED}  [✗] GHL API test failed — no output file created${NC}"
fi

# =============================================================
# STEP 10 — Firewall
# =============================================================
head "Step 10/10 — Firewall"
ufw --force reset >/dev/null 2>&1
ufw default deny incoming >/dev/null
ufw default allow outgoing >/dev/null
ufw allow OpenSSH >/dev/null
ufw --force enable >/dev/null
ok "Firewall active — inbound: SSH only | outbound: open"

# =============================================================
# DONE
# =============================================================
echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${GREEN}  Setup complete.${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""
echo "  VPS               : root@76.13.212.238"
echo "  Project           : $REPO_DIR"
echo "  GHL MCP           : $MCP_DIR"
echo "  Claude settings   : $CLAUDE_DIR/settings.json"
echo "  Anthropic key     : configured in /etc/environment"
echo ""
echo -e "${YELLOW}  Next step — start Claude Code:${NC}"
echo ""
echo "    cd $REPO_DIR && claude"
echo ""
echo "  Claude will auto-read CLAUDE.md and know the full project."
echo "  GHL MCP will load automatically — live account access ready."
echo ""
if [ -f "$REPO_DIR/audit/audit_data.json" ]; then
    echo -e "${GREEN}  Live GHL data was pulled.${NC}"
    echo "  First thing to ask Claude:"
    echo "    'Analyse audit/audit_data.json against the verification checklist'"
    echo "    'Tell me what's built, what's missing, and what needs fixing'"
    echo ""
fi
echo -e "${CYAN}============================================================${NC}"
echo ""
