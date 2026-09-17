# Test Cases: LT-107816 - Display Bookable Flag on Lesson Calendar Details Screen

## Suite: Bookable Flag on Lesson Calendar Detail (LT-107816)

### [Support] Lesson Calendar Detail - Bookable Flag ON shows check icon

**Description:** LT-107816 - Component Display - Calendar lesson detail shows a check icon when the lesson is bookable.

**Preconditions:**
- Logged in as HQ/CM Staff in Salesforce.
- `Lesson_Custom_Settings__c.Lesson_Booking__c = true`.
- Lesson `Bookable Lesson A` exists on Lesson Calendar with `Bookable_Flag__c = true`.
- User has permission to view `Lesson__c.Bookable_Flag__c`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Salesforce Lesson Calendar for the lesson date/location. | Calendar loads and `Bookable Lesson A` is visible. | lesson = Bookable Lesson A |
| 2 | Click the lesson card to open the Calendar lesson detail panel. | The right-side Calendar detail panel opens for the selected lesson. | entry_point = Lesson Calendar |
| 3 | Inspect the Detail tab rows. | `Bookable Flag` label is displayed. | custom_setting = Lesson_Booking__c true |
| 4 | Inspect the Bookable Flag value. | A check icon is displayed; the value is not `--`. | Bookable_Flag__c = true |

**Severity:** major
**Priority:** high

---

### [Support] Lesson Calendar Detail - Bookable Flag OFF shows dash

**Description:** LT-107816 - Decision Table - Calendar lesson detail shows `--` when the lesson is not bookable.

**Preconditions:**
- Logged in as HQ/CM Staff in Salesforce.
- `Lesson_Custom_Settings__c.Lesson_Booking__c = true`.
- Lesson `Non-bookable Lesson A` exists on Lesson Calendar with `Bookable_Flag__c = false`.
- User has permission to view `Lesson__c.Bookable_Flag__c`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Salesforce Lesson Calendar for the lesson date/location. | Calendar loads and `Non-bookable Lesson A` is visible. | lesson = Non-bookable Lesson A |
| 2 | Click the lesson card to open the Calendar lesson detail panel. | The right-side Calendar detail panel opens. | entry_point = Lesson Calendar |
| 3 | Inspect the Bookable Flag row. | `Bookable Flag` label is displayed and the value is `--`. | Bookable_Flag__c = false |
| 4 | Confirm no check icon is shown in this row. | No `utility:check` icon appears for the false value. | expected_icon = hidden |

**Severity:** major
**Priority:** high

---

### [Support] Lesson Calendar Detail - Lesson Booking setting disabled hides Bookable Flag row

**Description:** LT-107816 - Feature Setting Guard - Calendar detail hides Bookable Flag when Lesson Booking is disabled.

**Preconditions:**
- Logged in as HQ/CM Staff in Salesforce.
- `Lesson_Custom_Settings__c.Lesson_Booking__c = false`.
- Lesson `Bookable Hidden Setting Lesson A` exists on Lesson Calendar with `Bookable_Flag__c = true`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Salesforce Lesson Calendar for the lesson date/location. | Calendar loads and the lesson is visible. | lesson = Bookable Hidden Setting Lesson A |
| 2 | Click the lesson card to open the Calendar lesson detail panel. | The right-side Calendar detail panel opens. | custom_setting = Lesson_Booking__c false |
| 3 | Inspect all Detail tab rows. | `Bookable Flag` row is not displayed. | Bookable_Flag__c = true |
| 4 | Confirm other lesson detail rows still render normally. | Existing fields such as Status, Date/Time, Capacity, Teachers, and Students remain visible. | regression = existing fields unaffected |

**Severity:** major
**Priority:** high

---

### [Support] Lesson Calendar Detail - Bookable Flag refreshes after edit

**Description:** LT-107816 - State Refresh - Calendar detail reflects the latest Bookable Flag after the lesson is edited.

**Preconditions:**
- Logged in as HQ/CM Staff in Salesforce with lesson edit permission.
- `Lesson_Custom_Settings__c.Lesson_Booking__c = true`.
- Lesson `Bookable Refresh Lesson A` exists on Lesson Calendar with `Bookable_Flag__c = false`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the lesson from Salesforce Lesson Calendar. | Calendar detail panel opens and `Bookable Flag` value is `--`. | initial Bookable_Flag__c = false |
| 2 | Open the lesson edit flow from the Calendar detail panel. | Edit modal opens and the Bookable Flag checkbox reflects the current false value. | entry_point = calendar detail edit |
| 3 | Turn Bookable Flag ON and save. | Save succeeds and Calendar detail refreshes. | new Bookable_Flag__c = true |
| 4 | Inspect the same Calendar detail panel after refresh. | `Bookable Flag` value changes from `--` to a check icon without navigating away from Calendar. | expected refresh = check icon |

**Severity:** major
**Priority:** high

---

### [Support] Lesson Calendar Collapsible Detail - Bookable Flag value uses same mapping

**Description:** LT-107816 - Regression - Collapsible lesson detail uses `Lesson__c.Bookable_Flag__c` consistently with the main Calendar detail panel.

**Preconditions:**
- Logged in as HQ/CM Staff in Salesforce.
- `Lesson_Custom_Settings__c.Lesson_Booking__c = true`.
- Lesson `Collapsible Bookable Lesson A` has `Bookable_Flag__c = true`.
- Lesson `Collapsible Non-bookable Lesson A` has `Bookable_Flag__c = false`.
- Calendar surface supports the collapsible lesson detail component.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Calendar detail/collapsible view for `Collapsible Bookable Lesson A`. | Detail component loads without data error. | Bookable_Flag__c = true |
| 2 | Inspect the Bookable Flag row. | `Bookable Flag` displays a check icon. | expected = check icon |
| 3 | Open Calendar detail/collapsible view for `Collapsible Non-bookable Lesson A`. | Detail component loads without data error. | Bookable_Flag__c = false |
| 4 | Inspect the Bookable Flag row. | `Bookable Flag` displays `--`, matching the main Calendar detail behavior. | expected = -- |

**Severity:** minor
**Priority:** medium

