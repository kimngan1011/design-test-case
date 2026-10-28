# Test Cases: LT-112926 — Notification language is org-configured

## Suite: Lesson communications — language configuration

### LANG-001 — Bulk publish — teacher email follows org language, not publishing Admin

**Preconditions:** T1 is an eligible lesson teacher with a working mailbox. Two Draft lessons for T1 span 2026-11-03 through 2026-11-05. Admin EN and Admin JA can bulk publish them.

| # | Action | Expected Result |
|---:|---|---|
| 1 | Set `Notification_Language__c = ja`; sign in as Admin EN and bulk publish the first unique batch. | T1 receives one email for the batch. Subject is `授業予定が公開されました`; body uses the Japanese template and period `2026年11月3日～2026年11月5日`. |
| 2 | Set `Notification_Language__c = en_US`; sign in as Admin JA and bulk publish a second unique batch with the same date range. | T1 receives one email for the second batch. Subject is `Lesson Schedule Published`; body uses the English template and period `November 3, 2026 ~ November 5, 2026`. |
| 3 | Compare deliveries and lesson status. | Both batches are Published; exactly one email per teacher per action. Only localized copy/date format changes. |

**Priority:** high
**Severity:** critical

### LANG-002 — Bulk publish — teacher Chatter is intentionally suppressed

**Preconditions:** T1 is an Available assigned teacher on one Draft lesson in each unique bulk batch.

| # | Action | Expected Result |
|---:|---|---|
| 1 | Set config to `ja`; Admin EN bulk publishes batch A. | Batch A lessons are Published and teacher email is sent, but no new teacher-publish Chatter post is created. |
| 2 | Set config to `en_US`; Admin JA bulk publishes batch B. | Batch B lessons are Published and teacher email is sent, but no new teacher-publish Chatter post is created. |
| 3 | Compare each lesson's Chatter feed before and after bulk publish. | No teacher @mention/Chatter notification is created in either language partition. This suppression is independent of language configuration. |

**Priority:** high
**Severity:** major

### LANG-003 — Single publish — student/parent push follows org language

**Preconditions:** S1 has an active allocation in each Draft lesson, P1 is S1's default parent, and both push inboxes are available.

| # | Action | Expected Result |
|---:|---|---|
| 1 | Set config to `ja`; Admin EN publishes lesson A and elects to send notifications. | Eligible recipients receive the Japanese values of `Lesson_Published_Notification_Title` and `Lesson_Published_Notification_Content`, including lesson name and `yyyy-MM-dd | HH:mm - HH:mm`. Custom data is `lesson_published` for lesson A. |
| 2 | Set config to `en_US`; Admin JA publishes lesson B and elects to send notifications. | Eligible recipients receive the English values of the same labels and the same date-time/data shape for lesson B. |
| 3 | Open each delivered notification. | Each opens the corresponding lesson; Admin language has not determined either payload. |

**Priority:** high
**Severity:** critical

### LANG-004 — Single publish — teacher Chatter follows org language

**Preconditions:** T1 is an Available assigned teacher on each Draft lesson; T1 has an active Salesforce user.

| # | Action | Expected Result |
|---:|---|---|
| 1 | Set config to `ja`; Admin EN publishes lesson A. | The new post mentions T1 and uses the Japanese teacher-publish template: `が公開されました。詳細はこちらをクリックしてください。` |
| 2 | Set config to `en_US`; Admin JA publishes lesson B. | The new post mentions T1 and uses the English teacher-publish template: `has been published. Click to see more details.` |
| 3 | Check T1's Salesforce notification center. | T1 receives the normal @mention notification for each post; it is not duplicated and the lesson hyperlink remains valid. |

**Priority:** high
**Severity:** major

### LANG-005 — Send lesson report — push to student and default parent follows org language

**Preconditions:** A report for `Math 1` is eligible for notification for S1; P1 is S1's default parent.

| # | Action | Expected Result |
|---:|---|---|
| 1 | Set config to `ja`; Admin EN triggers the report notification. | S1 and P1 receive title `指導簿が公開されました` and body `Math 1の指導簿が公開されました。` |
| 2 | Set config to `en_US`; Admin JA triggers a second eligible report notification. | S1 and P1 receive title `Lesson Report ready!` and body `Lesson report for Math 1 is now available.` |
| 3 | Open each push. | Recipient set and report deep link are unchanged by language configuration. |

