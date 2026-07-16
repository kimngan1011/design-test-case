# Test Coverage: LT-94694 - Booking Link to Event List page

**Jira:** https://manabie.atlassian.net/browse/LT-94694
**Date:** 2026-07-03

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| 1 | AC 01.1 | Booking-link landing page is Activity Event List. |
| 2 | AC 01.1 | First screen must not force authentication. |
| 3 | AC 01.2 | Event list is browsable by unauthenticated users through booking link. |
| 4 | AC 01.2 | Event detail is browsable by unauthenticated users through booking link. |
| 5 | AC 01.3 | Reserve action requires authentication. |
| 6 | AC 01.3 | Login redirect trigger is tied to Reserve action only. |
| 7 | AC 01.4 | Post-auth continuation returns user to booking flow context. |
| 8 | AC 01.4 | Register path follows same continuation rule as login path. |
| 9 | AC 01.5 | Existing in-app booking path remains unchanged for logged-in users. |
| 10 | AC 01.5 | Direct navigation handling must not regress current event page behavior for existing users. |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.1 | 1, 2 | State transition, Conditional logic |
| AC 01.2 | 3, 4 | Display completeness |
| AC 01.3 | 5, 6 | Permission, Conditional logic |
| AC 01.4 | 7, 8 | State transition, Cross-system impact |
| AC 01.5 | 9, 10 | Regression, Data integrity |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| State transition | State Transition Testing, Regression Analysis |
| Conditional logic | Decision Table, Equivalence Partitioning |
| Display completeness | Component Testing, Equivalence Partitioning |
| Permission | Permission Matrix, Negative Testing |
| Cross-system impact | Regression Analysis, Scenario Testing |
| Data integrity | CRUD Testing, Regression Analysis |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1 | Booking link opens Activity Event List as first screen | State transition | State Transition Testing | Critical | Deep |
| AC 01.1 | Login page is not shown before user action on reserve | Conditional logic | Decision Table | High | Deep |
| AC 01.2 | Event list fields render in pre-login mode | Display completeness | Component Testing | High | Standard |
| AC 01.2 | Event detail is accessible in pre-login mode | Display completeness | Equivalence Partitioning | High | Standard |
| AC 01.3 | Reserve tap redirects unauthenticated user to Login/Register | Permission | Permission Matrix | Critical | Deep |
| AC 01.3 | Login trigger occurs only on Reserve action | Conditional logic | Decision Table | Critical | Deep |
| AC 01.4 | Login path resumes booking flow after successful auth | State transition | State Transition Testing | Critical | Deep |
| AC 01.4 | Register path resumes booking flow after successful auth | Cross-system impact | Scenario Testing | High | Standard |
| AC 01.5 | Existing in-app booking flow remains unchanged | Regression | Regression Analysis | Critical | Deep |
| AC 01.5 | Direct navigation remains stable for existing users | Data integrity | Regression Analysis | High | Standard |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Booking-link routing + auth trigger split | If auth is still triggered at entry, the business objective fails and user drop-off remains. | End-to-end state transition checks with explicit assertion that login is triggered only at Reserve tap. |
| Post-auth continuation flow | Broken return context after login/register can lose selected event or booking intent. | Deep scenario tests for login and register path with preserved event context. |
| Existing in-app flow regression | Routing changes can unintentionally alter currently stable logged-in flow. | Mandatory regression suite for no-change flow and direct event navigation path. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Pre-login Event List/Event Detail rendering | Missing fields or broken visibility can make browsing unusable. | Display completeness checks for mandatory cards/details and action affordances. |
| Direct navigation behavior | Legacy redirect middleware may force auth unexpectedly. | Regression test for direct Event Detail URL/path behavior. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Login/Register cancellation handling | Not fully defined in AC; potential UX inconsistency. | Exploratory follow-up tests after PM clarification. |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Booking link opens Event List before auth | No dedicated LT-94694 cases found | None | ✅ New suite and cases for booking-link entry routing |
| Reserve-only auth trigger | Koyu booking suites focus on already-authenticated flows | Partial | ✅ New auth trigger boundary checks |
| Post-login/register continuation | Existing cases do not validate booking-link return context | None | ✅ New continuation flow cases |
| Existing in-app flow unchanged | Covered in older suites but not against LT-94694 change set | Partial | ✅ Regression cases explicitly tied to LT-94694 |

---

## 7. Suggested Test Suite Structure

```
epics/OOP/koyu/LT-94694-booking-link-event-list-page/test-cases/
├── 01-booking-link-prelogin-navigation.md -> AC 01.1-01.2
├── 02-reserve-auth-trigger-and-continuation.md -> AC 01.3-01.4
├── 03-existing-flow-regression.md -> AC 01.5
```
