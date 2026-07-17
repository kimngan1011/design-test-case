# Test Coverage: LT-101725 — Riso Lesson Publish Notifications to Teachers

**Jira:** https://manabie.atlassian.net/browse/LT-101725
**Date:** 2026-06-23
**Partner scope:** Riso only (config flag: On = Riso, Off = all other tenants)
**Platforms:** SF (single publish Chatter + bulk publish email) + BO (bulk publish email trigger)

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| BR-01 | AC-01 | Draft→Published (single publish) → SF Flow Builder creates exactly 1 Chatter post per lesson |
| BR-02 | AC-01 | Republish (Published→Draft→Published) → NEW Chatter post created; no deduplication |
| BR-03 | AC-02.1 | Flow Builder Step 1: detect lesson status change Draft→Published |
| BR-04 | AC-02.1 | Flow Builder Step 2: retrieve Lesson Teachers where working_status=Available AND working_type IN (Full Time, Part Time) |
| BR-05 | AC-02.1 | Flow Builder Step 3: create Chatter post with @mention of ALL retrieved teachers in a single post |
| BR-06 | AC-03 | Chatter post appears in the Chatter section of the SF Lesson Detail page |
| BR-07 | AC-03 | Chatter post visibility = LBAC rules (only SF users with access to lesson record can view) |
| BR-08 | AC-04 | Each Available Lesson Teacher must be @mentioned directly in the post body |
| BR-09 | AC-04 | Multiple teachers → single Chatter post (not one post per teacher) |
| BR-10 | AC-05 | Chatter post EN body: `@[Teacher Name] — [Lesson Name.hyperlink] has been published. Click to see more details.` |
| BR-11 | AC-05 | Chatter post JP body: `@[先生名] — [授業名.hyperlink]が公開されました。詳細はこちらをクリックしてください。` |
| BR-12 | AC-05 | Lesson Name in Chatter post = hyperlink to SF Lesson Detail page |
| BR-13 | AC-06 | SF notification center delivered via default SF @mention mechanism (no custom code); single publish only |
| BR-14 | AC-07 | ONLY @mentioned teachers receive notification center alert; LBAC-only users can VIEW post but get NO alert |
| BR-15 | AC-08 | Clicking Lesson Name hyperlink → opens SF Lesson Detail in new tab |
| BR-16 | AC-09 | Bulk publish → one email per Available Lesson Teacher per bulk action |
| BR-17 | AC-09 | Email content = published period summary (not individual lesson details) |
| BR-18 | AC-10 | One email per teacher per bulk action regardless of how many lessons in batch |
| BR-19 | AC-09 | Email subject EN: `Lesson Schedule Published` |
| BR-20 | AC-09 | Email subject JP: `授業予定が公開されました` |
| BR-21 | AC-09 | Email body EN: `Hi [Teacher Name], Lesson schedules for the following period have been published: Duration: Month Day, Year ~ Month Day, Year` |
| BR-22 | AC-09 | Email body JP: `[先生名]様, 下記の期間の授業が公開されました。 Year年Month月Day日～Year年Month月Day日` |
| BR-23 | AC-09 | Period calc (SF Lesson Calendar bulk publish) = calendar view Start Date ~ End Date |
| BR-24 | AC-09 | Period calc (SF Lesson List + BO) = earliest ~ latest lesson date across batch |
| BR-25 | AC-11 | Email failure → does NOT block or roll back lesson publication; failure logged |
| BR-26 | AC-01 | Teacher added to Published future-date lesson → Chatter post + SF notification for added teacher(s) |
| BR-27 | AC-03 | Config flag: On=Riso → feature active; Off=all other tenants → feature disabled |
| BR-28 | AC-09 | All lessons in batch already Published/Completed/Cancelled → NO email sent (silent skip) |

---

## 2. Logic Type Categorization

