# Test Cases: LT-68996 — A.ver eligible subject filter

## Suite: Add Teacher eligible subject filter

### [A.ver] Lesson Teacher – Add Teacher – Multiple selected subjects – Only teachers eligible for every subject are listed

**Description:** AC 01, AC 04 — Decision Table — The Add Teacher search returns the intersection of eligible subjects for A.ver.

**Preconditions:**
- Logged in as HQ or CM Staff to the A.ver Salesforce org.
- The eligible-subject filter customization is enabled for A.ver.
- Teacher A is eligible for Mathematics and English; Teacher B is eligible for Mathematics only; Teacher C is eligible for English only.
- A lesson is open and supports adding a teacher.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the lesson's Add Teacher component. | The teacher search is available. | tenant = A.ver; selected_subjects = Mathematics, English |
| 2 | Select Mathematics and English as the required subjects. | The selected-subject criteria show both subjects. | required_subjects = {Mathematics, English} |
| 3 | View the available teachers. | Teacher A is listed; Teachers B and C are not listed. | Teacher A = {Mathematics, English}; Teacher B = {Mathematics}; Teacher C = {English} |

**Severity:** major
**Priority:** high

---

### [A.ver] Lesson Teacher – Add Teacher – Partial eligible-subject match – Teacher is excluded

**Description:** AC 02 — Negative — A teacher matching only a subset of the selected subjects cannot be selected.

**Preconditions:**
- Logged in as HQ or CM Staff to the A.ver Salesforce org.
- The eligible-subject filter customization is enabled for A.ver.
- Teacher B is eligible for Mathematics only; no teacher is eligible for both Mathematics and English.
- A lesson is open and supports adding a teacher.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the lesson's Add Teacher component. | The teacher search is available. | tenant = A.ver; Teacher B = {Mathematics} |
| 2 | Select Mathematics and English as the required subjects. | Both subjects are active filter criteria. | required_subjects = {Mathematics, English} |
| 3 | Search for Teacher B. | Teacher B is not returned and cannot be added. | matched_subjects = {Mathematics}; missing_subjects = {English} |
| 4 | View the teacher results without a name search. | The component shows no eligible teacher result. | eligible_for_all_selected_subjects = none |

**Severity:** major
**Priority:** high

---

### [A.ver] Lesson Teacher – Add Teacher – One selected subject – All teachers eligible for that subject remain listed

**Description:** AC 03 — Equivalence Partitioning — A single selected subject retains single-subject eligibility behavior.

**Preconditions:**
- Logged in as HQ or CM Staff to the A.ver Salesforce org.
- The eligible-subject filter customization is enabled for A.ver.
- Teacher A is eligible for Mathematics and English; Teacher B is eligible for Mathematics only; Teacher C is eligible for English only.
- A lesson is open and supports adding a teacher.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the lesson's Add Teacher component. | The teacher search is available. | tenant = A.ver |
| 2 | Select Mathematics as the only required subject. | Mathematics is the only active filter criterion. | required_subjects = {Mathematics} |
| 3 | View the available teachers. | Teachers A and B are listed; Teacher C is not listed. | Teacher A = {Mathematics, English}; Teacher B = {Mathematics}; Teacher C = {English} |

**Severity:** minor
**Priority:** medium
