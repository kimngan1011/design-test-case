# Test Cases: LT-105350 — [EN] Finding and Emailing Substitute Teacher Candidates

## Suite: Teacher Filter

**Available Teacher logic:** When the Available Teacher checkbox / "Only teachers free at this time" toggle is ON, a teacher appears only if both checks pass:
- Working-hours coverage: `staff_start_time <= lesson_start_time < lesson_end_time <= staff_end_time` on the lesson's JST/displayed date, and the working-hours record is not Off Day.
- Existing lesson no-overlap: no existing Draft/Published lesson for that teacher overlaps the target lesson, across any location. Overlap is `existing_lesson_start < target_lesson_end AND target_lesson_start < existing_lesson_end`. Cancelled and Completed lessons are ignored by the conflict check.

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox OFF – Teacher with overlapping lesson visible in results

**Description:** AC 02.1 — Decision Table — When the Available Teacher checkbox is OFF (unchecked), the combined availability filter does not apply; teachers who have conflicting lessons at the target lesson time can still appear in the list if they pass the other filters.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher A exists, affiliated with the target lesson's brand-level location; Teacher A has an existing lesson from 10:30–11:30 JST on the same date as the target lesson
- Target lesson time: 10:00–11:00 JST on 2026-08-01

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-08-01; lesson_start = 10:00 JST; lesson_end = 11:00 JST |
| 2 | Confirm the Available Teacher checkbox is **unchecked** (OFF) | Available Teacher checkbox shows unchecked state | "" |
| 3 | Observe the teacher list | Teacher A appears in the list despite having a lesson overlap at 10:30–11:30 JST, because the availability checkbox is OFF | Teacher A has existing lesson 10:30–11:30 JST on 2026-08-01 |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON, Teacher within working hours and no conflict – Teacher appears in candidate list

**Description:** AC 02.1, BR-03, BR-04 — Decision Table — When the Available Teacher checkbox is ON, a teacher who is fully covered by their registered working hours AND has no overlapping lessons appears in the candidate list.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher A exists, affiliated with target brand; working hours registered as 09:00–18:00 JST daily; no existing lessons on 2026-08-01
- Target lesson: 10:00–11:00 JST on 2026-08-01

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-08-01; lesson_start = 10:00 JST; lesson_end = 11:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher A working hours = 09:00–18:00 JST; no lessons on 2026-08-01 |
| 3 | Observe the teacher list | Teacher A appears in the results because both checks pass: working hours fully cover 10:00–11:00 JST and no existing lesson overlaps | "" |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON, Teacher outside working hours – Teacher excluded from results

**Description:** AC 02.1, BR-03 — Decision Table — When the Available Teacher checkbox is ON, a teacher whose registered working hours do not cover the lesson time is excluded from the candidate list, even if the teacher has no lesson conflict.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher B exists, affiliated with target brand; working hours registered as 13:00–18:00 JST daily (does not cover 10:00–11:00 JST); no existing lessons on 2026-08-01
- Target lesson: 10:00–11:00 JST on 2026-08-01

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-08-01; lesson_start = 10:00 JST; lesson_end = 11:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher B working hours = 13:00–18:00 JST; no lessons on 2026-08-01 |
| 3 | Observe the teacher list | Teacher B does **not** appear in the results | "" |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON, Working hours partially overlap target lesson – Teacher excluded from results

**Description:** AC 02.1, BR-03 — Boundary Value Analysis — A partial overlap with working hours is not enough. The teacher must have working hours that fully cover the target lesson (`staff_start_time <= lesson_start_time < lesson_end_time <= staff_end_time`).

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher B2 exists, affiliated with target brand; working hours registered as 10:30–18:00 JST on 2026-08-01; no existing lessons on 2026-08-01
- Target lesson: 10:00–11:00 JST on 2026-08-01

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-08-01; lesson_start = 10:00 JST; lesson_end = 11:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher B2 working hours = 10:30–18:00 JST; no lessons on 2026-08-01 |
| 3 | Observe the teacher list | Teacher B2 does **not** appear because the working-hours record starts after the lesson start time | Required coverage formula fails: 10:30 <= 10:00 is false |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON, Teacher has Off Day or no working-hours record – Teacher excluded from results

