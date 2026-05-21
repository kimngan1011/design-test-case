# LT-96662: [Renseikai] Core | Receive notifications when a new lesson is published (individually)

**ID:** https://manabie.atlassian.net/browse/LT-96662
**Status:** Ready for QA
**PRD:** https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2318663681 — [SF] [Mobile] Receive notifications when a new lesson is published (individually)
**Related ticket (similar flow):** https://manabie.atlassian.net/browse/LT-75180

---

## Summary

Renseikai occasionally publishes additional or temporary lessons after their regular bulk publishing. To ensure students and parents are aware of these new lessons, a new "Publish and notify student" button is added to the SF Lesson Detail page. When triggered, the system publishes the lesson (if Draft) and sends a push notification to the assigned student and all their associated parents via the Learner/Parent App. The feature is controlled by a custom permission **"Publish Lesson With Notification"** which is added to the Renseikai OOP Permission Set (PS) on the first release. Other partners are not granted this permission by default; additional partners may be considered in the future.

---

## Acceptance Criteria

### US 01 — Button to trigger sending of publish notification (AC 01.1 🟡)

**Feature:** Button to trigger sending of publish notification

- Add a button **"Publish and notify student"** to the SF Lesson Detail page
- Show only for **"Draft"** and **"Published"** status
- Hide for other statuses

---

### US 02 — Send notifications to student/parent

#### AC 02.1 🟡 — Send notifications to student/parent

**Trigger:** "Publish and notify student" is clicked

**System Action:**

- If lesson is **"Draft"**:
  - Marks the lesson as Published. Apply core lesson publishing rules.
  - Shows the send notification popup (see AC 02.2)
- If lesson is **"Published"**:
  - No change in status
  - Shows the send notification popup (see AC 02.2)

**Identify Notification Recipients:**

- **For Students:** Retrieve the Contact (Student) assigned to the lesson
- **For Parents:** Retrieve the Contact (Parent) who has a Relationship with the Student (all parents)

**Send Notifications:**

- The system combines the identified Parent & Student Contacts and the updated Lesson details to send a notification via the Learner/Parent App
- Notification content must clearly indicate lesson name and schedule
- Notifications sent in real-time upon lesson publish

**Notification content:**

- **Title:** Lesson Published
- **Content:**
  > The schedule for [Lesson Name] has been published.
  > Lesson Date: [date] | [start time - end time]
  > Tap the button below to view the lesson details.

#### AC 02.2 🟡 — Notification Confirmation Modal

**Modal Content and Options:**

- Message: "Would you like to send notifications about the publishing lesson to all allocated students?"
- Two options:
  - **Send** — triggers the notification flow as in AC 02.1; sends formatted notification to Student & Parent App
  - **Don't Send** — does not trigger the notification flow; no notifications sent

#### AC 02.3 🟡 — Retry mechanism for sending notifications

- **Retry on Failure:** If system fails to send notification, automatically retry up to **3 times**
- **Retry Interval:** Short delay between each attempt
- **Stop condition:** notification sent successfully OR 3 attempts exhausted
- **Logging:** Every attempt (success or failure) must be logged for monitoring and audit
- **Failure logging:** If all 3 attempts fail, log clearly (error log or admin dashboard)
- **No Duplicates:** Retry mechanism must ensure only one successful notification delivered even if multiple attempts are made

---

### US 03 — Navigate to lesson detail from notification

#### AC 03.1 🟡 — Navigate to lesson detail page from Notifications message

- Given student/parent has received notifications about a new lesson
- When student/parent opens the notification message
- And student/parent taps to view lesson details
- Then student/parent is able to navigate to the **Lesson Detail page** of the published lesson
- And user is able to view lesson detail with newly updated info

---

## JP Translation

