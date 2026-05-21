# Test Coverage: LT-87693 — Academic Calendar Closed Date per Location

**Jira:** https://manabie.atlassian.net/browse/LT-87693
**PRD:** https://manabie.atlassian.net/wiki/spaces/ERP/pages/1826848769
**Date:** 2026-05-18

---

## 1. Business Rules Extracted

| #   | AC      | Business Rule                                                                                                                                                                                                                |
| --- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | AC 01.1 | Only ACs created via the Salesforce UI are considered Academic Calendar Masters (ACM); the system flags them as `Master` upon creation                                                                                       |
| 2   | AC 01.1 | ACM cannot be associated with any Location field                                                                                                                                                                             |
| 3   | AC 01.1 | Each Academic Year (AY) can have **at most one** ACM                                                                                                                                                                         |
| 4   | AC 01.1 | Attempting to create a second ACM for the same AY (via New or Clone) shows error: "A Master Academic Calendar already exists for this Academic Year. Please update the existing master or select a different Academic Year." |
| 5   | AC 01.2 | ACM creation form includes a "Select Locations" panel for choosing which locations to apply the ACM to                                                                                                                       |
| 6   | AC 01.2 | When "Set as default to all locations" is **ON**, the location selector is disabled; all active locations are targeted                                                                                                       |
| 7   | AC 01.2 | When "Set as default to all locations" is **OFF**, the user can select one or more locations individually (single center, brand-level parent, or org-level)                                                                  |
| 8   | AC 01.2 | Closed-down Locations are **not displayed** in the location selection list                                                                                                                                                   |
| 9   | AC 01.2 | Applying an ACM clones the full AC content (weeks, terms) into a new Individual AC (ACI) for each selected location                                                                                                          |
| 10  | AC 01.2 | ACI naming format: `{ACMaster.name}_{Location.name}`                                                                                                                                                                         |
| 11  | AC 01.2 | Exactly **one ACI** is created per location per application action                                                                                                                                                           |
| 12  | AC 01.2 | ACI is only created for locations that **do not already have** an AC under the selected AY; existing ACIs for that location + AY are not overwritten                                                                         |
| 13  | AC 01.2 | Closed-down locations **never receive** an ACI, even when "Set as default to all locations" is ON                                                                                                                            |
| 14  | AC 01.3 | Closed Dates created under an ACM are automatically cloned into each resulting ACI when the ACM is applied to locations                                                                                                      |
| 15  | AC 01.3 | Each ACI receives a separate copy of every Closed Date that existed in the ACM at the time of application                                                                                                                    |
| 16  | AC 01.3 | Closed Dates added to an ACM **after** locations have already been applied are associated only with the ACM and are **not** auto-propagated to existing ACIs                                                                 |
| 17  | AC 01.4 | Only HQ profiles have permission to create, edit, or delete an ACM and its Closed Dates                                                                                                                                      |
| 18  | AC 01.4 | CM users can **view** an ACM but cannot edit or delete it                                                                                                                                                                    |
| 19  | AC 01.4 | HQ users can: create ACM, edit ACM, associate Closed Date with ACM, apply ACM to locations, and delete ACM                                                                                                                   |
| 20  | AC 01.4 | CM users can: create/edit/delete their own ACI only; the "Apply to location" button is hidden when a CM views or edits an ACI                                                                                                |
| 21  | AC 02.1 | Under the Academic Year record page, a custom Academic Calendar related list is added; it shows ACM as view-only for CM/Staff with a **Remarks** column showing "master", and shows each CM's own ACI                        |
| 22  | AC 02.1 | CM can edit their own ACI (terms, week dates, week order, name)                                                                                                                                                              |
| 23  | AC 02.1 | "Apply to All Locations" and "Apply to Selected Locations" actions are **hidden** in the ACI edit/detail UI                                                                                                                  |
| 24  | AC 02.1 | CM can delete their own ACI; after deletion the location is no longer associated with that AY's calendar                                                                                                                     |
| 25  | AC 02.1 | CM cannot clone an ACI; attempting to do so triggers the same duplicate-ACM error message as rule #4                                                                                                                         |
| 26  | AC 02.2 | Location-specific Closed Dates are stored under the ACI for that location                                                                                                                                                    |
| 27  | AC 02.2 | Deleting or modifying a Closed Date in an ACI does **not** affect the ACM or other ACIs                                                                                                                                      |
| 28  | AC 02.2 | CM can: retain cloned Closed Dates, add new Closed Dates to their ACI, or remove Closed Dates from their ACI                                                                                                                 |
| 29  | AC 02.3 | The Academic Calendar list/table view is filtered by user's location affiliation; CM sees only ACs where the location matches their affiliated location(s)                                                                   |
| 30  | AC 03.1 | A new Lookup field `Location__c` is added to the Academic Calendar object (1 Location : n ACs); the old 1:1 field on Location is deprecated                                                                                  |
| 31  | AC 03.1 | When a new ACM is created for a new AY and applied to all locations, it **accumulates** (each location gains an additional ACI); existing ACIs for prior AYs are not removed                                                 |
| 32  | AC 03.1 | A new Academic Calendar related list is added to the Location record page; permission set "View Location's AC" controls access                                                                                               |
| 33  | US 04   | SF/BO Calendar displays location Closed Dates by traversing: Location + Current AY → Academic Calendar → Closed Date                                                                                                         |
| 34  | US 04   | Learner App Calendar displays location Closed Dates by traversing: Enrollment Location → Location + Current AY → Academic Calendar → Closed Date                                                                             |

