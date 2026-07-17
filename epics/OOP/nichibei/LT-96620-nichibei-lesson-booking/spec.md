# LT-96620: [Nichibei] Core | App — Lesson Booking System (No.21)

**ID:** https://manabie.atlassian.net/browse/LT-96620
**Status:** In Development
**Client:** Nichibei
**Analysis Date:** 2026-05-05
**PRD:** https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2354577427/LessonBookingSystem
**Figma:** https://www.figma.com/design/ScYPiu6XQyIW207FySNm1a/-Ideation--Learner-App--Learnosity---LMS-2.0-?node-id=11770-15852
**QA Ticket:** LT-100859

> **Amendment — LT-104607** (https://manabie.atlassian.net/browse/LT-104607, analyzed 2026-07-01): Nichibei | Implement cancellation logging for Lesson Booking system. On student self-cancellation, creates a Salesforce Chatter post for the lesson's CM. See **US 07** and rows 33–39, 42–43 in Business Rules. Implementation ticket: PBT-3445.
>
> **Amendment — LT-104541** (https://manabie.atlassian.net/browse/LT-104541, analyzed 2026-07-01): Nichibei | Change requirement — revert lesson to Draft after the last booking is cancelled. **Confirmed in-scope alongside LT-104607** (same client Fb-list batch, both targeted for July release). This **supersedes** BR-32 / the Assumption / Clarification Q6 below, which had confirmed the opposite ("stays Published, never reverts"). See new **AC 04.5**.
>
> **Amendment — PM update (2026-07-01):** Confirmed — the Salesforce notification to the lesson's assigned teacher is **removed entirely**, for **both** the booking (AC 03.4) and cancellation (AC 04.4) flows. This resolves the discrepancy previously tracked in Conflict & Gap Analysis (was flagged as out-of-scope for LT-104607; PM has now confirmed it as a separate, real change). US 05 is fully deprecated. See **AC 03.4 / AC 04.4** updates and rows 21, 24 (superseded) + 44–45 (new) in Business Rules.

---

## Summary

This feature enables students to independently search for, browse, and book available lessons directly from the Manabie Learner App (Mobile), and to cancel their self-made bookings within the allowed timeframe. It leverages the existing Salesforce lesson enrollment data model (Student Session, Lesson Allocation) and adds a new self-service booking UI without replacing any staff back-office workflows. A new `Bookable Flag` on the Lesson object controls whether a lesson appears in the student's booking view. The feature is a CORE feature but requires explicit enablement per partner (default disabled).

**Key scope additions for this analysis (as requested):**

- This epic has **added Mobile scope** — the primary delivery platform is the Learner App
- Special focus: **switch account and switch student** logic — the PRD only defines 'Student' as the actor, but the Learner App supports parent logins with multiple linked students. The Event Booking System has established switch-student behavior that is **not yet mirrored** in this PRD.
- Cross-reference: **LT-96662** (Publish and Notify Student) — notification deep-link behavior intersects with lesson booking navigation

---

## Acceptance Criteria

### US 01 — View My Lessons (Top Screen)

#### AC 01.1 — Booking List as Top Screen

**Given** a student selects the "Lesson Booking" menu  
**When** the screen loads  
**Then** display the **Booking List Screen** as the top screen:

- Booked lessons list: **Booking Flag = TRUE**, `lesson_date >= today`
- "Reserve New Lesson" button (at the bottom of the page): visible ONLY when student has active LAs; navigates to the Filter page first, then to Lesson Search
- Lesson cards: name, date, center, teacher + Cancel button logic (see below)

**Sorting:** Lesson start time ASC → Group lessons before individual → Lesson ID ASC (tiebreaker)

**Cancel button on Booking List card:**
| State | Condition |
|-------|-----------|
| Cancel (enabled) | Booking Flag ON + within cancellation deadline |
| Cancel (disabled) | Booking Flag ON + past cancellation deadline → tooltip shown |

**Empty states:**
| Condition | Message |
|-----------|---------|
| No upcoming bookings | "You have no upcoming bookings" |
| No active LA | "No courses available for booking" + Browse button inactive |

---

### US 02 — Lesson Search & Browse

#### AC 02.1 — Prerequisites

- No active LA → "No lessons available for booking" empty state; no lesson list shown
- Active LA(s) → proceed to lesson list

#### AC 02.2 — Lesson Display Conditions (ALL must be met)

| Condition     | Rule                                            |
| ------------- | ----------------------------------------------- |
| Location      | Lesson location linked to student's active LA's Location Course |
| Bookable Flag | = TRUE                                          |
| Status        | Draft OR Published                              |
| Date          | Lesson date >= today + X days AND <= today + 14 days |

#### AC 02.3 — Filters

| Filter        | Type                     | Default           | Notes                                                         |
| ------------- | ------------------------ | ----------------- | ------------------------------------------------------------- |
| Schedule      | Date range + day-of-week | Today to +1 month |                                                               |
| Location      | Single-select            | All LA's Location Course  | Only LA's Location Course linked locations shown              |
| Bookable Only | Toggle                   | OFF               | When ON: remaining capacity > 0 AND not yet booked by student |
| Subject       | Single-select (Required) | None              | Filtered by teacher's eligible subject. This field is required to filter. |
| Teacher       | Combobox (multi-select)  | None              | Filtered by selected subject AND selected location            |
| Lesson Name   | Text field               | None              | Partial match                                                 |

#### AC 02.4 — Lesson Card Display

**Sorting:** Start time ASC → Group > Individual → Lesson ID ASC

**Action button states (exactly ONE visible):**
| State | Condition |
|-------|-----------|
| Reserve (enabled) | Student NOT allocated + bookable + not full + within deadline |
| Reserve (disabled) + tooltip | Lesson full OR past deadline |
| No button | Booking Flag OFF/blank (staff-allocated) |
| Cancel (enabled) | Booking Flag ON + within cancellation deadline |
| Cancel (disabled) + tooltip | Booking Flag ON + past cancellation deadline |

---

### US 03 — Book a Lesson

#### AC 03.1 — Booking Confirmation Screen

Fields shown: Lesson name, Date+time, Location+classroom, Teacher name  
Remarks field: optional free-text, label "Add a note (Optional)"  
Buttons: "Back (×)" (top) + "Confirm Reservation" (primary, prominent)

#### AC 03.2 — Booking Processing (Atomic)

Steps execute **atomically**:

1. Re-validate: LA active + lesson not full + within deadline + no duplicate
2. Create Student Session with `Booking_Flag = TRUE`
3. If remarks entered: save to `Attendance_Response_Remark` prefixed with "Booking Note: "
4. If lesson status = Draft: **auto-set to Published**

**LA Selection Rule (multiple active LAs):**

1. Active LA (lesson date within LA duration)
2. LA location = Lesson location
3. LA start date earlier
4. LA created earlier

#### AC 03.3 — Validation Error Messages

| Constraint          | Condition                        | Error Message                                            |
| ------------------- | -------------------------------- | -------------------------------------------------------- |
| Duplicate           | Already allocated in this lesson | "You have already reserved this lesson."                 |
| Capacity            | Session count >= capacity        | "This lesson is now full. Please choose another lesson." |
| Booking Deadline    | Now > 5:00 PM JPT the day before lesson date     | "The booking deadline has passed for this lesson."       |
| No LA               | No active Lesson Allocation                      | "You are not eligible to reserve lessons at this time."  |
| Insufficient Points | Remaining points < lesson cost   | "Remaining points are insufficient to book this lesson." |
| Connection          | Network timeout                  | "Connection error. Please try again."                    |
| Other               | Generic error                    | "Something went wrong. Please try again later."          |

#### AC 03.4 — Post-Booking Actions

1. Navigate to Booking Success Screen (confirmation + lesson details + buttons)
2. Lesson appears in student's Booking List
3. ~~**Salesforce notification to assigned teacher** (async, within 30 seconds): Message: "[Student Name] has reserved [Lesson Name]". Trigger: app booking ONLY (not staff SF allocations)~~  
   **[REMOVED — PM update 2026-07-01]** No notification of any kind is sent to the lesson's assigned teacher on booking. Confirmed for both app booking and staff SF allocation paths (both already sent nothing to the teacher on the allocation path; app booking's notification is now removed too).

---

### US 04 — Cancel a Booking

#### AC 04.1 — Cancellation Entry Points

1. Booking List Screen — Cancel button on each booking card
2. Lesson List Screen — Cancel button on lessons with Booking Flag ON

Cancel button only appears for **Booking Flag = TRUE** lessons.  
Staff-allocated lessons (Booking Flag OFF) show no cancel button.

#### AC 04.2 — Cancellation Constraints

| Condition                                      | Button State                                                                  |
| ---------------------------------------------- | ----------------------------------------------------------------------------- |
| Within deadline (now <= 5:00 PM JPT of the day before lesson date) | Enabled                                                                       |
| Past deadline                                  | Disabled + tooltip: "Cancellation not available after 5:00 PM the day before" |

**At submission time:** re-validate deadline + booking method.

#### AC 04.3 — Cancellation Confirmation Dialog

- Title: "Cancel Booking?"
- Message: "Are you sure you want to cancel this reservation?"
- Buttons: "×" (secondary) + "Cancel Reservation" (destructive, red)

#### AC 04.4 — Cancellation Processing (Atomic)

1. Delete Student Session record
2. Lesson removed from student's Booking List
3. ~~**Salesforce notification to assigned teacher** (async, within 30 seconds): Message: "[Student Name] has cancelled [Lesson Name]"~~  
   **[REMOVED — PM update 2026-07-01]** No notification of any kind is sent to the lesson's assigned teacher on cancellation.
4. **[ADDED by LT-104607]** Salesforce Chatter post created for the lesson's CM — see **US 07**
5. **[ADDED by LT-104541]** Lesson status reversion check — see **AC 04.5**
6. Return to updated Booking List

#### AC 04.5 — Lesson Status Reversion (LT-104541)

**Supersedes BR-32 / Clarification Q6** (previously: lesson stays Published forever, no revert).

- **Trigger:** student self-cancels via app (same trigger as AC 04.4) AND this was the lesson's last remaining Student Session (0 students left after this cancellation) AND the lesson is currently **Published**.
- **Then:** revert lesson status to **Draft** — applies regardless of how the lesson originally became Published (auto-published via booking per AC 03.2, or manually published by staff before any booking existed).
- **If** other Student Sessions still exist on the lesson after this cancellation → lesson **remains Published** (no status change).
- **Staff manually removing a Student Session via Salesforce does NOT trigger this reversion** — even if it results in 0 students on a Published lesson, the lesson stays Published. Only the app self-cancel path (AC 04.4) triggers the Draft revert.
- Confirmed by Maria Nawatani (PBT-3445, 2026-06-23): *"Lesson is auto-published when there is at least 1 student books the lesson (lesson is Draft before). When last student cancels (no students in the lesson), revert the lesson to Draft. If there is still student, remain as Published."*

---

### US 05 — Receive Booking Notifications (Teacher) — ~~REMOVED~~ [DEPRECATED — PM update 2026-07-01]

**This entire user story is removed.** The lesson's assigned teacher no longer receives any Salesforce notification for booking or cancellation. Kept below (struck through) for historical traceability only — do not implement or test against it.

#### ~~AC 05.1 — Notification: New Booking~~

- ~~Trigger: app booking only~~
- ~~Message: "[Student Name] has reserved [Lesson Name]"~~
- ~~Delivery: within 30 seconds~~

#### ~~AC 05.2 — Notification: Cancellation~~

- ~~Trigger: app cancellation only~~
- ~~Message: "[Student Name] has cancelled [Lesson Name]"~~
- ~~Delivery: within 30 seconds~~

---

### US 06 — Manage Lesson Availability (Staff — Salesforce)

#### AC 06.1 — Bookable Flag Configuration

- Checkbox on Lesson create/edit screen; default OFF
- Users with Lesson edit permissions can change
- Turning OFF: existing Student Sessions **unaffected** (no cascading deletion)
- Change history tracked via Salesforce field history
- New fields also added: Lesson Schedule.Bookable_Flag (CSV bulk import only, low priority MVP)

---

### US 07 — Cancellation Logging: Notify CM via Chatter (LT-104607)

> Additive to US 04 / AC 04.4. ~~Does not change US 05 (teacher notifications).~~ **Note (2026-07-01): US 05 has since been removed entirely per a separate PM update — see AC 03.4 / AC 04.4.** At the time LT-104607 was analyzed, teacher notifications were unchanged; that is no longer true.

#### AC 07.1 — Trigger

Fires on the same event as AC 04.4 (student self-cancels a booking via app — Student Session deleted). Staff-initiated removal of a Student Session via Salesforce does **not** trigger this flow (mirrors the staff-exclusion behavior already verified for teacher notifications by Qase case 20924).

#### AC 07.2 — Chatter Post Content

- Hardcoded to Japanese regardless of the viewing/admin user's language setting (confirmed 2026-06-30 — same pattern as the existing student-absence notification).
- Content template: `[Student Name]が[Lesson Name]をキャンセルしました。`
- `[Student Name]` hyperlinked to the Student's LA record; `[Lesson Name]` hyperlinked to the Lesson detail record.
- EN reference (translation table only, not shown in product): "[Student Name] - (hyperlink to Student's LA) has cancelled booking of [Lesson Name] - (hyperlink to lesson detail)"

#### AC 07.3 — Relate To & Topic

- Chatter post "Related To" = the target Lesson record → surfaces automatically in the Lesson Detail's Chatter/Activity tab, no extra sync step.
- Grouped under Topic (hardcoded JA): `予約授業のキャンセル` (EN reference: "Lesson Booking Cancellation").

#### AC 07.4 — Recipient & Visibility

- Recipient: the lesson location's CM **AND any CM assigned at the location's Brand level** — i.e. if Location 1 belongs to Brand A and a CM is assigned to Brand A (not to Location 1 individually), that CM must also receive the Chatter post for Location 1's lesson cancellations.
- **Zero-CM case (confirmed 2026-07-01):** if no CM is assigned to the lesson's location (checking both the direct location assignment and the brand-level resolution) → **no Chatter post is created at all.**
- **Dual-assignment case (confirmed 2026-07-01):** if a CM is assigned directly to the location AND a different CM is assigned at the Brand level → exactly **ONE** Chatter post is created, **@mentioning both CMs** (not two separate posts).
- Lesson teacher is **not** a recipient of this Chatter post. (Originally documented as "teacher notification per US 05 is unchanged and continues separately" — **no longer true**: US 05 has since been removed entirely, see AC 03.4 / AC 04.4.)
- Visibility follows standard Salesforce LBAC: a user sees the post if they can view the related Lesson record, are @mentioned, or it was manually shared with them. No additional ACL layer.
- **Test coverage requirement:** cases must verify (a) delivery to a CM assigned directly to the lesson's location, (b) delivery to a CM assigned only at the Brand level, (c) no post created when no CM resolves at either level, and (d) exactly one post with both CMs mentioned when both levels have a CM assigned.

---

## Business Rules (Extracted)

| #   | AC         | Business Rule                                                                               | Field               | Field Behavior       | Platform |
| --- | ---------- | ------------------------------------------------------------------------------------------- | ------------------- | -------------------- | -------- |
| 1   | AC 01.1    | Booking List shows ONLY Booking Flag=TRUE sessions, lesson_date >= today                    | Booking List filter | auto-filtered        | [Mobile] |
| 2   | AC 01.1    | Browse Lessons (+) button visible ONLY when student has active LA                           | Browse button       | visible/hidden       | [Mobile] |
| 3   | AC 01.1    | Cancel button ENABLED within deadline; DISABLED with tooltip past deadline                  | Cancel button       | enabled/disabled     | [Mobile] |
| 4   | AC 02.2    | Lesson visible: location linked to student's active LA's Location Course                    | Lesson visibility   | filtered             | [Mobile] |
| 5   | AC 02.2    | Lesson visible: Bookable Flag = TRUE                                                        | Lesson visibility   | filtered             | [Mobile] |
| 6   | AC 02.2    | Lesson visible: status = Draft OR Published                                                 | Lesson visibility   | filtered             | [Mobile] |
| 7   | AC 02.2    | Lesson visible: date >= today + X days                                                      | Lesson visibility   | filtered             | [Mobile] |
| 8   | AC 02.3    | Location filter shows only student's active LA's Location Course locations                  | Location dropdown   | restricted           | [Mobile] |
| 9   | AC 02.4    | Reserve button ENABLED: not allocated + bookable + not full + within deadline               | Reserve button      | enabled              | [Mobile] |
| 10  | AC 02.4    | Reserve button DISABLED: lesson full OR past deadline                                       | Reserve button      | disabled             | [Mobile] |
| 11  | AC 02.4    | No button for staff-allocated (Booking Flag OFF/blank)                                      | Action button       | hidden               | [Mobile] |
| 12  | AC 03.2    | Booking is ATOMIC: validate → create session → save remarks → auto-publish                  | Student Session     | atomic write         | [SF API] |
| 13  | AC 03.2    | Draft lesson → auto-Published when booked                                                   | Lesson status       | auto-transition      | [SF API] |
| 14  | AC 03.2    | Remarks prefixed "Booking Note: " on Attendance Response field                              | Attendance Response | auto-prefixed text   | [SF API] |
| 15  | AC 03.2    | LA selection priority: active → location match → earliest start → earliest created          | LA selection        | auto-selected        | [SF API] |
| 16  | AC 03.3    | Duplicate allocation blocked                                                                | Booking validation  | rejected             | [SF API] |
| 17  | AC 03.3    | Capacity full → blocked                                                                     | Booking validation  | rejected             | [SF API] |
| 18  | AC 03.3    | Past booking deadline → blocked                                                             | Booking validation  | rejected             | [SF API] |
| 19  | AC 03.3    | No active LA → blocked                                                                      | Booking validation  | rejected             | [SF API] |
| 20  | AC 03.3    | Insufficient points → blocked                                                               | Booking validation  | rejected             | [SF API] |
| 21  | ~~AC 03.4~~ | ~~SF notification to teacher within 30s on booking~~ — **REMOVED, see #44**                 | SF notification     | removed               | [SF]     |
| 22  | AC 04.2    | Cancel: enabled until 5PM day before; disabled + tooltip past deadline                      | Cancel button       | enabled/disabled     | [Mobile] |
| 23  | AC 04.4    | Cancel is ATOMIC: delete session → remove from list                                         | Cancellation        | atomic delete        | [SF API] |
| 24  | ~~AC 04.4~~ | ~~SF notification to teacher within 30s on cancellation~~ — **REMOVED, see #45**             | SF notification     | removed               | [SF]     |
| 25  | AC 06.1    | Bookable Flag OFF: existing sessions unaffected                                             | Bookable Flag       | non-cascading        | [SF]     |
| 26  | PRD/Tech   | Deadline evaluation uses LESSON timezone (not user device)                                  | Deadline calc       | timezone-aware       | [SF API] |
| 27  | PRD/Tech   | Capacity check uses optimistic locking at submission time                                   | Capacity check      | optimistic lock      | [SF API] |
| 28  | PRD/Config | Feature disabled by default; must be enabled per partner                                    | App menu            | hidden when disabled | [Mobile] |
| 29  | Confirmed  | **Parent users CANNOT access Lesson Booking** — Student scope only                          | App menu            | hidden for parent    | [Mobile] |
| 30  | Confirmed  | **Auto-publish on booking is SILENT** — no push notification triggered                      | Lesson publish      | silent, no notify    | [SF API] |
| 31  | Confirmed  | **Points calc = same as manual student assignment** (Nichibei existing logic)               | Points check        | existing mechanism   | [SF API] |
| 32  | ~~Confirmed~~ | ~~Auto-published lesson stays Published after all bookings cancelled — no revert to Draft~~ — **Superseded by AC 04.5 (LT-104541)** | Lesson status       | see AC 04.5           | [SF API] |
| 33  | AC 07.1    | Chatter/CM flow triggers only on student self-cancel via app, not staff SF removal          | Chatter trigger     | trigger-conditional  | [SF]     |
| 34  | AC 07.2    | Chatter post body hardcoded JA: "[Student Name]が[Lesson Name]をキャンセルしました。"              | Chatter post body   | auto-generated, JA   | [SF]     |
| 35  | AC 07.2    | [Student Name] hyperlinked to Student's LA; [Lesson Name] hyperlinked to Lesson detail       | Chatter post body   | embedded links       | [SF]     |
| 36  | AC 07.3    | Chatter post "Related To" = target Lesson → auto-shows in Lesson Detail Chatter tab          | Chatter — Related To| auto-set = Lesson    | [SF]     |
| 37  | AC 07.3    | Chatter post grouped under Topic "予約授業のキャンセル"                                          | Chatter — Topic     | fixed value          | [SF]     |
| 38  | AC 07.4    | Recipient = CM assigned to the lesson's Location OR to its parent Brand                     | Chatter — recipients| role/hierarchy-scoped| [SF]     |
| 39  | AC 07.4    | Chatter post visibility follows native SF LBAC — no additional ACL layer                    | Chatter visibility  | inherited from LBAC  | [SF]     |
| 40  | AC 04.5    | App self-cancel that empties last Student Session on a Published lesson → revert to Draft   | Lesson status       | conditional revert   | [SF API] |
| 41  | AC 04.5    | Staff manual Student Session removal via SF does NOT trigger the Draft revert               | Lesson status       | no revert (excluded) | [SF]     |
| 42  | AC 07.4    | No CM resolves for lesson's location (direct or Brand-level) → no Chatter post created       | Chatter creation    | conditional skip      | [SF]     |
| 43  | AC 07.4    | CM assigned at BOTH location and Brand level → exactly ONE post, mentioning both CMs         | Chatter creation    | single post, dual mention | [SF] |
| 44  | AC 03.4    | **(PM update 2026-07-01)** No SF notification of any kind sent to teacher on booking (app booking or staff SF allocation) | SF notification     | removed              | [SF]     |
| 45  | AC 04.4    | **(PM update 2026-07-01)** No SF notification of any kind sent to teacher on cancellation (app self-cancel or staff SF removal) | SF notification     | removed              | [SF]     |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| #   | Tag          | Source                                              | AC                       | Description                                                                                                                                                                                                                                                                                                                                                                                                                    |
| --- | ------------ | ---------------------------------------------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `[REPLACED]` | LT-104541 (https://manabie.atlassian.net/browse/LT-104541) | BR-32, Clarification Q6, Missing-in-Requirements #8, new AC 04.5 | **Resolved.** LT-104541 ("Revert lesson to Draft after last booking cancelled") is confirmed **in scope**, analyzed alongside LT-104607 in this pass. It **supersedes** BR-32 / the PdM-confirmed Assumption / Clarification Q6, which had said the opposite ("stays Published, no revert"). New behavior implemented as **AC 04.5**. |
| 2   | `[REPLACED]` | PBT-3445 comments (2026-06-29, Tuyen Hua) + PM update (2026-07-01) | AC 03.4, AC 04.4, US 05  | **Resolved.** PBT-3445's comment thread proposed removing the existing SF teacher notification entirely (both booking and cancellation). Previously (2026-07-01, earlier in this pass) confirmed as NOT in LT-104607's scope. **PM has since confirmed (same day) this removal IS happening**, as a separate change independent of the Chatter post. Teacher notification (US 05) is now fully removed — see updated AC 03.4 / AC 04.4 and BR #21, #24 (superseded), #44–45 (new). |

---

### Missing in Requirements

| #   | Tag                    | Source                                                  | AC              | Description                                                                                                                                                                                                                                                                                                                 |
| --- | ---------------------- | ------------------------------------------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `[ROLE GAP]`           | US 01–US 04 (actor = Student only)                      | All             | **Parent role undefined**: All user stories only define 'Student' as the actor. No AC covers what a Parent sees when opening Lesson Booking, whether parents can book for children, or which student's context is used. The Event Booking System (LT-73558) has explicit parent support — Lesson Booking does not.          |
| 2   | `[MISSING BEHAVIOR]`   | AC 01.1; Event Booking Cases 3928–3931                  | AC 01.1         | **Switch Student — Booking List**: No AC defines which student's Booking List is shown when a Parent with multiple students opens the Lesson Booking menu. No AC defines whether the list refreshes when parent switches students globally.                                                                                 |
| 3   | `[MISSING BEHAVIOR]`   | AC 03.2; Event Booking Case 3931                        | AC 03.2         | **Switch Student DURING Booking Confirmation**: If a parent switches student context while on the Booking Confirmation screen, the Student Session is created for which student? LA selection rule (AC 03.2) doesn't lock the student context at 'Reserve' tap time.                                                        |
| 4   | `[MISSING BEHAVIOR]`   | AC 02.2 — location filter uses student's LA             | AC 02.2         | **Switch Student DURING Lesson Browse**: When parent switches student on the Lesson Search screen, should the lesson list auto-refresh? The location filter, Bookable Only state, and action button states are all student-specific and would be incorrect if the screen doesn't refresh.                                   |
| 5   | `[MISSING BEHAVIOR]`   | LT-96662 spec Finding #10; PX-2026-04-13.json Case 3931 | AC 03.4 (cross) | **Switch Account + Notification Deep-Link**: When a push notification (from LT-96662 or future lesson notification) arrives for Student A's lesson while parent is in Student B's context — does the app auto-switch with a confirmation alert (like Event Booking Case 3931), or navigate directly? Behavior is undefined. |
| 6   | `[MISSING BEHAVIOR]`   | AC 03.2 auto-publish + LT-96662 AC 02.1                 | AC 03.2         | **Auto-Publish Collision**: When a student books a Draft lesson, AC 03.2 auto-publishes it. If LT-96662 (Publish and Notify) is enabled on the same org, this auto-publish could trigger push notifications to ALL assigned students. Should the booking-triggered auto-publish be 'silent' (no notification) or regular?   |
| 7   | `[MISSING BEHAVIOR]`   | AC 03.3 error table                                     | AC 03.3         | **Points Calculation Undefined**: AC 03.3 references 'Insufficient Points' error but no AC defines: how per-lesson point cost is determined, which LA's point balance is checked, or if it's aggregate points.                                                                                                              |
| 8   | ~~`[MISSING BEHAVIOR]`~~ | ~~AC 04.4; AC 03.2 auto-publish~~ — **Resolved by AC 04.5 (LT-104541)** | AC 04.4, AC 04.5 | Resolved. Lesson now reverts to Draft when the last Student Session is cancelled via app (see AC 04.5). Superseded the earlier "stays Published" answer. |
| 9   | `[UNDOCUMENTED IN AC]` | PRD User Flow step 1                                    | AC 01.1         | **Lesson Booking Menu Position in App Navigation**: No AC defines where the 'Lesson Booking' menu appears in the app navigation (position, icon, label).                                                                                                                                                                    |
| 10  | ~~`[MISSING BEHAVIOR]`~~ | ~~AC 07.4 — CM recipient rule~~ — **Resolved** | AC 07.4         | Resolved 2026-07-01. No CM assigned at either Location or Brand level → no Chatter post is created at all.                                                                  |
| 11  | ~~`[MISSING BEHAVIOR]`~~ | ~~AC 07.4 — CM recipient rule~~ — **Resolved** | AC 07.4         | Resolved 2026-07-01. CM assigned at both Location and Brand level → exactly ONE Chatter post is created, @mentioning both CMs (not two separate posts).                     |

---

### Lesson-Learned Risks

| #   | Incident                                                     | Date       | AC               | Risk                                                                                                                                                                                                                  | Guardrail                                                                                                                         |
| --- | ------------------------------------------------------------ | ---------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Aso — Duplicate Student Sessions from Parallel Creation      | 2026-04-13 | AC 03.2, AC 03.3 | LT-96620 introduces a third Student Session creation path (app booking). If staff assigns same student via SF Calendar/Lesson Detail simultaneously, duplicate session risk exists. Prior incident: 1,655 duplicates. | Verify duplicate validation in AC 03.2 uses read-lock that also blocks concurrent SF assignments for same (student, lesson) pair. |
| 2   | Nichibei — Student Sessions Missing LA → Points Not Deducted | 2026-03-04 | AC 03.2, AC 03.3 | Nichibei LA records can be unexpectedly deleted (SPO sync bugs). Booking flow validates LA at step 1 but if LA is deleted before step 2 (TOCTOU), session created with null LA bypasses point deduction.              | Verify LA reference is held atomically from validation to write. If LA deleted mid-flow, booking must fail cleanly.               |

---

### E2E Scenario Impact

| Scenario | Title                                                   | Impact                                                                                                                              | Action                                         |
| -------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| New      | E2E: Student Self-Books and Cancels a Lesson            | New complete user flow: Mobile app → Lesson Booking menu → Browse → Reserve → Confirm → Success → Booking List → Cancel → Confirmed | CREATE                                         |
| New      | E2E: Parent Switches Student and Books Lesson for Child | Parent in Student B → switches to Student A → books lesson → verify Student Session created for Student A                           | CREATE (pending parent behavior clarification) |

---

### Assumptions Made

- The Lesson Booking System is SEPARATE from the existing Lesson Calendar/Schedule view in the app. It is a new self-contained menu entry.
- ~~Salesforce notifications to teachers (AC 03.4, AC 04.4) use the existing SF notification infrastructure, not push notifications.~~ **Moot — PM update 2026-07-01**: teacher notifications are removed entirely for both booking and cancellation.
- The "Bookable Flag" is independent of the lesson's publication status — a Draft lesson can be Bookable.
- Points check (AC 03.3) uses Nichibei's existing point-consumption mechanism on Student Session.
- ~~Auto-publish (AC 03.2) is irreversible from the student's booking flow — cancellation does NOT revert lesson to Draft.~~ **Superseded by LT-104541 / AC 04.5**: a Published lesson DOES revert to Draft once its last Student Session is removed via app self-cancel (not via staff manual removal).
- LT-96662 and LT-96620 are different partner features (Renseikai vs Nichibei) that do not currently coexist. Cross-feature questions are for future planning.

---

## Clarification Questions

> ✅ All questions answered by PdM on 2026-05-05. Not posted to Jira.

1. **[ROLE GAP]** Can a Parent user book lessons on behalf of their linked students?  
   ✅ **Answer:** No. This feature scope is Student only. Parents have no access to Lesson Booking.

2. **[MISSING BEHAVIOR]** Auto-publish from booking: silent or regular publish?  
   ✅ **Answer:** Silent publish — no notification triggered when a Draft lesson is auto-published via student booking.

3. **[LESSON-LEARNED RISK]** Duplicate session concurrency (concurrent SF staff assignment).  
   ✅ **Answer:** N/A — removed per PdM (not in scope for this question).

4. **[LESSON-LEARNED RISK]** Nichibei LA integrity under booking (TOCTOU gap).  
   ✅ **Answer:** N/A — removed per PdM (not in scope for this question).

5. **[MISSING BEHAVIOR]** Points calculation method for 'Insufficient Points' in AC 03.3.  
   ✅ **Answer:** Same logic as the existing student assignment flow in Nichibei (same point-deduction mechanism).

6. **[MISSING BEHAVIOR]** Auto-published lesson after last booking cancelled: stays Published or reverts to Draft?  
   ~~✅ **Answer (2026-05-05):** Stays Published. Lesson status does not revert to Draft after all bookings are cancelled.~~  
   🔁 **Superseded 2026-07-01 by LT-104541:** Lesson now reverts to Draft when the last Student Session is removed via app self-cancel (staff manual removal does NOT trigger the revert). See AC 04.5.

### LT-104607 — Answered 2026-07-01

7. **[MISSING BEHAVIOR]** When neither the lesson's Location nor its parent Brand has a CM assigned, is the Chatter post still created (AC 07.4)?  
   ✅ **Answer:** No. If no CM resolves for the lesson's location (direct or Brand-level), the Chatter post is not created.

8. **[MISSING BEHAVIOR]** When a CM is assigned directly to the Location AND a different CM is assigned at the Brand level, is one Chatter post shared to both, or are two separate posts/notifications sent?  
   ✅ **Answer:** Exactly one Chatter post is created, @mentioning both CMs.

---

## Related Specs

- `input/specs/LT-73558 Target Segment in Event Management` — Event Booking System with established parent/switch student patterns (Cases 3928–3932, 3931 for switch-student notification flow)
- `input/specs/LT-96662 Renseikai Receive notifications when a new lesson is published/spec.md` — Push notification deep-link to Lesson Detail; Finding #10 documents same switch-student notification gap

## Related Test Cases

- `output/test-cases/PX-2026-04-13.json` — Case 3931 (switch student on notification), Cases 3928–3930 (parent access patterns in Event Booking) — patterns to replicate for Lesson Booking if parent role is confirmed

## QASE Coverage Gaps

- AC 01.1 — No existing test cases for Booking List screen (student with bookings / no bookings / no active LA)
- AC 01.1 — No existing test cases for Browse Lessons button visibility rules (with/without active LA)
- AC 01.1 — No existing test cases for Cancel button state (within/past deadline)
- AC 02.2 — No existing test cases for lesson visibility conditions (all 4 conditions)
- AC 02.3 — No existing test cases for filter functionality (each filter option)
- AC 02.4 — No existing test cases for lesson card action button states (all 5 states)
- AC 03.2 — No existing test cases for booking atomic flow (success path + each validation failure)
- AC 03.2 — No existing test cases for Draft → Published auto-publish on booking
- AC 03.2 — No existing test cases for LA selection priority rule (multiple active LAs)
- AC 03.3 — No existing test cases for all 5 validation errors (duplicate, capacity, deadline, no LA, insufficient points)
- AC 04.2 — No existing test cases for cancellation deadline boundary (within / past)
- AC 04.4 — No existing test cases for cancel atomic flow
- AC 04.5 — No existing test cases for Draft-revert on last-cancel, remain-Published when others booked, and staff-removal exclusion (LT-104541 — new)
- ~~AC 05.1/05.2 — No existing test cases for teacher SF notification on booking/cancellation~~ **US 05 REMOVED (PM update 2026-07-01)** — all 7 cases in Qase suite 2764 "Teacher Notifications" (20922–20928) deprecated; no replacement coverage kept, per team decision (feature fully removed)
- AC 06.1 — No existing test cases for Bookable Flag effects (on/off/existing sessions)
- AC 07.1–07.4 — No existing test cases for the CM Chatter post (trigger scoping, content/language, related-to/topic, recipient resolution incl. zero-CM and dual-CM cases) (LT-104607 — new)
- **Switch Student/Account** — No existing test cases defined (pending clarification Q-01 through Q-05)
