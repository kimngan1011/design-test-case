# Test Coverage: LT-94105 — Riso | Core | Location Closed Date and Holiday

**Jira:** https://manabie.atlassian.net/browse/LT-94105  
**Date:** 2026-08-14

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| 1–3 | AC 01.1 | `Closed Date.Type` is a picklist with the `Closed Date / 休校日` and `Holiday / 祝日` values; new records default to Closed Date. |
| 4–6 | AC 01.2 | The New Closed Date dialog shows Type; a user can change it at creation and edit it later. |
| 7–14 | AC 01.3 | The Learner Calendar and day detail render weekday, Holiday, Closed Date, selected, and today states with the specified colors, patterns, labels, and unchanged closed-date body content. |
| 15 | AC 01.3 | The Learner App resolves Type through Enrollment Location → Location/current AY → Academic Calendar → ACI Closed Date. |
| 16–21 | AC 02.1 | One-time and manual lessons are allowed on either Type; recurring creation and extension skip Closed Date only when `Skip Closed Date` is enabled, and create lessons on Public Holiday. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.1 | 1–3 | Validation logic; Data integrity; Cross-system impact |
| AC 01.2 | 4–6 | State transition; Permission logic; Data integrity; Cross-system impact |
| AC 01.3 | 7–14 | Display completeness; Conditional logic; Cross-system impact |
| AC 01.3 | 15 | Data integrity; Cross-system impact; Conditional logic |
| AC 02.1 | 16–21 | Conditional logic; Recurrence logic; State transition; Cross-system impact |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Validation logic | Equivalence Partitioning; Negative |
| Data integrity | CRUD; Regression; Decision Table |
| State transition | State Transition; CRUD |
| Permission logic | Permission Matrix; Decision Table |
| Conditional logic | Decision Table; Negative |
| Recurrence logic | State Transition; Regression |
| Cross-system impact | Regression; CRUD |
| Display completeness | Component; Negative (field absent) |

## 4. Mandatory Edge-Case Assessment

| Area | Applies? | Coverage decision |
|---|---|---|
| A. Configuration-driven thresholds | N/A | No configurable threshold is in scope. `Skip Closed Date` is a confirmed decision-table behavior, including inherited behavior in Extend Recurrence. |
| B. Date / time | Yes | Cover today/date boundaries in JST, device time zones either side of midnight, and cross-midnight refresh for Calendar display and recurring generation. DST is N/A because the business timezone is JST. |
| C. Concurrent / stale state | Yes | Cover Type change while the Learner Calendar is open, duplicate save protection for Closed Date creation, and recurring-generation retry/idempotency. |
| D. Permission & role | Yes | HQ creates and edits Closed Dates. Centre Manager views all Closed Dates and may link an existing Closed Date to its own ACI, but cannot create or edit any Closed Date. Tenant isolation for Riso is required. |
| E. State transition | Yes | Cover default Closed Date → Holiday update and Holiday → Closed Date update; define that historical-lesson effects are pending product confirmation. |
| F. Cross-system / surface | Yes | Verify Salesforce closed-date data is rendered consistently in the Learner App and used by the recurring lesson generator. |
| G. Downstream effects | Yes | Inventory below maps every relevant write/change to an owning planned case. |
| H. Display & ordering | Yes | Inventory below covers each changed component. No sort rule is stated; no Ordering/Sort case is planned. |
| H.1 Spec–Figma display mismatch | Resolved | The Figma URL is not accessible. At the user's direction, the ticket's linked PRD **Riso \| Core \| Closed date and Public Holiday** is the visual authority. Its Calendar screenshots/text match the spec for Type default/editing, Saturday/Sunday/Holiday/Closed Date/selected/today states, `祝日`, and unchanged Closed Date body content. No PRD–spec mismatch was found. |

### H.1 PRD Visual Comparison (substituted for inaccessible Figma)

| Screen / Component | Field / state | In spec? | In linked PRD? | Mismatch type | Resolution |
|---|---|---|---|---|---|
| New Closed Date popup | Type field, Closed Date default, Holiday change/edit | ✅ | ✅ | None | PRD accepted as the visual authority by user. |
| Learner Calendar | Saturday, Sunday/Holiday, Closed Date, selected, and today treatment | ✅ | ✅ | None | PRD accepted as the visual authority by user. |
| Learner day detail | `祝日` next to Holiday date; unchanged Closed Date body content | ✅ | ✅ | None | PRD accepted as the visual authority by user. |

