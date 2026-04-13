# PreBuild Factory — full live capture (MCP + REST)

> **Generated (UTC):** 2026-04-13T23:51:20Z  
> **Location ID:** `cVCso4OlgGoOoXMpbxxA`  
> **Sources:** Cursor MCP **`user-ghl-prebuild-demo`** (live API) + `audit/audit_data.json` for workflows/forms/survey/SMS/calendar list not in MCP toolset.  
> **Workflow internals / form fields:** run `python3 audit/ghl_audit_collector.py --deep …` and/or GHL UI.  

---

## A. MCP — `locations_get-location`

```json
{
  "location": {
    "id": "cVCso4OlgGoOoXMpbxxA",
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
    "currency": "",
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
    "settings": {
      "allowDuplicateContact": false,
      "allowDuplicateOpportunity": false
    }
  }
}
```

## B. MCP — `locations_get-custom-fields` (model=all)

| GHL name | fieldKey | Data type | Picklist size |
|---|---|---|---|
| cf_prelim_fee_s2 | `contact.cf_prelim_fee_s2` | NUMERICAL | — |
| Business Name | `contact.business_name` | TEXT | — |
| cf_lost_reason | `contact.cf_lost_reason` | TEXT | — |
| cf_finance_status | `contact.cf_finance_status` | SINGLE_OPTIONS | 5 |
| How did you arrive at that budget figure? | `contact.cf_budget_how` | SINGLE_OPTIONS | 5 |
| How did you hear about us? | `contact.cf_how_heard` | SINGLE_OPTIONS | 5 |
| State | `contact.state_dropdown` | SINGLE_OPTIONS | 5 |
| Engagement Phase | `contact.contactcf_engagement_phase` | SINGLE_OPTIONS | 2 |
| cf_partner_email | `contact.cf_partner_email` | TEXT | — |
| cf_lead_temperature | `contact.cf_lead_temperature` | SINGLE_OPTIONS | 3 |
| cf_finance_contingency | `contact.cf_finance_contingency` | SINGLE_OPTIONS | 5 |
| cf_open_to_fee (long label) | `contact.cf_open_to_fee` | SINGLE_OPTIONS | 4 |
| cf_council_contingency | `contact.cf_council_contingency` | SINGLE_OPTIONS | 5 |
| What are the two most important things… | `contact.cf_top_priorities` | MULTIPLE_OPTIONS | 6 |
| cf_land_contingency | `contact.cf_land_contingency` | SINGLE_OPTIONS | 4 |
| cf_delivery_status | `contact.cf_delivery_status` | SINGLE_OPTIONS | 5 |
| Is there anything else we should know before the call? | `contact.cf_precall_additional_notes` | TEXT | — |
| cf_delivery_due_date | `contact.cf_delivery_due_date` | DATE | — |
| cf_design_contingency | `contact.cf_design_contingency` | SINGLE_OPTIONS | 5 |
| cf_lead_score | `contact.cf_lead_score` | NUMERICAL | — |
| cf_service_phase | `contact.cf_service_phase` | SINGLE_OPTIONS | 2 |
| What's your #1 priority in a builder? | `contact.cf_top_priority_1` | SINGLE_OPTIONS | 5 |
| cf_prelim_fee_s3 | `contact.cf_prelim_fee_s3` | NUMERICAL | — |
| Are you the main decision-maker… | `contact.cf_decision_maker` | RADIO | 3 |
| What's the most important thing on our call? | `contact.cf_precall_main_topic` | TEXT | — |
| cf_contact_role | `contact.cf_contact_role` | SINGLE_OPTIONS | 2 |
| cf_budget_range | `contact.cf_budget_range` | SINGLE_OPTIONS | 7 |
| cf_delivery_completed_date | `contact.cf_delivery_completed_date` | DATE | — |
| How would you prefer we stay in touch? | `contact.cf_communication_pref` | RADIO | 4 |
| cf_qualification_score | `contact.cf_qualification_score` | NUMERICAL | — |
| Do you have plans or drawings? | `contact.cf_precall_has_plans` | RADIO | 3 |
| cf_delivery_start_date | `contact.cf_delivery_start_date` | DATE | — |
| cf_partner_phone | `contact.cf_partner_phone` | PHONE | — |
| Decline Sent Date | `contact.cf_decline_sent_date` | DATE | — |
| Have you spoken to any other builders? | `contact.cf_other_builders` | RADIO | 3 |
| cf_land_status | `contact.cf_land_status` | SINGLE_OPTIONS | 4 |
| cf_household_id | `contact.cf_household_id` | TEXT | — |
| cf_project_type | `contact.cf_project_type` | SINGLE_OPTIONS | 5 |
| cf_partner_name | `contact.cf_partner_name` | TEXT | — |
| Have you received any other quotes? | `contact.cf_precall_other_quotes` | RADIO | 2 |
| cf_timeline | `contact.cf_timeline` | SINGLE_OPTIONS | 5 |
| cf_suburb | `contact.cf_suburb` | TEXT | — |
| What's your #2 priority? | `contact.cf_top_priority_2` | SINGLE_OPTIONS | 5 |
| cf_estimator_status | `contact.cf_estimator_status` | SINGLE_OPTIONS | 5 |
| Is there a specific timeline driving your project? | `contact.cf_precall_timeline_driver` | TEXT | — |

