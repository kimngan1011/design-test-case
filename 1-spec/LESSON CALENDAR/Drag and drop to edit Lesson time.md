# LT-92190 – EEA | Core | Drag and Drop to Edit Lesson Time on Calendar

- **Jira Key:** LT-92190  
- **Project:** Learning and Teaching (LT)  
- **Type:** Epic  
- **Team:** Tech – Scheduling Management  
- **System Type:** ERP  
- **Partner:** EEA  
- **Assignee (Dev):** Long Le  
- **QA:** Nguyễn Châu Thùy Linh  
- **Product Manager:** Tuyen Hua  
- **Start Date (Dev):** 2026-01-19  
- **Due Date (Dev complete, excl. QA):** 2026-02-28  
- **Internal UAT Date:** 2026-03-02  
- **External UAT Date:** 2026-03-02  
- **Target Production Release (Fix Version):** v2026.03.30  
- **Production Release Date:** 2026-03-30  
- **Status:** Ready for QA  

---

## 1. High-Level Description

**Epic Summary:**  
> EEA | Core | Drag and drop to edit Lesson time on Calendar

This epic enables users to drag and drop lesson cards on the lesson calendar to adjust:

- Date and time  
- Teacher  
- Classroom  

The feature is controlled by a lesson custom setting:

> `Enable Calendar Drag And Drop`

This is for **EEA (SF only)** and is classified as a **Core feature / Function addition**.

---

## 2. Requirements & Scope

### 2.1 Source Requirement

- **Requirement `#276`** in the spreadsheet:  
  https://docs.google.com/spreadsheets/d/1r0yJr7X5kIc2Tl7B4gIqiZ3eVMQ48UTja3fCYquPSTs/edit?gid=1908148601#gid=1908148601&fvid=1468401666  

- **PRD:**  
  https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2083881519/SF+only+Drag+Drop+to+adjust+Lesson+info  

### 2.2 Behavior Expectations

- **EEA expectation (from AS-IS system):**
  - EEA expects to drag and drop lessons every **10 minutes** or so.
  - This is **an expectation**, not a strict requirement, but is treated as an important UX target.

- **Weekly View:**
  - Allow drag and drop to different hour blocks.
  - Each hour block is divided into **4 sub-blocks (10 mins each)**.
  - Includes **recurring lessons** (when editing lesson date/time via drag and drop).

- **Daily View:**
  - Allow drag and drop with **10-min granularity**.

- **Scope Constraints (from PRD):**
  - **Only SF** (Salesforce-based partner EEA).
  - **No confirmation popup** (no Lesson Detail modal confirmation after drag and drop).

### 2.3 Additional Requirement

From Jira comment:  
https://manabie.atlassian.net/browse/LT-92190?focusedCommentId=154456  

> **Additional Requirement:**  
> - Always show **10 mins grids in Daily view**.

---

## 3. Release Notes

### 3.1 Internal Release Note (JP)

> 授業カレンダーにドラッグ・アンド・ドロップ機能を追加  
> 区分: 機能追加  
> 詳細: 授業カレンダーで授業カードをドラッグすることで日時、講師、教室を変更することができるようになりました。  
> 利用方法: カスタム設定で機能をONにしてください：**Enable Calendar Drag And Drop**

### 3.2 Internal Release Note (EN)

> Lesson Custom Settings: **Enable Calendar Drag And Drop**

### 3.3 External Release Note (JP)

> 授業カレンダーにドラッグ・アンド・ドロップ機能を追加  
> 区分: 機能追加  
> 詳細: 授業カレンダーで授業カードをドラッグすることで日時、講師、教室を変更することができるようになりました。

---

## 4. Threads Summary – Functional & UX Details

This section consolidates the 3 Slack threads.

### 4.1 Thread 1 – Lesson Calendar DnD: Behavior, Performance, Expectations

**Link:**  
- https://manabie.slack.com/archives/C037409QQ4S/p1770878102102619  

#### 4.1.1 Partner Requests (Maria)

- Ability to **change the start day of the week** in calendar:
  - EEA wants the week to **start on Thursday**.
- **Always show 10-min grid** in **Daily View** by default.

#### 4.1.2 Current Design & Plan (Long)

- **Week start day configuration:**
  - Current implementation assumes a fixed **7-day week starting at a standard day**.
  - Changing the start day of the week is considered an **improvement** and is **planned for later** (expected **around April**; not in current epic scope).

- **10-min grid:**
  - Implementation of a **10-min grid** is **feasible**.
  - Work is **planned after Lunar New Year** (around **March**).
  - Additional requirement: **Always show 10-min grids in Daily View** (already formalized in Jira).

#### 4.1.3 Performance Considerations (Daily View)

Daily View performance heavily depends on the number of teachers/classrooms and the total number of time slots.

Example estimation:

- Suppose:
  - 20 teachers
  - 18 hours displayed per day
  - 6 slots/hour (10-min increments)  