### G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (planned TC) |
|---|---|---|---|
| Create Closed Date with Type | Type persists with the selected/default value and remains scoped to the target ACI/location/AY | Salesforce Closed Date / ACI | `closed-date-type-management` |
| Create Closed Date with Type | The matching date resolves to the appropriate calendar appearance and day-detail label | Learner App Calendar | `learner-calendar-holiday-display` |
| Update Closed Date Type | Subsequent calendar reads and future recurring-generation evaluation use the new Type | Learner App; recurring lesson generator | `closed-date-type-management`; `lesson-creation-by-date-type` |
| Create or extend recurring lesson on Closed Date | The occurrence is skipped only when `Skip Closed Date` is enabled; the schedule continues without a duplicate/retry-created lesson | Lesson / schedule chain | `lesson-creation-by-date-type` |
| Create or extend recurring lesson on Public Holiday | A lesson is created normally with the expected date and sequence, including when `Skip Closed Date` is enabled | Lesson / schedule chain | `lesson-creation-by-date-type` |
| Create one-time or manually added lesson | The requested lesson is created on either Type without an unintended Closed Date block | Lesson; Lesson Schedule Add Lesson | `lesson-creation-by-date-type` |

### H. Display & Ordering Inventory

| Screen / Component | Required Fields / States | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| New Closed Date popup | Type field; `Closed Date` default; `Holiday / 祝日` selectable | Existing record supports Type edit | N/A — no ordering behavior stated | `Closed Date`; `Holiday`; `祝日` |
| Learner Calendar cell | Saturday blue; Sunday/Holiday `#295ACB`; Closed Date gray/diagonal; selected `#DEEBFF`; today bold white/`#395AD2` circle | Selected Closed Date retains diagonal lines; today overlays Closed Date/selected | N/A — no ordering behavior stated | Exact color tokens above |
| Learner day detail | `祝日` next to date for Holiday; existing Closed Date body/name unchanged | Holiday label appears only for Holiday | N/A — no ordering behavior stated | `祝日` |

## 5. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1 | Type picklist exposes exactly Closed Date / `休校日` and Holiday / `祝日` | Validation logic | Equivalence Partitioning; Negative | High | Deep |
| AC 01.1 | New Closed Date defaults Type to Closed Date | Validation logic; State transition | Equivalence Partitioning; CRUD | Medium | Standard |
| AC 01.1 | Type persists without corrupting the ACI, location, or AY relationship | Data integrity; Cross-system impact | CRUD; Regression | High | Deep |
| AC 01.2 | New Closed Date popup exposes Type and permits the Holiday selection | Display completeness; Conditional logic | Component; Decision Table | Medium | Standard |
| AC 01.2 | Existing Closed Date Type can change in both directions | State transition; Data integrity | State Transition; CRUD | High | Deep |
| AC 01.2 | Only authorised Riso staff can create or edit Type, within their permitted location scope | Permission logic | Permission Matrix; Negative | High | Deep |
| AC 01.3 | Calendar renders Saturday, Sunday, Holiday, and Closed Date with the exact required treatment | Display completeness; Conditional logic | Component; Decision Table | Medium | Deep |
| AC 01.3 | Selected Closed Date and today overlays retain their required pattern/circle precedence | Conditional logic; Display completeness | Decision Table; Component | Medium | Deep |
| AC 01.3 | Day detail displays `祝日` for Holiday and retains Closed Date body content | Display completeness; Cross-system impact | Component; Regression | Medium | Standard |
| AC 01.3 | Calendar resolves only the enrolled learner's location/current-AY ACI Type | Data integrity; Cross-system impact | CRUD; Decision Table; Regression | High | Deep |
| AC 01.3 | Calendar updates safely after a Type update and on a device near JST midnight | Conditional logic; Cross-system impact | State Transition; Negative | Medium | Deep |
| AC 02.1 | One-time lesson is created on Closed Date and Public Holiday | Conditional logic | Decision Table | High | Standard |
| AC 02.1 | Manual Add Lesson is created on Closed Date and Public Holiday | Conditional logic; State transition | Decision Table; Regression | High | Standard |
| AC 02.1 | Recurring creation and extension skip Closed Date only when `Skip Closed Date` is enabled and preserve the correct chain/sequence | Recurrence logic; Data integrity | State Transition; Regression | High | Deep |
| AC 02.1 | Recurring creation and extension occur normally on a Closed Date when `Skip Closed Date` is disabled and on Public Holiday | Recurrence logic; Conditional logic | Decision Table; Regression | High | Deep |
| AC 02.1 | Retry/double-submit does not create duplicate lessons or skip an additional occurrence | Data integrity; Recurrence logic | Negative; Regression | High | Deep |

