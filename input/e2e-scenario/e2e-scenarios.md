# Manabie Scheduling — E2E Scenarios

> **Purpose:** Cross-feature end-to-end scenarios covering the full user workflow across SF → BO → Mobile App. Each scenario integrates multiple features to maximize coverage per test.
> **Last updated:** 2026-04-07
> **Coverage:** 4,191 test cases across Lesson Management, Calendar, Event, Customization, and Master Data.

---

## How to Read This Document

Each E2E scenario is a numbered sequence of user actions across platforms:

- **[SF]** = Salesforce (staff actions)
- **[BO]** = Back Office (teacher/CM actions)
- **[Mobile]** = Learner App (student/parent actions)
- **[System]** = Automated/background processes

**Features covered** are listed after each scenario, mapping to Qase suite areas.

### Core Verification Principle

> **Every E2E scenario that involves lessons MUST include these verification steps, regardless of how the lesson/student/teacher is created:**
>
> 1. **Create Lesson** — The scenario must include lesson creation (or verify the lesson exists)
> 2. **Assign Students** — Students must be assigned to the lesson (via add student, class auto-assignment, import, or reallocation)
> 3. **Assign Teachers** — Teachers must be assigned to the lesson
> 4. **Verify on Mobile App** — The student/parent must verify the lesson, or report on the Learner App
>
> These four features — Lesson CRUD, Student Session, Lesson Teacher, and Mobile App — are the **most critical features** in Manabie Scheduling. Skipping any of them in an E2E scenario means the scenario is incomplete.

---

## E2E-01: Lesson Lifecycle — Create, Teach, Report, View

> **Theme:** The core happy path from lesson creation to student viewing.

| #   | Platform | Action                                                                                                                                              |
| --- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates a **one-time group lesson** on the Lesson List (date, time, name, location, AY, course, class, teaching method=Group, medium=Offline) |
| 2   | [SF]     | Staff views the lesson on **SF Calendar** (verify it appears on the correct date/time)                                                              |
| 3   | [SF]     | Staff **assigns a teacher** to the lesson on Lesson Detail                                                                                          |
| 4   | [SF]     | Staff **adds students** to the lesson on Lesson Detail (verify LA Require Allocation = True filter)                                                 |
| 5   | [System] | Verify **Lesson Report** auto-created with Draft status and Lesson Report Details per student                                                       |
| 6   | [System] | Verify **Lesson Allocation** updated: Lesson Allocated incremented, status updated                                                                  |
| 7   | [SF]     | Staff changes lesson status from **Draft → Published**                                                                                              |
| 8   | [BO]     | Teacher logs in (CPU) → sees the lesson on **BO Calendar** (filtered by lesson teacher)                                                             |
| 9   | [BO]     | Teacher opens lesson detail on BO → **collects attendance** for each student                                                                        |
| 10  | [BO]     | Teacher **writes and submits lesson report** on BO Lesson Detail                                                                                    |
| 11  | [BO]     | Teacher **publishes the lesson report**                                                                                                             |
| 12  | [Mobile] | Student opens Learner App → sees the **Published lesson** in their schedule                                                                         |
| 13  | [Mobile] | Student views the **lesson report** published by teacher                                                                                            |
| 14  | [SF]     | Staff changes lesson status to **Completed**                                                                                                        |

**Features covered:**

- Lesson > Create on Lesson List (51 cases)
- Calendar > Lesson on SF Calendar (464 cases)
- Lesson Teacher > Assign in lesson detail (27 cases)
- Student Session > Assign by Add Student (70 cases)
- Lesson Allocation > LA tab (36 cases)
- Lesson Status > Change status (7 cases)
- Calendar on BO > Calendar View (67 cases)
- Lesson on BO > CM/PT Teacher > Lesson Mgmt (110 cases)
- Lesson on BO > CM/PT Teacher > Report BO (54 cases)
- Lesson Mobile > View lesson (6 cases)
- Lesson Mobile > Submit attendance (28 cases)

---

## E2E-02: Recurring Lesson — Create, Edit Chain, Delete, Calendar Drag

> **Theme:** Full recurring lesson lifecycle with calendar operations.

| #   | Platform | Action                                                                                                       |
| --- | -------- | ------------------------------------------------------------------------------------------------------------ |
| 1   | [SF]     | Staff creates a **weekly recurring lesson** (repeat every 1 week, end after 5 lessons, skip closed dates ON) |
| 2   | [System] | Verify 5 lessons created with incremented lesson codes; closed dates skipped                                 |
| 3   | [SF]     | Staff views all 5 lessons on **SF Calendar Week view**                                                       |
| 4   | [SF]     | Staff **edits lesson name** using "This and the following lessons" on the 2nd lesson                         |
| 5   | [System] | Verify lessons 2-5 updated; lesson 1 unchanged                                                               |
| 6   | [SF]     | Staff **assigns teacher** using "This and the following" on lesson 1                                         |
| 7   | [SF]     | Staff verifies **clashing alert** by assigning same teacher to an overlapping lesson                         |
| 8   | [SF]     | Staff **drags lesson 3** on SF Calendar to reschedule to a new time slot                                     |
| 9   | [SF]     | Staff **duplicates lesson 1** to create a new one-time lesson                                                |
| 10  | [SF]     | Staff **adds a lesson** to the existing schedule from Lesson Schedule Detail                                 |
| 11  | [SF]     | Staff **deletes lesson 5** from the chain                                                                    |
| 12  | [System] | Verify lesson report and student sessions deleted for lesson 5; LA updated                                   |
| 13  | [BO]     | Teacher views the remaining lessons on **BO Calendar**                                                       |
| 14  | [SF]     | Staff **bulk updates status** of all remaining lessons to Published                                          |

**Features covered:**

- Lesson > Create on Lesson List — Weekly recurrence (51 cases)
- Lesson > Edit lesson info — "This and following" (87 cases)
- Lesson Teacher > Clashing Alert (34 cases)
- Calendar SF > Drag & Drop (44 cases)
- Lesson > Duplicate lesson (32 cases)
- Lesson > Create in Lesson Schedule Detail (58 cases)
- Lesson > Delete lesson (9 cases)
- Lesson Status > Bulk update (5 cases)
- Calendar on BO > Lesson View (35 cases)

---

## E2E-03: Class-Based Student Auto-Assignment — Setup & Effective Date Logic

> **Theme:** Class member auto-assignment pipeline: class setup → student assignment → lesson creation → auto-mapping with effective date validation.

| #   | Platform | Action                                                                                                                                             |
| --- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates a **Class** under a Location Course                                                                                                  |
| 2   | [SF]     | Staff assigns **Student A** to Course → **Assign Class** with effective date = today                                                               |
| 3   | [SF]     | Staff assigns **Student B** to Course → **Bulk Assign Class** with effective date = next week                                                      |
| 4   | [SF]     | Staff creates a **group lesson** with the class assigned                                                                                           |
| 5   | [System] | **Run Master Queue** → Student A auto-assigned to the lesson (effective date ≤ lesson date); Student B NOT assigned (effective date > lesson date) |
| 6   | [SF]     | Staff creates a second lesson next week with the same class                                                                                        |
| 7   | [System] | Both Student A and Student B auto-assigned to lesson 2 (both effective dates ≤ lesson date)                                                        |
| 8   | [SF]     | Staff **changes Student A's class** from Class 1 to Class 2                                                                                        |
| 9   | [System] | Student A removed from future lessons in Class 1; assigned to lessons in Class 2                                                                   |

**Features covered:**

- Student Session > Class management > Student Course (36 cases)
- Student Session > Class management > Location Course (23 cases)
- Student Session > Class management > Change Course/Class (30 cases)
- Student Session > Class management > Change Location Course (7 cases)

---

## E2E-04: Class-Based Student Auto-Assignment — Import, Multiple Classes & Verification

> **Theme:** Import class members, assign multiple classes to a lesson, then verify publish → BO → Mobile lifecycle.

| #   | Platform | Action                                                                        |
| --- | -------- | ----------------------------------------------------------------------------- |
| 1   | [SF]     | Staff **imports class members** via CSV                                       |
| 2   | [SF]     | Staff verifies student sessions and lesson reports auto-created               |
| 3   | [SF]     | Staff views **LA detail** → sees updated Lesson Allocated count               |
| 4   | [SF]     | Staff assigns class to a lesson with **Multiple Classes** (Class 1 + Class 2) |
| 5   | [System] | Students from both classes auto-assigned                                      |
| 6   | [SF]     | Staff **assigns a teacher** to the lesson                                     |
| 7   | [SF]     | Staff **publishes** the lesson                                                |
| 8   | [BO]     | Teacher views the lesson with auto-assigned students on **BO Calendar**       |
| 9   | [Mobile] | Student A views the lesson on **Learner App** schedule                        |

