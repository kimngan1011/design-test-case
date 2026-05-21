# Test Coverage Strategy – LT-94674 – [koyu] Core | 524 – Cancel Booked Event (App)

**Epic:** LT-94674
**Component:** Event Management – Cancel Booked Event
**Partner:** Core / Koyu
**Date:** 2026-03-25
**Qase Suite:** PX suite 2506 (Update - Cancel Booked Event)

---

## 1. Business Rules Categorized by Logic Type

### 1.1 Validation Logic

| # | AC | Rule |
|---|---|---|
| 1 | AC 01.3 | Cancellation Deadline: integer, 0–4 digits, no decimals |
| 2 | AC 03.2 | Mandatory cancellation reason selection — confirm disabled until provided |
| 3 | AC 03.3 | "Other" selected → detail field required; confirm disabled if empty |
| 4 | AC 05.2 | Cancellation Reason Detail: max 255 characters, inline error on exceed |

### 1.2 Boundary / Range Logic

| # | AC | Rule |
|---|---|---|
| 5 | AC 01.3 | Deadline = 0 or null → deadline equals event date |
| 6 | AC 01.3 | Cutoff = Event Start Datetime − Deadline Hours (evaluated in Event timezone) |
| 7 | AC 01.5 | Current date < Booking Start Date → Reserve button disabled |
| 8 | AC 02.2 | Button disabled when deadline expired (current time ≥ cutoff) |
| 9 | AC 02.2 | Button disabled when event is in the past |
| 10 | AC 05.2 | 255-char boundary — at limit vs. exceed |

### 1.3 Conditional Logic

| # | AC | Rule |
|---|---|---|
| 11 | AC 01.1 | Cancel button visible when Cancel Type = Cancel or Cancel Request AND event in future |
| 12 | AC 01.1 | Cancel Type = Do not allow → button hidden |
| 13 | AC 01.2 | Cancel Type = Do not allow → cancel-related fields disabled |
| 14 | AC 01.3 | Cancellation Deadline enabled only when Cancel Type = Cancel or Cancel Request |
| 15 | AC 01.4 | Response Notification = Cancel but Cancel Type = Do not allow → no notification |
| 16 | AC 02.1 | Deadline = 0 → hide Cancellation Deadline section on mobile |
| 17 | AC 02.3 | Button hidden when participant source not allowed by permission settings |
| 18 | AC 03.4 | Cancel Now: remove participant, update capacity |
| 19 | AC 04.2 | Cancel Request: keep participant, do NOT remove |

### 1.4 State Transition

| # | AC | Rule |
|---|---|---|
| 20 | AC 01.3 | Update deadline for in-progress event → warning → Confirm (recompute unstarted) / Cancel (no change) |
| 21 | AC 03.4 | Response Status: Attend → Canceled (Cancel Now) |
| 22 | AC 04.2 | Response Status: Attend → Cancel Requested (Cancel Request) |
| 23 | AC 02.1 | Already Canceled/Cancel Requested → button not shown |
| 24 | AC 10.1 | Canceled + removed → re-booking allowed → new participant record |

### 1.5 Permission Logic

| # | AC | Rule |
|---|---|---|
| 25 | AC 02.1 / 02.3 | Direct participant: Allow_Cancel_Direct__c controls cancellation eligibility |
| 26 | AC 02.1 / 02.3 | Booked participant: Allow_Cancel_Booked__c controls cancellation eligibility |
| 27 | AC 02.3 | Participant source mismatch with permission → button hidden |

### 1.6 Data Integrity

| # | AC | Rule |
|---|---|---|
| 28 | AC 01.1 | Migration: Cancel Config ON → Cancel Type = Cancel; OFF → Do not allow |
| 29 | AC 03.4 | Cancel Now saves: Cancellation Reason, Detail, updates capacity |
| 30 | AC 04.2 | Cancel Request saves: Cancellation Reason, Detail, Cancellation_Request_Date |
| 31 | AC 10.1 | Re-booking: previous record retained for audit; new record has blank cancellation fields |

### 1.7 Cross-System Impact

| # | AC | Rule |
|---|---|---|
| 32 | AC 06.1 | Calendar: canceled/requested event still visible with status indicator |
| 33 | AC 07.1 | SF bell notification to staff; content includes student name, event, type, reason |
| 34 | AC 07.1 | Notification only for mobile-initiated actions, not admin/manual/import |
| 35 | AC 08.1 | Participant list: Response column with new values + Requested Date |
| 36 | AC 08.2 | Participant detail: Cancellation Reason + Detail visible |
| 37 | AC 08.3 | Edit participant: new response selections; Filter: new response options |

