# Test Cases: LT-96234 — [Riso] Course Field – Individual Teaching Method

## Suite: Course Field – Individual Teaching Method

### [Riso] Lesson Creation Form – Course Field – Teaching Method Individual selected – Course field shown and optional

**Description:** AC 03.1 + AC 03.2 — Component — When Teaching Method = Individual is selected in the Riso lesson creation form, the Course field appears and is not marked as required.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- On the New Lesson creation form

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Lessons and click **New Lesson** | Lesson creation form opens | "" |
| 2 | Select **Teaching Method** = Individual | Teaching Method shows "Individual" | "" |
| 3 | Observe the **Course** field on the form | Course field is visible on the form | "" |
| 4 | Observe whether the Course field is marked as required | Course field is not marked as required (no asterisk or required indicator) | "" |
| 5 | Leave Course blank, fill other required fields, and click **Save** | Lesson saved without a validation error for Course | "" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson Creation Form – Course Field – Teaching Method Group selected – Course field not shown

**Description:** AC 03.1 — Conditional logic (Negative) — When Teaching Method = Group, the Course field is not shown in the Riso lesson creation form.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- On the New Lesson creation form

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Lessons and click **New Lesson** | Lesson creation form opens | "" |
| 2 | Select **Teaching Method** = Group | Teaching Method shows "Group" | "" |
| 3 | Observe the form for the **Course** field | Course field is not visible (hidden for Group teaching method) | "" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson – Create Lesson – Individual TM, Course blank – Lesson saved and Name generated from Subject alone

**Description:** AC 03.2 — Equivalence Partitioning — Course is optional for Individual TM; lesson can be saved with Course blank, and Lesson Name is generated from Subject only.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Subject Master contains "Physics"
- New lesson not yet saved

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Lessons and click **New Lesson** | Lesson creation form opens | "" |
| 2 | Set **Teaching Method** = Individual | Course field appears | "" |
| 3 | Select **Subject** = "Physics" | Subject shows "Physics" | Subject: "Physics" |
| 4 | Leave **Course** blank | Course field remains empty | Course: blank |
| 5 | Fill required fields and click **Save** | Lesson saved without error (Course is optional; no validation error) | "" |
| 6 | Open the lesson detail and observe **Lesson Name** | Lesson Name = "Physics" | "" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson – Create Lesson – Individual TM, Subject and Course provided – Course contributes to auto-generated name

**Description:** AC 03.3 — Decision Table — When Teaching Method = Individual and both Subject = "Chemistry" and Course = "Course C" are provided, Course participates in name generation producing Lesson Name = "Chemistry - Course C".

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Subject "Chemistry" and Course "Course C" exist in master data
- New lesson not yet saved

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Lessons and click **New Lesson** | Lesson creation form opens | "" |
| 2 | Set **Teaching Method** = Individual | Course field appears | "" |
| 3 | Select **Subject** = "Chemistry" | Subject shows "Chemistry" | Subject: "Chemistry" |
| 4 | Select **Course** = "Course C" | Course shows "Course C" | Course: "Course C" |
| 5 | Fill required fields and click **Save** | Lesson saved | "" |
| 6 | Open the lesson detail and observe **Lesson Name** | Lesson Name = "Chemistry - Course C" (Course contributed to name generation) | "" |

**Severity:** minor
**Priority:** medium
