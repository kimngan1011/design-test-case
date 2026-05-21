# Class Assignment (Auto-Assign / Auto-Remove + Multi-Class Lessons)

Class-based auto-assignment links students to lessons via Class Member records through the Master Queue. A single lesson can have **multiple classes assigned** (LT-74136, feature-flagged), but the auto-assign/remove behavior is the same regardless of single vs multi-class.

## Auto-Assign / Auto-Remove flow

```
Student ──enrolled in──→ Course ──→ Class ──→ Class Member (with duration)
                                                    │
                                 ┌──────────────────┘
                                 ↓
                          Run Master Queue
                                 │
                    ┌────────────┼────────────┐
                    ↓            ↓            ↓
              Assign student  Remove student  Remain in
              to lesson       from lesson     completed
              (within class   (outside class  lessons
              member duration) member duration)
```

### Triggers

1. Create / import new lesson.
2. Assign a class to student.
3. Update LA duration.
4. Update lesson schedule class (LSC).
5. Add/remove an LSC record via the related list on an existing lesson (multi-class case — students from added class are auto-assigned; from removed class are auto-removed).
6. Bulk Assign Class on UI (Location Course page).
7. Individual Assign Class (Contact page).
8. Bulk Assign Class by Academic Level (Contact page).
9. Class Member Import (Salesforce Import Wizard).

### Behavior

- **Within class member duration** → student is **assigned** to lessons matching the class.
- **Outside class member duration** → student is **removed** from lessons.
- **Completed lessons** → student **remains** even if outside duration (historical preservation).

### Duplicate prevention (LT-99546)

Unique-key constraint on `(student_id, lesson_id)` prevents duplicate Student Sessions when a student belongs to multiple classes assigned to the same lesson. LA Lesson Allocated count increments only once per unique (student, lesson) assignment.

### Nichibei exception

Nichibei does NOT use class-based auto-assignment. See `../partner-rules/nichibei-lesson-allocation.md`.

### Performance

Handles 50–100 students per class via async Master Queue batch processing.

---

## Multiple Classes per Lesson (LT-74136, 2026-05-18)

Core feature (all orgs). Extends lesson creation from single-class to multi-class via a new **Lesson Schedule Class (LSC)** junction object. **Only the lesson creation/configuration changes — the auto-assign/auto-remove behavior above is unchanged.**

### Feature Flags

| Flag | Type | Purpose |
|---|---|---|
| `Multiple_Classes_In_Lesson__c` | SF Custom Setting | Enables multi-class selection on SF lesson creation UI |
| `Lesson_BackOffice_LessonSF_MultipleClassesSF` | Unleash | Enables multi-class display on BO and Calendar |

**When flag is OFF:** System reverts to single-class behavior. Class field shows as single-select. Already-created multi-class lessons display as single class.

### Lesson Schedule Class (LSC)

Junction object linking a Lesson Schedule to multiple Class records.

| Field | Type | Notes |
|---|---|---|
| Lesson Schedule | Master-Detail (parent) | Cascade-deletes LSC when LS deleted |
| Class | Lookup | Links to Class record |

- **Deprecated:** `Class` field on `Lesson Schedule` object — migrated to LSC at DB level; **not shown on any UI surface** (SF or BO) post-migration.
- **Class formula field on Lesson:** auto-calculated from LSC records; displays comma-separated class names.

### Class Selection Rules (SF Lesson Creation)

- Multi-select field: staff can select **multiple classes under the same course** when creating a lesson.
- **Recurring lessons:** all selected classes applied to every lesson in the chain upon generation.
- **Course field + Class field: locked (non-editable) after lesson creation via the Lesson form.**
- **Post-creation edit via LSC related list:** Staff CAN add/remove Lesson Schedule Class records via the related list on an existing lesson. When a class is removed, students from that class are auto-removed; when added, students from that class are auto-assigned (per the auto-assign/auto-remove flow above).

### CSV Import Rules

| Teaching Method | Class field behavior |
|---|---|
| **Group** | Multi-class supported; semicolon-delimited (e.g., `Class A;Class B`) |
| **Individual** | Class field **hidden** — multi-class input not possible |

**New import steps (To-Be):**
1. Create Lesson Schedule
2. Create Lesson Schedule Class (one LSC per class)
3. Create Lesson (Class field = formula from LSC)
4. Create Lesson Teacher
5. Create Lesson Assignment (Student Sessions)

**Access:** All SF users who can log into SF can perform CSV import — no role restriction.

### Class Schedule Related List (on Class Record)

- Updated on **both SF and BO** Class detail views.
- Source changed from Lesson Schedule → Lesson Schedule Class.
- Tab label: **Class Schedule**.
- Columns: Lesson Name, Start Date, End Date, Lesson Schedule hyperlink.

### Display Format

| Platform | Surface | Display |
|---|---|---|
| SF | Lesson List, Lesson Detail, Lesson Schedule Detail, Compact Layout | Comma-separated class names (from LSC) |
| SF | Calendar lesson card (Group) | Multiple classes shown |
| BO | Lesson List, Lesson Detail | Comma-separated class names (from LSC) |
| BO | Calendar lesson card (Group) | Multiple classes shown |
| Mobile | Calendar Lesson detail | Classes from LSC |

### Calendar Class Filter

Both SF and BO Calendar class filter use **ALL-match** (AND) logic — see `../calendar/calendar-sf.md` § Multiple Classes on Calendar.