**Features covered:**

- Student Session > Class management > LA Detail (11 cases)
- Student Session > Class management > Import (3 cases)
- Student Session > Class management > Multiple Classes (8 cases)
- Calendar SF > Multiple Classes (8 cases)
- Lesson Teacher > Assign in lesson detail (27 cases)
- Lesson Mobile > View lesson (6 cases)

---

## E2E-05: Online Lesson with Zoom

> **Theme:** Zoom-integrated lesson: setup, student links, calendar sync.

| #   | Platform | Action                                                                      |
| --- | -------- | --------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates a **recurring weekly lesson** with Teaching Medium = **Zoom** |
| 2   | [System] | **Single Zoom link** auto-created; Zoom Owner = assigned teacher            |
| 3   | [SF]     | Staff verifies Zoom links on Lesson Detail                                  |
| 4   | [SF]     | Staff **adds students** → students become Zoom Participants                 |
| 5   | [System] | Verify Zoom Calendar event created with start/end from lesson chain         |
| 6   | [SF]     | Staff **edits Zoom Owner** on lesson 3 ("This and following")               |
| 7   | [System] | Lessons 3-5 get new Zoom links; lessons 1-2 keep old Zoom links             |
| 8   | [SF]     | Staff **edits lesson date/time** on lesson 2 ("Only this")                  |
| 9   | [System] | New Zoom entry created for lesson 2                                         |
| 10  | [BO]     | Teacher opens lesson → verifies **Zoom link** is joinable                   |
| 11  | [BO]     | Teacher **generates Zoom link manually** for a lesson without one           |
| 12  | [BO]     | Teacher views **Zoom clashing alert** for overlapping Zoom meetings         |
| 13  | [Mobile] | Student opens lesson → sees **Join Zoom** button                            |

**Features covered:**

- Lesson Zoom on BO > Setup Zoom Owner (27 cases)
- Lesson Zoom on BO > Verify UI/UX Zoom + Clashing (48 cases)
- Lesson Zoom on BO > Single Zoom > Create/Update/Delete/View (154 cases)
- Lesson Zoom on BO > Multiple Zoom > Create/Edit/Delete/View (187 cases)

---

## E2E-06: Event Master — Setup, Activity Event & Calendar

> **Theme:** Event Master creation → target segments → activity event → calendar visibility for assigned staff.

| #   | Platform | Action                                                                         |
| --- | -------- | ------------------------------------------------------------------------------ |
| 1   | [SF]     | Staff creates an **Event Master** with name, date, capacity                    |
| 2   | [SF]     | Staff adds **Target Segments**: Target Location + Target Grade + Target Course |
| 3   | [SF]     | Staff adds **Master Participants** based on target segments                    |
| 4   | [SF]     | Staff adds **Master Staff** to the event                                       |
| 5   | [SF]     | Staff creates an **Activity Event** from the Event Master                      |
| 6   | [SF]     | Staff verifies event appears on **SF Calendar**                                |
| 7   | [SF]     | Assigned staff sees the event on their **SF Calendar**                         |
| 8   | [SF]     | Staff **assigns students** to the event via "Assign to Event"                  |

**Features covered:**

- Event Master > Creating (15 cases)
- Event Master > Record details > Participant list > Target Segments (53 cases)
- Event Master > Record details > Master Participants (11 cases)
- Event Master > Record details > Master Staff (11 cases)
- Event Master > Activity Event > Creating (22 cases)
- Calendar SF > Events (51 cases)
- Event Master > SF Calendar > Show Events for Assigned Staff (7 cases)

---

## E2E-07: Event Master — Booking, Mobile Interaction & Status

> **Theme:** Internal booking → learner mobile interaction → status management → BO calendar visibility.

| #   | Platform | Action                                                      |
| --- | -------- | ----------------------------------------------------------- |
| 1   | [SF]     | Staff uses **Internal Booking** → Reserve by target segment |
| 2   | [System] | Notification sent to booked participants                    |
| 3   | [Mobile] | Student sees **Activity Card** on Learner App               |
| 4   | [Mobile] | Student **Accepts** the event invitation                    |
| 5   | [SF]     | Staff views updated response/attendance on Activity Event   |
| 6   | [SF]     | Staff edits **event status** (status change)                |
| 7   | [SF]     | Staff **downloads participant list**                        |
| 8   | [BO]     | Teacher/CM views the event on **BO Calendar**               |

**Features covered:**

- Event Master > Booking System > Internal Booking (93 cases)
- Event Master > Activity Event > Status changes (7 cases)
- Event Master > Activity Event > Learner App Card (14 cases)
- Calendar BO > Events (51 cases)

---

## E2E-08: External Booking & Koyu Auto-Create Application

> **Theme:** External event booking flow with Koyu-specific auto-application.

| #   | Platform   | Action                                                                                            |
| --- | ---------- | ------------------------------------------------------------------------------------------------- |
| 1   | [SF]       | Staff creates an **Event Master** with external booking enabled                                   |
| 2   | [SF]       | Staff configures **External Booking Link**                                                        |
| 3   | [SF]       | Staff sets up **pricing** for the event                                                           |
| 4   | [External] | External user opens booking link → registers with **existing email**                              |
| 5   | [System]   | **Koyu Auto Create Application** triggered: auto-generates application record for the participant |
| 6   | [External] | External user opens booking link → registers with **new email**                                   |
| 7   | [System]   | New contact created; auto-application generated                                                   |
| 8   | [SF]       | Staff views all bookings and auto-created applications                                            |
| 9   | [SF]       | Staff **cancels a booked event** (Koyu Cancel Booked Event)                                       |
| 10  | [System]   | Cancellation record created with proper status                                                    |
| 11  | [SF]       | Staff **updates the cancellation** details                                                        |
| 12  | [SF]       | Staff manages event in **Draft Status** (Koyu Draft Status)                                       |

**Features covered:**

- Event Master > Booking System > External Booking (108 cases)
- Event Master > Booking System > External link (4 cases)
- Event Master > Booking System > Koyu Auto Create Application (51 cases)
- Koyu Cancel Booked Event (68 cases)
- Update Cancel Booked Event (65 cases)
- Koyu Draft Status (19 cases)
- Event Master > Contact page > Available event list (8 cases)
- Learner App - Event (8 cases)

---

## E2E-09: Lesson Allocation — New Order, Change Course & Void

> **Theme:** LA lifecycle: new order → LA auto-created → change course → void; verifying SPO and LA state transitions.

| #   | Platform | Action                                                                           |
| --- | -------- | -------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates a **new Order Group (OG)** for a student with a course             |
| 2   | [System] | **SPO** created → **LA** auto-created (Require Allocation = True)                |
| 3   | [SF]     | Staff verifies LA on the **LA tab** (duration, status, allocated count)          |
| 4   | [SF]     | Staff assigns student to a lesson → verify LA updated                            |
| 5   | [SF]     | Staff creates a **new OG to change course** (effective date = start date)        |
| 6   | [System] | Old SPO soft-deleted → Old LA deleted → New SPO created → New LA with new course |
| 7   | [SF]     | Staff verifies student removed from old course lessons; LA reflects new course   |
| 8   | [SF]     | Staff **voids the course change**                                                |
| 9   | [System] | Old SPO restored → Old LA re-created; New SPO deleted → New LA deleted           |
| 10  | [SF]     | Staff creates an **enrollment order** → LA created                               |

**Features covered:**

- Lesson Allocation > Create LA New Order (8 cases)
- Lesson Allocation > Enrollment (3 cases)
- Lesson Allocation > Change Course (2 cases)
- Lesson Allocation > Cancel (10 cases)
- Lesson Allocation > Void (10 cases)
- Lesson Allocation > LA tab (36 cases)

---

## E2E-10: Lesson Allocation — LOA, Add Course & Lesson Assignment

> **Theme:** LA through LOA and add-course orders, then lesson creation → teacher → publish → BO → Mobile.

| #   | Platform | Action                                                                                                             |
| --- | -------- | ------------------------------------------------------------------------------------------------------------------ |
| 1   | [SF]     | Staff **cancels the LOA order** → LA deleted                                                                       |
| 2   | [SF]     | Staff processes **Resume LOA** → LA created                                                                        |
| 3   | [SF]     | Staff **cancels resume LOA** → LA deleted                                                                          |
| 4   | [SF]     | Staff creates OG to **add more course** → additional LA created                                                    |
| 5   | [SF]     | Staff **voids add course** → additional LA deleted                                                                 |
| 6   | [SF]     | Staff creates a **lesson** for the course and **assigns the student** → verifies LA Lesson Allocated count updates |
| 7   | [SF]     | Staff **assigns a teacher** to the lesson                                                                          |
| 8   | [SF]     | Staff **publishes** the lesson                                                                                     |
| 9   | [BO]     | Teacher views the lesson on **BO Calendar**                                                                        |
| 10  | [Mobile] | Student views the lesson on **Learner App** schedule                                                               |

