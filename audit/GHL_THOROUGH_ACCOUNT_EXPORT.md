# GHL sub-account — thorough capture (from API audit)

> **Source file:** `audit/audit_data.json`  
> **Collected at (UTC):** 2026-03-14T01:24:30.543139  
> **Location ID:** `cVCso4OlgGoOoXMpbxxA`  
> **Note:** Source JSON predates collector v2. Re-run `audit/ghl_audit_collector.py` with `--deep` (and optional `--markdown`) to include extra sections and per-ID workflow/form/survey payloads.  

This document lists **everything the collector returned**: assets that exist in the sub-account, configuration fields (including `isActive`, `status`, draft/published), and API errors where an endpoint was tried but failed. **Activation state is factual metadata only** — not a judgement on build completeness.

---

## Location (full payload)

```json
{
  "location": {
    "id": "cVCso4OlgGoOoXMpbxxA",
    "brandId": "iyIyu3eT50TualcpGTBY",
    "companyId": "wws9evg7Qi0D5XsBNk8X",
    "name": "MASTER FACTORY \u2014 PREBUILD ENGINE",
    "address": "3 ocean street",
    "city": "New Castle",
    "state": "NSW",
    "country": "AU",
    "postalCode": "2290",
    "website": "centriweb.com",
    "timezone": "Pacific/Auckland",
    "firstName": "Jerald",
    "lastName": "Immanuel",
    "email": "jerald@centriweb.com",
    "phone": "+61 466 046 109",
    "logoUrl": "",
    "business": {
      "name": "MASTER FACTORY \u2014 PREBUILD ENGINE",
      "address": "3 ocean street",
      "city": "New Castle",
      "state": "NSW",
      "country": "AU",
      "postalCode": "2290",
      "website": "centriweb.com",
      "timezone": "Pacific/Auckland",
      "email": ""
    },
    "social": {
      "facebookUrl": "",
      "googlePlus": "",
      "linkedIn": "",
      "foursquare": "",
      "twitter": "",
      "yelp": "",
      "instagram": "",
      "youtube": "",
      "pinterest": "",
      "blogRss": "",
      "googlePlacesId": ""
    },
    "settings": {
      "allowDuplicateContact": false,
      "allowDuplicateOpportunity": false,
      "allowFacebookNameMerge": false,
      "disableContactTimezone": false,
      "contactUniqueIdentifiers": [
        "email",
        "phone"
      ],
      "crmSettings": {
        "deSyncOwners": true,
        "syncFollowers": {
          "contact": true,
          "opportunity": true
        }
      },
      "saasSettings": {
        "saasMode": "not_activated",
        "twilioRebilling": {
          "markup": 10,
          "enabled": false
        }
      }
    },
    "dateAdded": "2026-02-25T14:30:13.758Z",
    "domain": "",
    "currency": "",
    "isAgencySubAccount": false,
    "defaultEmailService": "",
    "permissions": {},
    "snapshotId": ""
  },
  "traceId": "7c705c9c-d090-462a-9d86-61a70a40667e"
}
```

## Pipelines (summary table)

**Count:** 1

| # | Name / label | ID | Status / flags |
|---|--------------|-----|------------------|
| 1 | Prebuild Pipeline | `KRZs6JZq3qKVnJyvTmZh` | — |

### Pipelines — stages and full JSON

## Pipelines (complete payload)

