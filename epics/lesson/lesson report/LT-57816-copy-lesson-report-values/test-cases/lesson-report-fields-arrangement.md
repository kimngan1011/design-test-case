# Test Cases: LT-108358 — Lesson Report fields arrangement SF<>BO

## Suite: Lesson Report Fields Arrangement

### Lesson Report – Internal Remark Labels – English and Japanese UI – Updated labels displayed

**Description:** AC 108358.1 — Component and Negative — Salesforce displays the specified English and Japanese labels instead of the legacy labels.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce and can open an editable Lesson Report.
- A Lesson Report exists with the internal-remark field visible in the English UI.
- The same Lesson Report is accessible in the Japanese UI.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | HQ or CM Staff opens the Lesson Report in the English UI. | The internal-remark field label displays exactly `Remark (Internal Only)`. | `locale = English; expected_label = Remark (Internal Only)` |
| 2 | HQ or CM Staff inspects the same field label in the English UI. | The label `Remarks` is not displayed for the internal-remark field. | `legacy_label = Remarks` |
| 3 | HQ or CM Staff switches to the Japanese UI and opens the same Lesson Report. | The internal-remark field label displays exactly `特筆事項（社内用)`. | `locale = Japanese; expected_label = 特筆事項（社内用)` |
| 4 | HQ or CM Staff inspects the same field label in the Japanese UI. | The label `備考` is not displayed for the internal-remark field. | `legacy_label = 備考` |

**Severity:** minor
**Priority:** medium

---

### Lesson Report – Content Requiredness – Optional on SF and BO – Blank value saved

**Description:** AC 108358.2 — Decision Table and Equivalence Partitioning — Both report surfaces present Content as optional and retain a blank value after save.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce and Back Office.
- An editable Lesson Report exists on Salesforce and its corresponding Back Office report is accessible.
- `Lesson_Report_Require_Fields_Setting` in Back Office configures `Content/[公開]授業内容` as optional.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | HQ or CM Staff opens the editable Lesson Report in Salesforce. | The `Content/[公開]授業内容` label does not display an asterisk. | `surface = Salesforce; content = blank; expected_required = false` |
| 2 | HQ or CM Staff clears `Content/[公開]授業内容` and saves the Salesforce report. | The Salesforce report saves and Content remains blank after refresh. | `surface = Salesforce; content = blank` |
| 3 | HQ or CM Staff opens the corresponding editable Lesson Report in Back Office. | The `Content/[公開]授業内容` label does not display an asterisk and the optional configuration is applied. | `surface = Back Office; config = Lesson_Report_Require_Fields_Setting; content = blank; expected_required = false` |
| 4 | HQ or CM Staff clears `Content/[公開]授業内容` and saves the Back Office report. | The Back Office report saves and Content remains blank after refresh. | `surface = Back Office; content = blank` |

**Severity:** major
**Priority:** high

---

### Lesson Report – Group Lesson Layout – Report Fields – Specified sequence displayed

**Description:** AC 108358.3 — Component and Scenario — Salesforce displays every group-lesson field in the specified relative order.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- An editable Group Lesson Report exists with values in Homework Completion, In-Lesson Quiz, Understanding, Remark (Internal Only), and CM Note.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | HQ or CM Staff opens the editable Group Lesson Report in Salesforce. | The Group Lesson Report displays Homework Completion, In-Lesson Quiz, Understanding, Remark (Internal Only), and CM Note. | `teaching_method = Group` |
| 2 | HQ or CM Staff reads the fields from the first listed field to the last listed field. | The fields appear in this exact relative order: Homework Completion, In-Lesson Quiz, Understanding, Remark (Internal Only), CM Note. | `expected_order = 1 Homework Completion; 2 In-Lesson Quiz; 3 Understanding; 4 Remark (Internal Only); 5 CM Note` |

**Severity:** minor
**Priority:** medium

---

### Lesson Report – Individual Lesson Layout – Report Fields – Specified sequence displayed

**Description:** AC 108358.4 — Component and Scenario — Salesforce displays every individual-lesson field in the specified relative order.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- An editable Individual Lesson Report exists with values in all fields covered by the ticket.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | HQ or CM Staff opens the editable Individual Lesson Report in Salesforce. | The Individual Lesson Report displays Content, Next Lesson’s Homework, Next Lesson's Announcement, Homework Completion, In-Lesson Quiz, Understanding, Remark (Internal Only), and CM Note. | `teaching_method = Individual` |
| 2 | HQ or CM Staff reads the fields from the first listed field to the last listed field. | The fields appear in this exact relative order: Content, Next Lesson’s Homework, Next Lesson's Announcement, Homework Completion, In-Lesson Quiz, Understanding, Remark (Internal Only), CM Note. | `expected_order = 1 Content; 2 Next Lesson’s Homework; 3 Next Lesson's Announcement; 4 Homework Completion; 5 In-Lesson Quiz; 6 Understanding; 7 Remark (Internal Only); 8 CM Note` |

**Severity:** minor
**Priority:** medium
