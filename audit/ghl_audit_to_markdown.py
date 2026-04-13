#!/usr/bin/env python3
"""
Convert audit_data.json (from ghl_audit_collector.py) into a thorough Markdown
report for Claude / humans. Includes every section and deep-detail blocks when
present. Active vs inactive is reported as data only, not prioritised.
"""

import argparse
import json
import sys


def _short_json(obj, max_len=12000):
    s = json.dumps(obj, indent=2, default=str)
    if len(s) > max_len:
        return s[: max_len - 80] + "\n\n… [truncated for size; see full audit_data.json] …\n"
    return s


def _error_block(d):
    if isinstance(d, dict) and "error" in d:
        return f"**API error:** `{d.get('error')}` — {str(d.get('message', ''))[:500]}"
    return None


def _render_workflow_detail(wf_id, data):
    lines = [f"#### Workflow `{wf_id}`"]
    err = _error_block(data)
    if err:
        lines.append(err)
        return "\n".join(lines)
    if not isinstance(data, dict):
        lines.append(_short_json(data, 8000))
        return "\n".join(lines)
    # Common GHL shapes (varies by API version)
    for key in ("workflow", "data", "result"):
        if key in data and isinstance(data[key], dict):
            inner = data[key]
            lines.append("```json")
            lines.append(_short_json(inner, 10000))
            lines.append("```")
            return "\n".join(lines)
    lines.append("```json")
    lines.append(_short_json(data, 10000))
    lines.append("```")
    return "\n".join(lines)


def _summarize_list_section(title, data, id_keys=("id",), name_keys=("name", "title")):
    lines = [f"## {title}", ""]
    err = _error_block(data)
    if err:
        lines.append(err)
        lines.append("")
        return "\n".join(lines)
    if isinstance(data, list):
        items = data
        wrapper = None
    elif isinstance(data, dict):
        items = None
        for k in ("workflows", "forms", "surveys", "calendars", "templates", "tags", "pipelines", "products", "blogs", "users", "customFields", "customValues", "campaigns", "funnels"):
            if k in data and isinstance(data[k], list):
                items = data[k]
                break
        if items is None:
            lines.append("*(No list array found in this section; raw JSON below.)*")
            lines.append("")
            lines.append("```json")
            lines.append(_short_json(data, 6000))
            lines.append("```")
            lines.append("")
            return "\n".join(lines)
    else:
        lines.append("```json")
        lines.append(_short_json(data, 4000))
        lines.append("```")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"**Count:** {len(items)}")
    lines.append("")
    lines.append("| # | Name / label | ID | Status / flags |")
    lines.append("|---|--------------|-----|------------------|")
    for i, it in enumerate(items, 1):
        if not isinstance(it, dict):
            lines.append(f"| {i} | — | — | `{it}` |")
            continue
        name = "—"
        for nk in name_keys:
            if it.get(nk):
                name = str(it[nk])[:120]
                break
        oid = "—"
        for ik in id_keys:
            if it.get(ik):
                oid = str(it[ik])
                break
        flags = []
        for fk in ("status", "isActive", "published", "state", "version", "type"):
            if fk in it and it[fk] is not None:
                flags.append(f"{fk}={it[fk]}")
        flag_s = ", ".join(flags) if flags else "—"
        lines.append(f"| {i} | {name} | `{oid}` | {flag_s} |")
    lines.append("")
    return "\n".join(lines)


