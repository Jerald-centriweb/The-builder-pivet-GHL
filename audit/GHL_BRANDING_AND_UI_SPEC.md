# GHL Branding & UI Spec — Complete Visual Capture

> **Purpose:** Enable any platform to fully understand the subaccount's visual identity (colors, fonts, logos, styling) without logging into GHL. The GHL API does **not** expose most of this — Brand Boards returned empty; forms/surveys/templates return 401 or empty bodies. This spec provides the schema and capture process.

---

## What the API Gives Us vs What We Need

| Asset | API Status | Capture Method |
|-------|------------|----------------|
| **Brand Boards** | Empty (0 boards) | N/A — not configured |
| **Location logo** | `logoUrl: ""` | Manual or Custom Value `builder_logo_url` |
| **Forms/Surveys** | 401 (route not supported) | Manual capture |
| **Email templates** | Empty body | Spec has copy; styling in Email Builder |
| **Funnels/Websites** | Limited API | Manual or browser capture |
| **Custom Values** | Structure only (no values) | Manual — values set in GHL UI |

---

## Branding Schema (Fill Manually)

Use this structure when capturing from GHL. Other platforms can consume this as the source of truth.

### Colors

```json
{
  "colors": {
    "primary": "#HEX",
    "secondary": "#HEX",
    "accent": "#HEX",
    "text": "#HEX",
    "text_light": "#HEX",
    "background": "#HEX",
    "button_bg": "#HEX",
    "button_text": "#HEX",
    "link": "#HEX"
  }
}
```

**Where to find in GHL:**
- Marketing → Brand Boards → Global Custom Colors
- Funnels → [Funnel] → Design → Color picker
- Forms/Surveys → Style / Theme settings
- Settings → Company → Custom CSS (if used)

### Typography

```json
{
  "fonts": {
    "heading": {
      "family": "e.g. Poppins, Montserrat",
      "weight": "600",
      "size": "24px"
    },
    "body": {
      "family": "e.g. Open Sans, Roboto",
      "weight": "400",
      "size": "16px"
    },
    "button": {
      "family": "inherit or specific",
      "weight": "600",
      "size": "16px"
    }
  }
}
```

**Where to find in GHL:**
- Funnels → Design → Typography
- Forms/Surveys → Font settings
- Email Builder → Template font settings
- Brand Boards (if configured)

### Logo & Assets

```json
{
  "assets": {
    "logo_url": "https://...",
    "logo_favicon_url": "https://...",
    "logo_dark_url": "https://... (if dark variant)"
  }
}
```

**Custom Value:** `builder_logo_url` — set during onboarding. Check GHL → Settings → Custom Values.

### Form & Survey Styling

```json
{
  "forms": {
    "FRM-Lead-Intake": {
      "background_color": "#HEX",
      "button_color": "#HEX",
      "border_radius": "4px",
      "font_family": "..."
    },
    "SRV-Qualification-Survey": {
      "background_color": "#HEX",
      "button_color": "#HEX",
      "progress_bar_color": "#HEX",
      "font_family": "..."
    }
  }
}
```

### Email Template Styling

Email templates in GHL use HTML. Styling is inline or in `<style>` blocks. Capture:

```json
{
  "email_styling": {
    "body_bg": "#HEX",
    "text_color": "#HEX",
    "link_color": "#HEX",
    "button_bg": "#HEX",
    "button_text": "#HEX",
    "font_family": "...",
    "header_logo_height": "60px"
  }
}
```

### Calendar Widget (CAL-Intro-Call)

```json
{
  "calendar": {
    "primary_color": "#HEX",
    "slot_selected_color": "#HEX",
    "font_family": "..."
  }
}
```

### Portal / Membership Pages

```json
{
  "portal": {
    "header_bg": "#HEX",
    "sidebar_bg": "#HEX",
    "card_bg": "#HEX",
    "accent_color": "#HEX",
    "font_family": "..."
  }
}
```

---

## Manual Capture Checklist

Run through this in GHL to populate the spec. Save output to `audit/ghl_branding_captured.json`.

### Step 1 — Brand Boards
- [ ] GHL → Marketing → Brand Boards
- [ ] If boards exist: note each color name + hex
- [ ] Note default font(s)

### Step 2 — Location Settings
- [ ] Settings → Company → Locations → [This location]
- [ ] Logo URL (if set)
- [ ] Any theme/color overrides

### Step 3 — Custom Values
- [ ] Settings → Custom Values
- [ ] Copy actual values for: `builder_logo_url`, `builder_name`, `builder_phone`, etc.
- [ ] (Values are not in API response — must be read from UI)

### Step 4 — Forms
- [ ] Marketing → Forms → FRM-Lead-Intake → Style/Design
- [ ] Note: background, button, font, border radius
- [ ] Repeat for each form

### Step 5 — Survey
- [ ] Marketing → Surveys → SRV-Qualification-Survey
- [ ] Note: colors, fonts, progress bar, page layout

### Step 6 — Email Templates
- [ ] Marketing → Email Templates → PreBuild Autopilot folder
- [ ] Open 1–2 templates → inspect HTML for colors/fonts
- [ ] Note common values (most templates share styling)

### Step 7 — Calendar
- [ ] Calendars → CAL-Intro-Call → Design/Style
- [ ] Note: slot colors, font

### Step 8 — Funnels (if any)
- [ ] Funnels → list all → for each: Design → Colors, Fonts

### Step 9 — Portal
- [ ] Memberships → Portal pages
- [ ] Note: header, sidebar, card styling

---

## Recommended: Add Branding Custom Values

To make future capture API-friendly, add these Custom Values in GHL:

| Key | Example | Use |
|-----|---------|-----|
| `primary_color` | #039BE5 | Buttons, links, accents |
| `secondary_color` | #1a237e | Headers, secondary elements |
| `heading_font` | Poppins | All headings |
| `body_font` | Open Sans | Body text |

Then use `{{custom_values.primary_color}}` in funnel/email builders where GHL supports dynamic tokens. Once set, these can be documented and other platforms can reference them.

---

## Output File: ghl_branding_captured.json

After manual capture, create `audit/ghl_branding_captured.json` with the structure above filled in. Add to repo (or keep local if it contains builder-specific branding). Other platforms can read this + the other audit files for a complete picture.

---

## Summary: What Exists Today

| Source | Content |
|-------|---------|
| `audit/audit_data.json` | Pipelines, workflows, custom fields, tags, location, templates (metadata) |
| `audit/GHL_SUBACCOUNT_DUMP.md` | Human-readable structure summary |
| `audit/GHL_WRITTEN_CONTENT_DUMP.md` | All SMS/email/survey copy |
| `audit/GHL_BRANDING_AND_UI_SPEC.md` | **This file** — schema + checklist for colors, fonts, styling |
| `audit/ghl_branding_captured.json` | *(Create after manual capture)* — actual values |

**Gap:** Colors, fonts, and per-asset styling require manual capture until GHL exposes them via API or we add Custom Values for them.
