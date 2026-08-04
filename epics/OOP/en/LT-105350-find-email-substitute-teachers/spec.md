---
ticket_id: LT-105350
ticket_url: https://manabie.atlassian.net/browse/LT-105350
title: "[EN] Finding and Emailing Substitute Teacher Candidates"
module: lesson-management
status: In Development
internal_uat_date: 2026-07-27
production_release_date: 2026-08-10
last_updated: 2026-07-22
---

# LT-105350: [EN] Finding and Emailing Substitute Teacher Candidates

## Summary

When a lesson requires a substitute teacher, EN (Education Network) staff need a way to quickly identify available candidate teachers and bulk-send offer emails to them directly from the Lesson Detail page. The feature enhances the existing **Add Teacher popup** on Lesson Detail with EN-specific filtering (Flagged teachers, available-teacher logic that checks both registered working hours and existing lesson conflicts, brand-level location, subject) and adds an email composer that bulk-sends to all selected candidates via the company email tool.

---

## Sources

| Source | URL | Notes |
|---|---|---|
| Jira epic | https://manabie.atlassian.net/browse/LT-105350 | Status: In Development |
| Working Hours epic | https://manabie.atlassian.net/browse/LT-64009 | Defines teacher working-hours object and the "Only teachers free at this time" filter behavior |
| PRD (Confluence draft) | https://manabie.atlassian.net/wiki/pages/resumedraft.action?draftId=2687467521 | Title: "EN Requirements - Aug 2026" — primary source |
| Flow (Miro) | https://miro.com/app/board/uXjVL2P0mmI=/?moveToWidget=3458764675672452956&cot=14 | High-level user flow diagram |
| JP PRD (for Client) | https://docs.google.com/document/d/1p8QifBXLofEDIINnU8NZ8WmV1_VgQqxh-6tABmE9SgM/edit?tab=t.0 | JP-language version of PRD |
| PBT epic | https://manabie.atlassian.net/browse/PBT-3394 | [EN] Finding and Emailing Substitute Teacher Candidates |

---

## Reference Scale (EN-specific context)

- Entire Kanto area: up to **~400 teachers**
- After filtering by subject: **~80 teachers** (~1/5 of area)
- Expected recipients per bulk email offer: **~50 teachers**

---

## Acceptance Criteria

> **Source:** PRD "EN Requirements - Aug 2026" (Confluence draft ID 2687467521). All ACs below are extracted from PRD headings "User Story & Acceptance Criteria". Items marked `[TBC]` remain unconfirmed in the PRD.

---

### US-01: Select Lesson (as is — existing flow, no change)

| # | Action | Acceptance Criteria / Error Handling | UI Surface |
|---|---|---|---|
| AC 01.1 | Staff opens a lesson that requires a substitute teacher | Lesson opens from the Lesson Calendar | Lesson Calendar (SF) |
| AC 01.2 | Staff clicks "Add Teacher" on Lesson Detail page | Teacher list popup opens | Lesson Detail (SF) |

---

### US-02: Search and Filter Teacher Candidates

| # | Action | Acceptance Criteria / Error Handling | UI Surface |
|---|---|---|---|
| AC 02.1 | Staff searches and filters candidates; staff selects candidates | See detailed filter rules below | Add Teacher popup (SF) |

**Filter rules (all part of AC 02.1):**

| Filter | Rule |
|---|---|
| **Location Selector** | Same UI pattern as current Master Event segments location selector. Staff first selects a broad area (brand), then can exclude lower-level Locations to narrow candidates. EN teachers are affiliated at Brand or Area level. EN teachers can be community plus users OR contact-level users. |
| **Subject filter** | Filter teachers by eligible subjects. `[TBC]` — subject availability for EN is unconfirmed. |
| **Available Teacher Checkbox / "Only teachers free at this time"** | When ON, only teachers who pass **both** availability checks are shown: (1) the target lesson is fully covered by the teacher's registered working hours, and (2) the teacher has no existing lesson overlapping the target lesson time in any location. When OFF, this combined availability filter is not applied. |
| **Flagged Teacher Checkbox** | Filters the candidate list by "Flagged" status on the teacher's Contact record. **Default: UNchecked** (flagged teachers are excluded by default). When checkbox is **enabled**: teachers whose Contact has "Flagged" checked are also included in results. |
| **Flagged column (teacher list)** | A "Flagged" (要注意講師) column is shown in the teacher list inside the Add Teacher popup so staff can identify flagged candidates before selecting. |
| **Real-time count** | The current number of matching teachers is displayed in real time as filter criteria change. |

**Note on Flagged:** "Flagged" can represent various reasons. Staff should check and update the reason on the Contact page. On the Lesson side, only filtering is required — no management of the flag itself.

