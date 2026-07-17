# Test Cases: LT-101735 - [koyu2] Core | Event Participant Detail page

## Suite: Event Participant Detail page (Qase Suite ID: 3185)

### [Koyu2] Event Participant Detail - Navigation from Participant List - Detail page opens for selected row

**Description:** Core flow - Staff can open Event Participant Detail from Event Participant List and land on the correct participant record.

**Preconditions:**
- Staff user can access Salesforce Event Participant List.
- At least one Activity Event has participant rows.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Activity Event Participant List in Salesforce. | Participant list is displayed. | surface = SF_event_participant_list |
| 2 | Click participant row A (or detail icon/link). | Event Participant Detail page opens. | participant = row_A |
| 3 | Verify page header/identifier. | Header identifies the same participant selected from list. | expected_identity = row_A |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Event Participant Detail - Core field rendering - All required sections are visible

**Description:** Core display - Detail page shows all mandatory participant information blocks required by PRD/Figma.

**Preconditions:**
- Staff user can open Event Participant Detail.
- Participant has complete profile/event data.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Event Participant Detail for participant with full data. | Detail page loads successfully. | participant = full_dataset |
| 2 | Scan page sections from top to bottom. | All required sections are present with labels as designed. | baseline = PRD_figma |
| 3 | Check key values in each section. | Values are populated and human-readable (no raw IDs unless intended). | expected_format = display_ready |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Event Participant Detail - Student Classification - Value displayed when set

**Description:** Note1 alignment - Student Classification is included in detail page and shows current value when available.

**Preconditions:**
- Participant has Student Classification value set (from PBT-2463 scope).
- Staff user can access detail page.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Event Participant Detail for participant with classification value. | Detail page loads. | participant_classification = set |
| 2 | Locate Student Classification field on detail page. | Field is visible. | field = student_classification |
| 3 | Read displayed value. | Displayed value matches record value exactly. | expected_value = in_record |

**Severity:** major
**Priority:** high

---

### [Koyu2] Event Participant Detail - Student Classification - Empty-state handling

**Description:** Negative display - When Student Classification is not set, page shows configured empty state without breaking layout.

**Preconditions:**
- Participant has no Student Classification value.
- Staff user can access detail page.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Event Participant Detail for participant with null classification. | Detail page loads. | participant_classification = null |
| 2 | Locate Student Classification field. | Field remains visible in expected position. | field = student_classification |
| 3 | Observe value rendering. | Empty-state placeholder is shown consistently (blank or dash per design), no error text. | expected_empty_state = design_default |

**Severity:** major
**Priority:** medium

---

### [Koyu2] Event Participant Detail - Koyu OOP fields - Field set appears and values are correct

**Description:** Note2 alignment - Koyu-specific OOP information is displayed on the detail page with correct mapping.

**Preconditions:**
- Participant record has Koyu OOP fields populated.
- Staff user can access detail page.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Event Participant Detail for participant with Koyu OOP values. | Detail page loads. | participant = koyu_oop_full |
| 2 | Locate Koyu OOP information block. | OOP block and fields are visible. | section = koyu_oop |
| 3 | Compare displayed values against source record. | Each displayed OOP field matches source record value. | expected_mapping = exact |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Event Participant Detail - Data consistency with Participant List

**Description:** Cross-view consistency - Key summary values shown in list and detail are consistent for the same participant.

**Preconditions:**
- Participant list includes at least one row with known values.
- Staff user can open list and detail pages.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Note key values for row A in Participant List (e.g., student name, response/status). | Snapshot of list values is captured. | participant = row_A |
| 2 | Open detail page for row A. | Detail page opens for the same participant. | participant = row_A |
| 3 | Compare key values list vs detail. | Values are consistent across list and detail for the same fields. | comparison = list_vs_detail |

**Severity:** major
**Priority:** high

---

### [Koyu2] Event Participant Detail - Back navigation - Return to originating list context

**Description:** UX flow - Returning from detail should preserve navigation context and avoid losing operator position.

**Preconditions:**
- Staff user opens detail from a participant list with filters/sort applied.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | From filtered/sorted Participant List, open participant detail. | Detail page opens. | list_state = filtered_sorted |
| 2 | Click Back button or use in-app return action. | User returns to Participant List. | action = back |
| 3 | Verify list state. | Filter/sort and pagination context are preserved where supported by design. | expected_context = preserved |

**Severity:** major
**Priority:** medium

---

### [Koyu2] Event Participant Detail - Permission matrix - Authorized roles can access

**Description:** Access control positive - Expected staff roles can open and read Event Participant Detail page.

**Preconditions:**
- Test users for supported roles are available (e.g., HQ, CM, Staff/Teacher per partner policy).
- Participant record exists.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Login as authorized role A and open participant detail from list. | Page opens and required fields are visible. | role = authorized_A |
| 2 | Repeat for authorized role B. | Page opens and required fields are visible. | role = authorized_B |
| 3 | Repeat for authorized role C. | Page opens and required fields are visible. | role = authorized_C |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Event Participant Detail - Permission matrix - Unauthorized user blocked

**Description:** Access control negative - Users without permission cannot open Event Participant Detail directly or via list action.

**Preconditions:**
- Test user without required permission exists.
- Participant record ID/deep link is available.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Login as unauthorized user and open participant list. | Detail action is hidden/disabled or inaccessible. | role = unauthorized |
| 2 | Attempt direct URL/deep link to detail page. | Access is denied with proper authorization handling. | entry = deep_link |
| 3 | Verify no sensitive participant data is exposed. | User cannot view participant details. | data_exposure = none |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Event Participant Detail - Robustness - Invalid or deleted participant record handling

**Description:** Error handling - Opening non-existent participant detail should show controlled error state.

**Preconditions:**
- Invalid or deleted participant record ID is available.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open detail page with invalid/deleted participant ID. | System does not crash. | participant_id = invalid_or_deleted |
| 2 | Observe page response. | User sees controlled error/empty state per platform standard. | expected_error_state = standard |
| 3 | Navigate back to list/home. | Navigation remains functional after error state. | recovery = successful |

**Severity:** major
**Priority:** medium

---

### [Koyu2] Event Participant Detail - Regression - Participant List behavior remains unchanged

**Description:** Regression - Adding detail page link does not break existing Participant List behaviors.

**Preconditions:**
- Existing participant list features are available in environment (search/filter/sort/pagination as applicable).

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Use participant list search/filter/sort before opening any detail. | List behaves as baseline. | baseline_check = before_open_detail |
| 2 | Open and close several participant detail pages. | Navigation works without errors. | iteration = multiple_rows |
| 3 | Re-check search/filter/sort/pagination in list. | List features still behave as baseline. | baseline_check = after_return |

**Severity:** major
**Priority:** medium
