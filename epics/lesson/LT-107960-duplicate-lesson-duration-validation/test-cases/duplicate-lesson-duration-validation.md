# Test Cases: LT-107960 - Duplicate Lesson Duration validation

## Suite: Duplicate Lesson

### [Core] Duplicate Lesson - Lesson Detail - Duration prefilled value does not show required validation

**Description:** Exact LT-107960 regression - Duplicate individual lesson from Lesson Detail should save when Duration is already populated.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- `Enable Duration Field on Lesson Form` is enabled.
- Individual lesson `LES-107960-01` exists with Start Time `06:40`, End Time `07:40`, and Duration `60`.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open lesson detail for `LES-107960-01`. | Lesson detail opens. | source_lesson = LES-107960-01 |
| 2 | Click `Duplicate` / `Duplicate individual lesson`. | Duplicate Lesson form opens. | entry_point = Lesson Detail |
| 3 | Observe `Duration (minutes)`. | Duration is populated with `60`. | start = 06:40; end = 07:40; duration = 60 |
| 4 | Fill any remaining required fields without clearing Duration and click Save. | No `Complete this field.` message appears under Duration. | forbidden_error = Complete this field. |
| 5 | Confirm the duplicated lesson. | Duplicate lesson is saved successfully with Duration `60`. | expected_duration = 60 |

### [Core] Duplicate Lesson - Calendar popup - Duration prefilled value saves successfully

**Description:** Calendar entry-point regression - Duplicate from Calendar should not show false required validation for a populated Duration value.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce Calendar.
- `Enable Duration Field on Lesson Form` is enabled.
- Individual lesson `LES-107960-02` appears on Calendar with Start Time `06:40`, End Time `07:40`, and Duration `60`.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Calendar and click lesson `LES-107960-02`. | Lesson popup/detail drawer opens. | source_lesson = LES-107960-02 |
| 2 | Click Duplicate from the Calendar lesson popup/detail drawer. | Duplicate Lesson form opens from Calendar. | entry_point = Calendar |
| 3 | Observe `Duration (minutes)`. | Duration is populated with `60`. | expected_duration = 60 |
| 4 | Save the duplicate without editing Duration. | No required validation appears under Duration; save succeeds. | forbidden_error = Complete this field. |
| 5 | Refresh Calendar. | The duplicated lesson appears at the selected date/time. | expected = duplicate_card_visible |

### [Core] Lesson Edit - Valid Duration value does not trigger required validation

**Description:** Adjacent regression from Jira note - Edit mode must not show `Complete this field.` when Duration already has a valid value.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- `Enable Duration Field on Lesson Form` is enabled.
- Lesson `LES-107960-03` exists with Start Time `09:00`, End Time `10:00`, and Duration `60`.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open lesson `LES-107960-03` in Edit mode. | Edit Lesson form opens. | lesson = LES-107960-03 |
| 2 | Observe `Duration (minutes)`. | Duration is populated with `60`. | duration = 60 |
| 3 | Change a non-time required-safe field such as Lesson Name suffix. | Form remains valid. | change = name suffix |
| 4 | Click Save. | No `Complete this field.` message appears under Duration; lesson saves successfully. | forbidden_error = Complete this field. |

### [Core] Lesson forms - Extend Recurrence and drag/drop derived Duration do not trigger required validation

**Description:** Adjacent regression from Jira note - Extend Recurrence and drag/drop flows use derived/prefilled Duration and must not show false required validation.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- `Enable Duration Field on Lesson Form` is enabled.
- Recurring lesson schedule `LS-107960-04` exists with Start Time `09:00`, End Time `10:00`, Duration `60`.
- A draggable lesson `LES-107960-04` exists on Calendar.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open `LS-107960-04` and click Extend Recurrence. | Extend Recurrence form opens. | schedule = LS-107960-04 |
| 2 | Observe Duration and save a valid extension. | Duration is populated; no `Complete this field.` appears; extension saves. | duration = 60 |
| 3 | Drag `LES-107960-04` to a valid new time slot on Calendar. | Edit form opens with derived Start/End/Duration values. | entry_point = drag_drop |
| 4 | Save the drag/drop edit without clearing Duration. | No `Complete this field.` appears under Duration; moved lesson saves. | forbidden_error = Complete this field. |