**Available-teacher logic (from LT-64009 + LT-105350 Jira confirmation):**

| Check | Rule |
|---|---|
| Working-hours coverage | A teacher passes when the target lesson's weekday/time is within a non-Off Day working-hours record for that teacher: `staff_start_time <= lesson_start_time < lesson_end_time <= staff_end_time`. The comparison uses the lesson time in JST/displayed local time. |
| Existing lesson no-overlap | A teacher passes when they have no existing lesson whose time overlaps the target lesson. Overlap is defined as `existing_lesson_start < target_lesson_end AND target_lesson_start < existing_lesson_end`. Existing lessons are checked across any location. **Cancelled and Completed lessons are excluded from the conflict set**; overlapping Cancelled/Completed lessons must not exclude the teacher. |
| Adjacent lesson boundary | Existing lessons that end exactly at the target lesson start, or start exactly at the target lesson end, are not overlaps and must not exclude the teacher. |
| Combined result | The teacher appears only when both checks pass. Failing either working-hours coverage or no-overlap excludes the teacher while the checkbox/toggle is ON. |

---

### US-03: Send Email to Selected Candidates

| # | Action | Acceptance Criteria / Error Handling | UI Surface |
|---|---|---|---|
| AC 03.1 | After selecting teacher candidates, staff clicks "Send Email" | Email editor opens. **Error case:** If no candidate is selected when "Send Email" is clicked, prevent opening the editor and display error message: EN: "Please select one or more Teachers." / JP: "1人以上の講師を選択してください". Alternatively, the "Send Email" button may be deactivated/disabled until at least one teacher is selected. | Add Teacher popup (SF) |
| AC 03.2 | Staff edits the email content on the editor and confirms sending | Offer-emails are bulk-sent to all selected candidates. See detailed email rules below. | Email editor popup (SF) |

**Email rules (part of AC 03.2):**

| Rule | Specification |
|---|---|
| **Candidate count display** | The editor shows the number of selected candidates. |
| **Email subject template** | Default subject/title: `代講をお願いいたします`. Subject remains editable by staff unless implementation confirms otherwise. |
| **Email body template** | Default body is text-only template from PRD: `案件名：` / `時間：`. Staff edits message per case. Template text can be configured per partner. |
| **Content type** | Text only. |
| **Sending method** | The system generates the recipient list; staff creates and sends using the company email tool (outside Manabie/SF). |
| **Recipient privacy** | Each email must be sent separately, or via BCC, so that no candidate sees other candidates' email addresses. |
| **Receiver volume / limit** | EN expected recipient volume is around 50 teachers, sometimes 70-80. The flow must not impose an arbitrary 50-recipient cap. If the sending method has a 5,000 emails/day limit for non-SF-account recipients, the system must handle the limit visibly and must not silently drop recipients. SF-account recipients are expected to have no such per-day receiver cap. |
| **Email log** | Sent email logs can be attached to each recipient teacher's Contact so staff can verify send history from the Contact record. |
| **Post-send operations** | Reply, negotiation, and final teacher assignment are done outside Manabie/SF. Staff changes the teacher assignment once the substitute is confirmed. |

---

## Localization

