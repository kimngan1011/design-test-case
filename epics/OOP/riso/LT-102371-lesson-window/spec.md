---
ticket_id: LT-102371
ticket_url: https://manabie.atlassian.net/browse/LT-102371
prd_url: https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2604597491/PRD+Riso+OOP+Lesson+Window
pbt_ticket: PBT-3051
figma_url: https://www.figma.com/design/PQ0TNOtuOiqlvJrYdcHHVG/Lesson-Master-and-Mana-Calendar?node-id=13267-63959&t=TADbluXRlzgeSnJX-4
title: "[Riso] OOP | Lesson Window"
module: scheduling
bucket: OOP/riso
status: In Progress
internal_uat_date: 2026-06-15
production_release_date: 2026-08-10
prd_status: Done
prd_owner: Angelica Abu
last_updated: 2026-07-14
---

# LT-102371: [Riso] OOP | Lesson Window

## Summary

This feature introduces a **Location Lesson Window (LLW)** (`Location_Lesson_Window__c`) object in Salesforce for Riso partner. An LLW is a closure record for a specific location-period combination. CMs create LLWs and mark them **Complete** to signal that a month's lessons are finalized. Once a LLW is marked **Complete**, new lesson creation **and** lesson date updates are blocked for that location within the closed date range. CMs and HQ can **reopen** a Complete LLW (subject to time restrictions). Riso's external system retrieves closure data nightly via a GET API.

**Out of scope:** Standalone `Lesson_Window__c` object (not needed — `Location_Lesson_Window__c` is the only new object), lesson status management, timesheet calculation.

---

## Data Model — `Location_Lesson_Window__c`

| Field | API Name | Type | Notes |
|---|---|---|---|
| Academic Year | `Academic_Year__c` | Lookup (Academic Year) | Required. Scopes uniqueness. Read-only on edit. |
| Location | `Location__c` | Lookup (Account) | Required. Location this window applies to. |
| Month | _(picklist)_ | Month dropdown | Drives auto-population of Start/End Date. Default = current month. Disabled when Academic Year is cleared. |
| Start Date | `Start_Date__c` | Date | Required. Auto-populated from Month + Academic Year. Manually editable. |
| End Date | `End_Date__c` | Date | Required. Auto-populated as last day of the month. Manually editable. |
| Status | `Status__c` | Picklist | Options: `Open` (default) / `Complete`. |
| Created Date | `CreatedDate` | DateTime (SF system) | Standard SF field. Read-only. |
| Last Modified Date | `LastModifiedDate` | DateTime (SF system) | Standard SF field. Read-only. |
| Last Modified By | `LastModifiedById` | Lookup (User, SF system) | Standard SF field. Read-only. |

---

## Acceptance Criteria

### US-01: Create and Manage Location Lesson Window

**AC-01.1 — Create LLW from Account detail page (Path A)**
- Add a new **Lesson Window tab** on the Account detail page.
- The tab lists all `Location_Lesson_Window__c` records for that location, showing: Academic Year, Start Date, End Date, Status, Last Modified Date, Last Modified By.
- **New button**: Opens a creation form.
  - Auto-fills: Academic Year = current academic year; Status = Open; Location = current location (non-editable).
  - Month dropdown defaults to current month. Selecting a Month auto-populates Start Date and End Date from the Academic Year's calendar range. User can manually override after auto-population.
  - End Date auto-populates when Start Date is entered.
- **Delete button**: Visible only on records where Status = **Open**. Follows Salesforce standard data dependency behavior (blocked if linked detail records exist). Available to **staff with `full_access_v2` PS only** (CM without this PS cannot see the Delete button).
- **Status toggle / Complete action**: Available inline or via record action. Sets Status = Complete.
- **Reopen action**: Sets Status = Open. Subject to restrictions in AC-06, AC-07, AC-08.

**AC-01.2 — Create LLW from LLW List View (Path B)**
- From the Location Lesson Window list view, a **New button** opens the same creation form but with a **multi-select Location field**.
- On save: create LLW for each selected location. If one location has an overlapping LLW, that location is **skipped**; other locations proceed normally.
- Available to CM (for their locations) and HQ (for all locations).
- Reuses the same popup, validation, and auto-population logic as Path A.
- The List View does **not** include Complete or Reopen actions (Salesforce standard limitation).
- The Location column must render as a **clickable link** so CM can navigate to the Location detail → Lesson Window tab to manage status.

**AC-02 — Uniqueness validation**
- If a LLW already exists for the same Location + Academic Year and the date range **overlaps** with an existing record, block creation and display:
  - EN: `"A Lesson Window already exists for this location and period."`
  - JA: `"この期間のレコードは既に存在します。"`

