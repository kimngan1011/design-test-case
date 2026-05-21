ID: https://manabie.atlassian.net/browse/LT-73558
Epic: Core | Event Management & Booking system | Reserve event in booking system by target segment
Status: Done | Labels: SF-Event, nozomi-promised
Timeline: 2025-03-17 pre-prod → 2025-03-31 prod

---

## Summary

Target Segment is a filtering mechanism on Event Master that restricts which students/parents can see and book events via the Booking System. It consists of 4 dimensions: **Target Location, Target Grade, Target School, Target Course** — each stored as separate child objects. When Target Segment is set, only students matching the segment criteria (or explicitly added to the Master Participant list) can see and reserve the event in the Learner App Booking System.

---

## Related Epics & Tickets

### Core Epics
| Key | Summary | Status |
|---|---|---|
| LT-73558 | Core — Reserve event in booking system by target segment | Done |
| LT-60685 | Event Master Record Page (includes Target Segment section) | Done |
| LT-78534 | Core — Enrollment status in Target segment | Done |
| LT-83503 | [Nozomi] Available event list in Student contact page (target segment) | Done |
| LT-96178 | [Renseikai] Add Location Filter to Master Staff | Ready for QA |

### Implementation Sub-tickets (LT-73558)
| Key | Summary | Status |
|---|---|---|
| LT-73909 | [SF] Validate get event master by target segment | Done |
| LT-73910 | [ME] Integrate new API for get event master | Done |
| LT-73912 | [ME] Separate Event master detail screen for internal user via link | Done |
| LT-73913 | [ME] Auto assign student to event master after booking | Done |
| LT-74799 | [SF] Update Assign Event — get participant by target segment | Done |
| LT-74802 | [SF] Update Send Booking Reminder — display target audience by target segment | Done |
| LT-74804 | [SF] Improve send booking reminders logic with large number of students | Done |
| LT-75149 | [ME] Update sorting for activity event list in booking system | Done |
| LT-75437 | [ERPv2 SF] Hide attached image in description for event master & activity event | Done |

### Bugs (all Closed)
| Key | Summary | Status |
|---|---|---|
| LT-75473 | Parent sees event master with non-participant student when switching student | Closed |
| LT-75474 | Show error when parent selects student not in target segment or participant list | Closed |
| LT-75774 | SF user cannot search student and location in Assign to Event popup | Closed |
| LT-75854 | Incorrect participant count after filtering Location in Assign to Event popup | Closed |
| LT-76166 | Cannot search student and location in Assign to Event popup | Closed |
| LT-82525 | Two students reserving same event concurrently → wrong error message in learner app | Closed |
| LT-86686 | CM did not see student in master participant creation form at initial time | Closed |
| LT-88813 | Cannot search student by full name from Master Participant List in Assign to Event | Closed |
| LT-66652 | Only get center location (lowest location) in Location Target Segment | Closed |

---

## Confluence Pages

| Page | URL | Relevance |
|---|---|---|
| [Salesforce] Event Management | spaces/PRDM/pages/1127122162 | Objects 8–11 define Target Segment data model |
| [SF & App] Booking Systems | spaces/PRDM/pages/1176993793 | Booking system overview and scope |
| [US 07–15] Booking System in App | spaces/PRDM/pages/1187708930 | How target segment affects Learner App booking |
| [US 01–06] Event Master Booking Settings | spaces/PRDM/pages/1187807235 | SF-side booking settings (Open/Close, Who Can Reserve) |
| Nozomi — Available Events in Contact | spaces/PRDM/pages/1521352705 | Available event list per target segment in Contact page |

---

## Data Model — Target Segment Objects

Target Segment is implemented as 4 separate child objects on Event Master (Master Detail relationship):

| Object | Key Field | Description |
|---|---|---|
| **Event Target Location** (Object 8) | Target Location (Lookup: Account.location) | Multiple locations allowed; when deleted → unlinked |
| | Enrollment Status (Lookup: Enrollment.EnrollmentStatus) | Combined with location to filter students |
| **Event Target School** (Object 9) | Target School (Lookup: School) | Multiple schools allowed |
| **Event Target Grade** (Object 10) | Target Grade (Lookup: Grade) | Multiple grades allowed |
| **Event Target Course** (Object 11) | Target Course (Lookup: Course Master) | Multiple courses allowed |