---

## 2. Coverage Strategy

| # | AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|---|
| 1 | AC 01.1 | Cancel button visibility by Cancellation Type | Conditional | Decision Table | Critical | Deep |
| 2 | AC 01.1 | Migration: Cancel Config → Cancel Type | Data Integrity | CRUD Testing | Critical | Deep |
| 3 | AC 01.2 | Cancellation Type options and behavior | Conditional | Decision Table | High | Standard |
| 4 | AC 01.3 | Cancellation Deadline enable/disable | Conditional | Decision Table | High | Standard |
| 5 | AC 01.3 | Cutoff = Event Start − Deadline Hours | Boundary | BVA | Critical | Deep |
| 6 | AC 01.3 | Deadline 0/null = event date | Boundary | BVA | High | Standard |
| 7 | AC 01.3 | Update deadline for in-progress event | State Transition | State Transition Testing | High | Deep |
| 8 | AC 01.3 | Deadline validation (integer, 0–4 digits) | Validation | EP + Negative Testing | Medium | Standard |
| 9 | AC 01.4 | Response Notification default + Cancel option | Conditional | Decision Table | High | Standard |
| 10 | AC 01.4 | Cancel Notification + Cancel Type mismatch | Conditional | Decision Table | Medium | Standard |
| 11 | AC 01.5 | Booking Start Date controls Reserve button | Boundary | BVA | High | Standard |
| 12 | AC 01.6 | Event Master View new sections | Validation | EP | Low | Smoke |
| 13 | AC 02.1 | Button visible+enabled for eligible participant | Conditional | Decision Table | Critical | Deep |
| 14 | AC 02.1 | Deadline = 0 hides Deadline section | Conditional | EP | Medium | Standard |
| 15 | AC 02.2 | Button disabled: deadline expired or past event | Boundary | BVA | Critical | Deep |
| 16 | AC 02.3 | Button hidden: source mismatch | Permission | Permission Matrix | Critical | Deep |
| 17 | AC 02.1 | Button hidden: already Canceled/Requested | State Transition | State Transition Testing | High | Standard |
| 18 | AC 03.1 | Cancel Now modal content | Validation | EP | Medium | Standard |
| 19 | AC 03.2 | Mandatory reason + confirm disabled | Validation | EP + Negative Testing | Critical | Deep |
| 20 | AC 03.3 | Other → detail required | Conditional | Decision Table | Critical | Deep |
| 21 | AC 03.4 | Execute Cancel Now (remove, capacity, status) | State Transition | State Transition + CRUD | Critical | Deep |
| 22 | AC 04.1 | Cancel Request modal content | Validation | EP | Medium | Standard |
| 23 | AC 04.2 | Execute Cancel Request (keep participant, request date) | State Transition | State Transition + CRUD | Critical | Deep |
| 24 | AC 05.1 | Cancellation reason options list | Validation | EP | Medium | Smoke |
| 25 | AC 05.2 | Detail max 255 chars + inline error | Boundary | BVA + Negative Testing | Medium | Standard |
| 26 | AC 06.1 | Calendar status display | Cross-system | Regression Analysis | High | Standard |
| 27 | AC 07.1 | Staff notification content + trigger | Cross-system | Regression Analysis | High | Deep |
| 28 | AC 07.1 | No notification for admin/manual actions | Conditional | Decision Table | Medium | Standard |
| 29 | AC 08.1 | Participant list response column + requested date | Cross-system | CRUD Testing | High | Standard |
| 30 | AC 08.2 | Participant detail: reason + detail | Cross-system | CRUD Testing | Medium | Standard |
| 31 | AC 08.3 | Edit participant + Filter new responses | Cross-system | CRUD Testing | Medium | Standard |
| 32 | AC 09.1 | Manual post-cancellation actions | Data Integrity | CRUD Testing | Medium | Smoke |
| 33 | AC 10.1 | Re-booking after cancellation | State Transition | State Transition + CRUD | Critical | Deep |
| 34 | AC 10.1 | Audit trail: old record retained, new blank | Data Integrity | CRUD Testing | High | Standard |

---

## 3. High-Risk Areas

### 🔴 Critical Risk

