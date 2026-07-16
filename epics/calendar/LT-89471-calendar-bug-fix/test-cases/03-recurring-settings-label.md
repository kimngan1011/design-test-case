# Test Cases: LT-89471 — Recurring Settings label text

**Suite:** Recurring Settings Label
**Qase suite:** PX > Calendar > LT-89471 Calendar Bug Fix > Recurring Settings Label
**Epic:** https://manabie.atlassian.net/browse/LT-89471
**AC covered:** AC 02.2

---

## Suite: Recurring Settings Label

### Lesson Detail Right Panel - SF - Recurring Section Uses Exact Text Recurring Settings

**Description:** AC 02.2 — Component — Recurring section label in SF right panel displays exact text Recurring Settings.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce
- A recurring lesson exists and can be opened in lesson detail right panel

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open recurring lesson detail right panel in SF | Recurring section is displayed | surface = SF right panel |
| 2 | Read the recurring section header text | Header text is exactly Recurring Settings | expected_label = Recurring Settings |
| 3 | Search visible recurring section for old wording | Weekly Recurring text is not shown in the target panel | forbidden_label = Weekly Recurring |

**Severity:** minor
**Priority:** medium

---

### Lesson Detail Right Panel - BO - Recurring Section Uses Exact Text Recurring Settings

**Description:** AC 02.2 — Component + Regression — Recurring section label in BO right panel displays exact text Recurring Settings.

**Preconditions:**
- Logged in as HQ or CM Staff to Back Office
- A recurring lesson exists and can be opened in lesson detail right panel

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open recurring lesson detail right panel in BO | Recurring section is displayed | surface = BO right panel |
| 2 | Read the recurring section header text | Header text is exactly Recurring Settings | expected_label = Recurring Settings |
| 3 | Search visible recurring section for old wording | Weekly Recurring text is not shown in the target panel | forbidden_label = Weekly Recurring |

**Severity:** minor
**Priority:** medium

---

### Lesson Detail Right Panel - Label Stability After Panel Reopen - Recurring Settings Persists

**Description:** AC 02.2 — Regression — Label remains Recurring Settings after panel close/reopen to avoid stale UI text.

**Preconditions:**
- Logged in as HQ or CM Staff
- A recurring lesson exists

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open recurring lesson detail right panel and read recurring section header | Header text is Recurring Settings | expected_label = Recurring Settings |
| 2 | Close lesson panel, reopen same lesson panel | Right panel reloads recurring section | panel_action = close_reopen |
| 3 | Read recurring section header again | Header text remains Recurring Settings and old wording is absent | forbidden_label = Weekly Recurring |

**Severity:** trivial
**Priority:** low