- Total slots: `20 × 18 × 6 = 2160` slots.

Rendering thousands of slots can cause lag.

Team decision:

- Optimize for up to **≈30 teachers/classrooms** in a single view.
- If there are more than that:
  - Recommend users to **use filters** to reduce the number of teachers/classrooms displayed concurrently.

#### 4.1.4 Rollout & Documentation Needs

- Feature is behind a **custom setting toggle**:
  - `Enable Calendar Drag And Drop`.
- The feature has been enabled on **pre-prod Manabie** for internal validation.
- Maria requested:
  - **Clear internal documentation** plus **release note / user guide** for PS team:
    - How to enable the feature.
    - Configuration/custom settings behavior.
    - Constraints and performance expectations.

---

### 4.2 Thread 2 – Impact Areas for Drag & Drop Epic (Testing Scope)

**Link:**  
- https://manabie.slack.com/archives/C02H52ZJFDY/p1769681362488219  

This thread focuses on QA impact analysis and initial test effort estimation (~50 test cases).

#### 4.2.1 Impacted Areas (from Long)

1. **Edit Lesson**
2. **Lesson Recurring**
3. **Assign Teacher**
4. **Calendar (Weekly, Daily)**
5. **Teacher Classing Alert**

#### 4.2.2 API vs UI Testing Scope

- **API Integration:**
  - Only **Edit Lesson** requires **backend API integration testing** (lesson update logic, clashing, etc.).

- **UI-Only Focus:**
  - The following are mainly **UI behavior** tests (no heavy API-specific coverage beyond basic flows):
    1. Lesson Recurring
    2. Assign Teacher
    3. Calendar views (Weekly, Daily)
    4. Teacher Classing Alert

  For these, QA should focus on:

  - Drag and drop behavior (mouse interaction).
  - Display updates (time, teacher, classroom labels).
  - Accurate reflection of state in the calendar UI.
  - Correct clashing alerts shown in the UI.

---

### 4.3 Thread 3 – Dev Smoke Test Results: AC Status & Performance

**Link:**  
- https://manabie.slack.com/archives/C02H52ZJFDY/p1770796589366279  

This thread summarizes developer smoke test results against Acceptance Criteria (AC) and stresses performance behavior.

#### 4.3.1 Acceptance Criteria Status

**ACs Passed:**

- 1.1, 1.2, 1.4  
- 2.1, 2.3  
- 3.1, 3.3  

**ACs / Areas with Issues:**

1. **AC 1.3 – Clashing Alert Validation**
   - **Correct behavior** when:
     - Only **time is changed**, **teacher remains the same**.
   - **Incorrect behavior** when:
     - **Teacher is changed** and **time is changed** simultaneously.
   - Clashing validation logic does not fully cover the combined scenario.

2. **Classrooms View**
   - Failing at the time of report.
   - A PR with fixes has been created and updated.
   - Status: **waiting for review**.

3. **Teacher View & AC 2.2**
   - Correct behavior **only when** editing the lesson **without changing teacher**.
   - When teacher is changed, some expectation from AC 2.2 is not fully met.

4. **AC 3.2**
   - Implementation updated in PR.
   - Demo on staging failed due to **deployment error** (environment issue, not necessarily functional).

#### 4.3.2 Performance / Stress Testing Results

- When there are **>20 classes/teachers** in the Daily View:
  - Observed **~3 seconds delay**.
- When approaching **~100 teachers**:
  - System may **freeze / hang** due to extreme number of slots (~9000).
  - Calculation example:
    - 100 teachers × 15 hours × 6 slots/hour = 9000 slots (approx).

**Action/Expectation from Khuong:**

- Performance optimization is required, especially around:
  - Rendering large numbers of slots.
  - Handling the stress test scenario more gracefully.
- This optimization is one of the criteria to evaluate Long’s capability level (junior vs mid).

#### 4.3.3 Consolidated Known Issues (as of 22/01/2026)

1. **Issue 1 – Clashing Alert Validation**
   - Incorrect handling when:
     - Changing both **teacher** and **time** via drag and drop.
   - Need to re-check:
     - Overlapping by teacher.
     - Overlapping by classroom.
   - Teacher/classroom clashing logic must be consistent in:
     - Edit Lesson.
     - Teacher View.
     - Classroom View.

2. **Issue 2 – Stress Test / Performance**
   - Daily View becomes slow (~3s delay) when:
     - More than **20 teachers** displayed.
   - Potential freeze when:
     - **~100 teachers** displayed at once.
   - Required improvements:
     - Performance tuning (lazy rendering, virtualization, etc.).
     - UX guidance (recommending filters when displaying many teachers).

---

## 5. QA Testing Perspective

### 5.1 Functional Scope to Cover

Based on the epic description and the 3 threads, QA should cover:

1. **Edit Lesson (Including API Integration)**
   - Drag and drop to adjust:
     - Start/end time.
     - Date (different day).
     - Teacher.
     - Classroom.
   - Ensure API updates are correct:
     - Lesson entity is persisted with new time/teacher/classroom.
     - Recurring pattern updates (if applicable).