```json
{
  "pipelines": [
    {
      "stages": [
        {
          "id": "66dfc3ca-9268-4210-8b5e-4a1e4d6e40b7",
          "name": "New Enquiry",
          "originId": "NzE0NDYyYTQtZjQ0OS00ZGE1LTliNTktNTY2NzQxNTBjOGYy",
          "position": 0,
          "showInFunnel": true,
          "showInPieChart": true
        },
        {
          "id": "0e125a91-9bad-4807-8f5c-9459f9c7bd18",
          "name": "Survey Completed",
          "originId": "NDliY2E0ZDYtODEwYS00MmQwLWJjZjgtMDRjNWNmNTBlOGRj",
          "position": 1,
          "showInFunnel": true,
          "showInPieChart": true
        },
        {
          "id": "8883cbd1-098e-4829-bfa2-1bd558653e28",
          "name": "Qualified - Hot",
          "originId": "MGNmZGMwYjEtNjYzYS00OTYxLWE0ZjUtMDUxMWY0NmQyNzNk",
          "position": 2,
          "showInFunnel": true,
          "showInPieChart": true
        },
        {
          "id": "333e7953-2cea-472e-875e-33d14dd286a8",
          "name": "Nurture - Warm",
          "originId": "MWI1MzhmY2YtZjNiMi00NjA3LTkyZTgtNjc5YWQzOGU1MmI1",
          "position": 3,
          "showInFunnel": true,
          "showInPieChart": true
        },
        {
          "id": "91b6d5c4-2337-40e1-80ea-bbf01e93c8a7",
          "name": "Intro Call Booked",
          "originId": "ZjQxYzczNjktZjMwZi00MDNmLTk3NWUtZDU2ODVlNTM3Njc4",
          "position": 4,
          "showInFunnel": true,
          "showInPieChart": true
        },
        {
          "id": "b35dabb7-d871-4b3c-945a-0a3ad26129a7",
          "name": "Proposal Sent",
          "originId": "MTJlNTllNDgtNmNjMy00ZTE2LWE3MzctNjA1OWM2OTFiNTgw",
          "position": 5,
          "showInFunnel": true,
          "showInPieChart": true
        },
        {
          "id": "c0a80e7f-6347-4f9b-87ad-f9062cbc4ca7",
          "name": "Engaged",
          "originId": "ZGYzZjFmYTQtNjk5ZC00NGE1LWJlMzktNmRkNmE5M2M5ZmM3",
          "position": 6,
          "showInFunnel": true,
          "showInPieChart": true
        },
        {
          "id": "617535ae-a933-440c-96c6-06bf25675d9e",
          "name": "Delivered",
          "originId": "N2QwZWM5MjUtMjYwMS00NWE2LTg2M2UtMDg5Y2M5YjU5ZTBm",
          "position": 7,
          "showInFunnel": true,
          "showInPieChart": true
        },
        {
          "id": "448d8524-9d58-41f7-b6eb-c8f048d4cb28",
          "name": "Won",
          "originId": "YTgzMGI1NDItNjk0NS00MzczLTliMmEtY2NhZTc3OWRjMjRk",
          "position": 8,
          "showInFunnel": true,
          "showInPieChart": true
        },
        {
          "id": "a82b6def-f219-468b-b45c-2ef1032785d3",
          "name": "Not Now",
          "originId": "MWQyMWM0ZDMtZmIwMy00ZjRiLThjY2UtNWNmM2VlNmYzOWNi",
          "position": 9,
          "showInFunnel": true,
          "showInPieChart": true
        },
        {
          "id": "e2bd3aa2-0f5d-42e3-843f-fb63fd1070df",
          "name": "Lost",
          "originId": "OTAxY2VhMGMtZTJjMi00NzY5LWE1YzYtNDQ1NWM3N2NhMDA2",
          "position": 10,
          "showInFunnel": true,
          "showInPieChart": true
        }
      ],
      "dateAdded": "2026-02-25T14:41:43.976Z",
      "dateUpdated": "2026-02-25T14:41:43.977Z",
      "name": "Prebuild Pipeline",
      "originId": "BTGrTxiiFedNARJ2SQR9",
      "id": "KRZs6JZq3qKVnJyvTmZh"
    }
  ],
  "traceId": "f15459e4-a046-49bd-be27-2dc799cdd853"
}
```

## Workflows (list)

**Count:** 10