**Features covered:**

- Lesson Allocation > Add Course (5 cases)
- Lesson Allocation > Withdrawal (6 cases)
- Lesson Allocation > LOA (6 cases)
- Lesson Allocation > Special Cases (11 cases)
- Lesson Allocation > Reprocess (4 cases)
- Lesson Teacher > Assign in lesson detail (27 cases)
- Lesson Mobile > View lesson (6 cases)

---

## E2E-11: Point Consumption (Nichibei) — Priority Chain & Edge Cases

> **Theme:** Point consumption priority logic: matching course → general course → invalid duration → no Point LA edge cases.

| #   | Platform | Action                                                                                                                 |
| --- | -------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff verifies **Course Categories** with Point Consumption values (e.g., Category 1 = 10pts, Category 2 = 30pts)      |
| 2   | [SF]     | Staff verifies student has multiple **LAs** with different Priority flags and durations                                |
| 3   | [SF]     | Staff creates a lesson with a **matching course** and assigns the student                                              |
| 4   | [System] | Points consumed from LA following priority chain: Duration → Priority+Matching → Priority+General → Matching → General |
| 5   | [SF]     | Verify LA's Consumed Points updated, Remaining Points decreased                                                        |
| 6   | [SF]     | Staff creates a lesson with a **general course** (General Flag = True) and assigns student                             |
| 7   | [System] | Points consumed from Priority+General LA                                                                               |
| 8   | [SF]     | Staff creates a lesson where student's LA duration is **invalid** but Point LA exists                                  |
| 9   | [System] | Assignment allowed; points calculated from valid Point LA                                                              |
| 10  | [SF]     | Staff creates a lesson where student's LA duration is valid but **no Point LA** exists                                 |
| 11  | [System] | Error message or skip behavior                                                                                         |

**Features covered:**

- Customization > Nichibei > Point Consumption (145 cases)
- Customization > Nichibei > Lesson Syllabus (24 cases)

---

## E2E-12: Point Consumption (Nichibei) — Publish, Reporting & Reallocation

> **Theme:** Publish lesson with point-consuming students, verify reports and LA Dashboard, then reallocation and trial lesson.

| #   | Platform | Action                                                                                                                  |
| --- | -------- | ----------------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff **assigns a teacher** to the lesson                                                                               |
| 2   | [SF]     | Staff **publishes** the lesson                                                                                          |
| 3   | [BO]     | Teacher views the lesson on **BO Calendar** and sees assigned students with point-consuming LA                          |
| 4   | [Mobile] | Student views the lesson on **Learner App** schedule                                                                    |
| 5   | [SF]     | Staff views **Point Consumption Report**                                                                                |
| 6   | [SF]     | Staff verifies **LA Dashboard** with remaining points                                                                   |
| 7   | [SF]     | Staff **reallocates** student to another lesson → student session moved; **no point recalculation** (session-move only) |
| 8   | [SF]     | Staff manages **Trial Lesson** assignment (trial student flow)                                                          |

**Features covered:**

- Customization > Nichibei > Reallocation (26 cases)
- Customization > Nichibei > Trial Lesson (20 cases)
- Customization > Nichibei > Limit Teacher (6 cases)
- SF Report > LA Dashboard (7 cases)
- SF Report > Point Consumption (6 cases)
- Lesson Teacher > Assign in lesson detail (27 cases)
- Lesson Mobile > View lesson (6 cases)

---

## E2E-13: Aver Lesson Report & Subject Flow

> **Theme:** Aver-customized lesson report: create, fill, correct, view on mobile.

| #   | Platform | Action                                                                                                     |
| --- | -------- | ---------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates a lesson with **Aver-specific course** (with subject and test prep settings)                 |
| 2   | [SF]     | Staff assigns teacher and students                                                                         |
| 3   | [SF]     | Staff publishes the lesson                                                                                 |
| 4   | [BO]     | Teacher opens lesson → fills in **Aver Lesson Report** (extended fields including subject, test prep data) |
| 5   | [BO]     | Teacher **submits** the lesson report                                                                      |
| 6   | [BO]     | Teacher realizes a mistake → uses **Lesson Report Correction** to update                                   |
| 7   | [System] | Correction record created; original report preserved                                                       |
| 8   | [BO]     | Teacher **publishes corrected report**                                                                     |
| 9   | [Mobile] | Student views the **corrected lesson report** on Learner App                                               |
| 10  | [SF]     | Staff verifies **Risk Flag Report** based on student performance                                           |
| 11  | [BO]     | Verify **permission rules**: specific roles can access report vs. not                                      |

**Features covered:**

- Customization > Aver > Lesson Report (203 cases)
- Customization > Aver > Lesson Report correct (178 cases)
- Customization > Aver > Test prep/Subject (24 cases)
- Customization > Aver > Permission (9 cases)
- SF Report > Risk Flag Report (5 cases)

---

## E2E-14: Aso Curriculum & Syllabus with Student Groups

> **Theme:** Aso-specific: syllabus setup, student groups, class enforcement, lesson survey.

| #   | Platform | Action                                                                            |
| --- | -------- | --------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates a **Student Group** and assigns members (filtered by location)      |
| 2   | [SF]     | Staff assigns **Student Group Staff Association**                                 |
| 3   | [SF]     | Staff uses **Bulk Assign Class** from Student Group                               |
| 4   | [SF]     | Staff creates/imports **Curriculum** with linked courses and schedules            |
| 5   | [SF]     | Staff creates **Syllabus Master** with Syllabus Details (code + description)      |
| 6   | [SF]     | Staff creates lessons and verifies **"Make sure lessons have class"** enforcement |
| 7   | [SF]     | Staff creates a lesson linked to the syllabus                                     |
| 8   | [BO]     | Teacher opens lesson → completes **Lesson Survey** (Aso-specific)                 |
| 9   | [SF]     | Staff **assigns a teacher** to the lesson                                         |
| 10  | [SF]     | Staff **publishes** the lesson                                                    |
| 11  | [BO]     | Teacher views lesson with syllabus info on **BO Calendar**                        |
| 12  | [Mobile] | Student views the lesson on **Learner App** schedule                              |
| 13  | [SF]     | Staff views **curriculum progress** across students                               |
| 14  | [SF]     | Staff **imports Student Group Members** via CSV                                   |

**Features covered:**

- Customization > Aso > Student Group (41 cases)
- Customization > Aso > Curriculum & Syllabus (219 cases)
- Customization > Aso > Lesson Survey (12 cases)
- Customization > Aso > Make sure lessons have class (7 cases)
- Lesson Teacher > Assign in lesson detail (27 cases)
- Lesson Mobile > View lesson (6 cases)

---

## E2E-15: Academic Calendar & Closed Dates Impact

> **Theme:** Academic Calendar master data setup and its impact on lessons.

| #   | Platform | Action                                                                                       |
| --- | -------- | -------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates **Academic Calendar Master (ACM)** for 2026                                    |
| 2   | [SF]     | Staff creates **ACM per location** (ACM-2026-LOC1, ACM-2026-LOC2)                            |
| 3   | [SF]     | Staff adds **Closed Dates (ACI)** to the calendar                                            |
| 4   | [SF]     | Staff creates a **recurring lesson** with Skip Closed Date = ON at LOC1                      |
| 5   | [System] | Verify lessons are NOT created on closed dates                                               |
| 6   | [SF]     | Staff **edits a closed date** → lesson chain recalculated                                    |
| 7   | [SF]     | Staff **deletes a closed date** → new lesson created on that date                            |
| 8   | [SF]     | Staff creates a **Course Schedule** lesson → verify week order aligns with academic calendar |
| 9   | [SF]     | Staff **assigns teacher and students** to the recurring lesson                               |
| 10  | [SF]     | Staff **publishes** the lesson                                                               |
| 11  | [BO]     | Teacher views the recurring lessons (with skipped closed dates) on **BO Calendar**           |
| 12  | [Mobile] | Student sees only lessons on non-closed dates on **Learner App** schedule                    |
| 13  | [SF]     | Staff verifies **LA session count** calculation respects closed dates                        |
| 14  | [SF]     | Verify **permissions**: HQ Admin vs Centre Manager access to ACM                             |

**Features covered:**