| Location             | EN                                                                                                                                                  | JP                                                                                                                              |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Header button        | Publish and notify student                                                                                                                          | 公開して生徒にお知らせを送る                                                                                                    |
| Notification title   | Lesson Published                                                                                                                                    | 授業公開のおしらせ                                                                                                              |
| Notification content | The schedule for [Lesson Name] has been published. Lesson Date: [date] \| [start time - end time]. Tap the button below to view the lesson details. | [Lesson Name] の授業が公開されました。授業日: [date] \| [start time - end time]. 授業詳細を見るにはボタンをタップしてください。 |
| Modal title          | Send Notification                                                                                                                                   | おしらせ配信                                                                                                                    |
| Modal message        | Would you like to send notifications about the publishing lesson to all allocated students?                                                         | 授業に参加する生徒へ授業公開のおしらせを配信しますか？                                                                          |
| Send                 | Send                                                                                                                                                | 今すぐ送る                                                                                                                      |
| Don't Send           | Don't Send                                                                                                                                          | 送らない                                                                                                                        |

---

## Out of Scope

- Bulk lesson publish from **SF Lesson List**, **SF Lesson Calendar**, or **BO** — does NOT trigger this notification

---

## Business Rules (Extracted)

| #   | AC      | Business Rule                                                                                                                                                   |
| --- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| 1   | AC 01.1 | "Publish and notify student" button added to SF Lesson Detail page                                                                                              |
| 2   | AC 01.1 | Button visible only when lesson status = Draft OR Published; hidden for all other statuses                                                                      |
| 3   | AC 02.1 | When clicked on Draft lesson: publishes lesson (core rules apply) + shows confirmation modal                                                                    |
| 4   | AC 02.1 | When clicked on Published lesson: no status change + shows confirmation modal                                                                                   |
| 5   | AC 02.2 | Confirmation modal: "Would you like to send notifications about the publishing lesson to all allocated students?" with Send / Don't Send options                |
| 6   | AC 02.1 | Notification recipients = student assigned to lesson + ALL parent contacts linked to that student via Relationship                                              |
| 7   | AC 02.1 | Notification title: "Lesson Published"                                                                                                                          |
| 8   | AC 02.1 | Notification body: lesson name + lesson date + start/end time + CTA to view details                                                                             |
| 9   | AC 02.1 | Notifications sent in real-time (not batched)                                                                                                                   |
| 10  | AC 02.3 | Retry on failure: up to 3 attempts with short delay between each                                                                                                |
| 11  | AC 02.3 | Idempotent delivery — no duplicate notifications on retry success                                                                                               |
| 12  | AC 02.3 | Every attempt logged (success and failure) for audit                                                                                                            |
| 13  | AC 02.3 | If all 3 attempts fail → failure logged clearly (error log / admin dashboard)                                                                                   |
| 14  | AC 03.1 | Notification deep-links to the specific Lesson Detail page                                                                                                      |
| 15  | PRD     | Button visibility is controlled by the custom permission **"Publish Lesson With Notification"** — users without this permission cannot see the button           |     |
| 17  | PRD     | Custom permission added to Renseikai OOP Permission Set (PS) on initial release; other partners do not receive it by default — future consideration per request |     |

About the switch student and switch account create more test cases to check when have multiple students under the same parent and when the parent have multiple accounts, how the notification work in those cases, please help me confirm the expected behavior with the product team and then create test cases to check those cases.

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| #   | Tag                 | Source                                                                                              | AC      | Description                                                                                                                                                                                                                                                                                               |
| --- | ------------------- | --------------------------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| 1   | `[REGRESSION RISK]` | `output/test-cases/lesson-management/lesson/lesson-status/lesson-status.md` — TC-1456, TC-9786–9791 | AC 02.1 | Existing TCs cover Draft→Published transition without a notification flow. The new "Publish and notify student" button is an alternative publish path from SF Lesson Detail. TCs asserting Draft→Published behaviour need to verify they cover both the existing publish action AND this new button path. | -> update existing test cases |

### Missing in Requirements