| # | Name / label | ID | Status / flags |
|---|--------------|-----|------------------|
| 1 | WF-01-Speed-to-Lead | `9f2b93e5-9662-4749-b9d0-6b40c5c1b6a2` | status=draft, version=2 |
| 2 | WF-02-Survey-Reminders | `17891e4d-c278-4895-a3f7-357c3178fb6b` | status=draft, version=2 |
| 3 | WF-03-Scoring-and-Routing | `d52e3147-c48a-44d3-af52-6680e5573b47` | status=draft, version=95 |
| 4 | WF-04-Education-Sequence | `bbfe1ca0-14a6-4452-baea-7128661642b4` | status=draft, version=2 |
| 5 | WF-05-Booking-Flow | `5408bfe2-e1c0-4220-aae5-81c673113183` | status=draft, version=2 |
| 6 | WF-06-Proposal-and-Payment | `2fc5067c-be83-46d3-9a8c-550ce02e4a4e` | status=draft, version=2 |
| 7 | WF-09-Stage-Notifications | `bd849e9f-9361-4526-a3b6-98b976c85d17` | status=draft, version=2 |
| 8 | WF-10-Stale-Lead-Reminders | `c7241790-4b89-4995-b7fa-a1dba97d24db` | status=draft, version=2 |
| 9 | WF-11-Partner-Notifications | `d06709cc-f1fc-4736-8f5b-391682f4c1cc` | status=draft, version=2 |
| 10 | WF-12-Review-Request | `1c1a6318-4ff8-41f1-9a49-ea2176c9576f` | status=draft, version=2 |

## Forms (list)

**Count:** 3

| # | Name / label | ID | Status / flags |
|---|--------------|-----|------------------|
| 1 | FRM-Lead-Intake | `x1jLoeSHaBKZXm8Gm0gu` | — |
| 2 | Book a demo | `GbemuaflhwNAilmnqgEf` | — |
| 3 | SRV-Qualification-Survey | `ugnDa7Hh1lQNb52GUypu` | — |

## Surveys (list)

**Count:** 1

| # | Name / label | ID | Status / flags |
|---|--------------|-----|------------------|
| 1 | SRV-Qualification-Survey | `J30zhHTAz8daVE7wZP7P` | — |

## Calendars (list)

**Count:** 1

| # | Name / label | ID | Status / flags |
|---|--------------|-----|------------------|
| 1 | CAL-Intro-Call | `b4uPmlCoYV7J96XJZBsD` | isActive=False |

## Custom Fields

