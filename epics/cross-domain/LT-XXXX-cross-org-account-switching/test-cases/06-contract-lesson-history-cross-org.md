# Test Cases: LT-XXXX — Cross-organization account switching

## Suite: [Riso] OOP| Contract and Monthly Lesson history (App)

### [Riso] Account Switch – Contract and Lesson History – Riso and Nichibei students – Visibility follows organization

**Description:** AC PX-3249.01 — Decision Table — Contract Info and Lesson History are displayed for Riso and hidden for Nichibei after a parent switches students.

**Preconditions:**
- Parent CrossOrg is logged in to the mobile app.
- Parent CrossOrg is linked to Student Riso at Riso.
- Parent CrossOrg is linked to Student Nichibei at Nichibei.
- Student Riso has Contract Info and Lesson History records.
- Student Nichibei has lesson records.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Parent CrossOrg selects Student Riso and opens the account menu. | The account menu provides Contract Info and Lesson History for Student Riso. | selected student = Student Riso; organization = Riso |
| 2 | Parent CrossOrg opens Contract Info and Lesson History for Student Riso. | Contract Info and Lesson History display Student Riso's records. | selected student = Student Riso |
| 3 | Parent CrossOrg switches to Student Nichibei and opens the account menu. | Contract Info and Lesson History are not available for Student Nichibei. | selected student = Student Nichibei; organization = Nichibei |
| 4 | Parent CrossOrg switches back to Student Riso and opens the account menu. | Contract Info and Lesson History are available again for Student Riso. | selected student = Student Riso; organization = Riso |

**Severity:** minor
**Priority:** medium
