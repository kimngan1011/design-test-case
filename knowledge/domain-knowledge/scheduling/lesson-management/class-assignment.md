# Class Assignment (Auto-Assign / Auto-Remove + Multi-Class Lessons)

Class-based auto-assignment links students to lessons via Class Member records through the Master Queue. A single lesson can have **multiple classes assigned** (LT-74136, feature-flagged), but the auto-assign/remove behavior is the same regardless of single vs multi-class.

## Auto-Assign / Auto-Remove flow

```
Student ──enrolled in──→ Course ──→ Class ──→ Class Member (with duration)
                                                    │
                                 ┌──────────────────┘
                                 ↓
                          Run Master Queue
                                 │
                    ┌────────────┼────────────┐
                    ↓            ↓            ↓
              Assign student  Remove student  Remain in
              to lesson       from lesson     completed
              (within class   (outside class  lessons
              member duration) member duration)
```

### Triggers

1. Create / import new lesson.
2. Assign a class to student.
3. Update LA duration.
4. Update lesson schedule class (LSC).
5. Add/remove an LSC record via the related list on an existing lesson (multi-class case — students from added class are auto-assigned; from removed class are auto-removed).
6. Bulk Assign Class on UI (Location Course page).
7. Individual Assign Class (Contact page).
8. Bulk Assign Class by Academic Level (Contact page).
9. Class Member Import (Salesforce Import Wizard).

### Behavior