```json
{
  "customFields": [
    {
      "id": "4sz70FQcItdNAYWypP75",
      "name": "cf_finance_status",
      "model": "contact",
      "fieldKey": "contact.cf_finance_status",
      "placeholder": "",
      "dataType": "SINGLE_OPTIONS",
      "position": 1200,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.802Z",
      "standard": false,
      "picklistOptions": [
        "Yes, fully approved",
        "Yes, pre-approval in place",
        "We're in the process of arranging finance",
        "We're using cash / equity",
        "Not yet, still researching costs first"
      ]
    },
    {
      "id": "65TbdMo6scjMuTjJkqpw",
      "name": "How did you arrive at that budget figure?",
      "model": "contact",
      "fieldKey": "contact.cf_budget_how",
      "placeholder": "",
      "dataType": "SINGLE_OPTIONS",
      "position": 350,
      "documentType": "field",
      "parentId": "9FnvOHrvltkxU4GkB6DQ",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-26T13:19:13.136Z",
      "standard": false,
      "picklistOptions": [
        "I spoke to a bank or broker and got a borrowing figure",
        "I researched build costs online / got rough quotes",
        "A family member or friend built recently and gave me a figure",
        "It's a rough number \u2014 I'm not sure if it's realistic"
      ]
    },
    {
      "id": "BnhU18zxb5FTowoII5Bv",
      "name": "cf_partner_email",
      "model": "contact",
      "fieldKey": "contact.cf_partner_email",
      "placeholder": "",
      "dataType": "TEXT",
      "position": 1350,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.855Z",
      "standard": false
    },
    {
      "id": "GvDfWDn1fVXi7zzeAhIq",
      "name": "Our process involves a paid preconstruction consultation to prepare a detailed budget and project scope before any construction begins. Are you open to this?",
      "model": "contact",
      "fieldKey": "contact.cf_open_to_fee",
      "placeholder": "",
      "dataType": "SINGLE_OPTIONS",
      "position": 750,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.853Z",
      "standard": false,
      "picklistOptions": [
        "Yes, I understand professional advice has a cost",
        "I'd like to understand more about what's included first",
        "I'm not sure, it depends on the cost",
        "No, I expect quotes and consultations to be free"
      ]
    },
    {
      "id": "Q3J4eIjb6jBNWShBassD",
      "name": "cf_lead_score",
      "model": "contact",
      "fieldKey": "contact.cf_lead_score",
      "placeholder": "",
      "dataType": "NUMERICAL",
      "position": 900,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.799Z",
      "standard": false
    },
    {
      "id": "Qrl9ArsqpOoTJLwaEm3Z",
      "name": "cf_service_phase",
      "model": "contact",
      "fieldKey": "contact.cf_service_phase",
      "placeholder": "",
      "dataType": "SINGLE_OPTIONS",
      "position": 1150,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.804Z",
      "standard": false,
      "picklistOptions": [
        "Phase 1 - Budget Assessment",
        "Phase 2 - Detailed Estimate"
      ]
    },
    {
      "id": "aaxgKaLrDXpu3WkUEBDG",
      "name": "cf_contact_role",
      "model": "contact",
      "fieldKey": "contact.cf_contact_role",
      "placeholder": "",
      "dataType": "SINGLE_OPTIONS",
      "position": 850,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.788Z",
      "standard": false,
      "picklistOptions": [
        "Primary",
        "Partner"
      ]
    },
    {
      "id": "agfjXtjPV85k1yIIxNAt",
      "name": "cf_budget_range",
      "model": "contact",
      "fieldKey": "contact.cf_budget_range",
      "placeholder": "",
      "dataType": "SINGLE_OPTIONS",
      "position": 1050,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.844Z",
      "standard": false,
      "picklistOptions": [
        "Under $300K",
        "$300K\u2013$500K",
        "$500K\u2013$800K",
        "$800,000 \u2013 $1,200,000",
        "$1,200,000+",
        "I'm not sure yet, I need help understanding costs"
      ]
    },
    {
      "id": "j4VfskwKJcjzjx1EhaI8",
      "name": "cf_partner_phone",
      "model": "contact",
      "fieldKey": "contact.cf_partner_phone",
      "placeholder": "",
      "dataType": "PHONE",
      "position": 950,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.861Z",
      "standard": false
    },
    {
      "id": "mI294jc8bR3ocPSUyyaZ",
      "name": "cf_land_status",
      "model": "contact",
      "fieldKey": "contact.cf_land_status",
      "placeholder": "",
      "dataType": "SINGLE_OPTIONS",
      "position": 800,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.848Z",
      "standard": false,
      "picklistOptions": [
        "Yes, I own the land/property",
        "We're under contract to purchase",
        "We're actively looking for land",
        "Not applicable \u2014 I'm renovating my existing home"
      ]
    },
    {
      "id": "o5VzkmKKYAKbobEtgk0E",
      "name": "cf_household_id",
      "model": "contact",
      "fieldKey": "contact.cf_household_id",
      "placeholder": "",
      "dataType": "TEXT",
      "position": 1100,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.847Z",
      "standard": false
    },
    {
      "id": "o8Mmf8PKrWkhyMgFNsxC",
      "name": "cf_project_type",
      "model": "contact",
      "fieldKey": "contact.cf_project_type",
      "placeholder": "",
      "dataType": "SINGLE_OPTIONS",
      "position": 1250,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.784Z",
      "standard": false,
      "picklistOptions": [
        "New build",
        "Knockdown rebuild",
        "Major renovation",
        "Extension or addition",
        "Not sure yet"
      ]
    },
    {
      "id": "pL3PpzFrHXXaYhymuGx5",
      "name": "cf_partner_name",
      "model": "contact",
      "fieldKey": "contact.cf_partner_name",
      "placeholder": "",
      "dataType": "TEXT",
      "position": 1000,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.796Z",
      "standard": false
    },
    {
      "id": "rhqrfzfvIDV3IpN3VnMm",
      "name": "When are you hoping to start construction?",
      "model": "contact",
      "fieldKey": "contact.cf_timeline",
      "placeholder": "",
      "dataType": "SINGLE_OPTIONS",
      "position": 1300,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.805Z",
      "standard": false,
      "picklistOptions": [
        "As soon as possible",
        "Within 3-6 months",
        "In 6-12 months",
        "12+ months away",
        "I'm just exploring at this stage"
      ]
    },
    {
      "id": "rnRryJlMEJF6R7GczxmQ",
      "name": "cf_suburb",
      "model": "contact",
      "fieldKey": "contact.cf_suburb",
      "placeholder": "",
      "dataType": "TEXT",
      "position": 1400,
      "documentType": "field",
      "parentId": "9J5apjY7yE5DoT87ovOS",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "dateAdded": "2026-02-25T14:41:35.846Z",
      "standard": false
    }
  ],
  "traceId": "84bf1f0f-8c0e-4f9e-a9dc-a81912becddf"
}
```

