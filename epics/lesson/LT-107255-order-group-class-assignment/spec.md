---
ticket: LT-107255
title: Improvement | Handle order group class assignment for One time & Slot based
scope: Core
status: Ready for QA
---

# LT-107255 — Order Group Class Assignment and Lesson Assignment Reconciliation

## Acceptance criteria

| ID | Area | Requirement |
|---|---|---|
| AC-01 | Create Order — class selected | A new order with a selected class creates the LA and a Class Member whose duration follows the product start and end dates. |
| AC-02 | Create Order — past start date | When the product start date is before the submission date, the Class Member starts today and ends on the product end date. |
| AC-03 | Add associated course — class selected | Adding a course with a selected class creates the LA and Class Member using the add-course date rule for the product type. |
| AC-04 | No class | A submitted order or added course without a selected class creates the LA only; it creates no Class Member and triggers no class-based auto-assignment. |
| AC-05 | Same course, different duration | Multiple rows for the same course in one Order Group create separate LAs. Each LA is linked to the class selected on the row with the same course and duration. This holds whether the selected classes differ or are the same. |
| AC-06 | Add associated course — product types | The class-selected add-course flow creates the LA and Class Member for One-Time, Slot-Based, and Schedule products. Frequency follows the corrected add-course baseline case. |
| AC-07 | Reconciliation scope | Class-based reconciliation removes only sessions created through auto-assignment when they are no longer eligible. Staff-created manual sessions are retained. |
| AC-08 | Reconciliation triggers | The rule in AC-07 applies when creating a class lesson, changing/adding/cancelling a class on an LA, changing class in Lesson Schedule Detail, and importing Class Members. |

## Business rules

1. **Create Order:** every product type follows the selected product start and end dates for the LA and Class Member. When the product start date is in the past, the Class Member start date is today; its end date remains the product end date.
2. **Add New Course — Schedule / Frequency:** staff selects an effective date; the added-course LA and Class Member duration follows it.
3. **Add New Course — One-Time / Slot-Based:** staff does not select an effective date. The Order Group Class (OGC) defaults its effective date to the submission date and the Class Member starts on that OGC date.
4. Class resolution must never use Course alone when duplicate course rows exist; it uses Course + LA duration.
5. No class is a supported input, not an error condition.
6. A manual student assignment is user intent and must survive all automatic class reconciliation tasks.

## Scope and regression surfaces

- Salesforce Order Group and Course tab / Lesson Allocation details.
- Class Member history and dates.
- Group lessons and Student Sessions created by automatic class assignment.
- Lesson Schedule Detail class updates and Class Member import.
- Existing Schedule and Frequency behaviour remains the reference behaviour for class dates.
