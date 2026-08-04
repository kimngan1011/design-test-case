# Test Cases: LT-105350 — [EN] Finding and Emailing Substitute Teacher Candidates

## Suite: Email Compose & Send

### [EN] Substitute Teacher – Send Email – No candidate selected, click Send Email – Email editor blocked and error message displayed

**Description:** AC 03.1, BR-13 — Equivalence Partitioning + Negative — When no teacher is selected in the candidate list and the staff clicks "Send Email", the email editor does not open and an error message is displayed.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Add Teacher popup is open; no teacher checkbox is selected (0 selections)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Confirm that no teacher is selected (all checkboxes are unchecked) | 0 teachers selected | Selected count = 0 |
| 3 | Click the **Send Email** (メールを送信する) button | Email editor popup does **not** open; an error message appears within or below the popup | "" |
| 4 | Observe the error message | An error message is displayed to the user | "" |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Send Email – No candidate selected – Error message shows exact English text

**Description:** AC 03.1, BR-14 — Component — When "Send Email" is clicked with 0 candidates selected, the error message displays the exact English string "Please select one or more Teachers."

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Add Teacher popup is open; no teacher is selected; EN locale is active

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Ensure no teacher is selected and click **Send Email** | Error message is displayed | Selected count = 0 |
| 3 | Read the error message text | Error message reads exactly: **Please select one or more Teachers.** | Expected text = "Please select one or more Teachers." |

**Severity:** minor
**Priority:** medium

---

### [EN] Substitute Teacher – Send Email – No candidate selected – Error message shows exact Japanese text

**Description:** AC 03.1, BR-14 — Component — When "Send Email" is clicked with 0 candidates selected, the error message displays the exact Japanese string "1人以上の講師を選択してください".

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Add Teacher popup is open; no teacher is selected; JP locale is active (or bilingual display is enabled)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Ensure no teacher is selected and click **Send Email** (メールを送信する) | Error message is displayed | Selected count = 0 |
| 3 | Read the Japanese error message text | Error message reads exactly: **1人以上の講師を選択してください** | Expected text = "1人以上の講師を選択してください" |

**Severity:** minor
**Priority:** medium

---

### [EN] Substitute Teacher – Send Email – At least one candidate selected – Email editor opens

**Description:** AC 03.1, BR-13 — Equivalence Partitioning — When at least one teacher is selected in the candidate list and the staff clicks "Send Email", the email editor popup opens successfully.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- Add Teacher popup is open; at least 1 teacher is selected (checkbox checked)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Select at least 1 teacher from the candidate list | 1 teacher is selected (checkbox checked) | Selected count = 1 |
| 3 | Click the **Send Email** (メールを送信する) button | Email editor popup opens; no error message is shown | "" |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Email Editor – Open with multiple candidates selected – Candidate count and PRD template shown

**Description:** AC 03.2, BR-16, BR-17 — Component — When the email editor opens with multiple candidates selected, it displays the correct candidate count, default subject/title, and body template from the PRD.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Add Teacher popup is open; 3 teachers (Teacher A, Teacher B, Teacher C) are selected

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In the Add Teacher popup, select 3 teachers and click **Send Email** | Email editor popup opens | Selected teachers = Teacher A, Teacher B, Teacher C; count = 3 |
| 2 | Observe the candidate count indicator in the email editor | The count shows **3** (matching the number of selected teachers) | "" |
| 3 | Observe the email subject/title field | The subject/title field is pre-filled with **代講をお願いいたします** | Expected subject/title = "代講をお願いいたします" |
| 4 | Observe the email body area | The email body text area is pre-filled with the PRD template lines **案件名：** and **時間：** | Expected body template = "案件名：<br>時間：" |
| 5 | Observe the email body content type | The body area accepts text input only; no rich text formatting controls (bold, images, etc.) | "" |

**Severity:** minor
**Priority:** medium

---

### [EN] Substitute Teacher – Email Editor – Default subject/title template – Subject matches PRD

