# Test Cases: LT-102422 - Publish lesson menu in Lesson Calendar

## Suite: Publish Lesson Menu in Lesson Calendar

### Lesson Calendar - Publish Action - Draft Lesson - Click Publish Lesson - Status Changes To Published

**Description:** AC 01.5 - State Transition - User publishes a draft lesson directly from calendar menu without opening lesson detail page.

**Preconditions:**
- Logged in as HQ or CM Staff on Salesforce calendar.
- A lesson with status Draft exists on calendar day view.
- Lesson detail page is not opened in current browser tab.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson Calendar and select a Draft lesson card. | Lesson detail side menu opens in calendar context. | lesson_status = Draft |
| 2 | Open the right-side lesson menu and click Publish Lesson. | Publish action is accepted from calendar menu. | trigger = calendar_menu |
| 3 | Refresh calendar view and reopen the same lesson card. | Lesson status shows Published and Publish Lesson action is no longer displayed. | expected_status = Published |
| 4 | Confirm current tab remains Lesson Calendar screen. | User is still on calendar and did not navigate to lesson detail page. | navigation = stay_on_calendar |

**Severity:** critical
**Priority:** high

---

### Lesson Calendar - Publish Action - Non SF Surfaces - Publish Lesson Entry Point - Not Exposed

**Description:** AC 01.6 - Permission Matrix - Publish Lesson menu entry point is SF-only and does not appear on BO or mobile surfaces.

**Preconditions:**
- Draft lesson exists for the same tenant data set.
- User has access to SF and BO environments.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Salesforce Lesson Calendar and select the Draft lesson menu. | Publish Lesson action is visible in SF calendar menu. | surface = SF |
| 2 | Open Back Office lesson management for the same draft lesson. | Calendar-menu Publish Lesson entry point is not available in BO. | surface = BO |
| 3 | Open mobile lesson surfaces for the same draft lesson if available. | Calendar-menu Publish Lesson entry point is not available in mobile surfaces. | surface = Mobile |

**Severity:** major
**Priority:** high

---

### Lesson Calendar - Publish Action - Stale Draft Menu - Click Publish Lesson - Graceful Rejection

**Description:** AC 01.5 - Negative - If another user publishes the lesson first, stale menu click does not create invalid transition and calendar reflects final Published state.

**Preconditions:**
- Session A and Session B are both opened as HQ or CM Staff.
- Same lesson is Draft in both sessions before action.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | In Session B publish the draft lesson and confirm status becomes Published. | Session B shows lesson status Published. | actor_b_action = publish |
| 2 | In Session A without refreshing click Publish Lesson from stale menu state. | System rejects duplicate publish attempt without creating invalid state. | actor_a_state = stale_draft |
| 3 | Refresh Session A calendar and reopen the lesson. | Lesson remains Published and Publish Lesson action is not displayed. | expected_status = Published |

**Severity:** major
**Priority:** high
