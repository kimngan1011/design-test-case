# Test Coverage: LT-XXXX — Cross-organization account switching

## 1. Business Rules

1. **AC PX-320.01:** A parent linked to a Renseikai student and an Asojuku student can switch the selected student and view only that student's lesson details.
2. **AC PX-320.02:** The same parent can view only the selected student's lesson report.
3. **AC PX-320.03:** Attendance submitted after a switch is recorded for the selected student only.
4. **AC PX-1507.01:** Students at Renseikai and Asojuku can each join their own Zoom lesson.
5. **AC PX-331.01:** Students at Renseikai and Asojuku can each submit the survey for their own completed lesson.
6. **AC PX-331.02:** A parent can switch between those students and view the selected student's submitted survey.
7. **AC PX-504.01:** Point Consumption is shown for Nichibei and hidden for Renseikai after a parent switches students.
8. **AC PX-2762.01:** A parent can switch across organizations and book a lesson for each selected student.
9. **AC PX-3249.01:** Contract Info and Lesson History are available for Riso and unavailable for Nichibei after a parent switches students.

## 4. Coverage Strategy

| AC | Technique | Risk | Depth |
|---|---|---|---|
| PX-320.01 to PX-320.03 | Scenario | Medium | Standard |
| PX-1507.01 | Scenario | Medium | Smoke |
| PX-331.01 to PX-331.02 | Scenario | Medium | Standard |
| PX-504.01 | Decision Table | Medium | Standard |
| PX-2762.01 | Scenario | Medium | Standard |
| PX-3249.01 | Decision Table | Medium | Standard |

## 7. Suggested Test Suite Structure

1. Lesson Mobile
2. View and join lesson zoom
3. Lesson Survey
4. Point Consumption
5. Lesson Booking
6. [Riso] OOP| Contract and Monthly Lesson history (App)
