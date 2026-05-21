# LT-87693: Academic Calendar Closed Date per Location

**ID:** https://manabie.atlassian.net/browse/LT-87693
**Status:** Done
**Analysis Date:** 2026-05-18
**Partner Scope:** Core (all partners — no tenant restriction)
**Priority:** Medium
**Epic Type:** Epic
**Feature Flag:** `Lesson_Custom_Setting__c.Enable_Enhance_Academic_Calendar`
**PRD:** [SF – Academic Calendar and Closed Date improvement](https://manabie.atlassian.net/wiki/spaces/ERP/pages/1826848769)
**DS Notes:** [Academic Calendar and Location Closed Days](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/1349582903/DSnotes#Academic-Calendar-and-Location-Closed-Days)
**Assignee:** Pham Van Loi

---

## Summary

LT-87693 redesigns the Academic Calendar system to support a **centralized Master + decentralized Individual** model. Previously, each location could only have one Academic Calendar and every setup had to be done per location independently; only Admins could update it.

This epic introduces:

1. **Master Academic Calendar (ACM)** — HQ creates one ACM per Academic Year, sets up all terms, weeks, and Closed Dates, then bulk-applies it to all or selected locations. Each location receives a cloned **Individual Academic Calendar (ACI)**.
2. **Local Customization by CM** — Each Center Manager can edit their own ACI (terms, weeks, closed dates) without affecting the ACM or other locations.
3. **Multi-year Accumulation** — Locations now support multiple ACIs across years (1 location : n ACs); new AYs accumulate rather than overwrite.
4. **Permission Separation** — HQ controls the ACM; CMs control only their affiliated ACI. The "Apply to location" action is hidden from ACI views.
5. **Cross-platform Visibility** — Closed Dates stored under each location's ACI are surfaced in SF Calendar, Back Office Calendar, and Learner App Calendar via the location traversal path.

**Key data structure changes:**

- New Lookup field `Location__c` on Academic Calendar object (replaces the old 1:1 `Academic_Calendar__c` on Account/Location)
- New related list on Academic Year record page (shows ACM + each location's ACI)
- New related list on Location record page (shows all ACIs across AYs)
- Permission sets: `View Academic Calendar`, `Edit Academic Calendar`, `Edit Academic Calendar for location`, `Edit Master Academic Calendar - New`

---

## Acceptance Criteria

### US 01 — HQ creates and deploys Master Academic Calendar

#### AC 01.1 — Create Academic Calendar Master

- Only ACs created via the Salesforce UI are treated as ACM; they are flagged as `Master` upon creation
- ACM **cannot** be associated with any Location field
- Each Academic Year can have **at most one** ACM
- When a second ACM is attempted (via **New** or **Clone**) for the same AY, show error:
  > "A Master Academic Calendar already exists for this Academic Year. Please update the existing master or select a different Academic Year."

#### AC 01.2 — Apply Master AC to All or Selected Locations

- New UI panel **"Select Locations"** added to the ACM creation form
- When **"Set as default to all locations"** is **ON** → the Select Locations panel is disabled; all active locations are targeted
- When **"Set as default to all locations"** is **OFF** → user selects specific locations (one/multiple, center-level or brand/parent level)
- **Closed-down locations** are not displayed in the location picker and never receive an ACI
- Applying ACM clones the full AC content (all weeks, all terms) into a new ACI for each selected location
- ACI naming format: `{ACMaster.name}_{Location.name}`
- Exactly **one ACI per location** per application
- If a location already has an ACI for the selected AY → **skip** that location (no overwrite, no error); only locations **without** an existing AC for that AY receive a new ACI

#### AC 01.3 — Associate Closed Dates with Master Calendar

- Closed Dates (CDs) are created directly under the ACM
- When the ACM is applied to locations, every CD on the ACM is **cloned** into each resulting ACI
- CDs added to the ACM **after** the ACM has already been applied to locations are associated with the ACM only — they are **not auto-propagated** to existing ACIs; CMs must manually add them to their ACI if needed

#### AC 01.4 — Restrict Master Calendar Editing (Permission)

- **HQ profiles only** can: create ACM, edit ACM, associate CDs with ACM, apply ACM to locations, delete ACM
- **CM** can view ACM (read-only) but cannot edit or delete it
- **Delete restriction on ACM:** ACM cannot be deleted while any ACI derived from it still exists
  - Error message: "You cannot delete master academic calendar while individual academic calendars exist."
  - `作成済の個別年度カレンダーがある場合、マスタ年度カレンダーは削除できません。`

---

### US 02 — CM edits location-specific Academic Calendar

#### AC 02.1 — Edit Academic Calendar for Assigned Location

- Under the **Academic Year** record page, a new custom Academic Calendar related list is added:
  - Shows the ACM row in **read-only** for CM/Staff; the **Remarks** column displays `"master"` for the ACM row
  - HQ can edit the ACM from this list; CM cannot
  - Shows each CM's own ACI (linked to their affiliated location); CM can edit their ACI from this list
- When CM opens their ACI:
  - CM can edit: name, term names, start date, number of weeks, week order
  - The **"Apply to All Locations"** and **"Apply to Selected Locations"** actions are **hidden** in the ACI UI
  - CM can **delete** their ACI → the location loses its association with that AY's calendar
  - CM **cannot clone** their ACI → attempting to clone shows the same duplicate-ACM error (rule AC 01.1)

#### AC 02.2 — Manage Closed Dates at Location Level

- Location-specific CDs are stored under the location's ACI
- Editing or deleting a CD in an ACI does **not** affect the ACM or other locations' ACIs
- CM can:
  - **Retain** CDs cloned from the ACM
  - **Add** new CDs directly to their ACI
  - **Remove** any CD from their ACI (whether cloned or locally added)

#### AC 02.3 — Restrict AC Visibility to Affiliated Location

- The Academic Calendar list/table view is filtered by the user's location affiliation
- CM sees only ACIs where the Location matches their affiliated location(s); ACIs of other locations are not visible

---

### US 03 — Create new AC at new Academic Year

#### AC 03.1 — Location accumulates ACs across years

- Existing feature retained: user can create new ACM for a new AY and apply to all locations
- **New behavior:** new application **accumulates** (each location gains an additional ACI for the new AY); existing ACIs for prior AYs are not overwritten or removed
- New `Location__c` Lookup field on Academic Calendar object enables 1 Location : n ACs
- Under the **Location** record page: new **Academic Calendar related list** shows all ACIs across all AYs; controlled by permission set `"View Location's AC"`
- Validation: **1 Location : 1 ACI : 1 AY** (uniqueness per location + AY combination still enforced)

---

### US 04 — Calendar Visualization Across Platforms

#### AC 04.1 — SF / Back Office Calendar

- Location Closed Dates are surfaced in the SF/BO Calendar via the traversal:
  **Location + Current AY → Academic Calendar → Closed Date**

#### AC 04.2 — Learner App Calendar

- Location Closed Dates are surfaced in the Learner App via:
  **Enrollment Location → Location + Current AY → Academic Calendar → Closed Date**

---

## Business Rules (Extracted)

| #   | AC Ref  | Business Rule                                                                              | Field                 | Field Behavior       | Platform |
| --- | ------- | ------------------------------------------------------------------------------------------ | --------------------- | -------------------- | -------- |
| 1   | AC 01.1 | Only ACs created via UI are considered ACM; flagged as Master at creation                  | AC Type / Remarks     | read-only flag       | SF       |
| 2   | AC 01.1 | ACM cannot be associated with any Location field                                           | Location\_\_c on AC   | blocked on ACM       | SF       |
| 3   | AC 01.1 | Each AY can have at most one ACM                                                           | Uniqueness constraint | 1 ACM per AY         | SF       |
| 4   | AC 01.1 | Attempting to create/clone a 2nd ACM for same AY → error message                           | Validation            | error shown          | SF       |
| 5   | AC 01.2 | New "Select Locations" panel added to ACM creation form                                    | Select Locations UI   | multi-select input   | SF       |
| 6   | AC 01.2 | "Set as default to all locations" ON → location selector disabled                          | Toggle conditional    | selector disabled    | SF       |
| 7   | AC 01.2 | "Set as default to all locations" OFF → select by center, brand, or org level              | Toggle conditional    | selector active      | SF       |
| 8   | AC 01.2 | Closed-down locations hidden from location picker                                          | Location filter       | closed-down excluded | SF       |
| 9   | AC 01.2 | Applying ACM clones full AC content (weeks, terms) into new ACI per location               | Clone operation       | full content copy    | SF       |
| 10  | AC 01.2 | ACI naming format: `{ACMaster.name}_{Location.name}`                                       | AC Name field         | auto-generated       | SF       |
| 11  | AC 01.2 | Exactly one ACI created per location per apply action                                      | Uniqueness            | 1 ACI per location   | SF       |
| 12  | AC 01.2 | Locations that already have an ACI for the selected AY are skipped (no overwrite)          | Conditional skip      | no duplicate         | SF       |
| 13  | AC 01.2 | Closed-down locations never receive ACI, even with "Set as default" ON                     | Conditional skip      | excluded             | SF       |
| 14  | AC 01.3 | CDs on ACM are cloned into every resulting ACI at time of apply                            | CD clone              | full CD copy         | SF       |
| 15  | AC 01.3 | CDs added to ACM after locations applied are associated with ACM only; not auto-propagated | Conditional CD        | ACM-only after       | SF       |
| 16  | AC 01.4 | HQ only: create, edit, delete ACM and its CDs                                              | Permission            | HQ-restricted        | SF       |
| 17  | AC 01.4 | CM: view ACM read-only; cannot edit or delete                                              | Permission            | view-only for CM     | SF       |
| 18  | AC 01.4 | ACM cannot be deleted while any ACI still exists; shows error message                      | Delete restriction    | blocked with error   | SF       |
| 19  | AC 02.1 | AY page new related list: ACM row (view-only for CM, Remarks = "master") + own ACI rows    | Related list          | role-filtered        | SF       |
| 20  | AC 02.1 | CM can edit their ACI: name, terms, weeks, dates, week order                               | CRUD on ACI           | CM editable          | SF       |
| 21  | AC 02.1 | "Apply to All / Selected Locations" hidden from ACI edit UI                                | Permission / UI       | button hidden        | SF       |
| 22  | AC 02.1 | CM can delete their own ACI; location loses AY calendar association                        | Delete ACI            | CM can delete        | SF       |
| 23  | AC 02.1 | CM cannot clone ACI; shows same duplicate-ACM error                                        | Clone restriction     | blocked              | SF       |
| 24  | AC 02.2 | Location CDs stored under ACI                                                              | CD storage            | per ACI              | SF       |
| 25  | AC 02.2 | Editing/deleting ACI CDs does not affect ACM or other ACIs                                 | Isolation             | no propagation       | SF       |
| 26  | AC 02.2 | CM can retain, add, or remove CDs in their ACI                                             | CD management         | full CRUD for CM     | SF       |
| 27  | AC 02.3 | AC list filtered by user's location affiliation; CM sees only own ACI                      | Visibility filter     | location-scoped      | SF       |
| 28  | AC 03.1 | New Location\_\_c lookup on AC object; 1 Location : n ACs                                  | Object structure      | 1:n relation         | SF       |
| 29  | AC 03.1 | Applying new AY's ACM accumulates ACI per location; no overwrite of prior AY               | Accumulation          | no overwrite         | SF       |
| 30  | AC 03.1 | Location record page: new AC related list + PS "View Location's AC"                        | Related list          | new PS required      | SF       |
| 31  | AC 04.1 | SF/BO Calendar shows CDs via Location + Current AY → AC → Closed Date                      | Data traversal        | location-scoped      | SF/BO    |
| 32  | AC 04.2 | Learner Calendar shows CDs via Enrollment Location → Location + AY → AC → CD               | Data traversal        | learner-scoped       | App      |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| #   | Tag                  | Finding                                                                                                                                                                         | Resolution                                                                                                                                                                                                                               |
| --- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [REGRESSION RISK]    | Existing `Academic_Calendar__c` Lookup on Account (Location) is deprecated and replaced by `Location__c` on Academic Calendar. Any code/report reading the old field may break. | ✅ Per Jira comment (Pham Van Loi 2025-12-16): old field deprecated; page layout on Location updated to remove old field and add new related list. **Test that old field is removed from Location layout; new related list is present.** |
| 2   | [REGRESSION RISK]    | Location-based AC retrieval traversal path changes: previously `Location → AC`, now `Location + AY → AC → CD`. Any BO/Learner calendar code using the old path must be updated. | Document as regression test target for AC 04.1 and AC 04.2                                                                                                                                                                               |
| 3   | [MISSING BEHAVIOR]   | AC 01.2 does not define what happens to ACI names when the ACM name is edited post-apply.                                                                                       | ✅ Inferred from implementation: likely the ACI names are **not** retroactively updated since they were generated at clone time. **Create negative test to confirm: edit ACM name → ACIs retain original names.**                        |
| 4   | [MISSING BEHAVIOR]   | AC 01.2 does not specify the exact scope of "closed-down" — whether it means a specific field value (e.g. `Closed_Down__c = true`) or a specific status.                        | ✅ Inferred from existing system behavior: `Closed Down` is a standard location type in the org. **Precondition: use a location that has been marked as Closed Down in the test org.**                                                   |
| 5   | [UNDOCUMENTED IN AC] | The ACM delete error message content is documented in Jira comments and JP translation tables (LT-91348), not in the formal AC.                                                 | ✅ EN: "You cannot delete master academic calendar while individual academic calendars exist." JP: "作成済の個別年度カレンダーがある場合、マスタ年度カレンダーは削除できません。" — treat as confirmed.                                  |
| 6   | [ROLE GAP]           | AC 01.4 defines HQ and CM roles but does not specify behavior for **Staff** profiles (non-CM, non-HQ-Admin).                                                                    | ⚠️ **Open** — Staff visibility and edit rights not explicitly stated. Infer: same as CM (view-only on ACM, edit own location's ACI). **Flag for dev confirmation if test fails.**                                                        |
| 7   | [MISSING BEHAVIOR]   | AC 04.1/04.2 does not specify what a location calendar shows when **no ACI exists** for the current AY (e.g. the location was closed down or never received an ACI).            | ⚠️ **Open** — no CDs should be shown; confirm no error or broken calendar view.                                                                                                                                                          |
| 8   | [MISSING BEHAVIOR]   | AC 01.2 does not define what happens when the user clicks "Apply" on an already-applied ACM with the same location list (no new locations added).                               | ✅ Inferred from rule 12: no new ACIs are created; operation is a no-op for already-covered locations. **Test explicitly.**                                                                                                              |

### Lesson-Learned Risks

_No directly applicable incidents found in the lesson-learned files._ The feature is new infrastructure.

| Incident                                    | Date       | Reason Not Applicable                                                                                 |
| ------------------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------- |
| Aso — Duplicate Student Sessions            | 2026-04-13 | Different domain (student_session). LT-87693 is calendar/closed-date management, no session creation. |
| Nichibei — Missing LA → Points Not Deducted | 2026-03-04 | Different domain (lesson_allocation/SPO). No financial or allocation logic in LT-87693.               |

### E2E Scenario Impact

| Scenario                     | Title                                                            | Impact                                                                                  | Action                                                              |
| ---------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| E2E (Lesson Calendar)        | Any flow relying on `Location → Academic Calendar → Closed Date` | Traversal path has changed; E2E scenarios reading CDs via the old path may fail         | **UPDATE** E2E to use new path: `Location + AY → ACI → Closed Date` |
| E2E (Academic Calendar CRUD) | Any existing AC create/edit flows                                | ACM concept and form fields are new; old flows may hit the "1 Master per AY" validation | **UPDATE** to use the new form with correct toggle state            |

---

## Clarification Questions

> Posted to Jira: LT-87693 (Jira comment by Kim Ngan Doan Thi, 2025-12-12; test results posted 2025-12-22 and 2025-12-26). Epic is **Done**. Below questions are documentation-only for future test maintenance.

| #   | Tag                | Question                                                                                                                                           | Answer / Status                                                                                                |
| --- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Q1  | [MISSING BEHAVIOR] | When ACM name is edited post-apply, are ACI names retroactively updated?                                                                           | ⚠️ **Not explicitly stated in AC** — infer: ACIs keep their original names. **Verify against implementation.** |
| Q2  | [ROLE GAP]         | What can Staff profiles (not HQ Admin, not CM) do with ACM and ACI?                                                                                | ⚠️ **Not defined in AC** — infer same-as-CM. **Confirm with dev if needed.**                                   |
| Q3  | [MISSING BEHAVIOR] | When no ACI exists for a location + current AY, what does the SF/BO/Learner Calendar show?                                                         | ⚠️ **Not defined** — expected: no closed dates shown; no error. **Verify with test.**                          |
| Q4  | [MISSING BEHAVIOR] | Does the 1-Location:1-ACI:1-AY uniqueness constraint apply globally or only on initial apply?                                                      | ✅ **Inferred from rule 12**: constraint applies on every apply action; existing ACIs are always skipped.      |
| Q5  | [REGRESSION RISK]  | What reports or automation rely on the deprecated `Academic_Calendar__c` field on Location?                                                        | ⚠️ **Unknown** — regression risk. Flag for regression test scope review.                                       |
| Q6  | [MISSING BEHAVIOR] | JP translation for "Remarks" column header — is it "備考" or another label?                                                                        | ✅ **Confirmed from Jira comment (LT-91348)**: "備考".                                                         |
| Q7  | [MISSING BEHAVIOR] | Are the two messages below implemented in this epic? (1) "年度カレンダーの拠点は変更できません。" (2) "マスターカレンダーの拠点は設定できません。" | ✅ **Skipped** — agreed with PdM and TL in LT-91348. Not implemented in this epic.                             |

---

## Related Specs

- `input/specs/event-master-form-latest.md` — AC / Academic Calendar context for event scheduling
- `input/domain-knowledge/scheduling/scheduling-domain-knowledge.md` — Academic Week, Term, Closed Date domain rules
- LT-91348 — JP translation and UI copy for this epic (referenced in Jira comments)

## Related Test Cases

- `output/test-cases/lesson-management/academic-calendar/LT-87693-acm.md` — CRUD ACM test cases
- `output/test-cases/lesson-management/academic-calendar/LT-87693-aci.md` — CRUD ACI test cases
- `output/test-cases/lesson-management/academic-calendar/LT-87693-general.md` — Translation + Migration test cases
- `output/test-coverages/LT-87693-academic-calendar-closed-date-per-location.md` — Coverage matrix for this epic

## QASE Coverage Gaps

- AC 01.1 — No existing test case verifies the "1 ACM per AY" uniqueness constraint
- AC 01.1 — No existing test case verifies the duplicate-ACM error message (EN and JP)
- AC 01.2 — No existing test case verifies the "Set as default to all locations" toggle behavior
- AC 01.2 — No existing test case verifies brand-level vs center-level location selection
- AC 01.2 — No existing test case verifies the "skip existing ACI" behavior (no overwrite)
- AC 01.2 — No existing test case verifies closed-down location exclusion (selector + no ACI created)
- AC 01.3 — No existing test case verifies CD cloning completeness at apply time
- AC 01.3 — No existing test case verifies post-apply CD non-propagation to ACIs
- AC 01.4 — No existing test case verifies ACM delete restriction (blocks when ACI exists)
- AC 01.4 — No existing test case verifies HQ vs CM permission boundary on ACM
- AC 02.1 — No existing test case verifies "Apply to location" button hidden from ACI UI
- AC 02.1 — No existing test case verifies CM cannot clone ACI
- AC 02.2 — No existing test case verifies ACI CD isolation from ACM and sibling ACIs
- AC 03.1 — No existing test case verifies multi-AY accumulation per location (no overwrite across AYs)
- AC 04.1 — No existing test case verifies SF/BO Calendar closed date visibility via new traversal path
- AC 04.2 — No existing test case verifies Learner App Calendar closed date visibility
- Migration — No existing test case verifies pre-existing AC records are intact post-deployment