## 6. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

No Critical risk is identified: the ticket does not directly change billing, payments, or destructive data operations.

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Closed Date Type and ACI isolation | A wrong Type/location/AY lookup changes calendar behavior for the wrong learner population. | Create contrasting ACI records across two locations and academic years; assert both stored data and Learner App result. |
| Type update and permissions | An unauthorised or incorrectly scoped change alters operational dates. | Full role/location permission matrix; default/change/reload checks; stale-page save test. |
| Recurrence by Type | A wrong decision creates or omits lessons across the Type × `Skip Closed Date` matrix. | Decision table across Type × operation (creation/extension) × Skip Closed Date; assert created occurrence dates, chain continuity, and retry idempotency. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Calendar visual state precedence | Incorrect styling can mislead students/parents about center availability. | Component inventory with separate selected/today/Closed Date combinations; exact color/text assertions. |
| Day-detail labeling | A missing or incorrect `祝日` label creates a user-facing inconsistency. | Positive Holiday and negative Closed Date assertions on the same location/AY data. |

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Type field/value/default/edit lifecycle | LT-87693 ACI Closed Date cases | Existing cases cover ACI Closed Date CRUD but not Type. | ✅ Picklist values, default, edit both directions, legacy/null behavior, and persistence. |
| Type permissions and Riso scope | LT-87693 ACI role cases | Existing cases establish ACI permissions but not Type-specific authorisation. | ✅ Role/location matrix and denied-user behavior. |
| Learner Calendar / day-detail Type display | LT-87693 general calendar baseline | Existing baseline does not distinguish Holiday from Closed Date. | ✅ Exact state inventory, `祝日`, lookup isolation, and calendar refresh. |
| One-time/manual lesson behavior by Type | E2E-02 / E2E-15 | Existing scenarios cover Closed Date and manual add paths, not Type decisioning. | ✅ Operation × Type decision table. |
| Recurring lesson behavior by Type | E2E-02 / E2E-15 | Existing Skip Closed Date behavior conflicts with the ticket. | ✅ Type × Skip Closed Date regression matrix for creation and Extend Recurrence, sequence, retry, and confirmed Type-edit effective time. |
| Timezone/date transition | No matching case found | Not covered by existing artifacts. | ✅ JST midnight and cross-midnight Calendar/recurrence evaluation. |

## 8. Suggested Test Suite Structure

```text
epics/OOP/riso/LT-94105-riso-location-closed-date-holiday/test-cases/
├── closed-date-type-management.md       → AC 01.1–01.2 — Type field, default, edit, permissions, ACI isolation
├── learner-calendar-holiday-display.md  → AC 01.3 — Calendar/day-detail states, lookup, localization, timezone refresh
├── lesson-creation-by-date-type.md      → AC 02.1 — One-time, recurring, manual, and Extend Recurrence decision matrix
└── recurrence-type-regression.md        → AC 01.2 + AC 02.1 — Type edit effects, Skip Closed Date compatibility, retry/idempotency
```

## 9. Open Product Decisions Carried into Test Design

- Confirmed: a Closed Date occurrence is skipped only when `Skip Closed Date` is enabled; with it disabled, the occurrence is created normally.
- The effect of changing Type after recurring lessons already exist is still unconfirmed.
- The legacy-record backfill/null behavior is still unconfirmed.
- The PRD uses both `Holiday` and `Public Holiday`; generated cases must use the confirmed canonical value when it is available.