| BR | AC | Business Rule Summary | Logic Type |
|---|---|---|---|
| BR-01 | AC-01 | Draft→Published → 1 Chatter post | State transition, Cross-system impact |
| BR-02 | AC-01 | Republish → new Chatter post (no dedup) | State transition, Data integrity |
| BR-03 | AC-02.1 | Flow Builder: detect Draft→Published | State transition |
| BR-04 | AC-02.1 | Filter teachers: working_status=Available AND (FT or PT) | Conditional logic, Data integrity |
| BR-05 | AC-02.1 | Create Chatter post with @mention all retrieved teachers | Data integrity, Cross-system impact |
| BR-06 | AC-03 | Post in SF Lesson Detail Chatter section | Display completeness, Cross-system impact |
| BR-07 | AC-03 | Chatter post visibility = LBAC | Permission logic |
| BR-08 | AC-04 | Each Available teacher @mentioned in post body | Data integrity, Validation logic |
| BR-09 | AC-04 | Multiple teachers → single post | Data integrity |
| BR-10 | AC-05 | Chatter post EN body exact content | Validation logic, Display completeness |
| BR-11 | AC-05 | Chatter post JP body exact content | Validation logic, Display completeness |
| BR-12 | AC-05 | Lesson Name = hyperlink | Display completeness |
| BR-13 | AC-06 | SF notification center via @mention | State transition, Cross-system impact |
| BR-14 | AC-07 | Only @mentioned teachers receive notification alert | Permission logic, Conditional logic |
| BR-15 | AC-08 | Hyperlink → new tab | Display completeness |
| BR-16 | AC-09 | Bulk publish → email per Available teacher | State transition, Cross-system impact |
| BR-17 | AC-09 | Email body = period summary | Validation logic, Display completeness |
| BR-18 | AC-10 | One email per teacher per bulk action | Data integrity |
| BR-19 | AC-09 | Email subject EN exact text | Validation logic |
| BR-20 | AC-09 | Email subject JP exact text | Validation logic |
| BR-21 | AC-09 | Email body EN exact format | Validation logic, Display completeness |
| BR-22 | AC-09 | Email body JP exact format | Validation logic, Display completeness |
| BR-23 | AC-09 | Period calc: SF Calendar = view dates | Conditional logic, Boundary/range logic |
| BR-24 | AC-09 | Period calc: SF List + BO = batch min/max dates | Conditional logic, Boundary/range logic |
| BR-25 | AC-11 | Email failure → publish not blocked; logged | Data integrity |
| BR-26 | AC-01 | Teacher added to Published future-date lesson → Chatter post | State transition, Conditional logic, Boundary/range logic |
| BR-27 | AC-03 | Config flag On=Riso, Off=others | Permission logic, Conditional logic |
| BR-28 | AC-09 | 0 Draft→Published in batch → no email (silent skip) | Conditional logic, Data integrity |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| State transition | State Transition (all documented transitions positive; undocumented negative), CRUD |
| Conditional logic | Decision Table, Negative |
| Data integrity | CRUD, Regression, Decision Table |
| Permission logic | Permission Matrix, Decision Table |
| Validation logic | Equivalence Partitioning, Negative (exact text match) |
| Display completeness | Component (enumerate all required fields), Negative (field absent) |
| Boundary/range logic | Boundary Value Analysis (date boundaries), Negative |
| Cross-system impact | Regression, CRUD |

---

## 4. Mandatory Edge-Case Checklist (Step 4.5)

### A. Configuration-driven thresholds (triggered by BR-27)
- [x] Config = ON (Riso) → Chatter post and email triggered → positive test per notification path
- [x] Config = OFF (non-Riso) → no Chatter post, no email → negative isolation test (F-10 regression risk)
- [ ] N/A: No numeric threshold — boolean flag only; BVA at min/max not applicable