def _section_generic(title, data):
    lines = [f"## {title}", ""]
    err = _error_block(data)
    if err:
        lines.append(err)
        lines.append("")
        return "\n".join(lines)
    lines.append("```json")
    lines.append(_short_json(data, 14000))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def build_markdown(audit, source_path):
    loc = audit.get("location_id", "")
    collected = audit.get("collected_at", "")
    sections = audit.get("sections", {})
    deep = sections.get("deep", {})

    out = []
    out.append("# GHL sub-account — thorough capture (from API audit)")
    out.append("")
    out.append(f"> **Source file:** `{source_path}`  ")
    out.append(f"> **Collected at (UTC):** {collected}  ")
    out.append(f"> **Location ID:** `{loc}`  ")
    if audit.get("collector_version") is None:
        out.append(
            "> **Note:** Source JSON predates collector v2. Re-run `audit/ghl_audit_collector.py` "
            "with `--deep` (and optional `--markdown`) to include extra sections and per-ID workflow/form/survey payloads.  "
        )
    out.append("")
    out.append(
        "This document lists **everything the collector returned**: assets that exist in the "
        "sub-account, configuration fields (including `isActive`, `status`, draft/published), "
        "and API errors where an endpoint was tried but failed. **Activation state is factual "
        "metadata only** — not a judgement on build completeness."
    )
    out.append("")
    out.append("---")
    out.append("")

    # Location first
    if "location" in sections:
        out.append(_section_generic("Location (full payload)", sections["location"]))
    if "pipelines" in sections:
        pl = sections["pipelines"]
        out.append(_summarize_list_section("Pipelines (summary table)", pl))
        out.append("### Pipelines — stages and full JSON")
        out.append("")
        out.append(_section_generic("Pipelines (complete payload)", pl))

    if "workflows" in sections:
        out.append(_summarize_list_section("Workflows (list)", sections["workflows"]))

    if deep.get("workflows_by_id"):
        out.append("## Workflows — per-ID detail (deep fetch)")
        out.append("")
        out.append(
            "Each block is the raw API response for that workflow ID. "
            "If steps/triggers appear here, Claude can reason about logic; if empty or error-only, "
            "the public API may not expose builder internals for that token/version."
        )
        out.append("")
        for wf_id in sorted(deep["workflows_by_id"].keys(), key=str):
            out.append(_render_workflow_detail(wf_id, deep["workflows_by_id"][wf_id]))
            out.append("")

    if "forms" in sections:
        out.append(_summarize_list_section("Forms (list)", sections["forms"]))
    if deep.get("forms_by_id"):
        out.append("## Forms — per-ID detail (deep fetch)")
        out.append("")
        for fid in sorted(deep["forms_by_id"].keys(), key=str):
            out.append(f"### Form `{fid}`")
            err = _error_block(deep["forms_by_id"][fid])
            if err:
                out.append(err)
            else:
                out.append("```json")
                out.append(_short_json(deep["forms_by_id"][fid], 12000))
                out.append("```")
            out.append("")

    if "surveys" in sections:
        out.append(_summarize_list_section("Surveys (list)", sections["surveys"]))
    if deep.get("surveys_by_id"):
        out.append("## Surveys — per-ID detail (deep fetch)")
        out.append("")
        for sid in sorted(deep["surveys_by_id"].keys(), key=str):
            out.append(f"### Survey `{sid}`")
            err = _error_block(deep["surveys_by_id"][sid])
            if err:
                out.append(err)
            else:
                out.append("```json")
                out.append(_short_json(deep["surveys_by_id"][sid], 12000))
                out.append("```")
            out.append("")

    if "calendars" in sections:
        out.append(_summarize_list_section("Calendars (list)", sections["calendars"]))
    if deep.get("calendars_by_id"):
        out.append("## Calendars — per-ID detail (deep fetch)")
        out.append("")
        for cid in sorted(deep["calendars_by_id"].keys(), key=str):
            out.append(f"### Calendar `{cid}`")
            err = _error_block(deep["calendars_by_id"][cid])
            if err:
                out.append(err)
            else:
                out.append("```json")
                out.append(_short_json(deep["calendars_by_id"][cid], 14000))
                out.append("```")
            out.append("")

    if deep.get("templates_by_id"):
        out.append("## Templates — per-ID detail (deep fetch)")
        out.append("")
        for tid in sorted(deep["templates_by_id"].keys(), key=str):
            out.append(f"### Template `{tid}`")
            err = _error_block(deep["templates_by_id"][tid])
            if err:
                out.append(err)
            else:
                out.append("```json")
                out.append(_short_json(deep["templates_by_id"][tid], 12000))
                out.append("```")
            out.append("")

    order_rest = [
        "custom_fields",
        "custom_values",
        "tags",
        "templates",
        "campaigns",
        "brand_boards",
        "funnels",
        "products",
        "blogs",
        "users",
        "calendar_groups",
        "custom_objects",
        "contacts",
        "payments",
        "forms_submissions",
        "surveys_submissions",
        "invoices",
        "estimates",
    ]
    for key in order_rest:
        if key not in sections:
            continue
        title = key.replace("_", " ").title()
        out.append(_section_generic(title, sections[key]))

    # Any sections not covered
    done = set(
        [
            "location",
            "pipelines",
            "workflows",
            "forms",
            "surveys",
            "calendars",
            "deep",
        ]
        + order_rest
    )
    for key, val in sorted(sections.items()):
        if key in done:
            continue
        if key.startswith("opportunities_"):
            out.append(_section_generic(f"Opportunities ({key})", val))
        else:
            out.append(_section_generic(key.replace("_", " ").title(), val))

    if "analysis" in audit:
        out.append("## Collector-side analysis")
        out.append("")
        out.append("```json")
        out.append(_short_json(audit["analysis"], 4000))
        out.append("```")
        out.append("")

    out.append("---")
    out.append("")
    out.append("*End of export. For full fidelity without truncation, use the JSON source file.*")
    out.append("")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="Audit JSON → thorough Markdown")
    parser.add_argument("input_json", help="Path to audit_data.json")
    parser.add_argument("-o", "--output", default="audit/GHL_THOROUGH_ACCOUNT_EXPORT.md", help="Output .md path")
    args = parser.parse_args()

    try:
        with open(args.input_json, "r", encoding="utf-8") as f:
            audit = json.load(f)
    except OSError as e:
        print(f"Cannot read {args.input_json}: {e}", file=sys.stderr)
        sys.exit(1)

    md = build_markdown(audit, args.input_json)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Wrote {args.output} ({len(md)} chars)")


if __name__ == "__main__":
    main()
