# Live Lesson - Suite 3214 - Testcase Formatter V2

## Scope
- Total cases: 11
- Core flow: 6 cases
- URL/Auth: 5 cases
- Language: English
- Start Lesson button location: BO Calendar lesson detail panel (right panel)

## Case 1
Case ID: [UNKNOWN]
App/Domain: BackOffice
Env/Tenant: [UNKNOWN]
Title: Live Lesson - Start Lesson is visible when Teaching Medium is Online
Preconditions:
- Teacher is logged in to BackOffice.
- BO Calendar lesson detail panel (right panel) can be opened.
- Teaching Medium is Online.
Steps:
1. Open BO Calendar lesson detail panel (right panel) for an online lesson.
2. Check action area at the bottom of BO Calendar right panel.
Expected:
1. BO Calendar lesson detail panel opens successfully.
2. Start Lesson button is visible.

## Case 2
Case ID: [UNKNOWN]
App/Domain: BackOffice
Env/Tenant: [UNKNOWN]
Title: Live Lesson - Start Lesson must NOT be visible when Teaching Medium is Offline
Preconditions:
- Teacher is logged in to BackOffice.
- BO Calendar lesson detail panel (right panel) can be opened.
- Teaching Medium is Offline.
Steps:
1. Open BO Calendar lesson detail panel (right panel) for an offline lesson.
2. Check action area at the bottom of BO Calendar right panel.
Expected:
1. BO Calendar lesson detail panel opens successfully.
2. Start Lesson button must NOT be visible.

## Case 3
Case ID: [UNKNOWN]
App/Domain: BackOffice
Env/Tenant: [UNKNOWN]
Title: Live Lesson - Clicking Start Lesson opens live session and keeps BackOffice tab context
Preconditions:
- Teacher is logged in to BackOffice.
- An online lesson in BO Calendar shows Start Lesson.
- Session is valid and not expired.
Steps:
1. Open BO Calendar lesson detail panel (right panel) for an online lesson.
2. Click Start Lesson.
3. Observe redirect behavior.
Expected:
1. BO Calendar lesson detail panel opens and Start Lesson is shown.
2. Click action is executed successfully.
3. Live lesson session opens and BackOffice tab context is preserved.

## Case 4
Case ID: [UNKNOWN]
App/Domain: BackOffice
Env/Tenant: [UNKNOWN]
Title: Live Lesson - With valid SSO session the flow should NOT ask for login again after Start Lesson
Preconditions:
- Teacher is logged in to BackOffice with valid session.
- An online lesson in BO Calendar shows Start Lesson.
Steps:
1. Open BO Calendar lesson detail panel (right panel).
2. Click Start Lesson.
3. Observe destination screen.
Expected:
1. BO Calendar lesson detail panel opens successfully.
2. Redirect to live lesson is triggered.
3. System should NOT show login screen again.

## Case 5
Case ID: [UNKNOWN]
App/Domain: BackOffice
Env/Tenant: [UNKNOWN]
Title: Live Lesson - When live lesson service is unavailable the system shows error and must NOT lose current context
Preconditions:
- Teacher is logged in to BackOffice.
- An online lesson in BO Calendar shows Start Lesson.
- Environment can simulate live lesson service unavailable.
Steps:
1. Open BO Calendar lesson detail panel (right panel) for an online lesson.
2. Click Start Lesson while service is unavailable.
3. Observe message and current screen state.
Expected:
1. BO Calendar lesson detail panel opens successfully.
2. Click action is sent.
3. System shows proper error and must NOT lose BackOffice context.

## Case 6
Case ID: [UNKNOWN]
App/Domain: BackOffice + Learner
Env/Tenant: [UNKNOWN]
Title: Live Lesson - Student can join after teacher starts live lesson
Preconditions:
- Teacher is logged in to BackOffice.
- Student is logged in to Learner App.
- Student is assigned to valid online lesson.
- BO Calendar lesson detail panel shows Start Lesson for teacher.
Steps:
1. Teacher opens BO Calendar lesson detail panel (right panel) in BackOffice.
2. Teacher clicks Start Lesson.
3. Student opens the same lesson in Learner App.
4. Student joins live lesson.
Expected:
1. BO Calendar lesson detail panel opens successfully for teacher.
2. Live lesson session is created.
3. Learner App shows lesson as joinable.
4. Student joins successfully and should NOT receive permission error.