---

## 2. Logic Type Categorization

| AC      | Business Rule # | Logic Type(s)                               |
| ------- | --------------- | ------------------------------------------- |
| AC 01.1 | 1               | Data integrity                              |
| AC 01.1 | 2               | Validation logic                            |
| AC 01.1 | 3               | Data integrity, Validation logic            |
| AC 01.1 | 4               | Validation logic, Error handling            |
| AC 01.2 | 5               | CRUD Testing                                |
| AC 01.2 | 6               | Conditional logic                           |
| AC 01.2 | 7               | Conditional logic, Equivalence partitioning |
| AC 01.2 | 8               | Conditional logic, Validation logic         |
| AC 01.2 | 9               | Data integrity, Recurrence logic            |
| AC 01.2 | 10              | Validation logic                            |
| AC 01.2 | 11              | Data integrity                              |
| AC 01.2 | 12              | Conditional logic, Data integrity           |
| AC 01.2 | 13              | Conditional logic, Data integrity           |
| AC 01.3 | 14, 15          | Recurrence logic, Data integrity            |
| AC 01.3 | 16              | Conditional logic, Data integrity           |
| AC 01.4 | 17, 18, 19, 20  | Permission logic                            |
| AC 02.1 | 21              | Permission logic, CRUD Testing              |
| AC 02.1 | 22              | CRUD Testing                                |
| AC 02.1 | 23              | Permission logic, Conditional logic         |
| AC 02.1 | 24, 25          | CRUD Testing, Validation logic              |
| AC 02.2 | 26, 27, 28      | Data integrity, CRUD Testing                |
| AC 02.3 | 29              | Permission logic, Conditional logic         |
| AC 03.1 | 30, 31, 32      | Data integrity, State transition            |
| US 04   | 33, 34          | Cross-system impact                         |

---

## 3. Test Technique Selection

| Logic Type          | Applicable Techniques                             |
| ------------------- | ------------------------------------------------- |
| Validation logic    | Equivalence Partitioning, Negative Testing        |
| Conditional logic   | Decision Table, Negative Testing                  |
| Data integrity      | CRUD Testing, Regression Analysis, Decision Table |
| Recurrence logic    | State Transition Testing, Regression Analysis     |
| State transition    | State Transition Testing, CRUD Testing            |
| Permission logic    | Permission Matrix, Decision Table                 |
| Cross-system impact | Regression Analysis, CRUD Testing                 |
| Error handling      | Negative Testing, Equivalence Partitioning        |

---

## 4. Structured Coverage Strategy

