# Test Cases: LT-108376 — Add "Not Started" option as default in student filter in Lesson Calendar

> Source: `test-coverage.md` (CS-01..CS-16 + mandatory JST↔UTC case). Status rule follows current code (date only, logged-in user's timezone) — open question Q3.

## Suite: Lesson Calendar – Student List – Student Course Status Default (LT-108376)

### Lesson Calendar – Student List – Student Course Status Filter – First open – Active and Not Started pre-selected, Inactive not selected

**Description:** AC-01 — Component + Negative — On first load the Student Course Status filter shows Active and Not Started as default chips; Inactive is not selected; the same default applies to HQ and CM Staff. _(Coverage: CS-01 / CS-14)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- At Location A: **Student A** has LA Math 2026-04-01 → 2027-03-31 (Active)
- At Location A: **Student B** has LA English 2026-11-01 → 2027-03-31 (Not Started)
- At Location A: **Student C** has LA Science 2026-04-01 → 2026-09-30 (Inactive)
- The test is run twice: once as HQ Staff, once as CM Staff (same Location A affiliation)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A for the first time in a new browser session | Lesson Calendar loads; the Student panel on the left shows the Student list | today = 2026-10-20 (JST); current AY = AY 2026 |
| 2 | HQ or CM Staff clicks the filter (funnel) icon on the Student panel | The filter popover opens; the **Student Course Status** field shows two chips in this order: **Active ×** and **Not Started ×** | default_statuses = [Active, Not Started] |
| 3 | HQ or CM Staff opens the Student Course Status option list | Options Active, Not Started, Inactive are listed; Active and Not Started are selected; **Inactive is not selected** | options = [Active, Not Started, Inactive] |
| 4 | HQ or CM Staff clicks × on the **Not Started** chip, then closes the popover without clicking Save | The Student list does not change (still Student A and Student B); reopening the filter shows Active and Not Started again | unsaved change discarded |
| 5 | HQ or CM Staff repeats steps 1–3 logged in with the other role (HQ ↔ CM) | Same result: Active and Not Started pre-selected, Inactive not selected | role_2 = CM Staff (or HQ Staff) |

**Severity:** major
**Priority:** high

---

### Lesson Calendar – Student List – Default Filter – Active and Not Started LAs – Listed; Inactive LA hidden

**Description:** AC-02 — Equivalence Partitioning — With the default filter, the Student list shows LAs in the Active and Not Started partitions and hides the Inactive partition; the item count matches. _(Coverage: CS-02)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- At Location A: **Student A** has LA Math 2026-04-01 → 2027-03-31 (Active)
- At Location A: **Student B** has LA English 2026-11-01 → 2027-03-31 (Not Started — newly ordered, future start)
- At Location A: **Student C** has LA Science 2026-04-01 → 2026-09-30 (Inactive)
- No other LA exists at Location A in AY 2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A without opening the filter | The Student list shows **Student A** and **Student B**; the header shows **2 items** | today = 2026-10-20 (JST); current AY = AY 2026; A: start 2026-04-01 ≤ today ≤ end 2027-03-31 → Active; B: start 2026-11-01 > today → Not Started; C: end 2026-09-30 < today → Inactive |
| 2 | HQ or CM Staff looks for Student C in the Student list | **Student C is not listed** | C = Inactive → hidden by default |
| 3 | HQ or CM Staff types "Student C" in the Search Student Name box | No row is shown (0 items) — the search applies on top of the default status filter | keyword = Student C |

**Severity:** major
**Priority:** high

---

### Lesson Calendar – Student List – Default Filter – LA Start Date at today vs tomorrow – Both listed (Active / Not Started)

**Description:** AC-02 — BVA — Boundary on LA Start Date: an LA starting today is Active and an LA starting tomorrow is Not Started; both are in the default list. _(Coverage: CS-03)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- At Location A: **Student D** has LA Math with Start Date 2026-10-20 and End Date 2027-03-31
- At Location A: **Student E** has LA Math with Start Date 2026-10-21 and End Date 2027-03-31

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A | Student D and Student E are both in the Student list | today = 2026-10-20 (JST); current AY = AY 2026; D.start = 2026-10-20; E.start = 2026-10-21 |
| 2 | HQ or CM Staff opens the filter, removes **Not Started** (only Active selected) and clicks Save | Only **Student D** is listed | D.start 2026-10-20 = today → Active (boundary); E.start 2026-10-21 = today+1 → not Active |
| 3 | HQ or CM Staff opens the filter, removes **Active**, adds **Not Started** (only Not Started selected) and clicks Save | Only **Student E** is listed | E.start 2026-10-21 > today → Not Started; D.start = today → not Not Started |

**Severity:** major
**Priority:** high

---

### Lesson Calendar – Student List – Default Filter – LA End Date at today vs yesterday – Today listed as Active; yesterday hidden as Inactive

**Description:** AC-02 — BVA + Negative — Boundary on LA End Date: an LA ending today is still Active (listed); an LA that ended yesterday is Inactive (hidden by default). _(Coverage: CS-03)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- At Location A: **Student F** has LA Math with Start Date 2026-04-01 and End Date 2026-10-20
- At Location A: **Student G** has LA Math with Start Date 2026-04-01 and End Date 2026-10-19

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A | **Student F** is listed; **Student G** is not listed | today = 2026-10-20 (JST); current AY = AY 2026; F.end = 2026-10-20 (= today → Active); G.end = 2026-10-19 (today−1 → Inactive) |
| 2 | HQ or CM Staff opens the filter, adds **Inactive** to the selection and clicks Save | Student F and **Student G** are both listed | statuses = [Active, Not Started, Inactive] |
| 3 | HQ or CM Staff opens the filter, keeps only **Inactive** and clicks Save | Only **Student G** is listed | G.end 2026-10-19 < today → Inactive; F.end = today → not Inactive |

**Severity:** major
**Priority:** high

---

### Lesson Calendar – Student List – Default Filter – Student with an Inactive LA and a Not Started LA – Only the Not Started LA row shown

**Description:** AC-02 — Scenario — A student who has an ended LA and a newly ordered future LA appears by default through the future LA only. _(Coverage: CS-04)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- At Location A: **Student H** has LA #1 English 2026-04-01 → 2026-09-30 (Inactive)
- At Location A: **Student H** has LA #2 English Advanced 2026-12-01 → 2027-03-31 (Not Started)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A | **Student H** is listed with exactly **one row**, showing the allocation of LA #2 (English Advanced) | today = 2026-10-20 (JST); current AY = AY 2026; LA#1.end 2026-09-30 < today → Inactive (hidden); LA#2.start 2026-12-01 > today → Not Started (shown) |
| 2 | HQ or CM Staff opens the filter, adds **Inactive** and clicks Save | Student H now has **two rows**: one for LA #1 and one for LA #2 | statuses = [Active, Not Started, Inactive] |

**Severity:** minor
**Priority:** medium

---

### Lesson Calendar – Student List – Default Filter – Change Associated Course with future effective date – Two rows, one per LA

**Description:** AC-02 — Scenario — After Change Associated Course with a future effective date (old LA ends at the effective date, new LA starts at it), the student shows one row per LA by default — expected. _(Coverage: CS-05)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- At Location A: **Student J** has an order with Course **Math** from 2026-04-01 → 2027-03-31 (LA Math)
- HQ or CM Staff has changed the associated course of Student J's order from Math to **Science** with effective date **2026-11-01** (same flow as Qase PX-1774)
- Result of the update: LA Math end = 2026-11-01; LA Science start = 2026-11-01, end = 2027-03-31

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A | **Student J** is listed in **two rows**: one row for LA Math and one row for LA Science; each row shows its own allocation count | today = 2026-10-20 (JST); current AY = AY 2026; LA Math: 2026-04-01 ≤ today ≤ 2026-11-01 → Active; LA Science: start 2026-11-01 > today → Not Started |
| 2 | HQ or CM Staff opens the filter, removes **Not Started** and clicks Save | Student J is listed in **one row** (LA Math only) | statuses = [Active] |

**Severity:** minor
**Priority:** medium

---

### Lesson Calendar – Student List – Default Filter – Future LA in the next Academic Year – Hidden until that Academic Year is selected

**Description:** AC-02 — Decision Table — With the default current-AY filter, a newly ordered LA of the next academic year is not listed; it appears once the next AY is added (by design). _(Coverage: CS-06)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- At Location A: **Student K** has LA Math in **AY 2027**: 2027-04-01 → 2028-03-31 (Not Started, next AY)
- At Location A: **Student B** has LA English in **AY 2026**: 2026-11-01 → 2027-03-31 (Not Started, current AY)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A | Academic Year filter = **AY 2026**; Student Course Status = Active + Not Started; **Student B is listed; Student K is not listed** | today = 2026-10-20 (JST); current AY = AY 2026; AY filter = AY 2026 AND status ∈ {Active, Not Started} |
| 2 | HQ or CM Staff opens the filter, adds **AY 2027** to Academic Year and clicks Save | **Student K is now listed** together with Student B | AY filter = [AY 2026, AY 2027]; K.start 2027-04-01 > today → Not Started |
| 3 | HQ or CM Staff opens the filter, removes **AY 2026** (only AY 2027 selected) and clicks Save | Only **Student K** is listed | AY filter = [AY 2027] |

**Severity:** minor
**Priority:** medium

---

### Lesson Calendar – Student List – Student Course Status Filter – Selection changed from default – List matches every selected status

**Description:** AC-01 — Decision Table — Changing the default selection filters the list by the selected statuses combined with OR. _(Coverage: CS-07)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- At Location A: **Student A** has LA 2026-04-01 → 2027-03-31 (Active)
- At Location A: **Student B** has LA 2026-11-01 → 2027-03-31 (Not Started)
- At Location A: **Student C** has LA 2026-04-01 → 2026-09-30 (Inactive)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A | Student A and Student B are listed (default) | today = 2026-10-20 (JST); current AY = AY 2026; selection = [Active, Not Started] |
| 2 | HQ or CM Staff opens the filter, removes **Not Started** and clicks Save | Only **Student A** is listed | selection = [Active] |
| 3 | HQ or CM Staff opens the filter, removes **Active**, adds **Not Started** and clicks Save | Only **Student B** is listed | selection = [Not Started] |
| 4 | HQ or CM Staff opens the filter, selects **Active, Not Started and Inactive** and clicks Save | Students A, B and C are listed | selection = [Active, Not Started, Inactive] |
| 5 | HQ or CM Staff opens the filter, removes all three status chips and clicks Save | Students A, B and C are listed (no status condition) | selection = [] → all statuses |

**Severity:** minor
**Priority:** medium

---

### Lesson Calendar – Student List – Default Filter combined with Course filter and name search – Only rows matching all conditions shown

**Description:** AC-01 — Pairwise — The default status filter is combined with AND with other filters and the name search. _(Coverage: CS-08)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- At Location A: **Student A** has LA Math 2026-04-01 → 2027-03-31 (Active)
- At Location A: **Student B** has LA English 2026-11-01 → 2027-03-31 (Not Started)
- At Location A: **Student L** has LA Math 2026-12-01 → 2027-03-31 (Not Started)
- At Location A: **Student M** has LA Math 2026-04-01 → 2026-09-30 (Inactive)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A | Students A, B and L are listed; Student M is not listed | today = 2026-10-20 (JST); current AY = AY 2026 |
| 2 | HQ or CM Staff opens the filter, selects Course Master = **Math** and clicks Save | Student Course Status still shows Active + Not Started; **Students A and L** are listed; B (English) and M (Inactive) are not | course = Math; status = [Active, Not Started] |
| 3 | HQ or CM Staff types "Student L" in the Search Student Name box | Only **Student L** is listed | keyword = Student L |
| 4 | HQ or CM Staff clears the search box and types "Student M" | No row is listed | keyword = Student M; M is Inactive |

**Severity:** minor
**Priority:** medium

---

### Lesson Calendar – Student List – Filter Reset + Save – All filters cleared except calendar location; Inactive and other-AY LAs listed

**Description:** AC-01 — Decision Table + Negative — Reset clears Student Course Status, Academic Year and Type (all filters except the calendar location); after Save the list includes Inactive LAs and LAs of other academic years. The default is NOT restored. _(Coverage: CS-09)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- At Location A: **Student A** has LA 2026-04-01 → 2027-03-31 (Active, AY 2026)
- At Location A: **Student B** has LA 2026-11-01 → 2027-03-31 (Not Started, AY 2026)
- At Location A: **Student C** has LA 2026-04-01 → 2026-09-30 (Inactive, AY 2026)
- At Location A: **Student N** has LA 2025-04-01 → 2026-03-31 (Inactive, **AY 2025**)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A | Students A and B are listed (default) | today = 2026-10-20 (JST); current AY = AY 2026 |
| 2 | HQ or CM Staff opens the filter and clicks **Reset** | In the popover: Location keeps the chip **Location A**; Academic Year, Type and **Student Course Status are empty** (no Active / Not Started chips) | after_reset: location = Location A; others = empty |
| 3 | HQ or CM Staff clicks **Save** | Students **A, B, C and N** are listed | status = [] → all statuses; AY = [] → all years |
| 4 | HQ or CM Staff opens the filter again | Student Course Status is still empty — the Active + Not Started default is **not** restored by Reset | — |

**Severity:** major
**Priority:** high

---

### Lesson Calendar – Student List – Custom status selection then page reload – Default Active and Not Started re-applied

**Description:** AC-01 — Scenario — A custom selection is not kept after a page reload; the default is re-applied. _(Coverage: CS-10)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- At Location A: **Student A** has LA 2026-04-01 → 2027-03-31 (Active)
- At Location A: **Student B** has LA 2026-11-01 → 2027-03-31 (Not Started)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A, opens the filter, keeps only **Active** and clicks Save | Only Student A is listed | today = 2026-10-20 (JST); current AY = AY 2026; selection = [Active] |
| 2 | HQ or CM Staff reloads the browser page | Lesson Calendar reloads; Students A and B are listed | after reload |
| 3 | HQ or CM Staff opens the filter | Student Course Status shows **Active ×** and **Not Started ×** again | default re-applied |

**Severity:** minor
**Priority:** medium

---

### Lesson Calendar – Student List – Custom status selection then calendar location or view changed – Selection kept; only Location chip changes

**Description:** AC-01 — Scenario — Changing the calendar location or view keeps the user's filter selection; only the Location chip follows the calendar location. _(Coverage: CS-11)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- HQ or CM Staff is also affiliated with **Location B**
- At Location A: **Student A** has LA 2026-04-01 → 2027-03-31 (Active); **Student B** has LA 2026-11-01 → 2027-03-31 (Not Started)
- At Location B: **Student P** has LA 2026-04-01 → 2027-03-31 (Active); **Student Q** has LA 2026-12-01 → 2027-03-31 (Not Started)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A in **Weekly** view, opens the filter, keeps only **Active** and clicks Save | Only Student A is listed | today = 2026-10-20 (JST); current AY = AY 2026; selection = [Active] |
| 2 | HQ or CM Staff switches the calendar to **Daily** view | Only Student A is still listed; the filter still shows only **Active** | view = Daily |
| 3 | HQ or CM Staff changes the calendar location to **Location B** | Only **Student P** is listed (Student Q, Not Started, is not) | location = Location B |
| 4 | HQ or CM Staff opens the filter | Location chip = **Location B**; Student Course Status still shows only **Active** (the default is not re-applied) | — |

**Severity:** minor
**Priority:** medium

---

### Lesson Master – Student List – Student Course Status Filter – First open – Only Active pre-selected (unchanged)

**Description:** Scope (BR-13) — Regression — The Lesson Master student list shares the same component but keeps the Active-only default. _(Coverage: CS-12)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- At Location A: **Student A** has LA 2026-04-01 → 2027-03-31 (Active); **Student B** has LA 2026-11-01 → 2027-03-31 (Not Started)
- A Lesson Master record exists at Location A for AY 2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Lesson Master record and its Student list | The Student list loads | today = 2026-10-20 (JST); current AY = AY 2026 |
| 2 | HQ or CM Staff opens the Student list filter | Student Course Status shows **Active ×** only; **Not Started is not selected** | Lesson Master default = [Active] |
| 3 | HQ or CM Staff looks at the Student list | Student A is listed; **Student B is not listed** | B = Not Started |

**Severity:** major
**Priority:** high

---

### Lesson Calendar – Student List – Student Course Status Filter – Japanese language – Field and option labels in Japanese

**Description:** AC-01 — Component — Field and option labels are translated when the user's language is Japanese. _(Coverage: CS-13)_

**Preconditions:**
- Academic Year **AY 2026** = 2026-04-01 → 2027-03-31 (current AY); **AY 2027** = 2027-04-01 → 2028-03-31
- HQ or CM Staff is logged in to Salesforce and is affiliated with **Location A**
- HQ or CM Staff's Salesforce Time Zone = (GMT+09:00) Japan Standard Time
- HQ or CM Staff's Salesforce language = 日本語 (Japanese)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A and opens the Student list filter | Field label shows **生徒コースのステータス**; default chips show **アクティブ** and **未来のコース** | today = 2026-10-20 (JST); current AY = AY 2026; language = ja |
| 2 | HQ or CM Staff opens the Student Course Status option list | Options show **アクティブ**, **未来のコース**, **過去のコース** | — |

**Severity:** trivial
**Priority:** low

---

### Lesson Calendar – Student List – Timezone gap, user behind location (ICT vs JST) – LA near midnight JST classified by the user's own date

**Description:** AC-02 (Q3 assumption) — BVA + Decision Table — The status is decided by the logged-in user's Salesforce timezone (date only). An ICT (GMT+7) user and a JST user see a different status for LAs whose start/end falls between 00:00 and 02:00 JST. _(Coverage: CS-15)_

**Preconditions:**
- Academic Year AY 2026 = 2026-04-01 → 2027-03-31 (current AY)
- **User 1** (HQ or CM Staff) Salesforce Time Zone = (GMT+09:00) Japan Standard Time, affiliated with Location A
- **User 2** (HQ or CM Staff) Salesforce Time Zone = (GMT+07:00) Indochina Time (Asia/Ho_Chi_Minh), affiliated with Location A
- At Location A: **Student R** has an LA with Start Date Time **2026-10-21 00:30 JST (= 2026-10-20 22:30 ICT)**, End 2027-03-31
- At Location A: **Student S** has an LA with Start 2026-04-01, End Date Time **2026-10-20 01:00 JST (= 2026-10-19 23:00 ICT)**
- LA date-times above are set on the LA records directly (record edit / data import)
- Run window: 2026-10-20 10:00–20:00 JST so both users are on the same calendar date 2026-10-20

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | User 1 (JST) opens Lesson Calendar for Location A | **Student S** is listed; **Student R** is listed | today (JST) = 2026-10-20; R.start = 2026-10-21 00:30 JST → date 2026-10-21 > today → Not Started; S.end = 2026-10-20 01:00 JST → date 2026-10-20 = today → Active |
| 2 | User 1 opens the filter, keeps only **Active** and clicks Save | Only **Student S** is listed | JST: R = Not Started, S = Active |
| 3 | User 2 (ICT) opens Lesson Calendar for Location A | **Student R** is listed; **Student S is not listed** | today (ICT) = 2026-10-20; R.start = 2026-10-20 22:30 ICT → date = today → Active; S.end = 2026-10-19 23:00 ICT → date < today → Inactive (hidden) |
| 4 | User 2 opens the filter, keeps only **Active** and clicks Save | Only **Student R** is listed | ICT: R = Active, S = Inactive |

**Severity:** minor
**Priority:** medium

---

### Lesson Calendar – Student List – Timezone gap, user ahead of location (Brisbane vs JST) – LA near midnight JST classified by the user's own date

**Description:** AC-02 (Q3 assumption) — BVA + Decision Table — A user on Australia/Brisbane (GMT+10, no daylight saving) is one hour ahead of JST; LAs starting/ending between 23:00 and 24:00 JST fall on the next date for that user. _(Coverage: CS-16)_

**Preconditions:**
- Academic Year AY 2026 = 2026-04-01 → 2027-03-31 (current AY)
- **User 1** (HQ or CM Staff) Salesforce Time Zone = (GMT+09:00) Japan Standard Time, affiliated with Location A
- **User 3** (HQ or CM Staff) Salesforce Time Zone = (GMT+10:00) Australian Eastern Standard Time (Australia/Brisbane), affiliated with Location A
- At Location A: **Student T** has an LA with Start Date Time **2026-10-20 23:30 JST (= 2026-10-21 00:30 AEST)**, End 2027-03-31
- At Location A: **Student U** has an LA with Start 2026-04-01, End Date Time **2026-10-19 23:30 JST (= 2026-10-20 00:30 AEST)**
- LA date-times above are set on the LA records directly (record edit / data import)
- Run window: 2026-10-20 10:00–22:00 JST (= 11:00–23:00 AEST) so both users are on 2026-10-20

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | User 1 (JST) opens Lesson Calendar for Location A | **Student T** is listed; **Student U is not listed** | today (JST) = 2026-10-20; T.start = 2026-10-20 23:30 JST → date = today → Active; U.end = 2026-10-19 23:30 JST → date < today → Inactive (hidden) |
| 2 | User 1 opens the filter, keeps only **Not Started** and clicks Save | No row for Student T or U | JST: T = Active, U = Inactive |
| 3 | User 3 (Brisbane) opens Lesson Calendar for Location A | **Student T** is listed; **Student U** is listed | today (AEST) = 2026-10-20; T.start = 2026-10-21 00:30 AEST → date > today → Not Started; U.end = 2026-10-20 00:30 AEST → date = today → Active |
| 4 | User 3 opens the filter, keeps only **Not Started** and clicks Save | Only **Student T** is listed | AEST: T = Not Started, U = Active |

**Severity:** minor
**Priority:** medium

---

### Lesson Calendar – Student List – Timezone gap, UTC user vs JST user – LA crossing the JST/UTC date boundary classified by the user's own date

**Description:** AC-02 (Q3 assumption) — BVA — Mandatory JST↔UTC boundary: an LA starting 2026-10-21 08:00 JST is 2026-10-20 23:00 UTC; a UTC user sees it as Active while a JST user sees it as Not Started. _(Coverage: TZ-UTC)_

**Preconditions:**
- Academic Year AY 2026 = 2026-04-01 → 2027-03-31 (current AY)
- **User 1** (HQ or CM Staff) Salesforce Time Zone = (GMT+09:00) Japan Standard Time, affiliated with Location A
- **User 4** (HQ or CM Staff) Salesforce Time Zone = (GMT+00:00) Coordinated Universal Time (UTC), affiliated with Location A
- At Location A: **Student V** has an LA with Start Date Time **2026-10-21 08:00 JST (= 2026-10-20 23:00 UTC)**, End 2027-03-31
- At Location A: **Student W** has an LA with Start 2026-04-01, End Date Time **2026-10-20 08:00 JST (= 2026-10-19 23:00 UTC)**
- LA date-times above are set on the LA records directly (record edit / data import)
- Run window: 2026-10-20 10:00–20:00 JST (= 01:00–11:00 UTC) so both users are on 2026-10-20

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | User 1 (JST) opens Lesson Calendar for Location A, opens the filter, keeps only **Active** and clicks Save | Only **Student W** is listed | today (JST) = 2026-10-20; V.start = 2026-10-21 08:00 JST → Not Started; W.end = 2026-10-20 08:00 JST → date = today → Active |
| 2 | User 4 (UTC) opens Lesson Calendar for Location A, opens the filter, keeps only **Active** and clicks Save | Only **Student V** is listed | today (UTC) = 2026-10-20; V.start = 2026-10-20 23:00 UTC → date = today → Active; W.end = 2026-10-19 23:00 UTC → Inactive |
| 3 | User 4 opens the filter, restores the default (Active + Not Started) and clicks Save | **Student V** is listed; **Student W is not listed** | UTC: W = Inactive → hidden by default |

**Severity:** minor
**Priority:** medium

---
