# Test Cases: LT-102371 — [Riso] OOP | Lesson Window

## Suite: [Riso] LLW – GET API

---

### [Riso] Location Lesson Window – GET API – Response – All Required Fields Returned for Each Record

**Description:** AC-14, AC-15 — Component — The GET API endpoint returns all eight required fields for each Location Lesson Window record.

**Preconditions:**
- API credentials for Riso's external system are available
- At least two LLW records exist in the Riso org:
  - Record 1: Location A, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31, Status = Complete
  - Record 2: Location B, AY = 2026, Start Date = 2026-08-01, End Date = 2026-08-31, Status = Open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send a GET request to the LLW API endpoint with valid authentication | Request is sent | endpoint = TBC with tech; auth = standard Riso-Manabie auth |
| 2 | Receive the API response | HTTP 200 response is returned | — |
| 3 | Inspect each record in the response for Record 1 (Location A, July) | Response contains: **Partner Internal ID** = Location A's configured partner identifier (not Salesforce Location ID), **Location Name** = "Location A", **Academic Year** = 2026, **Start Date** = 2026-07-01, **End Date** = 2026-07-31, **Status** = "Complete", **Last Modified Date** = a valid datetime, **Last Modified By External User ID** = the modifying Contact's external user ID | expected_fields = [Partner Internal ID, Location Name, Academic Year, Start Date, End Date, Status, Last Modified Date, Last Modified By External User ID] |
| 4 | Inspect each record in the response for Record 2 (Location B, August) | All eight fields present and correct for Record 2 | — |
| 5 | Confirm no extra undocumented fields are required to parse the response | Response schema matches AC-15 specification | — |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – GET API – Response – Status Field Reflects Current LLW Status Correctly

**Description:** AC-15 — CRUD — The Status field in the GET API response accurately reflects the current status of each LLW record (Open or Complete).

**Preconditions:**
- Two LLW records: one with Status = **Open**, one with Status = **Complete**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send a GET request to the LLW API endpoint | Response received | — |
| 2 | Check the `Status` field for the Open LLW record | Status field = **"Open"** (or the equivalent API value) | expected_open_status = "Open" |
| 3 | Check the `Status` field for the Complete LLW record | Status field = **"Complete"** (or the equivalent API value) | expected_complete_status = "Complete" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – GET API – Response Updated After Status Change – Last Modified Date Reflects Change

**Description:** AC-15, System / Data / Integration — CRUD — After an LLW record's status is changed from Open to Complete, the next GET API call returns the updated Last Modified Date.

**Preconditions:**
- LLW record: Location A, July 2026, Status = **Open**
- Note the current Last Modified Date via API before the status change

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Call the GET API and note the **Last Modified Date** for the Location A July LLW | Last Modified Date = T₁ | T1 = initial_last_modified |
| 2 | Navigate to the Riso SF org and mark the LLW as **Complete** | Status changes to Complete | — |
| 3 | Call the GET API again for the same record | Response received | — |
| 4 | Observe the **Last Modified Date** and **Status** in the response | Status = "Complete"; Last Modified Date = T₂ where T₂ > T₁ | T2 > T1 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – GET API – NFR-04 – Nightly Batch Call – Response Time Acceptable

**Description:** AC-19, NFR-04 — Cross-system — The GET API responds within acceptable latency for a nightly batch call scenario.

**Preconditions:**
- At least 50 LLW records exist across multiple locations in the Riso org (realistic nightly batch volume)
- API credentials available

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send a GET request to the LLW API endpoint during off-peak hours | Request initiated | volume = 50+ records; call_time = off-peak (simulating nightly batch) |
| 2 | Measure the response time | Response is received within an acceptable time (confirm SLA with Riso if defined; no timeout error) | — |
| 3 | Confirm all records are returned without pagination errors | Full result set returned correctly | — |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – GET API – Authentication – Unauthenticated Request Rejected

**Description:** AC-18 — Negative — A GET API call without valid authentication credentials returns an authentication error (HTTP 401 or equivalent).

**Preconditions:**
- No authentication token or an invalid token is provided for the request

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send a GET request to the LLW API endpoint with **no authentication** header | Request sent without credentials | auth = none |
| 2 | Observe the HTTP response code | Response is **HTTP 401 Unauthorized** (or equivalent authentication error) | expected_status = 401 |
| 3 | Confirm no LLW data is returned in the response body | Response body contains an error message, not LLW records | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – GET API – Integration – Riso External System Nightly Call Returns All Active LLW Records

**Description:** AC-14, AC-19 — Cross-system — The GET API call from Riso's external system during nightly batch retrieves all LLW records (both Open and Complete statuses) for all Riso locations.

**Preconditions:**
- LLW records exist: Location A (Complete, July), Location B (Open, August), Location C (Complete, June)
- Riso external system API integration is configured

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Simulate a nightly GET API call from Riso's external system | Request sent | — |
| 2 | Count the records returned in the response | All 3 LLW records are returned (Location A, B, C) | expected_count = 3 |
| 3 | Confirm records include both Open and Complete status records | All statuses included in the response | — |
| 4 | Confirm the response completes without error | HTTP 200, no rate limit error, no timeout | — |

**Severity:** minor
**Priority:** medium
