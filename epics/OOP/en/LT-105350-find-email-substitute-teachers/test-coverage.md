# Test Coverage: LT-105350 — [EN] Finding and Emailing Substitute Teacher Candidates

**Jira:** https://manabie.atlassian.net/browse/LT-105350
**Date:** 2026-07-22

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| BR-01 | AC 01.2 | Entry point is the existing "Add Teacher" button on Lesson Detail — not a separate menu |
| BR-02 | AC 01.2 | Clicking "Add Teacher" opens the Teacher list popup (existing popup, enhanced) |
| BR-03 | AC 02.1 | Available Teacher Checkbox / "Only teachers free at this time": when ON, filters teachers whose registered working-hours record fully covers the target lesson time (`staff_start_time <= lesson_start_time < lesson_end_time <= staff_end_time`) |
| BR-04 | AC 02.1 | Available Teacher Checkbox / "Only teachers free at this time": when ON, also excludes teachers with existing Draft/Published lessons overlapping the target lesson time in any location; Cancelled/Completed lessons are ignored |
| BR-05 | AC 02.1 | Location filter: brand-level first, then exclude lower-level Locations (same pattern as Master Event segments) |
| BR-06 | AC 02.1 | EN teacher affiliation is at Brand or Area level |
| BR-07 | AC 02.1 | EN teachers can be community plus users OR contact-level users |
| BR-08 | AC 02.1 | Flagged Teacher Checkbox default: UNchecked (flagged teachers excluded by default) |
| BR-09 | AC 02.1 | When Flagged checkbox is enabled: teachers whose Contact has "Flagged" checked are included in results |
| BR-10 | AC 02.1 | "Flagged" column shown in teacher list within Add Teacher popup |
| BR-11 | AC 02.1 | Matching teacher count is updated in real time as filters change |
| BR-12 | AC 02.1 | Filter by eligible subjects `[TBC — subject scope for EN unconfirmed]` |
| BR-13 | AC 03.1 | "Send Email" with 0 selected candidates: prevent opening editor + show error OR disable button |
| BR-14 | AC 03.1 | Error message — EN: "Please select one or more Teachers." / JP: "1人以上の講師を選択してください" |
| BR-15 | AC 03.2 | Offer-emails bulk-sent to all selected candidates simultaneously |
| BR-16 | AC 03.2 | Selected candidate count displayed in email editor |
| BR-17 | AC 03.2 | Email editor opens with PRD template: subject/title `代講をお願いいたします` and body `案件名：` / `時間：`; body is text-only and template can be configured per partner |
| BR-18 | AC 03.2 | System generates recipient list → staff sends via company email tool (outside Manabie/SF) |
| BR-19 | AC 03.2 | Emails sent separately or BCC; each candidate must not see other candidates' addresses |
| BR-20 | AC 03.2 | Post-send operations (reply, negotiate, final teacher assignment) outside Manabie/SF |
| BR-21 | AC 03.2 | Email log is attached to each selected teacher Contact after send |
| BR-22 | AC 03.2 | Receiver volume supports around 50 and sometimes 70-80 recipients; no arbitrary 50 cap. Non-SF-account 5,000 emails/day limit, if applicable, is handled visibly; SF-account recipients have no such cap |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.2 | BR-01 | Display completeness |
| AC 01.2 | BR-02 | Display completeness |
| AC 02.1 | BR-03 | Conditional logic, Date/Time logic |
| AC 02.1 | BR-04 | Conditional logic, Data integrity, Date/Time logic |
| AC 02.1 | BR-05 | Conditional logic |
| AC 02.1 | BR-06 | Permission logic |
| AC 02.1 | BR-07 | Conditional logic |
| AC 02.1 | BR-08 | Display completeness, Conditional logic |
| AC 02.1 | BR-09 | Conditional logic, Data integrity |
| AC 02.1 | BR-10 | Display completeness |
| AC 02.1 | BR-11 | Display completeness, Conditional logic |
| AC 02.1 | BR-12 | Conditional logic `[TBC]` |
| AC 03.1 | BR-13 | Validation logic, Conditional logic |
| AC 03.1 | BR-14 | Display completeness |
| AC 03.2 | BR-15 | Data integrity, Cross-system impact |
| AC 03.2 | BR-16 | Display completeness |
| AC 03.2 | BR-17 | Display completeness, Validation logic |
| AC 03.2 | BR-18 | Cross-system impact |
| AC 03.2 | BR-19 | Data integrity |
| AC 03.2 | BR-20 | Cross-system impact |
| AC 03.2 | BR-21 | Data integrity, Cross-system impact |
| AC 03.2 | BR-22 | Boundary Value, Validation logic, Cross-system impact |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Display completeness | Component, Negative (field absent) |
| Conditional logic | Decision Table, Negative |
| Data integrity | CRUD, Regression, Decision Table |
| Permission logic | Permission Matrix, Decision Table |
| Validation logic | Equivalence Partitioning, Negative |
| Cross-system impact | Regression, CRUD |
| Date/Time logic | Decision Table, Boundary Value Analysis, Timezone Regression |
| Boundary Value | Boundary Value Analysis, Volume Regression |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.2 | BR-01: "Add Teacher" button visible on Lesson Detail as entry point | Display completeness | Component | Medium | Smoke |
| AC 01.2 | BR-02: Clicking "Add Teacher" opens Teacher list popup | Display completeness | Component | High | Standard |
| AC 02.1 | BR-03: Available Teacher Checkbox — working-hours coverage required when ON | Conditional logic, Date/Time logic | Decision Table, Boundary Value Analysis | Critical | Deep |
| AC 02.1 | BR-04: Available Teacher Checkbox — no-overlap check required when ON | Conditional logic, Data integrity, Date/Time logic | Decision Table, Boundary Value Analysis, Negative | Critical | Deep |
| AC 02.1 | BR-05: Location filter — brand-level first, then narrow by lower-level | Conditional logic | Decision Table | High | Deep |
| AC 02.1 | BR-06: EN affiliation — Brand or Area level | Permission logic | Permission Matrix | High | Standard |
| AC 02.1 | BR-07: EN teacher type — community plus OR contact-level | Conditional logic | Decision Table | High | Standard |
| AC 02.1 | BR-08: Flagged checkbox default UNchecked (flagged excluded by default) | Display completeness, Conditional logic | Component, Decision Table | High | Standard |
| AC 02.1 | BR-09: Flagged checkbox enabled → flagged teachers included in list | Conditional logic, Data integrity | Decision Table, Negative | High | Deep |
| AC 02.1 | BR-10: "Flagged" column visible in teacher list | Display completeness | Component | Medium | Smoke |
| AC 02.1 | BR-11: Match count updates in real time as filters change | Display completeness, Conditional logic | Component, Scenario | Medium | Standard |
| AC 02.1 | BR-12: Subject filter `[TBC]` | Conditional logic | Decision Table | Medium | Standard |
| AC 03.1 | BR-13: "Send Email" with 0 selected → error or disabled button | Validation logic, Conditional logic | Equivalence Partitioning, Negative | Critical | Deep |
| AC 03.1 | BR-14: Error message text — EN and JP exact strings | Display completeness | Component | Medium | Standard |
| AC 03.2 | BR-15: Bulk email sent to all selected candidates | Data integrity, Cross-system impact | CRUD, Regression | Critical | Deep |
| AC 03.2 | BR-16: Candidate count shown in email editor | Display completeness | Component | Medium | Standard |
| AC 03.2 | BR-17: Email subject/body template from PRD, text only | Display completeness, Validation logic | Component, Equivalence Partitioning | High | Standard |
| AC 03.2 | BR-18: System generates recipient list → external email tool | Cross-system impact | Regression, CRUD | High | Deep |
| AC 03.2 | BR-19: BCC/separate — each candidate cannot see others' email | Data integrity | CRUD, Negative | Critical | Deep |
| AC 03.2 | BR-20: Post-send operations outside Manabie/SF | Cross-system impact | Smoke | Low | Smoke |
| AC 03.2 | BR-21: Email logs attached to selected teacher Contacts | Data integrity, Cross-system impact | CRUD, Regression | High | Deep |
| AC 03.2 | BR-22: Receiver volume and daily limit handling | Boundary Value, Validation logic, Cross-system impact | Boundary Value Analysis, Negative, Regression | High | Deep |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| BR-03/BR-04: Combined available-teacher filter | Incorrect AND logic could show teachers who pass only one condition: within working hours but already booked, or conflict-free but outside working hours | Decision table covering: pass both (included), fail working-hours only (excluded), fail existing-lesson overlap only (excluded), fail both (excluded), checkbox OFF (combined filter not applied) |
| BR-04: No-overlap check | Incorrect filter could allow double-booking a teacher at the same time or wrongly hide teachers whose only overlaps are Cancelled/Completed | Decision table covering: Draft/Published overlap excluded; Cancelled/Completed overlap ignored; adjacent lesson not overlap; test both checkbox ON and OFF |
| BR-13: "Send Email" guard | If the guard fails, the email editor opens with no recipients, causing misleading empty-send behavior | Negative: 0 selected → assert error message text verbatim; test button disabled state if that approach is used |
| BR-15: Bulk email send | Core feature — failure means no emails sent; partial send (some succeed, some fail) is undocumented | CRUD path: select N teachers, open editor, send; verify system generates complete recipient list |
| BR-19: BCC/separate recipient privacy | Violating BCC means candidates can see each other's contact info — a serious privacy issue | CRUD path: verify email headers or Manabie-generated list does not expose all addresses in To/CC field |
| BR-21: Email log on Contact | Missing logs prevent staff from auditing which candidates were contacted | CRUD path: send to multiple candidates, verify one email log per candidate Contact with subject/body/timestamp |
| BR-22: Receiver volume/limit | A hidden cap could block expected EN usage (50, sometimes 70-80), or daily limit errors could silently drop recipients | Boundary path: send 50 and 80 recipients; negative path for non-SF-account 5,000/day limit; verify visible handling |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| BR-02: Popup opens | Core navigation; if popup fails to open, the entire feature is blocked | Standard: happy path + popup does not re-open on double-click |
| BR-03: Working-hours coverage | Incorrect working-hours comparison means unavailable teachers appear or available teachers are hidden | Decision table + boundary checks: exact boundary match included; start-after or end-before partial coverage excluded; Off Day/no working-hours record excluded; JST date used |
| BR-05: Location filter (brand-level) | Incorrect scope means wrong teacher pool; EN-specific brand affiliation logic differs from core | Deep: brand filter shows brand-level teachers; narrow by sub-location; verify count |
| BR-06: EN affiliation type | Brand vs Area level affiliation must both be valid; community plus vs contact-level must both appear | Permission matrix: community plus user + Area affiliation; contact-level user + Brand affiliation |
| BR-07: Community plus vs contact-level | Both teacher types must appear in results | Decision table: each type independently |
| BR-08: Flagged checkbox default UNchecked | Wrong default (checked) would expose flagged teachers silently | Component: on popup open, assert checkbox is unchecked by default |
| BR-09: Flagged teacher inclusion/exclusion | Wrong toggle logic could either show dangerous candidates or hide valid ones | Decision table: 4 states (checkbox ON/OFF × teacher Flagged/Unflagged) |
| BR-18: Recipient list generation | If recipient list is incomplete or malformed, some candidates won't receive the email | CRUD path + regression: verify list contains all selected teachers' emails |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| BR-01: Entry point | Wrong entry point (e.g., new "Find substitute" menu was originally in Jira description) | Smoke: "Add Teacher" button visible; no separate "Find substitute" menu item |
| BR-10: Flagged column display | Column absence means staff cannot distinguish flagged candidates visually | Smoke: column header "Flagged" visible in teacher list |
| BR-11: Real-time count | Count mismatch causes confusion; not a data error | Standard: change filter, assert count updates without page reload |
| BR-12: Subject filter [TBC] | Blocked on clarification; test if and when confirmed | Standard: subject filter visible; filtering correctly limits list |
| BR-14: Error message exact text | Wrong text (especially JP) causes localization defect | Standard: assert verbatim EN and JP strings |
| BR-16: Candidate count in editor | Cosmetic but affects trust | Standard: select N candidates, open editor, assert count = N |
| BR-17: Email subject/body template | Wrong template or translation causes wrong customer-facing email content | Standard: open editor, assert subject/title `代講をお願いいたします` and body `案件名：` / `時間：`; assert text-only editing |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| BR-01/02 Entry point + popup | `epics/cross-domain/LT-96237-*/test-cases/add-teacher-popup-working-status-filter.md` (tests popup opening generally) | Partial — existing tests open the popup but don't verify the EN "Find substitute" entry via "Add Teacher" button specifically | ✅ New smoke TC: EN entry point via "Add Teacher" on Lesson Detail |
| BR-03 Available Teacher filter (working hours) | `epics/cross-domain/LT-96237-*/test-cases/add-teacher-popup-working-status-filter.md` and Jira `LT-64009` | Partial — existing tests cover Working Status dropdown and free-time label, not working-hour containment against target lesson time | ✅ New DT/BVA TCs: checkbox ON with exact/full coverage included; start-after/end-before partial coverage excluded; Off Day/no working-hours excluded |
| BR-04 No-overlap check (new) | Clashing alert overlap rules provide boundary precedent; no substitute-candidate filter test exists | Partial — overlap concept exists, but not as candidate exclusion | ✅ New DT/BVA TCs: exact same-time conflict excluded; partial and contains overlap excluded; Draft/Published conflict excluded; Cancelled/Completed conflict ignored; both adjacent boundaries not excluded; cross-location/non-affiliated existing lesson excluded |
| BR-05 Brand-level Location filter | None | None | ✅ New DT TCs: brand → sub-location narrowing; EN teacher at brand vs area level |
| BR-06 EN affiliation type | None | None | ✅ New permission matrix TCs: Brand affiliation; Area affiliation |
| BR-07 Community plus vs contact-level | None | None | ✅ New decision table TCs: both user types appear |
| BR-08 Flagged checkbox default | None | None | ✅ New component TC: default state UNchecked on popup open |
| BR-09 Flagged include/exclude | None | None | ✅ New DT TCs: all 4 toggle × flag combinations |
| BR-10 Flagged column display | None | None | ✅ New smoke TC: Flagged column visible |
| BR-11 Real-time count | None | None | ✅ New scenario TC: change filter → count updates |
| BR-12 Subject filter [TBC] | None | None | ✅ New TCs pending clarification on subject scope |
| BR-13 Send Email guard (0 selection) | None | None | ✅ New negative TCs: 0 selected → error; 0 selected → button disabled |
| BR-14 Error message text (EN + JP) | None | None | ✅ New component TCs: assert exact error strings |
| BR-15 Bulk email send | None | None | ✅ New CRUD TCs: select candidates → open editor → send; all candidates in recipient list |
| BR-16 Candidate count in editor | None | None | ✅ New component TC: count = N selected |
| BR-17 Email subject/body PRD template | None | None | ✅ New component TC: default subject/title + body template + text-only editing |
| BR-18 Recipient list generation | None | None | ✅ New cross-system TC: system-generated list contains all selected teachers |
| BR-19 BCC/separate privacy | None | None | ✅ New CRUD TC: recipient list does not expose all addresses; BCC behavior verified |
| BR-20 Post-send (out of scope) | N/A — external tool | N/A | Smoke only: note that post-send is outside Manabie/SF |
| BR-21 Email logs on Contact | None | None | ✅ New CRUD TC: email activity/log attached to each selected teacher Contact |
| BR-22 Receiver volume / daily limit | None | None | ✅ New BVA/negative TCs: 50 and 70-80 recipients; non-SF 5,000/day limit handling; SF account no cap |