**Constraint (LT-66652):** Target Location only accepts **center location (lowest location)** — NOT brand/parent locations.

---

## Acceptance Criteria

### AC 1 — Booking System (Learner App): Student opens booking system

| Case | Given | When | Then |
|---|---|---|---|
| Target Segment SET + Master Participant has value | EM open to booking, expiration >= today, Target Segment set (Location/Grade/School/Course), Master Participant has value | Student/parent opens booking system | Student/parent sees event masters where they match target segment OR are in master participant list. After reserving: student added to Event Master + Activity Event participant records. |
| Target Segment NOT SET + Master Participant has value | EM open to booking, expiration >= today, Target Segment empty, Master Participant has value (Student C) | Student/parent opens booking system | Only students in master participant list can see the event. No target-segment-based listing. |
| Target Segment NOT SET + Master Participant empty | EM open to booking, expiration >= today, Target Segment empty, Master Participant empty | Student/parent opens booking system | No student can see the event to book. |

**Example (Target Segment SET):**
- EM01: Target Location A, B, C — Master Participant: Student C
- EM02: Target Location A, Grade 1
- EM03: Target Location B, Grade 1 — Master Participant: Student C
- Student A: Enrolled Location A, Grade 1 → sees EM01, EM02
- Student B: Enrolled Location B, Grade 1 → sees EM01, EM03
- Student C: Enrolled Location D, Grade 1 → sees EM01 (participant), EM03 (participant)

### AC 2 — Booking System via Direct Link

| Case | Given | When | Then |
|---|---|---|---|
| Via direct booking link | EM open to booking, expiration >= today, Target Segment set | Student/parent accesses booking link and logs in | Student/parent sees activity event list WITHOUT target segment validation and WITHOUT master participant validation. After reserving: added to Event Participant. |

### AC 3 — HQ/CM Assign to Event (SF)

| Case | Given | When | Then |
|---|---|---|---|
| Target Segment SET | EM open to booking, Target Segment set | HQ/CM opens Assign to Event | Student list queried by target segment + master participant. Filters: Location (from target location OR master participant's main location), Grade (from target grade OR master participant's grade). Student added to Event Participant after assignment. |
| Target Segment NOT SET, Master Participant has value | EM open, no target segment, has master participant | HQ/CM opens Assign to Event | Show students from master participant only. |
| No target segment, no master participant | EM open, nothing set | HQ/CM opens Assign to Event | Show no students. |

### AC 4 — Enrollment Status in Target Location (LT-78534)

| Enrollment Status on Target Location | Assign to Event behavior | Booking System behavior |
|---|---|---|
| NULL | Default pre-filter: Enrolled + Temporary. User can select other statuses. | All enrollment statuses at target location can book. |
| Has value (e.g., Enrolled only) | Default filter = specified enrollment status. Filter dropdown only shows statuses set in target segment. | Only students with matching enrollment status AND location can book. |

### AC 5 — [Nozomi] Available Events in Contact (LT-83503)

New related list under Contact → Event History tab: **Available Event List**

Shows event masters where student is eligible (target segment match OR in master participant list) AND event is open to booking / expiration >= today.

Columns: Event master name (hyperlink) | No of available events | Target Location | Target Grade | Target School | Target Course | Description

NOT shown when: event closed to booking OR expiration date < today OR student not in target segment nor participant list.

### AC 6 — [Renseikai] Location Filter in Add Master Staff (LT-96178) — Ready for QA

- Add location filter in Add Master Staff modal (similar to Add Master Participant)
- Pre-populate location filter from Target Location values of the Event Master

---

## Business Rules (Extracted)

