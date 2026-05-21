# Test Cases: LT-87693 — Academic Calendar Closed Date per Location

**Suite:** Academic Calendar – General
**Qase suite:** PX > Master data > Academic Calendar
**Epic:** [LT-87693](https://manabie.atlassian.net/browse/LT-87693)
**ACs covered:** AC 01.1, AC 02.1 (translation), Data Migration

**Precondition (all cases):**

- Feature flag `Enable_Enhance_Academic_Calendar` is enabled in the org
- Org is configured with Japanese language support

---

## Suite: Academic Calendar – General

### Academic Calendar – UI Translation – Japanese Labels – All New UI Elements Display Correct JP Text

**Description:** AC 01.1, AC 01.2, AC 02.1 — UI Validation — Confirms that all new UI labels introduced by this feature display the correct Japanese translation when the Salesforce org is viewed in Japanese.

**Preconditions:**

- Logged in as HQ Admin with the Salesforce org language set to **Japanese**
- At least one ACM and one ACI exist

| #   | Action                                                                                                                         | Expected Result                                                                                                                           | Test Data |
| --- | ------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the Create ACM form and observe all field labels and button labels                                                 | All labels display in Japanese                                                                                                            |           |
| 2   | Confirm the error message for duplicate AY appears in Japanese when triggered (attempt to create a second ACM for the same AY) | Error message reads: **"この年度に対応するマスターカレンダーは既に存在します。既存のレコードを更新するか、別の年度を選択してください。"** |           |
| 3   | On the Create ACM form, locate the **"Select All"** button (if present in the location selector)                               | Button label reads: **"全選択"**                                                                                                          |           |
| 4   | When some locations are selected in the location picker, observe the selection count label                                     | Label reads in the format: **"X個の項目を選択中"** (e.g., "2個の項目を選択中")                                                            |           |
| 5   | Locate the **"Select Locations"** panel header                                                                                 | Header reads: **"拠点を選択"**                                                                                                            |           |
| 6   | Locate the **"Selected Locations"** indicator                                                                                  | Label reads: **"選択中の拠点"**                                                                                                           |           |
| 7   | On the Academic Calendar related list in the Academic Year page, locate the **"Remarks"** column header                        | Column header reads: **"備考"**                                                                                                           |           |
| 8   | Observe the error message when attempting to delete an ACM that has existing ACIs                                              | Error message reads: **"作成済の個別年度カレンダーがある場合、マスタ年度カレンダーは削除できません。"**                                   |           |

**Severity:** minor
**Priority:** medium

---

### Academic Calendar – UI Translation – Skipped Messages – Confirmed Out of Scope for This Epic

**Description:** Translation review — Documents two messages that were agreed with PdM and TL to be **skipped** (not translated / not implemented) in this epic.

**Preconditions:**

- Logged in as HQ Admin (Japanese)
- Refer to LT-91348 for the skipped translations

| #   | Action                                                                       | Expected Result                                                                                                           | Test Data                      |
| --- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| 1   | Attempt to change the location on an existing ACM (if the field is editable) | Note: Message **"年度カレンダーの拠点は変更できません。"** is skipped — this restriction was not implemented in this epic | Skip (aligned with PdM and TL) |
| 2   | Attempt to set a location on an ACM (Master AC cannot have a location)       | Note: Message **"マスターカレンダーの拠点は設定できません。"** is skipped — not implemented in this epic                  | Skip (aligned with PdM and TL) |

**Severity:** trivial
**Priority:** low

---

### Academic Calendar – Data Migration – Existing Records Preserved After Feature Deployment

**Description:** Data Migration — Confirms that existing Academic Calendar records created before this feature was deployed are preserved and correctly accessible after deployment. No data loss or corruption should occur.

**Preconditions:**

- The org has **pre-existing** Academic Calendar records (created before `Enable_Enhance_Academic_Calendar` was enabled)
- Logged in as HQ Admin

| #   | Action                                                                                        | Expected Result                                                                                                                                    | Test Data |
| --- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the Academic Year record page for a year that had an existing AC before migration | The Academic Calendar related list shows the pre-existing AC record(s)                                                                             |           |
| 2   | Open a pre-existing AC record                                                                 | All fields (name, terms, weeks, closed dates) are intact and readable                                                                              |           |
| 3   | Check whether pre-existing ACs are flagged correctly (master vs individual)                   | Pre-existing records that were linked to locations should appear as Individual ACs; pre-existing records not linked to a location appear as Master |           |
| 4   | Confirm no data has been duplicated or corrupted                                              | Record count and field values match the state before migration                                                                                     |           |
| 5   | Log in as a CM and check that their pre-existing AC is still accessible in their location     | CM can still view and edit their pre-existing AC                                                                                                   |           |

**Severity:** critical
**Priority:** high
