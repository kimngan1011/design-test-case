# LT-98529 Test Coverage

## Coverage Matrix

| Case ID | Area | AC | Coverage Type | Risk |
|---|---|---|---|---|
| LT-98529-TC-001 | SF Lesson Form | US01.1 | Component / Config | Field missing when setting ON |
| LT-98529-TC-002 | SF Lesson Form | US01.1 | Negative / Config | Field exposed when setting OFF |
| LT-98529-TC-003 | SF Save | US01.1, US01.3 | BVA | 32,768-char note save |
| LT-98529-TC-004 | SF Save | US01.1 | Negative / BVA | 32,769-char note invalid/truncated |
| LT-98529-TC-005 | BO Lesson Form | US01.1 | Component / Config | BO feature setting mismatch |
| LT-98529-TC-006 | BO Save | US01.3 | Integration | BO note not saved to Lesson |
| LT-98529-TC-007 | Permissions | US01.2 | Role/Permission | Read-only user can edit note |
| LT-98529-TC-008 | SF Calendar Info | US01.4 | Display | Calendar information misses note |
| LT-98529-TC-009 | App Calendar Card | US02.1 | Component | Note tag not shown for valued note |
| LT-98529-TC-010 | App Calendar Card | US02.1 | Negative | Note tag shown for blank note |
| LT-98529-TC-011 | App Lesson Detail | US02.2 | Component | Note section content/label/layout |
| LT-98529-TC-012 | App Lesson Detail | US02.2 | Negative | Blank note section still occupies UI |
| LT-98529-TC-013 | App Lesson Detail | US02.2 | Data Format | Line breaks/plain text escaped incorrectly |
| LT-98529-TC-014 | Data Sync | US01.3, US02.1, US02.2 | State Transition | Edit note not reflected immediately |
| LT-98529-TC-015 | Data Sync | US01.3, US02.1, US02.2 | State Transition | Clearing note leaves stale App tag |
| LT-98529-TC-016 | App Calendar Card | US03.1 | Component | Timeslot card format |
| LT-98529-TC-017 | App Lesson Detail | US03.2 | Component | Timeslot detail row/label |
| LT-98529-TC-018 | App Timeslot | US03.1, US03.2 | Negative | No-timeslot lesson renders empty parentheses |
| LT-98529-TC-019 | App Timeslot Config | US03.1, US03.2 | Config | Timeslot shown when partner config OFF |
| LT-98529-TC-020 | Localization | US02.1, US02.2, US03.2 | i18n | EN/JP labels wrong |
| LT-98529-TC-021 | App Access | US02, US03 | Role/Scope | Parent/student sees unrelated lesson note |
| LT-98529-TC-022 | Regression | US03 + LT-98530 | Regression | Existing Lesson History timeslot display breaks |
| LT-98529-TC-023 | BO Lesson Form | US01.1 | Negative / Config | BO exposes Lesson Note when feature setting OFF |
| LT-98529-TC-024 | App Calendar/Detail | US02.1, US02.2 | Negative / Blank Handling | Whitespace-only note renders empty tag/section |

## Data Fixtures

- `Lesson A`: Published lesson, student assigned, note = `Bring workbook A\nUse classroom entrance B`, Timeslot = `TimeSlot S`, 09:00-10:00.
- `Lesson B`: Published lesson, student assigned, note blank, Timeslot blank, 10:20-11:20.
- `Lesson C`: Published lesson, student assigned, note whitespace-only, Timeslot = `TimeSlot T`, 13:00-14:00.
- `Lesson D`: Published lesson for another student/child, note exists, Timeslot exists.
- `Timeslot S`: active Timeslot Master, Name = `TimeSlot S`, Start = 09:00, End = 10:00, Sequence = 1.
- `Timeslot T`: active Timeslot Master, Name = `TimeSlot T`, Start = 13:00, End = 14:00, Sequence = 2.

## Config Matrix

| Config | ON Expectation | OFF Expectation |
|---|---|---|
| `Lesson_Custom_Settings__c.Show_Lesson_Note__c` | SF field/detail visible | SF field/detail hidden |
| `lesson.lesson_note.is_enabled` | BO field/detail visible | BO field/detail hidden |
| `Lesson_Custom_Settings__c.Show_Timeslot_In_Lesson__c` | App Timeslot display allowed | App Timeslot hidden |

## Automation Notes

- Assert data at three levels for note cases: SF/BO field value, API/record value, App UI display.
- Use App Calendar card text selectors for tag and time line, then open the same lesson detail to verify full note content.
- For line break test, use a note with two lines and symbols: `Bring workbook A\nUse classroom entrance B <Room 301>`.
- For permission test, use an account with Lesson read permission but no update permission if available; otherwise verify disabled/read-only field state through an existing restricted Lesson profile.
- For parent account, switch selected child and verify only that child's allocated lessons expose notes/timeslots.

## Regression Guardrails

- Do not require Lesson Report to exist or be published for Lesson Note display.
- Do not assert rich-text rendering; PRD says plain text.
- Do not use SF formula `Lesson_Timeslot__c` format as App expected format.
- Do not include unrelated Contract Info or Monthly Lesson History calculation tests; those belong to LT-98530.
