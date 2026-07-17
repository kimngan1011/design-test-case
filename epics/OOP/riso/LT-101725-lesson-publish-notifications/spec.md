---
ticket_id: LT-101725
ticket_url: https://manabie.atlassian.net/browse/LT-101725
title: "[Riso] Core | Lesson Publish Notifications to Teachers"
module: scheduling
bucket: OOP/riso
status: In Development
internal_uat_date: null
production_release_date: null
last_updated: 2026-06-23
---

# LT-101725: [Riso] Core | Lesson Publish Notifications to Teachers

**ID:** https://manabie.atlassian.net/browse/LT-101725
**Status:** In Development
**Priority:** High
**Labels:** Q3_2026_Scheduling, Riso_P2

---

## Summary

Riso teachers need to be notified when lessons they are assigned to are published, so they can check their teaching schedule in advance. This feature introduces two independent notification paths via Salesforce (SF):

1. **Single Publish → SF Chatter post + @mention → SF Notification Center** — triggered on each individual lesson publish (Draft→Published), or when a teacher is added to an already-published future lesson.
2. **Bulk Publish → Email** — triggered when multiple lessons are published at once from SF Lesson List, SF Lesson Calendar, or BO Lesson Management. One email per teacher per bulk publish action, summarizing the published period.

A third component (US3 — Chatter Digest) is ops-configuration only and has no technical deliverable.

The feature is **Riso-only** (config flag On = Riso, Off = all other tenants). It must not affect non-Riso SF orgs.

**Out of scope:** Auto-publish from the Booking System (Riso will not use the Lesson Booking feature).

---

## Comparison with Related Features

| Feature | Trigger | Audience | Channel | Tenant |
|---|---|---|---|---|
| LT-101725 (this) — Single Publish | Draft→Published (single), or teacher added to published future lesson | Lesson Teachers | SF Chatter post + @mention → SF Notification Center | Riso only |
| LT-101725 (this) — Bulk Publish | Bulk publish (SF List / Calendar / BO) | Lesson Teachers | Email | Riso only |
| LT-98532 — Bulk Publish by Student | Bulk publish (SF Calendar) | Students + Parents | Mobile push | Riso only |
| LT-96662 — Publish & Notify Student | "Publish and Notify" button click | Students + Parents | Mobile push | Renseikai only |

---

## Acceptance Criteria

### US1 — Single Publish: Chatter Post + Default SF Notification

#### AC-01 — Trigger: Chatter post on Draft→Published

When a user changes a lesson status from Draft to Published (single publish), the SF Flow Builder runs and creates **one Chatter post per published lesson**. This also applies when a teacher is added to a lesson that is already Published and has a future date.

> **Special case — Teacher Added to Published Lesson:** When a teacher is added to a lesson that is already in Published status AND the lesson date is a **future date**, the system triggers a Chatter post and default SF notification for the newly added teacher(s). _(Note: "future date" boundary — strictly > today vs. ≥ today — is an open question. See Q6.)_

#### AC-02.1 — Flow Builder steps

The SF Flow Builder must execute the following steps:

1. Detect lesson status change from Draft → Published.
2. Retrieve all Lesson Teachers assigned to the lesson where `working_status = Available` AND `working_type IN (Full Time, Part Time)`.
3. Create a Chatter post on the lesson record, @mentioning ALL retrieved Lesson Teachers in a **single post** (not one post per teacher).

> **Republish behavior:** If a lesson is unpublished (Published→Draft) and then republished (Draft→Published), a **new Chatter post is created** — notifications are NOT suppressed. Each Draft→Published transition creates a new post.

#### AC-03 — Chatter post placement and visibility

The Chatter post must appear in the **Chatter section of the Lesson Detail page** in SF. Visibility is governed by **LBAC rules** — only SF users with access to the lesson record can view the post. Feature is controlled by config flag (On = Riso only).

#### AC-04 — @mention requirement

Each assigned Lesson Teacher (working_status=Available) must be **@mentioned directly in the Chatter post body** — not just as a viewer of the lesson record. Multiple teachers on the same lesson are mentioned in a **single Chatter post**.

#### AC-05 — Chatter post content

Chatter post content (both EN and JP templates provided; language selection TBD — see Q7):

