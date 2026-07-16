# Test Cases: PBT-3120 - Type Option Translation in Bulk Mark Attendance

## Suite: Type Option Translation

### Bulk Mark Attendance - Type Option - Japanese mapping applied - Displays 通常 体験 講習 exactly

**Description:** AC 02.2 - Component - Confirm all required JP labels are rendered exactly for Type options.

**Preconditions:**
- Logged in as HQ or CM Staff.
- Open the target Bulk Mark Attendance view where Type options are displayed.
- UI language/context is the target configuration used for this requirement.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Bulk Mark Attendance and locate Type options | Type option control is visible | page = BO Calendar Bulk Mark Attendance |
| 2 | Expand or display all Type options | Exactly three required JP labels are visible: 通常, 体験, 講習 | expected_labels = 通常|体験|講習 |
| 3 | Select each option one by one | Selected value always shows the same JP label text with no truncation | select_each = true |

**Severity:** minor
**Priority:** medium

---

### Bulk Mark Attendance - Type Option - English fallback removed in target scope - Does not show Regular Trial Seasonal

**Description:** AC 02.2 - Negative - Ensure untranslated English labels are not present in the target scope.

**Preconditions:**
- Logged in as HQ or CM Staff.
- Open Bulk Mark Attendance Type options for the target flow.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Type options list | Options list is visible | scope = target flow |
| 2 | Scan visible label strings in the options list | `Regular`, `Trial`, and `Seasonal` are not displayed in this target scope | forbidden_labels = Regular|Trial|Seasonal |
| 3 | Choose each JP option and observe selected state text | Selected state keeps JP text and does not switch back to EN labels | selected_state = JP only |

**Severity:** minor
**Priority:** medium

---

### Bulk Mark Attendance - Type Option - Role consistency for label localization - CPU Teacher and SPU CM see identical JP labels

**Description:** AC 02.2 - Decision Table - Validate localization consistency across eligible BO roles.

**Preconditions:**
- CPU Teacher and SPU CM accounts both can access the same lesson in BO Calendar.
- Type options are visible in both role contexts.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Sign in as CPU Teacher and open Type options | JP labels are visible as 通常, 体験, 講習 | role = CPU Teacher |
| 2 | Record visible labels as snapshot A | Snapshot A captured | snapshot = A |
| 3 | Sign in as SPU CM and open Type options | JP labels are visible as 通常, 体験, 講習 | role = SPU CM |
| 4 | Record labels as snapshot B and compare with snapshot A | Snapshot B matches snapshot A exactly | compare = A vs B |

**Severity:** trivial
**Priority:** low
