# Test Cases: LT-96158 — [Riso] Core | Timeslot Master — Inactive Timeslot on Edit Lesson form

> Added 2026-10-08 from a QA-reported gap: existing PX-20328 checks the lesson detail only, not the Edit form. Qase suite 2719.

## Suite: [Riso] Timeslot Master - Active/Inactive

### [Riso] Timeslot - Inactive Timeslot - Edit lesson already assigned to it - Timeslot still shown as selected in Edit form

**Qase:** PX-29633 · **Bug:** [LT-112874](https://manabie.atlassian.net/browse/LT-112874)

**Description:** AC US02.4 - Regression + Negative: A lesson keeps showing its existing Timeslot in the Edit form after that Timeslot is deactivated; only new selection of an inactive Timeslot is blocked. Found 2026-10-08: the Edit form currently shows the Timeslot field blank because the dropdown only loads Active Timeslots — this case is expected to fail until fixed.

**Preconditions:**
- Partner config "Show Timeslot In Lesson" is ON
- HQ or CM Staff is logged in to Salesforce with Lesson edit permission
- Timeslot Master "Morning" (09:00 ~ 10:00) was Active when Lesson P1 was created
- Lesson P1 at Location A is dated 2026-10-21 09:00 - 10:00 and has Timeslot "Morning"
- Timeslot Master "Morning" has since been set to Active = false (Inactive)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson P1 detail in Salesforce | Lesson P1 detail shows Timeslot "Morning" | today = 2026-10-20; lesson_date = 2026-10-21; Morning = Inactive |
| 2 | HQ or CM Staff clicks Edit on Lesson P1 | The Edit form opens; the Timeslot field shows "Morning (09:00 ~ 10:00)" as the selected value (not blank) | expected selected = Morning |
| 3 | HQ or CM Staff looks at Start Time and End Time in the Edit form | Start Time = 09:00 and End Time = 10:00 | unchanged times |
| 4 | HQ or CM Staff opens Lesson Calendar for Location A on 2026-10-21, clicks Lesson P1 and opens the Edit popup | The Edit popup opens; the Timeslot field shows "Morning (09:00 ~ 10:00)" as the selected value (not blank) | surface = Lesson Calendar Edit popup; lesson_date = 2026-10-21 |

**Severity:** critical
**Priority:** high

---

### [Riso] Timeslot - Inactive Timeslot - Edit lesson and save without touching Timeslot - Timeslot value retained on the lesson

**Qase:** PX-29634 · **Bug:** [LT-112874](https://manabie.atlassian.net/browse/LT-112874)

**Description:** AC US02.4 - CRUD (update) + Regression: Saving the Edit form of a lesson whose Timeslot is inactive must not clear or replace the Timeslot. Found 2026-10-08: the Edit form currently shows the Timeslot field blank because the dropdown only loads Active Timeslots — this case is expected to fail until fixed.

**Preconditions:**
- Partner config "Show Timeslot In Lesson" is ON
- HQ or CM Staff is logged in to Salesforce with Lesson edit permission
- Timeslot Master "Morning" (09:00 ~ 10:00) was Active when Lesson P1 was created
- Lesson P1 at Location A is dated 2026-10-21 09:00 - 10:00 and has Timeslot "Morning"
- Timeslot Master "Morning" has since been set to Active = false (Inactive)
- Lesson P1 has Lesson Name "Math P1"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson P1 in Salesforce and clicks Edit | The Edit form opens | today = 2026-10-20; Morning = Inactive |
| 2 | HQ or CM Staff changes Lesson Name to "Math P1 updated", does not touch the Timeslot field and clicks Save | The lesson is saved without error | only Lesson Name changed |
| 3 | HQ or CM Staff reopens Lesson P1 detail | Lesson Name = "Math P1 updated"; Timeslot still shows "Morning"; time is still 09:00 - 10:00 | expected Timeslot = Morning (retained) |
| 4 | HQ or CM Staff clicks Edit on Lesson P1 again and clicks Save without any change, then reopens Lesson P1 detail | Timeslot still shows "Morning" | second save, no change |

**Severity:** critical
**Priority:** high

---
