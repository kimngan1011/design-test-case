# Test Cases: LT-68996 — A.ver eligible subject filter

## Suite: Teacher list eligible subject filter

### [A.ver] Teacher List – Eligible subject filter – Multiple selected subjects – Only full matches are displayed

**Description:** AC 01, AC 04 — Decision Table — The Teacher list applies AND matching to the selected eligible subjects.

**Preconditions:**
- Logged in as HQ or CM Staff to the A.ver Salesforce org.
- The eligible-subject filter customization is enabled for A.ver.
- Teacher A is eligible for Mathematics, English, and Science; Teacher B is eligible for Mathematics and English; Teacher C is eligible for Mathematics and Science.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Teacher list. | The Eligible Subject filter is available. | tenant = A.ver |
| 2 | Select Mathematics, English, and Science in the Eligible Subject filter. | All three subjects appear as active criteria. | required_subjects = {Mathematics, English, Science} |
| 3 | Apply the filter. | Teacher A is displayed; Teachers B and C are not displayed. | Teacher A = all 3; Teacher B = Mathematics, English; Teacher C = Mathematics, Science |

**Severity:** major
**Priority:** high

---

### [A.ver] Teacher List – Eligible subject filter – Partial match – Teacher is omitted from results

**Description:** AC 02 — Negative — A teacher who matches one of two selected subjects is omitted from the filtered list.

**Preconditions:**
- Logged in as HQ or CM Staff to the A.ver Salesforce org.
- The eligible-subject filter customization is enabled for A.ver.
- Teacher B is eligible for Mathematics only; Teacher C is eligible for English only; no teacher is eligible for both subjects.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Teacher list. | The Eligible Subject filter is available. | tenant = A.ver |
| 2 | Select Mathematics and English in the Eligible Subject filter. | Both subjects appear as active criteria. | required_subjects = {Mathematics, English} |
| 3 | Apply the filter. | The list shows no matching teacher. | Teacher B = {Mathematics}; Teacher C = {English}; full_matches = none |
| 4 | Search for Teacher B and Teacher C. | Neither teacher is returned while both subjects remain selected. | search_names = Teacher B, Teacher C |

**Severity:** major
**Priority:** high

---

### Teacher List – Eligible subject filter – Non-A.ver tenant – Existing OR matching is retained

**Description:** AC 05 — Regression — The tenant-specific configuration does not change the existing non-A.ver OR filter behavior.

**Preconditions:**
- Logged in as HQ or CM Staff to a non-A.ver tenant where the A.ver customization is not enabled.
- Teacher B is eligible for Mathematics only; Teacher C is eligible for English only.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Teacher list. | The Eligible Subject filter is available. | tenant = non-A.ver; eligible-subject-filter-config = disabled |
| 2 | Select Mathematics and English in the Eligible Subject filter. | Both subjects appear as active criteria. | selected_subjects = {Mathematics, English} |
| 3 | Apply the filter. | Teachers B and C are displayed because each matches at least one selected subject. | expected_matching_rule = OR; Teacher B = {Mathematics}; Teacher C = {English} |

**Severity:** major
**Priority:** high