*Full picklists: call MCP or GHL UI.*

## C. MCP — `opportunities_get-pipelines`

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

## D. MCP — `contacts_get-contacts` (limit 100)

**meta.total:** 13. *PII: real emails/phones exist on records — table omits email/phone; fetch via GHL/MCP as needed.*

| Contact ID | Name | source | tags (comma) |
|---|---|---|---|
| `rak4VWhq1U6JRdZJ3qO7` | trixy testing | FRM-Lead-Intake | form-lead-intake-completed, survey-completed, lead-hot |
| `jKFMsgKs6eDnjERcu2iH` | karen white | — | — |
| `EhNjYGOZwzy32fxX2znO` | steve harris | — | — |
| `R9eeWJFGvyZBWWfECPsA` | rachel cooper | — | — |
| `m8nuGqQRuzkLEcPGwvhP` | mark anderson | — | — |
| `2FSHZmIAub2zJmyZ91uA` | lisa taylor | — | — |
| `0dhewvmcmLqP6ZArqxT7` | david brown | — | — |
| `oGhQ70aLAPCtYPF2mLYN` | emily chen | — | — |
| `2jcgipjVLeYzuWovyj8p` | james wilson | — | — |
| `RDbX3pqB1LG4MxF2aDBF` | trixy macaraeg | — | — |
| `OWmlyS0bGRvNJZPb9lmJ` | tom mitchell | — | — |
| `wDGAd6lYnAJrQ3zHiuKw` | sarah johnson | — | — |
| `u7thPj7XGpKCvE83oMSl` | test test | FRM-Lead-Intake | form-lead-intake-completed |

## E. MCP — `opportunities_search-opportunity` (Prebuild Pipeline)

```json
{
  "meta": {
    "total": 3
  },
  "opportunities": [
    {
      "id": "Ki59EK9y3l672pjaLpc8",
      "name": "Trixy Testing",
      "pipelineStageId": "8883cbd1-098e-4829-bfa2-1bd558653e28",
      "stageName": "Qualified - Hot",
      "status": "open",
      "contactId": "rak4VWhq1U6JRdZJ3qO7",
      "source": "FRM-Lead-Intake"
    },
    {
      "id": "3E9nYtTtmNvbq1Ne243v",
      "name": "Trixy Macaraeg",
      "pipelineStageId": "333e7953-2cea-472e-875e-33d14dd286a8",
      "stageName": "Nurture - Warm",
      "status": "open",
      "contactId": "RDbX3pqB1LG4MxF2aDBF",
      "source": null
    },
    {
      "id": "UEsbmTWDYm1u2dQq1qpG",
      "name": "TEST TEST",
      "pipelineStageId": "66dfc3ca-9268-4210-8b5e-4a1e4d6e40b7",
      "stageName": "New Enquiry",
      "status": "open",
      "contactId": "u7thPj7XGpKCvE83oMSl",
      "source": "FRM-Lead-Intake"
    }
  ]
}
```

## F. MCP — `conversations_search-conversation` (summary)

```json
{
  "total": 3,
  "conversations": [
    {
      "id": "eSy7c8ztSQi44quZBp3c",
      "contactId": "RDbX3pqB1LG4MxF2aDBF",
      "lastMessageType": "TYPE_EMAIL",
      "unreadCount": 0
    },
    {
      "id": "yzlkhm8MIpGfj5i8kQal",
      "contactId": "rak4VWhq1U6JRdZJ3qO7",
      "lastMessageType": "TYPE_EMAIL",
      "unreadCount": 0
    },
    {
      "id": "LXLPzV6na258qwqpxuL3",
      "contactId": "u7thPj7XGpKCvE83oMSl",
      "lastMessageType": "TYPE_NO_SHOW",
      "unreadCount": 0
    }
  ]
}
```