- **Within class member duration** → student is **assigned** to lessons matching the class.
- **Outside class member duration** → student is **removed** from lessons.
- **Completed lessons** → student **remains** even if outside duration (historical preservation).
- **Only ACTIVE class memberships may be used to assign or remove a student — never an already-expired (past) one.** A `Class_Member__c` whose `Effective_End_Date_Time__c` has already passed must not be used to justify touching a Student Session, even if the *lesson's own date* happens to fall inside that now-expired member's historical window. Lessons that already happened under a since-ended class membership are historical data and must be left alone by both the assign and the remove engines — same spirit as "Completed lessons remain," extended to "past class membership" rather than just "past lesson status." **This was violated by `removeAutoAssignedSessionsByRemovedLessonScheduleClasses` (LT-109020's fix) until LT-107584/PR #22445**: when two classes on the same Lesson Schedule were removed together — one Past, one Active — the code iterated *every* Class_Member of the LA (including expired ones) to decide "removed vs. remaining" coverage, so a Past class's own historical lessons got wrongly caught and removed. Fix: the Class_Member query backing that removed/remaining check now adds `Effective_End_Date_Time__c >= TODAY`, so expired memberships are excluded from consideration entirely. **Whether the equivalent auto-*assign* path (`assignSessionsByClass` / `registerLessonStudents`) has the same class of gap has not been separately verified — treat as unconfirmed, not "known safe."**
- **Assignment origin is preserved (mostly).** A Student Session has an `Assignment_Source__c` field (`Auto` / `Manual`, added LT-107584). The core re-scan query (`removeSessionsByClass`) only ever fetches `Assignment_Source__c = Auto` sessions — **Manual sessions are structurally excluded from this query and can never be touched by it**, regardless of duration or class match.
- **Exception — LA end date always wins, even for Auto sessions in a classless lesson.** Inside `removeSessionsByClass`, the very first check is `lesson.Start_Date_Time > LA.End_Date_Time` → remove immediately, **before** the classless-lesson-group check runs. So when an LA's end date is shortened (e.g. Withdrawal, Cancel, LOA, manual duration edit), an **Auto** session past the new end date is removed even if its lesson has no class at all. Only **Manual** sessions are safe there (they never entered the query).
- **Lessons with no class linked at all are otherwise fully protected (LT-108992).** Once a session passes the LA-end-date check, `isLessonGroupWithoutClass` skips it entirely if its lesson's schedule has zero `Lesson_Schedule_Class__c` records — this protects both Auto and Manual-origin data equally (moot for Manual, since Manual never reached the query; meaningful for Auto). This is the fix for the 2026-08-19 incident (LT-109020) where classless lessons were wrongly treated as "invalid" and cleared.

This origin rule applies to all class-based triggers, including creating a lesson with a class, changing or adding a class on an LA, cancelling a scheduled class update, editing classes on Lesson Schedule Detail, and importing Class Members — **except** the "LA end date shortened" case above, which removes Auto sessions unconditionally.

### Duplicate prevention (LT-99546, backfilled LT-104284)

Unique-key constraint on `(student_id, lesson_id)` prevents duplicate Student Sessions when a student belongs to multiple classes assigned to the same lesson. LA Lesson Allocated count increments only once per unique (student, lesson) assignment. Legacy records missing this key were backfilled under LT-104284 after a 2026-06-18 incident (duplicate students on lesson copy) — see `lesson-learned/core.md`.

### Nichibei exception

Nichibei does NOT use class-based auto-assignment. See `../partner-rules/nichibei-lesson-allocation.md`. Its own "Apply to Next X Lessons" assignment flow (Qase suite: Multiple Classes – Student Auto-Assignment / Nichibei-specific suites) is a **separate, parallel Apex implementation** — it does not share the engine below, so a fix to the Core engine does not automatically protect Nichibei's flow and vice versa.

### Performance

Handles 50–100 students per class via async Master Queue batch processing. `ClassMemberMasterQueueExecutor`'s batch chunk size is **2 Lesson_Allocation records per chunk** (`super(2)`) — intentionally small, so a large re-scan spans many chunks/jobs rather than one big transaction.

---

## Engine Internals (code-verified against `erp-salesforce`, reviewed via PR #22428 / LT-108992, 2026-08-20)

This section documents the actual Apex entry points behind each trigger, for anyone who needs to read or modify the code directly. Business behavior above is unchanged; this is the "how".

### Trigger → Apex entry point map

| # | Business trigger | Apex entry point | Notes |
|---|---|---|---|
| 1 | Create / import lesson (bulk, CSV) | `CreateLessonBatchable.doExecute` → `doFinish` | Creates "Assign Class Member" `Master_Queue__c` jobs **chunked within the live DML budget** (`Limits.getLimitDmlRows() - Limits.getDmlRows() - 500`); overflow deferred to `doFinish`, deduped by Lesson Allocation Id across chunks (LT-108992 fix for the 2026-08-18 incident) |
| 3 | Update LA duration | `LessonAllocationHandler.afterUpdate` → `LessonClassMemberHandler.onAfterLessonAllocationChangeDuration` → `updateClassMemberAfterChangeLessonAllocationDuration` | Adjusts each Class_Member's window to fit the new LA duration, or soft-deletes it (`DeletedAt__c`) if there's no overlap at all; then calls `createAssignClassMemberJobs` → re-scan |
| 4–5 | Remove/replace a class on a Lesson Schedule (single LSC record, or deleting a whole Lesson Schedule) | `LessonScheduleClassHandler` / `LessonScheduleHandler` `.removeLessonScheduleClasses` → `LessonClassMemberHandler.removeAutoAssignedSessionsByRemovedLessonScheduleClasses` | **LT-108992 rewrite.** No longer enqueues a broad "Assign Class Member" re-scan job — computes and unassigns only the exact in-scope Auto sessions. Correctly keeps: Manual sessions, Completed-lesson sessions, sessions outside the class member's duration, sessions on other Lesson Schedules, sessions still covered by a *remaining* class on the same schedule (multi-class), and sessions where the same class is linked via a second, non-removed LSC record (duplicate link edge case). **LT-109126 follow-up (PR #22445):** the Class_Member query used for the removed/remaining coverage check now also requires `Effective_End_Date_Time__c >= TODAY` — otherwise an already-expired (Past) class membership could get used to justify removing sessions on lessons that happened *during* that past membership, when it was removed together with an Active class on the same schedule. |
| 6–8 | Bulk/Individual Assign Class (Location Course page, Contact page, Academic Level) | `ClassMemberTrigger` (`Class_Member__c` **AFTER_INSERT only**) → `LessonClassMemberHandler.afterInsert` → `createAssignClassMemberJobs` | **Single shared entry point for every Class_Member insert**, regardless of which UI created it — so the classless-lesson and origin-preservation fixes below apply uniformly to all of these |
| 9 | Class Member Import (SF Import Wizard) | Same as above (`ClassMemberTrigger` AFTER_INSERT) | |
| — | Change Location Course (LA Detail popup) | `LessonAllocationLocationCourseHandler.changeLessonAllocationLocationCourse` — branches on `LessonFeatureToggles.isEnableCancelOldLocationCourseClass()` (`Lesson_Custom_Settings__c.Cancel_Old_Location_Course_Class__c`, **field-metadata default = `false`**) | `LA.Location_Course__c` update always runs first, unconditionally. **Toggle OFF (default) + no new class picked:** the entire branch is skipped — old Class_Member is left **completely untouched** (no date change, no delete). This is correct by design, not a gap: `ClassMemberMasterQueueExecutor`'s match logic (`assignSessionsByClass`/`removeSessionsByClass`) never queries `Location_Course__c` at all, so an old Class_Member pointing at the previous location course still matches and keeps the student's sessions valid. **Toggle OFF + new class picked:** deletes other future-dated ("reserve") Class_Members via `getOtherReserveClassMember`/`deleteOtherReserveClassMember`, then `createClassMember` inserts the new one → insert triggers the normal `ClassMemberTrigger` AFTER_INSERT re-scan. **Toggle ON (opt-in, not the coded default):** `cancelClassMembersOnLocationCourseChange` runs regardless of whether a new class is picked, end-dating/soft-deleting the OLD Class_Member. If no new class is picked in this mode, that end-date is a plain UPDATE — Class_Member has **no AFTER_UPDATE trigger** — so no re-scan is enqueued and the change doesn't propagate to already-assigned sessions. **Live toggle value not confirmed against any specific org** — treat the toggle-ON gap as conditional, not the default path. |
| — | General re-scan (assign + remove together) | `ClassMemberMasterQueueExecutor` (`Master_Queue__c.Apex_Class_Name__c = 'ClassMemberMasterQueueExecutor'`, registered as `MasterQueueHandler.Executors.ASSIGN_CLASS_MEMBER`) | `doExecute` → `removeSessionsByClass` (see order-of-checks above) + `assignSessionsByClass`. This is what every "create Assign Class Member job" call above ultimately runs. |

**Dead code warning:** `AssignClassMemberBatchable.cls` still exists in the repo and implements the same kind of assign/remove logic (its own query has **no** `Assignment_Source__c` filter at all), but it is **not** registered in `MasterQueueHandler.Executors` and nothing else in the codebase references it. Treat it as legacy/orphaned — do not confuse it with `ClassMemberMasterQueueExecutor` when reading code or logs.

### Caller map — `LessonClassMemberHandler` blast radius

Useful when assessing how far a change inside this class can reach. Each method below is a separate, independent code path — a change scoped to one method does **not** affect the others.

| Method | Called from | Business trigger |
|---|---|---|
| `removeAutoAssignedSessionsByRemovedLessonScheduleClasses` | `LessonScheduleClassHandler.removeLessonScheduleClasses`, `LessonScheduleHandler.removeLessonScheduleClasses` | Remove a class from a Lesson Schedule (single LSC via related list, or cascading from a schedule-level change) — the **only** two callers of this specific method |
| `createAssignClassMemberJobByClassIds` | `LessonScheduleClassHandler` (adding a class), `LessonScheduleHandler` (3 call sites), `UpdateLessonHandler` (2 call sites) | The broad, pre-LT-108992-style re-scan — still the live code path whenever a class is *added* (not removed), or on other lesson-update flows |
| `onAfterLessonAllocationChangeDuration` | `LessonAllocationHandler.afterUpdate` | Update LA duration |
| `cancelClassMembersOnLocationCourseChange` | `LessonAllocationLocationCourseHandler.changeLessonAllocationLocationCourse` | Change Location Course |
| `assignClassMemberByOrderGroupClass` | `BatchInsertStudentSession`, `BatchStudentSessionCreation`, `LessonAllocationHandler.afterUpdate` | Order Group class assignment |
| `assignClassMemberToLessonWithMultipleClasses` | `LessonScheduleHandler` (multi-class lesson creation) | Creating a new multi-class lesson |
| `createAssignClassMemberJobs` (+ overloads) | Many call sites (Bulk/Individual Assign, Import, `resyncClassMemberByLessonAllocationId`, etc.) | Enqueues the general `ClassMemberMasterQueueExecutor` re-scan |

**Why the LT-109126 bug was isolated to just one method:** `ClassMemberMasterQueueExecutor.doStart()` (the general re-scan engine, used by every trigger *except* "remove a class from a Lesson Schedule") already filters its Class_Member subquery with `Effective_End_Date_Time__c >= TODAY` — it was never vulnerable to this bug. `removeAutoAssignedSessionsByRemovedLessonScheduleClasses` was written as a brand-new, separate query in LT-108992 and simply didn't carry over that same filter. Lesson for future changes in this class: **when adding a new Class_Member query here, check whether the existing `doStart()` filter pattern (`Effective_End_Date_Time__c >= TODAY AND DeletedAt__c = NULL`) should be replicated** rather than re-deriving the WHERE clause from scratch.

### Fix lineage (chronological)

| Ticket | Merged | What it changed |
|---|---|---|
| LT-99546 | — | `Unique_Key__c` (student, lesson) constraint — dedup on assignment. Fix for 2026-04-13 incident. |
| LT-104284 | — | Backfilled `Unique_Key__c` on legacy Student Sessions. Fix for 2026-06-18 incident. |
| **LT-107584** | 2026-07-31 | Added `Assignment_Source__c` field + `= Auto` filter to `removeSessionsByClass`. No backfill for pre-existing records (confirmed with Dev as not required) — legacy sessions simply have `Assignment_Source__c = NULL` and are excluded from this query either way, same as Manual. |
| **LT-108992** (PR #22428) | 2026-08 | `isLessonGroupWithoutClass` guard in `ClassMemberMasterQueueExecutor`; DML-budget-aware chunking in `CreateLessonBatchable`; precise `removeAutoAssignedSessionsByRemovedLessonScheduleClasses` replacing the broad re-scan on class removal; per-class-name validation caching in `MasterQueueHandler`. Fixes the 2026-08-18 (MANACS-2540) and 2026-08-19 (LT-109020) incidents. |
| **LT-109126** (PR #22445, branch tagged LT-107584) | open, not yet merged as of 2026-08-21 | 1-line fix: added `Effective_End_Date_Time__c >= TODAY` to the Class_Member query inside `removeAutoAssignedSessionsByRemovedLessonScheduleClasses`, so an already-expired class membership can no longer be used to justify removing sessions on lessons that occurred during it. Found via QA testing of the LT-108992 hotfix, days after that PR merged — see bullet above in Behavior. PR bundles an unrelated cleanup (deletes the obsolete `Migrate1037` one-time migration + its test) — low risk on its own, but scope creep worth calling out in review. **No new/updated Apex test accompanies the fix** — nothing in the codebase's automated suite guards this exact scenario (past + active class removed together) from regressing; coverage currently relies solely on the Qase manual case (PX-13960, rewritten 2026-08-20). |

### Known unresolved risks (as of 2026-08-21)

1. **LSC removal is synchronous and unbatched.** `removeAutoAssignedSessionsByRemovedLessonScheduleClasses` is called directly from `@AuraEnabled LessonScheduleClassHandler.lwcRemoveLessonScheduleClasses` (the "remove class" button in the UI) — one query, one `Database.update` for the whole affected list, inside the LWC's own transaction. A class removal affecting >10,000 eligible sessions (plausible at Renseikai's scale) would throw a DML-row-limit exception. Flagged by automated review on PR #22428, not addressed as of merge.
2. **Change Location Course without picking a new class — conditional on `Cancel_Old_Location_Course_Class__c`, field-metadata default `false`.** Under the default (toggle OFF), this is correct behavior, not a gap — the old Class_Member is left untouched and the auto-engine never checks `Location_Course__c` anyway. The real (narrower) open risk is toggle-ON: old Class_Member gets end-dated with no re-scan afterward (Class_Member has no AFTER_UPDATE trigger), leaving stale sessions. Live toggle value not confirmed against any specific org (see table above).
3. **Reallocation (`ReallocationHandler.cls`) and Nichibei's own assignment flow are separate code, not audited** for the same origin-preservation/classless-lesson protections during this review — treat as unverified, not "known safe".
4. **The "active class member only" rule (see Behavior above) has only been confirmed fixed on the *remove* path (LT-109126/PR #22445).** The *assign* path (`assignSessionsByClass` / `registerLessonStudents` in `ClassMemberMasterQueueExecutor`) has not been independently checked for the same class of bug (using an expired Class_Member to justify a new assignment) — unconfirmed, follow up if similar symptoms appear on the assign side.

---

## Multiple Classes per Lesson (LT-74136, 2026-05-18)

Core feature (all orgs). Extends lesson creation from single-class to multi-class via a new **Lesson Schedule Class (LSC)** junction object. **Only the lesson creation/configuration changes — the auto-assign/auto-remove behavior above is unchanged.**

### Feature Flags

| Flag | Type | Purpose |
|---|---|---|
| `Multiple_Classes_In_Lesson__c` | SF Custom Setting | Enables multi-class selection on SF lesson creation UI |
| `Lesson_BackOffice_LessonSF_MultipleClassesSF` | Unleash | Enables multi-class display on BO and Calendar |

**When flag is OFF:** System reverts to single-class behavior. Class field shows as single-select. Already-created multi-class lessons display as single class.

### Lesson Schedule Class (LSC)

Junction object linking a Lesson Schedule to multiple Class records.

| Field | Type | Notes |
|---|---|---|
| Lesson Schedule | Master-Detail (parent) | Cascade-deletes LSC when LS deleted |
| Class | Lookup | Links to Class record |

- **Deprecated:** `Class` field on `Lesson Schedule` object — migrated to LSC at DB level; **not shown on any UI surface** (SF or BO) post-migration.
- **Class formula field on Lesson:** auto-calculated from LSC records; displays comma-separated class names.

### Class Selection Rules (SF Lesson Creation)

- Multi-select field: staff can select **multiple classes under the same course** when creating a lesson.
- **Recurring lessons:** all selected classes applied to every lesson in the chain upon generation.
- **Course field + Class field: locked (non-editable) after lesson creation via the Lesson form.**
- **Post-creation edit via LSC related list:** Staff CAN add/remove Lesson Schedule Class records via the related list on an existing lesson. When a class is removed, students from that class are auto-removed; when added, students from that class are auto-assigned (per the auto-assign/auto-remove flow above).

### CSV Import Rules

| Teaching Method | Class field behavior |
|---|---|
| **Group** | Multi-class supported; semicolon-delimited (e.g., `Class A;Class B`) |
| **Individual** | Class field **hidden** — multi-class input not possible |

**New import steps (To-Be):**
1. Create Lesson Schedule
2. Create Lesson Schedule Class (one LSC per class)
3. Create Lesson (Class field = formula from LSC)
4. Create Lesson Teacher
5. Create Lesson Assignment (Student Sessions)

**Access:** All SF users who can log into SF can perform CSV import — no role restriction.

### Class Schedule Related List (on Class Record)

- Updated on **both SF and BO** Class detail views.
- Source changed from Lesson Schedule → Lesson Schedule Class.
- Tab label: **Class Schedule**.
- Columns: Lesson Name, Start Date, End Date, Lesson Schedule hyperlink.

### Display Format

| Platform | Surface | Display |
|---|---|---|
| SF | Lesson List, Lesson Detail, Lesson Schedule Detail, Compact Layout | Comma-separated class names (from LSC) |
| SF | Calendar lesson card (Group) | Multiple classes shown |
| BO | Lesson List, Lesson Detail | Comma-separated class names (from LSC) |
| BO | Calendar lesson card (Group) | Multiple classes shown |
| Mobile | Calendar Lesson detail | Classes from LSC |

### Calendar Class Filter

Both SF and BO Calendar class filter use **ALL-match** (AND) logic — see `../calendar/calendar-sf.md` § Multiple Classes on Calendar.