- **EN:** `@[Teacher Name] — [Lesson Name] has been published. Click to see more details.`
- **JP:** `@[先生名] — [授業名]が公開されました。詳細はこちらをクリックしてください。`

The **Lesson Name must be hyperlinked** to the SF Lesson Detail page (opens in new tab per AC-08).

#### AC-06 — SF Notification Center delivery (single publish only)

The Lesson Teacher receives an **SF notification center message** via the default SF @mention notification mechanism. No custom notification center message is required. This applies to single publish only (not bulk publish).

#### AC-07 — Notification isolation

Only @mentioned Lesson Teachers receive the SF notification center alert. **Other SF users with LBAC access to the lesson record may view the Chatter post but must NOT receive a notification center alert.** _(Specific roles — see Q10.)_

#### AC-08 — Lesson Name hyperlink navigation

When a user clicks the Lesson Name hyperlink in the Chatter post or notification center, they must be redirected to the **SF Lesson Detail page in a new tab**.

---

### US2 — Bulk Publish: Email Notification to Teachers

#### AC-09 — Trigger: Email on bulk publish

When lessons are bulk published (from SF Lesson List, SF Lesson Calendar, or BO Lesson Management), each assigned Lesson Teacher with `working_status=Available` receives an **email to their SF-registered email address** containing the published period summary.

**Published period calculation (surface-specific):**

| Surface | Period calculation |
|---|---|
| SF Lesson Calendar | Start Date and End Date of the **calendar view** |
| SF Lesson List | Earliest and latest date across **all published lessons in the batch** |
| BO Lesson Management | Earliest and latest date across **all published lessons in the batch** |

**Email content:**

| Field | EN | JP |
|---|---|---|
| Subject | `Lesson Schedule Published` | `授業予定が公開されました` |
| Body greeting | `Hi [Teacher Name],` | `[先生名]様,` |
| Body text | `Lesson schedules for the following period have been published:` | `下記の期間の授業が公開されました。` |
| Duration format | `Duration: Month Day, Year ~ Month Day, Year` | `Year年Month月Day日～Year年Month月Day日` |

**Email sender:** SF system email (org-wide email address). _(Specific from-address TBC — see Q8.)_

**Edge case — No valid Draft→Published transitions:** If the bulk publish batch contains ONLY already-published, Completed, or Cancelled lessons (zero Draft→Published transitions), **NO email is sent** and no error is shown to the user (silent skip). _(This edge case is defined in the Confluence PRD Case Matrix but absent from AC text — see Q4.)_

#### AC-10 — One email per teacher per bulk action

Each teacher receives **exactly one email per bulk publish action**, regardless of how many lessons in the batch they are assigned to. The email summarizes the overall published period, not individual lesson details.

#### AC-11 — Email failure handling

If email delivery fails, the failure must **NOT block or roll back the lesson publication**. Failed email attempts must be **logged for debugging**. _(Individual-teacher-level partial failure behavior undefined — see Q8.)_

---

### US3 — Chatter Digest (Ops-only, no technical deliverable)

#### AC-12, AC-13, AC-14 — Chatter Digest [OPS ONLY]

Because Lesson Teachers are @mentioned in Chatter posts (AC-04), notifications automatically appear in the teacher's SF Chatter Digest without additional system configuration. Digest frequency (daily/weekly) is configured individually by each teacher in SF settings. Chatter post content (including JP text and Lesson Name) carries through to the digest as-is. The digest email wrapper is SF-standard and not customizable.

**No technical deliverable — ops configuration only.**

---

## Business Rules

