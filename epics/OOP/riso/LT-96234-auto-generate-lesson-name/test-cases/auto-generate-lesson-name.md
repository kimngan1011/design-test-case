# Test Cases: LT-96234 — [Riso] Auto Generate Lesson Name

## Suite: Auto Generate Lesson Name

### [Riso] Auto Generate Lesson Name – Create Lesson – Subject and Course provided – Name set as [Subject] - [Course]

**Description:** AC 01.1 — Decision Table — First save with Subject = "Math" and Course = "Course A" produces Lesson Name = "Math - Course A".

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Subject Master contains "Math"
- Course Master contains "Course A"
- A new lesson has not been saved yet

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Lessons and click **New Lesson** | Lesson creation form opens | "" |
| 2 | Set **Teaching Method** = Individual | Teaching Method shows "Individual"; Course field appears on the form | "" |
| 3 | Select **Subject** = "Math" | Subject field shows "Math" | Subject: "Math" |
| 4 | Select **Course** = "Course A" | Course field shows "Course A" | Course: "Course A" |
| 5 | Fill all remaining required fields (date, time, location) and click **Save** | Lesson saved without error | Date: any valid future date; Location: any available |
| 6 | Open the newly created lesson's detail page | Lesson detail page loads | "" |
| 7 | Observe the **Lesson Name** field | Lesson Name = "Math - Course A" | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] Auto Generate Lesson Name – Create Lesson – Subject provided, Course blank – Name set as [Subject]

**Description:** AC 01.2 — Decision Table — First save with Subject = "Science" and Course blank produces Lesson Name = "Science".

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Subject Master contains "Science"
- A new lesson has not been saved yet

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Lessons and click **New Lesson** | Lesson creation form opens | "" |
| 2 | Set **Teaching Method** = Individual | Teaching Method shows "Individual"; Course field appears | "" |
| 3 | Select **Subject** = "Science" | Subject field shows "Science" | Subject: "Science" |
| 4 | Leave **Course** blank (do not select any value) | Course field remains empty | Course: blank |
| 5 | Fill required fields and click **Save** | Lesson saved | "" |
| 6 | Open the new lesson's detail page | Lesson detail loads | "" |
| 7 | Observe the **Lesson Name** field | Lesson Name = "Science" | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] Auto Generate Lesson Name – Create Lesson – Subject and Course blank – Name set as -

**Description:** AC 01.3 — Decision Table — First save with both Subject blank and Course blank produces Lesson Name = "-".

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A new lesson has not been saved yet

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Lessons and click **New Lesson** | Lesson creation form opens | "" |
| 2 | Set **Teaching Method** = Individual | Teaching Method shows "Individual" | "" |
| 3 | Leave **Subject** blank | Subject field is empty | Subject: blank |
| 4 | Leave **Course** blank | Course field is empty | Course: blank |
| 5 | Fill required fields and click **Save** | Lesson saved | "" |
| 6 | Open the new lesson's detail page | Lesson detail loads | "" |
| 7 | Observe the **Lesson Name** field | Lesson Name = "-" | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] Auto Generate Lesson Name – Create Lesson – Subject blank, Course provided – Name set as -

**Description:** AC 01.3 — Decision Table (edge case) — First save with Subject blank and Course = "Course B" produces Lesson Name = "-"; Course alone does not contribute to name generation when Subject is absent.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Course Master contains "Course B"
- A new lesson has not been saved yet

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Lessons and click **New Lesson** | Lesson creation form opens | "" |
| 2 | Set **Teaching Method** = Individual | Teaching Method shows "Individual"; Course field appears | "" |
| 3 | Leave **Subject** blank | Subject field is empty | Subject: blank |
| 4 | Select **Course** = "Course B" | Course field shows "Course B" | Course: "Course B" |
| 5 | Fill required fields and click **Save** | Lesson saved | "" |
| 6 | Open the new lesson's detail page | Lesson detail loads | "" |
| 7 | Observe the **Lesson Name** field | Lesson Name = "-" (Course alone does not produce a name when Subject is absent) | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] Auto Generate Lesson Name – Edit Lesson After First Save – Subject changed – Lesson Name unchanged

**Description:** AC 01.4 — State Transition — After auto-generation on first save, editing Subject to "English" does not re-trigger name generation; Lesson Name remains "Math - Course A".

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A Riso lesson already exists with: Subject = "Math", Course = "Course A", Lesson Name = "Math - Course A" (auto-generated on first save)
- Subject Master contains "English"

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the existing Riso lesson detail page | Lesson Name shows "Math - Course A" | "" |
| 2 | Click **Edit** on the lesson | Lesson edit form opens; Lesson Name field shows "Math - Course A" | "" |
| 3 | Change **Subject** to "English" | Subject field shows "English" | Subject: "English" |
| 4 | Click **Save** | Lesson saved without error | "" |
| 5 | Observe the **Lesson Name** field on the detail page | Lesson Name still = "Math - Course A" (not regenerated to "English - Course A") | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] Auto Generate Lesson Name – Lesson Name Field – Manual edit post-generation – Updated name persists on re-save

