# Test Cases: LT-92533 — Riso Compensation Ratio

## Suite: Compensation Ratio — CSV Import

### [Riso] Compensation Ratio – CSV import – Explicit 100% row – 100% persists

**Description:** AC 01.2 — Equivalence Partitioning / CRUD — An explicit allowed value imports unchanged.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A lesson CSV template includes the Compensation Ratio column.
- A CSV row has valid required lesson data.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff sets Compensation Ratio to `100%` in the CSV row. | The CSV row contains the explicit allowed value. | CSV ratio = 100% |
| 2 | HQ or CM Staff imports the CSV and opens the imported lesson. | The imported lesson has Compensation Ratio `100%`. | expected ratio = 100% |

**Severity:** critical
**Priority:** high

---

### [Riso] Compensation Ratio – CSV import – Explicit 60% row – 60% persists

**Description:** AC 01.2 — Equivalence Partitioning / CRUD — The second allowed value imports unchanged.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A lesson CSV template includes the Compensation Ratio column.
- A CSV row has valid required lesson data.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff sets Compensation Ratio to `60%` in the CSV row. | The CSV row contains the explicit allowed value. | CSV ratio = 60% |
| 2 | HQ or CM Staff imports the CSV and opens the imported lesson. | The imported lesson has Compensation Ratio `60%`. | expected ratio = 60% |

**Severity:** critical
**Priority:** high

---

### [Riso] Compensation Ratio – CSV import – Blank row value – 100% default persists

**Description:** AC 01.2 — Equivalence Partitioning / CRUD — A blank CSV field uses the documented default.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A lesson CSV template includes the Compensation Ratio column.
- A CSV row has valid required lesson data.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff leaves Compensation Ratio blank in the CSV row. | The CSV row is ready for import with no Compensation Ratio value. | CSV ratio = blank |
| 2 | HQ or CM Staff imports the CSV and opens the imported lesson. | The imported lesson has Compensation Ratio `100%`. | expected ratio = 100% |

**Severity:** critical
**Priority:** high

---

### [Riso] Compensation Ratio – CSV import – NA row value – Invalid row rejected

**Description:** AC 01.2 — Negative / Equivalence Partitioning — A value not defined by the PRD is rejected.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A lesson CSV template includes the Compensation Ratio column.
- A CSV row has valid required lesson data except Compensation Ratio.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff sets Compensation Ratio to `NA` in the CSV row. | The CSV row contains an invalid Compensation Ratio. | CSV ratio = NA |
| 2 | HQ or CM Staff imports the CSV. | The row is rejected and displays a row-level error identifying Compensation Ratio. | expected row status = rejected |

**Severity:** critical
**Priority:** high

---

### [Riso] Compensation Ratio – CSV import – Mixed valid and invalid rows – Valid rows continue

**Description:** AC 01.2 — Decision Table / Regression — One invalid row does not prevent valid and blank rows from importing.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A lesson CSV template includes the Compensation Ratio column.
- A four-row CSV has distinct valid lesson names.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff prepares four CSV rows with Compensation Ratio values `100%`, `60%`, blank, and `NA`. | The file contains three importable rows and one invalid row. | row 1 = 100%; row 2 = 60%; row 3 = blank; row 4 = NA |
| 2 | HQ or CM Staff imports the CSV. | Rows 1 through 3 import and row 4 is rejected with a row-level Compensation Ratio error. | expected imported rows = 1, 2, 3; rejected row = 4 |
| 3 | HQ or CM Staff opens the three imported lessons. | Their Compensation Ratios are `100%`, `60%`, and `100%` respectively. | expected ratios = 100%, 60%, 100% |

**Severity:** critical
**Priority:** high

---

### [Riso] Compensation Ratio – CSV import – Corrected rejected row – Retry imports corrected value

**Description:** AC 01.2 — Negative / Regression — A rejected row can be corrected and retried with an allowed value.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A CSV row with Compensation Ratio `NA` was rejected with a row-level error.
- The CSV import flow provides the documented correction and retry path.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff corrects the rejected row's Compensation Ratio to `60%`. | The corrected row contains an allowed value. | corrected ratio = 60% |
| 2 | HQ or CM Staff retries the corrected row through the CSV import flow. | The corrected row imports without a Compensation Ratio error. | retry row = corrected row |
| 3 | HQ or CM Staff opens the imported lesson. | The lesson has Compensation Ratio `60%`. | expected ratio = 60% |

**Severity:** critical
**Priority:** high
