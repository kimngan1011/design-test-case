# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 3305 — "Class Member Import"](https://app.qase.io/project/PX?suite=3305) (2 existing cases, under "Withus Juku | Allowing past dates for Classmember start date", LT-107256, parent 3303). None of the 2 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace confirmation — confirmed new gap.** The shared "Allow Class Member Start In The Past" validator (`LessonClassMemberHandler.cls`, `ClassMemberValidator.retrieveData`/`validateClassMember`, lines 73-96) looks up the target Lesson Allocation with `Archived_At__c = NULL`; if the LA is archived, it's simply absent from the result map, and `validateClassMember` **returns early with no error** (lines 94-96) instead of rejecting the insert — this early-return path was built to skip validation for a missing/invalid Id, not to explicitly block an archived one. Every OTHER entry point for this feature (Contact/Course picker, Location Course, LA Student Session, Bulk Assign) is protected because their pickers already exclude archived LAs from being selectable at all (`LessonAllocationController.cls:15`). Import is the one path that bypasses this protection, since it works from a typed/file-provided Lesson Allocation reference rather than the UI picker.

## Suite: Class Member Import

### [WithUs Juku] Class Member Import – Archived LA Referenced – Backdated Class Member Silently Created, No Error Shown

**Description:** AC-5 — Negative — confirmed gap. Contrasts with existing baseline (#26091 "Import – Date Before LA Start – Exact validation message shown", which only tests the date-boundary error, not an archived target). Since the shared validator silently skips validation when the referenced LA is archived, an import file pointing at an archived Lesson Allocation is expected to succeed and create a Class Member against it — the opposite of the intended protection.

**Preconditions:**
- HQ or CM Staff has Class Member import access to the Withus Juku Salesforce org.
- Student A's Course A Lesson Allocation is archived (`Archived_At__c` populated, via its order group being fully removed) — it would otherwise be a valid target (start 2026-08-01, end 2026-12-31) if still active.
- The import file contains one row: Student A, Class A, effective date = 2026-08-01 (matching the archived LA's own start date), referencing the archived LA's Id or the Student+Course combination that resolves to it.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Import Class Member and uploads the prepared file | The preview shows the submitted row | today = 2026-08-12; import rows = 1 |
| 2 | HQ or CM Staff starts the import | Per AC-5, this should be rejected — the referenced Lesson Allocation is archived and should not accept a new Class Member | LA Archived_At__c = populated |
| 3 | HQ or CM Staff checks the import result and Student A's Class Member history | [Confirmed by code] The import completes with no error shown; a new Class A Class Member is created, start date 2026-08-01, linked to the archived LA (fail — route to the engineering owner of `LessonClassMemberHandler.validateClassMember`, which needs an explicit archived-LA rejection branch instead of its current empty-map early-return) | `validateClassMember` returns early with no error when the LA is absent from `lessonAllocationMap` (archived) |

**Severity:** critical
**Priority:** high

---
