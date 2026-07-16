# Test Cases: LT-89471 — Recurring-until date format by locale

**Suite:** Recurring Date Format by Locale
**Qase suite:** PX > Calendar > LT-89471 Calendar Bug Fix > Recurring Date Format by Locale
**Epic:** https://manabie.atlassian.net/browse/LT-89471
**AC covered:** AC 02.1

---

## Suite: Recurring Date Format by Locale

### Lesson Detail Right Panel - Japanese Locale - Recurring Until Uses yyyy/mm/dd

**Description:** AC 02.1 — Component + Decision Table — Japanese locale renders recurring-until date in yyyy/mm/dd format.

**Preconditions:**
- Logged in as HQ or CM Staff
- A recurring lesson exists and opens in lesson detail right panel
- User locale is set to Japanese (ja-JP)

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open lesson detail right panel for recurring lesson as Japanese locale user | Panel loads recurring section | recurring_until_source = 2026-12-31; locale = ja-JP |
| 2 | Read the recurring-until value in recurring section | Date is displayed as 2026/12/31 (yyyy/mm/dd) | expected_format = yyyy/mm/dd |
| 3 | Compare visible value against source date | Displayed date matches source date with slash format | source = 2026-12-31; shown = 2026/12/31 |

**Severity:** major
**Priority:** high

---

### Lesson Detail Right Panel - Non-Japanese Locale - Existing Locale Format Preserved

**Description:** AC 02.1 — Decision Table + Regression — Non-Japanese locale keeps existing locale-specific rendering.

**Preconditions:**
- Logged in as HQ or CM Staff
- A recurring lesson exists and opens in lesson detail right panel
- User locale is set to a non-Japanese locale

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open lesson detail right panel for recurring lesson as non-Japanese locale user | Panel loads recurring section | recurring_until_source = 2026-12-31; locale = en-US |
| 2 | Read the recurring-until value in recurring section | Date follows locale-specific non-JP format and is not forcibly rendered as yyyy/mm/dd | non_jp_expected = locale pattern |
| 3 | Confirm AC 02.1 scope is JP-only behavior | No global JP-format override is observed | forbidden_value = 2026/12/31 (for en-US) |

**Severity:** minor
**Priority:** medium

---

### Lesson Detail Right Panel - Locale Switch at Runtime - Recurring Until Re-renders by Active Locale

**Description:** AC 02.1 — Regression + Decision Table — Recurring-until rendering updates correctly after locale switch.

**Preconditions:**
- Logged in as HQ or CM Staff
- A recurring lesson exists and opens in lesson detail right panel
- User can switch locale between en-US and ja-JP

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open recurring lesson detail with en-US locale | Recurring-until shows non-JP locale format | recurring_until_source = 2026-12-31; locale = en-US |
| 2 | Switch user locale to ja-JP and refresh lesson detail panel | Recurring-until re-renders as yyyy/mm/dd | locale = ja-JP; expected = 2026/12/31 |
| 3 | Switch back to en-US and refresh again | Recurring-until returns to non-JP locale format | locale = en-US |

**Severity:** minor
**Priority:** medium

---

### Lesson Detail Right Panel - Japanese Locale - Single Digit Month and Day Keep Zero Padding

**Description:** AC 02.1 — Boundary Value Analysis — Japanese format preserves zero padding in month/day for single-digit values.

**Preconditions:**
- Logged in as HQ or CM Staff
- A recurring lesson exists with single-digit month/day recurring-until date
- User locale is set to Japanese (ja-JP)

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open recurring lesson detail right panel as Japanese locale user | Panel loads recurring section | recurring_until_source = 2026-01-05; locale = ja-JP |
| 2 | Read recurring-until displayed value | Date is displayed as 2026/01/05 with zero padding | expected = 2026/01/05 |
| 3 | Compare visible value to format rule | Display matches yyyy/mm/dd exactly | pattern = ^YYYY/MM/DD$ |

**Severity:** major
**Priority:** high
