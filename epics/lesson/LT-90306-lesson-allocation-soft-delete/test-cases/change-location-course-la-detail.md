# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 318 — "Change Location Course in LA Detail"](https://app.qase.io/project/PX?suite=318) (10 existing cases). None test the "Change Location" popup's behavior when the Lesson Allocation itself is archived.

Code trace: the "Change Location" button lives in `highlightPanelLessonAllocation.js` (LA Detail highlight panel) → `ModalChangeLessonAllocationLocationCourse` → `LessonAllocationLocationCourseHandler.changeLessonAllocationLocationCourseLWC`. The UI's `isDisableChangeLocationButton` getter only checks `this.isTrialType || !this.lessonAllocation.locationCourseId` — it never checks `isArchived`, which is wired in only to render a "record deleted" banner elsewhere on the panel. So the button is clickable on an archived LA, same class of gap as the "Assign Class" button (suite 1293). Unlike "Assign Class" (which silently succeeds on an archived LA), the Apex side here DOES implicitly block it — but via an unhandled crash, not a validation message: `changeLessonAllocationLocationCourse` does `SELECT ... FROM Lesson_Allocation__c WHERE Id = :lessonAllocationId AND Archived_At__c = NULL` as a single-row assignment with no try/catch. On an archived LA this query returns zero rows, throwing `System.ListException: List has no rows for assignment to SObject`, which surfaces to the user as a raw/generic error toast via the LWC's catch block, not a friendly "this Lesson Allocation is archived" message.

## Suite: Change Location Course in LA Detail

### LA Detail – Change Location Popup – Archived Lesson Allocation – Button Not Disabled; Submit Fails with Unhandled Error Instead of Friendly Validation

**Description:** Gap case — Decision Table — contrasts with the existing baseline cases (1829/11369/11370, which all exercise this popup only on non-archived LAs): on an archived Lesson Allocation, the "Change Location" button is not disabled, so staff can open the popup and attempt a save exactly as if the LA were active, but the save fails server-side with a raw unhandled exception instead of a validation message, because the Apex handler's single-row SOQL excludes archived LAs with no error-handling around it.

**Preconditions:**
- Student A's Lesson Allocation for Math 101 has been archived (Archived_At__c populated) after its Student Package Order was fully removed.
- A different Location Course with an available Class exists as a valid target for the Change Location popup.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's archived Lesson Allocation detail page | The LA Detail page loads; the Archived_At__c field shows a populated timestamp; the "record deleted"/archived banner is shown | Page reachable despite archive, by design |
| 2 | HQ or CM Staff clicks "Change Location" on this archived LA | The Change Location popup opens normally — the button is not disabled, unlike what a staff member might expect given the archived banner is already visible | isDisableChangeLocationButton only checks Trial type / missing Location Course, never Archived_At__c/isArchived |
| 3 | HQ or CM Staff selects a new Location Course and Class, and clicks Save | The save fails; the user sees a raw/generic error toast rather than a clear "this Lesson Allocation is archived and cannot be changed" message | LessonAllocationLocationCourseHandler.changeLessonAllocationLocationCourse's SOQL (`WHERE Id = :lessonAllocationId AND Archived_At__c = NULL`) returns zero rows for an archived LA, throwing an unhandled System.ListException |
| 4 | HQ or CM Staff refreshes the LA Detail page | The LA's Location Course and Class remain unchanged from before the attempted save — no partial update occurred | Archived_At__c still populated; no DML was ever reached in the failed Apex call |

**Severity:** minor
**Priority:** medium

---

### LA Detail – Student Auto-Assigned via Change Location + Class Flow – Lesson Allocation Archived – Hidden from Lesson; Restored – Shown Again with Updated Location/Course/Class

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — continuing from the "Change Location + Class" baseline (case 11369/25014, where changing Location/Course/Class ends the old class member and creates a new one, which then gets auto-assigned into the new class's future lessons): once the Lesson Allocation is later archived, that auto-assigned session is hidden purely by the `Is_Archived__c` formula, and on restore it reappears on the same record, still reflecting the new Location Course and new Class B chosen during the earlier Change Location action — not reverted to the old Class A.

**Preconditions:**
- Student A's Lesson Allocation for Math 101 was active under old Location Course "LC1" and old Class A.
- HQ or CM Staff used the Change Location popup to move Student A's Lesson Allocation to new Location Course "LC2" and new Class B (effective today) — Class A membership was ended, a new Class B membership was created, and Student A is now auto-assigned to Class B's future lessons.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens a future Class B lesson's Student Sessions section | Student A is listed as an active student, under the new Location Course LC2 / Class B | Student A Is_Archived__c = FALSE → shown; Lesson Allocation Location_Course__c = LC2 |
| 2 | The Student Package Order behind Student A's Math 101 Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated; Student A's Class B Student Session flips to archived via the same formula | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens the future Class B lesson's Student Sessions section | Student A no longer appears | Student A Is_Archived__c = TRUE (via formula) → hidden |
| 4 | A living Student Package Order reappears for Student A's Math 101 Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again; Location Course and Class fields still show LC2 / Class B | Archived_At__c = null (restored); Location_Course__c and Class membership untouched by the archive/restore cycle |
| 5 | HQ or CM Staff reopens the future Class B lesson's Student Sessions section | Student A reappears — the same original Student Session created by the Change Location + Class flow, still under LC2 / Class B, not reverted to the old LC1 / Class A | Student A Is_Archived__c = FALSE (restored) → shown again |

**Severity:** major
**Priority:** high

---