**Description:** AC 03.2, BR-17 — Component — The email editor uses the default EN subject/title template confirmed in the PRD.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Add Teacher popup is open; at least 1 teacher is selected

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click **Send Email** | Email editor popup opens | Selected count >= 1 |
| 2 | Observe the subject/title field | Subject/title is pre-filled exactly as **代講をお願いいたします** | Expected subject/title = "代講をお願いいたします" |
| 3 | Edit the subject/title field | User can edit the subject/title text before sending | Subject/title = "代講をお願いいたします（確認）" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Email Editor – Default body template – Body contains PRD lines

**Description:** AC 03.2, BR-17 — Component — The email body opens with the default text-only PRD template containing `案件名：` and `時間：`.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Add Teacher popup is open; at least 1 teacher is selected

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click **Send Email** | Email editor popup opens | Selected count >= 1 |
| 2 | Observe the email body field | Body contains **案件名：** on one line and **時間：** on the next line | Expected body = "案件名：<br>時間：" |
| 3 | Add text after each template label | Body remains editable as text-only content | 案件名：Lesson A; 時間：2026-08-01 10:00-11:00 JST |
| 4 | Verify formatting controls | No rich text/image formatting controls are available | Text-only template |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Bulk Send – Confirm send with multiple candidates – All selected candidates in recipient list

**Description:** AC 03.2, BR-15, BR-18 — CRUD — When the staff composes an email in the editor and confirms sending, the system generates a recipient list containing all selected teachers' email addresses.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher A (email: teacher-a@example.com), Teacher B (email: teacher-b@example.com), Teacher C (email: teacher-c@example.com) are selected
- Email editor is open with count = 3 and the PRD subject/body template loaded

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In the email editor, type an email body message | Body text is entered | Email body = "授業の日時について代講をお願いできますか。" |
| 2 | Click the send/confirm button in the email editor | The system processes the send action | "" |
| 3 | Verify the system-generated recipient list (via confirmation message, log, or review) | The recipient list includes all 3 selected teachers: teacher-a@example.com, teacher-b@example.com, teacher-c@example.com | Teacher A: teacher-a@example.com; Teacher B: teacher-b@example.com; Teacher C: teacher-c@example.com |
| 4 | Confirm that no teacher is missing from the recipient list | All 3 emails are present; no selected teacher is omitted | "" |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Bulk Send – 50 candidates selected – Email can be prepared and sent without recipient cap error

**Description:** AC 03.2, BR-15, BR-18, BR-22 — Boundary Value Analysis — EN expected average recipient volume is around 50 teachers. Selecting and sending to 50 candidates must be supported without arbitrary recipient-cap blocking.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- 50 teacher candidates exist with valid email addresses and pass current filters
- Add Teacher popup is open with 50 candidates selected

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click **Send Email** | Email editor opens successfully | Selected count = 50 |
| 2 | Observe candidate count and recipient list | Candidate count = 50; recipient list contains 50 unique email addresses | Expected recipient count = 50 |
| 3 | Confirm send | Email send is accepted; no arbitrary 50-recipient cap error is shown | "" |
| 4 | Verify dispatch result or log | All 50 selected candidates are included in dispatch/log result | 50 unique teacher Contacts |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Bulk Send – 70 to 80 candidates selected – Flow supports high EN recipient volume

**Description:** AC 03.2, BR-15, BR-18, BR-22 — Boundary Value Analysis — EN may send offers to 70-80 teachers. The flow must support this higher volume and must not silently truncate recipients.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- 80 teacher candidates exist with valid email addresses and pass current filters
- Add Teacher popup is open with 80 candidates selected

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click **Send Email** | Email editor opens successfully | Selected count = 80 |
| 2 | Observe candidate count and generated recipient list | Candidate count = 80; recipient list contains all 80 unique email addresses | Expected recipient count = 80 |
| 3 | Confirm send | Email send is accepted, or any platform-limit warning is shown before send; no recipient is silently dropped | "" |
| 4 | Verify dispatch result or log | Dispatch/log result contains all selected recipients, or clearly reports any blocked recipients with reason | 80 unique teacher Contacts |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Bulk Send – Non-SF-account recipients exceed 5,000 emails/day – Limit handled visibly