### B. Date / Time logic (triggered by BR-26, BR-23, BR-24)
- [x] BR-26 "future date" boundary: lesson date = today — include or exclude? (Q6 open — test both interpretations; expect clarification before TC freeze)
- [x] BR-26: lesson date = yesterday (past) → no Chatter post triggered (negative)
- [x] BR-23/BR-24 period calc: Start Date = End Date (single-day bulk publish) → "Month Day, Year ~ Month Day, Year" shows same date twice — verify format
- [x] BR-24: batch spans month boundary (e.g., May 31 ~ Jun 2) → date format verified per language (EN/JP)
- [ ] TZ gap: N/A — Riso is JP-tenant; JST does not observe DST; single timezone context

### C. Concurrent / stale state (triggered by bulk publish async nature)
- [x] Lesson changes status to Completed/Cancelled between bulk publish initiation and job execution → that lesson excluded from email period and notification
- [x] Email send initiated for teacher, teacher SF account deleted mid-send → failure logged, publish not blocked (AC-11)
- [ ] Double-submit of bulk publish: edge case at platform level; note for dev verification

### D. Permission & role (triggered by BR-04, BR-07, BR-14, BR-27)
- [x] Lesson Teacher (Available, Full Time) → @mentioned in Chatter post; receives SF notification center alert
- [x] Lesson Teacher (Available, Part Time) → @mentioned in Chatter post; receives SF notification center alert
- [x] Lesson Teacher (working_status=Unavailable) → NOT @mentioned; no notification
- [x] No teachers assigned to lesson → behavior TBD (Q5); test after clarification
- [x] HQ Admin (LBAC access) → can view Chatter post; does NOT receive notification center alert
- [x] Centre Manager (LBAC access) → can view Chatter post; does NOT receive notification center alert
- [x] BO Teacher (CPU) → SF account existence TBD (Q10); flag as dependency
- [x] Cross-tenant: non-Riso org (config=OFF) → no Chatter post, no email

### E. State transition (triggered by BR-01, BR-02, BR-16, BR-26)
- [x] Draft → Published (single publish) → Chatter post created ✅ positive
- [x] Draft → Published (bulk publish) → email sent ✅ positive
- [x] Published → Draft (unpublish) → NO notification triggered ✅ negative
- [x] Published → Completed → NO publish notification ✅ negative (not a publish event)
- [x] Draft → Published → Draft → Published (republish) → new Chatter post created on second publish ✅
- [x] Cancelled lesson included in bulk publish batch → excluded from email/notification (batch filters Draft only)
- [x] Teacher added to Published lesson with future date → Chatter post triggered ✅ special case

### F. Cross-system / cross-surface (triggered by BR-01, BR-13, BR-16)
- [x] Single publish: SF status change → Chatter post visible in SF Lesson Detail Chatter section within SLA
- [x] Single publish: Chatter post @mention → SF notification center alert received by teacher
- [x] Bulk publish from SF Lesson List → email received by teacher
- [x] Bulk publish from SF Lesson Calendar → email received by teacher
- [x] Bulk publish from BO Lesson Management → email received by teacher (BO surface must also trigger email)
- [x] Email failure does not affect lesson status → lesson remains Published after email failure
- [x] LT-98532 student push notification unaffected when LT-101725 teacher email fires (F-09 regression risk)

