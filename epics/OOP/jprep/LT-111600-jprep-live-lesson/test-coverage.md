# Test Coverage: LT-111600 — JPREP Live Lesson

**Jira:** https://manabie.atlassian.net/browse/LT-111600 (epic LT-54444)
**Date:** 2026-09-26

---

## 1. Business Rules Extracted

See `spec.md` § Business Rules (29 rules, BR1–BR29, each with source IDs S1–S26).

## 2. Logic Type Categorization

| AC | BR # | Logic Type |
|---|---|---|
| AC 01.1 / 01.2 | 1, 2, 29 | Cross-system, State transition, Date/time display |
| AC 02.1 / 02.2 | 3, 4 | Display completeness, Cross-surface navigation |
| AC 03.1 | 5 | Conditional |
| AC 03.2 / 03.3 / 03.4 | 6, 7, 8 | Cross-system, Conditional (feature flag), Data integrity |
| AC 03.5 / 03.6 | 9, 10 | State transition |
| AC 03.7 | 11 | Permission |
| AC 03.8 | 12 | Conditional |
| AC 04.x | 13, 14, 15 | CRUD, Permission, Cross-system |
| AC 05.1 | 16 | Display completeness |
| AC 05.2–05.4 | 17, 18 | Conditional (config-driven), State transition |
| AC 05.5–05.7 | 19, 20, 21 | Cross-system, State transition |
| AC 06.x | 22–28 | Cross-surface, Permission, State |

## 3. Test Technique Selection

| Logic Type | Techniques |
|---|---|
| Conditional | Decision Table, Negative |
| Config-driven (whitelist) | Equivalence Partitioning (whitelisted / not), Regression per newly added course |
| State transition | State Transition |
| Permission | Permission Matrix |
| Cross-system | Regression, Scenario |
| CRUD | CRUD |
| Display completeness | Component |

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Technique | Risk | Depth |
|---|---|---|---|---|---|
| AC 02.1 | Paired lesson name per week | Display | Component | Medium | Standard |
| AC 02.2 | Lesson name opens detail | Cross-surface | Scenario | Medium | Standard |
| AC 03.1 | Start button Online vs Offline | Conditional | Decision Table | High | Deep |
| AC 01.2 | Offline→Online via sync | State transition | State Transition | High | Standard |
| AC 01.1 | JST/UTC display boundary | Date/time | BVA (TZ) | Medium | Standard |
| AC 03.2 | Start → TW room, SSO, new tab | Cross-system | Scenario | Critical | Deep |
| AC 03.3 | URL format flag OFF / ON | Conditional | Decision Table | High | Deep |
| AC 03.4 | Account switch | Data integrity | Scenario | High | Standard |
| AC 03.5 | Refresh stays in room | State | State Transition | Medium | Standard |
| AC 03.6 | Leave/End closes tab | State | State Transition | Medium | Standard |
| AC 03.7 | Teacher vs Admin | Permission | Permission Matrix | High | Deep |
| AC 03.8 | Recording dialog Cancel / Start | Conditional | Decision Table | High | Deep |
| AC 04.1 | Admin add / delete material | CRUD | CRUD | Medium | Standard |
| AC 04.2 | Teacher read-only | Permission | Permission Matrix | Medium | Standard |
| AC 04.3 | Material available in room | Cross-system | Regression | High | Standard |
| AC 05.1 | Learner schedule + materials | Display | Component | Medium | Standard |
| AC 05.2 | Whitelisted course → Join | Config | EP | Critical | Deep |
| AC 05.3 | Non-whitelisted → no Join | Config | EP / Negative | Critical | Deep |
| AC 05.4 | Added to whitelist → Join after refresh | State | State Transition | High | Standard |
| AC 05.2 | Newly whitelisted EX240 / EX280 (PROD) | Config | Regression | Critical | Smoke |
| AC 05.5 | Late member sync | Cross-system | Scenario | High | Standard |
| AC 05.6 | Waiting room | State | State Transition | Medium | Standard |
| AC 05.7 | End for all | State | State Transition | High | Standard |
| AC 06.1 | Cam/mic toggle + rapid clicks | State | Scenario + Negative | High | Standard |
| AC 06.2 | Share PDF / image / video | Cross-surface | Scenario | High | Standard |
| AC 06.3 | Whiteboard / annotation | Cross-surface | Scenario | Medium | Standard |
| AC 06.4 | Public chat | Cross-surface | Scenario | Medium | Standard |
| AC 06.5 | Private chat | Permission | Permission Matrix | High | Standard |
| AC 06.6 | Share screen hidden | Conditional | Negative | Low | Smoke |
| AC 06.7 | Reconnect | State | State Transition | High | Standard |