## Case 7
Case ID: [UNKNOWN]
App/Domain: BackOffice
Env/Tenant: [UNKNOWN]
Title: Live Lesson - URL uses new redirect format when ImproveSSO flag is ON
Preconditions:
- Teacher is logged in to BackOffice.
- An online lesson in BO Calendar shows Start Lesson.
- Feature flag User_Authentication_ImproveSSO is ON.
Steps:
1. Open BO Calendar lesson detail panel (right panel) for an online lesson.
2. Click Start Lesson.
3. Observe opened redirect URL.
Expected:
1. BO Calendar lesson detail panel opens successfully.
2. Click action is executed successfully.
3. Redirect URL follows new format and data is valid by tenant rule.

## Case 8
Case ID: [UNKNOWN]
App/Domain: BackOffice
Env/Tenant: [UNKNOWN]
Title: Live Lesson - URL uses legacy format when ImproveSSO flag is OFF
Preconditions:
- Teacher is logged in to BackOffice.
- An online lesson in BO Calendar shows Start Lesson.
- Feature flag User_Authentication_ImproveSSO is OFF.
Steps:
1. Open BO Calendar lesson detail panel (right panel) for an online lesson.
2. Click Start Lesson.
3. Observe opened redirect URL.
Expected:
1. BO Calendar lesson detail panel opens successfully.
2. Click action is executed successfully.
3. URL follows legacy format and should NOT use new redirect format.

## Case 9
Case ID: [UNKNOWN]
App/Domain: BackOffice
Env/Tenant: [UNKNOWN]
Title: Live Lesson - JPREP URL has correct structure and should NOT contain double slash
Preconditions:
- Teacher is logged in to BackOffice.
- An online lesson in BO Calendar exists in JPREP tenant.
- Start Lesson is visible and clickable.
Steps:
1. Open BO Calendar lesson detail panel (right panel) for an online lesson in JPREP.
2. Click Start Lesson.
3. Observe redirect URL in destination tab.
Expected:
1. BO Calendar lesson detail panel opens successfully.
2. Click action is executed successfully.
3. URL matches JPREP structure and must NOT contain double slash in path.

## Case 10
Case ID: [UNKNOWN]
App/Domain: BackOffice
Env/Tenant: [UNKNOWN]
Title: Live Lesson - URL contains user_id parameter according to tenant rule
Preconditions:
- Teacher is logged in to BackOffice.
- An online lesson in BO Calendar shows Start Lesson.
- Tenant requires user_id in redirect URL.
Steps:
1. Open BO Calendar lesson detail panel (right panel) for an online lesson.
2. Click Start Lesson.
3. Observe query parameters in redirect URL.
Expected:
1. BO Calendar lesson detail panel opens successfully.
2. Click action is executed successfully.
3. URL contains user_id for teacher identity and must NOT be empty.

## Case 11
Case ID: [UNKNOWN]
App/Domain: BackOffice
Env/Tenant: [UNKNOWN]
Title: Live Lesson - With pop-up blocker enabled the system shows guidance or fallback
Preconditions:
- Teacher is logged in to BackOffice.
- An online lesson in BO Calendar shows Start Lesson.
- Browser pop-up blocker is ON.
Steps:
1. Open BO Calendar lesson detail panel (right panel) for an online lesson.
2. Click Start Lesson while pop-up blocker is ON.
3. Observe guidance message or fallback behavior.
Expected:
1. BO Calendar lesson detail panel opens successfully.
2. Click action is executed.
3. System shows guidance/fallback as designed and must NOT crash/show blank screen.