| Area | Risk Reason | Recommended Approach |
|---|---|---|
| Cancel button visibility logic (AC 01.1, 02.1, 02.2, 02.3) | Complex multi-condition decision: Cancel Type × deadline × event date × participant source × response status. Any mistake hides or wrongly shows the button. | Full Decision Table: enumerate all condition combinations |
| Cancel Now execution (AC 03.4) | Participant removed + capacity updated immediately. Incorrect behavior = data loss or stale capacity. | State Transition + negative cases + concurrent scenarios |
| Cancel Request execution (AC 04.2) | Must NOT remove participant. If confused with Cancel Now logic → data corruption. | Explicit comparison tests: Cancel Now vs Cancel Request side-by-side |
| Cancellation deadline evaluation (AC 01.3) | Cutoff computed dynamically using Event timezone. Off-by-one or timezone errors → wrong eligibility. | BVA at exact cutoff boundary + timezone variation tests |
| Migration (AC 01.1) | Existing data must be correctly migrated. Wrong mapping → all existing events have broken cancellation. | CRUD: verify pre/post migration state for both ON and OFF config |

### 🟠 High Risk

| Area | Risk Reason | Recommended Approach |
|---|---|---|
| Re-booking after cancellation (AC 10.1) | Audit trail must be preserved; new record must be clean. Race condition if capacity fills. | State Transition + CRUD + boundary (capacity = 1 remaining) |
| Staff notification (AC 07.1) | Must only trigger on mobile-initiated, not admin. Wrong trigger → notification spam. | Decision Table: mobile vs. admin × notification setting |
| Update deadline for in-progress event (AC 01.3) | Recomputation must only affect unstarted activities. Wrong scope → past events recalculated. | State Transition: mix of past/current/future activities |
| Permission matrix (AC 02.3) | Direct vs. Booked × Allow_Cancel_Direct × Allow_Cancel_Booked → 4 combinations. | Permission Matrix: all 4 combinations tested |

### 🟡 Medium Risk

| Area | Risk Reason | Recommended Approach |
|---|---|---|
| Cancellation Reason detail (AC 05.2) | 255-char limit; reuses existing field. Overwrite risk. | BVA: 254, 255, 256 chars |
| Calendar status display (AC 06.1) | Visual indicator. Low logic risk but high visibility. | Smoke: Canceled and Cancel Requested displayed |
| Participant list & detail (AC 08.x) | New response values in list/filter/edit. | EP: each new value appears correctly |
| Event Master View (AC 01.6) | Layout change only. | Smoke: sections present |

---

## 4. Coverage Gaps (vs. Existing Suite 2446)

| Gap Area | Existing (Suite 2446) | Overlap | New Coverage Needed in Suite 2506 |
|---|---|---|---|
| AC 01.1 — Cancel button by Cancel Type | Covered (original AC with checkboxes) | Partial — old logic used checkboxes, new uses Cancel Type | Retest with updated logic: Cancel Type controls visibility |
| AC 01.1 — Migration logic | Not covered | None | New: Cancel Config ON/OFF → Cancel Type mapping |
| AC 01.5 — Open to Booking section | Not covered | None | New: Booking Start Date, Reserve button, message display |
| AC 02.1 — Deadline = 0 hides section | Partially covered | Partial | Verify section hidden (not just button behavior) |
| AC 05.2 — 255-char boundary | Not explicitly covered | None | New: BVA at 254/255/256 chars + inline error |
| AC 08.3 — Edit + Filter responses | Not explicitly covered | None | New: Edit participant with new responses + filter |
| AC 10.1 — Re-booking + audit trail | Not covered | None | New: full re-booking flow + record retention check |

---

## 5. Suggested Test Suite Structure

```
output/test-cases/lesson-management/event/cancel-booked-event/
  ├── LT-94674-cancel-booked-event-update.csv     → Full CSV for Qase import (suite 2506)
```

**Qase Suite Hierarchy under suite 2506:**

```
Update - [koyu] Core | 524 - Cancel Booked Event (App)  (2506)
  ├── US01 - Configure Cancellation Settings (Updated)
  ├── US02 - Display Cancel Reservation Action (Updated)
  ├── US03 - Cancel Now (Updated)
  ├── US04 - Cancel Request (Updated)
  ├── US05 - Cancellation Reason Input
  ├── US06 - Calendar Status Display
  ├── US07 - Staff Notifications
  ├── US08 - Participant List & Detail
  ├── US09 - Post-Cancellation Actions
  └── US10 - Re-book After Cancellation
```

**Note:** Since suite 2446 already has comprehensive coverage of the original ACs, suite 2506 should focus on:
- Updated behavior (Cancel Type replacing checkbox-based visibility)
- Migration logic
- New features (Booking section, re-booking, audit trail)
- Gaps identified above
- Avoid duplicating test cases already well-covered in suite 2446