**AC-03 — LBAC enforcement**
- A CM can only create, view, and manage LLW records for locations they are assigned to.
- Attempting to access or create a LLW for a different location is blocked by LBAC.

**AC-04 — Complete action**
- Any authorized user (Admin / HQ / CM) can set a LLW to **Complete** at any point, regardless of the current date or lesson content.
- No additional validation is required at the time of completing (v1).

**AC-05 — Delete restriction**
- The Delete action is only available on records where Status = **Open**.
- If the LLW has linked detail records, Salesforce standard data dependency behavior applies (deletion blocked).
- **Staff with `full_access_v2` PS only.** CM without this PS cannot delete.

---

### US-02: Reopen a Complete Location Lesson Window

**AC-06 — CM reopen — allowed months**
- A CM can set a Complete LLW back to **Open** only if the LLW's month is the **current calendar month** or the **immediately preceding calendar month**.
- On success: Status = Open; lesson creation in that date range is unblocked immediately (no cache/delay).

**AC-07 — CM reopen — blocked months**
- If the LLW's month is **older than one month prior**, the CM's reopen attempt is blocked.
- Error message:
  - EN: `"This window can no longer be reopened. Please contact HQ."`
  - JA: `"未完了状態に戻すことはできません。本部に連絡してください。"`

**AC-08 — HQ / Admin reopen**
- HQ and Admin can reopen **any** Complete LLW regardless of how old the month is. No restriction.

---

### US-03: Lesson Creation Blocked in Closed Window

**AC-09 — Validation on lesson creation and date update — all paths**
- When a user **creates** a new lesson OR **updates** `Lesson_Date__c` on an existing lesson, and the date falls within `Start_Date__c` and `End_Date__c` of a **Complete** LLW for the **same location AND same Academic Year** → the save is **blocked**.
- A Complete LLW for the same location but a **different Academic Year** does **not** block lesson creation.
- Applies to **all** lesson creation and date-change paths:
  1. SF Lesson List
  2. Lesson Schedule detail page
  3. SF Calendar (including **drag-and-drop** to a new date)
  4. Lesson Schedule CSV import
  5. Recurring lesson creation
- Also applies to **lesson date updates** when `Lesson_Date__c` is changed on an existing lesson (via Edit form or DnD).
- **Note:** ACI closed-date validation silently **skips** lesson creation (no error shown); LLW validation shows an explicit **error message**. The two mechanisms behave differently and do not conflict.

**AC-10 — Error message**
- EN: `"Selected lesson date is already closed."`
- JA: `"選択された授業期間は既に完了済です"`
- Message appears inline on the creation form or as a system error depending on the creation path.

**AC-11 — Other lesson fields not restricted by LLW**
- LLW does **not** block editing of other lesson fields (teacher, student, time, etc.).
- Only `Lesson_Date__c` changes to a date within a Complete LLW range are blocked.

**AC-12 — Lesson date update — validation**
- If a lesson's date is updated after creation, LLW validation fires on the new date.
- If the new date falls within a Complete LLW for the same location → update is blocked with the same error (AC-10).

**AC-13 — Unblocked after reopen**
- If a Complete LLW is set back to Open (US-02), lessons can be created in that date range again **immediately**. No cache or delay.

---

### US-04: GET API for External System

**AC-14 — API availability**
- A GET endpoint is available for Riso's external system to retrieve `Location_Lesson_Window__c` records.
- Endpoint path and authentication method: **to be confirmed with tech**.

**AC-15 — Response content**
- Each record in the response includes: Location ID, Location Name, Academic Year, Start Date, End Date, Status, Last Modified Date, Last Modified By.

**AC-16 / AC-17 — Sample request / response** — TBC with tech.

**AC-18 — Authentication**
- Follows standard Riso-Manabie API authentication. Exact auth method to be confirmed with tech.

**AC-19 — Nightly call support**
- Supports nightly batch calls. No rate limit issues expected. Frequency may increase at end of month.

---

### US-05: Edit LLW

**AC-20 — Edit LLW**
- A user can edit an existing LLW only when Status = **Open** (or after Reopen).
- Editable fields when Status = Open: Start Date, End Date, Month, Status.
- **Academic Year is read-only** on edit. User must create a new LLW to change Academic Year.
- Once Status = Complete → record is read-only (Standard Salesforce inline edit or Edit button).
- Validation rules (overlap, academic year scoping) fire on save.

