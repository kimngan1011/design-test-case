# Test Cases: LT-96234 — Scope & Isolation

## Suite: Scope & Isolation

### Non-Riso Lesson – Create Lesson – Non-Riso org – Lesson Name not auto-generated

**Description:** AC 04.1 — Regression — On a non-Riso org, creating a lesson does not auto-generate Lesson Name; the field remains blank or retains only the manually entered value.

**Preconditions:**
- Logged in as HQ or CM Staff to a **non-Riso** Salesforce org
- Access to the Lesson creation form on the non-Riso org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to Lessons on the non-Riso org and click **New Lesson** | Lesson creation form opens | Org: non-Riso |
| 2 | Select a Subject if Subject field is available on this org | Subject set (or field absent) | "" |
| 3 | Fill required fields and click **Save** | Lesson saved | "" |
| 4 | Open the new lesson's detail page | Lesson detail loads | "" |
| 5 | Observe the **Lesson Name** field | Lesson Name is not auto-generated; it is blank or shows only the manually entered value — the "[Subject] - [Course]" format is not applied | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson – Create Lesson – HQ Staff and CM Staff – Both roles can create lesson with auto-generated name

**Description:** AC 04.2 — Permission Matrix (Smoke) — No new permission required; HQ Staff and CM Staff can both create Riso lessons and receive the auto-generated Lesson Name without restriction.

**Preconditions:**
- Access to the Riso Salesforce org under both HQ Staff role and CM Staff role
- Subject "Biology" exists in Subject Master

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Log in as **HQ Staff** to the Riso SF org | Logged in as HQ Staff; lesson management is accessible | Role: HQ Staff |
| 2 | Navigate to Lessons and click **New Lesson** | Lesson creation form opens without a permission error | "" |
| 3 | Set Teaching Method = Individual, Subject = "Biology", leave Course blank; fill required fields and click **Save** | Lesson saved without access denied or permission error | Subject: "Biology" |
| 4 | Observe the **Lesson Name** field | Lesson Name = "Biology" (auto-generated) | "" |
| 5 | Log out and log in as **CM Staff** to the Riso SF org | Logged in as CM Staff | Role: CM Staff |
| 6 | Navigate to Lessons and click **New Lesson** | Lesson creation form opens without a permission error | "" |
| 7 | Set Teaching Method = Individual, Subject = "Biology", leave Course blank; fill required fields and click **Save** | Lesson saved without access denied or permission error | Subject: "Biology" |
| 8 | Observe the **Lesson Name** field | Lesson Name = "Biology" (auto-generated) | "" |

**Severity:** trivial
**Priority:** low
