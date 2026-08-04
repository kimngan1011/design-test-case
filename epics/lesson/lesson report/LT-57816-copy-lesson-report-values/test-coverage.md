# Test Coverage: LT-57816 — Copy Lesson Report Values to Lesson Report Details

**Jira:** https://manabie.atlassian.net/browse/LT-57816  
**Date:** 2026-07-31

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
| --- | --- | --- |
| 1 | AC 01.1 | The propagation rule applies when Teaching Method = Group. |
| 2 | AC 01.1 | A stored Content value is copied from the Lesson Report to every per-student Lesson Report Detail. |
| 3 | AC 01.1 | A stored Next Lesson's Announcement value is copied from the Lesson Report to every per-student Lesson Report Detail. |
| 4 | AC 01.1 | A stored Next Lesson's Homework value is copied from the Lesson Report to every per-student Lesson Report Detail. |
| 5 | AC 01.2 | Updating one of the three shared values overwrites that value on every existing per-student Lesson Report Detail. |
| 6 | AC 01.3 | Updating an unrelated Lesson Report field preserves all three stored shared values on the source report and every per-student detail. |
| 7 | AC 01.4 | The source and per-student values remain identical on SF and BO, on Lesson Report under Lesson and Lesson Report Detail. |
| 8 | AC 01.5 | After the Lesson and Lesson Report are Published, the enrolled student sees the same three stored values on the Learner App. |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
| --- | --- | --- |
| AC 01.1 | 1 | Conditional logic |
| AC 01.1 | 2, 3, 4 | Data integrity; Cross-system impact; Display completeness |
| AC 01.2 | 5 | Data integrity; CRUD; Cross-system impact |
| AC 01.3 | 6 | Data integrity; Cross-system impact |
| AC 01.4 | 7 | Data integrity; Display completeness |
| AC 01.5 | 8 | Cross-system impact; State transition; Display completeness |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
| --- | --- |
| Conditional logic | Decision Table |
| Data integrity | CRUD; Regression |
| Cross-system impact | Regression; CRUD |
| Display completeness | Component |
| State transition | State Transition; Regression |
| Negative / preservation | Negative; Regression |

---

## 4. Mandatory Edge-Case Assessment

| Area | Assessment | Coverage decision |
| --- | --- | --- |
| A. Configuration-driven thresholds | N/A — no configuration, limit, or tenant flag is specified. | None. |
| B. Date / time | N/A — no date or time rule is part of this change. | None. |
| C. Concurrent / stale state | N/A for this change — optimistic-locking cases already exist in Qase 3253–3255 and 13737–13739; LT-57816 does not define a new retry or conflict contract. | Do not duplicate locking coverage. |
| D. Permission & role | N/A — the change adds no role rule. Existing permission matrix allows Lesson Report edit for full-access, centre-level-edit, and BO-teacher users. | Use an authorized staff/teacher actor only. |
| E. State transition | Existing status rules apply — the Learner App assertion requires both Lesson and Lesson Report = Published. | Add a published-state precondition and confirm the values only after publication. |
| F. Cross-system / cross-surface | Yes — SF and BO can perform the requested updates; each stored value is evidenced in the student's Report History on both platforms. | After each SF or BO update, read the target lesson row in both SF Student Lesson Allocation → Report History and BO Lesson → Student Report History; add the published-report Mobile read-back check. |
| G. Downstream effects | Yes — every create/update writes the three values to child Lesson Report Details. | See Section 5. |
| H. Display completeness | Yes — each relevant surface must show the three exact stored values. No sort, tooltip, empty-state, or pagination rule is specified. | Add concrete-value assertions for both Report under Lesson and Report Detail on SF and BO. |
| H.1 Figma mismatch | N/A — no Figma URL is present in the Jira ticket. | None. |

---

## 5. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
| --- | --- | --- | --- |
| Store all three shared values on a Group Lesson Report from SF Report under Lesson | Each student's Report History row stores the same Content, Announcement, and Homework values. | SF Student Lesson Allocation → Report History; BO Lesson → Student Report History | TC-LR-01 |
| Store all three shared values on a Group Lesson Report from BO Report under Lesson | Each student's Report History row stores the same Content, Announcement, and Homework values. | SF Student Lesson Allocation → Report History; BO Lesson → Student Report History | TC-LR-02 |
| Update Content, Announcement, or Homework from SF Report under Lesson or SF Report Detail | The changed field replaces its prior value in each student's Report History row, while the other two shared fields retain their values. | SF Student Lesson Allocation → Report History; BO Lesson → Student Report History | TC-LR-03 to TC-LR-08 |
| Update Content, Announcement, or Homework from BO Report under Lesson or BO Report Detail | The changed field replaces its prior value in each student's Report History row, while the other two shared fields retain their values. | SF Student Lesson Allocation → Report History; BO Lesson → Student Report History | TC-LR-09 to TC-LR-14 |
| Update an unrelated Lesson Report field from every in-scope surface | No shared field is cleared or replaced in any student's Report History row. | SF Student Lesson Allocation → Report History; BO Lesson → Student Report History | TC-LR-15 to TC-LR-18 |
| Publish the Lesson and Lesson Report after stored values exist | The enrolled student sees the exact Content, Announcement, and Homework values from that student's Lesson Report Detail. | Learner App | TC-LR-19, TC-LR-20 |

No inverse action, counter, notification, or status change is specified by LT-57816.

---

