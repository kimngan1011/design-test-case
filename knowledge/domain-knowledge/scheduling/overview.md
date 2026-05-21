# Manabie Scheduling — Overview

> **Purpose:** Reference document for QA analysis. Read this for orientation, then deep-read the specific sub-domain files relevant to the ticket.
> **Last updated:** 2026-05-21
> **Source:** 4,191 test cases (Qase PX suite 18), 11 system diagrams.

This folder is split per sub-domain. Use the file index below to scope your reading.

---

## 1. System Overview

Manabie Scheduling is a lesson-scheduling and event-management platform used by Japanese education companies. It runs across **three platforms**:

| Platform | Role | Users |
|---|---|---|
| **Salesforce (SF)** | Primary management UI | Staff (HQ Admin, Centre Manager, Centre Staff) |
| **Back Office (BO)** | Teaching and lesson delivery | Teachers (CPU/SPU), Centre Managers |
| **Learner App (Mobile)** | Viewing and attendance | Students, Parents |

Data flows **SF → BO → Mobile**. SF is the source of truth for lesson creation and student/teacher management. BO syncs from SF and extends with teaching features (reports, materials, Zoom). Mobile shows published lessons and reports.

---

## 2. Cross-domain interactions

### Lesson ↔ Calendar

```
Lesson (SF) ──create/edit──→ Calendar (SF) ──view──→ Calendar (BO)
                                  │
                                  ├── Drag & Drop to reschedule
                                  ├── Click to view/edit lesson detail
                                  ├── Teacher clashing alerts
                                  └── Filter by location/teacher/student
```

- Lessons created on SF auto-appear on SF Calendar and sync to BO Calendar.
- Calendar provides visual management: drag-and-drop reschedule, click-to-edit.
- Teacher clashing alerts show on both Calendar and Lesson detail.
- Calendar views filter lessons by the user's access level (CPU sees own lessons, SPU sees location lessons).

### Lesson ↔ Event

```
Event Master ──creates──→ Activity Event ──shown on──→ Calendar (SF + BO)
                               │
                               ├── Assign staff ──→ staff sees on SF Calendar
                               ├── Assign students ──→ students see on Mobile
                               └── Booking system ──→ reserves slots
```

- Events and Lessons coexist on the Calendar.
- Events can assign staff (teachers) who see them on their calendar, similar to lesson teacher view.
- Students see assigned events on Mobile Learner App.
- Both events and lessons respect location-based access control.

---

## 3. File index — read by name match

When analyzing a Jira ticket, scan the filenames below and **deep-read only the files whose name matches keywords in the spec** (entities, features, partners).

### Lesson Management (`lesson-management/`)
- `lesson.md` — Lesson entity, recurrence, status transitions, CRUD, lesson code, end-date logic, closed-date skipping, edit rules, Zoom, lesson report, sync direction.
- `lesson-allocation.md` — Core LA authorization model (Require Allocation, Duration, lifecycle, order coupling).
- `student-session.md` — Student Session entity, assignment methods, recurring scope rules, filter rules, name display.
- `class-assignment.md` — Class-based auto-assign/auto-remove + Multiple Classes per Lesson (LT-74136).
- `lesson-teacher.md` — Lesson Teacher entity, clashing alert, cross-location access, Monthly Lesson Count (LT-96673).
- `lesson-mobile.md` — Mobile (Learner App) viewing + Publish & Notify (Renseikai LT-96662) + Nichibei silent auto-publish.

### Event (`event/`)
- `event-master.md` — Event Master record, Target Segments, Master Record Details.
- `activity-event.md` — Activity Event instances, Learner App Activity Card.
- `booking-system.md` — Internal + External booking (Reserve, Notification, External link).
- `events-on-calendar.md` — Event display on SF/BO Calendar.

### Calendar (`calendar/`)
- `calendar-sf.md` — SF Calendar features (560 cases): Lesson CRUD, views, drag & drop, multi-class display, clashing alert, filter + Bulk Publish (Riso LT-98532).
- `calendar-bo.md` — BO Calendar features (224 cases) including Renseikai Bulk Attendance Update.
- `student-teacher-reallocation-list.md` — Core feature (114 cases): the three contextual lists on SF Calendar lesson detail.
- `access-by-user-type.md` — Calendar access matrix; CPU vs SPU distinction (Aver-specific) vs affiliation-based (other partners).