**AC-21 — Edit dates then mark Complete**
- When user updates Start Date or End Date and then marks Complete → the new duration locks lessons within the new scope.

---

## Permissions & LBAC — `Location_Lesson_Window__c`

LBAC is applied at **two independent layers** for this new object.

### Layer 1 — Object-level permissions (Profile / Permission Set)

| Operation | User with `full_access_v2` PS | CM (no `full_access_v2` PS) | BO Teacher |
|---|---|---|---|
| Create | ✅ | ✅ | ❌ |
| Read | ✅ | ✅ | ❌ |
| Update (fields + status) | ✅ | ✅ (with BR-03 reopen restriction) | ❌ |
| Delete | ✅ | ❌ | ❌ |

- **Delete permission gate:** `full_access_v2` Permission Set. Staff with this PS can delete LLW; CM without it cannot.
- BO Teacher has **no object visibility** — cannot see, create, or interact with LLW in any way.
- Riso-specific: all permissions gated to Riso org/package only. No impact to other partners.

### Layer 2 — Record-level sharing (OWD + `Sharing_Setting__c`)

- OWD for `Location_Lesson_Window__c` must be set to **Private** (CM cannot see records outside their location).
- `Sharing_Setting__c` (existing sharing rules mechanism) must be extended to cover `Location_Lesson_Window__c`, granting each CM access to records where `Location__c` ∈ their assigned location(s).
- **Tech dependency (from PRD NFR-02):** Verify with tech whether the existing `Sharing_Setting__c` configuration can cover the new object with a new entry, or whether a new sharing rule/configuration is required. This must be confirmed before release.
- HQ and Admin: see **all** LLW records across all locations (no sharing restriction).

### LBAC enforcement summary

| User | Object access | Records visible |
|---|---|---|
| Staff with `full_access_v2` PS | Full CRUD (incl. Delete) | All locations |
| CM (no `full_access_v2` PS) | Create / Read / Update (with BR-03 reopen restriction) | Own location(s) only |
| BO Teacher | None | None |

---

## Business Rules (from PRD)

| BR | Description | Platform |
|---|---|---|
| BR-01 | **Uniqueness**: No two LLW records for the same Location + Academic Year may have overlapping date ranges. Trigger on before-insert and before-update. Error: "A Lesson Window already exists for this location and period." | [SF] |
| BR-02 | **Lesson creation/update block**: When `Lesson_Date__c` is set (on creation **or update**) to a date within `Start_Date__c`–`End_Date__c` of any LLW with **Status = Complete** for the **same location AND same Academic Year** → operation is blocked. Fires on `Lesson__c` before-insert and before-update. A Complete LLW for a different Academic Year does not block lesson creation. | [SF] |
| BR-03 | **CM reopen restriction**: CM can set Complete → Open only if LLW's month = current or immediately preceding calendar month. Older months cannot be reopened by CM. | [SF] |
| BR-04 | **Audit trail**: Handled by SF standard system fields (`CreatedById`, `CreatedDate`, `LastModifiedById`, `LastModifiedDate`). No custom audit fields required. | [SF] |
| BR-05 | **LBAC scope — record level**: LLW records follow `Sharing_Setting__c` pattern. OWD = Private. CM can only see and manage LLW records for their assigned location(s). HQ/Admin see all. | [SF] |
| BR-06 | **Lesson date update also blocked**: Same LLW validation (BR-02) fires when `Lesson_Date__c` is changed on an existing lesson. | [SF] |
| BR-07 | **Complete action**: User can set LLW to Complete at any time. No date or content validation required at completion (v1). | [SF] |
| BR-09 | **Delete restriction**: LLW can only be deleted if Status = **Open** AND no linked detail records exist. Salesforce standard data dependency behavior applies. | [SF] |
| BR-10 | **Academic Year scoping**: Uniqueness is scoped per Location + Academic Year. The same date range may exist for the same location under a **different academic year** without conflict. | [SF] |
| BR-11a | **Month-to-date mapping**: Academic Year defaults to current; mandatory. If Academic Year cleared → Month dropdown, Start Date, End Date are **disabled**. When Month selected → Start Date and End Date auto-populate from the Academic Year's calendar range. User can manually override after auto-population. | [SF] |
| BR-11b | **Edit restriction**: LLW fields (Academic Year, Month, Start Date, End Date) are editable only when Status = Open. Complete LLWs are read-only except via the Reopen action. Academic Year is always read-only on edit. | [SF] |
| BR-CRUD | **CRUD permissions**: Create: all staff (Admin/HQ/CM). Read: all staff. Update: all staff (CM with BR-03 reopen restriction). Delete: **staff with `full_access_v2` PS only** (CM without this PS cannot delete). All subject to LBAC (both object + record level). | [SF] |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [CONFLICT — RESOLVED by PRD] | Jira SR-03 vs PRD BR-CRUD / AC-05 | Jira description says "for CM to create/delete LLW." PRD resolves: Delete = Admin/HQ only. CM has NO delete access. Account detail page Delete button must NOT be shown to CM. |
| 2 | [CONFLICT — RESOLVED] | AC-09/AC-12 vs existing DnD behavior | **Resolved (2026-07-14):** DnD IS blocked by LLW. LLW blocks ALL create and edit lesson flows including DnD on SF Calendar. This is intentional divergence from ACI behavior (ACI silently skips, LLW shows error). |
| 3 | [CONFLICT] | BR-11a: Academic Year required | Academic Year is mandatory and defaults to current. If no Academic Year exists for the current period (org data setup missing), the creation form would be non-functional. No fallback defined in PRD. |