**Description:** AC 02.1, BR-03 — Decision Table — When the Available Teacher checkbox is ON, a teacher is excluded if the lesson date is marked as Off Day or no matching working-hours record exists for that weekday/time, even if the teacher has no lesson conflict.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher B3 exists, affiliated with target brand; Saturday working hours are absent or marked Off Day; no existing lessons on 2026-08-01
- Target lesson: Saturday 2026-08-01 10:00–11:00 JST

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = Saturday 2026-08-01; lesson_start = 10:00 JST; lesson_end = 11:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher B3: Saturday = Off Day or no working-hours record; no lessons on 2026-08-01 |
| 3 | Observe the teacher list | Teacher B3 does **not** appear because working-hours availability is not registered for the target lesson time | "" |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON, Teacher has overlapping lesson – Teacher excluded from results

**Description:** AC 02.1, BR-04 — Decision Table — When the Available Teacher checkbox is ON, a teacher who has an existing lesson that overlaps with the target lesson time is excluded from results even when working-hours coverage passes.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher C exists, affiliated with target brand; working hours 09:00–18:00 JST; has an existing lesson 10:30–11:30 JST on 2026-08-01 (overlaps with target)
- Target lesson: 10:00–11:00 JST on 2026-08-01

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-08-01; lesson_start = 10:00 JST; lesson_end = 11:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher C working hours = 09:00–18:00 JST; existing lesson = 10:30–11:30 JST on 2026-08-01 |
| 3 | Observe the teacher list | Teacher C does **not** appear in the results due to lesson overlap, even though working hours cover the target lesson | Overlap formula is true: 10:30 < 11:00 AND 10:00 < 11:30 |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON, Teacher has overlapping lesson in another location – Teacher excluded from results

**Description:** AC 02.1, BR-04 — Decision Table — Existing lesson conflicts are checked across any location. A teacher who has an overlapping lesson in a different location is excluded when the Available Teacher checkbox is ON.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher C2 exists, affiliated with target brand; working hours 09:00–18:00 JST; has an existing lesson 10:15–10:45 JST on 2026-08-01 at Location B
- Target lesson: 10:00–11:00 JST on 2026-08-01 at Location A

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | target_location = Location A; lesson_date = 2026-08-01; lesson_start = 10:00 JST; lesson_end = 11:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher C2 working hours = 09:00–18:00 JST; existing lesson = 10:15–10:45 JST at Location B |
| 3 | Observe the teacher list | Teacher C2 does **not** appear because existing lesson overlap is evaluated across locations | Overlap formula is true: 10:15 < 11:00 AND 10:00 < 10:45 |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON, Teacher has overlapping Draft or Published lesson – Teacher excluded from results

**Description:** AC 02.1, BR-04 — Decision Table — Draft and Published existing lessons are included in the no-overlap conflict set. When either status overlaps the target lesson, the teacher is excluded while the Available Teacher checkbox is ON.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher C3 exists, affiliated with target brand; working hours 09:00–18:00 JST; has an existing Draft lesson 15:30–16:30 JST on 2026-07-17
- Teacher C4 exists, affiliated with target brand; working hours 09:00–18:00 JST; has an existing Published lesson 15:30–16:30 JST on 2026-07-17
- Target lesson: 15:00–16:00 JST on 2026-07-17

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-07-17; lesson_start = 15:00 JST; lesson_end = 16:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher C3 existing lesson status = Draft; Teacher C4 existing lesson status = Published |
| 3 | Observe the teacher list | Teacher C3 and Teacher C4 do **not** appear because Draft/Published overlapping lessons are treated as conflicts | Overlap formula is true: 15:30 < 16:00 AND 15:00 < 16:30 |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON, Teacher has overlapping Cancelled or Completed lesson – Teacher not excluded

**Description:** AC 02.1, BR-04 — Decision Table — Cancelled and Completed existing lessons are excluded from the no-overlap conflict set. A teacher whose only overlapping lessons are Cancelled or Completed remains eligible if all other filters pass.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher C5 exists, affiliated with target brand; working hours 09:00–18:00 JST; has an existing Cancelled lesson 15:30–16:30 JST on 2026-07-17
- Teacher C6 exists, affiliated with target brand; working hours 09:00–18:00 JST; has an existing Completed lesson 15:30–16:30 JST on 2026-07-17
- Target lesson: 15:00–16:00 JST on 2026-07-17

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-07-17; lesson_start = 15:00 JST; lesson_end = 16:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher C5 existing lesson status = Cancelled; Teacher C6 existing lesson status = Completed |
| 3 | Observe the teacher list | Teacher C5 and Teacher C6 **appear** because Cancelled/Completed overlapping lessons are ignored by the conflict check | Both teachers pass working-hours coverage and have no Draft/Published overlap |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON, Teacher has adjacent lesson (end equals target start) – Teacher not excluded