| UI Section | EN | JP |
|---|---|---|
| Teacher candidate search pop-up — Filter: Area | Area | エリア |
| Teacher candidate search pop-up — Filter: Subject | Subject | 科目 |
| Teacher candidate search pop-up — Filter: Working Hour | Working Hour | 勤務可能時間 |
| Teacher candidate search pop-up — Filter: Commutable day of week | Commutable day of week | 勤務可能曜日 |
| Teacher candidate search pop-up — Flagged teacher filter label | Flagged teacher | 要注意講師 |
| Teacher candidate search pop-up — Teacher list column | Flagged | 要注意講師 |
| Contact page — Teacher flag | Flagged | 要注意講師 |
| Teacher candidate search pop-up — Send Email button | Send Email | メールを送信する |
| Error: no selection | Please select one or more Teachers. | 1人以上の講師を選択してください |
| Email editor — Default subject/title | — | 代講をお願いいたします |
| Email editor — Default body template | — | 案件名： / 時間： |

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| BR-01 | AC 01.2 | Entry point is the existing "Add Teacher" button on Lesson Detail — not a separate "Find substitute teachers" menu | Add Teacher button | editable | [SF] |
| BR-02 | AC 01.2 | Clicking "Add Teacher" opens the Teacher list popup (the existing Add Teacher popup, enhanced) | Teacher list popup | — | [SF] |
| BR-03 | AC 02.1 | Available Teacher Checkbox / "Only teachers free at this time": when ON, filters teachers whose registered working-hours record fully covers the target lesson time (`staff_start_time <= lesson_start_time < lesson_end_time <= staff_end_time`) | Available Teacher Checkbox | editable | [SF] |
| BR-04 | AC 02.1 | Available Teacher Checkbox / "Only teachers free at this time": when ON, also excludes teachers who have existing Draft/Published lessons overlapping the target lesson time in any location; Cancelled/Completed lessons are ignored | — | auto-calc | [SF] |
| BR-05 | AC 02.1 | Location filter: brand-level first, then exclude lower-level Locations (same pattern as Master Event segments location selector) | Location Selector | editable | [SF] |
| BR-06 | AC 02.1 | EN teacher affiliation is at Brand or Area level | — | locked | [SF] |
| BR-07 | AC 02.1 | EN teachers can be community plus users OR contact-level users | — | locked | [SF] |
| BR-08 | AC 02.1 | Flagged Teacher Checkbox default: UNchecked (flagged teachers excluded by default) | Flagged Teacher Checkbox | editable | [SF] |
| BR-09 | AC 02.1 | When Flagged checkbox is enabled: teachers whose Contact has "Flagged" checked are included in results | — | auto-calc | [SF] |
| BR-10 | AC 02.1 | "Flagged" column shown in teacher list within Add Teacher popup | Flagged column | locked | [SF] |
| BR-11 | AC 02.1 | Matching teacher count is updated in real time as filters change | Match count | auto-calc | [SF] |
| BR-12 | AC 02.1 | Filter by eligible subjects is available `[TBC — subject scope for EN]` | Subject filter | editable | [SF] |
| BR-13 | AC 03.1 | "Send Email" with 0 selected candidates: prevent opening email editor + show error OR disable button | Send Email button | locked | [SF] |
| BR-14 | AC 03.1 | Error message — EN: "Please select one or more Teachers." / JP: "1人以上の講師を選択してください" | Error message | auto-calc | [SF] |
| BR-15 | AC 03.2 | Email bulk-sent to all selected candidates simultaneously | Email send action | editable | [SF] |
| BR-16 | AC 03.2 | Selected candidate count displayed in email editor | Candidate count | auto-calc | [SF] |
| BR-17 | AC 03.2 | Email editor opens with PRD template: subject/title `代講をお願いいたします` and body `案件名：` / `時間：`; body is text-only and template can be configured per partner | Email subject/body | editable | [SF] |
| BR-18 | AC 03.2 | System generates recipient list → staff sends via company email tool (outside Manabie/SF) | — | auto-calc | [SF] |
| BR-19 | AC 03.2 | Emails sent separately or BCC; each candidate must not see other candidates' addresses | — | locked | [SF] |
| BR-20 | AC 03.2 | Post-send operations (reply, negotiate, final teacher assignment) are done outside Manabie/SF | — | — | [SF] |
| BR-21 | AC 03.2 | Email log is attached to each selected teacher Contact after send, so staff can verify candidate email history | Contact email activity/log | auto-calc | [SF] |
| BR-22 | AC 03.2 | Receiver volume supports EN expected usage: around 50 recipients and sometimes 70-80; no arbitrary 50-recipient cap. If applicable, non-SF-account 5,000 emails/day limit is handled visibly; SF-account recipients have no such cap | Recipient volume/limit | auto-calc | [SF] |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [EXTENDED] | `epics/cross-domain/LT-96237-assign-teachers-available-status-only/` + Jira `LT-64009` | AC 02.1 / BR-03-04 | The existing Add Teacher popup "Only teachers free at this time" toggle is enhanced for EN substitute search. When ON, it stacks both checks: working-hours coverage from `LT-64009` AND no existing lesson overlap from `LT-105350`. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [MISSING BEHAVIOR] | Jira description (not in PRD) | Jira mentions "Sync Email activities under selected lesson to observe recipients read status" but this is absent from PRD ACs. Scope unclear. |
| 2 | [MISSING BEHAVIOR] | AC 03.2 | No AC defines the UI state after bulk email is sent: does the popup close? Is there a success confirmation toast or banner? |
| 3 | [MISSING BEHAVIOR] | AC 03.2 | No AC defines failure handling when email sending fails (network error, invalid email address, or company email tool error). |
| 4 | [MISSING BEHAVIOR] | AC 02.1 / BR-12 | Subject filter scope for EN is marked `[TBC]` in both Jira and PRD. No AC defines which subjects are available or how they are configured. |
| 5 | [MISSING BEHAVIOR] | PRD Reference Scale | No AC covers pagination or load performance for ~400 teachers. For ~80 filtered results, a single page may be acceptable, but it is not specified. |
| 6 | [MISSING BEHAVIOR] | AC 03.2 | No AC specifies whether staff can resend email (re-open editor) after the initial send, or if there is a limit per lesson. |
| 7 | [ROLE GAP] | AC (all sections) | No AC specifies which SF user roles (HQ Admin, CM, Staff) are authorized to see and use the "Send Email" button. Jira description says "EN CM or HQ staff" but this is not in the PRD ACs. |
| 8 | [CONFIRMED VIA PRD] | PRD body (Send Email section) | Default email subject/title is `代講をお願いいたします`; default body template is `案件名：` / `時間：`. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | — | — | — | No directly relevant lesson-learned incidents found in `core.md` or `oop.md`. | — |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| — | No existing E2E scenario covers the substitute teacher search + email flow | New coverage needed | CREATE new E2E scenario: "Find and Email Substitute Teacher Candidates (EN)" |

