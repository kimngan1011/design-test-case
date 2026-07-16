---
ticket_id: LT-94694
ticket_url: https://manabie.atlassian.net/browse/LT-94694
title: [koyu] Core | Booking Link to Event List page
module: scheduling
bucket: OOP/koyu
status: Done
internal_uat_date: null
production_release_date: null
last_updated: 2026-07-03
---

# LT-94694: [koyu] Core | Booking Link to Event List page

## Summary

This epic changes the external booking-link entry flow for Koyu so first-time users can browse Activity Events before authentication.
The booking link must land on Activity Event List, let users open Event Detail, and only require Login/Register when they tap Reserve.
The in-app logged-in booking flow remains unchanged.

---

## Acceptance Criteria

### US01 - Booking link entry behavior

| AC | Description |
|---|---|
| AC 01.1 | External booking link opens Activity Event List page as the first screen, not Login/Sign up. |
| AC 01.2 | User can open Activity Event Detail from Activity Event List without being forced to log in first. |
| AC 01.3 | User tapping Reserve from Activity Event Detail is redirected to Login/Register when unauthenticated. |
| AC 01.4 | After successful Login/Register from the booking-link flow, user continues booking flow (Booking verified screen and downstream process). |
| AC 01.5 | Existing in-app flow is unchanged: Login > Calendar > Booking system > Master Event > Activity Event List > Activity Event Detail > Reserve. |

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| 1 | AC 01.1 | Booking-link landing page is Activity Event List. | booking_link_entrypoint | route changed from auth page to event list page | [App] |
| 2 | AC 01.1 | First screen must not force authentication. | auth_gate | delayed until reserve action | [App] |
| 3 | AC 01.2 | Event list is browsable by unauthenticated users through booking link. | activity_event_list | readable without login | [App] |
| 4 | AC 01.2 | Event detail is browsable by unauthenticated users through booking link. | activity_event_detail | readable without login | [App] |
| 5 | AC 01.3 | Reserve action requires authentication. | reserve_button | redirects to Login/Register when user is not authenticated | [App] |
| 6 | AC 01.3 | Login redirect trigger is tied to Reserve action only. | login_trigger_point | no login prompt before reserve tap | [App] |
| 7 | AC 01.4 | Post-auth continuation returns user to booking flow context. | post_auth_redirect | continues to booking verified screen and normal process | [App] |
| 8 | AC 01.4 | Register path follows same continuation rule as login path. | register_redirect | returns to booking flow context after registration | [App] |
| 9 | AC 01.5 | Existing in-app booking path remains unchanged for logged-in users. | app_internal_flow | no behavior change | [App] |
| 10 | AC 01.5 | Direct navigation handling must not regress current event page behavior for existing users. | deep_link_handling | preserve existing behavior outside booking-link entry flow | [App] |

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [REPLACED] | booking-link legacy behavior | AC 01.1 | Prior behavior redirected first-time users to Login/Register as entry screen; this is replaced by Activity Event List first. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [MISSING BEHAVIOR] | LT-94694 description | Requirement does not define behavior for expired/invalid booking links when user is unauthenticated. |
| 2 | [MISSING BEHAVIOR] | LT-94694 description | Requirement does not define behavior after login failure or user cancel on Login/Register page. |
| 3 | [ROLE GAP] | AC 01.x | Requirement references user flow but does not separate student vs parent account behavior when both can reserve. |
| 4 | [UNDOCUMENTED IN AC] | Figma node 7593-44460 | Requirement does not explicitly list required fields on Activity Event List and Activity Event Detail that must remain visible pre-login. |
| 5 | [REGRESSION RISK] | LT-94697 child feature | Existing login-first/redirect logic might still execute for deep links, causing intermittent login-first regressions. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | OOP flow divergence from core without explicit guards caused partner-side regressions in production (Nichibei SPO sync lesson learned) | 2026-03-04 | AC 01.1-01.5 | Koyu-specific entry-flow change can accidentally reuse old core auth redirect middleware and reintroduce login-first behavior. | Add explicit regression coverage for both booking-link flow and existing in-app flow; verify redirect trigger point is Reserve only. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-EVT-BOOK-01 | External booking link end-to-end | Entry routing and auth trigger behavior changed | UPDATE |
| E2E-EVT-BOOK-02 | Logged-in in-app booking | Must remain unchanged | UPDATE |

### Assumptions Made

- Ticket scope applies to Koyu booking-link entry flow in Learner App / web app experience only.
- Child features LT-94695, LT-94696, LT-94697 are implementation split and inherit the parent acceptance scope.
- Booking verified screen remains the existing post-auth screen and no copy/UI changes are requested.

## Clarification Questions

1. **[MISSING BEHAVIOR]** What should happen when the booking link is invalid or expired: show event-list fallback, error page, or login page?
2. **[MISSING BEHAVIOR]** If user reaches Login/Register from Reserve and then cancels auth, should they return to Event Detail or Event List?
3. **[UNDOCUMENTED IN AC]** Which exact fields and ordering on Event List/Event Detail are mandatory in pre-login mode?
4. **[ROLE GAP]** For parent accounts with multiple children, which child context should be used when resuming post-auth booking flow?
5. **[REGRESSION RISK]** Should direct URL navigation to Event Detail outside booking-link flow also bypass login until Reserve, or remain current behavior?

> Not posted to Jira (MCP Jira tool unavailable in this session).

## Related Specs

- `epics/OOP/koyu/LT-94674-cancel-booked-event-update/spec.md` - shared event booking flow and auth/Reserve behavior dependencies for Koyu.
- `epics/event/LT-73558-target-segment-event-management/spec.md` - baseline behavior for event list visibility and reserve flow.

## Related Test Cases

- `epics/OOP/koyu/LT-94674-cancel-booked-event-update/test-cases/LT-94674-cancel-booked-event-update.csv` - regression-sensitive booking/reserve behavior for Koyu.
- `epics/OOP/koyu/LT-90578-auto-create-application/test-cases/LT-90578-auto-create-application.csv` - downstream booking/application continuity checks.

## QASE Coverage Gaps

- AC 01.1-01.2 pre-login Event List and Event Detail browsing from booking link has no dedicated LT-94694 suite yet.
- AC 01.3 login/register trigger point at Reserve requires explicit gating tests (no premature auth prompt).
- AC 01.4 post-auth continuity from booking-link flow to booking verified screen needs explicit test coverage.
- AC 01.5 unchanged in-app flow must have regression checks to prevent side effects from routing change.
