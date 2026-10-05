# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2256 — "Check clashing across locations"](https://app.qase.io/project/PX?suite=2256) (20 existing cases, under parent 2129 "CM/Teacher Verify Zoom Owner"). This suite covers the Zoom Owner occupied/vacant check used when generating a Zoom link for a lesson: a Zoom Owner (teacher) affiliated with one location is excluded from the selectable Zoom Owner list for a lesson at a different location if they are already "occupied" by another lesson that overlaps in time. Baseline case 16742 ("Delete student so that from occupied -> vacant") shows this occupied state is tied to whether the occupying lesson still has an active student session, not merely to the lesson or teacher assignment existing — directly relevant to this epic's archive mechanism.

Code trace:
- **Client-side check (the actual "Zoom Owner not in list" behavior)** — `school-portal-admin/src/squads/lesson/domains/LessonManagement/modules/lesson-sf-detail/hooks/useGetZoomOwnerSF.ts:10-23`. The query selects `MANAERP__Zoom_Owner__c` records NOT IN a subquery of `MANAERP__Zoom_Participant__c` rows that overlap the target lesson's time window at a different lesson, where that participant row counts as "occupying" only if `MANAERP__Student_Session__c = NULL` OR its linked `Student_Sessions__c` has both `Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`.
- **Server-side equivalent** — `LessonZoomRestAPI.cls:180`: `SELECT Id, Lesson__c, Lesson_Allocation__c FROM Student_Sessions__c WHERE Lesson__c IN :lessons AND Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`.
- Both queries were patched by commit `5e9fb50e` (LT-111546) to add the `Is_Archived__c` clause alongside `Is_Deleted__c` — confirming archiving a lesson's only active student correctly frees that lesson's Zoom Owner for use elsewhere, exactly like deleting the student does (case 16742's baseline behavior).
- **Gap found**: `LessonAllocationHandler.afterUpdate` (restore path, processes records where `Archived_At__c == NULL`) only runs `enqueueManualSessionCleanup`/class-member duration logic on restore — it does **not** re-run any Zoom Owner clash/occupied revalidation. So if, during the window while Lesson 1's allocation was archived (and its Zoom Owner therefore showed "vacant"), a DIFFERENT lesson at another location independently generates a zoom with that SAME Zoom Owner, restoring Lesson 1's allocation afterward does not detect, alert on, or prevent the resulting double-booking — both lessons simply keep their own already-generated Zoom Owner assignment with no cross-check ever re-running.
- **Follow-up trace — does editing a lesson's date/time afterward ever self-heal this?** Checked the "Edit lesson info with Apply this and the following" cascade (`UpdateLessonHandler.cls` → `LessonRecurrenceUpdateHandler.cls` → `LessonUpdateProcessor.cls`, and the `Lesson__c` trigger chain `LessonTrigger.trigger` → `LessonHandler.cls`). None of these reference `Zoom_Owner__c`/`Zoom_Participant__c`/clash/overlap logic at all. The only Zoom-related code reached on a date/time edit is `LessonZoomHandler.calcRenewLessonZoomLinks` (`LessonZoomHandler.cls:600-655`), called from `UpdateLessonHandler.cls:65-76` when `isDateTimeChanged` is true — but this only re-reads the **already-assigned** Zoom Owner off the existing `Zoom_Participant__c` row and re-calls the external Zoom API to regenerate the meeting link; it never re-queries `Zoom_Participant__c` for overlap or re-validates clash at all. This holds identically whether or not any party involved is archived (no `Is_Archived__c` branching exists anywhere in this cascade). **Conclusion: once the archive/restore race above creates a double-booking, no subsequent lesson date/time edit on either lesson will ever detect or correct it — the collision is permanent until someone happens to reopen the Zoom Owner dropdown for an unrelated third lesson (TC2 step 6).**

## Suite: Check clashing across locations (suite TBD)

### Zoom Owner Clash Check – Archiving the Last Active Student on an Occupying Lesson Frees the Zoom Owner for an Overlapping-Time Lesson at a Different Location

**Description:** Regression / control case — Decision Table, mirrors baseline case 16742 ("Delete student so that from occupied -> vacant") but substitutes the trigger mechanism with an archive instead of a manual student removal — confirms `useGetZoomOwnerSF.ts`'s `Is_Archived__c = FALSE` clause (added by commit `5e9fb50e`) produces the identical "occupied -> vacant" transition as deleting the student outright.

**Preconditions:**
- Teacher ZO_A's affiliation location: LOC_1.
- Lesson 1 exists at Location LOC_2, date&time 2026/03/01 13h-14h, with Student A assigned and Zoom generated using ZO_A (single Zoom type).
- Lesson 2 exists at Location LOC_1, date&time 2026/03/01 10h-13h30 (overlaps Lesson 1's time window), with no Zoom Owner generated yet.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | CM/Teacher opens Lesson 2 and attempts to select ZO_A for "Generate the single zoom" | ZO_A does not appear in the selectable Zoom Owner list — Lesson 1's active Zoom_Participant__c row (linked to Student A's non-archived session) marks ZO_A as occupied for the overlapping window | Student A Is_Archived__c = FALSE → counted as occupying |
| 2 | The Student Package Order behind Student A's Lesson Allocation on Lesson 1 is fully removed, so the Lesson Allocation is archived | Lesson 1's Student Session for Student A shows Is_Archived__c = TRUE (via formula) | Archived_At__c = current timestamp |
| 3 | CM/Teacher reopens Lesson 2 and attempts to select ZO_A for "Generate the single zoom" again | ZO_A now appears in the selectable Zoom Owner list and the zoom link generates successfully — Lesson 1's Zoom_Participant__c row no longer counts as occupying, since its linked Student Session now fails the `Is_Archived__c = FALSE` filter | useGetZoomOwnerSF's subquery excludes Lesson 1's participant row; Lesson 2 generates Zoom with ZO_A |

**Severity:** minor
**Priority:** medium

---

### Zoom Owner Clash Check – Restoring an Archived Lesson Allocation After the Freed Zoom Owner Was Reassigned Elsewhere Creates an Undetected Double-Booking

**Description:** Gap case — Decision Table, contrasts with the control case above — once a Lesson Allocation's archive frees its Zoom Owner for use on a different, overlapping-time lesson at another location, restoring that Lesson Allocation does not re-run any clash/occupied revalidation (`LessonAllocationHandler.afterUpdate`'s restore path only triggers session-cleanup/class-member-duration logic). The result is a genuine double-booking — the same Zoom Owner generated on two different lessons that overlap in time at two different locations — with no system alert, warning, or automatic correction on either lesson; the collision is silently left in place and only surfaces if staff happen to re-open the Zoom Owner list for one of the two lessons afterward.

**Preconditions:**
- Teacher ZO_A's affiliation location: LOC_1.
- Lesson 1 exists at Location LOC_2, date&time 2026/03/01 13h-14h, with Student A assigned and Zoom already generated using ZO_A (single Zoom type).
- Lesson 2 exists at Location LOC_1, date&time 2026/03/01 13h01-13h59 (overlaps Lesson 1's time window), with no Zoom Owner generated yet.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | The Student Package Order behind Student A's Lesson Allocation on Lesson 1 is fully removed, so the Lesson Allocation is archived | Lesson 1's Student Session for Student A shows Is_Archived__c = TRUE; Lesson 1's own Zoom_Participant__c record for ZO_A is untouched and remains active (archiving a student does not un-generate an already-generated zoom) | Archived_At__c = current timestamp |
| 2 | CM/Teacher opens Lesson 2 and selects ZO_A for "Generate the single zoom" | ZO_A appears in the selectable list (Lesson 1 no longer counts as occupying) and the zoom link generates successfully for Lesson 2 with ZO_A | Lesson 2's Zoom_Participant__c row created for ZO_A |
| 3 | A living Student Package Order reappears for Student A's Student Course, so Lesson 1's Lesson Allocation is restored (Archived_At__c cleared) on the same record Id | The Lesson Allocation shows Archived_At__c blank again; Lesson 1's Student Session Is_Archived__c = FALSE | Archived_At__c = null (restored) |
| 4 | CM/Teacher reopens Lesson 1's detail screen | Lesson 1 still shows ZO_A as its generated Zoom Owner, exactly as before archiving — no warning, error, or indication that ZO_A is now also assigned to Lesson 2 at an overlapping time in a different location | Lesson 1's Zoom_Participant__c for ZO_A was never removed/invalidated during the archive window |
| 5 | CM/Teacher reopens Lesson 2's detail screen | Lesson 2 also still shows ZO_A as its generated Zoom Owner, with no warning, error, or indication of the conflict with Lesson 1 | Lesson 2's Zoom_Participant__c for ZO_A likewise untouched; no revalidation triggered by Lesson 1's restore |
| 6 | CM/Teacher opens the Zoom Owner selection list for a third, new overlapping-time lesson at any location and checks whether ZO_A is excluded | ZO_A is correctly excluded here (the live query correctly finds at least one non-archived, non-deleted occupying session), but this gives no indication to staff that Lesson 1 and Lesson 2 are ALREADY double-booked against each other — the system has no mechanism that proactively flags the pre-existing collision between them | Both Lesson 1 and Lesson 2's participant rows independently satisfy the occupied subquery now, but neither lesson's own screen ever cross-checks against the other |

**Severity:** major
**Priority:** high

---

### Zoom Owner Double-Booking From the Archive/Restore Race Persists Indefinitely — Subsequent Lesson Date/Time Edits Never Trigger Clash Revalidation

**Description:** Gap case — Decision Table, extends the double-booking gap above — confirms via code trace that NO code path anywhere (not `UpdateLessonHandler`, `LessonRecurrenceUpdateHandler`, `LessonUpdateProcessor`, `LessonHandler`'s trigger chain, nor `LessonZoomHandler.calcRenewLessonZoomLinks`, which only re-generates the Zoom meeting link for the already-assigned owner via an external API callout) ever re-validates Zoom Owner clash when a lesson's date or time is edited. This means once the archive/restore race (previous case) creates a double-booking between Lesson 1 and Lesson 2, any number of subsequent, routine date/time edits on either lesson — made for completely unrelated reasons — will never surface or correct the conflict. The collision is not a transient side-effect that resolves itself over time; it is permanent until someone happens to reopen the Zoom Owner dropdown for a third, unrelated lesson that also wants ZO_A at an overlapping time.

**Preconditions:**
- Continuing directly from the end state of the previous case: Lesson 1 (LOC_2, recurring weekly chain) and Lesson 2 (LOC_1) both currently show ZO_A as their generated Zoom Owner at overlapping times, as a result of the archive/restore race.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | CM edits Lesson 1's time only (e.g., 13h-14h → 14h-15h) via "Edit lesson time" with "only this lesson", for a reason unrelated to the double-booking (e.g., a scheduling preference change) | The time updates successfully; `LessonZoomHandler.calcRenewLessonZoomLinks` re-generates the Zoom meeting link for the same already-assigned owner ZO_A via the external Zoom API — no clash/overlap check is performed, no warning about Lesson 2 is shown | isDateTimeChanged = TRUE triggers calcRenewLessonZoomLinks, which reads the existing Zoom_Participant__c row and does not query for overlap |
| 2 | CM edits Lesson 2's date with "Apply this and the following" (shifts the remaining weekly chain forward by one week), also for an unrelated reason | The dates update successfully for the whole remaining chain; Zoom links are regenerated per shifted lesson for the same existing owner ZO_A; still no clash check against Lesson 1 or any other lesson in the system | LessonUpdateProcessor's date recalculation never references Zoom_Participant__c or Lesson_Allocation__c |
| 3 | CM/Teacher reopens both Lesson 1's and Lesson 2's detail screens after both edits | Both lessons continue to independently show ZO_A as a valid, working Zoom Owner — with no indication anywhere that the two have ever conflicted, or that they might still conflict at their current (possibly changed) times | Neither lesson's detail screen cross-checks its Zoom Owner against any other lesson's assignment |

**Severity:** major
**Priority:** medium

---
