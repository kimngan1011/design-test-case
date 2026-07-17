# Test Cases: LT-102371 — [Riso] OOP | Lesson Window

## Suite: [Riso] LLW – Localization & Non-Functional

---

### [Riso] Location Lesson Window – Localization – Object Label – Japanese text shown in UI

**Description:** Localization — Component — The Location Lesson Window object label is displayed in Japanese as "拠点別授業完了期間" in the Riso Salesforce org (ja-JP locale).

**Preconditions:**
- Riso Salesforce org is set to Japanese locale (ja-JP)
- Logged in as HQ or CM Staff

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Salesforce object list or any screen that shows the object name | The object is labeled **"拠点別授業完了期間"** (not "Location Lesson Window") | expected_ja_label = "拠点別授業完了期間" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Localization – Tab Label on Account Page – Japanese text shown

**Description:** Localization — Component — The Lesson Window tab on the Account detail page is labeled "授業完了期間" in Japanese locale.

**Preconditions:**
- Riso Salesforce org is set to Japanese locale (ja-JP)
- Navigate to an Account detail page

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to an Account detail page and observe the tabs | A tab labeled **"授業完了期間"** is visible (Japanese for "Lesson Window") | expected_tab_ja = "授業完了期間" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Localization – Field Labels – All field labels shown in Japanese

**Description:** Localization — Component — All LLW field labels are shown in Japanese in the Riso SF org (ja-JP locale).

**Preconditions:**
- Riso Salesforce org is set to Japanese locale (ja-JP)
- Navigate to an LLW record detail or creation form

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open an LLW record and observe the field labels | The following Japanese labels are shown: Academic Year = **"年度"**, Location = **"拠点"**, Start Date = **"開始日"**, End Date = **"終了日"**, Status = **"ステータス"** | expected_labels = {Academic Year: "年度", Location: "拠点", Start Date: "開始日", End Date: "終了日", Status: "ステータス"} |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Localization – Status Picklist – Open value shown as "未完了"

**Description:** Localization — Component — The Status picklist value "Open" is displayed as "未完了" in the Japanese locale.

**Preconditions:**
- Riso Salesforce org is set to Japanese locale (ja-JP)
- An LLW record with Status = Open exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to an LLW record with Status = Open | Record detail page is shown | — |
| 2 | Observe the **Status** field value | Status displays as **"未完了"** (not "Open") | expected_ja_open = "未完了" |
| 3 | Open the creation form and expand the Status dropdown | "未完了" appears as the first/default option | — |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Localization – Status Picklist – Complete value shown as "完了"

**Description:** Localization — Component — The Status picklist value "Complete" is displayed as "完了" in the Japanese locale.

**Preconditions:**
- Riso Salesforce org is set to Japanese locale (ja-JP)
- An LLW record with Status = Complete exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to an LLW record with Status = Complete | Record detail page is shown | — |
| 2 | Observe the **Status** field value | Status displays as **"完了"** (not "Complete") | expected_ja_complete = "完了" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Localization – Uniqueness Validation Error – Japanese message shown

**Description:** AC-02, Localization — Component — When an LLW creation is blocked due to an overlapping date range, the Japanese error message is shown in the ja-JP locale.

**Preconditions:**
- Riso Salesforce org is set to Japanese locale (ja-JP)
- Existing Complete LLW: Location A, AY = 2026, July 2026 (2026-07-01–2026-07-31)
- Attempt to create a new overlapping LLW for Location A, AY = 2026, July 2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Fill in the LLW creation form: Location A, AY = 2026, Start = 2026-07-10, End = 2026-07-31 | Form filled | — |
| 2 | Click **Save** | Save is blocked | — |
| 3 | Observe the error message | Error text is exactly: **"この期間のレコードは既に存在します。"** | expected_ja_error = "この期間のレコードは既に存在します。" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson Creation – LLW Validation – Localization – Blocked Lesson Error Message in Japanese

**Description:** AC-10, Localization — Component — When lesson creation is blocked by a Complete LLW, the Japanese error message is shown in the ja-JP locale.

**Preconditions:**
- Riso Salesforce org is set to Japanese locale (ja-JP)
- Complete LLW: Location A, July 2026, Status = Complete
- Attempt to create a lesson on 2026-07-15 for Location A

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a lesson: Location A, Lesson Date = 2026-07-15 and click **Save** | Save is blocked | lesson_date = 2026-07-15 |
| 2 | Observe the error message in Japanese | Error text is exactly: **"選択された授業期間は既に完了済です"** | expected_ja = "選択された授業期間は既に完了済です" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Localization – CM Reopen Blocked Error – Japanese message shown

**Description:** AC-07, Localization — Component — When a CM's reopen attempt is blocked (LLW older than 1 month), the Japanese error message is shown in the ja-JP locale.

**Preconditions:**
- Riso Salesforce org is set to Japanese locale (ja-JP)
- Logged in as CM Staff
- Complete LLW for May 2026 (2 months ago), Status = Complete

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Attempt to reopen the May 2026 Complete LLW | Reopen blocked | today = 2026-07-14; llw_month = May 2026 |
| 2 | Observe the error message in Japanese | Error text is exactly: **"未完了状態に戻すことはできません。本部に連絡してください。"** | expected_ja = "未完了状態に戻すことはできません。本部に連絡してください。" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – NFR-05 – Riso Org Isolation – Other Partner Org Cannot Access LLW Object