**Description:** AC 02.1, BR-04 — Boundary Value Analysis — A teacher whose existing lesson ends exactly when the target lesson starts (adjacent, no time overlap) is NOT excluded when the Available Teacher checkbox is ON.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher D exists, affiliated with target brand; working hours 08:00–18:00 JST; has an existing lesson 09:00–10:00 JST on 2026-08-01 (ends exactly at target start time)
- Target lesson: 10:00–11:00 JST on 2026-08-01

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-08-01; lesson_start = 10:00 JST; lesson_end = 11:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher D existing lesson = 09:00–10:00 JST on 2026-08-01; end (10:00) = target start (10:00) |
| 3 | Observe the teacher list | Teacher D **appears** in the results; adjacent lesson is not treated as an overlap and working hours cover the target lesson | Existing lesson end equals target start: 10:00 = 10:00 |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Lesson at midnight JST boundary – Availability evaluated using JST date, not UTC

**Description:** AC 02.1, BR-03, BR-04 — Boundary Value Analysis (Timezone) — When the target lesson falls on a date that differs between JST and UTC (midnight boundary), the Available Teacher filter evaluates the teacher's working hours against the JST date, not the UTC date.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher A: working hours registered as 00:00–02:00 JST on Fridays (2026-07-03 is a Friday); no conflicting lessons
- Teacher B: working hours registered as 09:00–18:00 JST daily; no conflicting lessons
- Target lesson: 2026-07-03 00:30 JST (= 2026-07-02 15:30 UTC) — Friday in JST, Thursday in UTC

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the midnight-boundary lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date (JST) = 2026-07-03; lesson_start = 00:30 JST (= 2026-07-02 15:30 UTC) |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher A: working hours 00:00–02:00 JST on Fridays; Teacher B: 09:00–18:00 JST daily |
| 3 | Observe Teacher A in the teacher list | Teacher A **appears** in results (available at 00:30 JST on Friday July 3) | Lesson date used for comparison = 2026-07-03 JST (not 2026-07-02 UTC) |
| 4 | Observe Teacher B in the teacher list | Teacher B does **not** appear (00:30 JST is outside their 09:00–18:00 working hours) | "" |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON and working hours exactly match target lesson – Teacher appears in candidate list

**Description:** AC 02.1, BR-03 — Boundary Value Analysis — A teacher whose working-hours start equals lesson start and working-hours end equals lesson end is included because both boundaries are inclusive.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher A2 exists, affiliated with target brand; working hours registered as 10:00–11:00 JST on 2026-08-01; no existing lessons on 2026-08-01
- Target lesson: 10:00–11:00 JST on 2026-08-01

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-08-01; lesson_start = 10:00 JST; lesson_end = 11:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher A2 working hours = 10:00–11:00 JST; no lessons on 2026-08-01 |
| 3 | Observe the teacher list | Teacher A2 **appears** because `staff_start_time <= lesson_start_time` and `lesson_end_time <= staff_end_time` are both true at equality | Boundary equality: staff_start = lesson_start and staff_end = lesson_end |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON and working hours end before target lesson end – Teacher excluded from results

**Description:** AC 02.1, BR-03 — Boundary Value Analysis — A teacher is excluded when their working-hours record starts before the lesson but ends before the target lesson end time.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher B4 exists, affiliated with target brand; working hours registered as 09:00–10:30 JST on 2026-08-01; no existing lessons on 2026-08-01
- Target lesson: 10:00–11:00 JST on 2026-08-01

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-08-01; lesson_start = 10:00 JST; lesson_end = 11:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher B4 working hours = 09:00–10:30 JST; no lessons on 2026-08-01 |
| 3 | Observe the teacher list | Teacher B4 does **not** appear because the working-hours record ends before the lesson end time | Required coverage formula fails: 11:00 <= 10:30 is false |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON and teacher has lesson at exact same time – Teacher excluded from results

