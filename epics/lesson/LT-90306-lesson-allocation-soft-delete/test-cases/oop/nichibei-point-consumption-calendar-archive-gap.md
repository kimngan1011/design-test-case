# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 624 — "Calendar"](https://app.qase.io/project/PX?suite=624) (16 existing cases, under OOP FEATURES → Nichibei → Point Consumption, parent 372). This suite duplicates the same business logic as sibling suite 373 ("Lesson detail") from a different entry point (Calendar page instead of Lesson detail page) — the existing 16 cases are the Calendar-suite twins of suite 373's 15 cases (e.g. #6779 ~ #2794, #6784/#8540 ~ #2802). This is spec.md's single highest-risk OOP impact: "LA is the financial authorization record... an archived LA must not be selected in the priority chain or have points consumed from it" — a release blocker tied to a prior production incident (Lesson-Learned Risk #2, 2026-03-04: sessions ended up with no LA and incorrect point totals).

**Business logic (fully specified by the existing cases, used as ground truth):** when a student is assigned to a lesson, the system picks ONE Lesson Allocation to deduct points from: prefer a course-matching LA over a "general" one, then `Priority = TRUE`, then an LA whose duration covers the lesson date, then fewer remaining points, tie-broken by earlier created date. A recurring lesson can draw from a different LA per occurrence. Removing a student or deleting a lesson refunds the points to the same LA they came from. None of the 16 existing cases reference `Archived_At__c`/`Is_Archived__c` — the archive dimension is new. These test cases mirror `nichibei-point-consumption-lesson-detail-archive-gap.md` (suite 373), re-entered from the Calendar page to match this suite's own entry point, per the same 1:1 duplication pattern already used by the existing cases.

**Code-trace note:** the real production selection method (`StudentSessionHandlerOutSide.assignStudentToLesson`) is invoked via Apex reflection and is not present in `erp-salesforce` (confirmed by an explicit test comment). The business logic itself is fully known from the cases above; only the archive-filter implementation is unverifiable by code, so cases below are marked [UNVERIFIED] where they depend on the actual selection/refund implementation. The simpler fallback booking path (non-"custom assign", `BookingLessonHandlerOutSide.cls:638-651`) already filters `Archived_At__c = NULL` — included below as a control case, not a gap.

**Scope note:** spec's open Clarification Question #2 (should archiving itself trigger a refund/hold/leave-as-is policy change, does unarchive re-consume) is a forward-looking product decision, out of scope here. What's testable now, per this epic's existing AC-3/AC-8 design principles: an archived LA must never be newly selected; a normal refund must still land on the correct (same-Id) LA even if it has since archived; unarchive does not retroactively re-run consumption.

## Suite: Calendar

### [Nichibei] Point Consumption – Priority Chain – Archived LA Excluded Even When It Would Otherwise Win – Points Taken From Next Eligible LA

