# Test Coverage: LT-111303 - Static Student Panel Divider on Lesson Calendar

## Scope

Validate that the blue divider between the Student panel and Calendar panel on Salesforce Lesson Calendar is no longer draggable/resizable, while the existing arrow toggle remains the only supported collapse/expand control.

## Requirement Mapping

| ID | Requirement | Risk | Coverage |
|---|---|---|---|
| R1 | Divider drag does not resize Student panel or Calendar panel | Critical | TC-01, TC-02 |
| R2 | Divider is not exposed as a resize handle | High | TC-01 |
| R3 | Arrow toggle still collapses and expands Student panel | Critical | TC-03 |
| R4 | Daily/Weekly Calendar and lesson detail keep working after attempted drag | High | TC-04 |
| R5 | Layout remains stable after filter/search, right drawer, viewport resize, and zoom | High | TC-04, TC-05 |

## Test Design

| Case ID | Title | Technique | Depth | Priority |
|---|---|---|---|---|
| TC-01 | Lesson Calendar divider - Dragging blue divider does not resize panels | Bug Reproduction + Negative Testing | Deep | High |
| TC-02 | Lesson Calendar divider - Pointer/touch drag on divider has no resize side effects | Interaction Robustness | Medium | High |
| TC-03 | Lesson Calendar divider - Arrow toggle remains the only collapse/expand control | State Transition | Deep | High |
| TC-04 | Lesson Calendar divider - Calendar view, filters, and detail drawer remain stable | Regression | Deep | High |
| TC-05 | Lesson Calendar divider - Layout remains aligned after browser resize and zoom | Responsive Regression | Medium | Medium |

## Automation Notes

Recommended automation assertions:

- Capture bounding boxes for:
  - Student panel container.
  - Calendar panel/container.
  - Blue divider/white toggle column.
- Attempt pointer drag from divider center to the right and left.
- Assert Student panel width and Calendar panel left edge remain within 2 px of the original values.
- Click only the arrow toggle and assert Student panel collapses/expands.
- Run the core no-resize assertion in Daily view and Weekly view.

## Suggested Test Suite Structure

| Suite | Parent Suite | Purpose |
|---|---|---|
| Static Student Panel Divider on Lesson Calendar (LT-111303) | Calendar lesson | Core SF regression suite for Student panel divider and collapse behavior |
