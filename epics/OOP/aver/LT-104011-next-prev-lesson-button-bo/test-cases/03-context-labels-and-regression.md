# Test Cases: LT-104011 - Add Next and Prev lesson button in BO

## Suite: [Aver] BO Lesson Detail Navigation - Context Reload, Labels, and Regression

### [Aver] Lesson Detail Navigation - Destination context reload - Previous lesson opened - Header and lesson-specific content replaced

**Description:** AC 01.2 - CRUD - After lesson navigation, BO Lesson Detail reloads destination lesson-specific content instead of persisting source lesson data.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff with access to Aver lesson detail.
- Recurring lesson chain RC-1001 exists with LES-1001 and LES-1002 containing distinct lesson names, dates, and student lists.
- LES-1002 detail page is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Record the header, schedule information, and student list shown for LES-1002. | Source lesson details are visible and identifiable before navigation. | source_lesson = LES-1002; source_marker = unique_header_and_student_list |
| 2 | Click `Previous Lesson`. | BO navigates to the previous lesson detail. | action = Previous Lesson |
| 3 | Observe the destination lesson header, schedule information, and student list. | Header and lesson-specific content are replaced with LES-1001 data and no stale LES-1002 content remains. | destination_lesson = LES-1001 |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Detail Navigation - Report tab binding - Destination lesson selected - Report surface follows destination context

**Description:** AC 01.2 edge - Regression - After lesson navigation, report-related surfaces open for the destination lesson instead of the source lesson.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff with access to Aver lesson detail.
- Recurring lesson chain RC-1001 exists with LES-1001 and LES-1002, and each lesson has its own report-related content.
- LES-1002 detail page is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Click `Previous Lesson` from LES-1002. | BO opens LES-1001 detail page. | source_lesson = LES-1002; destination_lesson = LES-1001 |
| 2 | Open the report-related surface for the currently displayed lesson. | The report-related surface loads from the destination lesson context. | target_surface = lesson_report |
| 3 | Observe the report identifier or lesson reference on that surface. | Report content references LES-1001 and does not retain LES-1002 context. | expected_report_owner = LES-1001 |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Detail Navigation - Translation label - Aver tenant - Japanese labels shown exactly

**Description:** AC 01.5 - Component - Aver tenant displays the lesson-navigation labels exactly as `前の特訓` and `次の特訓`.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff in the Aver tenant.
- Recurring lesson LES-1002 is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Lesson Detail for LES-1002 in the Aver tenant. | Lesson Detail page loads. | tenant = Aver; lesson = LES-1002 |
| 2 | Observe the text shown on the two lesson-navigation buttons. | The backward button label is `前の特訓` and the forward button label is `次の特訓`. | expected_labels = 前の特訓 / 次の特訓 |
| 3 | Refresh the page and observe the same button labels again. | The same Aver labels remain unchanged after reload. | validation = label_persistence |

**Severity:** minor
**Priority:** medium

---

### [Aver] Lesson Detail Navigation - Translation label - Core rollout enabled - Core labels shown exactly

**Description:** AC 01.5 - Decision Table - If the feature is enabled for Core, BO Lesson Detail displays the Core translation labels exactly as `前の授業` and `次の授業`.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff in a Core tenant where LT-104011 rollout is enabled.
- Recurring lesson LES-2002 is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Lesson Detail for LES-2002 in the Core tenant with the feature enabled. | Lesson Detail page loads. | tenant = Core; lesson = LES-2002 |
| 2 | Observe the text shown on the two lesson-navigation buttons. | The backward button label is `前の授業` and the forward button label is `次の授業`. | expected_labels = 前の授業 / 次の授業 |
| 3 | Refresh the page and observe the same button labels again. | The same Core labels remain unchanged after reload. | validation = label_persistence |

**Severity:** minor
**Priority:** medium

---

### [Aver] Lesson Detail Navigation - Surface regression - Nested report view opened - Duplicate lesson-navigation pair not introduced

**Description:** AC 01.1 / AC 01.2 - Regression - Legacy report-navigation scope stays intact and does not create an unintended duplicate lesson-navigation pair on nested report surfaces.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff in the Aver tenant.
- Recurring lesson LES-1002 is open in BO Lesson Detail view mode.
- The lesson has an accessible nested report surface.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Observe the lesson-navigation pair on the main Lesson Detail surface for LES-1002. | One intended pair of lesson-navigation buttons is visible on the main lesson-detail surface. | surface = lesson_detail_view |
| 2 | Open the nested report surface for the same lesson. | The nested report surface opens normally. | nested_surface = lesson_report_view |
| 3 | Inspect the nested report surface for lesson-navigation duplication. | No unintended duplicate lesson-navigation pair is introduced on the nested report surface. | expected_duplicate = absent |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Detail Navigation - Existing action regression - Destination lesson loaded - Standard lesson-detail actions remain usable

**Description:** AC 01.2 - Regression - After lesson navigation, existing BO Lesson Detail actions remain available for the destination lesson and are not left in a stale source-lesson state.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff in the Aver tenant.
- Recurring lesson chain RC-1001 exists with LES-1001 and LES-1002.
- LES-1002 detail page is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Click `Previous Lesson` from LES-1002. | BO opens LES-1001 detail page. | source_lesson = LES-1002; destination_lesson = LES-1001 |
| 2 | Observe the standard lesson-detail actions on the destination page. | Standard lesson-detail actions are still visible and enabled or disabled according to LES-1001 state. | expected_actions = destination_lesson_default_actions |
| 3 | Open one standard lesson-detail action for the destination lesson. | The action opens from LES-1001 context and does not reference LES-1002. | action_context = LES-1001 |

**Severity:** major
**Priority:** high