**Description:** AC 02.1, BR-04 — Boundary Value Analysis — A teacher with an existing Draft/Published lesson whose start and end time exactly match the target lesson is excluded.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher C7 exists, affiliated with target brand; working hours 09:00–18:00 JST; has an existing Published lesson 09:00–10:00 JST on 2026-04-27
- Target lesson: 09:00–10:00 JST on 2026-04-27

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-04-27; lesson_start = 09:00 JST; lesson_end = 10:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher C7 existing lesson = 09:00–10:00 JST; status = Published |
| 3 | Observe the teacher list | Teacher C7 does **not** appear because exact same-time existing lessons are conflicts | Overlap formula is true: 09:00 < 10:00 AND 09:00 < 10:00 |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON and existing lesson fully contains target lesson – Teacher excluded from results

**Description:** AC 02.1, BR-04 — Boundary Value Analysis — A teacher is excluded when an existing Draft/Published lesson starts before the target lesson and ends after the target lesson.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher C8 exists, affiliated with target brand; working hours 08:00–18:00 JST; has an existing Draft lesson 09:00–12:00 JST on 2026-08-01
- Target lesson: 10:00–11:00 JST on 2026-08-01

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-08-01; lesson_start = 10:00 JST; lesson_end = 11:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher C8 existing lesson = 09:00–12:00 JST; status = Draft |
| 3 | Observe the teacher list | Teacher C8 does **not** appear because the existing lesson fully contains the target lesson time | Overlap formula is true: 09:00 < 11:00 AND 10:00 < 12:00 |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON and existing lesson starts when target lesson ends – Teacher not excluded

**Description:** AC 02.1, BR-04 — Boundary Value Analysis — A teacher whose existing lesson starts exactly when the target lesson ends is not excluded because the lessons are adjacent, not overlapping.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Teacher D2 exists, affiliated with target brand; working hours 08:00–18:00 JST; has an existing Published lesson 11:00–12:00 JST on 2026-08-01
- Target lesson: 10:00–11:00 JST on 2026-08-01

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson and click **Add Teacher** | Add Teacher popup opens | lesson_date = 2026-08-01; lesson_start = 10:00 JST; lesson_end = 11:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Teacher D2 existing lesson = 11:00–12:00 JST on 2026-08-01 |
| 3 | Observe the teacher list | Teacher D2 **appears** because the existing lesson starts exactly at the target lesson end time | Overlap formula is false: existing_start 11:00 < target_end 11:00 is false |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Available Teacher Filter – Checkbox ON and teacher has same-time lesson in non-affiliated location – Teacher excluded from results

**Description:** AC 02.1, BR-04 — Regression — Existing lesson conflicts are checked by teacher assignment, not only by the teacher affiliation or selected search location. A same-time lesson in another or non-affiliated location still excludes the teacher.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Staff A is affiliated with Location 1 and has working hours covering 09:00–10:00 JST on 2026-04-27
- Staff A is already assigned to Lesson 1 at Location 2 from 09:00–10:00 JST on 2026-04-27
- Staff B opens Add Teacher for Lesson 2 at Location 1 from 09:00–10:00 JST on 2026-04-27

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson 2 at Location 1 and click **Add Teacher** | Add Teacher popup opens | target_location = Location 1; lesson_date = 2026-04-27; lesson_start = 09:00 JST; lesson_end = 10:00 JST |
| 2 | Enable the **Available Teacher** checkbox | Checkbox is checked (ON) | Staff A affiliation = Location 1; existing Lesson 1 location = Location 2; existing lesson time = 09:00–10:00 JST |
| 3 | Observe the teacher list | Staff A does **not** appear because the existing same-time lesson is a conflict even though it is in another or non-affiliated location | Conflict source = teacher already assigned to another lesson at the same time |

**Severity:** critical
**Priority:** high

---
### [EN] Substitute Teacher – Location Filter – Select brand-level area – Only teachers affiliated to that brand shown

**Description:** AC 02.1, BR-05, BR-06 — Decision Table — Selecting a brand-level area in the Location Selector limits the teacher list to teachers affiliated with that brand.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Brand A exists with 5 affiliated teachers; Brand B exists with 3 different affiliated teachers
- A lesson affiliated with Brand A is open on Lesson Detail

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | In the Location Selector, select **Brand A** as the area | Location filter is set to Brand A | Brand A (5 teachers); Brand B (3 different teachers) |
| 3 | Observe the teacher list | Only the 5 teachers affiliated with Brand A are shown; Brand B's 3 teachers are absent | "" |
| 4 | Change the Location Selector to **Brand B** | Filter updates | "" |
| 5 | Observe the teacher list | Brand B's 3 teachers are shown; Brand A's teachers are absent | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Location Filter – Exclude sub-location from brand selection – Teacher count decreases for that sub-location