## 4.5 Edge-case checklist (summary)

- **A Config thresholds** — whitelist: in / not in / added while lesson exists → covered (AC 05.2–05.4). Removing a course: N/A (no removal flow requested).
- **B Date/time** — sync epoch vs JST display, date boundary 00:30 JST → 1 TC. Cross-midnight while open: N/A (lesson start/end only).
- **C Concurrent** — account switch (multi-session) → TC; rapid cam/mic taps → TC. Double click Start: covered by rapid-click note in Start TC.
- **D Permission** — Teacher, Admin (flag OFF / ON), Student, non-member student → TCs. Cross-tenant: N/A (JPREP-only org).
- **E State** — Offline→Online, Waiting→In room, In room→Ended, Refresh, Disconnect→Reconnect → TCs.
- **F Cross-system** — sync → BO → TW → Learner → TCs.
- **G Downstream** — Start lesson → room opened for students (Join), End → Join removed; Upload material → visible in Teacher view + room; Delete material → removed in both.
- **H Display** — Course Lesson tab (Week, Lesson name), Lesson detail (Start button), Learner lesson card (lesson name, time, materials, Join).
- **H.1 Figma** — N/A for this run: Figma file (Back-Office rOZgu6kDszz3t7NMvOkTET) predates current UI; assertions use current labels observed in incident screenshots/Slack.

## 5. High-Risk Areas

### 🔴 Critical
| Area | Reason | Approach |
|---|---|---|
| Course whitelist gates student Join | Caused 2026-09-21 PROD incident, class moved to Zoom | Positive + negative + add-to-whitelist + per-new-course smoke |
| Start from BO opens room | Only entry point for JPREP teachers | End-to-end with SSO and new tab |

### 🟠 High
| Area | Reason | Approach |
|---|---|---|
| URL format / account identity | Past hotfixes LT-91604, LT-98050 | Flag decision table + switch account |
| Admin start | Unclear, error seen in PROD | Permission matrix with flag states |
| Recording dialog | MANACS-2343 | Both choices |
| End for all / late sync | Incident side findings | State transition TCs |

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing TC | Overlap | New Coverage Needed |
|---|---|---|---|
| JPREP URL format (flag OFF) | PX-19523, PX-25086 | Partial (URL only, 1 step) | ✅ Full BO→TW flow with user_id |
| user_id in URL | PX-19524, PX-25084 | Partial | ✅ merged into URL TC + switch account |
| Course Lesson tab | none | None | ✅ |
| Start button Online/Offline (JPREP BO lesson detail) | PX-19510/25076/25078 (SF calendar drawer) | Different surface | ✅ |
| Whitelist / Join | none | None | ✅ |
| Materials JPREP | PX-19541–19545 (SF drawer) | Different surface/role | ✅ |
| In-room features JPREP | PX-28765/28766 (generic) | Partial | ✅ JPREP-only (private chat, recording, share screen hidden) |

## 7. Suggested Test Suite Structure

```
Qase PX > Manabie Scheduling > OOP FEATURES (311) > JPREP (new) > [JPREP] Live Lesson (new)
epics/OOP/jprep/LT-111600-jprep-live-lesson/test-cases/
├── jprep-live-lesson-bo-course-and-detail.md   → AC 01.x, 02.x, 03.1  (6 TCs)
├── jprep-live-lesson-start-from-bo.md          → AC 03.2–03.8          (10 TCs)
├── jprep-live-lesson-student-join-whitelist.md → AC 05.x               (9 TCs)
├── jprep-live-lesson-materials.md              → AC 04.x               (4 TCs)
└── jprep-live-lesson-in-room-features.md       → AC 06.x               (10 TCs)
```