### Assumptions Made

- The "Add Teacher" popup is the existing BO popup (Lesson Detail), enhanced — not a new screen.
- "Send Email" opens a second popup (email editor) within the Add Teacher popup flow.
- Sending is handled by the company's external email tool; Manabie/SF generates and passes the recipient list.
- EN (Education Network) is a new OOP partner tenant (not currently in the partner list). Folder placed under `epics/OOP/en/`.
- The "Flagged" flag lives on the Salesforce Contact record for the teacher.
- Roles: "EN CM or HQ staff" (from Jira description) can access this feature; exact SF profile names not specified.

---

## Clarification Questions

> Status: **Not yet posted to Jira**

1. **[ROLE GAP]** Which SF user roles (e.g., HQ Admin, Centre Manager, Centre Staff) are authorized to see and use the "Send Email" button in the Add Teacher popup? The PRD says "EN CM or HQ staff" — please confirm the exact SF profile list.
   _Evidence: AC (all sections) — no role restriction is defined in any AC._

2. **[MISSING BEHAVIOR]** "Sync Email activities under selected lesson to observe recipients read status" is mentioned in the Jira description but is absent from all PRD ACs. Is this feature in scope for LT-105350? If yes, please add an AC with the expected behavior.
   _Evidence: Jira description (solution list, item 9) vs. PRD ACs — no corresponding AC exists._

3. **[MISSING BEHAVIOR]** After staff clicks "Send Email" and the bulk email send is confirmed, what does the UI show? Does the Add Teacher popup close, stay open, or show a success message?
   _Evidence: AC 03.2 — no success/post-send state is defined._

4. **[MISSING BEHAVIOR]** What happens if the bulk email send fails (e.g., network error, invalid email address, or company email tool API error)? Should the system show an error message? Which candidates' failures should be reported?
   _Evidence: AC 03.2 — no failure handling is defined._

5. **[MISSING BEHAVIOR]** Is Subject filtering in scope for this ticket? The PRD and Jira both mark it `[TBC]`. Please confirm whether subject filter is included in the initial release or deferred.
   _Evidence: PRD AC 02.1 "(available subject) TBC" and Jira description "(available subject) TBC"._

---

## Related Specs

- `epics/cross-domain/LT-96237-assign-teachers-available-status-only/` — Existing "Add Teacher" popup with "Only teachers free at this time" toggle and Working Status filter; BR-03-04 of this ticket extend that behavior.
- `https://manabie.atlassian.net/browse/LT-64009` — Working Hours epic; defines teacher working-hours records and time containment logic used by BR-03.

## Related Test Cases

- `epics/cross-domain/LT-96237-assign-teachers-available-status-only/test-cases/add-teacher-popup-working-status-filter.md` — Existing tests for the "Only teachers free at this time" filter label and behavior; may need regression checks.
- `epics/cross-domain/LT-96237-assign-teachers-available-status-only/test-cases/lesson-calendar-teacher-list-working-status-filter.md` — Teacher list panel filter baseline.

## QASE Coverage Gaps

- Local test cases now cover AC 02.1 / BR-03-04, including working-hours coverage, Draft/Published overlap exclusion, Cancelled/Completed overlap ignore, cross-location overlap, and adjacent boundary. Qase import/update may still be needed.
- Local test cases now cover AC 02.1 / BR-08-11, including Flagged Teacher default/exclusion/inclusion, Flagged column, and real-time count. Qase import/update may still be needed.
- Local test cases now cover AC 02.1 / BR-05-07, including EN brand/area location affiliation and community plus/contact-level users. Qase import/update may still be needed.
- Local test cases now cover AC 03.1 / BR-13-14, including Send Email 0-selection guard and PRD translations. Qase import/update may still be needed.
- Local test cases now cover AC 03.2 / BR-15-22, including PRD subject/body template, recipient list, BCC/separate privacy, Contact email logs, receiver volume, and daily-limit handling. Qase import/update may still be needed.
- Remaining requirement gap: subject filter scope for EN is still TBC.
