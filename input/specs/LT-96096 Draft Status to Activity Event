ID: https://manabie.atlassian.net/browse/LT-96096
Epic: https://manabie.atlassian.net/browse/LT-93068
Parent Epic: https://manabie.atlassian.net/browse/PBT-2218
Design: https://www.figma.com/design/qmHa3rUESxPnfenYsKXbtv/-Eng--Event-Management?node-id=7359-5959

## Summary

Add a new "Draft" status to Activity Event in Salesforce. When creating a new Activity Event, users can select either "Draft" or "Published" (default = Published). Draft events support field validation, participant management, and CRUD operations (Edit, Delete, Duplicate). Status transitions are restricted: Draft → Published and Draft → Cancel are allowed, but Draft → Completed is blocked with an error message. Draft events must not appear in the Learner app (Calendar or Booking system). A flag control function gates the feature.

## Acceptance Criteria

### US01 — Activity Event Status Picklist
- AC 01.1: A new "Draft" picklist value is added to the Activity Event Status field (creation form shows only Draft and Published — no Completed option on create).
- AC 01.2: When creating a new Activity Event, user can select either "Draft" or "Published".
- AC 01.3: Default Status on a new Activity Event is "Published" (same as current behavior).

### US02 — Draft Event – Field Validation & Operations
- AC 02.1: Draft events must validate mandatory fields (same validation rules as Published).
- AC 02.2: Draft events allow adding/removing participants.
- AC 02.3: Draft events allow Delete operation.
- AC 02.4: Draft events allow Edit operation.
- AC 02.5: Draft events allow Duplication operation.

### US03 — Status Transitions
- AC 03.1: Draft → Published: Allowed.
- AC 03.2: Draft → Completed: NOT allowed. Error message displayed:
  - EN: "You cannot mark a Draft event to Complete. Please Publish first."
  - JP: 下書きのイベントを完了にすることはできません。イベントを公開してください。
- AC 03.3: Draft → Cancel: Allowed.

### US04 — Learner App Visibility
- AC 04.1: Draft events are NOT shown in the Learner app Calendar.
- AC 04.2: Draft events are NOT shown in the Learner app Booking system.

### US05 — Flag Control
- AC 05.1: The Draft Status feature is controlled by a feature flag (LT-96627).

## Business Rules (Extracted)

| #  | AC      | Business Rule                                                              |
|----|---------|---------------------------------------------------------------------------|
| 1  | AC 01.1 | "Draft" picklist value exists in Activity Event Status field               |
| 2  | AC 01.2 | Create Activity Event form shows Draft and Published as status options     |
| 3  | AC 01.3 | Default status on new Activity Event = Published                           |
| 4  | AC 02.1 | Draft events enforce the same mandatory field validation as Published      |
| 5  | AC 02.2 | Participants can be added/removed on a Draft event                         |
| 6  | AC 02.3 | Draft events can be deleted                                                |
| 7  | AC 02.4 | Draft events can be edited                                                 |
| 8  | AC 02.5 | Draft events can be duplicated                                             |
| 9  | AC 03.1 | Status transition Draft → Published is allowed                             |
| 10 | AC 03.2 | Status transition Draft → Completed is blocked with error message          |
| 11 | AC 03.3 | Status transition Draft → Cancel is allowed                                |
| 12 | AC 04.1 | Draft events do not appear in Learner app Calendar                         |
| 13 | AC 04.2 | Draft events do not appear in Learner app Booking system                   |
| 14 | AC 05.1 | Feature is gated by a feature flag                                         |

## Clarification Questions

1. Can a Published event be transitioned back to Draft? (Not mentioned in requirements — assumed NO)
2. Can a Cancelled event be transitioned to Draft? (Assumed NO)
3. Does the Draft event appear on the SF Calendar view for staff, or only in the list view?
4. When the feature flag is OFF, does the Draft option simply not appear in the picklist, or is the entire status transition logic also disabled?
5. Are there any tenant-specific differences between Koyu and Renseikai for Draft behavior?
6. Does duplicating a Draft event create another Draft, or does the duplicate default to Published?
7. Is there a visual indicator (badge/tag/color) to distinguish Draft events from Published events in the list view?
8. When Draft → Cancel, does the system still send cancellation notifications (if configured on Event Master)?

## Related Specs

- None found in workspace.

## Related Test Cases

- `3-testcases/lesson-management/event/` — existing event test cases (cancel-booked-event, create event master)
- Qase PX suite 19: 1 existing case (PX-13261 "Verify event data migration on UI")

## QASE Coverage Gaps

- All 14 business rules above need new test cases (no existing coverage for Draft Status feature).

## Child Tickets (Implementation)

| Key       | Summary                                                       | Status |
|-----------|---------------------------------------------------------------|--------|
| LT-93069  | [SF] Create new picklist value Draft to Activity Event Status | Done   |
| LT-93070  | [SF] Modify formActivityEvent UI                              | Done   |
| LT-93071  | [SF] Modify API handle create/edit Activity Event             | Done   |
| LT-93072  | [SF] Modify validation logic when changing Activity Event Status | Done |
| LT-93073  | [SF] Update API to filter do not show Draft status of Activity Event | Done |
| LT-96627  | [SF] Create flag control function                             | Done   |
