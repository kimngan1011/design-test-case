ID: https://manabie.atlassian.net/browse/PBT-1859 (Improvement context)
Confluence: https://manabie.atlassian.net/wiki/spaces/CC/pages/2375712769
Confluence (Flow): https://manabie.atlassian.net/wiki/spaces/PRDM/pages/1279623170

## Summary

Lesson Allocation (LA) is the core data record that links a student to a course for a defined
duration and slot configuration. An LA is created automatically when a student order is placed
(via new order group, enrollment, or update order), and its duration and slot values are updated
or deleted in response to subsequent order changes (cancel, update slot, void), or application
flows (withdrawal, LOA, resume, graduation). This spec covers the complete LA lifecycle:
creation, update, deletion, and the impact on class assignment, student sessions, and lesson reports.

**PBT-1859 scope** (improvement): Allow adding a new course to an existing product using a past
effective date. Previously blocked; now enabled for Renseikai with boundary validation.

---

## Acceptance Criteria

### US 01 — LA Created from New Order Group

A CM creates a new order group for a student, selects a product offering with one or more courses
(Require Allocation = True), sets a start date (past, today, or future), and submits.
The system creates an LA per course per product.

| ID       | Business Rule                                                                                                                        |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| AC 01.1  | LA is created for each course where Require Allocation flag = True                                                                   |
| AC 01.2  | LA start date = order start date                                                                                                     |
| AC 01.3  | LA end date = order end date                                                                                                         |
| AC 01.4  | LA teaching method = teaching method of the course offering's course master                                                          |
| AC 01.5  | LA type = course type of the course linked to the product                                                                            |
| AC 01.6  | Product detail = course + package type (Schedule / Frequency / One-Time / Slot-Based)                                                |
| AC 01.7  | Purchased Slot: Schedule = sessions/week; Frequency = slot/week; One-Time = slots from program master; Slot-Based = slots from order |
| AC 01.8  | Total session count = 0 on creation; no student session auto-created                                                                 |
| AC 01.9  | LA visible in Contact → Course tab → Require Lesson Allocation list and Lesson Allocation list                                       |
| AC 01.10 | If a class is assigned on the order, class_member is created with start date & end date = LA duration                                |
| AC 01.11 | Start date may be in the past (past-date creation is supported for all product types)                                                |

---

### US 02 — LA Created from Enrollment Order

A CM creates an enrollment application, selects product + course, assigns a class, and submits.
LA creation follows the same rules as US 01.

| ID      | Business Rule                                          |
| ------- | ------------------------------------------------------ |
| AC 02.1 | LA is created with same rules as US 01 (AC 01.1–01.10) |
| AC 02.2 | Enrollment start date may be in the past (supported)   |

---

### US 03 — LA Updated: Add New Associated Course (Update Order)

A CM creates an update order on an existing product, adds a new course that was not in the
original product, and selects an effective date.

| ID      | Business Rule                                                                                                                                                                                                                                  |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AC 03.1 | Adding a new course (not previously in product) creates a new LA with start date = effective date                                                                                                                                              |
| AC 03.2 | Effective date must be ≥ product start date; if not, system blocks submission with error: EN: "The selected effective date is earlier than the product start date." / JP: "選択された適用開始日は、商品の開始日以降の日付を選択してください。" |
| AC 03.3 | Effective date may be in the past (past date ≥ product start date) — **newly supported by PBT-1859**                                                                                                                                           |
| AC 03.4 | Effective date = today is allowed                                                                                                                                                                                                              |
| AC 03.5 | Effective date = future is allowed                                                                                                                                                                                                             |
| AC 03.6 | Existing LAs for other courses on the same product are NOT changed                                                                                                                                                                             |
| AC 03.7 | A class may be assigned for the new course; class_member created with start date = effective date                                                                                                                                              |

---

### US 04 — LA Updated: Change Associated Course (Update Order)

A CM creates an update order and changes an existing course (replaces it).

| ID      | Business Rule                                                                   |
| ------- | ------------------------------------------------------------------------------- |
| AC 04.1 | Old course LA: end date updated = effective date                                |
| AC 04.2 | New course LA: created with start date = effective date                         |
| AC 04.3 | Effective date = start date: old LA closed from start, new LA starts from start |
| AC 04.4 | Effective date = future: both LAs co-exist until effective date                 |

---

### US 05 — LA Updated: Update Slot (Update Order)

A CM creates an update order to increase or decrease the slot/week or purchased slot of a product.

| ID      | Business Rule                                                     |
| ------- | ----------------------------------------------------------------- |
| AC 05.1 | Purchased slot is updated on the LA                               |
| AC 05.2 | LA duration (start & end date) remains unchanged                  |
| AC 05.3 | Total session count is recalculated                               |
| AC 05.4 | Lesson allocation is updated following the lesson allocated rules |
| AC 05.5 | No student session is auto-created on slot update                 |
| AC 05.6 | Effective date may be in the past, today, or future               |

---

### US 06 — LA Updated: Cancel Order (Cancel Product)

