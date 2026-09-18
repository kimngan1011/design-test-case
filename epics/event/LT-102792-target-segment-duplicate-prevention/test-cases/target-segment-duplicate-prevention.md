# Test Cases: LT-102792 - Target Segment duplicate prevention

## Suite: Target Segment - Lookup Constraints & Eligibility Engine

### [Core] Target Segment - Duplicate Target Location - Existing location disabled or hidden

**Description:** AC 01.1 - Negative - Existing Target Location value cannot be selected again for the same Event Master.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Event Master `EM-102792-01` exists.
- `EM-102792-01` already has Target Location `Tokyo Center`.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Event Master `EM-102792-01`. | Event Master detail page opens. | event_master = EM-102792-01 |
| 2 | Open Target Segments and click New Target Location. | Target Location creation UI opens. | segment = Target Location |
| 3 | Open/search the Target Location selector for `Tokyo Center`. | `Tokyo Center` is disabled or hidden from selectable results. | existing_location = Tokyo Center |
| 4 | Select a different center location and save. | The different Target Location is saved successfully. | new_location = Osaka Center |

### [Core] Target Segment - Duplicate Target Location - Save validation rejects stale duplicate payload

**Description:** AC 02.1 - API/CRUD Negative - Duplicate Target Location values are rejected even if a stale UI or API payload sends the duplicate.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Event Master `EM-102792-02` exists.
- `EM-102792-02` already has Target Location `Tokyo Center` with Enrollment Status `Enrolled`.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Attempt to save another Target Location row for `Tokyo Center` on `EM-102792-02` from stale UI/API. | Save is rejected with a validation/error state. | duplicate_location = Tokyo Center |
| 2 | Query Target Location records under `EM-102792-02`. | Only one active Target Location row exists for `Tokyo Center`. | expected_duplicate_count = 0 |
| 3 | Open Booking System eligibility setup for the event. | Existing Target Location filtering remains usable; no broken target segment state appears. | expected_state = valid_existing_segment |

### [Core] Target Segment - Duplicate Target Grade - Option hidden or disabled and save blocked

**Description:** AC 01.2 / AC 02.2 - Negative - Existing Target Grade value cannot be selected or persisted again.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Event Master `EM-102792-03` exists.
- `EM-102792-03` already has Target Grade `Grade 7`.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Event Master `EM-102792-03`. | Event Master detail page opens. | event_master = EM-102792-03 |
| 2 | Click New Target Grade and open/search the grade selector. | `Grade 7` is disabled or hidden from selectable results. | existing_grade = Grade 7 |
| 3 | Attempt to save duplicate Target Grade `Grade 7` from stale UI/API. | Save is rejected with a validation/error state. | duplicate_grade = Grade 7 |
| 4 | Query Target Grade records under the Event Master. | Only one active `Grade 7` Target Grade row exists. | expected_count = 1 |

### [Core] Target Segment - Duplicate Target School - Option hidden or disabled and save blocked

**Description:** AC 01.3 / AC 02.3 - Negative - Existing Target School value cannot be selected or persisted again.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Event Master `EM-102792-04` exists.
- `EM-102792-04` already has Target School `Sakura High School`.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Event Master `EM-102792-04`. | Event Master detail page opens. | event_master = EM-102792-04 |
| 2 | Click New Target School and open/search the school selector. | `Sakura High School` is disabled or hidden from selectable results. | existing_school = Sakura High School |
| 3 | Attempt to save duplicate Target School `Sakura High School` from stale UI/API. | Save is rejected with a validation/error state. | duplicate_school = Sakura High School |
| 4 | Query Target School records under the Event Master. | Only one active `Sakura High School` Target School row exists. | expected_count = 1 |

### [Core] Target Segment - Duplicate Target Course - Option hidden or disabled and save blocked

**Description:** AC 01.4 / AC 02.4 - Negative - Existing Target Course value cannot be selected or persisted again.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Event Master `EM-102792-05` exists.
- `EM-102792-05` already has Target Course `Math Advanced`.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Event Master `EM-102792-05`. | Event Master detail page opens. | event_master = EM-102792-05 |
| 2 | Click New Target Course and open/search the course selector. | `Math Advanced` is disabled or hidden from selectable results. | existing_course = Math Advanced |
| 3 | Attempt to save duplicate Target Course `Math Advanced` from stale UI/API. | Save is rejected with a validation/error state. | duplicate_course = Math Advanced |
| 4 | Query Target Course records under the Event Master. | Only one active `Math Advanced` Target Course row exists. | expected_count = 1 |

### [Core] Target Segment - Mixed unique values - Valid setup and filtering remain unchanged

**Description:** AC 03.1 / AC 03.2 / AC 03.3 - Regression - Duplicate prevention does not block valid unique values and does not change Target Segment filtering behavior.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Event Master `EM-102792-06` is open to Booking System and has an Activity Event.
- Student A matches Target Location `Tokyo Center`, Grade `Grade 7`, School `Sakura High School`, and Course `Math Advanced`.
- Student B does not match the configured Target Segments and is not in Master Participant list.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Add unique Target Location `Tokyo Center` with Enrollment Status `Enrolled`. | Target Location is saved. | location = Tokyo Center; status = Enrolled |
| 2 | Add unique Target Grade `Grade 7`, Target School `Sakura High School`, and Target Course `Math Advanced`. | All unique Target Segment records are saved. | grade = Grade 7; school = Sakura High School; course = Math Advanced |
| 3 | Open Booking System as Student A. | Event Master is visible because Student A matches the configured Target Segments. | student = Student A |
| 4 | Open Booking System as Student B. | Event Master is hidden because Student B does not match and is not in Master Participant list. | student = Student B |
| 5 | Reopen Target Segment add UI for each dimension. | Already-saved values are not selectable again; other valid values remain selectable. | expected = duplicate hidden/disabled |