**Description:** AC 01.4 / AC 01.5 — State Transition — Manually editing Lesson Name after auto-generation saves the new value; a subsequent save does not revert to the auto-generated name.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A Riso lesson exists with auto-generated Lesson Name = "Math - Course A"

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Riso lesson detail page | Lesson Name = "Math - Course A" | "" |
| 2 | Click **Edit** | Edit form opens | "" |
| 3 | Clear the **Lesson Name** field and enter "Custom Lesson Name" | Lesson Name field shows "Custom Lesson Name" | Lesson Name: "Custom Lesson Name" |
| 4 | Click **Save** | Lesson saved | "" |
| 5 | Observe the **Lesson Name** field | Lesson Name = "Custom Lesson Name" | "" |
| 6 | Click **Edit** again (without changing any field) and click **Save** | Lesson saved | "" |
| 7 | Observe the **Lesson Name** field | Lesson Name still = "Custom Lesson Name" (not reverted to "Math - Course A") | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] Auto Generate Lesson Name – Recurring Creation – First save with 3 occurrences – All lessons have same auto-generated name

**Description:** AC 01.1 + BR-11 — State Transition — Creating a weekly recurring lesson (3 occurrences) with Subject = "Math" and Course = "Course A" causes all 3 lessons to have Lesson Name = "Math - Course A".

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Subject Master contains "Math"; Course Master contains "Course A"
- No lessons in this recurring series exist yet

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Lessons and click **New Lesson** | Lesson creation form opens | "" |
| 2 | Set **Lesson Type** = Recurring and **Frequency** = Weekly | Recurring fields appear | Lesson Type: Recurring; Frequency: Weekly |
| 3 | Set **Teaching Method** = Individual | Course field appears | "" |
| 4 | Select **Subject** = "Math" and **Course** = "Course A" | Both fields set | Subject: "Math"; Course: "Course A" |
| 5 | Set recurrence to 3 occurrences, fill required fields, and click **Save** | All 3 lessons in the chain are created | Occurrences: 3 |
| 6 | Open the **first** lesson in the chain and observe **Lesson Name** | Lesson Name = "Math - Course A" | Lesson #1 |
| 7 | Open the **second** lesson in the chain and observe **Lesson Name** | Lesson Name = "Math - Course A" | Lesson #2 |
| 8 | Open the **third** lesson in the chain and observe **Lesson Name** | Lesson Name = "Math - Course A" | Lesson #3 |

**Severity:** major
**Priority:** high

---

### [Riso] Auto Generate Lesson Name – Duplicate Lesson – First save of duplicate – Name auto-generated from source Subject and Course

**Description:** AC 01.4 + BR-12 — State Transition — Duplicating a Riso lesson and saving the duplicate for the first time triggers auto-generation using the source lesson's Subject and Course; the pre-filled Lesson Name is overwritten.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A Riso source lesson exists with Subject = "Math", Course = "Course A", Lesson Name = "Math - Course A"

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Riso source lesson (Lesson Name = "Math - Course A") | Lesson detail shows: Subject = "Math", Course = "Course A", Lesson Name = "Math - Course A" | "" |
| 2 | Click **Duplicate** | New lesson creation form opens; Subject = "Math", Course = "Course A" pre-filled from source | "" |
| 3 | Do not change Subject or Course | Fields remain as pre-filled | "" |
| 4 | Fill required fields (date, time) and click **Save** | Duplicate lesson saved | "" |
| 5 | Open the duplicate lesson's detail page | Lesson detail loads | "" |
| 6 | Observe the **Lesson Name** field | Lesson Name = "Math - Course A" (auto-generated from source Subject and Course on first save) | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Auto Generate Lesson Name – Back Office – Name created in SF – Visible in BO Lesson Detail and Lesson Management

**Description:** AC 01.1 — Regression (cross-surface) — Lesson Name auto-generated in SF is visible and consistent in BO Lesson Detail and BO Lesson Management list.

**Preconditions:**
- Logged in as HQ or CM Staff to both the Riso SF org and the Riso Back Office
- A Riso lesson has been created in SF with Subject = "Math", Course = "Course A"; auto-generated Lesson Name = "Math - Course A"

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Riso SF org lesson detail for the created lesson | SF Lesson detail shows Lesson Name = "Math - Course A" | "" |
| 2 | Open the Riso Back Office and navigate to the same lesson's **Lesson Detail** page | BO Lesson Detail page loads | "" |
| 3 | Observe the **Lesson Name** field in BO | Lesson Name = "Math - Course A" | "" |
| 4 | Navigate to **BO Lesson Management** list and locate the lesson | Lesson appears in the BO list | "" |
| 5 | Observe the **Lesson Name** column for this lesson | Lesson Name column shows "Math - Course A" | "" |

**Severity:** major
**Priority:** high