| AC      | Business Rule Summary                                                   | Logic Type                        | Test Technique                             | Risk Level | Coverage Depth |
| ------- | ----------------------------------------------------------------------- | --------------------------------- | ------------------------------------------ | ---------- | -------------- |
| AC 01.1 | Only UI-created ACs become ACM; flagged as Master                       | Data integrity                    | CRUD Testing                               | High       | Standard       |
| AC 01.1 | ACM cannot be linked to a Location                                      | Validation logic                  | Negative Testing                           | High       | Standard       |
| AC 01.1 | Each AY allows only one ACM                                             | Data integrity                    | Equivalence Partitioning, Negative Testing | Critical   | Deep           |
| AC 01.1 | Duplicate ACM creation blocked with error                               | Validation logic                  | Negative Testing                           | Critical   | Deep           |
| AC 01.2 | "Select Locations" UI panel present on Create ACM form                  | CRUD Testing                      | CRUD Testing                               | Medium     | Smoke          |
| AC 01.2 | "Set as default to all locations" ON → selector disabled                | Conditional logic                 | Decision Table                             | High       | Standard       |
| AC 01.2 | "Set as default to all locations" OFF → select by center, brand, or org | Conditional logic                 | Decision Table, Equivalence Partitioning   | High       | Deep           |
| AC 01.2 | Closed-down locations hidden from selector                              | Conditional logic                 | Decision Table, Negative Testing           | High       | Standard       |
| AC 01.2 | Clone full AC content (weeks, terms) into ACI on apply                  | Data integrity, Recurrence logic  | CRUD Testing, State Transition Testing     | Critical   | Deep           |
| AC 01.2 | ACI naming: `ACMaster.name_Location.name`                               | Validation logic                  | CRUD Testing                               | Medium     | Standard       |
| AC 01.2 | One ACI per location per apply                                          | Data integrity                    | Decision Table                             | Critical   | Deep           |
| AC 01.2 | Skip locations that already have ACI for the AY                         | Conditional logic, Data integrity | Decision Table, Negative Testing           | Critical   | Deep           |
| AC 01.2 | Closed-down locations never receive ACI                                 | Conditional logic, Data integrity | Decision Table, Negative Testing           | High       | Standard       |
| AC 01.3 | Closed Dates cloned into each ACI at time of apply                      | Recurrence logic, Data integrity  | CRUD Testing, State Transition Testing     | Critical   | Deep           |
| AC 01.3 | New Closed Dates added post-apply not propagated to ACIs                | Conditional logic, Data integrity | Decision Table                             | Critical   | Deep           |
| AC 01.4 | HQ only can create/edit/delete ACM and its CDs                          | Permission logic                  | Permission Matrix                          | High       | Deep           |
| AC 01.4 | CM can view ACM; cannot edit or delete                                  | Permission logic                  | Permission Matrix, Negative Testing        | High       | Standard       |
| AC 02.1 | AY page shows ACM (view-only for CM) + own ACI                          | Permission logic, CRUD Testing    | Permission Matrix, CRUD Testing            | High       | Standard       |
| AC 02.1 | CM can edit their ACI (terms, weeks, dates, order)                      | CRUD Testing                      | CRUD Testing, Boundary Value Analysis      | High       | Deep           |
| AC 02.1 | "Apply to location" hidden from ACI UI                                  | Permission logic                  | Permission Matrix, Negative Testing        | High       | Standard       |
| AC 02.1 | CM can delete their own ACI                                             | CRUD Testing                      | CRUD Testing                               | High       | Standard       |
| AC 02.1 | CM cannot clone ACI; error message shown                                | Validation logic                  | Negative Testing                           | High       | Standard       |
| AC 02.2 | ACI CDs isolated from ACM and other ACIs                                | Data integrity                    | CRUD Testing, Decision Table               | Critical   | Deep           |
| AC 02.2 | CM can add/remove/retain CDs in their ACI                               | CRUD Testing                      | CRUD Testing                               | High       | Standard       |
| AC 02.3 | AC list filtered by CM's affiliated location                            | Permission logic                  | Permission Matrix                          | Medium     | Standard       |
| AC 03.1 | Location accumulates ACIs per AY (no overwrite)                         | State transition, Data integrity  | State Transition Testing, CRUD Testing     | Critical   | Deep           |
| AC 03.1 | Location record page shows new AC related list                          | CRUD Testing                      | CRUD Testing                               | Medium     | Smoke          |
| US 04   | SF/BO Calendar shows location CDs via AC                                | Cross-system impact               | Regression Analysis, CRUD Testing          | High       | Standard       |
| US 04   | Learner Calendar shows location CDs via enrollment                      | Cross-system impact               | Regression Analysis                        | High       | Standard       |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area                                             | Reason                                                                                                                                                              | Recommended Approach                                                                                                                 |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Duplicate ACM per AY prevention (rules 3, 4)     | Silent creation of a second ACM would corrupt the entire location calendar hierarchy for that AY                                                                    | Test via New + Clone paths; test with different AY to confirm the constraint is AY-scoped, not global                                |
| ACI cloning completeness (rules 9, 14, 15)       | If terms/weeks/closed dates are partially cloned, locations operate on incomplete academic data, causing scheduling errors                                          | Verify each field (name, all terms, all weeks, all closed dates) appears in every ACI after cloning; test with multiple closed dates |
| Skip existing ACI on re-apply (rule 12)          | If the system overwrites an existing ACI when re-applying the ACM, all local modifications made by the CM are silently lost                                         | Test: apply ACM → CM edits ACI → apply ACM again to same location → ACI must retain CM's changes and not be overwritten              |
| Closed Date post-apply non-propagation (rule 16) | If new CDs are auto-propagated after apply, locations lose control over their own CD set; if the reverse (CDs not cloned at apply time), locations have no base CDs | Test explicitly: apply ACM, then add CD to ACM; confirm existing ACIs do NOT receive the new CD                                      |
| ACI data isolation from ACM (rules 27, 28)       | If editing an ACI mutates the ACM or peer ACIs, all locations get unintended calendar changes                                                                       | Test: edit ACI terms/CDs → confirm ACM and sibling ACIs are unchanged                                                                |
| Multi-AY accumulation, no overwrite (rule 31)    | If the system overwrites the existing ACI when a new AY's ACM is applied, prior-year data is destroyed                                                              | Test: 2 AYs × 3 locations → each location should have 2 ACIs; count must be 2 per location                                           |

