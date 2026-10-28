# Test Cases: LT-108370 — Teacher Lesson Access

## Suite: Recovery Performance

### Teacher Lesson Access – One teacher with 100 lessons – Recovery completes with 100 unique lesson permissions

**Description:** AC-07 — Boundary Value Analysis, Regression — A high-volume teacher receives complete, non-duplicated access.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contact N is assigned to exactly 100 lessons named `LT108370-N-001` through `LT108370-N-100`.
- Teacher Contact N has no Salesforce User.
- None of the 100 lessons has a teacher permission for Teacher Contact N.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff creates an active Salesforce User linked to Teacher Contact N. | One recovery flow starts for Teacher Contact N and reaches completed status without a limit error. | Lesson assignment count = 100; User status = Active |
| 2 | HQ or CM Staff counts teacher permissions for Lessons `LT108370-N-001` through `LT108370-N-100`. | Exactly 100 unique Edit permissions exist for Teacher N, one per assigned lesson. | Expected permission count = 100; Duplicate count = 0 |

**Severity:** major
**Priority:** high

---

### Teacher Lesson Access – 100 teachers with 100 lessons each – Recovery workload – Complete unique permissions are created

**Description:** AC-07 — Boundary Value Analysis, Regression — The requested 100 × 100 stress workload produces complete access without duplicate permissions.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contacts `LT108370-P-001` through `LT108370-P-100` are each assigned to exactly 100 lessons.
- The 10,000 teacher-to-lesson assignments exist before the corresponding Salesforce Users are created.
- None of the 10,000 assignments has a teacher permission before recovery starts.
- The test environment has monitoring enabled for failed background recovery requests.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff creates or activates the 100 Salesforce Users linked to Teacher Contacts `LT108370-P-001` through `LT108370-P-100`. | Each eligible teacher has one recovery flow and no flow ends in Failed status. | User count = 100; Lessons per user = 100; Total assignments = 10,000 |
| 2 | HQ or CM Staff waits for all recovery flows to finish and counts the resulting teacher permissions. | Exactly 10,000 unique Edit permissions exist, one for every teacher-to-lesson assignment. | Expected permission count = 10,000; Duplicate count = 0; Failed request count = 0 |
| 3 | HQ or CM Staff samples the first, middle, and last teachers in Back Office. | Each sampled teacher sees the 100 lessons assigned to that teacher and no lesson from another sampled teacher. | Sample users = P-001, P-050, P-100; Expected lessons per sample = 100 |

**Severity:** major
**Priority:** high