**Description:** AC 03.2, BR-22 — Negative / Boundary Value Analysis — If the implementation uses a 5,000 emails/day limit for non-SF-account recipients, exceeding that limit must be handled visibly and must not silently drop recipients.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Non-SF-account recipient email quota is configured as 5,000 emails/day
- The org has already sent 4,980 non-SF-account recipient emails today
- Add Teacher popup is open with 30 non-SF-account teacher candidates selected

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click **Send Email** | Email editor opens and shows selected count = 30 | Daily sent count = 4,980; selected non-SF recipients = 30 |
| 2 | Confirm send | System blocks send before exceeding daily limit OR sends allowed recipients and clearly reports blocked recipients, according to implementation design | Effective daily limit = 5,000 |
| 3 | Verify user feedback | User sees a clear warning/error explaining the daily email limit; no recipient is silently omitted | Expected remaining capacity = 20 |
| 4 | Verify logs | Dispatch/log result records sent and blocked recipients accurately | 20 sent, 10 blocked OR full send blocked |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Bulk Send – SF-account recipients – No 5,000 daily receiver cap applied

**Description:** AC 03.2, BR-22 — Regression — SF-account teacher recipients are not blocked by the non-SF-account 5,000 emails/day receiver limit.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher candidates are Salesforce-account recipients with valid email addresses
- Non-SF-account daily email count is at or near 5,000
- Add Teacher popup is open with selected SF-account teacher recipients

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click **Send Email** | Email editor opens successfully | Recipient type = SF account |
| 2 | Confirm send | Send action is accepted for SF-account recipients; no non-SF daily-limit error is shown | Non-SF daily count >= 5,000 |
| 3 | Verify dispatch result or log | All selected SF-account recipients are included in dispatch/log result | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Bulk Send – Rapid re-click of Send button – Email dispatched only once

**Description:** AC 03.2, BR-15 — CRUD (Idempotency) — Clicking the send/confirm button multiple times in rapid succession results in the email being dispatched exactly once; no duplicate emails are sent.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- 2 teachers selected in Add Teacher popup; email editor is open with body text entered

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In the email editor, enter a body message | Body text is entered | Email body = "代講のお願いです。" |
| 2 | Click the send/confirm button twice in rapid succession (double-click) | The system accepts the first click; the second click is ignored or the button becomes disabled after the first click | "" |
| 3 | Verify the number of emails dispatched to each recipient | Each selected teacher receives exactly **1** email; no duplicate email is received | Selected count = 2 teachers |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Recipient Privacy – Multiple candidates selected – Each candidate cannot see other recipients' email addresses

**Description:** AC 03.2, BR-19 — CRUD — When bulk email is sent to multiple teacher candidates, each email is sent separately or via BCC so that no candidate can see other candidates' email addresses.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher A (teacher-a@example.com), Teacher B (teacher-b@example.com), Teacher C (teacher-c@example.com) are selected
- Email has been sent via the email editor

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Select 3 teachers, compose email, and confirm send | Email dispatch is processed | Teacher A: teacher-a@example.com; Teacher B: teacher-b@example.com; Teacher C: teacher-c@example.com |
| 2 | Review the email received by Teacher A (or review the system-generated dispatch method) | Teacher A's email shows only their own address in the To or BCC field; Teacher B's and Teacher C's addresses are **not visible** in To or CC | "" |
| 3 | Review the email received by Teacher B | Teacher B's email shows only their own address; Teacher A's and Teacher C's addresses are **not visible** | "" |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Recipient List – System-generated list – Contains all selected teachers' email addresses