## G. MCP — `calendars_get-calendar-events` (CAL-Intro-Call, 2024–2027)

Returned **0** events for range `1704067200000`–`1893456000000`.

## H. MCP — `payments_list-transactions`

**0** transactions (empty `data`).

## I. MCP — blogs + categories + authors

- `blogs_get-blogs`: **0** sites.  
- `blogs_get-all-categories-by-location`: **0** categories.  
- `blogs_get-all-blog-authors-by-location`: **0** authors.  

## J. MCP — `emails_fetch-template` (builder + folders)

| Name | ID | Type | childCount |
|---|---|---|---|
| ET-PROP: Unsigned Reminder | `69cda3631af4b43499b82feb` | builder | — |
| Phase 1 Agreement Email | `69cda5a039671024b5878bd7` | builder | — |
| Phase 1 Agreement Email (dup) | `69cda690c1eecde4acd267b4` | builder | — |
| 1. Speed-to-Lead + Survey Emails | `69cbcdd39f2cc51cf68ebf18` | folder | 3 |
| 2. Proposal, Payment + Portal Emails | `69cbcde59baa1b24edf06525` | folder | 4 |
| 4. Education Sequence | `69cba80744ec869b8d66fde6` | folder | 6 |
| 3. Nurture Re-engagement | `69cbce0044ec8692cd68ba34` | folder | 3 |
| 5. Post-Payment Delivery (WF-13) | `69cbce0841aaf0c198d5b3b8` | folder | 13 |
| 6. ET-BOOK-PRECALL | `69cbce119baa1b63a8f06838` | folder | 1 |
| 8. ET-NFE-NEXT-STEPS | `69cbce1daed86939bcf3ecd5` | folder | 1 |
| 7. NFE-BUILDER-INTRO | `69cbce1898caf347567e98f2` | folder | 1 |

## K. MCP — `social-media-posting_get-account`

`accounts`: **[]**, `groups`: **[]**.

## L. REST — `audit/audit_data.json` (collector snapshot)