2. **Lesson Recurring**
   - Drag and drop a recurring lesson:
     - Changing time within the same day.
     - Changing to a different day.
   - Verify how recurrence rules update or whether only an instance is changed (as specified in PRD/spec).

3. **Assign Teacher**
   - Dragging lessons between different teacher rows:
     - Same time, different teacher.
     - Different time, different teacher.
   - Validation for:
     - Teacher clashes.
     - Classroom constraints (if tied to teacher).

4. **Calendar Views (Weekly & Daily)**
   - **Weekly View:**
     - Hour blocks divided into **4 × 10-min sub-blocks**.
     - Drag and drop to any 10-min sub-block.
   - **Daily View:**
     - Always display **10-min grid**.
     - Dragging lessons in 10-min increments.
   - Cross-check:
     - Time labels are correct.
     - Visual snapping to the closest 10-min slot.
     - Week start day configuration (if/when implemented later).

5. **Teacher Classing Alert**
   - Clashing alerts when:
     - Two lessons overlap for the **same teacher**.
     - Two lessons overlap in the **same classroom**.
   - Special focus on:
     - **Changing both teacher and time** in one drag-and-drop action.
     - Cases where clashing is expected but not shown (per AC 1.3 issue).

### 5.2 Special Focus Scenarios

#### 5.2.1 Combined Change: Teacher + Time

This is a known problematic scenario:

- Steps:
  - Drag a lesson from Teacher A at 10:00 to Teacher B at 10:30 (for example).
- Expectations:
  - Clashing with teacher’s schedule is recalculated.
  - Clashing with classroom usage is recalculated.
  - Correct clashing alert should appear or not appear according to rules.
- Current status from dev:
  - Logic is correct only when keeping teacher the same and changing time.
  - Incorrect when teacher and time are both changed – must be covered thoroughly in QA.

#### 5.2.2 Performance & Stress Scenarios

- **Scenario sets:**
  1. **Small load (< 20 teachers)**:
     - Verify normal behavior; performance should feel smooth.
  2. **Medium load (~20–30 teachers)**:
     - This is the **design target**.
     - Measure perceived lag; confirm it is acceptable (<3s or as agreed).
  3. **High load (>30 teachers, up to ~100)**:
     - Document behavior as **known limitation**:
       - Potential lag or freeze.
       - Recommended mitigation: use filters to reduce teacher count.

- QA should:
  - Measure rough delay in key scenarios.
  - Record environment (browser, machine) to help dev interpret results.
  - Align with PM/Dev on acceptable thresholds.

---

## 6. Configuration & Enablement

- Feature is toggled by **Lesson Custom Setting**:

  - Name: `Enable Calendar Drag And Drop`

- When **ON**:
  - Users can drag and drop lesson cards in:
    - Weekly view.
    - Daily view.
  - Adjust:
    - Date and time.
    - Teacher.
    - Classroom.
  - Daily view should **always display 10-min grid** as per additional requirement.

- When **OFF**:
  - Calendar behaves as before:
    - No drag-and-drop adjustment of lessons.

---

## 7. Open Points / Future Improvements

From the threads and Jira context:

1. **Week Start Day Configuration**
   - Requirement: EEA wants **Thursday** as the first day of the week.
   - Status: Planned as an **improvement around April**, not necessarily part of the first GA release.

2. **Performance Optimization**
   - Further optimization required to handle:
     - Many teachers.
     - High-density lessons.
   - Might involve:
     - Virtualized rendering.
     - Pagination or grouping by teacher/classroom.
     - Clear UX recommendations for users.

3. **Documentation for PS & Customers**
   - Internal doc should describe:
     - How to enable `Enable Calendar Drag And Drop`.
     - Limitations (performance, max recommended teachers in view).
     - Clashing rules (teacher & classroom).
   - External release note already captured in Jira; may need localized manuals.

---

## 8. Links

- **Jira Epic:**  
  - https://manabie.atlassian.net/browse/LT-92190  

- **Requirement Spreadsheet:**  
  - https://docs.google.com/spreadsheets/d/1r0yJr7X5kIc2Tl7B4gIqiZ3eVMQ48UTja3fCYquPSTs/edit?gid=1908148601#gid=1908148601&fvid=1468401666  

- **PRD:**  
  - https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2083881519/SF+only+Drag+Drop+to+adjust+Lesson+info  

- **Slack Threads (internal):**  
  - Thread 1 (Behavior & Performance):  
    - https://manabie.slack.com/archives/C037409QQ4S/p1770878102102619  
  - Thread 2 (Impact Areas / QA Scope):  
    - https://manabie.slack.com/archives/C02H52ZJFDY/p1769681362488219  
  - Thread 3 (AC Results & Stress Test):  
    - https://manabie.slack.com/archives/C02H52ZJFDY/p1770796589366279  