## Custom Values

```json
{
  "customValues": [
    {
      "id": "W1PIwsKG6ei5r6GhDxTm",
      "name": "Meeting location",
      "fieldKey": "{{ custom_values.meeting_location }}",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "documentType": "field"
    },
    {
      "id": "vvaTgPGV8GKr55qeZd0H",
      "name": "calendar_link",
      "fieldKey": "{{ custom_values.calendar_link }}",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "documentType": "field",
      "parentId": "D9N3rxMFBkF7LyzBVoVn"
    },
    {
      "id": "3rf7KPRgEEMsbbkNaMu9",
      "name": "service_2_fee",
      "fieldKey": "{{ custom_values.service_2_fee }}",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "documentType": "field",
      "parentId": "D9N3rxMFBkF7LyzBVoVn"
    },
    {
      "id": "wlGZP6ZjVUVBJ6BINPn8",
      "name": "builder_email",
      "fieldKey": "{{ custom_values.builder_email }}",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "documentType": "field",
      "parentId": "D9N3rxMFBkF7LyzBVoVn"
    },
    {
      "id": "C4fROtgclp1luF56hvej",
      "name": "service_1_name",
      "fieldKey": "{{ custom_values.service_1_name }}",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "documentType": "field",
      "parentId": "D9N3rxMFBkF7LyzBVoVn"
    },
    {
      "id": "oLX1uWnN5sYxIqCqFTE2",
      "name": "refund_policy",
      "fieldKey": "{{ custom_values.refund_policy }}",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "documentType": "field",
      "parentId": "D9N3rxMFBkF7LyzBVoVn"
    },
    {
      "id": "8YFzb8p0PgzdVh1AR1tq",
      "name": "service_2_name",
      "fieldKey": "{{ custom_values.service_2_name }}",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "documentType": "field",
      "parentId": "D9N3rxMFBkF7LyzBVoVn"
    },
    {
      "id": "pfd60g17qledTetUmbn4",
      "name": "builder_logo_url",
      "fieldKey": "{{ custom_values.builder_logo_url }}",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "documentType": "field",
      "parentId": "D9N3rxMFBkF7LyzBVoVn"
    },
    {
      "id": "jhu1RHj3eMpAEzJjBeaD",
      "name": "builder_phone",
      "fieldKey": "{{ custom_values.builder_phone }}",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "documentType": "field",
      "parentId": "D9N3rxMFBkF7LyzBVoVn"
    },
    {
      "id": "d3pLVQwE0CIOWYVAwnlh",
      "name": "service_1_fee",
      "fieldKey": "{{ custom_values.service_1_fee }}",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "documentType": "field",
      "parentId": "D9N3rxMFBkF7LyzBVoVn"
    },
    {
      "id": "pS7Pziv6TlCv6CR2wNeJ",
      "name": "builder_name",
      "fieldKey": "{{ custom_values.builder_name }}",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "documentType": "field",
      "parentId": "D9N3rxMFBkF7LyzBVoVn"
    }
  ],
  "traceId": "2fd43791-5887-4dcb-b4ce-2957e24b4106"
}
```

## Tags