### Partner-specific (`partner-rules/`)
- `nichibei-lesson-booking.md` — Self-booking from Learner App, Bookable Flag, cancel rules (LT-96620), BO Lesson List enhancements (LT-96616).
- `nichibei-lesson-allocation.md` — Point consumption model: priority chain, point refund, reallocation, trial, limit teacher, lesson syllabus, point consumption report.
- `riso-lesson-allocation.md` — Manual UI LA creation (no order), purchased slot, subject in lesson (LT-94698), CSV import.
- `koyu-event-features.md` — Koyu Auto Create Application, Cancel Booked Event, Update Cancel, Draft Status.

### Lesson-learned (`lesson-learned/`)
- `core.md` — Production incidents affecting all partners.
- `oop.md` — Partner-specific production incidents.

### Permission matrix
- `scheduling-feature-permission-matrix.csv` — Role × feature access baseline.

---

## 4. Customization by Organization

| Organization | Key Features | Cases |
|---|---|---:|
| **Aver** | Extended lesson reports (203), Permission (9), Test prep/Subject (24), Lesson Report corrections (178) | 414 |
| **Aso** | Lesson Survey (12), Student Group (41), Curriculum & Syllabus (219), Class enforcement (7) | 279 |
| **Renseikai/Rensei** | Collect attendance SF (2)/BO (2), Configure error messages (15), Bulk attendance (34), Class name uniqueness (8), Collect Attendance new entry points (LT-96152), Publish and notify (LT-96662) | 61+ |
| **Nichibei** | Point Consumption (145), Lesson Syllabus (24), Limit Teacher (6), Reallocation (26), Trial Lesson (20) | 221 |
| **Withus Juku** | Lesson/Course (9), Event management (59), Custom event (23) | 91 |
| **EEA** | Acquire Teacher (20), Dual Lesson (40) | 60 |
| **Riso** | Lesson Allocation management (80), Subject in Lesson Detail (25), Monthly Lesson Count (LT-96673), Bulk Publish (LT-98532) | 105 |
| **Koyu** | Auto Create Application (51), Cancel Booked Event (68), Update Cancel (65), Draft Status (19) | 203 |

---

## 5. Master Data

| Entity | Description | Impact |
|---|---|---|
| **Academic Calendar Master (ACM)** | Year-based calendar per location; contains Closed Dates | Closed dates skip lesson creation; 94 test cases |
| **Academic Calendar Item (ACI)** | Individual closed date entry within ACM | Lesson and LA duration calculation |
| **Location** | Physical center/school | Scopes courses, classes, teachers, students, calendars |
| **Course Master** | Course definition; linked to Course Category | Determines lesson type, point consumption |
| **Course Category** | Groups courses; defines Point Consumption value | Point calculation base |
| **Program Master** | Defines week orders for Course Schedule lessons | Controls course schedule recurrence |
| **Class** | Group of students within a course at a location | Auto-assignment of students to lessons |
| **Classroom** | Physical room at a location | Assigned to lessons for capacity |
| **Student Group** | Custom grouping of students | Filtered by location; supports bulk class assign |

---

## 6. Key Data Relationships

```
Location
├── Academic Calendar Master → Academic Calendar Items (Closed Dates)
├── Course → Class → Class Member (Student)
├── Classroom
├── Teacher (via Affiliation)
└── Student (via Affiliation)

Student
├── Student Product Offering (SPO) → Lesson Allocation (LA)
├── Class Member → auto-assigned to Lessons
└── Student Session → Lesson

Lesson
├── Lesson Schedule (chain)
├── Lesson Report → Lesson Report Detail (per student)
├── Student Session (students)
├── Lesson Teacher (teachers)
├── Zoom Link (online)
└── Calendar (view)

Event Master
├── Target Segments (Location, School, Grade, Course)
├── Master Participants / Master Staff
├── Activity Event → Booking
└── Calendar (view)
```

---

## 7. Test Coverage Summary (4,191 cases)

| Domain | Cases | % |
|---|---:|---:|
| Lesson Management | 1,495 | 35.7% |
| Customization | 1,134 | 27.1% |
| Calendar | 784 | 18.7% |
| Event Master | 568 | 13.6% |
| Master Data | 104 | 2.5% |
| Extend Recurring Lesson | 64 | 1.5% |
| SF Report | 18 | 0.4% |
| Incident Prevention | 16 | 0.4% |
| Configuration | 3 | 0.1% |
| Lesson Master | 3 | 0.1% |
| Live Lesson | 2 | 0.0% |
