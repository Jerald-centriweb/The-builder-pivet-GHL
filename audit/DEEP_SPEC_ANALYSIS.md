# PreBuild Autopilot — Deep Spec & Code Analysis

> **What this is:** A thorough review of everything in this repo — the full spec, the scoring engine code, the collector script, and the architecture decisions. Conducted against the spec only (live API access blocked by environment proxy). This is as deep as can be done without live account access.

---

## Network Access Situation (Why Live Inspection Still Fails)

The environment this runs in proxies all outbound HTTPS through a gateway that blocks calls to `services.leadconnectorhq.com`. This is not an API key problem — the key is valid. Every API call fails with `Tunnel connection failed: 403 Forbidden`.

**To get live account access, there are two options:**

### Option 1: Run the collector yourself (easiest)
```bash
# On your local machine (not this environment):
python3 audit/ghl_audit_collector.py \
  --api-key "pit-335bf0ee-b8e4-4eaa-be07-997052ceb717" \
  --output audit/audit_data.json
```
Then paste the JSON contents here and I can analyse it immediately.

### Option 2: Install the GoHighLevel MCP server
The repo you linked — `mastanley13/GoHighLevel-MCP` — exposes 269+ GHL tools as Claude Code tools. Once installed, I can query the live account directly through Claude's tool calls.

**Setup:**
```bash
npm install -g ghl-mcp-server  # or clone and build locally
```
Then add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "ghl": {
      "command": "ghl-mcp-server",
      "env": {
        "GHL_API_KEY": "pit-335bf0ee-b8e4-4eaa-be07-997052ceb717",
        "GHL_LOCATION_ID": "YOUR_LOCATION_ID_HERE",
        "GHL_BASE_URL": "https://services.leadconnectorhq.com"
      }
    }
  }
}
```
**You need your Location ID** — find it in GHL at Settings → Company → Locations.

---

## What's Actually Been Built (Based on Spec Analysis)

### Assets Confirmed in Spec

| Category | Items Specified | Status |
|----------|----------------|--------|
| Pipeline stages | 8 active + 2 non-active = 10 total | Spec complete |
| Custom fields | 22 fields on Contact record | Spec complete |
| Custom values | 14 required + ~16 configurable + 5 dynamic | Spec complete |
| Workflows | WF-01 through WF-12 (WF-07 removed) = 11 workflows | Spec complete |
| Email templates | 14 named templates | Spec complete (1 missing copy — see bugs) |
| SMS templates | 9 named templates | Spec complete |
| Survey | SRV-Qualification with 15 questions | Spec complete |
| Proposal | 1 template (PROP-Engagement-Agreement) | Spec complete |
| Portal pages | 5 pages | Spec complete |
| Calendar | CAL-Intro-Call | Spec complete |
| Forms | FRM-Lead-Intake, FRM-Pre-Call | Spec listed, not detailed |
| Scoring engine | wf03_scoring_engine.py | Code exists — see bugs |
| Collector script | ghl_audit_collector.py | Code exists — see bugs |

### Build Milestones Status (per Section 16)

| Milestone | Criteria | Likely Status |
|-----------|----------|---------------|
| M1 — Factory Baseline | Pipeline + Custom Values + naming locked | Likely done (spec is detailed) |
| M2 — Core Workflows | All 11 workflows pass QA | Unknown — WF-03 scoring unverified |
| M3 — Demo Ready | Demo account with seeded contacts | Unknown |
| M4 — Snapshot v1.1 Export | Fresh install works in <1 day | Unknown |
| M5 — Pilot Install | 1–3 builders installed | Unknown |

---

## Bugs Found

### Bug 1 — CRITICAL: MAX_RAW_SCORE is wrong in scoring engine

**File:** `audit/wf03_scoring_engine.py`, line 137

**Problem:**
```python
MAX_RAW_SCORE = 145  # Sum of all max points
```

The actual sum of max points across all 10 fields in `SCORING_RUBRIC` is **130**, not 145. The comment is wrong.

**Effect:** A perfect lead (max score on every question) scores `130/145 × 100 = **90/100**`, not 100/100. Every normalised score in the system is artificially deflated by ~10 points.

**Impact on thresholds:**
- To reach HOT (≥80), a lead needs raw score of at least ⌈80% × 145⌉ = **116**, but against 10 fields totalling 130 possible — that's 89% of available points.
- With the corrected MAX of 130: need raw score of ⌈80% × 130⌉ = **104**, i.e. 80% of available points.
- A lead who aces every single question scores 90 (hot), not 100. A lead who scores 95% of possible points scores only 86 — valid but misleading.

**Root cause:** The scoring rubric in Section 7 of the spec has Question 8 "Referred by" (worth up to 15 pts — Existing client=15, Professional=12, Other=8, Online ad=5). This field was given 0 pts in the custom field definition (Section 5 says `cf_how_heard` is "0 pts — informational only"), so the engine correctly omitted it from scoring. But MAX_RAW_SCORE was set as if it still counted, creating a phantom 15-point gap.

**Fix:** Set `MAX_RAW_SCORE = 130`. (See spec contradiction note below — owner must decide whether `cf_how_heard` scores or not.)

---

### Bug 2 — CRITICAL: Tag removal code is unreachable in scoring engine

**File:** `audit/wf03_scoring_engine.py`, lines 280–290

**Problem:**
```python
def update_ghl_contact(contact_id, score_result, api_key, location_id=None):
    ...
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
            return result          # <-- returns here
    except urllib.error.HTTPError as e:
        ...
        return None               # <-- or returns here

    # 2. Remove tags (separate API call)   <--- THIS NEVER EXECUTES
    for tag in score_result.get("tags_to_remove", []):
        ...