| ID | AC | Rule |
|---|---|---|
| BR-01 | AC-01 | Draft→Published (single publish) → SF Flow Builder creates exactly 1 Chatter post per lesson |
| BR-02 | AC-01 | Republish (Draft→Published after Published→Draft) → NEW Chatter post created; no deduplication |
| BR-03 | AC-02.1 | Flow Builder Step 1: detect lesson status change Draft→Published |
| BR-04 | AC-02.1 | Flow Builder Step 2: retrieve Lesson Teachers where working_status=Available AND working_type IN (Full Time, Part Time) |
| BR-05 | AC-02.1 | Flow Builder Step 3: create Chatter post with @mention of ALL retrieved Lesson Teachers in a single post |
| BR-06 | AC-03 | Chatter post target = Lesson record (Lesson Detail page Chatter section) |
| BR-07 | AC-03 | Chatter post visibility = LBAC (only SF users with access to the lesson record can view) |
| BR-08 | AC-04 | Each Available Lesson Teacher must be @mentioned in the Chatter post body |
| BR-09 | AC-04 | Multiple teachers → single post (NOT one post per teacher) |
| BR-10 | AC-05 | Chatter post EN body: `@[Teacher Name] — [Lesson Name.hyperlink] has been published. Click to see more details.` |
| BR-11 | AC-05 | Chatter post JP body: `@[先生名] — [授業名.hyperlink]が公開されました。詳細はこちらをクリックしてください。` |
| BR-12 | AC-05 | Lesson Name in Chatter post = hyperlink to SF Lesson Detail page |
| BR-13 | AC-06 | SF notification center message = default SF @mention notification; no custom notification code required |
| BR-14 | AC-07 | Only @mentioned teachers receive notification center alert; LBAC-only users can view post but receive NO alert |
| BR-15 | AC-08 | Lesson Name hyperlink → opens SF Lesson Detail page in new tab |
| BR-16 | AC-09 | Bulk publish → one email per Available Lesson Teacher per bulk action |
| BR-17 | AC-09 | Email content = published period summary (not individual lesson details) |
| BR-18 | AC-10 | One email per teacher per bulk action (regardless of how many lessons in batch) |
| BR-19 | AC-09 | Email subject EN: `Lesson Schedule Published` |
| BR-20 | AC-09 | Email subject JP: `授業予定が公開されました` |
| BR-21 | AC-09 | Period calc (SF Lesson Calendar) = calendar view Start Date ~ End Date |
| BR-22 | AC-09 | Period calc (SF Lesson List, BO) = earliest ~ latest lesson date in batch |
| BR-23 | AC-11 | Email failure → does NOT block or roll back lesson publication |
| BR-24 | AC-11 | Email failure → logged for debugging |
| BR-25 | AC-09 | Edge: all lessons already published → NO email sent (silent skip) |
| BR-26 | AC-01 | Teacher added to Published future-date lesson → Chatter post + SF notification for added teacher(s) |
| BR-27 | AC-03 | Config flag: On=Riso, Off=all other tenants; non-Riso orgs must not be affected |
| BR-28 | AC-09 | Email sender = SF system email / org-wide email address (TBC) |

---

## Case Matrix

| Case | Surface | Trigger | Notification |
|---|---|---|---|
| Single publish (one-by-one) | SF Lesson Detail — Mark as Published; SF Lesson Detail — Publish & Notify Student | Draft→Published | Chatter post + SF notification center |
| Bulk publish | SF Lesson List, SF Lesson Calendar, BO Lesson Management | Batch Draft→Published | Email to each Available Lesson Teacher |
| Teacher added to published future lesson | SF Lesson Detail — Add Teacher/s; SF Lesson Calendar — Assign Teacher/s | Teacher assignment to Published, future-date lesson | Chatter post + SF notification center for added teacher(s) |
| Auto-publish from Booking System | N/A | N/A | **OUT OF SCOPE** — Riso will not use Lesson Booking |
| [Edge] Bulk publish includes all-already-published lessons | BO Lesson Management / SF Lesson List / Calendar | Bulk publish with zero Draft→Published transitions | **NO notification** (silent skip) |

---

## Impact Analysis

### Impact Summary

| Tag | Count |
|---|---|
| `[LESSON-LEARNED RISK]` | 1 |
| `[REGRESSION RISK]` | 2 |
| `[MISSING BEHAVIOR]` | 8 |
| `[ROLE GAP]` | 2 |
| `[UNDOCUMENTED IN AC]` | 1 |
| `[EXTENDED]` | 2 |
| **Total** | **16** |

### Lesson-Learned Risk

