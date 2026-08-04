# Test Cases: LT-98512 — Riso Classroom Reassignment by Student

## Suite: Scope Isolation and Riso Configuration

### [Riso] Classroom Adjustment – Tenant configuration – Riso setting enabled – Action is available

**Description:** Config — Decision Table — The feature is enabled for the intended tenant.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON for Riso.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson Calendar Daily View. | Classroom Adjustment is available in the action menu. | tenant = Riso; Optimize Classroom Assignment = ON |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Tenant configuration – Riso setting disabled – Action is unavailable

**Description:** Config — Negative — Disabling the Riso setting removes the feature without affecting Daily View.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = OFF for Riso.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson Calendar Daily View and open the action menu. | Classroom Adjustment is not displayed; existing Print Out remains available. | tenant = Riso; Optimize Classroom Assignment = OFF |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Tenant configuration – Non-Riso tenant – Riso action is unavailable

**Description:** Config — Permission Matrix — A tenant without the Riso feature configuration cannot invoke it.

**Preconditions:**
- Logged in as HQ or CM Staff to a non-Riso Salesforce org.
- Optimize Classroom Assignment is not enabled for that tenant.
- Location = Tokyo Main; lesson_date = 2026-07-23.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson Calendar Daily View and open the action menu. | Classroom Adjustment is not displayed. | tenant = Tokyo Main; Optimize Classroom Assignment = OFF |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Processing scope – Selected Location and date – Only eligible lessons change

**Description:** AC-03, AC-06 — Decision Table — The run updates only Individual lessons in the chosen scope.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON.
- Selected Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Seed eligible Individual lessons in Riso Shinjuku on 2026-07-23 and control lessons at another location, another date, and Group teaching.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment for Riso Shinjuku on 2026-07-23. | Only Individual lessons at Riso Shinjuku on 2026-07-23 are candidates for reassignment. | in-scope = Shinjuku, 2026-07-23, Individual |
| 2 | Compare every control lesson with its original classroom. | Other-location, other-date, and Group lessons retain their original classroom. | controls = Ikebukuro 2026-07-23, Shinjuku 2026-07-24, Group lesson |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Processing scope – JST and UTC date boundary – Selected Japanese lesson date is isolated

**Description:** AC-03, AC-06 — Boundary Value Analysis — The selected Lesson Date is not shifted by UTC storage/display conversion.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON; Location = Riso Shinjuku.
- Individual lesson A starts 2026-07-01 00:30 JST (= 2026-06-30 15:30 UTC); control lesson B starts 2026-06-30 23:30 JST (= 2026-06-30 14:30 UTC).

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Daily View for 2026-07-01 and run Classroom Adjustment. | Lesson A is processed as the 2026-07-01 lesson; lesson B is outside the selected date and is unchanged. | lesson_date JST = 2026-07-01; A = 00:30 JST / 15:30 UTC; B = 2026-06-30 23:30 JST / 14:30 UTC |
| 2 | View the resulting classrooms in Daily View. | The displayed result is associated with 2026-07-01 JST, not 2026-06-30 UTC. | display timezone = Asia/Tokyo; storage reference = UTC |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Processing scope – Group lesson – Classroom remains unchanged

**Description:** AC-03 — Negative — Group teaching is excluded from this individual-teaching feature.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON; Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Group lesson G at 10:00 is assigned to Room C; eligible Individual lesson I is also present.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | Lesson I may be processed; Group lesson G is not reassigned. | G = Teaching Method Group, Room C; I = Teaching Method Individual |
| 2 | Compare Group lesson G with its original room. | Group lesson G still has Room C. | expected Group classroom = Room C |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Processing scope – No Individual lessons – No classroom writes occur

**Description:** AC-03, AC-14 — Negative — A scope containing only excluded lessons does not create unintended updates.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON; Location = Riso Shinjuku; lesson_date = 2026-07-25.
- The scope contains Group lessons only, each with a recorded original classroom.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The run completes without updating any lesson. | lesson_date = 2026-07-25; Individual lessons = 0 |
| 2 | Compare all lesson classrooms with their original values. | Every Group lesson retains its original classroom. | expected writes = 0 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Processing scope – Different selected locations – Each run preserves the other location

**Description:** AC-06 — Decision Table — Location filtering is applied independently per run.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON; lesson_date = 2026-07-23.
- Riso Shinjuku and Riso Ikebukuro each contain eligible Individual lessons with different classroom fixtures.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment with Location = Riso Shinjuku. | Only Riso Shinjuku lessons can change. | selected location = Riso Shinjuku |
| 2 | Compare Riso Ikebukuro lesson classrooms with their originals. | All Riso Ikebukuro classrooms are unchanged. | control location = Riso Ikebukuro |

**Severity:** major  
**Priority:** high