```

The tag removal block at step 2 comes after the `return result` statement. **`survey-pending` is never removed from contacts.** This means:
- WF-02 survey reminder sequence never stops based on the tag
- Contacts keep the `survey-pending` tag after completing the survey
- Duplicate survey reminder SMSes could fire

---

### Bug 3 — Collector script missing location ID on key endpoints

**File:** `audit/ghl_audit_collector.py`, lines 90, 148

**Problem:**
```python
audit["sections"]["custom_fields"] = api_get("/locations/custom-fields", api_key)
audit["sections"]["custom_values"] = api_get("/locations/custom-values", api_key)
```

The GHL v2 API endpoints for custom fields and custom values require the location ID in the path:
- `/locations/{locationId}/customFields`
- `/locations/{locationId}/customValues`

Without the location ID, these calls return 404 or 401. The collector script has no way to get the location ID (it's not passed as an argument, and there's no auto-discovery call).

**Fix:** Add `--location-id` argument to the collector script and use it in these calls.

---

### Bug 4 — Spec contradiction: `cf_how_heard` scoring

**Two sections of the spec directly contradict each other:**

Section 5 (Custom Fields):
> How Heard | `cf_how_heard` | Dropdown | **0 pts — informational only**

Section 7 (Scoring Rubric — Question 8):
> Referred by | Existing client=15, Professional=12, Other=8, Online ad=5

The scoring engine uses 0 pts (matches Section 5). MAX_RAW_SCORE was 145 (implied Section 7 was intended to score). **Owner decision required:** should referral source score up to 15 points? If yes, add it to the engine and keep MAX_RAW_SCORE=145. If no, set MAX_RAW_SCORE=130.

**Recommendation:** Score it. Referral source is one of the strongest lead quality signals. "Referred by existing client" is meaningfully different from "saw a Facebook ad." Make it 15 pts and correct MAX_RAW_SCORE to 145 with the field added.

---

### Bug 5 — ET-BOOK-Confirmation template is unspecified

**File:** `PREBUILD_AUTOPILOT_CONTEXT.md`, Section 10 (folder structure)

The folder structure lists `ET-BOOK-Confirmation` as an email template. WF-05 spec (Action 4) references it. But the template copy library in Section 8 never defines its content. There is no copy for this template anywhere in the spec.

**Impact:** If this template is blank or missing in GHL, discovery call booking confirmations either fail to send or send an empty email.

---

### Bug 6 — Dynamic Custom Values architecture is flawed for concurrent clients

**File:** `PREBUILD_AUTOPILOT_CONTEXT.md`, Section 6

The spec defines "Dynamic Custom Values" — fields like `current_service_fee` and `current_phase_label` — that workflows update per contact based on `cf_service_phase`. But **GHL Custom Values are location-level**, not contact-level. They're shared across all contacts in the account.

If a builder has two clients simultaneously — one in Phase 1 and one in Phase 2 — WF-06 would overwrite `current_service_fee` with Phase 2's value for client B, breaking the proposal email for client A (which would now reference the Phase 2 fee instead of Phase 1).

**Fix:** Replace dynamic Custom Values with **contact-level Custom Fields**:
- Create `cf_current_service_fee` (Number or Text) on the Contact record
- Create `cf_current_phase_label` (Text) on the Contact record
- WF-06 writes to these per-contact fields using "Update Contact Field" action
- Templates reference them as `{{contact.cf_current_service_fee}}`

This requires updating the proposal template and all affected workflow actions.

---

### Bug 7 — WF-10 stale reminder implementation is underdefined

**File:** `PREBUILD_AUTOPILOT_CONTEXT.md`, Section 7 (WF-10)

The spec says: `Trigger: 7 days with no pipeline stage update`. GHL has no native trigger for "time since last stage change."

**Typical implementation:** Time delay from stage entry in each active stage workflow → check if contact is still in that stage after 7 days → if yes, send the builder SMS. This means WF-10 logic would need to be embedded within each stage-specific workflow OR a separate recurring check workflow.

The spec treats this as a single workflow with a simple trigger that doesn't exist in GHL natively.

---

### Bug 8 — Scoring rubric Q12 appears to duplicate Q6

**File:** `PREBUILD_AUTOPILOT_CONTEXT.md`, Section 7 (Scoring Rubric)

| Q6 | Prior quotes | First contact=10, 1–2 builders=10, 3+ builders=5 |
| Q12 | Number of builders | 1–2=10, First=10, 3+=5 |

These have identical scoring weights. If they're genuinely different questions (e.g., "how many quotes have you received vs. how many builders are you currently talking to"), they should have different field keys. If they're the same question listed twice, one should be removed.

---

## Architecture Issues Worth Fixing

### Issue 1: No `location_id` in the scoring engine's GHL update call

`update_ghl_contact()` calls `PUT /contacts/{contact_id}` — this works with a Private Integration key. But `customFields` update via this endpoint needs the field keys to match exactly. Field keys should be confirmed against the live account.

### Issue 2: WF-01 fires on ALL contact creation

The spec says WF-01 trigger = "Contact created (any source: form submission, FB Lead Ad, manual entry)." This will also fire for contacts manually created by the builder for internal purposes (notes, tasks, etc.) and for contacts created by other systems. The workflow needs a filter condition, e.g., only fire if the contact has a specific tag (`new-enquiry`) or was created via specific form/source.

### Issue 3: Education sequence exit condition is vague

WF-04 exit condition: "Tag `call-booked` added OR pipeline moves past Nurture." In GHL, the tag condition works (exit on `call-booked`). But "pipeline moves past Nurture" isn't a GHL event — it needs to be either a stage-change trigger to stop the active workflow execution, or the sequence needs conditions at each step checking stage is still Nurture. GHL's native "Stop other automations" action is the right tool here.

### Issue 4: n8n outreach has 5 documented but unresolved bugs

Per Section 19:
1. Column name capitalisation mismatch (`Email 1 Body` vs `Email 1 body`)
2. Trailing spaces on column names
3. Two different Google Spreadsheet IDs with possible missing transfer workflow
4. Missing default column initialisation (Analysed, Replied, Opted Out, Bounced, W1-2)
5. W1-2 type mismatch (must be strings "1" and "2", not integers)

These are in the outreach system feeding leads INTO GHL. If these bugs cause silent failures (blank emails, missing status tracking), the lead pipeline is starved before it even reaches GHL.

---

## What's Actually Good (Genuinely Strong Design)

### 1. Custom Values alias layer
One of the best design decisions in the whole system. Internal asset names never change. Every builder-facing string — fees, service names, testimonials, calendar links — comes through Custom Values. This is what makes the snapshot model work cleanly. It's done correctly.

### 2. Single PROP-Engagement-Agreement with phase conditional
Using one template + `cf_service_phase` conditional logic instead of two templates is the right call. WF-06 merged with WF-07 is cleaner. Less maintenance surface.

### 3. Hard disqualifiers as overrides (not just low scores)
Budget under $300K and "No" to fee both trigger disqualification regardless of all other scores. This is correct — a great lead who refuses to pay a fee is a no, full stop. The engine implements this properly.

### 4. Tag schema is well-designed
Tags are namespaced consistently (`lead-hot`, `survey-pending`, `stage-won`). The `payment-manual` override tag is a smart escape hatch. The `review-requested` dedup tag prevents double-firing WF-12.

### 5. `fee_structure` preset system
Three presets (`two_tier`, `single_tier`, `no_fee`) handled via a single Custom Value + workflow branching, not separate snapshots. Clean. The preset comparison table in Section 11 is clear.

### 6. 5-day onboarding spec
Detailed enough to be executable. Hours are realistic (15 total). The separation of "pre-built in snapshot" vs "builder provides" is clear and correct.

### 7. Demo build spec with seeded contacts
The 5-minute demo script with AHA lines is sharp. The three seeded contacts (hot/warm/active) cover the scenarios that matter on a sales call.

---

## Improvements Worth Building Now

### Improvement 1: Fix the scoring engine (bugs 1 + 2 + referral scoring)

Priority: **Immediate before any real leads go through**

- Fix MAX_RAW_SCORE (130 or add referral scoring and keep 145)
- Fix unreachable tag removal code (move before the return)
- Decision on `cf_how_heard` scoring

### Improvement 2: Fix the dynamic Custom Values architecture (Bug 6)

Priority: **Before any builder has 2+ concurrent active clients**

Replace location-level custom values (`current_service_fee`, `current_phase_label`, etc.) with contact-level custom fields. This is a breaking change that requires updating WF-06 actions and the proposal template.

### Improvement 3: Define ET-BOOK-Confirmation template copy (Bug 5)

Priority: **Before QA Test 7 can pass**

Write and add the discovery call booking confirmation email to Section 8.

### Improvement 4: Add referral scoring to scoring engine

Priority: **High** — referral source is the single strongest predictor of conversion

```python
"referral_source": {
    "Existing client referral": 15,
    "Professional referral (architect, broker, etc.)": 12,
    "Other referral": 8,
    "Google Search": 5,
    "Facebook / Instagram": 5,
    "Builder Website": 5,
    "House & Land": 5,
}
```
This would bring MAX_RAW_SCORE to 145 (correct) and all scores to their intended values.

### Improvement 5: Resolve n8n bugs before scaling outreach

Priority: **Before sending more than 50 outreach sequences**

The silent blank email bug (column capitalisation mismatch) means leads could be getting contacted with empty emails. Fix in n8n before scaling.

### Improvement 6: Add `--location-id` to collector script

Priority: **Before running the collector**

Without this, custom fields and custom values calls will fail, even with network access.

---

## Spec Sections That Need Writing

| Missing | Where Referenced | Priority |
|---------|-----------------|----------|
| ET-BOOK-Confirmation copy | Section 10 folder structure, WF-05 Action 4 | High |
| FRM-Pre-Call spec | Section 10 folder structure | Medium |
| WF-13 Long-Term Nurture spec | Verification checklist | Low (not in v1.1) |
| Demo seeded contact data | Section 15 Demo Build Spec (partial) | High — needed for M3 |
| Partner/couple coordination design | Section 19 open questions | Medium |

---

## Priority Action Order

**Do these before demoing or going live with any builder:**

1. **Fix scoring engine** — MAX_RAW_SCORE bug means every score is wrong. Takes 20 minutes.
2. **Fix tag removal bug** — `survey-pending` never clears. Survey reminders fire indefinitely.
3. **Add location ID to collector script** — makes the data collection actually work.
4. **Decide on referral scoring** — resolves the spec contradiction and makes scores meaningful.
5. **Write ET-BOOK-Confirmation template** — QA test 7 can't pass without it.
6. **Resolve dynamic Custom Values architecture** — before more than 1 client is active.
7. **Fix n8n outreach bugs** — before scaling lead gen.

---

*Last updated: March 2026 — based on full spec review of PREBUILD_AUTOPILOT_CONTEXT.md v1.1 and code review of wf03_scoring_engine.py and ghl_audit_collector.py*
