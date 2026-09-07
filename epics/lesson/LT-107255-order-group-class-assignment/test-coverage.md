# Test Coverage: LT-107255 — Order Group Class Assignment and Lesson Assignment Reconciliation

## 1. Business rules

| Rule | Acceptance criteria |
|---|---|
| BR-01 | AC-01, AC-02 — Create Order class-member duration follows product start/end; a past product start is normalized to today for the Class Member start date. |
| BR-02 | AC-04 — No selected class creates no Class Member or class-driven Student Session. |
| BR-03 | AC-05 — Duplicate-course class mapping uses course + duration, including same-class rows. |
| BR-04 | AC-03, AC-06 — Add-course flows create a Class Member for class-selected One-Time, Slot-Based, Schedule and Frequency product baselines; Schedule/Frequency use selected effective date and One-Time/Slot-Based use OGC submission date. |
| BR-05 | AC-07, AC-08 — Automatic reconciliation removes automatic sessions only and retains manual sessions for every listed trigger. |

## 4. Coverage strategy

| AC | Technique | Risk | Depth | Coverage intent |
|---|---|---:|---|---|
| AC-01–AC-03 | Decision table + BVA | High | Deep | Separate Create Order and Add New Course date rules, including a past product-start boundary. |
| AC-04 | Equivalence partitioning | High | Standard | Selected class versus no selected class. |
| AC-05 | Pairwise | Critical | Deep | Different-class and same-class duplicate course rows with distinct durations. |
| AC-06 | Decision table | High | Deep | One-Time, Slot-Based, Schedule, Frequency, and no-class add-course variants. |
| AC-07–AC-08 | State transition | Critical | Deep | Manual and automatic session origins across all reconciliation triggers. |

## 5. High-risk areas

- Duplicate-course rows can attach the wrong class to an LA if duration is ignored.
- Create Orders whose product starts in the past can create an invalid Class Member duration if the start is not normalized to today.
- Automatic cleanup can delete a staff-intended manual student assignment.
- Date-only Order Group data must preserve the business date across a JST/UTC calendar boundary.

## 6. Coverage gaps

| Gap | Status | Resolution |
|---|---|---|
| One-Time class-selected new order | New Coverage Needed | Update PX-10451. |
| Slot-Based class-selected new order | New Coverage Needed | Update PX-10454. |
| Frequency add-course baseline | Existing case needs correction | Update PX-18825. |
| Duplicate-course duration mapping | New Coverage Needed | New cases under Create LA – New Order Group. |
| Lesson-assignment origin preservation | New Coverage Needed | New child suite under Class management. |

## 7. Suggested test suite structure

1. **Create LA – New Order Group** (Qase parent 2570): no-class and duplicate-course duration cases; existing One-Time and Slot-Based cases updated.
2. **Add Associated Course** (Qase parent 2572): product-type class-selected and no-class cases; Frequency baseline corrected in existing PX-18825.
3. **Lesson Assignment Update** (Qase parent 1289): reconciliation-origin cases for each trigger.
