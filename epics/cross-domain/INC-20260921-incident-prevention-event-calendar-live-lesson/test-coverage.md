# Test Coverage: Incident Prevention - Event, Calendar, Live Lesson, Lesson-Learn

## Strategy

The cases are manual prevention checks designed for release gates, hotfix verification, and incident-retro regression. They emphasize end-to-end data integrity over isolated UI checks.

## Coverage Matrix

| ID | Area | Risk | Existing Qase Coverage | New Case |
|---|---|---|---|---|
| IP-01 | Live lesson | Expired provider/session token blocks lesson start | Partial: `PX-15457`, `PX-16249` | Yes |
| IP-02 | Live lesson | Network interruption, tab switch, or shared session breaks join state | Partial: `PX-16249` | Yes |
| IP-03 | Live lesson | Whiteboard/poll/annotation latency or undo/redo breaks class flow | No direct coverage | Yes |
| IP-04 | Zoom | One-way Zoom sync creates stale links after edit/delete/regenerate | Partial: `PX-15457` | Yes |
| IP-05 | Calendar/Lesson | Published/imported lesson has active class members but no Student Sessions | Partial: `PX-15454`, `PX-14019` | Yes |
| IP-06 | Calendar/Lesson | Lesson Allocation/order lifecycle silently removes or mislinks sessions | Partial: `PX-17111`-`PX-17114` | Yes |
| IP-07 | Calendar/Lesson | Lesson report/calendar location/student-session data inconsistent after publish/edit | Partial: `PX-16714` | Yes |
| IP-08 | Calendar/Lesson | Recurring/full-year import creates duplicates or partial schedules | Partial: `PX-15467` | Yes |
| IP-09 | Event booking | Event org config and internal/external booking routes diverge | Partial: `PX-16248` | Yes |
| IP-10 | Event booking | Search/list limit or target segment query hides valid students/events | No direct coverage | Yes |
| IP-11 | Event booking | Event participant duplication under switch account or concurrent booking | Existing: `PX-16250`-`PX-16252` | Yes, expanded |
| IP-12 | Lesson-learn | Large course study plan update creates duplicate/empty/missing items | No direct coverage | Yes |
| IP-13 | Lesson-learn | Multi-tab/stale session creates incorrect learning time | No direct coverage | Yes |
| IP-14 | Release/config | Feature flag, hotfix, background job, or provider SDK change escapes to PROD | No direct coverage | Yes |

## Existing Impacted Cases

Keep these in combined regression runs because they are still relevant and should not be duplicated:

- `PX-15467`, `PX-14019`, `PX-15454`, `PX-15455`, `PX-15456`, `PX-15457`.
- `PX-16248`, `PX-16249`, `PX-16250`, `PX-16251`, `PX-16252`.
- `PX-16714`, `PX-17111`, `PX-17112`, `PX-17113`, `PX-17114`.

## Output

- Test case markdown: `test-cases/incident-prevention-event-calendar-live-lesson.md`
- Qase import CSV: `test-cases/incident-prevention-event-calendar-live-lesson.csv`
- Qase child suite: `Incident Prevention - Event Calendar Live Lesson Lesson-Learn` (`suite_id=3569`)
- New Qase cases: `PX-28764`, `PX-28765`, `PX-28766`, `PX-28767`, `PX-28768`, `PX-28769`, `PX-28770`, `PX-28771`, `PX-28772`, `PX-28773`, `PX-28774`, `PX-28775`, `PX-28776`, `PX-28777`