---

## 7a. Downstream Effects Inventory Table (Step G — CRUD/state-change rules)

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification |
|---|---|---|---|
| Staff enables Available Teacher Checkbox / "Only teachers free at this time" | Teachers outside registered working-hours coverage removed from list | Add Teacher popup — teacher list | TC in teacher-filter.md |
| Staff enables Available Teacher Checkbox / "Only teachers free at this time" | Teachers with overlapping existing lessons in any location removed from list | Add Teacher popup — teacher list | TC in teacher-filter.md |
| Staff disables Available Teacher Checkbox / "Only teachers free at this time" | Working-hours/no-overlap availability checks are not applied; other filters still apply | Add Teacher popup — teacher list | TC in teacher-filter.md |
| Staff enables Flagged Teacher Checkbox | Flagged teachers added to results + Flagged column shows flag | Add Teacher popup — teacher list | TC in teacher-filter.md |
| Staff disables Flagged Teacher Checkbox | Flagged teachers removed from results | Add Teacher popup — teacher list | TC in teacher-filter.md |
| Filter change (any) | Real-time count updates without page reload | Match count display in popup | TC in teacher-filter.md |
| Staff clicks "Send Email" with candidates selected | Email editor popup opens with candidate count, default subject/title, and PRD body template | Email editor popup | TC in email-compose-send.md |
| Staff clicks "Send Email" with 0 selected | Error shown OR button disabled; email editor does NOT open | Add Teacher popup — error message | TC in email-compose-send.md |
| Staff confirms send in email editor | System generates recipient list for all selected candidates | SF/Manabie internal (recipient list) | TC in email-compose-send.md |
| Staff confirms send in email editor | Emails dispatched via company email tool (BCC/separate) | External email tool | TC in email-compose-send.md |
| Staff confirms send in email editor | Each candidate email is sent without revealing other recipients | Email headers / BCC | TC in email-compose-send.md |
| Staff confirms send in email editor | Email log is attached to each selected teacher Contact | Contact Activity / Email log | TC in email-compose-send.md |
| Staff selects 50 or 70-80 candidates | Flow supports expected EN recipient volume without arbitrary 50-recipient cap | Email editor / recipient list | TC in email-compose-send.md |
| Staff confirms send → post-email | Staff can change teacher assignment in Lesson Detail (outside this feature) | SF Lesson Detail — Lesson Teacher section | Smoke only (out of scope for this feature) |

