# Test Cases: LT-89471 — Daily view horizontal scrollbar

**Suite:** Daily View Scrollbar
**Qase suite:** PX > Calendar > LT-89471 Calendar Bug Fix > Daily View Scrollbar
**Epic:** https://manabie.atlassian.net/browse/LT-89471
**AC covered:** AC 01.1

---

## Suite: Daily View Scrollbar

### Calendar Daily View - SF - Overflow Timeline - Horizontal Scrollbar Visible and Reachable

**Description:** AC 01.1 — Component + Decision Table — Under constrained width with overflow, SF Daily view provides horizontal navigation to access full timeline.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce calendar
- Daily view is open with enough timeline columns to overflow narrow viewport
- Browser window width is set to 1280 or smaller

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Lesson Calendar in Daily view on SF and set browser width to constrained size | Daily view is shown and timeline overflows available width | viewport_width = 1280 |
| 2 | Observe the timeline container footer area | Horizontal scrollbar is visible | timeline_columns = 10+ |
| 3 | Drag scrollbar to the far right | Far-right timeline columns become visible and interactive | scroll_position = max |

**Severity:** major
**Priority:** high

---

### Calendar Daily View - BO - Overflow Timeline - Horizontal Scrollbar Visible and Reachable

**Description:** AC 01.1 — Component + Regression — BO Daily view provides horizontal navigation under overflow and keeps parity with SF behavior.

**Preconditions:**
- Logged in as HQ or CM Staff to Back Office calendar
- Daily view is open with enough timeline columns to overflow narrow viewport
- Browser window width is set to 1280 or smaller

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Calendar in Daily view and set browser width to constrained size | Daily view is shown and timeline overflows available width | viewport_width = 1280 |
| 2 | Observe the timeline container footer area | Horizontal scrollbar is visible | timeline_columns = 10+ |
| 3 | Drag scrollbar to the far right | Far-right timeline columns become visible and interactive | scroll_position = max |

**Severity:** major
**Priority:** high

---

### Calendar Daily View - SF - Non-Overflow Timeline - Content Fully Visible Without Horizontal Scroll

**Description:** AC 01.1 — Decision Table + Negative — When timeline does not overflow, Daily view remains fully visible without clipped content.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce calendar
- Daily view is open with limited timeline columns
- Browser window width is 1920 or equivalent non-constrained width

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Daily view with non-overflow setup | Full timeline fits in the viewport | viewport_width = 1920; timeline_columns <= visible_limit |
| 2 | Observe timeline container | No hidden right-side columns and no clipped content | overflow = false |
| 3 | Interact with left-most and right-most visible columns | All visible columns are accessible without forced horizontal scrolling | interaction = click slot |

**Severity:** minor
**Priority:** medium

---

### Calendar Daily View - Viewport and Zoom Matrix - Scrollbar Behavior Stays Consistent

**Description:** AC 01.1 — Decision Table — Scrollbar behavior remains consistent across constrained viewport and common zoom settings.

**Preconditions:**
- Logged in as HQ or CM Staff
- Daily view is open with timeline overflow

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Set viewport and zoom combination A then open Daily view | Horizontal scrollbar is visible and works | viewport_width = 1366; zoom = 100% |
| 2 | Set combination B then open Daily view | Horizontal scrollbar is visible and works | viewport_width = 1280; zoom = 125% |
| 3 | Set combination C then open Daily view | Horizontal scrollbar is visible and works | viewport_width = 1024; zoom = 100% |

**Severity:** major
**Priority:** high