### G. Downstream Effects Inventory (MANDATORY)

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification TC |
|---|---|---|---|
| Single publish (Draft→Published) | Chatter post created in Lesson Detail Chatter section | SF Lesson Detail | chatter-post.md |
| Single publish | Available FT teacher @mentioned in post body | SF Chatter post body | chatter-post.md |
| Single publish | Available PT teacher @mentioned in post body | SF Chatter post body | chatter-post.md |
| Single publish | Unavailable teacher NOT @mentioned | SF Chatter post body | chatter-post.md |
| Single publish | Multiple teachers → single post (not per-teacher) | SF Chatter post | chatter-post.md |
| Single publish | Lesson Name in post = hyperlink to SF Lesson Detail | SF Chatter post | chatter-post.md |
| Single publish | Available teacher receives SF notification center alert | SF Notification Center | sf-notification.md |
| Single publish | LBAC-only user (HQ Admin) sees post, gets no notification alert | SF Notification Center + Chatter | sf-notification.md |
| Single publish | LBAC-only user (CM) sees post, gets no notification alert | SF Notification Center + Chatter | sf-notification.md |
| Single publish | Clicking hyperlink → SF Lesson Detail in new tab | SF browser navigation | chatter-post.md |
| Republish (Published→Draft→Published) | New Chatter post created | SF Lesson Detail Chatter | chatter-post.md |
| Republish | Old Chatter post(s) remain visible alongside new post | SF Lesson Detail Chatter | chatter-post.md |
| Republish | Teacher receives new notification center alert | SF Notification Center | sf-notification.md |
| Unpublish (Published→Draft) — inverse | NO new notification triggered | SF Notification Center | chatter-post.md |
| Teacher added to Published future-date lesson | Chatter post created for added teacher(s) | SF Lesson Detail Chatter | teacher-added.md |
| Teacher added to Published past-date lesson | NO Chatter post triggered (negative) | None | teacher-added.md |
| Bulk publish (SF Lesson List) | Email sent to each Available teacher | Teacher SF email | bulk-email.md |
| Bulk publish (SF Lesson Calendar) | Email sent to each Available teacher | Teacher SF email | bulk-email.md |
| Bulk publish (BO Lesson Mgmt) | Email sent to each Available teacher | Teacher SF email | bulk-email.md |
| Bulk publish | Email subject EN: `Lesson Schedule Published` | Teacher SF email | bulk-email.md |
| Bulk publish | Email subject JP: `授業予定が公開されました` | Teacher SF email | bulk-email.md |
| Bulk publish | Email body EN: correct format with period | Teacher SF email | bulk-email.md |
| Bulk publish | Email body JP: correct format with period | Teacher SF email | bulk-email.md |
| Bulk publish (SF Calendar) | Period = calendar view Start/End Date | Email body | bulk-email.md |
| Bulk publish (SF List / BO) | Period = earliest ~ latest lesson date in batch | Email body | bulk-email.md |
| Bulk publish (same-day) | Period shows same date twice: `Day, Year ~ Day, Year` | Email body | bulk-email.md |
| Bulk publish (email fails) | Lesson publish NOT rolled back; lessons remain Published | Lesson status | bulk-email.md |
| Bulk publish (email fails) | Failure logged for debugging | SF log / error log | bulk-email.md |
| Bulk publish — 0 Draft→Published | NO email sent (silent skip) | None | bulk-email.md |
| Bulk publish — all-already-published | NO email sent, no user-facing error | None | bulk-email.md |
| Non-Riso org publishes lesson (config=OFF) | NO Chatter post, NO email triggered | SF + Email | tenant-isolation.md |
| LT-98532 student push fires on same bulk publish | Teacher email (LT-101725) must not interfere | Mobile push + Email | bulk-email.md |

### H. Display completeness (triggered by BR-06, BR-10, BR-11, BR-17, BR-21, BR-22)

| Component | Required Fields | Conditional Fields | Text to Assert |
|---|---|---|---|
| SF Chatter post body | @[Teacher Name], [Lesson Name hyperlink], notification sentence | Language EN or JP (Q7) | `has been published. Click to see more details.` (EN) / `が公開されました。詳細はこちらをクリックしてください。` (JP) |
| Bulk publish email | Subject, `Hi [Teacher Name],` / `[先生名]様,`, body text, `Duration: X ~ Y` / `Year年...～...日` | Language EN or JP | Exact strings per BR-19 through BR-22 |

### H.1 — Spec–Figma mismatch
N/A: No Figma URL in spec.

---

## 5. Coverage Strategy Table