**Description:** AC 02.1, BR-05 — Decision Table — After selecting a brand, excluding a specific sub-location reduces the teacher count to remove teachers affiliated only at that sub-location.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Brand A has sub-locations: Center X (3 teachers), Center Y (2 teachers); total = 5 Brand A teachers
- A lesson is open on Lesson Detail

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Select **Brand A** in the Location Selector | 5 teachers from Brand A are shown | Brand A total = 5 (Center X: 3, Center Y: 2) |
| 3 | In the Location Selector, exclude **Center X** from the selection | Filter updates | "" |
| 4 | Observe the teacher list and match count | 2 teachers (Center Y only) are shown; Center X's 3 teachers are absent; match count = 2 | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Location Filter – Teacher with Area-level affiliation – Teacher appears when area is within selected brand

**Description:** AC 02.1, BR-06 — Permission Matrix — A teacher affiliated at Area level (not specific sub-location) appears in results when the selected brand contains that area.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher E has an Area-level affiliation with Kanto Area (which is under Brand A)
- Brand A is selected in the Location Selector

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Select **Brand A** in the Location Selector | Location filter set to Brand A | Teacher E affiliation = Kanto Area (under Brand A) |
| 3 | Observe the teacher list | Teacher E **appears** in the results (Area affiliation is within the selected brand) | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Location Filter – Teacher registered as community plus user – Teacher appears in filtered results

**Description:** AC 02.1, BR-07 — Decision Table — A teacher who is a community plus user type appears in the filtered candidate list when their affiliation matches the selected location.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher F is a community plus user, affiliated with Brand A
- Brand A is selected in the Location Selector

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Select **Brand A** in the Location Selector | Location filter set to Brand A | Teacher F = community plus user; affiliation = Brand A |
| 3 | Observe the teacher list | Teacher F **appears** in the results | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Location Filter – Teacher registered as contact-level user – Teacher appears in filtered results

**Description:** AC 02.1, BR-07 — Decision Table — A teacher who is a contact-level user type (not community plus) also appears in the filtered candidate list when their affiliation matches the selected location.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher G is a contact-level user (not community plus), affiliated with Brand A
- Brand A is selected in the Location Selector

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Select **Brand A** in the Location Selector | Location filter set to Brand A | Teacher G = contact-level user; affiliation = Brand A |
| 3 | Observe the teacher list | Teacher G **appears** in the results | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Flagged Teacher Filter – Popup open – Flagged checkbox unchecked by default

**Description:** AC 02.1, BR-08 — Component — When the Add Teacher popup first opens, the Flagged Teacher checkbox is unchecked (OFF) by default, meaning flagged teachers are excluded from the initial results.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- A lesson is open on Lesson Detail; Add Teacher popup not yet opened in this session

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail for the target lesson | Lesson Detail is displayed | "" |
| 2 | Click the **Add Teacher** button | Add Teacher popup opens (fresh open) | "" |
| 3 | Observe the Flagged Teacher checkbox state | The Flagged Teacher (要注意講師) checkbox is **unchecked** (OFF) | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Flagged Teacher Filter – Checkbox OFF, flagged teacher – Flagged teacher excluded from results

**Description:** AC 02.1, BR-08, BR-09 — Decision Table — When the Flagged Teacher checkbox is OFF (default), a teacher whose Contact record has "Flagged" checked does not appear in the candidate list.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher H exists, affiliated with target brand; Teacher H's Contact record has the **Flagged** field checked
- A lesson is open on Lesson Detail

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Confirm the Flagged Teacher checkbox is **unchecked** (OFF) | Flagged checkbox is unchecked | Teacher H: Flagged = true on Contact |
| 3 | Observe the teacher list | Teacher H does **not** appear in the results | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Flagged Teacher Filter – Checkbox ON, flagged teacher – Flagged teacher included in results

