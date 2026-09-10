# Test Coverage: LT-107665 - Learner App Calendar Empty-State Messages

## Coverage Matrix

| Coverage ID | AC / Rule | Scenario | Technique | Risk | Depth |
|---|---|---|---|---|---|
| ES-01 | AC-01, BR-01, BR-02, BR-06 | All tab has no Lesson or Event for selected date; validate English then Japanese text. | State / localization | High | Deep |
| ES-02 | AC-02, BR-01, BR-03, BR-06 | Lesson tab is empty while an Event exists on the same date; validate English then Japanese text. | Decision table / negative | Critical | Deep |
| ES-03 | AC-03, BR-01, BR-04, BR-06 | Event tab is empty while a Lesson exists on the same date; validate English then Japanese text. | Decision table / negative | Critical | Deep |

## Existing Testcases Impacted

| Existing case | Why impacted | Required action |
|---|---|---|
| No directly matching existing Qase testcase was located by title search for `no lesson`, `no event`, or `empty`. | The new copy is not covered as an explicit regression assertion. | Add the three dedicated cases below; no existing case text should be overwritten. |
| PX-26150 - Learner App Calendar: Draft Activity Event remains hidden | It opens Learner App Calendar, but asserts item invisibility rather than the empty-state message. | Regression only; keep unchanged. |
| PX-26009 - Learner App Calendar: Student sees event dot on every spanned day | Uses Learner App Calendar event rendering, not an empty calendar state. | Regression only; keep unchanged. |
| Existing Learner App Calendar lesson-note/timeslot cases under LT-98529 | Use populated Lesson cards/detail and do not assert empty state. | Regression only; keep unchanged. |

## Automation Notes

- Use stable test data for a future date and a learner account scoped to the records in each case.
- Assert the exact localized string, including the final punctuation.
- Verify the counterpart item exists before switching tab in ES-02 and ES-03; this proves the message is tab-scoped rather than a generic no-data response.