| BR | AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|---|
| BR-01 | AC-01 | Draft→Published → Chatter post created (1 per lesson) | State transition, Cross-system | State Transition, CRUD | 🔴 Critical | Deep |
| BR-02 | AC-01 | Republish → new Chatter post; old posts persist | State transition, Data integrity | State Transition, CRUD | 🟠 High | Standard |
| BR-03 | AC-02.1 | Flow Builder detects Draft→Published status change | State transition | State Transition | 🔴 Critical | Deep |
| BR-04 | AC-02.1 | Filter: Available teachers only (FT + PT); Unavailable excluded | Conditional logic, Data integrity | Decision Table, Permission Matrix | 🔴 Critical | Deep |
| BR-05 | AC-02.1 | All retrieved teachers @mentioned in single Chatter post | Data integrity, Cross-system | CRUD, Decision Table | 🔴 Critical | Deep |
| BR-06 | AC-03 | Chatter post in SF Lesson Detail Chatter section | Display completeness, Cross-system | Component, Regression | 🟠 High | Standard |
| BR-07 | AC-03 | Chatter post visibility = LBAC | Permission logic | Permission Matrix | 🟠 High | Standard |
| BR-08 | AC-04 | Each Available teacher @mentioned in post body (required) | Data integrity, Validation | CRUD, Negative | 🔴 Critical | Deep |
| BR-09 | AC-04 | Multiple teachers → single post | Data integrity | CRUD | 🟠 High | Standard |
| BR-10 | AC-05 | Chatter post EN body exact content | Validation, Display completeness | Equivalence Partitioning, Component | 🟠 High | Standard |
| BR-11 | AC-05 | Chatter post JP body exact content | Validation, Display completeness | Equivalence Partitioning, Component | 🟠 High | Standard |
| BR-12 | AC-05 | Lesson Name = hyperlink to SF Lesson Detail | Display completeness | Component | 🟠 High | Standard |
| BR-13 | AC-06 | SF notification center via @mention (single publish only) | State transition, Cross-system | State Transition, Regression | 🔴 Critical | Deep |
| BR-14 | AC-07 | Only @mentioned teachers get notification alert; LBAC-only → no alert | Permission logic, Conditional | Permission Matrix, Decision Table | 🔴 Critical | Deep |
| BR-15 | AC-08 | Lesson Name hyperlink → new tab | Display completeness | Component | 🟡 Medium | Smoke |
| BR-16 | AC-09 | Bulk publish → email to each Available teacher | State transition, Cross-system | State Transition, CRUD | 🔴 Critical | Deep |
| BR-17 | AC-09 | Email content = period summary | Validation, Display | Component | 🟠 High | Standard |
| BR-18 | AC-10 | One email per teacher per bulk action | Data integrity | CRUD, Decision Table | 🔴 Critical | Deep |
| BR-19 | AC-09 | Email subject EN exact text | Validation | Equivalence Partitioning | 🟠 High | Standard |
| BR-20 | AC-09 | Email subject JP exact text | Validation | Equivalence Partitioning | 🟠 High | Standard |
| BR-21 | AC-09 | Email body EN exact format with period | Validation, Display | Component | 🟠 High | Standard |
| BR-22 | AC-09 | Email body JP exact format with period | Validation, Display | Component | 🟠 High | Standard |
| BR-23 | AC-09 | Period calc: SF Calendar = view Start/End Date | Conditional, Boundary/range | Decision Table, BVA | 🟠 High | Standard |
| BR-24 | AC-09 | Period calc: SF List + BO = earliest/latest batch date | Conditional, Boundary/range | Decision Table, BVA | 🟠 High | Standard |
| BR-25 | AC-11 | Email failure → publish not blocked; failure logged | Data integrity | CRUD, Negative | 🔴 Critical | Deep |
| BR-26 | AC-01 | Teacher added to Published future-date lesson → Chatter post | State transition, Conditional, Boundary | State Transition, BVA, Decision Table | 🟠 High | Standard |
| BR-27 | AC-03 | Config flag: On=Riso → active; Off=others → disabled | Permission, Conditional | Permission Matrix, Decision Table | 🔴 Critical | Deep |
| BR-28 | AC-09 | 0 Draft→Published in batch → no email (silent skip) | Conditional, Data integrity | Decision Table, Negative | 🟠 High | Standard |
| — | AC-06 | Single publish only (bulk publish does NOT trigger SF notification center) | Conditional | Negative, Decision Table | 🟠 High | Standard |
| F-01 | AC-05/09 | Cross-type dedup: teacher receives both Chatter (single) + Email (bulk) for same lesson | Data integrity | Decision Table, Regression | 🔴 Critical | Deep |
| F-09 | AC-09 | LT-98532 student push unaffected when LT-101725 teacher email fires | Cross-system, Data integrity | Regression | 🔴 Critical | Standard |

