# Calendar Access by User Type

Calendar visibility depends on the user's role and login type. The CPU vs SPU distinction is **Aver-specific**; other partners use affiliation-based location access regardless of login type.

## Access matrix

| User Type | Login Type | Access Method |
|---|---|---|
| PT Teacher | CPU (teacher login) | Get lesson by **lesson teacher** |
| Teacher | CPU | Get lesson by **lesson teacher** |
| Centre Manager | SPU (staff login) | Get lesson by **lesson location** |
| HQ Staff | SPU | Get lesson by **lesson location** |
| Centre Staff | SPU | Get lesson by **lesson location** |
| Brand Staff | SPU | Get lesson by **lesson location** |

## Access behavior by organization

- **Aver:** CPU users (teachers) see only lessons they're assigned to as teacher. SPU users see lessons at their affiliated locations. **This CPU/SPU distinction is Aver-specific.**
- **Other partners (Renseikai, Nichibei, Aso, Riso, Koyu, etc.):** All users follow **affiliation-based location access** — they see lessons at locations they are affiliated with, regardless of CPU/SPU login type.

## Cross-location teacher access

- Teachers can be assigned to lessons at **different locations** from their affiliation (triggers an alert but is allowed).
- Once assigned, the teacher retains access to the lesson even if students from their location are removed (51 cases: "View from another location").
- See `../lesson-management/lesson-teacher.md` § Cross-Location Access for details.

## Limit Teacher (Nichibei-specific)

When the `lesson.limit_teacher_access_other_lessons.is_enabled` config is enabled, CPU teachers' access to BO Calendar and Lesson List is further constrained. See `../partner-rules/nichibei-lesson-allocation.md` § Limit Teacher.