### Gaps Resolved by PRD

| # | Was a gap | PRD Answer |
|---|---|---|
| A | How does LLW get date range? | Academic Year (required) + Month dropdown. Month auto-populates Start/End Date. Manual override allowed. |
| B | All 6 lesson creation paths? | YES — AC-09 covers all 5 paths + lesson date updates. |
| C | Edit existing lesson date blocked? | YES — BR-06 + AC-12 confirm. |
| D | CM can delete? | NO — Delete = HQ/Admin only (AC-05, BR-CRUD). |
| E | Lessons unblocked after reopen? | YES — immediately (AC-13). |
| F | What fields CM can update on LLW? | Start Date, End Date, Month, Status (when Open). Academic Year = read-only always on edit. |
| G | GET API response fields? | Location ID, Location Name, Academic Year, Start Date, End Date, Status, Last Modified Date, Last Modified By (AC-15). |

### Gaps Resolved by Clarification (2026-07-14)

| # | Question | Answer |
|---|---|---|
| Q1 | DnD on SF Calendar — blocked or allowed? | **Blocked.** LLW blocks ALL create/edit lesson flows including DnD. |
| Q2 | LLW vs ACI validation interaction | **Different behaviors, no conflict.** LLW shows explicit error message. ACI silently skips lesson creation (no error). They can coexist. |
| Q4 | Retroactive LLW with Start_Date in the past | **Blocked.** Any lesson creation/date update where lesson date falls in a Complete LLW range is blocked, regardless of whether the LLW was created retroactively. Existing lessons are unaffected. |
| Q5 | Bulk creation skip UX (Path B) | **Skip silently** — no special feedback/summary required. Locations with overlap are skipped; the rest are created. |
| Q6 | GET API tech spec | **Follow PRD.** Test against AC-14/AC-15 response fields. No additional Swagger needed for test design. |

### Remaining Gaps

| # | Tag | Description |
|---|---|---|
| 1 | [MISSING BEHAVIOR — PENDING] | Recurring lesson chain with partial LLW overlap: create valid occurrences only, or block the entire batch? _(Reply pending from PM)_ |

### Lesson-Learned Risks

| # | Incident | Date | Risk | Guardrail |
|---|---|---|---|---|
| 1 | Dual-path validation (Aso duplicate sessions) | 2026-04-13 | LLW validation (BR-02, new trigger) + ACI closed-date validation (existing) both fire on `Lesson__c` before-insert/before-update. **RESOLVED 2026-07-14:** LLW shows error message; ACI silently skips (no error shown). Different behaviors — no simultaneous error risk. | Test both independently on the same lesson date to confirm they don't interfere. |

### E2E Scenario Impact

| Scenario | Impact | Action |
|---|---|---|
| E2E-01: Lesson Lifecycle — Create, Teach, Report, View | Create lesson step can be blocked if test location has a Complete LLW covering the test date. Preconditions must ensure no Complete LLW covers test lesson date/location. | UPDATE |
| E2E-02: Recurring Lesson — Create, Edit Chain, Delete, Calendar DnD | Recurring creation and DnD may be blocked by LLW. Preconditions need LLW-awareness. | UPDATE |
| E2E-LLW-01 (NEW) | Full LLW lifecycle: Create LLW → Complete → lesson creation blocked → Reopen → lesson creation succeeds → CM tries to reopen old LLW (blocked) → HQ reopens old LLW (success). | CREATE |

---

## Clarification Questions

> ✅ = answered · ⏳ = pending

1. ✅ **[RESOLVED — DnD behavior]** Does DnD on SF Calendar trigger LLW validation?
   → **Yes. LLW blocks ALL create/edit lesson flows including DnD.**

