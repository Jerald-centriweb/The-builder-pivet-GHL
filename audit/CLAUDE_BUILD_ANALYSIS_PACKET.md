# Claude — Build analysis packet (new chat)

## Data provenance (read this first)

| File | Is it live sub-account data? |
|------|------------------------------|
| **`audit/audit_data.json`** | **Yes.** Produced only by calling the GHL API (`audit/ghl_audit_collector.py`). This is the ground truth for what exists in the location (plus each endpoint’s errors, e.g. 403/404). |
| **`audit/GHL_THOROUGH_ACCOUNT_EXPORT.md`** | **Yes — but only a rendering of whatever is inside `audit_data.json` at generation time.** Same facts, human-readable. Regenerate after every collector run. |
| **`audit/GHL_PREBUILD_DEMO_FULL_CAPTURE.md`** | **Yes — merged** live MCP (`user-ghl-prebuild-demo`) + `audit_data.json` in one file. Regenerate with `python3 audit/build_full_capture_md.py` (update MCP blobs in script when re-capturing). |
| **`PREBUILD_AUTOPILOT_CONTEXT.md`** | **No.** It is the **design spec** (intent, copy, rules). It is not exported from GHL. |
| **This file (`CLAUDE_BUILD_ANALYSIS_PACKET.md`)** | **Mixed.** It routes you to the right artefacts and lists **priorities inferred** from last known live export + repo notes — not a substitute for `audit_data.json`. |

**If you only want execution reality from the real sub-account (nothing about “the idea”):** attach **`audit/audit_data.json`** *or* **`audit/GHL_THOROUGH_ACCOUNT_EXPORT.md`** — and **do not** attach `PREBUILD_AUTOPILOT_CONTEXT.md`. Re-run the collector first so the JSON is current:

```bash
python3 audit/ghl_audit_collector.py \
  --api-key "YOUR_PIT_KEY" \
  --location-id "YOUR_LOCATION_ID" \
  --output audit/audit_data.json \
  --deep \
  --markdown audit/GHL_THOROUGH_ACCOUNT_EXPORT.md
```

**Hard limit:** Anything GHL’s API does not return (e.g. some template bodies, some payment scopes, sometimes thin workflow internals) **cannot** appear in these files until GHL exposes it or you capture it manually in GHL UI. The collector stores those gaps as errors or empty fields — that is still “real” signal.

---

## Companion file (pick one — second attachment)

| Goal | Second file |
|------|-------------|
| **Execution only — what exists in GHL** | `audit/audit_data.json` **or** `audit/GHL_THOROUGH_ACCOUNT_EXPORT.md` (after command above) |
| **Compare live vs intended design** | `PREBUILD_AUTOPILOT_CONTEXT.md` **and** live JSON or thorough MD |
| **Narrated gap list** (live JSON vs spec, still partly interpretive) | `audit/SUBACCOUNT_BUILD_STATUS_FULL_AUDIT.md` |

**Default if you want “idea + execution”:** live export **+** `PREBUILD_AUTOPILOT_CONTEXT.md`.  
**Default if you want “only what’s in the account”:** **`audit_data.json`** (or thorough MD) **only** — no spec.

---

## What you’re building (context only — not from GHL)

*Skip this section if you attached only live JSON / thorough MD.*

PreBuild Autopilot is a GHL Factory snapshot for builder preconstruction funnels (enquiry → survey → scoring → nurture → call → proposal/pay → portal). Naming and rules live in `PREBUILD_AUTOPILOT_CONTEXT.md` if you need them.

---

## Remaining work (inferred — cross-check against `audit_data.json`)

These items are **not** re-fetched from GHL inside this packet; they were prioritised from the last exported audit + repo risk notes. After a fresh collector run, Claude should **verify each line against the new JSON**.

1. WF-03 wiring + external scorer vs live workflow payload (`--deep`).
2. Field keys / survey strings vs what appears on contacts and in deep form/survey payloads.
3. WF-08 presence (workflow list in JSON).
4. WF-11 naming vs list in JSON.
5. Custom values: keys in JSON; **values** may still need UI if API omits them.
6. Tags list in JSON vs what workflows expect.
7. `status` / `isActive` on workflows and calendars — as **facts** in JSON, not as “pass/fail”.
8. Template bodies if API returns empty.
9. Architecture / n8n / codebase — **outside** sub-account JSON; only if scope includes repo.

---

## “What can we do better?” (optional — not sub-account data)

Themes for product/process review; confirm in GHL only where relevant.

---

## Suggested prompts

**Execution-only:** “Using only the attached `audit_data.json`, inventory every asset, flag every `error` field, list every `status`/`isActive`/`draft` value, and note anything missing vs an empty Factory.”

**Live + spec:** “Compare attached live JSON to `PREBUILD_AUTOPILOT_CONTEXT.md` §4–§8; list mismatches.”

---

## Other paths (optional depth)

| Path | Nature |
|------|--------|
| `audit/wf03_scoring_engine.py` | Repo code, not GHL |
| `audit/DEEP_SPEC_ANALYSIS.md` | Repo analysis, not GHL |
| `CLAUDE.md` | Team notes, not GHL |

---

*Refresh `audit/audit_data.json` after any material GHL change; regenerate `GHL_THOROUGH_ACCOUNT_EXPORT.md` from that JSON.*
