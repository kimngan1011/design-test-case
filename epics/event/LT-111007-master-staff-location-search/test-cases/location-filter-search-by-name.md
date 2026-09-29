# Test Cases: LT-111007 — Search location by name in the Location filter

## Suite: [Renseikai] Add Master Staff – Location Filter (Qase 2614)

### [Renseikai] Add Master Staff – Location filter – Part of a location name typed – Matching location suggested and selecting it filters the staff list

**Description:** LT-111007 (bug fix) / LT-96178 AC 6 — Scenario — In the Add Master Staff popup, typing part of a location name in the Location filter lists only the matching locations; the selected location then filters the staff list.

**Spec sources:**
- [S1] Jira LT-111007 – [ERPv2] [Master Staff] Cannot search for location name in Location filter on Add Master Staff form — https://manabie.atlassian.net/browse/LT-111007
- [S2] Jira LT-96178 – [Renseikai] Core | Add Location Filter to Master Staff — https://manabie.atlassian.net/browse/LT-96178
- [S3] Jira LT-88464 / LT-88578 – Can not find out location name on activity event creation form, add master participant form and add master staff form (closed) — https://manabie.atlassian.net/browse/LT-88464

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce
- LT-96178 feature is enabled for Renseikai
- Center locations Loc_A = "Shibuya" and Loc_C = "Umeda" exist; no other location name contains "Ume"
- Event Master EM01 has Target Location = Loc_A only
- Staff_A is associated with Loc_A only
- Staff_C is associated with Loc_C only

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Add Master Staff popup from EM01 | The popup opens with the Location filter pre-populated with Loc_A; Staff_A is shown and Staff_C is not shown |  |
| 2 | HQ or CM Staff opens the filter panel, clicks into the Location field and types "Ume" | The location suggestion list shows Umeda (Loc_C); Shibuya (Loc_A) and locations whose name does not contain "Ume" are not listed; "No options" is not shown | Keyword = "Ume" |
| 3 | HQ or CM Staff selects Umeda from the suggestions | Umeda is added to the Location filter next to Shibuya | Filter: Loc_A, Loc_C |
| 4 | HQ or CM Staff removes Shibuya from the Location filter and clicks Apply | The staff list shows Staff_C; Staff_A is not shown | Filter: Loc_C |

**Severity:** major
**Priority:** medium

---

## Suite: Activity Event – Lookup Fields & Draft API Filter (Qase 2611)

### Create Activity Event – Location field – Part of a location name typed – Matching location suggested and saved on the event

**Description:** LT-111007 (same location search) / regression of LT-88464, LT-88578 — Scenario — On the Create Activity Event form, typing part of a location name in the Location field lists only the matching open locations; the selected location is saved on the Activity Event.

**Spec sources:**
- [S1] Jira LT-111007 – [ERPv2] [Master Staff] Cannot search for location name in Location filter on Add Master Staff form — https://manabie.atlassian.net/browse/LT-111007
- [S3] Jira LT-88464 / LT-88578 – Can not find out location name on activity event creation form, add master participant form and add master staff form (closed) — https://manabie.atlassian.net/browse/LT-88464
- [S4] Qase PX-11198 – Location field excludes Closed Down locations (LT-86517) — https://app.qase.io/case/PX-11198

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce
- Center locations Loc_A = "Shibuya" and Loc_C = "Umeda" exist; no other location name contains "Ume"
- Loc_C (Umeda) is not a Closed Down location
- Event Master EM01 exists
- The Activity Event list page is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff clicks New on the Activity Event list page | The Create Activity Event form opens |  |
| 2 | HQ or CM Staff clicks into the Location field and types "Ume" | The location suggestion list shows Umeda (Loc_C); Shibuya (Loc_A) and locations whose name does not contain "Ume" are not listed; "No options" is not shown | Keyword = "Ume" |
| 3 | HQ or CM Staff selects Umeda from the suggestions | The Location field shows Umeda | Location = Loc_C |
| 4 | HQ or CM Staff fills the required fields and clicks Save | The Activity Event is created and its detail shows Location = Umeda | Event Master = EM01; Event Name = LT111007-AE; Start / End = any future slot |

**Severity:** major
**Priority:** medium

---

## Suite: Add master participant (Qase 2618)

### Add Master Participant – Location filter – Part of a location name typed – Matching location suggested and selecting it filters the student list

**Description:** LT-111007 (same Location filter) / regression of LT-88464, LT-88578 — Scenario — In the Add Participant popup, typing part of a location name in the Location filter lists only the matching locations; the selected location then filters the student list.

**Spec sources:**
- [S1] Jira LT-111007 – [ERPv2] [Master Staff] Cannot search for location name in Location filter on Add Master Staff form — https://manabie.atlassian.net/browse/LT-111007
- [S3] Jira LT-88464 / LT-88578 – Can not find out location name on activity event creation form, add master participant form and add master staff form (closed) — https://manabie.atlassian.net/browse/LT-88464

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce
- Center locations Loc_A = "Shibuya" and Loc_C = "Umeda" exist; no other location name contains "Ume"
- Event Master EM01 exists (no target segment set) and its record page is open
- Student_A (Enrolled) is at Loc_A only
- Student_C (Enrolled) is at Loc_C only

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff clicks the 'Add Master Participant' button in the Event Master header | The 'Add Participant' popup opens with the student list |  |
| 2 | HQ or CM Staff clicks the filter icon (funnel), clicks into the Location field and types "Ume" | The location suggestion list shows Umeda (Loc_C); Shibuya (Loc_A) and locations whose name does not contain "Ume" are not listed; "No options" is not shown | Keyword = "Ume" |
| 3 | HQ or CM Staff selects Umeda from the suggestions and clicks Apply | The student list shows Student_C and every row has Location = Umeda; Student_A is not shown | Filter: Location = Loc_C; Enrollment Status = Enrolled, Temporary (default) |

**Severity:** major
**Priority:** medium

---