2. ✅ **[RESOLVED — LLW vs ACI interaction]** Which validation runs first? Can both errors show simultaneously?
   → **LLW shows an error message. ACI silently skips lesson creation (no error). Different behaviors — no conflict, no simultaneous error.**

3. ⏳ **[PENDING — Recurring partial overlap]** For a recurring lesson chain where SOME dates fall in a Complete LLW and others do not: create valid occurrences only, or block the entire batch?
   → _Reply pending from PM._

4. ✅ **[RESOLVED — Retroactive LLW]** If LLW is created with Start_Date in the past, does it block new creation for that date range?
   → **Yes — any lesson creation/date update where lesson date falls in the Complete LLW range is blocked, regardless of when the LLW was created. Existing lessons already created are unaffected.**

5. ✅ **[RESOLVED — Bulk creation skip UX]** What feedback is shown when locations are skipped in Path B?
   → **Just skip silently — no special feedback or summary required.**

6. ✅ **[RESOLVED — GET API spec]** Is there a Swagger doc available?
   → **Test cases follow PRD (AC-15 response fields). No additional tech doc needed for test design.**

---

## Localization (Japanese — ja-JP)

| Context | EN | JA |
|---|---|---|
| Object label | Location Lesson Window | 拠点別授業完了期間 |
| Field: Academic Year | Academic Year | 年度 |
| Field: Location | Location | 拠点 |
| Field: Start Date | Start Date | 開始日 |
| Field: End Date | End Date | 終了日 |
| Field: Status | Status | ステータス |
| Picklist: Open | Open | 未完了 |
| Picklist: Complete | Complete | 完了 |
| Tab label | Lesson Window | 授業完了期間 |
| Validation error (overlap) | A Lesson Window already exists for this location and period. | この期間のレコードは既に存在します。 |
| Lesson creation error | Selected lesson date is already closed. | 選択された授業期間は既に完了済です |
| Reopen blocked (CM) | This window can no longer be reopened. Please contact HQ. | 未完了状態に戻すことはできません。本部に連絡してください。 |

---

## Related Specs

- `epics/calendar/LT-98532-bulk-publish-lessons-by-student/spec.md` — Riso Bulk Publish: existing Riso lesson lifecycle feature.

## Related Test Cases

- `epics/calendar/LT-98532-bulk-publish-lessons-by-student/test-cases/bulk-action-monitoring.md`
- `epics/calendar/LT-98532-bulk-publish-lessons-by-student/test-cases/bulk-publish-modal.md`

## QASE Coverage Gaps

**LLW CRUD (Account page — Path A):**
- AC-01.1: New button, auto-fill fields, Month auto-populate Start/End Date, manual override
- AC-04: Complete action (any time, no content validation)
- AC-05: Delete restriction (Status=Open only, HQ/Admin only)
- AC-20: Edit LLW (Status=Open only; Academic Year read-only; validation on save)
- AC-21: Edit dates → mark Complete → new scope locks lessons

**LLW List View (Path B):**
- AC-01.2: Multi-location selection, skip on overlap, clickable location link, no Complete/Reopen in list

**Uniqueness:**
- AC-02: Overlap → error message (EN + JA)
- BR-10: Same date range allowed under different Academic Year

**Reopen:**
- AC-06: CM reopen current/prior month → success + immediate unblock
- AC-07: CM reopen older month → blocked + error message (EN + JA)
- AC-08: HQ/Admin reopen any window → success

**LBAC — Object-level permissions:**
- All staff (Admin/HQ/CM) can see the object; BO Teacher has no access
- CM **without `full_access_v2` PS** cannot delete (object permission)
- Delete button not rendered for CM without `full_access_v2` PS on Account detail page

**LBAC — Record-level sharing:**
- AC-03: CM can only see/manage LLW records for their assigned location(s)
- CM cannot view or access LLW records for other locations
- HQ/Admin can see all LLW records across all locations
- OWD = Private: CM at Location A cannot see LLW records of Location B

**Lesson Validation:**
- AC-09: Creation blocked on all 5 paths when date in Complete LLW
- AC-10: Error message (EN + JA)
- AC-12: Lesson date update blocked when new date in Complete LLW
- AC-11: Other lesson fields remain editable (LLW does not block)
- AC-13: Lesson creation unblocked immediately after LLW reopen

**GET API:**
- AC-14/AC-15: Endpoint returns correct fields
- AC-19: Supports nightly batch call

**Localization:**
- All 12 Japanese strings verified in UI