### 🟠 High Risk

| Area                                               | Reason                                                                                                                          | Recommended Approach                                                                                                    |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| HQ vs CM permission boundary (rules 17-20, 23, 25) | A CM who can edit or delete an ACM, or use "Apply to location", can inadvertently overwrite other centers' data                 | Permission Matrix: test all CRUD operations as CM on ACM; confirm all are blocked; confirm ACI "Apply" button is hidden |
| Closed-down location exclusion (rules 8, 13)       | If closed-down locations appear in the selector or receive ACIs, they pollute the location hierarchy and cause orphaned records | Confirm closed-down location absent from selector (UI) AND absent from created ACIs (data) after apply                  |
| ACI closed date management (rules 26-28)           | If ACI CD removes also delete from ACM, CMs effectively become able to corrupt the master calendar                              | Test remove CD from ACI → confirm ACM CD still exists; test add CD to ACI → confirm ACM unaffected                      |
| SF/BO Calendar visibility (rule 33)                | Closed dates must surface correctly on the calendar; if the traversal path breaks, lesson scheduling operates on wrong data     | End-to-end: create ACM → apply to location → view calendar for that location in SF/BO; confirm closed dates appear      |
| Learner App Calendar visibility (rule 34)          | Students/parents rely on accurate closed date display; incorrect CDs affect attendance expectations                             | End-to-end: verify closed dates visible in Learner App for a student enrolled at that location                          |

### 🟡 Medium Risk