| ID | AC | Finding |
|---|---|---|
| F-01 `[LESSON-LEARNED RISK]` | AC-05, AC-09 | **Aso dual-path pattern (2026-04-13):** LT-101725 introduces two independent teacher notification paths — single publish Chatter post AND bulk publish Email — with no cross-type deduplication between them. If a lesson is single-published (teacher receives Chatter post) and then falls within a subsequent bulk publish period, the teacher receives BOTH notifications. LT-98532 defined explicit cross-type dedup for students; LT-101725 defines none for teachers. Whether dual notification is acceptable must be confirmed. |

### Regression Risk

| ID | AC | Finding |
|---|---|---|
| F-09 `[REGRESSION RISK]` | AC-09 | LT-98532 (Riso Bulk Publish — student push notification) fires on the same bulk publish event. The LT-101725 teacher email must not interfere with LT-98532's async notification job. If they share any part of the SF Flow Builder, a failure in one could cascade to the other. |
| F-10 `[REGRESSION RISK]` | AC-03, BR-27 | Config flag isolation: if the SF Flow Builder is deployed globally (not Riso-sandbox-only), a misconfigured or missing flag could trigger Chatter posts or emails in non-Riso SF orgs. Existing lesson publish regression TCs for other partners must not be affected. |

### Missing Behavior

| ID | AC | Finding |
|---|---|---|
| F-02 | AC-02.1, AC-04 | No AC defines behavior when a lesson has NO assigned teachers, or when ALL assigned teachers are Unavailable. Should the Flow Builder skip post creation silently, create an empty post, or log an error? |
| F-03 | AC-01, BR-26 | "Future date" in Case Matrix is undefined — does it mean strictly > today or ≥ today? No AC covers teacher added to a Published lesson with a PAST date. |
| F-04 | AC-11 | AC-11 covers failure at bulk-action level but not at individual-teacher level. If Teacher A's email fails but Teacher B's succeeds, are they independent? Is Teacher A retried separately? |
| F-05 | AC-05 | Both EN and JP Chatter post templates are defined, but no AC specifies which language is used. JP-only? EN-only? Teacher locale? Both in one post? |
| F-06 | AC-01, AC-02 | On republish: old Chatter posts persist (no cleanup defined). No limit on number of posts that can accumulate per lesson. Teacher receives a new notification center alert each time. |
| F-07 | AC-09 | No fallback defined when a Lesson Teacher has no SF-registered email. Email sender (from-address) marked TBC in PRD. |
| F-08 | AC-09 | Period calculation edge: same Start Date = End Date (single-day batch). Presentation "Month Day, Year ~ Month Day, Year" may look odd. |
| F-14 | AC-02.1, AC-04 | SF Chatter may have a platform limit on the number of @mentions per post. No AC defines a fallback for lessons with many assigned teachers (10+). |

### Role Gap

| ID | AC | Finding |
|---|---|---|
| F-11 | AC-07 | AC-07 uses "LBAC access" generically. Permission matrix roles (HQ Admin, CM, CPU) not explicitly enumerated. Which roles can VIEW but must NOT receive notification center alert? |
| F-12 | AC-03, AC-06 | Riso Lesson Teachers may primarily use BO (CPU role) and may lack an active SF user account. If no SF account exists, the Chatter @mention notification cannot reach them via SF notification center. This case is unaddressed. |

### Undocumented in AC

| ID | AC | Finding |
|---|---|---|
| F-13 | AC-09 | The "all lessons already published → no email" edge case is defined only in the Confluence PRD Case Matrix, NOT in AC-09/AC-10/AC-11 text. Risk: test designers relying on ACs alone will miss this behavior. |

### Extended (no conflict)

| ID | AC | Finding |
|---|---|---|
| F-15 | AC-01, AC-02.1 | Additive: new feature adds teacher Chatter notification to the existing Draft→Published transition. No existing spec contradicted. New TCs must assert PRESENCE of Chatter post (positive assertion). |
| F-16 | AC-09, AC-10 | Additive: teacher email notification coexists with LT-98532 student push on the same bulk publish event. Two independent notification systems; no conflict. |

---

## E2E Scenario Impact