---

## 6. High-Risk Areas

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Flow Builder trigger accuracy (BR-01, BR-03) | If Flow Builder does not fire on Draft→Published, teachers receive no notification at all — silent miss | State Transition: verify every Draft→Published path (SF Lesson Detail, all entry points); verify NOT triggered on Published→Completed, Published→Draft |
| Teacher filter (BR-04) | Wrong filter includes Unavailable teachers (wrong audience) or excludes PT teachers (partial audience) — directly affects notification correctness | Decision Table: 2×2 (Available/Unavailable × FT/PT); verify boundary on working_status change between lesson assign and publish |
| @mention integrity (BR-05, BR-08) | Missing @mention → teacher receives no SF notification center alert at all (silent miss; notification center depends entirely on @mention per AC-06) | CRUD: verify all Available teachers @mentioned; verify Unavailable teachers excluded; verify single post for multi-teacher lesson |
| SF notification center delivery (BR-13, BR-14) | Teacher must receive notification center alert via @mention mechanism; LBAC-only users must NOT receive alert — testing both positive (teacher) and negative (CM, HQ Admin) | Permission Matrix: 3 roles × 2 expected outcomes; verify notification center, not just Chatter section visibility |
| Bulk publish email trigger (BR-16, BR-18) | If email does not fire on any of the 3 surfaces (SF List, SF Calendar, BO), teacher receives no advance notification of schedule | CRUD: verify all 3 surfaces independently; verify email count = 1 per teacher regardless of lessons in batch |
| Email failure isolation (BR-25) | Email failure MUST NOT block lesson publication — if it does, lesson remains in Draft state unexpectedly, blocking all downstream flows | Negative: simulate email send failure → verify lesson Published + failure logged + no rollback |
| Config flag isolation (BR-27, F-10) | If non-Riso orgs receive Chatter posts or emails, confidential lesson data exposed to wrong tenant — security/data integrity concern | Permission Matrix + Decision Table: verify non-Riso lesson publish → no notification; regression guard on existing non-Riso publish TCs |
| Cross-type dedup (F-01) | Teacher may receive both a Chatter post (single publish) and bulk email for the same lesson — same dual-path pattern as Aso 2026-04-13 incident | Decision Table: lesson single-published → then bulk-published → verify actual teacher experience; pending Q1 clarification |
| LT-98532 non-interference (F-09) | Two notification systems (student push + teacher email) sharing the same bulk publish event; failure in one must not cascade to the other | Regression: run LT-98532 bulk publish TC with LT-101725 live → verify student push still fires correctly |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Republish behavior (BR-02) | New Chatter post created each republish; old posts accumulate — risk: teacher confused by multiple posts for same lesson | State Transition: Draft→Published→Draft→Published; verify new post count + content + notification alert on second publish |
| Chatter post content accuracy (BR-10, BR-11) | Wrong teacher name, wrong lesson name, or broken hyperlink in post body — directly impacts notification usefulness | Component: exact text match including @mention variable substitution; verify Lesson Name hyperlink resolved at trigger time |
| Period calculation correctness (BR-23, BR-24) | Wrong period in email body (e.g., calendar view dates vs. batch dates) depends on which surface triggered bulk publish | Decision Table: 3 surfaces × period calc formula; BVA for same-day batch (start = end date) and cross-month range |
| Teacher-added-to-published-lesson (BR-26) | Special trigger path; "future date" boundary undefined (Q6) | BVA on lesson date relative to today; test today's lesson separately; confirm past-date → no notification |
| Multi-teacher single post (BR-09) | If implementation creates one post per teacher (bug), teacher receives multiple notifications and Chatter section becomes cluttered | CRUD: create lesson with 3+ teachers → verify exactly 1 Chatter post created with all teachers mentioned |
| 0-Draft batch silent skip (BR-28, F-13) | Not in AC text — test designers may miss this; if system sends spurious email on all-already-published batch, teachers receive unnecessary noise | Negative: batch with 0 Draft→Published transitions → verify no email sent, no error shown |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Chatter post hyperlink (BR-12, BR-15) | Hyperlink must open Lesson Detail in new tab; if it navigates in-place, user loses their Chatter context | Component: click hyperlink → verify new browser tab opens to correct lesson detail URL |
| Email body format localization (BR-21, BR-22) | Date format must differ by language (EN: `Month Day, Year`; JP: `Year年Month月Day日`) — mismatched formats are visible user-facing defects | Equivalence Partitioning: EN email → verify EN date format; JP email → verify JP date format |
| LBAC post visibility (BR-07) | Post visible only to LBAC-authorized users — verify user without lesson access cannot see post | Permission Matrix: SF user without LBAC access to the lesson → verify Chatter section shows no notification post |