```json
{
  "audit_collected_at": "2026-03-14T01:24:30.543139",
  "workflows": [
    {
      "id": "9f2b93e5-9662-4749-b9d0-6b40c5c1b6a2",
      "name": "WF-01-Speed-to-Lead",
      "status": "draft",
      "version": 2,
      "createdAt": "2026-02-25T14:41:55.437Z",
      "updatedAt": "2026-02-25T14:42:00.123Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "17891e4d-c278-4895-a3f7-357c3178fb6b",
      "name": "WF-02-Survey-Reminders",
      "status": "draft",
      "version": 2,
      "createdAt": "2026-02-25T14:41:55.741Z",
      "updatedAt": "2026-02-25T14:42:00.097Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "d52e3147-c48a-44d3-af52-6680e5573b47",
      "name": "WF-03-Scoring-and-Routing",
      "status": "draft",
      "version": 95,
      "createdAt": "2026-02-25T14:41:55.956Z",
      "updatedAt": "2026-02-26T14:41:00.025Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "bbfe1ca0-14a6-4452-baea-7128661642b4",
      "name": "WF-04-Education-Sequence",
      "status": "draft",
      "version": 2,
      "createdAt": "2026-02-25T14:41:56.217Z",
      "updatedAt": "2026-02-25T14:42:00.123Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "5408bfe2-e1c0-4220-aae5-81c673113183",
      "name": "WF-05-Booking-Flow",
      "status": "draft",
      "version": 2,
      "createdAt": "2026-02-25T14:41:56.425Z",
      "updatedAt": "2026-02-25T14:42:00.095Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "2fc5067c-be83-46d3-9a8c-550ce02e4a4e",
      "name": "WF-06-Proposal-and-Payment",
      "status": "draft",
      "version": 2,
      "createdAt": "2026-02-25T14:41:56.662Z",
      "updatedAt": "2026-02-25T14:42:00.087Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "bd849e9f-9361-4526-a3b6-98b976c85d17",
      "name": "WF-09-Stage-Notifications",
      "status": "draft",
      "version": 2,
      "createdAt": "2026-02-25T14:41:56.846Z",
      "updatedAt": "2026-02-25T14:42:00.292Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "c7241790-4b89-4995-b7fa-a1dba97d24db",
      "name": "WF-10-Stale-Lead-Reminders",
      "status": "draft",
      "version": 2,
      "createdAt": "2026-02-25T14:41:57.060Z",
      "updatedAt": "2026-02-25T14:41:59.904Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "d06709cc-f1fc-4736-8f5b-391682f4c1cc",
      "name": "WF-11-Partner-Notifications",
      "status": "draft",
      "version": 2,
      "createdAt": "2026-02-25T14:41:57.255Z",
      "updatedAt": "2026-02-25T14:42:00.127Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    },
    {
      "id": "1c1a6318-4ff8-41f1-9a49-ea2176c9576f",
      "name": "WF-12-Review-Request",
      "status": "draft",
      "version": 2,
      "createdAt": "2026-02-25T14:41:57.742Z",
      "updatedAt": "2026-02-25T14:42:00.123Z",
      "locationId": "cVCso4OlgGoOoXMpbxxA"
    }
  ],
  "forms": [
    {
      "id": "x1jLoeSHaBKZXm8Gm0gu",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "name": "FRM-Lead-Intake"
    },
    {
      "id": "GbemuaflhwNAilmnqgEf",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "name": "Book a demo"
    },
    {
      "id": "ugnDa7Hh1lQNb52GUypu",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "name": "SRV-Qualification-Survey"
    }
  ],
  "surveys": [
    {
      "id": "J30zhHTAz8daVE7wZP7P",
      "locationId": "cVCso4OlgGoOoXMpbxxA",
      "name": "SRV-Qualification-Survey"
    }
  ],
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
  "custom_value_names": [
    "Meeting location",
    "calendar_link",
    "service_2_fee",
    "builder_email",
    "service_1_name",
    "refund_policy",
    "service_2_name",
    "builder_logo_url",
    "builder_phone",
    "service_1_fee",
    "builder_name"
  ],
  "sms_templates": [
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
  "calendar": {
    "id": "b4uPmlCoYV7J96XJZBsD",
    "notifications": [],
    "locationId": "cVCso4OlgGoOoXMpbxxA",
    "teamMembers": [],
    "eventType": "RoundRobin_OptimizeForAvailability",
    "name": "CAL-Intro-Call",
    "description": "",
    "widgetSlug": "cal-intro-call-demo-9faa41b6-a29d-4ec6-8d79-cd88d220fe46",
    "calendarType": "round_robin",
    "widgetType": "default",
    "eventTitle": "{{contact.name}}",
    "eventColor": "#039BE5",
    "slotDuration": 30,
    "slotDurationUnit": "mins",
    "slotInterval": 30,
    "slotIntervalUnit": "mins",
    "slotBuffer": 0,
    "slotBufferUnit": "mins",
    "appoinmentPerSlot": 1,
    "appoinmentPerDay": "",
    "openHours": {},
    "enableRecurring": false,
    "recurring": {
      "count": 1,
      "bookingOption": "skip",
      "bookingOverlapDefaultStatus": "",
      "interval": null,
      "freq": "DAILY",
      "monthDays": [],
      "weekDays": []
    },
    "formId": "",
    "stickyContact": false,
    "autoConfirm": true,
    "googleInvitationEmails": true,
    "allowReschedule": true,
    "allowCancellation": true,
    "shouldAssignContactToTeamMember": false,
    "shouldSkipAssigningContactForExisting": false,
    "notes": "Phone:- {{contact.phone}}\nEmail:- {{contact.email}}\n\nNeed to make a change to this event?\nReschedule:-\n{{reschedule_link}}\n\nCancel:-\n{{cancellation_link}}",
    "pixelId": "",
    "formSubmitType": "ThankYouMessage",
    "formSubmitThanksMessage": "Thank you for your appointment request. We will contact you shortly to confirm your request. Please call our office at {{contactMethod}} if you have any questions.",
    "availabilityType": 0,
    "availabilities": [],
    "guestType": "collect_detail",
    "consentLabel": "I confirm that I want to receive content from this company using any contact information I provide.",
    "allowBookingAfterUnit": "days",
    "allowBookingAfter": 0,
    "allowBookingForUnit": "days",
    "preBuffer": 0,
    "preBufferUnit": "mins",
    "isActive": false
  }
}
```

## M. MCP tool coverage note

The **`user-ghl-prebuild-demo`** server exposes ~36 tools (contacts, pipelines, blogs, calendars events, conversations, payments, email builder list, social). It does **not** include workflow definition export, form schema, or survey schema — use **`ghl_audit_collector.py --deep`** for those.