A CM creates an update order to cancel an existing product.

| ID      | Business Rule                                                                                |
| ------- | -------------------------------------------------------------------------------------------- |
| AC 06.1 | Product type = Schedule or Frequency: LA end date updated = effective date (cancel date)     |
| AC 06.2 | Product type = Slot-Based or One-Time: LA is deleted                                         |
| AC 06.3 | Student is removed from lessons outside the new LA duration                                  |
| AC 06.4 | Class member end date updated = effective date (for group lessons)                           |
| AC 06.5 | Completed and cancelled lessons in the past remain visible                                   |
| AC 06.6 | Effective date may be in the past (past-date cancel is supported for Schedule and Frequency) |

---

### US 07 — LA Deleted or Reverted: Void Order

A CM voids an existing order from the billing tab.

| ID      | Business Rule                                                                                                                     |
| ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| AC 07.1 | Void new order: LA is deleted entirely                                                                                            |
| AC 07.2 | Void update order (slot change): LA slot reverts to previous value                                                                |
| AC 07.3 | Void update order (course change with effective date = start): old LA restored; new LA deleted                                    |
| AC 07.4 | Void update order (course change with effective date > start): new LA deleted; old LA end date restored                           |
| AC 07.5 | Void update order (add new associated course, future effective date): added course LA deleted                                     |
| AC 07.6 | Void update order (add new associated course, past effective date): added course LA deleted; original LA unchanged — **PBT-1859** |
| AC 07.7 | Void cancel order: LA restored to previous state                                                                                  |

---

### US 08 — LA Updated via Withdrawal Application

A CM submits a withdrawal application for a student.

| ID      | Business Rule                                                                                                       |
| ------- | ------------------------------------------------------------------------------------------------------------------- |
| AC 08.1 | Last attendance day > current date: LA end date updated = effective date; student removed from future lessons       |
| AC 08.2 | Last attendance day < current date: LA end date updated = effective date; student removed from lessons out of range |
| AC 08.3 | Lesson report of removed student is hidden                                                                          |
| AC 08.4 | Lesson allocation updated (Lesson Allocated, Status, Report History)                                                |
| AC 08.5 | Cancel withdrawal: LA reverted to original state                                                                    |

---

### US 09 — LA Updated via LOA Application

A CM submits a LOA (Leave of Absence) application.

| ID      | Business Rule                                                                                                       |
| ------- | ------------------------------------------------------------------------------------------------------------------- |
| AC 09.1 | Last attendance day > current date: LA end date updated = effective date; student removed from future lessons       |
| AC 09.2 | Last attendance day < current date: LA end date updated = effective date; student removed from lessons out of range |
| AC 09.3 | Cancel LOA: LA reverted to original state                                                                           |
| AC 09.4 | Resume LOA: new LA created from resume date                                                                         |
| AC 09.5 | Cancel resume LOA: new LA from resume date is deleted                                                               |

---

### US 10 — Special Cases

| ID       | Business Rule                                                                                        |
| -------- | ---------------------------------------------------------------------------------------------------- |
| AC 10.1  | Missing Lesson Allocation Week (LAW): LA created but total session count depends on LAW availability |
| AC 10.2  | Missing Academic Calendar: LA created; session count calculation may be affected                     |
| AC 10.3  | LA duration falls outside any defined week order: LA created; session count = 0                      |
| AC 10.4  | Multiple product offerings for same student: separate LAs created per product                        |
| AC 10.5  | Multiple courses per product: separate LA per course (all with Require Allocation = True)            |
| AC 10.6  | Multiple LAs with same course and duration: allowed; counted independently                           |
| AC 10.7  | Require Allocation = False: no LA created; LA not updated when slot changes                          |
| AC 10.8  | Product type = Monthly: LA is NOT created                                                            |
| AC 10.9  | Changes from class assigned via order group: class member updated accordingly                        |
| AC 10.10 | Cancel future class from order group: class member end date updated                                  |
| AC 10.11 | Import order via CSV: LA created with same rules as manual order                                     |

---

## Business Rules (Extracted)