---

## 7. Coverage Gaps vs. Existing Test Cases

### LT-98532 (Riso Bulk Publish — Student Notification)

| Gap Area | LT-98532 Existing TC | Overlap | New Coverage Needed |
|---|---|---|---|
| Bulk publish trigger | ✅ Covered: student push on bulk publish | Shared trigger event (same bulk publish) | ✅ New: verify teacher email fires independently of student push on same event |
| 0-Draft batch silent skip | ✅ Covered: student receives no notification | Student-side silent skip only | ✅ New: teacher-side silent skip — no email when 0 Draft→Published transitions |
| Email failure isolation | ❌ Not covered (student uses Mobile push, not email) | None | ✅ New: email failure does not block publish (AC-11) |
| Period calculation | ✅ Covered: period format `Month Day, Year ~ Month Day, Year` | Same date format for period summary | ✅ New: verify period calculation per surface (Calendar vs. List vs. BO) |

### LT-96662 (Renseikai Publish & Notify Student)

| Gap Area | LT-96662 Existing TC | Overlap | New Coverage Needed |
|---|---|---|---|
| Single publish trigger | ✅ Covered: "Publish and Notify" button press | Different mechanism (button vs. status change) | ✅ New: SF Flow Builder trigger on Draft→Published status change (no button needed) |
| Role-based notification | ✅ Covered: custom permission gates button visibility | Different gating (permission vs. config flag) | ✅ New: config flag gates Riso notification; no button required for teacher notification |
| Notification content | ✅ Covered: mobile push title/body for Renseikai | Different channel (mobile push vs. SF Chatter) | ✅ New: SF Chatter post body content (EN/JP), @mention, hyperlink |

### Nichibei LT-96620 (Teacher SF Notification)

| Gap Area | LT-96620 Existing TC | Overlap | New Coverage Needed |
|---|---|---|---|
| SF notification center delivery | ✅ Covered: teacher notification within 30s on student booking | Same SF notification center mechanism | ✅ New: notification triggered by publish event (not booking); verify @mention path |
| Notification isolation per teacher | ✅ Covered: Teacher A only notified for Lesson A | Same isolation principle | ✅ New: verify Riso LBAC-only users do NOT receive notification center alert (different isolation rule) |

### Net new coverage (no existing TCs anywhere)