---

## 7b. Display & Ordering Inventory Table (Step H)

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Add Teacher popup — Filter area | Location Selector, Available Teacher Checkbox / "Only teachers free at this time", Flagged Teacher Checkbox, Match count display | Subject filter (TBC) | None specified | Filter labels per localization table: "Area" / "エリア", "Subject" / "科目", "Working Hour" / "勤務可能時間", "Commutable day of week" / "勤務可能曜日", "Flagged teacher" / "要注意講師" |
| Add Teacher popup — Teacher list | Teacher name, Flagged column | Flagged column value (Y/N per teacher) | None specified | Column header: "Flagged" / "要注意講師" |
| Email editor popup | Email subject/title, Email body template, Candidate count, Send button | — | — | Subject/title: "代講をお願いいたします"; Body: "案件名：" / "時間："; Error: "Please select one or more Teachers." / "1人以上の講師を選択してください"; Button label: "Send Email" / "メールを送信する" |

**H.1 — N/A: No Figma URL in spec.** PRD draft has no linked Figma file. Localization table from PRD used as text source.

---

## 7c. Edge-Case Checklist Findings (Step 4.5)

**A. Configuration-driven thresholds:**
- BR-17 (email subject/body template configurable per partner): ✅ Test EN default subject/body template AND partner-configured text-only behavior if applicable.
- BR-22 (receiver volume/limit): ✅ Test EN expected volume around 50 and 70-80. If implementation uses a non-SF-account 5,000 emails/day limit, assert visible handling when exceeded and no silent recipient drops.