| Scenario | Action | Impact |
|---|---|---|
| E2E-19 — [Riso] Lesson Allocation & Subject | UPDATE | Step 8 "Staff publishes the lesson" must add verification: Chatter post created, teacher(s) @mentioned, teacher receives SF notification center message |
| E2E-01 — Lesson Lifecycle (Create, Teach, Report, View) | NOTE | Step 7 Draft→Published: for Riso-environment runs, add conditional Chatter post verification. For non-Riso runs, add negative assertion that NO Chatter post is created (regression guard for config flag isolation) |
| E2E-NEW-1 — [Riso] Single Publish: Teacher Chatter Notification | CREATE | New E2E: publish lesson in Riso tenant → verify Chatter post in Lesson Detail → verify teacher receives SF notification center alert → verify LBAC-only user (CM) can view post but receives no alert |
| E2E-NEW-2 — [Riso] Bulk Publish: Teacher Email Notification | CREATE | New E2E: bulk publish from SF Lesson List + SF Lesson Calendar + BO → verify teacher receives email with correct subject and period summary (EN and JP) → verify email failure does not block publish → verify 0-Draft batch → no email sent |

---

## Open Questions

> Questions are ordered by priority. Submit to PO/Dev before coverage definition.

**Q1 — [LESSON-LEARNED RISK] (Priority 2) — AC-05, AC-09: Cross-type deduplication between Chatter and Email**

LT-101725 introduces two independent teacher notification paths: (1) Single Publish → Chatter post; (2) Bulk Publish → Email. If a lesson is first single-published (teacher receives Chatter @mention) and the same period is subsequently covered by a bulk publish, the teacher receives BOTH a Chatter post AND a bulk email for the same lesson. LT-98532 explicitly defined cross-type dedup for student notifications — no equivalent is defined here.

**Is receiving both a single-publish Chatter post AND a bulk-publish email acceptable for teachers? If not, what cross-type deduplication rule applies?**

_Evidence: knowledge/domain-knowledge/scheduling/lesson-learned/core.md — 2026-04-13 Aso dual-path pattern; epics/calendar/LT-98532-bulk-publish-lessons-by-student/spec.md — cross-type dedup defined for students_

---

**Q2 — [REGRESSION RISK] (Priority 3) — AC-09: LT-98532 and LT-101725 coexistence**

LT-98532 fires a Mobile push to students and LT-101725 fires an email to teachers on the same bulk publish event. (a) Do both systems share any part of the SF Flow Builder, or are they fully independent? (b) If teacher email send fails (LT-101725), does this affect the student push notification (LT-98532), and vice versa?

_Evidence: epics/calendar/LT-98532-bulk-publish-lessons-by-student/spec.md AC-02.1 — student push on same bulk publish event_

---

**Q3 — [REGRESSION RISK] (Priority 3) — AC-03, BR-27: Non-Riso tenant isolation**

Is the SF Flow Builder deployed per-tenant (Riso-only sandbox) or globally with tenant-level config filtering? If global, what is the specific mechanism preventing the Flow Builder from creating Chatter posts or sending emails in non-Riso orgs?

_Evidence: BR-29 — "must not affect non-Riso SF orgs"; Confluence PRD § Users/Permissions_

---

**Q4 — [UNDOCUMENTED IN AC] (Priority 4) — AC-09: Silent-skip edge case not in AC text**

The Confluence PRD Case Matrix defines: "Bulk Publish includes an already published lesson → Do not generate notification if there is no valid lesson to be moved from Draft to Published." This edge case does NOT appear in AC-09/AC-10/AC-11. When the bulk publish batch has ZERO valid Draft→Published transitions: (a) skip silently with no email and no user-facing message? (b) show a warning? (c) other?

_Evidence: Confluence PRD Case Matrix — defined only in Case Matrix; epics/calendar/LT-98532-bulk-publish-lessons-by-student/spec.md — equivalent student case resolved as silent skip_

---

**Q5 — [MISSING BEHAVIOR] (Priority 5) — AC-02.1, AC-04: No teachers / all Unavailable + mention limit**

(a) When a lesson has NO assigned teachers, or ALL assigned teachers are working_status=Unavailable — should the Flow Builder skip Chatter post creation silently, create a post with no @mentions, or log an error? (b) Does the SF Chatter platform impose a @mention limit per post? If a lesson has 10+ teachers, what is the fallback?

_Evidence: AC-02.1 — retrieve Available teachers; AC-04 — @mention all teachers; no AC covers empty or overlimit cases_

---