**Description:** NFR-05 — Permission Matrix — The Location Lesson Window feature is Riso-specific. Users from other partner orgs (e.g., Aso, Koyu) cannot see or access the LLW object.

**Preconditions:**
- A test user exists in a **non-Riso partner org** (e.g., Aso or a generic Manabie org)
- LLW records exist in the Riso org

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Log in as a user from the non-Riso partner org | Logged in successfully | partner = non-Riso |
| 2 | Navigate to the Account detail page for any location | Page loads | — |
| 3 | Observe whether a **Lesson Window** tab is visible | **No Lesson Window tab** is visible (feature is Riso-specific) | — |
| 4 | Attempt to access the LLW object via search or direct URL | Object is not accessible | — |
| 5 | Confirm no LLW records from the Riso org are exposed | No data leakage between orgs | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – NFR-02 – LBAC – CM at Location A Cannot View Location B Records via List View

**Description:** NFR-02, BR-05 — Permission Matrix — A CM assigned only to Location A cannot see Location B's LLW records in the LLW List View, confirming Sharing_Setting__c record-level control is effective.

**Preconditions:**
- CM Staff user is assigned to **Location A only** (not Location B)
- LLW records exist for both Location A (Status = Open) and Location B (Status = Complete)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Logged in as CM Staff (assigned to Location A only) | Logged in | — |
| 2 | Navigate to the Location Lesson Window list view | List view opens | — |
| 3 | Observe all records in the list view | Only Location A's LLW records are visible; **Location B records are not shown** | — |
| 4 | Count total records visible | Only records for Location A appear | expected_count = count(Location A records only) |
| 5 | Attempt to navigate directly to a Location B LLW record URL | Access is **denied** or "record not found" | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – NFR-02 – LBAC – Sharing_Setting__c Config – HQ Sees All Records Across All Locations

**Description:** NFR-02, BR-05 — Permission Matrix — HQ Staff can view all LLW records across all locations, confirming the Sharing_Setting__c configuration does not restrict HQ access.

**Preconditions:**
- Logged in as **HQ Staff** to the Riso Salesforce org
- LLW records exist for Location A, Location B, Location C (multiple locations)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Location Lesson Window list view | List view opens | — |
| 2 | Observe all records in the list | LLW records for **all locations** (A, B, C) are visible | expected_locations = [A, B, C] |
| 3 | Open an LLW record for Location C | Record opens without access error | — |
| 4 | Confirm HQ can manage (edit, change status) any LLW record regardless of location | Management actions are available | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Non-Functional – Audit Trail – Last Modified By Updated on Status Change

**Description:** NFR-01, BR-04 — Component — When a user changes the LLW Status (e.g., to Complete or reopened), the Last Modified By field is updated to reflect the user who made the change.

**Preconditions:**
- Logged in as **HQ Staff** (user: "Test HQ User") to the Riso Salesforce org
- LLW exists: Location A, July 2026, Status = Open
- Last Modified By = some previous user

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Mark the LLW as **Complete** while logged in as Test HQ User | Status changes to Complete | actor = Test HQ User |
| 2 | Observe the **Last Modified By** field | Last Modified By = **"Test HQ User"** (updated to the user who changed the status) | — |
| 3 | Observe the **Last Modified Date** | Last Modified Date = today's date and current time | expected_date = 2026-07-14 |
| 4 | Confirm these fields are read-only (cannot be edited manually) | Fields are locked / read-only | — |

**Severity:** trivial
**Priority:** low

---

### [Riso] Location Lesson Window – Non-Functional – Edit Restriction – Complete LLW Fields Are Read-Only via API

**Description:** NFR-03, BR-11b — Negative — Attempting to update LLW field values (Start Date, End Date) via the Salesforce API on a Complete LLW is blocked by the trigger/validation rule.

**Preconditions:**
- LLW record: Location A, July 2026, Status = **Complete**
- API access is available (developer console or REST API)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Via the Salesforce API, attempt to update the Start Date of the Complete LLW to **2026-07-05** | API update request sent | new_start = 2026-07-05 |
| 2 | Observe the API response | Update is **rejected** by the Apex trigger/validation rule | — |
| 3 | Confirm the Start Date remains **2026-07-01** (unchanged) | Record is not modified | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Non-Functional – Performance – Lesson List Page Loads Without Delay After LLW Complete

**Description:** NFR — Regression — After marking an LLW as Complete, the Lesson List page for that location loads normally without noticeable performance degradation.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- At least 100 lessons exist for Location A in July 2026
- Mark the LLW for Location A, July 2026 as Complete

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Mark the LLW (Location A, July 2026) as **Complete** | Status = Complete | lesson_count = 100+ |
| 2 | Navigate to the SF Lesson List and filter by Location A | Lesson list loads | — |
| 3 | Observe page load time | Page loads within acceptable time (no significant delay compared to before LLW was completed) | — |
| 4 | Confirm all existing lessons are still listed (LLW Complete does not hide or delete existing lessons) | All 100+ lessons are still visible | — |

**Severity:** minor
**Priority:** medium