**Description:** AC 03.2, BR-18 — Regression — The system correctly generates the recipient list from the selected candidates; the list is complete and accurate before being handed to the company email tool.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher A, Teacher B, Teacher C are selected (each has a valid email address on their Contact or Salesforce User record)
- Email editor is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | With 3 teachers selected, observe the email editor | Email editor shows candidate count = 3 | Teacher A, B, C each have valid email addresses |
| 2 | Click send/confirm | System generates the recipient list | "" |
| 3 | Review the generated recipient list | The list contains exactly 3 entries: one email address per selected teacher; no entries are missing or duplicated | Teacher A: teacher-a@example.com; Teacher B: teacher-b@example.com; Teacher C: teacher-c@example.com |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Email Log – Sent email attached to each selected teacher Contact

**Description:** AC 03.2, BR-21 — CRUD — After sending candidate emails, an email log/activity is attached to each selected teacher's Contact record so staff can verify send history.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher A and Teacher B are selected as substitute candidates
- Email editor is open with default subject/title `代講をお願いいたします` and body template filled in

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Confirm send in the email editor | Emails are dispatched or queued for Teacher A and Teacher B | Teacher A Contact; Teacher B Contact |
| 2 | Open Teacher A's Contact record | Contact detail opens | "" |
| 3 | Check Activity / Email log on Teacher A Contact | A sent-email log exists for this substitute-teacher offer email | Subject/title = "代講をお願いいたします"; body contains "案件名：" and "時間：" |
| 4 | Open Teacher B's Contact record | Contact detail opens | "" |
| 5 | Check Activity / Email log on Teacher B Contact | A separate sent-email log exists for Teacher B | Timestamp/user/lesson reference match the send action |

**Severity:** critical
**Priority:** high

---

### [EN] Substitute Teacher – Email Log – Unselected teacher Contact has no email log

**Description:** AC 03.2, BR-21 — Negative — Only selected candidates receive email logs. Teachers visible in the candidate list but not selected must not get a substitute-offer email log.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- Teacher A and Teacher B are selected; Teacher C is visible but unselected
- Email editor is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Confirm send in the email editor | Emails are dispatched or queued for selected teachers only | Selected = Teacher A, Teacher B; Unselected = Teacher C |
| 2 | Open Teacher C's Contact record | Contact detail opens | "" |
| 3 | Check Activity / Email log on Teacher C Contact | No new substitute-offer email log is created for Teacher C | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Localization – Popup and email labels follow PRD translations

**Description:** AC 02.1, AC 03.1, AC 03.2, BR-14, BR-17 — Component — UI labels and messages follow the PRD localization table and email template text.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- JP locale or bilingual display is active
- Add Teacher popup and Email editor can be opened

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Detail and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Observe filter labels and teacher list column | Labels match PRD translations: Subject / 科目; Working Hour / 勤務可能時間; Commutable day of week / 勤務可能曜日; Flagged teacher / 要注意講師; Flagged / 要注意講師 | PRD version = 14 |
| 3 | Click **Send Email** with 0 selected teachers | Error message follows PRD translation | EN = "Please select one or more Teachers."; JP = "1人以上の講師を選択してください" |
| 4 | Select one teacher and click **Send Email** | Email editor opens | "" |
| 5 | Observe Send Email label and email template text | Button label = Send Email / メールを送信する; subject/title = 代講をお願いいたします; body contains 案件名： and 時間： | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Post-Send – Email sent outside Manabie – Lesson teacher assignment unchanged in Lesson Detail

**Description:** AC 03.2, BR-20 — Smoke — After the email send action, the Lesson Detail teacher assignment is not automatically changed; the substitute teacher must be manually assigned after the staff finalizes their choice through out-of-system negotiation.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- A lesson with no teacher assigned exists on Lesson Detail
- Email has been sent to substitute teacher candidates via the Add Teacher popup

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Complete the email send flow for the target lesson | Email is dispatched to selected candidates | "" |
| 2 | Close the email editor and Add Teacher popup | Popups close; Lesson Detail is displayed | "" |
| 3 | Observe the Lesson Teacher section on Lesson Detail | The lesson's teacher assignment is **unchanged** from before the email was sent; no teacher has been auto-assigned | "" |

**Severity:** trivial
**Priority:** low

---