## 6. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
| --- | --- | --- | --- | --- |
| SF Lesson Report under Lesson | Content; Next Lesson's Announcement; Next Lesson's Homework | Propagation applies only to Group lessons | None | None |
| BO Lesson Report under Lesson | Content; Next Lesson's Announcement; Next Lesson's Homework | Propagation applies only to Group lessons | None | None |
| SF Student Lesson Allocation → Report History → Lesson Report Details | Content; Next Lesson - Homework; Next Lesson - Announcement for the target lesson row | Per-student detail | None | None |
| BO Lesson → Student Report History | Content; Next Lesson - Homework; Next Lesson - Announcement for the target lesson row | Per-student detail | None | None |
| Learner App Lesson Report | Content; Next Lesson's Announcement; Next Lesson's Homework for the enrolled student | Lesson and Lesson Report = Published | None | None |

---

## 7. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
| --- | --- | --- | --- | --- | --- |
| AC 01.1 | Store all three shared fields on a Group Lesson Report from SF Report under Lesson and copy exact values to details for two enrolled students. | Conditional; Data integrity | Decision Table; CRUD | High | Deep |
| AC 01.1 | Store all three shared fields on a Group Lesson Report from BO Report under Lesson and copy exact values to details for two enrolled students. | Conditional; Data integrity | Decision Table; CRUD | High | Deep |
| AC 01.1 / AC 01.4 | Read the stored values from each student's SF and BO Report History row. | Data integrity; Display completeness | Regression; Component | High | Deep |
| AC 01.2 | Update Content, Next Lesson's Announcement, and Next Lesson's Homework separately from SF Report under Lesson and SF Report Detail; overwrite only the selected field on every detail. | Data integrity; CRUD | CRUD; Regression | High | Deep |
| AC 01.2 | Update Content, Next Lesson's Announcement, and Next Lesson's Homework separately from BO Report under Lesson and BO Report Detail; overwrite only the selected field on every detail. | Data integrity; CRUD | CRUD; Regression | High | Deep |
| AC 01.3 | Update an unrelated report field from SF Report under Lesson and SF Report Detail; retain all three shared values on source and details. | Data integrity | Negative; Regression | High | Deep |
| AC 01.3 | Update an unrelated report field from BO Report under Lesson and BO Report Detail; retain all three shared values on source and details. | Data integrity | Negative; Regression | High | Deep |
| AC 01.3 / AC 01.4 | After every SF or BO update, read the three fields from each student's SF and BO Report History row. | Data integrity; Regression | Regression | High | Deep |
| AC 01.5 | After publishing the Lesson and Lesson Report, read the three stored values as an enrolled student on the Learner App. | State transition; Cross-system; Display completeness | State Transition; Regression; Component | High | Deep |

---

## 8. High-Risk Areas Requiring Deeper Testing

### 🟠 High Risk

| Area | Reason | Recommended Approach |
| --- | --- | --- |
| Per-student value propagation | A Group lesson can have multiple student details. A partial write gives different students different report data. | Set up two named students and assert all three exact values for both students. |
| Update overwrite semantics | An update can leave stale values on a detail or overwrite one of the other shared values. | Change one shared field at a time from each requested update entry point; assert the changed field and the two preserved fields on every detail. |
| Unrelated update preservation | Saving another field can submit a partial payload and blank or revert the three stored fields. | Save an explicit unrelated field such as Remarks from each requested update entry point; assert the original three values remain unchanged on source and details. |
| SF/BO and surface parity | The report source and child details appear on four user-facing contexts. A sync or mapping issue may only be visible on one. | Use concrete values and read back from SF/BO Report under Lesson and Report Detail after an SF-originated and BO-originated update. |
| Learner App published report | Mobile reads the per-student stored values that this ticket introduces; stale or missing values defeat the feature purpose. | Publish both Lesson and Lesson Report, then assert all three exact values as the enrolled student. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
| --- | --- | --- |
| Group-only condition | Applying this change to a non-Group lesson is not specified. | Do not infer individual-lesson behaviour; keep all new cases explicitly Group. |

---

## 9. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
| --- | --- | --- | --- |
| Group-report shared fields updated on BO and Mobile | Qase 13747 — Edit Group Report | Partial: broad update/publish path, but no per-student exact-value mapping or overwrite check. | ✅ Assert all three values for each student detail after initial store and individual field updates. |
| Group-report updates from SF visible on BO | Qase 3173 — Group Lesson edit/publish | Partial: broad end-to-end path, but no exact mapping of Content, Announcement, Homework to every detail. | ✅ Add concrete source/detail values on both SF and BO. |
| Preserve shared fields when an unrelated field changes | None found | None | ✅ Add negative regression coverage for an unrelated field update. |
| BO Report under Lesson and BO Report Detail parity | Qase 427 and 1748 suites | Partial: the surfaces exist, but no exact LT-57816 mapping case found. | ✅ Add surface-specific read-back assertions. |
| Learner App values after Lesson and Report publication | Qase 13747 and 3173 | Partial: broad Mobile visibility after publishing, but no assertion that the three exact stored detail values are shown. | ✅ Add per-student, exact-value Mobile read-back after both publication states. |

---

## 10. Suggested Test Suite Structure

```text
epics/lesson/lesson report/LT-57816-copy-lesson-report-values/test-cases/
├── report-under-lesson-value-sync.md   → AC 01.1–01.4 — SF/BO Report-under-Lesson store, overwrite, and unrelated-update preservation (10 TCs)
├── report-detail-value-sync.md         → AC 01.1–01.5 — SF/BO Report-Detail overwrite, per-student persistence, and Learner App published-value checks (10 TCs)
```

Target Qase placement after approval:

- PX / suite 292 **Lesson Report BO** → existing child suite 427 **Lesson Report under Lesson**
- PX / suite 292 **Lesson Report BO** → existing child suite 1748 **Lesson Report Detail**