**Priority:** high
**Severity:** major

### LANG-006 — Lesson time changed — push follows org language

**Preconditions:** A Published lesson has S1 actively allocated and is eligible for time-change notification.

| # | Action | Expected Result |
|---:|---|---|
| 1 | Set config to `ja`; Admin EN changes lesson A from `2026-11-10 | 09:00 - 10:00` to `2026-11-10 | 11:00 - 12:00` and sends notification. | S1 receives Japanese `Lesson_Update_Time_Notice_Title` and content containing lesson name plus both the old and new 24-hour date-time values. Custom data type is `lesson_time_updated`. |
| 2 | Set config to `en_US`; Admin JA makes the same type of change on lesson B and sends notification. | S1 receives English values of the same labels with correct old/new date-times and `lesson_time_updated` data. |
| 3 | Open the notifications. | Each targets its changed lesson; no extra/missing recipient is introduced by changing configuration language. |

**Priority:** high
**Severity:** critical

### LANG-007 — Submit attendance — default-parent push follows org language

**Preconditions:** S1 is allocated to `Science 1`, P1 is S1's default parent, and an attendance response can be submitted for that student session.

| # | Action | Expected Result |
|---:|---|---|
| 1 | Set config to `ja`; Admin EN submits or changes the attendance response. | P1 receives title `出欠状況` and body `{S1}さんが{Science 1}への出欠連絡を送信しました。` with names substituted. |
| 2 | Set config to `en_US`; Admin JA submits/changes the response for a separate student session. | P1 receives the English `Attendance_Response` title and English `Attendance_Response_Submitted_Notification` body with names substituted. |
| 3 | Inspect the parent inbox/deep link. | The notification has the expected attendance-response destination/data; Admin profile language does not alter copy. |

**Priority:** high
**Severity:** major

### LANG-008 — Bulk publish — student/parent push must be Japanese with JP configuration

**Preconditions:** S1/P1 are eligible notification recipients for a unique Draft bulk-publish batch; their push inboxes are available.

| # | Action | Expected Result |
|---:|---|---|
| 1 | Set config to `ja`; Admin EN bulk publishes the batch. | S1/P1 receive a bulk-publish push whose title and body are the Japanese translations of `notification_bulk_publish_lesson_title` and `notification_bulk_publish_lesson_content`; the date range is Japanese-formatted. |
| 2 | Set config to `en_US`; Admin JA bulk publishes a separate batch. | S1/P1 receive the English values for the same labels and an English-formatted date range. |
| 3 | Record the JP result against the deployed label metadata. | If step 1 displays English, fail the case: the source requests Japanese but the Japanese translations are absent in the reviewed metadata. Do not accept English as the JP expected result. |

**Priority:** highest
**Severity:** critical

### LANG-009 — Nichibei booking cancellation — Chatter follows org language

**Preconditions:** For a Nichibei bookable lesson, S1 has a valid booking and CM1 resolves for the lesson location/brand. CM1's Salesforce language is the opposite of the config in each partition.

| # | Action | Expected Result |
|---:|---|---|
| 1 | Set config to `ja`; have S1 self-cancel booking through the app. | One Chatter post on the lesson uses `<Student> が <Lesson> をキャンセルしました。`, has valid student/lesson links, and mentions resolved CM1. |
| 2 | Set config to `en_US`; self-cancel a separate booking while CM1's UI remains Japanese. | One Chatter post uses `<Student> has cancelled booking of <Lesson>`, with the same links and CM mention behavior. |
| 3 | Compare recipient resolution. | Language changes only post template; cancellation, Chatter relation, and CM resolution are unaffected. |

**Priority:** high
**Severity:** major

### LANG-010 — Blank and unsupported language settings fall back to Japanese

**Preconditions:** Representative test records exist for a bulk-publish teacher email, a published-lesson time-change push, and a Nichibei booking cancellation post. The executing Admin uses English.

| # | Action | Expected Result |
|---:|---|---|
| 1 | Set config blank; trigger the three representative actions on separate records. | Email, push, and Chatter payloads use their Japanese templates. |
| 2 | Set config to unsupported `fr_FR`; trigger fresh equivalent actions. | Email, push, and Chatter payloads again use Japanese templates. |
| 3 | Set config to `jp_JP`; trigger one representative action. | Payload is Japanese, proving supported Japanese variants normalize to `ja`. |

**Priority:** high
**Severity:** critical
