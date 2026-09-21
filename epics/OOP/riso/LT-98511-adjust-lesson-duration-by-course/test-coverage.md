# Test Coverage: LT-98511 - Adjust Lesson Duration by Course

## Scope

Validate Riso Location Course duration configuration and lesson creation duration calculation. The main risk is silent wrong lesson time: staff may think the selected course has applied a shorter lesson duration, while the form still uses the 80-minute timeslot or keeps a stale manual value.

## Requirement Mapping

| ID | Requirement | Risk | Coverage |
|---|---|---|---|
| R1 | Location Course exposes optional duration only when config ON | High | TC-01, TC-02, TC-08 |
| R2 | Blank duration remains blank and does not block saving | Medium | TC-01, TC-02 |
| R3 | Saved Location Course duration is used by lesson creation | Critical | TC-03 |
| R4 | Location Course duration overrides timeslot duration | Critical | TC-03 |
| R5 | Timeslot duration is used when Location Course duration is blank | Critical | TC-04 |
| R6 | No duration source preserves existing default/manual behavior | Medium | TC-05 |
| R7 | Duration, Start Time, and End Time remain manually editable | High | TC-06 |
| R8 | Timeslot change recalculates after manual edits | High | TC-07 |
| R9 | Location Course change recalculates after manual edits | High | TC-08 |
| R10 | Non-Riso/OFF config keeps existing behavior | High | TC-08 |

## Test Design

| Case ID | Title | Technique | Depth | Priority |
|---|---|---|---|---|
| TC-01 | Location Course duration field - Config ON displays optional field and saves value | Configuration + CRUD | Deep | High |
| TC-02 | Location Course duration field - Blank default remains blank | Negative/Default | Medium | High |
| TC-03 | Lesson creation - Location Course duration overrides 80-minute timeslot | Decision Table | Deep | High |
| TC-04 | Lesson creation - Blank Location Course duration falls back to timeslot | Decision Table | Deep | High |
| TC-05 | Lesson creation - No course duration and no timeslot keeps existing default/manual behavior | Negative/Regression | Medium | Medium |
| TC-06 | Lesson creation - Manual Duration, Start Time, and End Time edits are retained until source change | State Retention | Deep | High |
| TC-07 | Lesson creation - Timeslot change recalculates after manual override | State Transition | Deep | High |
| TC-08 | Lesson creation - Location Course change recalculates and config OFF preserves old behavior | State Transition + Scope Guard | Deep | High |

## Test Data

| Fixture | Value | Purpose |
|---|---|---|
| Timeslot 1 | 09:00-10:20, 80 mins | Default Riso lesson duration |
| Timeslot 2 | 11:00-12:20, 80 mins | Recalculation after source change |
| Course A | Location Course Duration = 50 | Younger-student short lesson |
| Course B | Location Course Duration blank | Timeslot fallback |
| Course C | Location Course Duration = 60 | Course-change recalculation |
| Config ON | `config_Lesson_Location_Lesson_Duration__c = true` | Riso enabled behavior |
| Config OFF | `config_Lesson_Location_Lesson_Duration__c = false` | Non-Riso / disabled guard |

## Suggested Test Suite Structure

| Suite | Parent Suite | Purpose |
|---|---|---|
| Adjust Lesson Duration by Course (LT-98511) | Riso OOP | Location Course duration config and lesson creation duration calculation |