**Q6 — [MISSING BEHAVIOR] (Priority 5) — AC-01, BR-27: "Future date" boundary definition**

The Case Matrix states: "Teacher Added to a Published Lesson — Given that the Lesson is already published and in a future date." Does "future date" mean: (a) lesson date strictly > today (today's lessons excluded), or (b) lesson date ≥ today (today's lessons included)? Also: when a teacher is added to a Published lesson with a PAST date, should any notification be triggered?

_Evidence: Confluence PRD Case Matrix — "future date" used without definition; no AC defines the boundary_

---

**Q7 — [MISSING BEHAVIOR] (Priority 5) — AC-05: Chatter post language selection**

AC-05 provides both EN and JP Chatter post content templates. NFR-03 states JP is the primary language for Riso users. When the SF Flow Builder creates the Chatter post, which language is used: (a) JP only, (b) EN only, (c) both EN and JP in the same post body, or (d) based on the teacher's SF user locale?

_Evidence: Confluence PRD § 6.A — both EN and JP templates defined; NFR-03 — JP primary for Riso; AC-05 does not specify language selection_

---

**Q8 — [MISSING BEHAVIOR] (Priority 5) — AC-09, AC-11: Missing email address + TBC sender**

(a) If a Lesson Teacher has no SF-registered email address — skip silently, log the failure, or raise an error? Does this count as a "failure" per AC-11? (b) What is the confirmed org-wide email address (from-address) for Riso bulk publish emails? The PRD marks it as TBC. Has it been configured to avoid spam filtering?

_Evidence: Confluence PRD § 6.B — "Sender: SF system email (TBC)"; AC-09 — "Lesson Teacher's SF-registered email address" with no fallback_

---

**Q9 — [MISSING BEHAVIOR] (Priority 5) — AC-01, AC-02: Republish Chatter post accumulation**

On republish, the PRD confirms a new Chatter post is created each time (no dedup). (a) Do old Chatter posts from previous publish events remain visible alongside the new post? Any limit on accumulated posts per lesson? (b) When the teacher receives the SF notification center alert for a second/third Chatter post (republish), is this a new independent alert or combined with previous?

_Evidence: Confluence PRD Open Questions table — "Yes — send it again" on republish; AC-01/AC-02 define trigger but not cleanup or accumulation_

---

**Q10 — [ROLE GAP] (Priority 6) — AC-07, AC-06: LBAC roles + BO teacher SF access**

(a) Which specific SF roles have LBAC access to lesson records in Riso? AC-07 says "other SF users with LBAC access" without enumerating roles. HQ Admin? Centre Manager? Centre Staff? Test coverage requires knowing exact roles. (b) Riso Lesson Teachers may primarily use BO (CPU role) and may not have an active SF user account. If a Lesson Teacher has no SF account, does the Chatter @mention + SF notification center delivery mechanism reach them? If not, how?

_Evidence: scheduling-feature-permission-matrix.csv — roles: full_access (HQ Admin), center_level_edit (CM/Staff), bo_teacher (CPU); AC-07 — "LBAC access" generic; lesson-teacher.md — CPU login sees BO Calendar_

---

## Related Specs

- `epics/calendar/LT-98532-bulk-publish-lessons-by-student/spec.md` — Riso Bulk Publish (student push) — same bulk publish event; cross-type dedup parallel
- `epics/OOP/renseikai/LT-96662-publish-notify-student/spec.md` — Renseikai Publish & Notify Student — different tenant/audience/channel; separate feature
- `epics/OOP/nichibei/LT-96620-nichibei-lesson-booking/test-cases/teacher-notification.md` — SF teacher notification on booking (Nichibei) — different trigger but same notification center delivery mechanism

## Related Knowledge

- `knowledge/domain-knowledge/scheduling/lesson-management/lesson-teacher.md` — Lesson Teacher entity, working_status, working_type
- `knowledge/domain-knowledge/scheduling/calendar/calendar-sf.md` — SF Calendar bulk publish behavior
- `knowledge/domain-knowledge/scheduling/partner-rules/riso-lesson-allocation.md` — Riso-specific LA rules (context)
- `knowledge/domain-knowledge/scheduling/lesson-learned/core.md` — Aso 2026-04-13 dual-path incident (relevant to Q1)
