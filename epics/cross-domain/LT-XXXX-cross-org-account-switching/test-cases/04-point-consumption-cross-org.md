# Test Cases: LT-XXXX — Cross-organization account switching

## Suite: Point Consumption

### Account Switch – Point Consumption – Nichibei and Renseikai students – Visibility follows organization

**Description:** AC PX-504.01 — Decision Table — Point Consumption is available for a Nichibei student and unavailable for a Renseikai student after switching accounts.

**Preconditions:**
- Parent CrossOrg is logged in to the mobile app.
- Parent CrossOrg is linked to Student Nichibei at Nichibei.
- Parent CrossOrg is linked to Student Renseikai at Renseikai.
- Student Nichibei has a lesson allocation with Point Consumption information.
- Student Renseikai has a lesson allocation.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Parent CrossOrg selects Student Nichibei and opens the lesson allocation or contract screen. | The Point Consumption information is displayed for Student Nichibei. | selected student = Student Nichibei; organization = Nichibei |
| 2 | Parent CrossOrg switches to Student Renseikai and opens the lesson allocation or contract screen. | Point Consumption information is not displayed for Student Renseikai. | selected student = Student Renseikai; organization = Renseikai |
| 3 | Parent CrossOrg switches back to Student Nichibei. | Point Consumption information is displayed again only for Student Nichibei. | selected student = Student Nichibei; organization = Nichibei |

**Severity:** minor
**Priority:** medium
