# Test Coverage: LT-112926 — Japanese default notification language

## Common test data

- **Admin EN:** Salesforce language English. **Admin JA:** Salesforce language Japanese. Both can trigger the relevant action.
- **Teacher T1:** Available lesson teacher with an active Salesforce user and mailbox. **CM1:** resolved Nichibei Centre Manager with an active Salesforce user.
- **Student S1 / Parent P1:** active allocated student and S1's default parent; both have app push enabled.
- Use a unique lesson/report per execution and wait for async delivery before asserting. A payload is asserted in the recipient's email, push inbox, or Chatter feed—not from the sender's UI language.

| ID | Flow | Channel / recipient | Japanese default (Admin EN) | English override (Admin JA) | Risk |
|---|---|---|---|---|---|
| LANG-001 | Bulk publish | Teacher email | JP subject/body and JP period format | EN subject/body and EN period format | Critical |
| LANG-002 | Bulk publish | Teacher Chatter | No post (intentionally bypassed) | No post (intentionally bypassed) | High |
| LANG-003 | Publish lesson | Student/parent push | JP labels and 24-hour date-time | EN labels; same data/deep link | Critical |
| LANG-004 | Publish lesson | Teacher Chatter | Japanese publish template | English publish template | High |
| LANG-005 | Send lesson report | Student + default parent push | JP title/body with lesson name | EN title/body with lesson name | High |
| LANG-006 | Lesson time changed | Active allocated student push | JP title/body, old and new 24-hour date-times | EN title/body, old and new 24-hour date-times | Critical |
| LANG-007 | Submit attendance | Default parent push | JP title/body with student and lesson names | EN title/body with student and lesson names | High |
| LANG-008 | Bulk publish | Student/parent push regression | JP title/body expected; currently blocked by missing translations | EN title/body | Critical |
| LANG-009 | Nichibei cancellation booking | Chatter to resolved CM(s) | Japanese cancellation template | English cancellation template | High |
| LANG-010 | Shared fallback | Representative email, push, and Chatter | Blank/unsupported setting resolves to JP | N/A | Critical |

## Assertions that apply to every case

1. Change only `Notification_Language__c` between the JP and EN partitions; retain the same functional eligibility and recipient data.
2. The payload language follows the setting, even when the acting Admin has the opposite Salesforce profile language.
3. Recipient resolution, number of deliveries, Chatter mentions, links, and custom-data/deep-link type do not change because the language setting changes.
4. Run the JP and EN partitions with separate test records/actions so an existing delivery or Chatter post cannot satisfy the second assertion.

## Regression note

LANG-008 should be executed as a release gate. If JP configuration returns English text for the bulk-publish student/parent push, log it against the missing Japanese custom-label translations; do not change the expected result to English.