| # | Source | Business Rule |
|---|---|---|
| 1 | LT-73558 | Student sees event in booking system if: matches target segment (location/grade/school/course) OR is in master participant list (when target segment is set) |
| 2 | LT-73558 | Student sees event in booking system if: is in master participant list (when target segment is NOT set) |
| 3 | LT-73558 | No student sees event if: neither target segment nor master participant is configured |
| 4 | LT-73558 | Via direct booking link: skip target segment validation and master participant validation |
| 5 | LT-73558 | After successful reservation: student auto-added to Event Master + Activity Event participant records |
| 6 | LT-66652 | Target Location field only accepts center location (lowest level); brand/parent locations not allowed |
| 7 | LT-78534 | If Enrollment Status on Target Location is NULL → Assign to Event defaults to Enrolled+Temporary filter |
| 8 | LT-78534 | If Enrollment Status on Target Location has value → Assign to Event uses only that status; Booking System also restricts to matching status |
| 9 | LT-73558 | Assign to Event location filter = union of target locations + master participant's main locations |
| 10 | LT-73558 | Assign to Event grade filter = union of target grades + master participant's grades |
| 11 | LT-73558 | Who Can Reserve on EM controls which role (Student/Parent) can reserve in booking system |
| 12 | LT-75473 | Parent switching student → must validate new student against target segment or participant list |
| 13 | LT-75474 | Error message when student not in target segment or participant: "The selected student is not eligible for this booking." |
| 14 | LT-82525 | Concurrent reservation edge case: only one student can reserve last slot; other gets capacity error |
| 15 | LT-83503 | Available Event list shows event masters where student matches target segment OR master participant (event open, not expired) |
| 16 | LT-96178 | [Renseikai] Add Master Staff popup has location filter pre-populated from Target Location |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [MISSING BEHAVIOR] | LT-73558 AC | "HQ/CM send booking reminders" case is marked **OUT OF SCOPE** in the epic but LT-74802 was implemented (display target audience by target segment). Scope boundary is unclear. |
| 2 | [ROLE GAP] | LT-73558 | Teacher role behavior in Assign to Event is not defined — only HQ/CM is mentioned. |
| 3 | [MISSING BEHAVIOR] | LT-78534 | Booking system behavior when Enrollment Status set but student has no enrollment record is not specified. |
| 4 | [MISSING BEHAVIOR] | LT-73558 | What happens when student is removed from target segment AFTER having already reserved an event — no rule defined. |
| 5 | [MISSING BEHAVIOR] | LT-73558 | Behavior when event expiration date is updated while students have already booked — not documented. |

### Assumptions Made

- Target Segment is union (OR) across Location/Grade/School/Course — student matching ANY one dimension is eligible.
- "Matching" target location means student's enrolled location equals the target location (not parent hierarchy).
- Master Participant always overrides / supplements target segment (inclusive OR, not exclusive).

---

## Clarification Questions

1. **[ROLE GAP]** Can Teacher role access the Assign to Event function? If yes, what student list do they see?
   _Evidence: LT-73558 AC — only HQ/CM is mentioned in the Assign to Event use case_

2. **[MISSING BEHAVIOR]** If a student is removed from Target Segment after successfully reserving an event, should they be removed from Event Participant automatically or remain?
   _Evidence: LT-73558 — no rule defined for post-reservation segment removal_

3. **[MISSING BEHAVIOR]** What happens in Booking System when Enrollment Status is set on Target Location but a student has no enrollment record at all?
   _Evidence: LT-78534 — only covers students with enrollment records_

4. **[MISSING BEHAVIOR]** Is Target Segment matching OR or AND across dimensions? (e.g., must student match Target Location AND Target Grade, or just one of them?)
   _Evidence: LT-73558 example — ambiguous: EM02 has both Location A and Grade 1; Student A matches both, but spec doesn't clarify if both must match_

---

## Related Specs

- `input/specs/event-master-form-latest.md` — Event Master form fields including Booking Settings (Open to Booking, Expiration Date, Who Can Reserve)

## Related Test Cases

- Qase Suite 443: "Reserve event in booking system by target segment" — 22 existing cases linked to LT-73558
- Qase Suite 113: "Target Segments" — 0 cases (under Master Participant List → Event Master record details)

## QASE Coverage Gaps

- AC 4 (Enrollment Status in Target Segment — LT-78534): No existing TCs in suite 443
- AC 5 (Nozomi Available Events in Contact — LT-83503): No coverage in suite 443 (different feature scope)
- AC 6 (Renseikai Location Filter in Master Staff — LT-96178): No coverage yet (Ready for QA)
- Business Rule 12 (Parent switching student → re-validate): Bug LT-75473 was fixed, regression TC needed
- Business Rule 14 (Concurrent reservation race condition): Needs specific TC
- Business Rule 6 (Center location only, no brand): No explicit TC
