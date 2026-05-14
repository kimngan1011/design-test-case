# LT-96188: Add Student Classification to Event and Lesson Calendar

**ID:** https://manabie.atlassian.net/browse/LT-96188
**Status:** Ready for QA
**Analysis Date:** 2026-05-14
**Partner Scope:** Renseikai (label: Renseikai_Recovery)
**Priority:** Highest
**Epic Type:** Epic
**Related Ticket:** [PBT-2485](https://manabie.atlassian.net/browse/PBT-2485) — Add new field to Contact Object: Student Classification

---

## Summary

LT-96188 adds the `student_classification` field — a new Core picklist field being promoted from OOP (Renseikai, Withus Juku) to the Core package via PBT-2485 — to two display surfaces and four filter contexts on Salesforce. Staff can now see each student's classification status (enrolled/former enrolled/inquiry/seasonal) directly in the Event Participant List and Lesson Calendar Student Session list, and can filter by this classification when searching for students in event popups and lesson detail.

---

## Acceptance Criteria

### REQ 01 — Show student_classification as basic student information

#### AC 01.1 — Event Participant List Column

Show `student_classification` as one of the basic student information columns in the **Event Participant List** (SF).

#### AC 01.2 — Lesson Calendar Student Session Column

Show `student_classification` as one of the basic student information columns in the **Lesson Calendar (Student Session)** list (SF).

---

### REQ 02 — Add student_classification filter (multi-select picklist, below Type filter)

#### AC 02.1 — Add Master Participant Popup (SF Event)

Add `student_classification` multi-select picklist filter to the **Add Master Participant** popup. Position: below the **Type** filter.

#### AC 02.2 — Assign to Event Popup (SF Event)

Add `student_classification` multi-select picklist filter to the **Assign to Event** popup. Position: below the **Type** filter.

> ⚠️ **Two surfaces to cover (clarified 2026-05-14):**
>
> 1. **Event Master → Assign to Event** popup
> 2. **Activity Event → Assign to Event** popup
>
> Both surfaces share the same Assign to Event popup but are accessed from different parent pages. Both must be tested.

#### AC 02.3 — Lesson Calendar Student List Filter (Left Panel, SF)

Add `student_classification` multi-select picklist filter to the **SF Lesson Calendar Student List Filter** (left panel). Position: below the **Type** filter.

#### AC 02.4 — Add Student Filter in Lesson Detail (SF)

Add `student_classification` multi-select picklist filter to the **Add Student Filter in Lesson Detail** (SF). Position: below the **Type** filter.

---

### REQ 03 — [FROM COMMENT] Additional surfaces (Maria Nawatani, 2026-04-17)

> ⚠️ These requirements appear in a Jira comment only — NOT in the formal AC. **Confirmed in scope for test cases** (dev missed; Q1 answered 2026-05-14). Implementation will be handled separately by dev.

#### AC 03.1 — Collect Event Attendance Page

Add `student_classification` column to the **Collect Event Attendance** page.

#### AC 03.2 — CSV (Download Participants)

Add `student_classification` column to the **CSV export** from Download Participants.

---

## Student Classification Field Reference

From PBT-2485 and Confluence ([Student Classification Field PRD](https://manabie.atlassian.net/wiki/spaces/CA/pages/2347139073)):

| API Value         | Japanese Label | English Label   | Description                        |
| ----------------- | -------------- | --------------- | ---------------------------------- |
| `enrolled`        | 在籍生         | Enrolled        | Currently enrolled student         |
| `former_enrolled` | 元在籍生       | Former Enrolled | Former enrolled (no longer active) |
| `inquiry`         | 問合生         | Inquiry         | Prospect/inquiry student           |
| `seasonal`        | 季節講習生     | Seasonal        | Seasonal course student only       |

- **Default on creation:** 問合生 (inquiry)
- **Update mechanism:** Core Flow (auto-update based on enrollment lifecycle) or API
- **PBT-2485 status:** In Development — field may not yet be fully deployed in all environments

---

## Business Rules (Extracted)

| #   | AC Ref            | Business Rule                                                                                                                       | Field                         | Field Behavior        | Platform |
| --- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | --------------------- | -------- |
| 1   | AC 01.1           | student_classification displayed in Event Participant List as a read-only column                                                    | student_classification column | read-only display     | SF       |
| 2   | AC 01.1           | When student_classification is null, the column displays **blank** (empty cell — not '-' or 'N/A')                                  | student_classification column | null → blank          | SF       |
| 3   | AC 01.2           | student_classification displayed in Lesson Calendar Student Session list as a read-only column                                      | student_classification column | read-only display     | SF       |
| 4   | AC 01.2           | When student_classification is null, the column displays **blank** (empty cell — not '-' or 'N/A')                                  | student_classification column | null → blank          | SF       |
| 5   | AC 02.1           | student_classification multi-select picklist filter added to Add Master Participant popup, below Type filter                        | Student Classification filter | multi-select picklist | SF       |
| 6   | AC 02.1           | Filter returns students matching ANY selected value — **OR logic confirmed** (Q2)                                                   | Student Classification filter | multi-select OR logic | SF       |
| 7   | AC 02.1           | Filter default state: empty (no selection = show all students)                                                                      | Student Classification filter | empty = unfiltered    | SF       |
| 8a  | AC 02.2           | student_classification multi-select picklist filter added to **Event Master → Assign to Event** popup, below Type filter            | Student Classification filter | multi-select picklist | SF       |
| 8b  | AC 02.2           | student_classification multi-select picklist filter added to **Activity Event → Assign to Event** popup, below Type filter          | Student Classification filter | multi-select picklist | SF       |
| 9   | AC 02.3           | student_classification multi-select picklist filter added to SF Lesson Calendar Student List left panel filter, below Type filter   | Student Classification filter | multi-select picklist | SF       |
| 10  | AC 02.4           | student_classification multi-select picklist filter added to Add Student Filter in Lesson Detail, below Type filter                 | Student Classification filter | multi-select picklist | SF       |
| 11  | AC 03.1 [COMMENT] | student_classification column added to Collect Event Attendance page — **in scope for test cases** (dev missed, Q1)                 | student_classification column | read-only display     | SF       |
| 12  | AC 03.2 [COMMENT] | student_classification column included in CSV Download Participants — **in scope for test cases** (dev missed, Q1)                  | student_classification in CSV | exported column       | SF       |
| 13  | AC 02.x           | Filter picklist values are sourced **dynamically** from the `student_classification` picklist field definition — not hardcoded (Q3) | filter options                | dynamic picklist      | SF       |
| 14  | AC 02.3, 02.4     | **Type filter already exists** in all 4 filter surfaces including Lesson Calendar left panel and Add Student in Lesson Detail (Q5)  | filter placement              | below Type filter     | SF       |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

_No conflicts found._ This feature is purely additive — adding a new column and filter to existing surfaces. No existing rule states "student_classification must not appear" or defines contradicting behavior.

---

### Resolved During Analysis (2026-05-14)

| #   | Tag                  | Finding                                                                 | Resolution                                                |
| --- | -------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------- |
| 1   | [UNDOCUMENTED IN AC] | Collect Event Attendance + CSV Download not in formal AC (comment only) | ✅ **In scope for test cases** — dev missed (Q1)          |
| 2   | [MISSING BEHAVIOR]   | Null/blank display not defined                                          | ✅ **Blank** (empty cell) (Q4)                            |
| 3   | [MISSING BEHAVIOR]   | Multi-select filter logic (OR vs AND) not defined                       | ✅ **OR logic** (Q2)                                      |
| 4   | [MISSING BEHAVIOR]   | Filter picklist values source not specified                             | ✅ **Dynamic from picklist field** (Q3)                   |
| 5   | [MISSING BEHAVIOR]   | Type filter existence in AC 02.3/02.4 contexts unconfirmed              | ✅ **Type filter already exists** in all 4 surfaces (Q5)  |
| 6   | [ROLE GAP]           | Teacher access restriction for new filter in AC 02.3/02.4               | ✅ **BO Filter out of scope**; no restriction for SF (Q7) |

### Open Gaps (Not Fully Resolved)

| #   | Tag                | Source                                                    | Description                                                                                                             |
| --- | ------------------ | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 7   | [MISSING BEHAVIOR] | temp/current_system_inventory.json                        | Lesson Calendar Student List Filter persistence/reset behavior across navigation — undefined; test both behaviors       |
| 8   | [MISSING BEHAVIOR] | temp/business_rules.json — Rule #13                       | Column header label: English "Student Classification" vs Japanese "生徒区分" — use label as displayed in implementation |
| 9   | [MISSING BEHAVIOR] | temp/raw_requirement.json — PBT-2485 still In Development | **Precondition:** PBT-2485 must be deployed and field populated before testing — document as test precondition          |
| 10  | [REGRESSION RISK]  | E2E-06 Steps 3-4                                          | Add Master Participant + Assign to Event popups layout changes — **create new cases** for classification (Q6)           |
| 11  | [REGRESSION RISK]  | E2E-07 Step 7                                             | CSV Download column structure changes — covered under REQ 03 test cases                                                 |

---

### Lesson-Learned Risks

_No relevant historical incidents found._ Both entries in the lesson-learned files were assessed:

| Incident                                            | Date       | Reason Not Applicable                                                                                           |
| --------------------------------------------------- | ---------- | --------------------------------------------------------------------------------------------------------------- |
| Aso — Duplicate Student Sessions (bulk+auto assign) | 2026-04-13 | Different entity (student_session) + operation (create). LT-96188 is display+filter only — no session creation. |
| Nichibei — Missing LA → Points Not Deducted         | 2026-03-04 | Different entity (lesson_allocation) + operation (SPO sync). No financial/allocation logic in LT-96188.         |

---

### E2E Scenario Impact

| Scenario | Title                                                 | Impact                                                                                                                                              | Action                            |
| -------- | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| E2E-06   | Event Master — Create, Assign Participants & Calendar | Steps 3-4 (Add Master Participants / Target Segments) and Step 8 (Assign to Event): new filter appears in popups; participant list shows new column | UPDATE                            |
| E2E-07   | Event Master — Booking, Mobile Interaction & Status   | Step 7 (Download Participant List): CSV may include new column if AC 03.2 confirmed                                                                 | UPDATE (conditional on Q1 answer) |

---

### Confirmed Assumptions (2026-05-14)

- **PBT-2485 dependency:** The `student_classification` field must be deployed (PBT-2485) before this feature can be tested. If not deployed, all columns will show blank. This is a **testing precondition**.
- **Type filter confirmed:** The Type filter already exists in all 4 filter surfaces including SF Lesson Calendar left panel and Add Student Filter in Lesson Detail.
- **OR logic confirmed:** Multi-select filter returns students matching ANY selected value.
- **Dynamic picklist values:** Filter dropdown values are sourced from the `student_classification` picklist field definition — not hardcoded to 4 values.

---

## Clarification Questions & Answers (2026-05-14)

> All questions answered by QA team on 2026-05-14. **No Jira post required.**

| #   | Tag                  | Question                                                                | Answer                                                                           |
| --- | -------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Q1  | [UNDOCUMENTED IN AC] | Are Collect Event Attendance + CSV Download in scope for LT-96188?      | **Dev missed — create test cases; dev will handle implementation separately**    |
| Q2  | [MISSING BEHAVIOR]   | Multi-select filter: OR or AND logic?                                   | **OR logic**                                                                     |
| Q3  | [MISSING BEHAVIOR]   | Filter dropdown values: static 4 values or dynamic from picklist field? | **Dynamic — get values from `student_classification` picklist field**            |
| Q4  | [MISSING BEHAVIOR]   | Null classification display?                                            | **Blank** (empty cell)                                                           |
| Q5  | [MISSING BEHAVIOR]   | Does Type filter already exist in all 4 filter surfaces?                | **Yes — Type filter already exists**                                             |
| Q6  | [REGRESSION RISK]    | Do existing test cases assert exact filter count in popups?             | **Create new cases for classification filter; no existing case update required** |
| Q7  | [ROLE GAP]           | Restriction on teachers using the new filter?                           | **BO Filter is out of scope; no restriction for SF surfaces**                    |

---

## Related Specs

- `input/specs/event-master-form-latest.md` — consolidated Event Master form spec including participant settings, Add Master Participant, Assign to Event contexts
- `input/specs/[koyu] Core  524 - Cancel Booked Event (App).md` — documents Event Participant List columns and CSV download structure

## Related Test Cases

- `output/test-coverages/LT-94674-cancel-booked-event-update.md` — covers Participant List columns; may need student_classification column assertion
- `output/test-cases/lesson-management/event/` — event test cases covering participant flows
- `input/e2e-scenario/e2e-scenarios.md` — E2E-06 (event participant flow) and E2E-07 (CSV download) need updating

## QASE Coverage Gaps

- AC 01.1 — No existing test case verifies student_classification column in Event Participant List
- AC 01.2 — No existing test case verifies student_classification column in Lesson Calendar Student Session
- AC 02.1 — No existing test case verifies student_classification filter in Add Master Participant popup
- AC 02.2a — No existing test case verifies student_classification filter in **Event Master → Assign to Event** popup
- AC 02.2b — No existing test case verifies student_classification filter in **Activity Event → Assign to Event** popup
- AC 02.3 — No existing test case verifies student_classification filter in Lesson Calendar left panel
- AC 02.4 — No existing test case verifies student_classification filter in Add Student Filter (Lesson Detail)
- AC 03.1 — No test for student_classification column in Collect Event Attendance page (dev missed; in scope for test cases)
- AC 03.2 — No test for student_classification column in CSV Download Participants (dev missed; in scope for test cases)
- Null/blank display — **Blank** confirmed; test case needed for null classification display
- OR logic — Multi-select filter with 2+ values returning union of matches; test case needed
- Dynamic picklist values — Filter options loaded from picklist field definition; test case needed