- Master Data > Academic Calendar > CRUD ACM (16 cases)
- Master Data > Academic Calendar > CRUD ACI (10 cases)
- Master Data > Academic Calendar > Permissions (9 cases)
- Master Data > Academic Calendar > Work with AC location (57 cases)
- Lesson Teacher > Assign in lesson detail (27 cases)
- Student Session > Assign by Add Student (70 cases)
- Lesson Mobile > View lesson (6 cases)

---

## E2E-16: Teacher Access & Cross-Location Visibility

> **Theme:** Teacher assignment rules, access patterns, and cross-location scenarios.

| #   | Platform | Action                                                                                                       |
| --- | -------- | ------------------------------------------------------------------------------------------------------------ |
| 1   | [SF]     | Staff assigns **Teacher A** (Full-time, Location 1) to a lesson at Location 1                                |
| 2   | [SF]     | Staff assigns **Teacher B** (Part-time, Location 2) to the same lesson → triggers different location alert   |
| 3   | [SF]     | Staff verifies **teacher filter**: affiliation, location, working type, subject, working hours               |
| 4   | [SF]     | Staff assigns teacher to overlapping lesson → **Clashing Alert** in Confirm popup + Remark field             |
| 5   | [BO]     | Teacher A (CPU login) → sees lesson on **BO Calendar** (filtered by lesson teacher)                          |
| 6   | [BO]     | Centre Manager (SPU login) → sees ALL lessons at their location on **BO Calendar**                           |
| 7   | [SF]     | Staff removes Student B (from Teacher B's location) from the lesson                                          |
| 8   | [BO]     | Verify Teacher B **still has access** to the lesson (teacher assignment persists even after student removal) |
| 9   | [SF]     | Staff assigns teacher on **Lesson Teacher List** (separate from lesson detail)                               |
| 10  | [BO]     | Centre Manager views lesson as **CM role** (limited actions vs. teacher role)                                |

**Features covered:**

- Lesson Teacher > Assign/Unassign in lesson detail (27 cases)
- Lesson Teacher > Assign/Unassign on Teacher List (4 cases)
- Lesson Teacher > Clashing Alert (34 cases)
- Lesson Teacher > View from another location (51 cases)
- Lesson on BO > CM/PT Teacher (164 cases)
- Lesson on BO > Centre Manager (15 cases)

---

## E2E-17: Renseikai — Attendance & Error Configuration

> **Theme:** Renseikai-specific: attendance collection, bulk update, error message configuration.

| #   | Platform | Action                                                                                               |
| --- | -------- | ---------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates lessons and assigns students                                                           |
| 2   | [SF]     | Staff verifies **class name uniqueness** check (Renseikai rule)                                      |
| 3   | [SF]     | Staff **collects attendance on SF** (Renseikai-specific flow)                                        |
| 4   | [BO]     | Teacher **collects attendance on BO** (Renseikai-specific flow)                                      |
| 5   | [BO]     | Teacher uses **Bulk Update Attendance** from Calendar view (select multiple students, update status) |
| 6   | [SF]     | Staff **configures lesson student session error messages** (custom error display per org)            |
| 7   | [SF]     | Staff triggers a student assignment that violates a rule → verifies configured error message         |
| 8   | [SF]     | Staff verifies **Confirmation Alert** for mismatch scenarios                                         |
| 9   | [SF]     | Staff **assigns a teacher** to the lesson                                                            |
| 10  | [SF]     | Staff **publishes** the lesson                                                                       |
| 11  | [BO]     | Teacher views lesson with assigned students on **BO Calendar**                                       |
| 12  | [Mobile] | Student views the lesson on **Learner App** schedule                                                 |

**Features covered:**

- Customization > Renseikai > Collect attendance SF (2 cases)
- Customization > Renseikai > Collect attendance BO (2 cases)
- Calendar BO > Renseikai Bulk Update Attendance (34 cases)
- Student Session > Renseikai Configure Error Message (15 cases)
- Student Session > Confirmation Alert mismatch (10 cases)
- Master Data > Renseikai Class Name Unique check (8 cases)
- Lesson Teacher > Assign in lesson detail (27 cases)
- Lesson Mobile > View lesson (6 cases)

---

## E2E-18: EEA Dual Lesson — Paired Locations

> **Theme:** EEA dual lesson: create paired schedules, assign teachers across locations.

| #   | Platform | Action                                                                                       |
| --- | -------- | -------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates a **Lesson Schedule at Location 1**                                            |
| 2   | [SF]     | Staff creates a **paired Lesson Schedule at Location 2** → links as Dual Lesson (Partner LS) |
| 3   | [System] | Verify bidirectional partner relationship (LS1 ↔ LS2)                                        |
| 4   | [SF]     | Staff assigns **Teacher at Location 1** to LS1                                               |
| 5   | [SF]     | Staff uses **Acquire Teacher** (EEA flow) to assign teacher from Location 2                  |
| 6   | [SF]     | Staff assigns students from both locations                                                   |
| 7   | [SF]     | Staff **publishes** the lesson                                                               |
| 8   | [BO]     | Teacher at Location 1 sees the dual lesson on BO Calendar                                    |
| 9   | [BO]     | Teacher at Location 2 sees the same lesson on BO Calendar                                    |
| 10  | [Mobile] | Student views the dual lesson on **Learner App** schedule                                    |
| 11  | [SF]     | Staff edits the dual lesson → verify both LS chain updated                                   |

**Features covered:**

- Lesson > EEA Dual Lesson (40 cases)
- Customization > EEA > Acquire Teacher (20 cases)
- Lesson Teacher > View from another location (51 cases)
- Lesson Mobile > View lesson (6 cases)

---

## E2E-19: Riso — Lesson Allocation & Subject in Detail

> **Theme:** Riso-specific: LA management on UI and subject display.

| #   | Platform | Action                                                                                     |
| --- | -------- | ------------------------------------------------------------------------------------------ |
| 1   | [SF]     | Staff creates/updates **Lesson Allocation** via Riso UI                                    |
| 2   | [SF]     | Staff verifies LA fields: duration, slot type, require allocation flag                     |
| 3   | [SF]     | Staff creates a lesson and verifies **Subject displayed in Lesson Detail** (Riso-specific) |
| 4   | [SF]     | Staff assigns teacher with **eligible subject** matching lesson subject                    |
| 5   | [SF]     | Staff assigns students → LA consumption tracked                                            |
| 6   | [SF]     | Staff updates LA duration → class member auto-reassignment triggered                       |
| 7   | [SF]     | Staff **publishes** the lesson                                                             |
| 8   | [BO]     | Teacher views lesson with subject info on **BO Calendar**                                  |
| 9   | [Mobile] | Student views the lesson on **Learner App** schedule                                       |

**Features covered:**

- Customization > Riso > Lesson Allocation (80 cases)
- Customization > Riso > Subject in Lesson Detail (25 cases)
- Lesson Allocation > Update Slot (13 cases)
- Lesson Mobile > View lesson (6 cases)

---

## E2E-20: Withus Juku — Custom Event Management

> **Theme:** Withus Juku event customization: custom events, lesson/course specifics.

| #   | Platform | Action                                                             |
| --- | -------- | ------------------------------------------------------------------ |
| 1   | [SF]     | Staff creates a **Withus Juku-specific event** with custom fields  |
| 2   | [SF]     | Staff manages **event attendees** and capacity                     |
| 3   | [SF]     | Staff creates **custom event types**                               |
| 4   | [SF]     | Staff creates lessons with **Withus Juku lesson/course** specifics |
| 5   | [SF]     | Staff **assigns teacher and students** to the lesson               |
| 6   | [SF]     | Staff **publishes** the lesson                                     |
| 7   | [SF]     | Staff verifies event and lesson on Calendar                        |
| 8   | [BO]     | Teacher views events and lessons on **BO Calendar**                |
| 9   | [Mobile] | Student views the lesson on **Learner App** schedule               |

**Features covered:**

- Customization > Withus Juku > Event management (59 cases)
- Customization > Withus Juku > Custom event (23 cases)
- Customization > Withus Juku > Lesson/Course (9 cases)
- Lesson Teacher > Assign in lesson detail (27 cases)
- Student Session > Assign by Add Student (70 cases)
- Lesson Mobile > View lesson (6 cases)

---

## E2E-21: Extend Recurring Lesson

> **Theme:** Extend an existing recurring lesson chain with additional occurrences.

| #   | Platform | Action                                                                  |
| --- | -------- | ----------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates a **weekly recurring lesson** ending after 4 lessons      |
| 2   | [SF]     | Staff assigns teacher and students to the chain                         |
| 3   | [SF]     | Staff **extends the recurring lesson** to add more occurrences          |
| 4   | [System] | New lessons created with same settings; teacher and class auto-assigned |
| 5   | [SF]     | Staff verifies extended lessons on Calendar                             |
| 6   | [SF]     | Staff verifies LA updated with new session count                        |
| 7   | [SF]     | Staff **publishes** the extended lessons                                |
| 8   | [BO]     | Teacher sees extended lessons on **BO Calendar**                        |
| 9   | [Mobile] | Student views extended lessons on **Learner App** schedule              |

**Features covered:**

- Extend Recurring Lesson (64 cases)
- Lesson Teacher > Assign in lesson detail (27 cases)
- Lesson Mobile > View lesson (6 cases)

---

## E2E-22: Import Lesson & CSV Operations

> **Theme:** Bulk operations: import lessons, import class members, import syllabus.

| #   | Platform | Action                                                                           |
| --- | -------- | -------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff **imports lessons via CSV** (with teacher usernames, dates, course, class) |
| 2   | [System] | Lessons created; teachers auto-assigned; lesson reports auto-created             |
| 3   | [SF]     | Staff verifies imported lessons on Calendar                                      |
| 4   | [SF]     | Staff **imports class members via CSV** → students auto-assigned to lessons      |
| 5   | [SF]     | Staff **imports Event Master data**                                              |
| 6   | [SF]     | Staff **imports Activity Events**                                                |
| 7   | [SF]     | Staff **imports Syllabus** (Nichibei) via CSV                                    |
| 8   | [SF]     | Staff verifies all imported data integrity                                       |
| 9   | [SF]     | Staff **publishes** the imported lessons                                         |
| 10  | [BO]     | Teacher views imported lessons on **BO Calendar**                                |
| 11  | [Mobile] | Student views imported lessons on **Learner App** schedule                       |

**Features covered:**

- Lesson > Import Lesson (27 cases)
- Student Session > Class management > Import (3 cases)
- Event Master > Importing (2 cases)
- Activity Event > Importing (2 cases)
- Nichibei > Lesson Syllabus (24 cases)
- Lesson Teacher > Assign in lesson detail (27 cases)
- Lesson Mobile > View lesson (6 cases)

---

## E2E-23: Student Reallocation & Trial Lessons

> **Theme:** Full reallocation flow (Absent prerequisite → Reallocate checkbox → session move) plus trial student session update before removal.

| #   | Platform | Action                                                                                                                         |
| --- | -------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 1   | [SF]     | Staff creates two lessons for the same course; assigns a teacher to both                                                       |
| 2   | [SF]     | Staff assigns **Student A** to Lesson 1; verifies **Lesson Report Detail** auto-created                                        |
| 3   | [BO]     | Teacher opens Lesson 1 → **collects attendance** → sets Student A's status to **Absent**                                       |
| 4   | [System] | Verify **Reallocate checkbox** becomes enabled for the Absent session (disabled for Attend/Late/Leave Early)                   |
| 5   | [SF]     | Staff checks Reallocate checkbox → **Reallocation Request** created (Status = Open, New Lesson blank)                          |
| 6   | [SF]     | Staff opens Reallocation popup on LA Detail → selects Lesson 2 as target → confirms; session moved; **no point recalculation** |
| 7   | [SF]     | Staff views **Reallocation list** on Calendar; verifies Status = Completed, source/target lessons populated                    |
| 8   | [SF]     | Staff creates a **Trial Lesson** and assigns a trial student; verifies **"Trial Student" dot** on lesson card                  |
| 9   | [BO]     | Teacher opens Trial Lesson → **edits trial student session** (updates attendance status) — session updated before removal      |
| 10  | [SF]     | Staff **removes the trial student** from the lesson; verifies Lesson Report Detail deleted; LA Lesson Allocated decremented    |
| 11  | [SF]     | Staff verifies **Risk Flag** triggers based on attendance/performance; **New Flag** visible on first-enrolled student          |
| 12  | [SF]     | Staff **publishes** both lessons                                                                                               |
| 13  | [BO]     | Teacher views reallocation info and Calendar indicators on lesson detail                                                       |
| 14  | [Mobile] | Student views remaining assigned lessons on **Learner App** schedule                                                           |

**Features covered:**

- Student Session > Reallocation (23 cases)
- Student Session > Trial Student (20 cases)
- Nichibei > Reallocation (26 cases)
- Nichibei > Trial Lesson (20 cases)
- Student Session > Risk Flag (9 cases)
- Student Session > New flag (3 cases)
- Calendar SF > Student/Teacher/Reallocation list (114 cases)
- Lesson Teacher > Assign in lesson detail (27 cases)
- Lesson Mobile > View lesson (6 cases)

---

## E2E-24: Configuration, Translation & Live Lesson

> **Theme:** System configuration, multi-language, and live lesson features.

| #   | Platform | Action                                                                                     |
| --- | -------- | ------------------------------------------------------------------------------------------ |
| 1   | [SF]     | Staff configures **system settings** for lesson scheduling                                 |
| 2   | [SF]     | Staff verifies **translated labels** (Japanese ↔ English) across lesson and calendar views |
| 3   | [SF]     | Staff creates a **Live Lesson**                                                            |
| 4   | [BO]     | Teacher starts/joins the live lesson session                                               |
| 5   | [SF]     | Staff verifies **Lesson Master** translations                                              |
| 6   | [SF]     | Staff verifies **Incident Prevention** rules are applied                                   |

**Features covered:**

- Configuration (3 cases)
- Lesson Management > Translation (4 cases)
- Calendar > Translation (0 cases)
- Lesson Master > Translation (3 cases)
- Live Lesson (2 cases)
- Incident Prevention (16 cases)

---

## E2E-25: Create Lesson via Calendar & Non-Weekly Recurrence Types

> **Theme:** Fill gap — lesson creation triggered from Calendar UI, plus daily and custom recurrence types with end-date and count configurations.

| #   | Platform | Action                                                                                                                                            |
| --- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff opens **SF Calendar Week view** → clicks an empty time slot → creates a **one-time lesson** directly from the Calendar                      |
| 2   | [System] | Verify lesson created with correct date/time; **Lesson Report** auto-created with Draft status                                                    |
| 3   | [SF]     | Staff opens SF Calendar → creates a **daily recurring lesson** (repeat every 1 day, end after 7 occurrences)                                      |
| 4   | [System] | Verify 7 lessons generated on consecutive days; **Lesson Report** auto-created for each                                                           |
| 5   | [SF]     | Staff opens SF Calendar → creates a **custom recurrence** lesson (repeat on Mon/Wed/Fri, end date = 4 weeks from now)                             |
| 6   | [System] | Verify lessons created only on selected weekdays within the date range; **Lesson Report** auto-created for each                                   |
| 7   | [SF]     | Staff creates a recurring lesson with **End date** configuration (not number of lessons)                                                          |
| 8   | [SF]     | Staff creates a recurring lesson with **Number of lessons** configuration and verifies correct count                                              |
| 9   | [SF]     | Staff creates a recurring lesson using **Course Schedule** configuration → verify week-order numbering                                            |
| 10  | [SF]     | Staff creates a **custom recurrence** (Mon/Wed/Fri) with **"End after N"** (6 occurrences) → verify exactly 6 lessons generated on those weekdays |

**Features covered:**

- Lesson > Create via Calendar (Calendar click-to-create)
- Lesson > Create on Lesson List — Daily recurrence
- Lesson > Create on Lesson List — Custom recurrence + End by date (Mon/Wed/Fri)
- Lesson > Create on Lesson List — Custom recurrence + End after N lessons
- Lesson > Create on Lesson List — End date configuration
- Lesson > Create on Lesson List — Number of lessons configuration
- Lesson > Create in Lesson Schedule Detail — Course Schedule
- Lesson Report > Auto-created for Calendar-created lessons
- Lesson Report > Auto-created for daily/custom recurring lessons

---

## E2E-26: Create Lesson — Recurrence Verification & End-to-End Lifecycle

> **Theme:** Assign teacher and students to the created recurring lessons, then verify BO, Mobile view, and Mobile attendance submission.

| #   | Platform | Action                                                                                      |
| --- | -------- | ------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff **assigns teacher** to the daily recurring chain ("This and following" from lesson 1) |
| 2   | [SF]     | Staff **adds students** to the custom recurring chain                                       |
| 3   | [System] | Verify **Lesson Report Details** auto-created per student for all lessons                   |
| 4   | [SF]     | Staff **publishes** all lessons                                                             |
| 5   | [BO]     | Teacher views daily and custom lessons on **BO Calendar**                                   |
| 6   | [Mobile] | Student opens Learner App → sees all daily/custom lessons in schedule                       |
| 7   | [Mobile] | Student **submits attendance** for one lesson via Learner App                               |

**Features covered:**

- Lesson Report Detail > Auto-created per student
- Lesson Teacher > Assign in lesson detail (27 cases)
- Lesson Mobile > View lesson (6 cases)
- Lesson Mobile > Submit attendance (28 cases)

---

## E2E-27: Assign Student — Recurring Scope Selectors

> **Theme:** Fill gap — assign students to a recurring lesson using "Only this", "This and following", and "Specific number" scope selectors.

| #   | Platform | Action                                                                                                         |
| --- | -------- | -------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates a **weekly recurring lesson** (5 occurrences) with a class assigned                              |
| 2   | [SF]     | Staff opens Lesson Detail of occurrence 3 → **assigns Student A** with scope **"Only this"**                   |
| 3   | [System] | Verify Student A session created for occurrence 3 only; occurrences 1, 2, 4, 5 unchanged                       |
| 4   | [SF]     | Staff opens Lesson Detail of occurrence 2 → **assigns Student B** with scope **"This and following"**          |
| 5   | [System] | Verify Student B sessions created for occurrences 2, 3, 4, 5; occurrence 1 unchanged                           |
| 6   | [SF]     | Staff opens Lesson Detail of occurrence 1 → **assigns Student C** with scope **"Specific number"** (3 lessons) |
| 7   | [System] | Verify Student C sessions created for occurrences 1, 2, 3 only                                                 |
| 8   | [System] | Verify **LA Lesson Allocated** count incremented for Students A, B, and C                                      |

**Features covered:**

- Student Session > Assign by Add Student — "Only this" recurring scope
- Student Session > Assign by Add Student — "This and following" recurring scope
- Student Session > Assign by Add Student — "Specific number" recurring scope
- Lesson Allocation > LA tab — Lesson Allocated count updates

---

## E2E-28: Assign Student — Calendar, BO Platforms & Mobile Verification

> **Theme:** Fill gap — assign students from Calendar popover and BO Lesson Detail, then verify on Mobile.

| #   | Platform | Action                                                                                                         |
| --- | -------- | -------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff opens **SF Calendar** → selects a lesson → assigns **Student D** from the Calendar lesson-detail popover |
| 2   | [System] | Verify Student D session created; **Lesson Report Detail** auto-created for Student D                          |
| 3   | [BO]     | Teacher (or CM) opens lesson on **BO Lesson Detail** → **assigns Student E** from the student list on BO       |
| 4   | [System] | Verify Student E session created; **Lesson Report Detail** auto-created for Student E                          |
| 5   | [System] | Verify **LA Lesson Allocated** count incremented for Students D and E                                          |
| 6   | [SF]     | Staff **assigns a teacher** to the lesson chain                                                                |
| 7   | [SF]     | Staff **publishes** all lessons                                                                                |
| 8   | [Mobile] | Students D and E open Learner App → verify they see their assigned lessons                                     |
| 9   | [Mobile] | Student D **submits attendance** for their lesson via Learner App                                              |

**Features covered:**

- Student Session > Assign via Calendar (Calendar popover/click)
- Student Session > Assign via BO (BO Lesson Detail)
- Lesson Report Detail > Auto-created per student for all assignment flows
- Lesson Teacher > Assign in lesson detail (27 cases)
- Lesson Mobile > View lesson (6 cases)
- Lesson Mobile > Submit attendance (28 cases)

---

## E2E-29: Modify & Unassign Student — Setup & Recurring Scope Removals

> **Theme:** Create and publish a recurring lesson chain, then modify attendance and remove students using "Only this" and "This and following" recurring scope selectors.

| #   | Platform | Action                                                                                                                                                  |
| --- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates a **weekly recurring lesson** (5 occurrences) with class assigned; assigns Students A–E to all occurrences                                |
| 2   | [SF]     | Staff assigns a teacher and **publishes** all 5 lessons                                                                                                 |
| 3   | [System] | Verify **Lesson Report** and **Lesson Report Detail** auto-created for each student × each occurrence                                                   |
| 4   | [BO]     | Teacher opens occurrence 2 on BO → **edits attendance status** for Student A (e.g., Attend → Absent) — modifying the session before removal             |
| 5   | [SF]     | Staff opens Lesson Detail of occurrence 2 → **removes Student A** with scope **"Only this"**                                                            |
| 6   | [System] | Verify Student A session and Lesson Report Detail deleted for occurrence 2 only; occurrences 1, 3, 4, 5 unchanged; LA Lesson Allocated decremented by 1 |
| 7   | [SF]     | Staff opens occurrence 4 on Calendar → **edits the lesson time** (drag/reschedule) — modifying the lesson before removing student from the chain        |
| 8   | [SF]     | Staff opens Lesson Detail of occurrence 4 → **removes Student A** with scope **"This and following"**                                                   |
| 9   | [System] | Verify Student A sessions deleted for occurrences 4 and 5; Lesson Report Details removed; LA updated                                                    |

**Features covered:**

- Student Session > Modify attendance before unassign (BO)
- Student Session > Modify lesson time (Calendar drag) before unassign
- Student Session > Unassign — "Only this" recurring scope
- Student Session > Unassign — "This and following" recurring scope
- Lesson Report Detail > Auto-deleted on unassignment
- Lesson Allocation > LA tab — Lesson Allocated count decrements

---

## E2E-30: Modify & Unassign Student — Class Change & LA Detail Removals

> **Theme:** Modify LA slot or lesson list, then remove students via Change Class, Bulk Change Class, and LA Detail lesson removal.

| #   | Platform | Action                                                                                                                             |
| --- | -------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff opens **LA Detail** for Student B → updates the **duration** of an existing lesson allocation (modifying the session record) |
| 2   | [SF]     | Staff **changes Student B's class** in the **Course tab** (Change Class) → triggers unassignment from original class lessons       |
| 3   | [System] | Verify Student B removed from all remaining lessons of original class; Lesson Report Details removed; LA reflects new class        |
| 4   | [SF]     | Staff opens **LA Detail** for Student C → **modifies lesson list** (edits which lessons are allocated) before bulk class change    |
| 5   | [SF]     | Staff uses **Bulk Change Class** for Student C → triggers batch unassignment from original class lessons                           |
| 6   | [System] | Verify Student C removed from old class lessons in bulk; Lesson Report Details removed                                             |
| 7   | [BO]     | Teacher opens **LA Detail on BO** for Student D → **edits attendance** for one lesson (modifying session before removal)           |
| 8   | [SF]     | Staff opens **LA Detail on SF** for Student D → **removes one lesson** from the LA detail list                                     |
| 9   | [System] | Verify Student D session deleted for that lesson; Lesson Report Detail removed; LA Lesson Allocated decremented                    |

**Features covered:**

- Student Session > Modify LA slot/duration before class change
- Student Session > Class management > Change Class in Course tab (unassignment side)
- Student Session > Class management > Bulk Change Class (unassignment side)
- Student Session > LA Detail > Edit lessons (BO and SF)
- Student Session > LA Detail > Remove lesson
- Lesson Report Detail > Auto-deleted on unassignment

---

## E2E-31: Modify & Unassign Student — Lesson Schedule, Order, Calendar & BO Removals

> **Theme:** Remove students via Lesson Schedule changes, Lesson Allocation changes, Order-triggered duration shortening, and direct removal from Calendar and BO. Verify on Mobile.

| #   | Platform | Action                                                                                                                          |
| --- | -------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff **changes Course/Class in Lesson Schedule** → student sessions for lessons that no longer match are modified then removed |
| 2   | [System] | Verify student sessions updated: sessions for matching lessons remain; sessions for non-matching lessons removed                |
| 3   | [SF]     | Staff **changes Location/Class in Lesson Allocation** → student sessions outside the new scope are removed                      |
| 4   | [System] | Verify student removed from lessons under old location/class; LA reflects new assignment                                        |
| 5   | [SF]     | Staff processes an **Order** that shortens Student E's class member duration                                                    |
| 6   | [System] | Verify Student E auto-unassigned from lessons outside the new duration; Lesson Report Details removed; LA updated               |
| 7   | [SF]     | Staff opens **SF Calendar** → selects a lesson → **edits attendance** for a student in the Calendar popover (modify step)       |
| 8   | [SF]     | Staff opens **SF Calendar** → selects the same lesson → **removes the student** from the Calendar detail popover                |
| 9   | [System] | Verify session deleted; Lesson Report Detail removed; lesson still appears on Calendar with remaining students                  |
| 10  | [BO]     | Teacher opens a lesson on **BO Lesson Detail** → **edits a student's attendance status** (modify step)                          |
| 11  | [BO]     | Teacher opens the same lesson → **removes the student** from the student/attendance list on BO                                  |
| 12  | [System] | Verify session deleted; Lesson Report Detail removed                                                                            |
| 13  | [Mobile] | Affected students open Learner App → verify unassigned lessons **no longer appear** in their schedule                           |
| 14  | [Mobile] | Student with remaining sessions views their lesson and **submits attendance** via Learner App                                   |

**Features covered:**

- Student Session > Change Course/Class in Lesson Schedule (modify + unassignment side)
- Student Session > Change Location/Class in Lesson Allocation (modify + unassignment side)
- Student Session > Class member duration updated by Order
- Student Session > Unassign via Calendar (with prior modify step)
- Student Session > Unassign via BO (with prior modify step)
- Lesson Report Detail > Auto-deleted on unassignment for all flows
- Lesson Mobile > View lesson — verify removed lessons absent (6 cases)
- Lesson Mobile > Submit attendance (28 cases)

---

## E2E-32: Teacher Assignment — All Methods & Unassign via Lesson Detail

> **Theme:** Fill gap — assign teacher using "Only this" scope, Calendar, Teacher List, and Import; then unassign via Lesson Detail with "Only this" and "This and following".

| #   | Platform | Action                                                                                                             |
| --- | -------- | ------------------------------------------------------------------------------------------------------------------ |
| 1   | [SF]     | Staff creates a **weekly recurring lesson** (5 occurrences)                                                        |
| 2   | [SF]     | Staff opens Lesson Detail of occurrence 3 → **assigns Teacher A** with scope **"Only this"**                       |
| 3   | [System] | Verify Teacher A assigned to occurrence 3 only; occurrences 1, 2, 4, 5 have no teacher                             |
| 4   | [SF]     | Staff opens **SF Calendar** → selects occurrence 1 → assigns **Teacher B** from the Calendar lesson-detail popover |
| 5   | [System] | Verify Teacher B assigned to occurrence 1; clashing alert check performed if Teacher B has overlap                 |
| 6   | [SF]     | Staff assigns **Teacher C** to occurrence 1 via **Lesson Teacher List** (not Lesson Detail)                        |
| 7   | [System] | Verify Teacher C added to lesson teacher list for occurrence 1                                                     |
| 8   | [SF]     | Staff **imports a lesson CSV** that includes a teacher column → teacher auto-assigned on import                    |
| 9   | [System] | Verify imported lesson has correct teacher; **Lesson Report** auto-created                                         |
| 10  | [SF]     | Staff opens Lesson Detail of occurrence 2 → **unassigns Teacher B** with scope **"Only this"**                     |
| 11  | [System] | Verify Teacher B removed from occurrence 2 only; other occurrences unchanged                                       |
| 12  | [SF]     | Staff opens **Lesson Teacher List** for occurrence 1 → **removes Teacher C** via the Teacher List view             |
| 13  | [System] | Verify Teacher C removed from occurrence 1 via Teacher List; list updates immediately                              |

**Features covered:**

- Lesson Teacher > Assign — "Only this" recurring scope
- Lesson Teacher > Assign via Calendar (Calendar popover/click)
- Lesson Teacher > Assign on Lesson Teacher List
- Lesson Teacher > Assign via Import Lesson
- Lesson Teacher > Unassign — "Only this" recurring scope
- Lesson Teacher > Unassign via Lesson Teacher List
- Lesson Report > Auto-created for imported lessons with teacher

---

## E2E-33: Teacher Unassignment — All Methods, One-Time & BO Assignment

> **Theme:** Cover all remaining teacher management gaps: assign via BO, unassign "This and following", unassign via Calendar/BO, and unassign from one-time lesson.

| #   | Platform | Action                                                                                                        |
| --- | -------- | ------------------------------------------------------------------------------------------------------------- |
| 1   | [BO]     | CM opens occurrence 3 on **BO Lesson Detail** → **assigns Teacher D** from the teacher list on BO             |
| 2   | [System] | Verify Teacher D assigned to occurrence 3 via BO; lesson appears on Teacher D's BO Calendar                   |
| 3   | [SF]     | Staff opens Lesson Detail of occurrence 4 → **unassigns Teacher C** with scope **"This and following"**       |
| 4   | [System] | Verify Teacher C removed from occurrences 4 and 5; earlier occurrences unchanged                              |
| 5   | [SF]     | Staff opens **SF Calendar** → selects occurrence 2 → **unassigns teacher** from the Calendar detail popover   |
| 6   | [System] | Verify teacher removed from occurrence 2; BO Calendar no longer shows that teacher for this lesson            |
| 7   | [BO]     | Teacher opens occurrence 1 on **BO Lesson Detail** → **unassigns themselves** (or CM removes teacher from BO) |
| 8   | [System] | Verify teacher removed; lesson no longer appears on that teacher's BO Calendar                                |
| 9   | [SF]     | Staff creates a separate **one-time lesson** → assigns Teacher D to it on Lesson Detail                       |
| 10  | [SF]     | Staff **unassigns Teacher D** from the one-time lesson (no scope selector — takes effect immediately)         |
| 11  | [System] | Verify Teacher D removed from the one-time lesson only; no other lessons affected                             |
| 12  | [SF]     | Staff assigns students to remaining lessons and **publishes**                                                 |
| 13  | [BO]     | Remaining teachers see their lessons on **BO Calendar**                                                       |
| 14  | [Mobile] | Students view lessons on Learner App; student **submits attendance** for one lesson                           |

**Features covered:**

- Lesson Teacher > Assign via BO (BO Lesson Detail)
- Lesson Teacher > Unassign — "This and following" recurring scope
- Lesson Teacher > Unassign via Calendar
- Lesson Teacher > Unassign via BO (BO Lesson Detail)
- Lesson Teacher > Unassign from one-time lesson (no scope selector)
- Lesson Mobile > View lesson (6 cases)
- Lesson Mobile > Submit attendance (28 cases)

---

## E2E-34: Automated Reports — Lesson Creation & Student Assignment Flows

> **Theme:** Fill gap — verify Lesson Report + Lesson Report Detail auto-creation for every creation method: Calendar, recurring, extend, Lesson Schedule add, and Order-triggered assignment.

| #   | Platform | Action                                                                                                                 |
| --- | -------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates a **one-time lesson via Calendar** and adds a student                                                    |
| 2   | [System] | Verify **Lesson Report** auto-created (Draft); **Lesson Report Detail** auto-created for the student                   |
| 3   | [SF]     | Staff creates a **weekly recurring lesson via Lesson List** and assigns student via class auto-assignment              |
| 4   | [System] | Verify Lesson Report + Detail auto-created for **each occurrence** in the chain                                        |
| 5   | [SF]     | Staff **extends the recurring lesson** (adds 3 more occurrences) and verifies student class auto-assignment propagates |
| 6   | [System] | Verify Lesson Report + Detail auto-created for the **3 new extended occurrences**                                      |
| 7   | [SF]     | Staff **adds a lesson** via Lesson Schedule Detail (not initial creation) and assigns student                          |
| 8   | [System] | Verify Lesson Report + Detail auto-created for the manually added lesson                                               |
| 9   | [SF]     | Staff processes an **Order** that creates a new LA → student auto-assigned to lessons → verify reports                 |
| 10  | [System] | Verify Lesson Report Detail auto-created per student for Order-triggered assignments                                   |

**Features covered:**

- Lesson Report > Auto-created for Calendar-triggered lesson creation
- Lesson Report > Auto-created for Lesson List recurring creation (all occurrences)
- Lesson Report > Auto-created for Extend Recurring new occurrences
- Lesson Report > Auto-created for Lesson Schedule Detail "Add Lesson"
- Lesson Report > Auto-created for Order-triggered student assignment

---

## E2E-35: Automated Reports — Bulk Assign, Report Lifecycle & Mobile Attendance

> **Theme:** Verify reports for Bulk Assign and LA Detail assignment, complete the report lifecycle on BO, and verify Mobile attendance submission.

| #   | Platform | Action                                                                                                                  |
| --- | -------- | ----------------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff uses **Bulk Assign Class** → students auto-assigned → verify reports auto-created for all newly assigned students |
| 2   | [System] | Verify Lesson Report Detail created per student per lesson for all bulk-assigned sessions                               |
| 3   | [SF]     | Staff uses **LA Detail to assign** student to a lesson → verify Lesson Report Detail auto-created                       |
| 4   | [SF]     | Staff **assigns teacher** and **publishes** all lessons                                                                 |
| 5   | [BO]     | Teacher opens lesson on BO → verifies Lesson Report exists and is in **Draft** status for each published lesson         |
| 6   | [BO]     | Teacher fills in and **submits** the Lesson Report for the first lesson                                                 |
| 7   | [BO]     | Teacher **publishes** the Lesson Report                                                                                 |
| 8   | [Mobile] | Student opens Learner App → sees lesson → taps **Submit Attendance** → selects attendance status → confirms submission  |
| 9   | [Mobile] | Student views the **published Lesson Report** from the teacher on Learner App                                           |
| 10  | [Mobile] | Parent opens Learner App → verifies child's lesson and **published Lesson Report** visible                              |

**Features covered:**

- Lesson Report Detail > Auto-created for Bulk Assign Class
- Lesson Report Detail > Auto-created for LA Detail assignment
- Lesson Report > Status: Draft → Submitted → Published (BO flow)
- Lesson on BO > CM/PT Teacher > Report BO (54 cases)
- Lesson Mobile > Submit attendance — explicit step (28 cases)
- Lesson Mobile > View lesson (6 cases)
- Lesson Mobile > View published Lesson Report

---

## E2E-36: Change Lesson — Move Student Session via Calendar

> **Theme:** Use the "Change Lesson" feature on SF Calendar to move a student from one lesson to another within the same schedule, verifying session and report integrity.

| #   | Platform | Action                                                                                                                                                     |
| --- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [SF]     | Staff creates two lessons in the same **Lesson Schedule** (Lesson A and Lesson B); assigns a teacher to both                                               |
| 2   | [SF]     | Staff **assigns Student A** to Lesson A; verifies **Lesson Report Detail** auto-created; LA Lesson Allocated = 1                                           |
| 3   | [SF]     | Staff **publishes** both lessons                                                                                                                           |
| 4   | [SF]     | Staff opens **SF Calendar** → selects Lesson A → uses **"Change Lesson"** to move Student A's session to Lesson B                                          |
| 5   | [System] | Verify: Student A removed from Lesson A; Lesson Report Detail for Lesson A **deleted**; Student A assigned to Lesson B; new Report Detail **auto-created** |
| 6   | [System] | Verify LA Lesson Allocated count unchanged (still 1 — session moved, not removed or double-counted)                                                        |
| 7   | [BO]     | Teacher views Lesson B on **BO Calendar** → sees Student A in the student list                                                                             |
| 8   | [Mobile] | Student A opens Learner App → sees **Lesson B** (not Lesson A) in their schedule                                                                           |

**Features covered:**

- Calendar SF > Change Lesson (11 cases)
- Student Session > Session moved via Change Lesson
- Lesson Report Detail > Auto-deleted on Change Lesson (source lesson)
- Lesson Report Detail > Auto-created on Change Lesson (target lesson)
- Lesson Teacher > Assign in lesson detail (27 cases)
- Lesson Mobile > View lesson (6 cases)

---

## Coverage Matrix

| E2E Scenario                                                                  | Qase Cases Covered | Key Domains                                                    |
| ----------------------------------------------------------------------------- | -----------------: | -------------------------------------------------------------- |
| E2E-01: Lesson Lifecycle — Create, Teach, Report, View                        |               ~996 | Lesson, Calendar, BO, Mobile                                   |
| E2E-02: Recurring Lesson — Create, Edit Chain, Delete, Calendar Drag          |               ~320 | Lesson CRUD, Calendar, Scheduling                              |
| E2E-03: Class Auto-Assignment — Setup & Effective Date Logic                  |                ~80 | Class, Student Session, Effective Date                         |
| E2E-04: Class Auto-Assignment — Import, Multiple Classes & Verification       |                ~60 | Class, Import, Multiple Classes, LA                            |
| E2E-05: Online Lesson with Zoom                                               |               ~416 | Zoom, Lesson, BO                                               |
| E2E-06: Event Master — Setup, Activity Event & Calendar                       |               ~165 | Event, Calendar                                                |
| E2E-07: Event Master — Booking, Mobile Interaction & Status                   |               ~175 | Booking, Mobile, Event Status                                  |
| E2E-08: External Booking & Koyu Auto-Create Application                       |               ~323 | Booking, Koyu, Event                                           |
| E2E-09: Lesson Allocation — New Order, Change Course & Void                   |                ~60 | LA, Order, SPO                                                 |
| E2E-10: Lesson Allocation — LOA, Add Course & Lesson Assignment               |                ~55 | LA, LOA, Add Course, Mobile                                    |
| E2E-11: Point Consumption — Priority Chain & Edge Cases                       |               ~150 | Nichibei, Points, Priority                                     |
| E2E-12: Point Consumption — Publish, Reporting & Reallocation                 |                ~90 | Nichibei, Reports, Reallocation                                |
| E2E-13: Aver Lesson Report & Subject Flow                                     |               ~419 | Aver, Report, Mobile                                           |
| E2E-14: Aso Curriculum & Syllabus with Student Groups                         |               ~279 | Aso, Syllabus, Student Group                                   |
| E2E-15: Academic Calendar & Closed Dates Impact                               |                ~92 | Master Data, Calendar                                          |
| E2E-16: Teacher Access & Cross-Location Visibility                            |               ~295 | Teacher, BO, Permissions                                       |
| E2E-17: Renseikai — Attendance & Error Configuration                          |                ~71 | Renseikai, Attendance                                          |
| E2E-18: EEA Dual Lesson — Paired Locations                                    |               ~111 | Dual Lesson, EEA                                               |
| E2E-19: Riso — Lesson Allocation & Subject in Detail                          |               ~118 | Riso, LA, Subject                                              |
| E2E-20: Withus Juku — Custom Event Management                                 |                ~91 | Withus Juku, Event                                             |
| E2E-21: Extend Recurring Lesson                                               |                ~64 | Extend, Recurring                                              |
| E2E-22: Import Lesson & CSV Operations                                        |                ~58 | Import, Bulk                                                   |
| E2E-23: Student Reallocation & Trial Lessons                                  |               ~220 | Reallocation (full flow), Trial (session update), Risk, Mobile |
| E2E-24: Configuration, Translation & Live Lesson                              |                ~28 | Config, i18n, Live                                             |
| E2E-25: Create Lesson via Calendar & Non-Weekly Recurrence Types              |                ~65 | Create Lesson, Recurrence, Custom+Count, Reports               |
| E2E-26: Create Lesson — Recurrence Verification & End-to-End Lifecycle        |                ~55 | Teacher, Students, Mobile                                      |
| E2E-27: Assign Student — Recurring Scope Selectors                            |                ~50 | Student Session, Recurring Scope                               |
| E2E-28: Assign Student — Calendar, BO Platforms & Mobile Verification         |                ~50 | Student Session, Calendar, BO                                  |
| E2E-29: Modify & Unassign Student — Setup & Recurring Scope Removals          |                ~55 | Student Session, Unassign, Recurring                           |
| E2E-30: Modify & Unassign Student — Class Change & LA Detail Removals         |                ~55 | Student Session, Class Change, LA                              |
| E2E-31: Modify & Unassign Student — Lesson Schedule, Order, Calendar & BO     |                ~65 | Student Session, Order, Calendar, BO                           |
| E2E-32: Teacher Assignment — All Methods & Unassign via Lesson Detail/List    |                ~55 | Lesson Teacher, Assignment Methods, Teacher List Unassign      |
| E2E-33: Teacher Unassignment — All Methods, One-Time & BO Assignment          |                ~55 | Lesson Teacher, BO Assign, Unassign One-Time, Mobile           |
| E2E-34: Automated Reports — Lesson Creation & Student Assignment Flows        |                ~45 | Lesson Report, Auto-create                                     |
| E2E-35: Automated Reports — Bulk Assign, Report Lifecycle & Mobile Attendance |                ~50 | Lesson Report, BO, Mobile Attendance                           |
| E2E-36: Change Lesson — Move Student Session via Calendar                     |                ~20 | Calendar SF Change Lesson, Student Session, Mobile             |

> **Note:** Some test cases are covered by multiple E2E scenarios (shared features like Calendar views, LA updates). The total unique coverage exceeds 4,191 when cross-references are included.
>
> **Scenarios split from originals to keep each under 15 steps:**
>
> - E2E-03/04 ← original E2E-03 (18 steps)
> - E2E-06/07 ← original E2E-05 (16 steps)
> - E2E-09/10 ← original E2E-07 (20 steps)
> - E2E-11/12 ← original E2E-08 (19 steps)
> - E2E-25/26 ← original E2E-21 (16 steps)
> - E2E-27/28 ← original E2E-22 (16 steps)
> - E2E-29/30/31 ← original E2E-23 (32 steps)
> - E2E-32/33 ← original E2E-24 (21 steps)
> - E2E-34/35 ← original E2E-25 (20 steps)
> - E2E-36 ← new: Change Lesson gap coverage (Calendar SF > Change Lesson, 11 cases)