**Description:** AC 02.1, BR-09 — Decision Table — When the Flagged Teacher checkbox is enabled (ON), teachers whose Contact record has "Flagged" checked are included in the candidate list.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher H exists, affiliated with target brand; Teacher H's Contact record has **Flagged** checked
- A lesson is open on Lesson Detail

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Confirm Teacher H is **absent** from the list (Flagged checkbox OFF by default) | Teacher H not visible | Teacher H: Flagged = true on Contact |
| 3 | Enable the **Flagged Teacher** (要注意講師) checkbox | Checkbox is checked (ON) | "" |
| 4 | Observe the teacher list | Teacher H **appears** in the results; the Flagged column shows the flag indicator for Teacher H | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Flagged Teacher Filter – Enable then disable Flagged checkbox – Flagged teacher removed from results

**Description:** AC 02.1, BR-09 — Decision Table — After enabling the Flagged Teacher checkbox (ON) and then disabling it (OFF again), the flagged teacher is removed from results, restoring the default exclusion behavior.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher H exists, affiliated with target brand; Flagged = true on Contact
- A lesson is open on Lesson Detail

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Enable the **Flagged Teacher** checkbox | Teacher H appears in the list | Teacher H: Flagged = true |
| 3 | Disable the **Flagged Teacher** checkbox (uncheck it) | Checkbox returns to unchecked state; teacher list updates | "" |
| 4 | Observe the teacher list | Teacher H is **no longer visible** in the results | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Flagged Teacher Filter – Teacher list Flagged column – Column visible with correct flag indicator per teacher

**Description:** AC 02.1, BR-10 — Component — The teacher list in the Add Teacher popup shows a "Flagged" (要注意講師) column; the column correctly indicates flagged status for teachers when the Flagged checkbox is ON.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher H: Flagged = true on Contact; Teacher I: Flagged = false on Contact
- A lesson is open on Lesson Detail; Flagged Teacher checkbox is enabled (ON)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher**; enable the Flagged Teacher checkbox | Add Teacher popup shows both Teacher H and Teacher I | Teacher H: Flagged = true; Teacher I: Flagged = false |
| 2 | Observe the **Flagged** (要注意講師) column header in the teacher list | The column header "Flagged" (要注意講師) is visible | "" |
| 3 | Observe Teacher H's row in the Flagged column | Teacher H's Flagged column shows a flag indicator (marked as flagged) | "" |
| 4 | Observe Teacher I's row in the Flagged column | Teacher I's Flagged column shows no flag indicator (not flagged) | "" |

**Severity:** minor
**Priority:** medium

---

### [EN] Substitute Teacher – Match Count – Apply filter – Count updates in real time without page reload

**Description:** AC 02.1, BR-11 — Scenario — When a filter criterion changes, the displayed match count updates immediately to reflect the current filtered results, without requiring a page reload or manual refresh.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Brand A has 8 teachers total; 3 of them are flagged (Flagged = true on Contact); 5 are unflagged
- A lesson is open on Lesson Detail; Location Selector set to Brand A; Flagged checkbox is OFF

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher**; set Location Selector to Brand A | Add Teacher popup shows 5 unflagged teachers | Brand A total = 8 teachers; flagged = 3; unflagged = 5; Flagged checkbox OFF |
| 2 | Read the match count display | Match count shows **5** | "" |
| 3 | Enable the **Flagged Teacher** checkbox | Filter updates without page reload | "" |
| 4 | Read the match count display | Match count updates to **8** (all teachers including 3 flagged) | "" |
| 5 | Disable the **Flagged Teacher** checkbox again | Filter updates without page reload | "" |
| 6 | Read the match count display | Match count returns to **5** | "" |

**Severity:** minor
**Priority:** medium

---

### [EN] Substitute Teacher – Subject Filter – Filter by eligible subject [TBC] – Only teachers with matching subject shown

**Description:** AC 02.1, BR-12 — Decision Table [TBC — subject scope for EN unconfirmed] — When a subject is selected in the Subject filter, the teacher list is limited to teachers with that eligible subject. **Note: This TC is pending confirmation of subject scope for EN (see clarification Q5).**

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Subject filter is available for EN (TBC)
- Teacher J: eligible subject = Math; Teacher K: eligible subject = English
- A lesson of type Math is open on Lesson Detail

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Locate the Subject filter in the popup | Subject filter is visible (TBC) | Subject filter label = "Subject" / "科目" |
| 3 | Select **Math** as the subject filter | Filter is applied | Teacher J: subject = Math; Teacher K: subject = English |
| 4 | Observe the teacher list | Teacher J **appears**; Teacher K does **not** appear | "" |

**Severity:** minor
**Priority:** medium

---