| #   | Tag                    | Source                                                 | Description                                                                                                                                                                                                                    |
| --- | ---------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| 2   | `[MISSING BEHAVIOR]`   | AC 01.1                                                | Button visibility for "other statuses" is not explicitly listed. Statuses (Completed, Cancelled) should be confirmed as hidden.                                                                                                |
| 3   | `[MISSING BEHAVIOR]`   | AC 02.1                                                | No AC covers the case where the student has **no associated parent** — should notification still be sent to student only, or is this an error case?                                                                            | -> create test case to check this case after that share the result to the product team and confirm the expected behavior |
| 4   | `[MISSING BEHAVIOR]`   | AC 02.1                                                | No AC covers behaviour when student or parent has **no device token** (never logged into app) — silent skip, error log, or warning to sender?                                                                                  | -> notification only send when user login to app                                                                         |
| 5   | `[MISSING BEHAVIOR]`   | AC 02.3                                                | Failure after 3 retries is logged — but no AC defines whether the **SF user** (who clicked the button) is notified about the delivery failure                                                                                  | -> skip                                                                                                                  |
| 6   | `[MISSING BEHAVIOR]`   | AC 02.2                                                | When lesson is Draft and user chooses "Don't Send" in modal — AC 02.1 says lesson is published first, then modal is shown. Does "Don't Send" still leave the lesson in Published status? This must be clarified.               | -> create test case to check this case after that share the result to the product team and confirm the expected behavior |
| 7   | `[UNDOCUMENTED IN AC]` | PRD (Out of Scope section)                             | Bulk lesson publish paths (SF List, Calendar, BO) do NOT trigger notifications. This boundary is absent from the AC text.                                                                                                      | -> skip                                                                                                                  |
| 8   | `[ROLE GAP]`           | AC 01.1                                                | Button visibility is controlled by the custom permission **"Publish Lesson With Notification"** in the OOP Permission Set. Only SF users included in the Renseikai OOP PS (holding this custom permission) can see the button. | ✅ Confirmed                                                                                                             |
| 9   | `[MISSING BEHAVIOR]`   | PRD (permission)                                       | When user does **not** have the custom permission "Publish Lesson With Notification", the button is **hidden** (not rendered).                                                                                                 | ✅ Confirmed: hidden                                                                                                     |
| 10  | `[MISSING BEHAVIOR]`   | PX-2026-04-13.json — Switch Student domain (Case 3931) | When a parent is viewing Student B in the app and taps a notification for Student A's lesson, no AC defines whether the app auto-switches to Student A's context or stays on Student B                                         | -> create test case to check this case after that share the result to the product team and confirm the expected behavior |
| 11  | `[MISSING BEHAVIOR]`   | AC 03.1                                                | Deep-link: if student/parent is **not logged in** when tapping the notification, no AC defines the redirect flow (login → lesson detail, or just app home)                                                                     | -> create test case to check this case after that share the result to the product team and confirm the expected behavior |

### Assumptions Made

- The "Publish and notify student" button uses the same notification infrastructure as LT-75180 (Published lesson date/time updated) — different trigger event, same delivery/retry mechanism. -> correct
- "All parents" means all Parent Contacts linked to the student via Relationship records (parent-student type), consistent with the relationship domain knowledge. -> correct
- The custom permission "Publish Lesson With Notification" controls button visibility — users without this permission cannot see the button (not rendered).
- "Other statuses" where button is hidden includes at minimum: Completed, Cancelled. -> correct

---

## Clarification Questions

---

## Related Specs

- `input/specs/` — no existing spec for lesson notification feature

## Related Test Cases

- `output/test-cases/lesson-management/lesson/lesson-status/lesson-status.md` — existing lesson status change TCs (TC-1456, TC-9786–9791): Draft→Published flow may be impacted by new button path [REGRESSION RISK]

## QASE Coverage Gaps

- AC 01.1 — No existing test cases for "Publish and notify student" button visibility logic per status
- AC 02.1 — No existing test cases for notification trigger flow (Draft path, Published path)
- AC 02.2 — No existing test cases for confirmation modal (Send / Don't Send scenarios)
- AC 02.3 — No existing test cases for retry mechanism and duplicate prevention
- AC 03.1 — No existing test cases for notification deep-link to lesson detail
- PRD (Custom Permission) — No existing test cases for "Publish Lesson With Notification" permission-based button visibility (with permission / without permission)