**B. Date/Time logic:**
- BR-03/BR-04 (Available Teacher filter compares to lesson date/time): ✅ TZ risk — lesson stored in UTC, teacher availability window in local JST. Must assert filter uses displayed lesson time (JST), not raw UTC. Every TC must declare `lesson_datetime = YYYY-MM-DD HH:mm JST`.
- BR-03 (Working-hours coverage from LT-64009): ✅ Boundary risk — available only when `staff_start_time <= lesson_start_time < lesson_end_time <= staff_end_time`. Exact boundary equality is included; start-after and end-before partial overlaps are excluded.
- BR-04 (Existing lesson overlap): ✅ Boundary risk — overlap is evaluated by teacher assignment across locations, not just selected affiliation/search location. Exact same-time, partial overlap, containing overlap, and Draft/Published statuses are conflicts; Cancelled/Completed and adjacent boundaries are not conflicts.
- BR-04 (Existing lesson overlap): ✅ Boundary risk — overlap is `existing_start < target_end AND target_start < existing_end`; adjacent lessons where one end equals the other start are not overlaps.

**C. Concurrent/stale state:**
- BR-03/BR-04: ✅ Teacher's schedule could change between popup open and send (e.g., teacher gets assigned another lesson while staff is selecting). Scope: low priority but note for regression.
- BR-15: ✅ Double-submit on "Send Email" — could trigger duplicate email sends. Test rapid re-click.