```json
{
  "tags": [
    {
      "id": "MXOLGdGZbJieXmd94skG",
      "name": "lead-cold",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "tKwww2XKloLqXK8q7CvL",
      "name": "lead-hot",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "Dj7zf3vRSdlS1gc6ad3u",
      "name": "lead-warm",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "qZEvg5CBpDK2bCPGVUTd",
      "name": "role-partner",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "Vqpcvxmm3P8PGBkSY6BJ",
      "name": "role-primary",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    }
  ],
  "traceId": "54bef99b-1c32-4ad4-8e12-3cd92375724d"
}
```

## Templates

```json
{
  "templates": [
    {
      "dateAdded": "2026-02-25T14:41:45.195Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "name": "SMS-BOOK-Confirmation",
      "originId": "rKmL23eyEP8oR2in7sRc",
      "template": {
        "attachments": [],
        "body": "  "
      },
      "type": "sms",
      "id": "NJRMCgbDfy5I7CgJYeOw"
    },
    {
      "dateAdded": "2026-02-25T14:41:45.204Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "name": "SMS-BOOK-Reminder-24hr",
      "originId": "yLMfHriPsNzpHQQUBGNl",
      "template": {
        "attachments": [],
        "body": "  "
      },
      "type": "sms",
      "id": "HagMETiAlknBPzX5f8O7"
    },
    {
      "dateAdded": "2026-02-25T14:41:45.228Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "name": "SMS-PROP-Agreement-Sent",
      "originId": "rg4VIFfBZ3GNzp2pu9wg",
      "template": {
        "attachments": [],
        "body": "  "
      },
      "type": "sms",
      "id": "j69tNcYHetz36cQmwVBq"
    },
    {
      "dateAdded": "2026-02-25T14:41:45.199Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "name": "SMS-STL-Survey-Link",
      "originId": "njG9CDduIZQiJj3181jA",
      "template": {
        "attachments": [],
        "body": "  "
      },
      "type": "sms",
      "id": "bDXUKR51AfVU1iRrNQ1G"
    },
    {
      "dateAdded": "2026-02-25T14:41:45.235Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "name": "SMS-STL-Survey-Reminder",
      "originId": "tfzjlxmT4nhYRVefXAmL",
      "template": {
        "attachments": [],
        "body": "  "
      },
      "type": "sms",
      "id": "oSg6lXwcNAXEJeVkSYQV"
    }
  ],
  "totalCount": 5,
  "traceId": "ed3bb7c2-17b5-4be6-84eb-811f4ae78576"
}
```

## Campaigns

```json
{
  "campaigns": [],
  "traceId": "7a8f59e7-aed4-41c8-b517-a257ba196bdc"
}
```

## Brand Boards

```json
{
  "brandBoards": [],
  "totalCount": 0,
  "traceId": "54d6b54e-029c-4a77-843f-3b58b4ea3291"
}
```

## Funnels

```json
{
  "funnels": [],
  "count": 0,
  "traceId": "ca532d63-4132-4b24-8b63-9c6673de7525"
}
```

## Custom Objects

**API error:** `404` — {"message":"Cannot GET /locations/cVCso4OlgGoOoXMpbxxA/customObjects","error":"Not Found","statusCode":404}

## Contacts

```json
{
  "contacts": [],
  "total": 0,
  "traceId": "6460e413-6de1-4883-b4b5-206dcfea9f4f"
}
```

## Payments

**API error:** `403` — {"message":"Forbidden resource","error":"Forbidden","statusCode":403}

## Opportunities (opportunities_KRZs6JZq3qKVnJyvTmZh)

```json
{
  "opportunities": [],
  "meta": {
    "total": 0,
    "nextPageUrl": null,
    "startAfterId": null,
    "startAfter": null,
    "currentPage": 1,
    "nextPage": "",
    "prevPage": null
  },
  "traceId": "226458c7-b75a-4d36-900b-ff5cd83c2863"
}
```

## Collector-side analysis

```json
{
  "contacts": {
    "total_sampled": 0,
    "with_qualification_score": 0,
    "with_budget_range": 0,
    "with_lead_temperature": 0,
    "with_service_phase": 0,
    "with_email": 0,
    "with_phone": 0,
    "tag_distribution": {}
  }
}
```

---

*End of export. For full fidelity without truncation, use the JSON source file.*