| Area | Coverage Needed |
|---|---|
| SF Chatter post creation on lesson publish | ✅ New: all positive + negative states |
| @mention targeting (Available FT + PT; Unavailable excluded) | ✅ New: Decision Table 2×2 |
| LBAC isolation: HQ Admin + CM can view, NOT notified | ✅ New: Permission Matrix |
| Republish creates new post; old posts persist | ✅ New: State Transition |
| Teacher added to published future-date lesson | ✅ New: BVA on date boundary |
| Bulk publish from BO Lesson Management triggers email | ✅ New: BO surface verification |
| Config flag: non-Riso orgs get no notification | ✅ New: isolation negative test |
| Cross-type dedup: single-publish Chatter + bulk-publish Email for same lesson | ✅ New: pending Q1 resolution |
| LT-98532 non-interference regression | ✅ New: regression test on coexisting notification systems |

---

## 8. Suggested Test Suite Structure

```
epics/OOP/riso/LT-101725-lesson-publish-notifications/test-cases/
├── single-publish-chatter-post.md
│   → AC-01 through AC-05, AC-08
│   → Covers: Chatter post creation on Draft→Published, @mention targeting
│     (Available FT/PT included; Unavailable excluded; multi-teacher single post),
│     post body content (EN/JP), Lesson Name hyperlink, republish behavior,
│     teacher-added-to-published-lesson trigger, non-Riso tenant (no post)
│
├── sf-notification-center.md
│   → AC-06, AC-07
│   → Covers: SF notification center delivery to @mentioned teachers,
│     LBAC isolation (HQ Admin + CM can VIEW post but receive NO alert),
│     single-publish-only (bulk publish does NOT trigger notification center),
│     notification center message content
│
├── bulk-publish-email.md
│   → AC-09, AC-10, AC-11
│   → Covers: email trigger on all 3 surfaces (SF Lesson List, SF Lesson Calendar,
│     BO Lesson Management), email content (subject + body EN/JP), period calculation
│     per surface (Calendar = view dates; List+BO = batch min/max), one-email-per-teacher,
│     email failure isolation (publish not blocked), silent skip (0 Draft→Published),
│     same-day batch period format, cross-surface LT-98532 non-interference
│
└── tenant-isolation.md
    → AC-03 (BR-27), F-09, F-10
    → Covers: config flag On=Riso (feature active) vs. Off=non-Riso (no notification),
      non-Riso lesson publish regression guard, LT-98532 student push unaffected
      by LT-101725 teacher email on same bulk publish event
```

---

## 9. Open Dependencies (Block or Flag TCs)

The following open questions from the spec may affect specific TCs. Flag affected cases as `[PENDING Q#]` until clarified:

| Q# | Topic | Affected Suite | Impact |
|---|---|---|---|
| Q1 | Cross-type dedup (single Chatter + bulk Email same lesson) | bulk-publish-email.md | Test case must verify whether teacher receives 1 or 2 notifications when lesson is both single-published and bulk-published |
| Q4 | Silent skip not in AC text | bulk-publish-email.md | TC must assert no email sent on 0-Draft batch; confirm silent vs. warning behavior |
| Q5 | No teachers / all Unavailable → Chatter post behavior | single-publish-chatter-post.md | TC: what happens when available teacher list is empty — skip or empty post? |
| Q6 | "Future date" boundary: today inclusive or exclusive? | single-publish-chatter-post.md | BVA TC for today's lesson date requires knowing boundary direction |
| Q7 | Chatter post language selection (EN vs JP) | single-publish-chatter-post.md | EN and JP content TCs depend on knowing which language the Flow Builder selects |
| Q8 | Email sender TBC; missing teacher email → skip or error? | bulk-publish-email.md | TC for missing email address requires knowing expected behavior |
| Q10 | LBAC roles enumeration; BO teacher SF account existence | sf-notification-center.md | Permission Matrix TC requires confirmed role list and SF account baseline |