| Area                                     | Reason                                                                                                       | Recommended Approach                                                                                |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| ACI naming format (rule 10)              | Incorrect naming makes it hard for HQ/CMs to identify which ACI belongs to which location                    | Verify format exactly: `{ACM name}_{Location name}`; test with special characters in location name  |
| AC visibility filtering for CM (rule 29) | If the filter is missing, CM can view and potentially misuse other locations' ACIs                           | Log in as CM with single-location affiliation; confirm no other locations' ACIs are visible         |
| Remarks column on AY page (rule 21)      | Missing "master" indicator could cause CM to attempt editing the ACM                                         | Check related list Remarks column shows "master" for ACM row; is empty for ACI rows                 |
| JP translation accuracy (LT-91348)       | Incorrect Japanese labels cause confusion for Japanese-market users; some messages were agreed to be skipped | Verify each new UI label in Japanese; confirm skipped messages from LT-91348 are correctly excluded |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                                     | Existing Test Case                                                                | Overlap | New Coverage Needed                                                            |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------ |
| CRUD ACM (Create/Read/Update/Delete)                         | None                                                                              | None    | ✅ Full CRUD suite for ACM in `LT-87693-acm.md`                                |
| ACM → ACI clone (all content: terms, weeks, CDs)             | None                                                                              | None    | ✅ Test cloning completeness with multiple terms + multiple CDs                |
| "Set as default" toggle behavior                             | None                                                                              | None    | ✅ Decision table: toggle ON/OFF + location selector state                     |
| Brand-level vs center-level location selection               | None                                                                              | None    | ✅ 3 equivalence partitions: brand, center, org-level                          |
| Skip existing ACI on re-apply                                | None                                                                              | None    | ✅ Regression guard: apply ACM → CM edits ACI → re-apply → verify no overwrite |
| Post-apply CD non-propagation                                | None                                                                              | None    | ✅ Decision table: add CD before apply vs after apply                          |
| Permission matrix: HQ vs CM on ACM                           | None                                                                              | None    | ✅ Permission matrix for all CRUD operations                                   |
| CRUD ACI (Edit terms/weeks/CDs, Delete, cannot Clone)        | None                                                                              | None    | ✅ Full ACI edit/delete/clone-blocked suite in `LT-87693-aci.md`               |
| ACI data isolation from ACM and sibling ACIs                 | None                                                                              | None    | ✅ Isolation tests: edit ACI → verify ACM and sibling unchanged                |
| CM cannot "Apply to location" from ACI                       | None                                                                              | None    | ✅ Button-hidden test in ACI suite                                             |
| Closed-down location exclusion (selector + ACI not created)  | None                                                                              | None    | ✅ Negative tests in ACM create suite                                          |
| Multi-AY accumulation per location                           | None                                                                              | None    | ✅ Multi-AY test in ACM create suite                                           |
| Location record page new AC related list                     | None                                                                              | None    | ✅ Smoke test in ACI delete suite                                              |
| SF/BO Calendar closed date visibility                        | None — existing calendar tests may cover basic display but not new traversal path | Partial | ✅ New end-to-end regression case needed                                       |
| Learner Calendar closed date visibility                      | None                                                                              | None    | ✅ New end-to-end regression case needed                                       |
| JP translation accuracy                                      | None                                                                              | None    | ✅ Translation suite in `LT-87693-general.md`                                  |
| Data migration (pre-existing records intact post-deployment) | None                                                                              | None    | ✅ Migration validation in `LT-87693-general.md`                               |

---

## 7. Suggested Test Suite Structure

```
output/test-cases/lesson-management/academic-calendar/
  ├── LT-87693-acm.md
  │     → AC 01.1, 01.2, 01.3, 01.4 (rules 1–20)
  │     → CRUD Academic Calendar Master: create form, apply all/brand/center/org,
  │       clone CDs, post-apply CD non-propagation, edit, view (HQ vs CM),
  │       delete (with/without ACI), duplicate AY prevention, multi-AY accumulation
  │     → Roles tested: HQ Admin, CM
  │
  ├── LT-87693-aci.md
  │     → AC 02.1, 02.2, 02.3 (rules 21–29)
  │     → CRUD Academic Calendar Individual: view after clone, edit terms/weeks/order,
  │       add/delete terms, manage CDs (add/remove cloned/non-cloned), delete ACI,
  │       cannot clone ACI, delete from location page, CM visibility filtering
  │     → Roles tested: CM only (boundary with HQ where relevant)
  │
  └── LT-87693-general.md
        → US 04 (rules 33–34) + migration + translation
        → SF/BO Calendar and Learner Calendar closed date visibility,
          JP translation accuracy, data migration validation
```
