# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

**Purpose:** code trace confirmed these three surfaces (Add Student popup, Calendar student list, Lesson Allocation tab list views) are shared with Core — not forked by Nichibei's `outside-packages/` code (see `test-coverage.md` Addendum 7 for the full trace: `LessonAllocationHandler.cls:92`, `lesson-student-session.query.graphql:85-139`/`student-session.query.graphql:1-30`, and the 8 `Lesson_Allocation__c` list views respectively, all already filtering `Archived_At__c`/`Is_Archived__c`). Since Nichibei runs its own org/deployment, these test cases exist to **manually verify on the live Nichibei org** that the shared code actually behaves as the trace predicts there too — deployment or config drift (profile-specific list view assignments, feature flags, record-type differences) could in principle diverge from what the source code shows, even when the Apex/metadata itself is identical. No existing Qase suite is known for a Nichibei-specific grouping of these three Core features; map to whichever Nichibei suite/location is appropriate at import time, or keep as a standalone ad hoc regression set.

## Suite: Nichibei — Shared Core Surfaces (Add Student / Calendar / LA Tab)

### [Nichibei] Add Student Popup – Archived LA Excluded on the Live Nichibei Org

**Description:** AC-5 (parity) — Regression — manual verification of an already code-confirmed-safe path, run specifically against the Nichibei org to rule out deployment/config drift. Mirrors the Core case already covered in `assign-unassign-student-lesson-schedule.md`.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org.
- A lesson exists for a Nichibei course on 2026-05-20. Student A has a Lesson Allocation for that course, archived (`Archived_At__c` populated, via its order group being fully removed). Student B has an active Lesson Allocation for the same course.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the lesson's Student tab on the Nichibei org and clicks Add Student | The Add Student modal opens | — |
| 2 | HQ or CM Staff searches for Student A and Student B | Student A does not appear (archived); Student B appears (active) | Student A Archived_At__c = populated; Student B Archived_At__c = blank |
| 3 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 4 | HQ or CM Staff reopens Add Student and searches for Student A | Student A now appears, selectable exactly like Student B | Student A Archived_At__c = blank (restored) |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Calendar Student List – Archived Student Hidden on the Live Nichibei Org

**Description:** AC-5 (parity) — Regression — manual verification on the live Nichibei org. Mirrors the Core case already covered in `lesson-calendar-display-archive.md`.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org.
- A lesson on the SF/BO Calendar has Student A (active Lesson Allocation, currently shown in the lesson's student roster) and Student B (active Lesson Allocation).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the lesson from the Calendar and views its student roster | Both Student A and Student B are listed | Both sessions Is_Archived__c = FALSE |
| 2 | The Student Package Order group behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | Student A's Student Session becomes Is_Archived__c = TRUE via formula | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens the lesson from the Calendar and views the roster again | Student A no longer appears; Student B is unaffected | Student A excluded by the roster query's Is_Archived__c = FALSE filter |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | Student A's Student Session returns to Is_Archived__c = FALSE | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens the lesson from the Calendar | Student A reappears in the roster — the same original session, not newly created | Both sessions shown again |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Lesson Allocation Tab – All 8 List Views Exclude an Archived LA on the Live Nichibei Org

**Description:** AC-5 (parity) — Regression — manual verification on the live Nichibei org. Mirrors the Core case already covered in `lesson-allocation-tab-list-views-archive.md`, confirming the same 8 declarative list views (`All`, `All_2023`, `All_2024`, `Fully_Assigned_2024`, `None_Assigned_2024`, `Over_Assigned_2024`, `Partially_Assigned_2024`, `Recently_Updated`) behave identically on Nichibei's deployment, with no additional Nichibei-only view (e.g. a "Not Required Allocation" view) and no profile-specific divergence.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org, with access to the Lesson Allocation tab.
- Student A has a Lesson Allocation for a Nichibei course, Require Allocation = True, Academic Year = 2024, status = Partially Assigned. It currently appears in the `All`, `All_2024`, and `Partially_Assigned_2024` list views.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff navigates to the Lesson Allocation tab on the Nichibei org and confirms the full list of available list views matches the 8 already known from Core (no extra Nichibei-only view, e.g. no separate "Not Required Allocation" view) | Exactly the same 8 views are available, no more, no fewer | List view set = All, All_2023, All_2024, Fully_Assigned_2024, None_Assigned_2024, Over_Assigned_2024, Partially_Assigned_2024, Recently_Updated |
| 2 | HQ or CM Staff confirms the LA appears in `All`, `All_2024`, and `Partially_Assigned_2024` | The LA is visible in all three | Archived_At__c = blank → included |
| 3 | The Student Package Order behind this Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 4 | HQ or CM Staff checks each of the 8 list views in turn | The Lesson Allocation does not appear in any of the 8 views, including `Recently_Updated` despite its LastModifiedDate having just changed | All 8 views share the same Archived_At__c equals (blank) filter |
| 5 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 6 | HQ or CM Staff checks `All`, `All_2024`, and `Partially_Assigned_2024` again | The LA reappears in all three, correctly re-categorized by its actual status, not miscategorized | Archived_At__c = blank (restored) → included |

**Severity:** minor
**Priority:** medium

---
