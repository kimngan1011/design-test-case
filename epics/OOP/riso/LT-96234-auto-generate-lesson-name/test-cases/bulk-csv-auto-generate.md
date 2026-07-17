# Test Cases: LT-96234 — [Riso] Bulk Create Lesson – CSV Auto Generate

## Suite: Bulk CSV Auto Generate

### [Riso] Bulk Create Lesson – CSV Import – Subject and Course provided – Name auto-generated as [Subject] - [Course]

**Description:** AC 02.1 (BR-06) — Decision Table — A CSV row with Subject = "Math" and Course = "Course A" produces Lesson Name = "Math - Course A" after import.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Bulk Create Lesson CSV template prepared: one row with Subject = "Math", Course = "Course A", Lesson Name column = blank, all required fields filled
- "Math" and "Course A" exist in master data

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to the **Bulk Create Lesson** feature in the Riso SF org | Bulk Create Lesson page opens | "" |
| 2 | Upload the prepared CSV file | File accepted; import preview or confirmation shown | CSV: Subject="Math", Course="Course A", Lesson Name=blank |
| 3 | Confirm and submit the import | Import runs; success message shown | "" |
| 4 | Navigate to Lessons and find the imported lesson | Lesson appears in the list | "" |
| 5 | Open the imported lesson's detail page | Lesson detail loads | "" |
| 6 | Observe the **Lesson Name** field | Lesson Name = "Math - Course A" | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Create Lesson – CSV Import – Subject provided, Course blank – Name auto-generated as [Subject]

**Description:** AC 02.1 — Decision Table — CSV row with Subject = "Science" and Course blank produces Lesson Name = "Science".

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- CSV prepared: Subject = "Science", Course = blank, Lesson Name = blank, required fields filled

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Bulk Create Lesson | Bulk Create Lesson page opens | "" |
| 2 | Upload CSV with Subject = "Science" and Course blank | File accepted | Subject="Science", Course=blank |
| 3 | Confirm and submit | Import succeeds | "" |
| 4 | Open the imported lesson's detail page | Lesson detail loads | "" |
| 5 | Observe the **Lesson Name** field | Lesson Name = "Science" | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Create Lesson – CSV Import – Subject and Course blank – Name auto-generated as -

**Description:** AC 02.1 — Decision Table — CSV row with both Subject and Course blank produces Lesson Name = "-".

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- CSV prepared: Subject = blank, Course = blank, Lesson Name = blank, required fields filled

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Bulk Create Lesson | Bulk Create Lesson page opens | "" |
| 2 | Upload CSV with Subject blank and Course blank | File accepted | Subject=blank, Course=blank |
| 3 | Confirm and submit | Import succeeds | "" |
| 4 | Open the imported lesson's detail page | Lesson detail loads | "" |
| 5 | Observe the **Lesson Name** field | Lesson Name = "-" | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Create Lesson – CSV Import – Lesson Name pre-populated in CSV row – Auto-generated name overrides pre-populated value

**Description:** AC 02.1 + BR-13 — Negative / Data Integrity — When a CSV row has Lesson Name = "Old Name" pre-filled alongside Subject = "Math" and Course = "Course A", the import overrides the pre-populated value with the auto-generated name "Math - Course A".

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- CSV prepared: Subject = "Math", Course = "Course A", Lesson Name = "Old Name", required fields filled
- "Math" and "Course A" exist in master data

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Bulk Create Lesson | Bulk Create Lesson page opens | "" |
| 2 | Upload CSV where Lesson Name = "Old Name", Subject = "Math", Course = "Course A" | File accepted | Lesson Name="Old Name", Subject="Math", Course="Course A" |
| 3 | Confirm and submit the import | Import succeeds | "" |
| 4 | Open the imported lesson's detail page | Lesson detail loads | "" |
| 5 | Observe the **Lesson Name** field | Lesson Name = "Math - Course A" (auto-generated; pre-populated "Old Name" was overridden) | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Create Lesson – CSV Import – Multiple rows with different combinations – Each row receives independent auto-generated name

**Description:** AC 02.1 — Decision Table — A 3-row CSV with different Subject/Course values per row produces a distinct auto-generated Lesson Name for each lesson independently.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- CSV prepared with 3 rows:
  - Row 1: Subject = "Math", Course = "Course A", Lesson Name = blank
  - Row 2: Subject = "English", Course = blank, Lesson Name = blank
  - Row 3: Subject = blank, Course = blank, Lesson Name = blank
- All rows have other required fields filled

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Bulk Create Lesson | Bulk Create Lesson page opens | "" |
| 2 | Upload the 3-row CSV | File accepted; 3 lessons shown in import preview | Row 1: Subject="Math", Course="Course A"; Row 2: Subject="English", Course=blank; Row 3: Subject=blank, Course=blank |
| 3 | Confirm and submit | All 3 lessons imported | "" |
| 4 | Open the lesson from **Row 1** and observe **Lesson Name** | Lesson Name = "Math - Course A" | Row 1 |
| 5 | Open the lesson from **Row 2** and observe **Lesson Name** | Lesson Name = "English" | Row 2 |
| 6 | Open the lesson from **Row 3** and observe **Lesson Name** | Lesson Name = "-" | Row 3 |

**Severity:** major
**Priority:** high
