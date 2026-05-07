# LT-96152: Add Collect Attendance Menu in Lesson Report tab/page (BO)

**ID:** https://manabie.atlassian.net/browse/LT-96152
**Status:** Ready for QA
**Analysis Date:** 2026-04-14

---

## Summary

LT-96152 improves the BO teacher workflow by exposing the existing Collect Attendance action directly on Lesson Detail -> Report tab and Lesson Report Detail. The feature is an entry-point extension, not a new attendance engine, so the main QA focus is parity with the current collect-attendance behavior already covered in Qase suite 326.

---

## Acceptance Criteria

Derived from the Epic description, the user clarification on 2026-04-14, and the current collect-attendance baseline in Qase suite 326.

- **US 01 — Expose collect attendance from lesson report surfaces**
  - **AC 01.1** Show Collect Attendance on BO Lesson Detail -> Report tab.
  - **AC 01.2** Show Collect Attendance on BO Lesson Report Detail.
  - **AC 01.3** Clicking either new entry point opens the existing Collect Attendance popup used by the current BO flow.
  - **AC 01.4** Availability and disabled state of the new entry points follow the existing collect attendance logic.
  - **AC 01.5** Saving attendance from the new entry points preserves the current update and sync behavior across BO, lesson allocation, and Mobile.

---

## Business Rules (Extracted)

| #   | AC      | Business Rule                                                                                                                                         | Field                             | Field Behavior | Platform             |
| --- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- | -------------- | -------------------- |
| 1   | AC 01.1 | Collect Attendance action is shown on BO Lesson Detail -> Report tab.                                                                                 | Collect Attendance action         | visible        | [BO]                 |
| 2   | AC 01.2 | Collect Attendance action is shown on BO Lesson Report Detail.                                                                                        | Collect Attendance action         | visible        | [BO]                 |
| 3   | AC 01.3 | Clicking either new surface opens the existing collect attendance popup.                                                                              | Collect Attendance popup          | editable       | [BO]                 |
| 4   | AC 01.4 | Draft and Completed lessons remain unavailable for update on the new surfaces, consistent with the current flow.                                      | Collect Attendance action         | disabled       | [BO]                 |
| 5   | AC 01.4 | Attendance-eligible lessons keep the new entry points enabled.                                                                                        | Collect Attendance action         | editable       | [BO]                 |
| 6   | AC 01.5 | Saving from Report tab updates BO lesson detail student session data with the same status, reason, notice, and note as the current flow.              | Attendance data                   | editable       | [BO], [SF]           |
| 7   | AC 01.5 | Saving from Lesson Report Detail updates lesson allocation/report history and Mobile-facing attendance data with the same values as the current flow. | Attendance data                   | editable       | [BO], [SF], [Mobile] |
| 8   | AC 01.5 | Previously saved reason, notice, and note remain visible when the popup is reopened from the new entry points.                                        | Attendance Reason / Notice / Note | editable       | [BO]                 |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| #   | Tag               | Source                                                                                         | AC                          | Description                                                                                                                               |
| --- | ----------------- | ---------------------------------------------------------------------------------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [EXTENDED]        | Qase PX suite 326                                                                              | AC 01.1 / AC 01.2 / AC 01.3 | The feature extends the current BO collect-attendance workflow to two additional report surfaces rather than replacing the existing flow. |
| 2   | [REGRESSION RISK] | Qase PX suite 326 — User updates the attendance info                                           | AC 01.5                     | Save from the new entry points must hit the same update/sync pipeline or BO, lesson allocation, and Mobile values can diverge.            |
| 3   | [REGRESSION RISK] | Qase PX suite 326 — User cannot update attendance info                                         | AC 01.4                     | Draft and Completed lessons are currently unavailable for update; the new buttons must not bypass that guard.                             |
| 4   | [REGRESSION RISK] | Qase PX suite 326 — remark persistence and JP label cases                                      | AC 01.3 / AC 01.5           | The popup opened from the new surfaces must preserve existing prefill, remark persistence, and localization behavior.                     |
| 5   | [EXTENDED]        | output/test-cases/lesson-management/student-session/lesson-allocation/la-system-integration.md | AC 01.2                     | Lesson Report Detail already reflects attendance data; LT-96152 adds direct attendance actioning from that surface.                       |

### Missing in Requirements

| #    | Tag | Source | Description                                                                                                                                     |
| ---- | --- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| None | —   | —      | No open requirement gaps remain after the user clarified that the feature applies to both Lesson Detail -> Report tab and Lesson Report Detail. |

### Lesson-Learned Risks

| #    | Incident | Date | AC  | Risk                                                                | Guardrail                                                           |
| ---- | -------- | ---- | --- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| None | —        | —    | —   | No relevant historical incident matched this entry-point extension. | Keep parity checks focused on the existing collect-attendance flow. |

### E2E Scenario Impact

| Scenario | Title                                        | Impact                                                                                                          | Action |
| -------- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------ |
| E2E-17   | Renseikai — Attendance & Error Configuration | The BO collect attendance step should mention the additional report-tab and lesson-report-detail launch points. | UPDATE |

### Assumptions Made

- The new buttons reuse the existing collect-attendance popup and handler rather than a new attendance form.
- Existing disabled-state behavior from suite 326 applies to the new report surfaces as well.
- Visibility and permission follow the current collect-attendance permission model for BO users.

---

## Clarification Questions

None at this point. Scope was clarified on 2026-04-14: Collect Attendance must be shown in Lesson Detail -> Report tab and Lesson Report Detail.

---

## Related Specs

- No directly related local spec was found for this exact BO lesson-report entry-point change.

## Related Test Cases

- `Qase PX suite 326 — Collect Attendance on BO` — current collect-attendance logic baseline (status guards, save behavior, remark persistence, localization).
- `output/test-cases/lesson-management/student-session/lesson-allocation/la-system-integration.md` — attendance/report-history integration and lesson-report-detail accessibility.
- `output/test-cases/lesson-management/lesson-teacher/teacher-view-lesson-different-location.md` — placeholder report-surface collect-attendance scenarios that are impacted by the new entry points.

## QASE Coverage Gaps

- AC 01.1 — No existing case verifies Collect Attendance on Lesson Detail -> Report tab.
- AC 01.2 — No existing case verifies Collect Attendance on Lesson Report Detail.
- AC 01.4 — No existing case verifies disabled-state parity from the new report surfaces.
- AC 01.5 — No existing case verifies that saves from the new report surfaces preserve BO, lesson allocation, and Mobile sync behavior.
