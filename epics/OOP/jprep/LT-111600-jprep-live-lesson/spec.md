---
ticket_id: LT-111600
ticket_url: https://manabie.atlassian.net/browse/LT-111600
title: JPREP Live Lesson (Agora) — Launch from BO, Course Whitelist, Student Join, In-room Key Features
module: scheduling
bucket: OOP/jprep
status: Done
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-26
---

# LT-111600: JPREP Live Lesson — regression & incident-prevention spec

## Summary

JPREP is the only tenant that runs Live Lesson on **Agora** inside LMSv2. Lessons are **created by JPREP's sync API** (not by BO UI), then JPREP Teachers **start the live lesson from the Back Office (BO) lesson detail page**, which opens the Teacher Web live room via single sign-on. Students join from the Learner App/Web **only if the lesson's course is on the JPREP live-lesson course whitelist**. On 2026-09-21 (typhoon, EX240) students could not see the **Join** button because course EX240 was not on the whitelist (MANACS-2620 / LT-111600). QA (Lesson squad) was asked to re-test the whole JPREP live lesson flow with new courses. Qase PX had only 3–4 thin, URL-only JPREP cases, so this spec consolidates every known rule with its evidence.

Parent epic: [LT-54444 [LMS 2.0][JPREP] Launch Live Lesson on BO](https://manabie.atlassian.net/browse/LT-54444)

---

## Source Register (evidence for every rule)

| ID | Source | Link |
|---|---|---|
| S1 | Confluence — [JPREP] Agora in LMSv2 JPREP (functional spec) | https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790 |
| S2 | Jira LT-54444 epic + children LT-56091 / LT-57459 / LT-57985 (teacher login BO), LT-56315 (Lesson column in Course > Lesson tab), LT-56316 (teacher left menu), LT-56318 (teacher page access), LT-54446 (design) | https://manabie.atlassian.net/browse/LT-54444 |
| S3 | Jira LT-57917 — Hide Start Lesson for Offline teaching medium | https://manabie.atlassian.net/browse/LT-57917 |
| S4 | Jira LT-56380 — Login (SSO) when open Teacher Web from BO | https://manabie.atlassian.net/browse/LT-56380 |
| S5 | Jira LT-56381 — Keep staying in live lesson after refresh | https://manabie.atlassian.net/browse/LT-56381 |
| S6 | Jira LT-56382 — Close browser when leave/end live lesson | https://manabie.atlassian.net/browse/LT-56382 |
| S7 | Jira LT-88036 — Redirect URL format + unleash `User_Authentication_ImproveSSO` | https://manabie.atlassian.net/browse/LT-88036 |
| S8 | Jira LT-91604 — Fix JPREP URL (no `////`, course_id first) | https://manabie.atlassian.net/browse/LT-91604 |
| S9 | Jira LT-98048 — Attach `user_id` to JPREP live lesson URL | https://manabie.atlassian.net/browse/LT-98048 |
| S10 | Jira LT-98050 — Switch teacher account BO → Teacher Web | https://manabie.atlassian.net/browse/LT-98050 |
| S11 | Confluence — [JPREP][External] Role access level for backoffice | https://manabie.atlassian.net/wiki/spaces/LT/pages/969212037 |
| S12 | Confluence — [QA] Jprep LMSv2 integration test | https://manabie.atlassian.net/wiki/spaces/LT/pages/993427472 |
| S13 | Slack #jp_incidents — MANACS-2620 EX240 incident thread (whitelist root cause, Admin "Account is not registered", waiting room, sync payload, late member sync, EX280 added) | https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349 |
| S14 | Jira LT-111600 — add course to whitelist (whitelist origin LT-15745) | https://manabie.atlassian.net/browse/LT-111600 |
| S15 | Slack #draft-discuss-lesson-feature 2026-09-23 — re-test plan + unleash `User_Auth_AllowAllRolesToLoginTeacherWeb` | https://manabiebiz.slack.com/archives/C0BNPCH3605/p1790133887305919 |
| S16 | Slack DM Phuc → Linh 2026-09-26 — STG whitelist = 4 courses | https://manabiebiz.slack.com/archives/D0BNMBRTRNZ/p1790399497452229 |
| S17 | Confluence — Virtual Classroom Database Tables (whitelist config used when listing live lessons; course/academic year validated on join) | https://manabie.atlassian.net/wiki/spaces/TECH/pages/722468865 |
| S18 | Confluence — Test plan coverage KEY feature for Live Lesson | https://manabie.atlassian.net/wiki/spaces/TECH/pages/2189852681 |
| S19 | Confluence — Live Lesson Smoke Test Planning on PROD (share screen hidden on JPREP; Recording & Private chat JPREP-only) | https://manabie.atlassian.net/wiki/spaces/LT/pages/411631738 |
| S20 | Jira MANACS-2343 — Recording confirmation dialog: Cancel could not be clicked | https://manabie.atlassian.net/browse/MANACS-2343 |
| S21 | Confluence — [ChatV1] cleanup plan (live lesson chat still used by JPREP) + Slack #camp-communication 2026-08-19 "JPREP private chat on STAG working" | https://manabie.atlassian.net/wiki/spaces/TECH/pages/2627272747 |
| S22 | Google Sheet — [Jprep_PS] Live Lesson Account Test (UAT accounts/course/lesson) | https://docs.google.com/spreadsheets/d/1aZe8LVoFGeqA_61yfLpq0JJ81O-KMOZj58LQzUDaias |
| S23 | Confluence — Live Lesson - Launch Live lesson from BO (JPREP URL structure) | https://manabie.atlassian.net/wiki/spaces/TECH/pages/953253916 |
| S24 | Slack #draft-discuss-lesson-feature 2026-07-31 — test JPREP live lesson with Brightcove video | (search "tâm test livelesson jprep với brightcove") |
| S25 | Jira LT-11390 / LT-15745 — pilot course whitelist (2022) → blacklist A+ for lesson list | https://manabie.atlassian.net/browse/LT-15745 |
| S26 | Confluence postmortems — JPREP Live Lesson Post-mortem (2023, private chat CPU) / Room attendees cannot see sharing material (2024-03-30) | https://manabie.atlassian.net/wiki/spaces/ERP/pages/791511059 · https://manabie.atlassian.net/wiki/spaces/TECH/pages/937787471 |

---

## Acceptance Criteria (reconstructed from S1 user stories + later tickets)

- **US 01 – System creates JPREP live lessons through API** (S1). AC 01.1 Lessons, teaching medium (`online`/`offline`), start/end time, course, week and class come from JPREP sync (S13 payload). AC 01.2 A later sync that changes the lesson (e.g. offline → online, new members) is reflected in BO and Learner.
- **US 02 – JPREP BO user accesses the paired live lesson through the Course menu** (S1, S2 LT-56315). AC 02.1 Course > `Lesson` tab lists each Week with the **name of its paired lesson**. AC 02.2 Clicking the lesson name opens that lesson's detail page.
- **US 03 – JPREP BO user starts the live lesson** (S1). AC 03.1 `Start Live Lesson` shows only when teaching medium = Online; hidden/disabled when Offline (S3). AC 03.2 Click opens the Teacher Web live room in a new tab with the same account, no extra login (S2, S4). AC 03.3 URL format per unleash `User_Authentication_ImproveSSO` (S7, S8, S9, S23). AC 03.4 After BO account switch the room opens as the new account (S10). AC 03.5 Refresh keeps the teacher in the room (S5). AC 03.6 Leave/End closes the tab (S6). AC 03.7 Only Teacher role can enter; Admin gets "Account is not registered" unless `User_Auth_AllowAllRolesToLoginTeacherWeb` is ON (S13, S15 — needs confirmation). AC 03.8 Recording confirmation dialog: Cancel enters room without recording; Start recording records (S20).
- **US 04 – BO user uploads weekly live lesson materials** (S1, S11). AC 04.1 Admin can add/delete materials in Course > Lesson. AC 04.2 Teacher can only view materials. AC 04.3 Uploaded materials are available to share inside the room.
- **US 05 – JPREP Learner sees schedule, materials and joins** (S1, S13, S17). AC 05.1 Lesson list shows lesson + materials. AC 05.2 **Join** is available only when the lesson's course is on the live-lesson course whitelist (PROD 10 courses, STG 4 courses). AC 05.3 Non-whitelisted course → no Join button. AC 05.4 After course is added to whitelist, Join appears after refresh. AC 05.5 Students synced after start see Join after refresh. AC 05.6 Waiting room holds students until teacher turns it off. AC 05.7 After teacher ends lesson for all, Join is no longer shown.
- **US 06 – In-room KEY features** (S18, S19). AC 06.1 Camera/mic on-off (incl. rapid clicks). AC 06.2 Share PDF / image / video (Brightcove, S24). AC 06.3 Whiteboard / annotation. AC 06.4 Public chat. AC 06.5 Private chat (JPREP only, S21). AC 06.6 Share-screen control hidden for JPREP. AC 06.7 Disconnect / reconnect.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform | Source |
|---|---|---|---|---|---|---|
| 1 | AC 01.1 | JPREP lessons (incl. teaching medium) come only from JPREP sync; BO does not create them | Teaching medium | read-only (sync) | [BO] | S1, S13 |
| 2 | AC 01.2 | Sync update offline→online makes Start Live Lesson available | Teaching medium | sync-driven | [BO] | S3, S13 |
| 3 | AC 02.1 | Course > Lesson tab shows paired lesson name for each Week | Lesson column | display | [BO] | S1, S2 |
| 4 | AC 02.2 | Lesson name is a link to lesson detail | Lesson link | navigation | [BO] | S1, S2 |
| 5 | AC 03.1 | Start Live Lesson shown if Online, not available if Offline | Start button | conditional | [BO] | S1, S3 |
| 6 | AC 03.2 | Start opens Teacher Web live room in a new tab, SSO, BO tab kept | — | — | [BO→TW] | S2, S4 |
| 7 | AC 03.3 | ImproveSSO OFF: `/#/liveStreamScreen?course_id=…&lesson_id=…&user_id=…` (single slash, course_id first). ON: `/redirect?data=<base64 organization_name=jprep&access_level=&context=live_lesson&lesson_id=…>` | URL | auto-generated | [BO→TW] | S7, S8, S9, S23 |
| 8 | AC 03.4 | Room identity follows the account currently logged in to BO | user_id | auto | [BO→TW] | S10 |
| 9 | AC 03.5 | Page refresh keeps teacher in room | — | — | [TW] | S5 |
| 10 | AC 03.6 | Leave / End lesson closes the browser tab | — | — | [TW] | S6 |
| 11 | AC 03.7 | Only Teacher can start/join; Admin blocked ("Account is not registered") unless AllowAllRoles flag ON | Role | permission | [BO→TW] | S13, S15 |
| 12 | AC 03.8 | Recording dialog: Cancel → enter without recording; Start recording → recording on | Recording | conditional | [TW] | S19, S20 |
| 13 | AC 04.1 | Admin can add / delete weekly materials | Materials | READWRITE | [BO] | S1, S11 |
| 14 | AC 04.2 | Teacher sees materials read-only | Materials | READ | [BO] | S11 |
| 15 | AC 04.3 | Uploaded materials appear in the room for sharing | Materials | cross-surface | [BO→TW] | S1, S18 |
| 16 | AC 05.1 | Learner shows lesson schedule + materials | Lesson card | display | [Learner] | S1 |
| 17 | AC 05.2/05.3 | Join visible only for whitelisted courses | Join button | conditional (config) | [Learner] | S13, S14, S16, S17 |
| 18 | AC 05.4 | Adding course to whitelist makes Join appear after refresh | Whitelist | config change | [Learner] | S13 |
| 19 | AC 05.5 | Members synced after start see Join after refresh | Lesson members | sync-driven | [Learner] | S13 |
| 20 | AC 05.6 | Waiting room holds students until teacher disables it | Waiting room | state | [TW/Learner] | S13 |
| 21 | AC 05.7 | End lesson for all → lesson ended, Join no longer shown | Lesson state | state transition | [TW/Learner] | S13 |
| 22 | AC 06.1 | Camera/mic toggle reflected to others; rapid toggles stable | Cam/Mic | state | [TW/Learner] | S18 |
| 23 | AC 06.2 | Share PDF / image / video visible to students | Share | cross-surface | [TW/Learner] | S18, S24, S26 |
| 24 | AC 06.3 | Whiteboard / annotation synced | Annotation | cross-surface | [TW/Learner] | S18, S19 |
| 25 | AC 06.4 | Public chat visible to all participants | Chat | cross-surface | [TW/Learner] | S18, S21 |
| 26 | AC 06.5 | Private chat visible only to teacher + target student | Chat | permission | [TW/Learner] | S18, S21 |
| 27 | AC 06.6 | Share-screen control hidden in JPREP | Share screen | hidden | [TW] | S19 |
| 28 | AC 06.7 | Disconnect / reconnect restores room state | — | — | [TW/Learner] | S19 |
| 29 | AC 01.1 | Lesson time is sent as epoch (UTC) and shown in JST | Start/End | display | [BO/Learner] | S13 payload |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [CONFLICT] | S25 LT-15745 vs S13/S17 | AC 05.2 | LT-15745 (2022) moved JPREP student lesson list from course **whitelist → blacklist (A+ course)**, but the 2026-09-21 incident proves a course **whitelist** still gates live lessons. Which rule is authoritative for live lesson visibility/Join today? |
| 2 | [REGRESSION RISK] | Qase PX 19523 / 19524 / 25086 | AC 03.3 | Existing JPREP URL cases are 1-step and assume the SF calendar drawer flow; JPREP starts from BO lesson detail. They stay valid for URL only. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [ROLE GAP] | S13, S15 | Admin clicking Start Live Lesson shows "Account is not registered". Expected behavior and flag state per env are not documented. |
| 2 | [MISSING BEHAVIOR] | S13 | Teacher can start a lesson in a non-whitelisted course while students have no Join button. No warning in BO. Is this intended? |
| 3 | [MISSING BEHAVIOR] | S13 ③ | No alert when JPREP syncs an online lesson for a non-whitelisted course. |
| 4 | [UNDOCUMENTED IN AC] | S20 | Recording confirmation dialog behavior is not in any spec. |
| 5 | [MISSING BEHAVIOR] | S21, S26 | Private chat enabled state for JPREP PROD (was turned off in 2023, conversations deleted 2026-05). |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | MANACS-2620 EX240 Join button missing | 2026-09-21 | AC 05.2 | New/irregular course not whitelisted | Negative TC for non-whitelisted course + positive TC per newly whitelisted course (EX240, EX280) |
| 2 | MANACS-2620 late member sync | 2026-09-21 | AC 05.5 | Members synced after start | TC: add student after start, refresh → Join |
| 3 | MANACS-2620 lesson ended by teacher | 2026-09-21 | AC 05.7 | Teacher accidentally ends lesson | TC: End for all → Join gone |
| 4 | MANACS-2343 recording dialog | 2026-05-23 | AC 03.8 | Cancel not clickable | TC for both dialog choices |
| 5 | LT-91604 URL `////` | 2025-12-16 | AC 03.3 | Broken URL | URL assertion TC |
| 6 | LT-98050 wrong account | 2026-03-27 | AC 03.4 | Room opens with previous account | Account switch TC |
| 7 | 2024-03-30 attendees can't see shared PDF | 2024-03-30 | AC 06.2 | Material sharing fails | Share PDF TC with multiple students |
| 8 | 2023 JPREP private chat CPU | 2023-10 | AC 06.5 | Private chat load | Private chat TC (functional) |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| New | JPREP sync → BO start → student join → in-room → end | Not in knowledge/e2e-scenario | CREATE (optional, Phase 6) |

### Assumptions Made

- Env for execution: STG and UAT first, PROD only with JPREP approval (S15).
- STG whitelist = JPREP_COURSE_000000119, JPREP_COURSE_020240109, JPREP_COURSE_000000122, JPREP_COURSE_000000218 (S16). PROD whitelist = 10 courses (S13, 2026-09-25).
- Accounts: STG teacher `jprep.teachertest01` / `jprep.teachertest02` (S10); UAT accounts from S22. Passwords are not copied into test cases.
- "Admin" in this spec = JPREP BO Admin role in S11 (the JPREP role matrix names Admin explicitly).

---

## Clarification Questions (draft — not posted)

1. **[CONFLICT]** LT-15745 switched JPREP lesson list to a blacklist, but the live-lesson Join is gated by a whitelist. Is the whitelist the only rule for live lesson Join today?
2. **[ROLE GAP]** Should a JPREP Admin be able to start a live lesson? What is `User_Auth_AllowAllRolesToLoginTeacherWeb` on STG / UAT / PROD?
3. **[MISSING BEHAVIOR]** Should BO warn the teacher (or block Start) when the course is not whitelisted, since students cannot join?
4. **[LESSON-LEARNED RISK]** Is an alert for non-whitelisted online lessons at sync time in scope, or tracked separately (RCA ③)?
5. **[UNDOCUMENTED IN AC]** Confirm expected recording dialog behavior (Cancel = enter without recording) and whether MANACS-2343 is fixed.
6. **[MISSING BEHAVIOR]** Is private chat currently enabled for JPREP PROD?
7. Which envs have `User_Authentication_ImproveSSO` ON for JPREP?

---

## Related Test Cases (Qase PX)

- 19523, 19524 (suite 2655), 25084, 25086 (suite 3214) — JPREP URL only. Kept; referenced, not duplicated.
- 25076–25085 (suite 3214), 19510–19545 (suites 2651–2657) — core SF/BO calendar live lesson (not JPREP).
- 28764–28766 (suite 3569) — Incident Prevention live lesson (token refresh, reconnect, whiteboard latency).

## QASE Coverage Gaps

- AC 01.2, 02.x, 03.1, 03.2, 03.4–03.8, 04.x, 05.x, 06.x — no JPREP-specific case exists.

---

## Import Summary (Qase, 2026-09-26)

**Project:** PX · Parent: Manabie Scheduling (18) > OOP FEATURES (311)

| Suite | Status | Qase Suite ID | Cases |
|---|---|---|---|
| JPREP | Created | 3575 | – |
| [JPREP] Live Lesson | Created | 3576 | – |
| [JPREP] Live Lesson – BO Course Lesson Tab & Lesson Detail | Created | 3577 | PX-28993 – 28998 (6) |
| [JPREP] Live Lesson – Start from BO | Created | 3578 | PX-28999 – 29008 (10) |
| [JPREP] Live Lesson – Student Join & Course Whitelist | Created | 3579 | PX-29009 – 29017 (9) |
| [JPREP] Live Lesson – Weekly Materials | Created | 3580 | PX-29018 – 29021 (4) |
| [JPREP] Live Lesson – In-room Key Features | Created | 3581 | PX-29022 – 29031 (10) |

Totals: suites created 7 · cases created 39 · skipped (duplicates) 0 · failed 0 (one bulk call timed out and was re-sent after confirming nothing was created).
Old JPREP URL cases PX-19523, 19524, 25084, 25086 (created by Linh Nguyen) were fully covered by PX-29000 / PX-29002 and deleted on 2026-09-26 after user confirmation; PX-29000 step 5 now also asserts user_id is not empty.
All 39 cases re-fetched: title, preconditions, step count and every action/expected result match the local source.