**Description:** AC-5 (financial) — Decision Table — [UNVERIFIED]. Contrasts with existing baseline (#6779 "Taking points from LA with specific cases"). An LA that would win the priority chain on every documented criterion (matching course, `Priority__c = TRUE`, duration covers the lesson date, sufficient points) must still be excluded if it is archived; the system should fall through to the next eligible non-archived LA instead.

**Preconditions:**
- Course 3 has Number of point = 5, General flag = False.
- LA3 + Course 3: Required Allocation = False, Priority = True, Purchase Point = 10 — this LA would win the priority chain under every existing documented rule.
- LA3's `Archived_At__c` is populated (archived via its order group being fully removed), while LA4 + Course 3 also exists: Required Allocation = False, Priority = False, Purchase Point = 10 (the next-best eligible candidate).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff creates a group lesson with Course 3 from the Calendar, with the lesson date within the duration of LA3 and LA4, and assigns Student 1 to the lesson | Per AC-5's exclusion principle, LA3 should not be selected despite matching every priority-chain criterion, since it is archived | LA3 Archived_At__c = populated |
| 2 | HQ or CM Staff checks which LA the points were taken from | [UNVERIFIED] Record actual behavior: 5 points taken from LA4 (correct fallback, pass), or points taken from archived LA3 (fail — critical, financial data written against an archived allocation) | Actual result to be captured against live Nichibei org |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Point Consumption – Priority Chain – Archived LA's Duration Still Covers Lesson Date – Still Excluded From Selection

**Description:** AC-5 (financial) — Decision Table — [UNVERIFIED]. Contrasts with existing baseline (#6780 "Taking point from LA that has the duration to cover the lesson date"). An LA whose `Start/End_Date_Time__c` range still technically covers the lesson date is not eligible if it is archived — archive must override a duration match, not just be one more input alongside it.

**Preconditions:**
- LA2 + Course 2 (general course): Priority = True, Purchase Point = 20, Duration 2025-03-01–2025-07-01.
- LA3 + Course 3: Priority = True, Purchase Point = 10, Duration 2025-04-01–2025-06-01 — its duration covers the target lesson date and it would normally be preferred as the matching-course LA.
- LA3's `Archived_At__c` is populated.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff creates a group lesson with Course 3 from the Calendar, lesson date = 2025-04-15 (within LA3's duration), and assigns Student 1 | Per AC-5, LA3 remains ineligible despite its duration covering the date, because it is archived | LA3 Archived_At__c = populated; lesson_date = 2025-04-15 |
| 2 | HQ or CM Staff checks which LA the points were taken from | [UNVERIFIED] Record actual behavior: points taken from LA2 (the general-course fallback, pass), or from archived LA3 because its duration still matched (fail) | Actual result to be captured against live Nichibei org |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Point Consumption – No Non-Archived LA Available – Error Shown, Archived LA Not Silently Used

**Description:** AC-5 (financial) — Negative — [UNVERIFIED]. Contrasts with existing baseline (#6786 "There is no available point to take a point", #6792 "There is no available LA to take a point"). When the only LA(s) that would otherwise be eligible for a course are archived, the system must show the same "no available LA" error as today — it must never silently fall back to consuming from an archived LA just because nothing else qualifies.

**Preconditions:**
- Course 3 has no other eligible LA besides LA3; LA3 + Course 3 is archived (`Archived_At__c` populated).
- No general-course LA with remaining points is available either.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff creates a group lesson with Course 3 from the Calendar and assigns Student 1 to the lesson | Per AC-5, the system should behave exactly as it does today when no eligible LA exists at all — show the error message, do not assign the student by silently drawing from the archived LA | LA3 Archived_At__c = populated; no other eligible LA |
| 2 | HQ or CM Staff checks the assignment result | [UNVERIFIED] Record actual behavior: error message shown, student not assigned, no points touched on the archived LA (pass), or the student is silently assigned and points are deducted from the archived LA (fail — critical) | Actual result to be captured against live Nichibei org |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Point Consumption – Recurring Lesson – LA Archived Mid-Split – Remaining Occurrences Re-Split Across Only Non-Archived LAs

**Description:** AC-5 (financial) — State Transition — [UNVERIFIED]. Contrasts with existing baseline (#6784/#8540 "Taking point from LA for the recurring lesson" / "...daily/weekly/custom lesson", a 4-lesson split across LA2/LA3). If one of the LAs used mid-split archives between assigning the first and a later occurrence, the later occurrence's split must be recomputed using only the LAs that are still non-archived at the time of that assignment.

**Preconditions:**
- Same setup as #6784: LA2 (general, Purchase Point 20) and LA3 (Course 3, Purchase Point 10, Duration 2025-04-01–2025-06-01). A recurring group lesson with Course 3, created from the Calendar, has its 1st occurrence outside LA3's duration, 2nd onward within it.
- Student 1 is assigned to the 2nd occurrence only first (per #6784 step 1), drawing 7 points from LA3.
- Before assigning "this and the following" from the 1st occurrence, LA3's `Archived_At__c` becomes populated (its order group is fully removed).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the 1st occurrence from the Calendar and assigns Student 1 with "this and the following lesson" | Per AC-5, every occurrence that would have drawn from LA3 under the original split must now draw entirely from LA2 (or the next eligible non-archived LA), since LA3 is no longer selectable | LA3 Archived_At__c = populated before this action |
| 2 | HQ or CM Staff checks the points taken for each of the 1st–4th occurrences | [UNVERIFIED] Record actual behavior: all 4 occurrences now draw only from LA2 (or correctly fail/skip occurrences with no eligible LA, consistent with the "no available LA" case above) — never silently drawing any points from archived LA3 | Actual result to be captured against live Nichibei org |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Point Consumption – Remove Student / Delete Lesson – Refund Returns to Same LA Even If Now Archived

**Description:** AC-3 / AC-8 (financial) — Regression — [UNVERIFIED]. Contrasts with existing baseline (#6788 "Remove a student from the one-time lesson", #6790 "Delete the one-time lesson", #6793 "Delete the recurring lesson"). Per AC-3/AC-8's design principle (archive is a pure timestamp write that must not block other legitimate writes, and archiving never deletes financial history), a normal refund triggered by removing a student or deleting a lesson must still write the returned points back to the correct LA, identified by the same record Id, even if that LA has since archived.

**Preconditions:**
- Student 1 was assigned to a lesson with 5 points consumed from LA3 (per the baseline case #6779/#6788 setup).
- LA3's `Archived_At__c` becomes populated (its order group is fully removed) after the points were consumed but before the student is removed from the lesson.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff removes Student 1 from the lesson via the Calendar | Per AC-3/AC-8, the refund should still succeed and write 5 points back onto LA3 (same Id), consistent with archiving never blocking a legitimate write to an archived record | LA3 Archived_At__c = populated at time of removal |
| 2 | HQ or CM Staff checks LA3's remaining points and the student's total remaining | [UNVERIFIED] Record actual behavior: LA3's remaining points correctly increase by 5 and the student's total remaining is recalculated (pass), or the refund silently fails / errors / is written to the wrong LA because the write path doesn't expect an archived target (fail — route to the engineering owner of `[SF][Nichibei] Implement LA soft delete with consume point`) | Actual result to be captured against live Nichibei org |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Point Consumption – Custom Assign Disabled – Fallback Booking Path Already Excludes Archived LA

**Description:** AC-1 (parity) — Regression — control case, not a gap. Code-confirmed: `BookingLessonHandlerOutSide.cls:638-651` already filters `Archived_At__c = NULL` on the simpler, non-"custom assign" LA-selection query. This case locks in that the fallback path (used when `Use_Custom_Assign_Unassign_Student__c = FALSE`) is already correct and unaffected by this epic, regardless of whether booking is entered from the Calendar or Lesson detail.

**Preconditions:**
- Nichibei's "Use Custom Assign/Unassign Student" setting is disabled.
- Student 1 has an eligible LA (LA-X, `Required_Allocation__c = TRUE`, `Type__c` includes "Regular") whose duration covers the target lesson date, and a second LA (LA-Y, same course, otherwise eligible) that is archived (`Archived_At__c` populated).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student books/is assigned to a lesson from the Calendar via the fallback (non-custom-assign) path | The booking query filters out LA-Y by `Archived_At__c = NULL` and picks the earliest-starting eligible LA among the remaining candidates — LA-X is selected | LA-Y Archived_At__c = populated; LA-X Archived_At__c = null |
| 2 | HQ or CM Staff confirms which LA the booking drew from | LA-X — confirms this path requires no new coverage, since the archive filter is already present | Code-confirmed via `BookingLessonHandlerOutSide.cls:638-651` |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Point Consumption – Unarchive – No Automatic Re-Consumption for Historical Sessions

**Description:** AC-3 — Regression. Confirms that restoring an archived LA does not retroactively re-trigger point consumption for sessions whose points were already recorded before the archive — consistent with this epic's design principle that unarchive only restores visibility/state (`Archived_At__c` cleared, same Id) and recomputes forward-looking fields (duration, slot count), never replays past consumption events. This is distinct from, and does not resolve, the still-open policy question of whether archiving itself should trigger a refund (spec Clarification Question #2).

**Preconditions:**
- LA3 was archived with 5 points already consumed and recorded against it for a past session.
- A living Student Package Order reappears for the same `Student_Course_ID__c` group, and LA3 is unarchived on the same record Id.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms LA3 is restored (`Archived_At__c` cleared, same Id) via the Calendar | LA3's remaining points reflect the same balance it had at the moment of archiving (5 points still recorded as consumed from the past session) — not re-added, not re-deducted | LA3 Archived_At__c = null (restored) |
| 2 | HQ or CM Staff checks whether the past session's consumption record changed as a result of the unarchive | No new consumption event is created, and the original consumption record is untouched | Expect: 1 consumption record for the past session, unchanged |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Point Consumption – Unarchive – Restored LA Is Selectable Again in the Priority Chain for New Assignments

**Description:** AC-3 (financial) — Regression — [UNVERIFIED]. Direct inverse of the exclusion cases above: once an LA is unarchived (same Id, `Archived_At__c` cleared), it must become a normal, fully eligible candidate again — selectable by the priority chain for a brand-new lesson assignment exactly as if it had never been archived. Restoring must not leave the LA in a permanently-skipped or degraded state.

**Preconditions:**
- LA3 + Course 3 (Priority = True, Purchase Point = 10, remaining points = 10, i.e. nothing consumed from it since restore) was previously archived and is now unarchived on the same record Id (`Archived_At__c` cleared) — a living Student Package Order reappeared for the same `Student_Course_ID__c` group.
- No other LA for Course 3 currently outranks LA3 in the priority chain (matching course, Priority = True, duration covers the lesson date).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff creates a new group lesson with Course 3 from the Calendar, with the lesson date within LA3's duration, and assigns Student 2 (a different student, not involved in the earlier archive/unarchive cycle) to the lesson | Per AC-3, a restored LA must behave exactly like any other eligible, never-archived LA — it competes in the priority chain on its own merits, with archive history having no lingering effect | LA3 Archived_At__c = null (restored); LA3 is otherwise the best-matching candidate |
| 2 | HQ or CM Staff checks which LA the points were taken from | [UNVERIFIED] Record actual behavior: points correctly taken from LA3 (restore fully functional, pass), or LA3 is still skipped/ignored by the selection logic even though `Archived_At__c` is now null (fail — restore is incomplete, route to the engineering owner of `[SF][Nichibei] Implement LA soft delete with consume point`) | Actual result to be captured against live Nichibei org |

**Severity:** critical
**Priority:** high

---
