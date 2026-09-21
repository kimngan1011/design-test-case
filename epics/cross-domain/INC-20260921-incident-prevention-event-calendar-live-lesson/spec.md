# INC-20260921: Incident Prevention for Event, Calendar, Live Lesson, and Lesson-Learn

## Scope

This prevention set converts recurring JP incident patterns into reusable test coverage for:

- Event booking and event participant creation.
- SF Calendar and lesson scheduling flows.
- Live lesson and Zoom/Agora entry flows.
- Lesson-learn data integrity for study plans and learning time.

## Source Evidence

- Slack channel: `#jp_incidents` (`C0BPM7GABDW`), accessible history from 2021-08-07 to 2026-09-18.
- Qase root suite: Incident Prevention (`PX?suite=2183`).
- Qase child suite created for this work: `Incident Prevention - Event Calendar Live Lesson Lesson-Learn` (`suite_id=3569`).
- Existing related Qase cases found under suite 2183 tree:
  - `PX-15467`, `PX-14019`, `PX-15454`, `PX-15455`, `PX-15456`, `PX-15457`.
  - `PX-16248`, `PX-16249`, `PX-16250`, `PX-16251`, `PX-16252`.
  - `PX-16714`, `PX-17111`, `PX-17112`, `PX-17113`, `PX-17114`.

## Existing Coverage Impact

The existing suite covers isolated prevention points:

- Lesson duration edit and past recurring lesson behavior.
- Trial student assignment to a one-time lesson.
- Migrated student/parent attendance, Zoom link generation, live lesson join, and event participant duplication when switching accounts.
- Attendance note clearing.
- Lesson allocation total-session count around order actions.

## Main Gaps

| Area | Gap |
|---|---|
| Event booking | No broad org config matrix for event enabled/disabled, internal vs external booking, direct link, search/list limit, target segment aggregate limits, and concurrent reservation. |
| Calendar/lesson | No broad data-integrity coverage for generated/imported lessons, zero Student Sessions with active Class Members, duplicate lessons, location/timezone boundary, and Lesson Allocation side effects. |
| Live lesson | No coverage for provider token refresh, shared sessions, reconnect, tab switch, SDK/provider upgrade smoke, whiteboard/poll latency, and Zoom one-way sync. |
| Lesson-learn | No coverage for large-course study plan batching, duplicate/empty study plan item prevention, CSV update behavior, multi-tab learning time, stale sessions, and data checkers. |
| Release/config | No prevention case asserting feature flag parity, hotfix job isolation, and platform-event/background-job health during release windows. |

## Qase Target

- Parent suite: `Incident Prevention` (`suite_id=2183`).
- Child suite: `Incident Prevention - Event Calendar Live Lesson Lesson-Learn` (`suite_id=3569`).
- Created Qase cases: `PX-28764` through `PX-28777`.