| #   | AC       | Business Rule                                                                                        |
| --- | -------- | ---------------------------------------------------------------------------------------------------- |
| 1   | AC 01.1  | LA created per course where Require Allocation = True on product submission                          |
| 2   | AC 01.2  | LA start date = order start date                                                                     |
| 3   | AC 01.3  | LA end date = order end date                                                                         |
| 4   | AC 01.4  | LA teaching method = course master's teaching method                                                 |
| 5   | AC 01.5  | LA type = course type of the course                                                                  |
| 6   | AC 01.6  | LA product detail = course + package type                                                            |
| 7   | AC 01.7  | Purchased slot depends on package type (session/week, slot/week, slots from master, order slots)     |
| 8   | AC 01.8  | Total session count = 0 at LA creation; no auto student session                                      |
| 9   | AC 01.9  | LA visible in Contact → Course tab                                                                   |
| 10  | AC 01.10 | Class assigned → class_member created with LA duration                                               |
| 11  | AC 01.11 | Past start date is allowed for order-based LA creation (all product types)                           |
| 12  | AC 02.2  | Enrollment past start date is supported                                                              |
| 13  | AC 03.1  | Adding new course (update order) creates new LA with start = effective date                          |
| 14  | AC 03.2  | Effective date must be ≥ product start date; else blocked with EN+JP error                           |
| 15  | AC 03.3  | Past effective date allowed for add-course update order (≥ product start date)                       |
| 16  | AC 03.6  | Existing LAs unchanged when a new course is added via update order                                   |
| 17  | AC 04.1  | Change course: old LA end date = effective date                                                      |
| 18  | AC 04.2  | Change course: new LA start date = effective date                                                    |
| 19  | AC 05.1  | Update slot: purchased slot updated on LA                                                            |
| 20  | AC 05.2  | Update slot: LA duration unchanged                                                                   |
| 21  | AC 05.3  | Update slot: total session count recalculated                                                        |
| 22  | AC 05.5  | Update slot: no student session auto-created                                                         |
| 23  | AC 05.6  | Update slot: effective date may be past, today, or future                                            |
| 24  | AC 06.1  | Cancel Schedule/Frequency: LA end date = cancel effective date                                       |
| 25  | AC 06.2  | Cancel Slot-Based/One-Time: LA deleted                                                               |
| 26  | AC 06.3  | Cancel: student removed from lessons outside new LA duration                                         |
| 27  | AC 06.5  | Cancel: completed/cancelled past lessons remain visible                                              |
| 28  | AC 06.6  | Cancel with past effective date supported for Schedule and Frequency                                 |
| 29  | AC 07.1  | Void new order → LA deleted                                                                          |
| 30  | AC 07.2  | Void update (slot) → slot reverted                                                                   |
| 31  | AC 07.6  | Void update (add course past date) → added LA deleted; original unchanged                            |
| 32  | AC 08.1  | Withdrawal (last attendance > today): LA end date updated; student removed from future lessons       |
| 33  | AC 08.2  | Withdrawal (last attendance < today): LA end date updated; student removed from out-of-range lessons |
| 34  | AC 09.1  | LOA (last attendance > today): same as withdrawal                                                    |
| 35  | AC 09.4  | Resume LOA: new LA created from resume date                                                          |
| 36  | AC 10.7  | Require Allocation = False: no LA created or updated                                                 |
| 37  | AC 10.8  | Monthly product: LA NOT created                                                                      |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| #   | Tag               | Source                           | AC      | Description                                                                                                |
| --- | ----------------- | -------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------- |
| 1   | [EXTENDED]        | TC 1775/1776 (future/today only) | AC 03.3 | PBT-1859 extends allowed effective date range to include past dates ≥ product start date                   |
| 2   | [REGRESSION RISK] | TC 1775/1776 preconditions       | AC 03.6 | Existing TCs do not explicitly assert existing LA unchanged; new past-date flow must not alter original LA |

### Missing in Requirements

| #   | Tag                | Source       | Description                                                                      |
| --- | ------------------ | ------------ | -------------------------------------------------------------------------------- |
| 1   | [MISSING BEHAVIOR] | Suite 280    | No TC covers cancel with past date for Slot-Based or One-Time product types      |
| 2   | [MISSING BEHAVIOR] | Suite 280    | No TC covers enrollment order with past start date                               |
| 3   | [MISSING BEHAVIOR] | Suite 280    | No TC covers update slot with explicit past/today/future effective date variants |
| 4   | [MISSING BEHAVIOR] | PBT-1859 PRD | No TC covers void of update order that added course with past date               |
| 5   | [MISSING BEHAVIOR] | PBT-1859 PRD | Boundary: effective date = product start date not covered                        |

### Assumptions Made

- Graduate flow LA impact is out of scope for this plan (no AC in suite 280; requires separate PM confirmation).
- "Update slot with past date" behavior = same purchased-slot/session-count update logic as current date; no LA duration change.
- Slot-Based and One-Time cancel always deletes LA (not end-date update), consistent with TC 9922/9923 patterns.

## Related Specs

- `input/specs/LT-92532: Riso - Create Update LA on UI` — LA creation via UI (non-order path); separate flow

## Related Test Cases

- `output/test-cases/lesson-management/student-session/lesson-allocation/` — all existing LA test case files
- `output/test-cases/lesson-management/student-session/class-assignment-student-course.md` — class assignment side effects

## QASE Coverage Gaps

- AC 03.3 — Add course with past effective date ≥ product start date (PBT-1859 happy path)
- AC 03.2 — Add course with effective date < product start date (blocked, error message)
- AC 03.1/03.2 — Boundary: effective date = product start date
- AC 07.6 — Void update order that added course with past date
- AC 06.2/06.6 — Cancel Slot-Based/One-Time with past effective date
- AC 02.2 — Enrollment with past start date
- AC 05.6 — Update slot with past / today / future effective date (3 variants)
