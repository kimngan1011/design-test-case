# Test Cases: LT-111303 - Static Student Panel Divider on Lesson Calendar

## TC-01 - Lesson Calendar divider - Dragging blue divider does not resize panels

Verify the reported bug directly: the blue vertical divider is a static border and cannot resize the Student or Calendar panels.

## TC-02 - Lesson Calendar divider - Pointer/touch drag on divider has no resize side effects

Verify drag robustness across pointer interaction styles and directions.

## TC-03 - Lesson Calendar divider - Arrow toggle remains the only collapse/expand control

Verify the existing white-column arrow control still collapses and expands the Student panel.

## TC-04 - Lesson Calendar divider - Calendar view, filters, and detail drawer remain stable

Verify no regression in common Lesson Calendar workflows after attempted divider drag.

## TC-05 - Lesson Calendar divider - Layout remains aligned after browser resize and zoom

Verify the static divider stays aligned and does not introduce overflow/overlap on common desktop layouts.