**D. Permission & role:**
- BR-13/BR-15 [ROLE GAP]: ✅ Role restriction for "Send Email" is unconfirmed. Pending clarification Q1. When confirmed, add permission matrix TC: authorized role can send; unauthorized role cannot.

**E. State transition:**
- No entity status transitions in this feature scope. N/A.

**F. Cross-system:**
- BR-18/BR-19: ✅ If external email tool is unavailable, the system-generated recipient list should not be silently discarded. No AC — MISSING BEHAVIOR (Q4). Cover as negative TC: email tool error → Manabie behavior TBD.

**G. Downstream effects:** Covered in §7a above.

**H. Display completeness & ordering:** Covered in §7b above.

---

## 8. Coverage Gaps vs. Existing Test Cases (Summary Table)

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Entry point + popup open (BR-01, BR-02) | LT-96237 add-teacher-popup tests | Partial | ✅ EN-specific smoke + component |
| Available Teacher filter — working-hours (BR-03) | LT-96237 working-status filter + LT-64009 working-hours epic | Partial | ✅ New: working-hour coverage decision table + boundaries |
| No-overlap check (BR-04) | Clashing alert overlap concept | Partial | ✅ New: substitute-candidate exclusion DT (Draft/Published overlap excluded; Cancelled/Completed overlap ignored; adjacent/no-lesson/cross-location × checkbox ON/OFF) |
| Location filter brand-level (BR-05) | None | None | ✅ New: brand → sub-location narrowing |
| EN affiliation type (BR-06, BR-07) | None | None | ✅ New: community plus + contact-level DT |
| Flagged checkbox default (BR-08) | None | None | ✅ New: component TC default state |
| Flagged include/exclude (BR-09, BR-10) | None | None | ✅ New: 4-state DT + column display smoke |
| Real-time count (BR-11) | None | None | ✅ New: scenario TC |
| Subject filter (BR-12) | None | None | ✅ New: pending TBC clarification |
| Send Email guard (BR-13, BR-14) | None | None | ✅ New: negative + exact text assertion |
| Bulk email send (BR-15) | None | None | ✅ New: CRUD + recipient list verification |
| Email editor display (BR-16, BR-17) | None | None | ✅ New: component TCs for candidate count + PRD subject/body template |
| Recipient list + BCC (BR-18, BR-19) | None | None | ✅ New: CRUD + privacy verification |
| Post-send out of scope (BR-20) | N/A | N/A | Smoke note only |
| Email logs on Contact (BR-21) | None | None | ✅ New: CRUD verification on teacher Contact Activity / Email log |
| Receiver volume / daily limit (BR-22) | None | None | ✅ New: BVA/negative TCs for 50, 70-80, non-SF 5,000/day, SF account no cap |

---

## 9. Suggested Test Suite Structure

```
epics/OOP/en/LT-105350-find-email-substitute-teachers/test-cases/
├── entry-point-and-popup.md      → US-01 (AC 01.1, AC 01.2) + BR-01, BR-02
│                                    Smoke: entry point via "Add Teacher" button;
│                                    popup opens; popup shows all filter areas
├── teacher-filter.md             → US-02 (AC 02.1) + BR-03–BR-12
│                                    Available Teacher Checkbox / "Only teachers free at this time"
│                                    (working-hours coverage + no existing lesson overlap);
│                                    Location filter (brand-level); EN affiliation types;
│                                    Flagged checkbox (default, include/exclude);
│                                    Flagged column display; real-time count;
│                                    Subject filter [TBC]
└── email-compose-send.md         → US-03 (AC 03.1, AC 03.2) + BR-13–BR-22
                                     Send Email guard (0 selection → error or disabled);
                                     exact error text EN + JP;
                                     email editor display (candidate count, PRD subject/body template);
                                     bulk send; recipient list; BCC/separate privacy;
                                     Contact email logs; receiver volume/limit handling
```
