# Test Cases: LT-68996 — A.ver eligible subject filter

## Suite: Calendar eligible subject filter

### [A.ver] Calendar – Teacher filter – Multiple selected subjects – Only full eligible-subject matches are available

**Description:** AC 01, AC 04 — Decision Table — The Manacalendar teacher filter uses AND matching for A.ver.

**Preconditions:**
- Logged in as HQ or CM Staff to the A.ver Salesforce org.
- The eligible-subject filter customization is enabled for A.ver.
- Teacher A is eligible for Mathematics and English; Teacher B is eligible for Mathematics only; Teacher C is eligible for English only.
- The calendar contains lessons for each teacher in the active calendar range.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Manacalendar. | The Calendar filter is available. | tenant = A.ver; calendar_range = 2026-07-20 to 2026-07-26 |
| 2 | Open the Teacher filter and select Mathematics and English. | Both subjects appear as active eligibility criteria. | required_subjects = {Mathematics, English} |
| 3 | View the available teacher choices. | Teacher A is available; Teachers B and C are unavailable. | Teacher A = {Mathematics, English}; Teacher B = {Mathematics}; Teacher C = {English} |
| 4 | Select Teacher A and apply the filter. | Only Teacher A's lessons are shown in the calendar range. | selected_teacher = Teacher A |

**Severity:** major
**Priority:** high

---

### [A.ver] Calendar – Teacher filter – Partial eligible-subject match – Teacher and lessons are excluded

**Description:** AC 02 — Negative — A partial eligible-subject match is not available and cannot populate the calendar.

**Preconditions:**
- Logged in as HQ or CM Staff to the A.ver Salesforce org.
- The eligible-subject filter customization is enabled for A.ver.
- Teacher B is eligible for Mathematics only and has lessons in the active calendar range.
- No teacher is eligible for both Mathematics and English.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Manacalendar. | The Calendar filter is available. | tenant = A.ver; calendar_range = 2026-07-20 to 2026-07-26 |
| 2 | Select Mathematics and English in the Teacher filter. | Both subjects appear as active eligibility criteria. | required_subjects = {Mathematics, English} |
| 3 | Search for Teacher B in the available teacher choices. | Teacher B is unavailable for selection. | Teacher B = {Mathematics}; missing_subjects = {English} |
| 4 | Apply the filter without a teacher selection. | No Teacher B lesson is shown; the calendar indicates no eligible teacher match. | eligible_for_all_selected_subjects = none |

**Severity:** major
**Priority:** high

---

### [A.ver] Calendar – Teacher filter – One selected subject – Teachers eligible for that subject remain available

**Description:** AC 03 — Equivalence Partitioning — A one-subject Calendar filter returns every eligible teacher for that subject.

**Preconditions:**
- Logged in as HQ or CM Staff to the A.ver Salesforce org.
- The eligible-subject filter customization is enabled for A.ver.
- Teacher A is eligible for Mathematics and English; Teacher B is eligible for Mathematics only; Teacher C is eligible for English only.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Manacalendar. | The Calendar filter is available. | tenant = A.ver; calendar_range = 2026-07-20 to 2026-07-26 |
| 2 | Select Mathematics as the only subject in the Teacher filter. | Mathematics is the only active eligibility criterion. | required_subjects = {Mathematics} |
| 3 | View the available teacher choices. | Teachers A and B are available; Teacher C is unavailable. | Teacher A = {Mathematics, English}; Teacher B = {Mathematics}; Teacher C = {English} |

**Severity:** minor
**Priority:** medium
