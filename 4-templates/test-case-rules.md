# Test Case Design Rules

This document defines the standard rules for designing test cases.

Copilot must follow these rules when generating test cases.

---

# 1 Test Case Principles

## One Test Case = One Primary Logic

Each test case must validate only one of the following:

- business rule
- system behavior
- validation logic

Avoid combining multiple logics in one test case.

---

# 2 Avoid Vague Titles

Do NOT use verbs such as:

- Verify
- Check
- Test
- Properly
- Correctly
- Successfully

Bad example

Page A – Verify display correctly

Good example

Feature X – Page A – All components rendered

---

# 3 Avoid UI-only Test Cases

Test cases should represent:

- user scenario
- system behavior
- business rule

Avoid creating separate test cases for each UI element.

Bad example

Verify header title displayed  
Verify header description displayed  
Verify field A displayed

Good example

Registration Form – All fields and labels displayed as design

---

# 4 Avoid Over-Combination

Do not combine different logic in one test case.

Bad example

Verify assignment access

Good example

Student can view assignment details  
Teacher can edit assignment details  
Parent can view assignment status

---

# 5 Core vs OOP Test Case Naming

Core test cases

Do NOT prefix title with [Core]

Example

Lesson Schedule – Create Lesson – Successfully created

OOP test cases

MUST prefix with client name

Example

[Renseikai] Lesson Schedule – Create Lesson – Successfully created

---

# 6 Title Convention

Standard format

[Feature] – [Sub-feature] – [Component] – Condition – Expected Behavior

Example

Dynamic Form – Header Title – 60 characters – Displayed as design

Dynamic Form – Header Title – Exceeds 60 characters – Validation message shown

---

# 7 Test Case Focus

Test cases must focus on:

- user behavior
- business logic
- system response

Avoid:

- UI-only validation
- overly granular cases
- unclear titles
