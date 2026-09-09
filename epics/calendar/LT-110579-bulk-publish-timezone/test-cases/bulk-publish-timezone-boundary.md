# Test Cases: LT-110579 - Bulk Publish Lesson timezone boundary

## Suite: Bulk Publish Lesson - Salesforce Timezone Boundary

---

### Bulk Publish Lesson - Single Local Date GMT+9 - All Lessons Within Salesforce Date Are Published

**Description:** AC 01 - Boundary Value Analysis - A single selected Bulk Publish date publishes Draft lessons whose start datetime falls on that Salesforce local date, including lessons stored on the previous UTC date.

**Preconditions:**

- HQ or CM Staff is logged in to the Salesforce org using GMT+9 timezone.
- SF Lesson Calendar is open at location Ngan_Location_001.
- Lesson A is Draft at location Ngan_Location_001 and starts at 2030-09-19 00:00 GMT+9.
- Lesson B is Draft at location Ngan_Location_001 and starts at 2030-09-19 08:59 GMT+9.
- Lesson C is Draft at location Ngan_Location_001 and starts at 2030-09-19 23:59 GMT+9.
- Lesson D is Published at location Ngan_Location_001 and starts at 2030-09-19 10:00 GMT+9.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Bulk Publish Lesson from SF Lesson Calendar. | Bulk Publish modal opens with Start Date, End Date, and Location fields displayed. | sf_timezone = GMT+9; selected_start_date = 2030-09-19; selected_end_date = 2030-09-19; correct_utc_range = [2030-09-18 15:00, 2030-09-19 15:00) |
| 2 | HQ or CM Staff enters Start Date `2030-09-19` and End Date `2030-09-19`. | Date range is accepted by the modal. | start_date = 2030-09-19; end_date = 2030-09-19 |
| 3 | HQ or CM Staff keeps Location as `Ngan_Location_001` and clicks Save. | Success message appears and the user returns to SF Lesson Calendar. | location = Ngan_Location_001 |
| 4 | HQ or CM Staff waits for the async job to finish and clicks Refresh on SF Lesson Calendar. | Calendar reloads lesson statuses from the server. | async_job = completed |
| 5 | HQ or CM Staff observes Lesson A, Lesson B, Lesson C, and Lesson D. | Lesson A, Lesson B, and Lesson C are Published; Lesson D remains Published without duplicate status change. | Lesson A = 2030-09-19 00:00 GMT+9 (= 2030-09-18 15:00 UTC); Lesson B = 2030-09-19 08:59 GMT+9 (= 2030-09-18 23:59 UTC); Lesson C = 2030-09-19 23:59 GMT+9 (= 2030-09-19 14:59 UTC); Lesson D = Published before action |

**Severity:** critical
**Priority:** high

---

### Bulk Publish Lesson - Single Local Date GMT+9 - Lessons On Next Salesforce Date Remain Draft

**Description:** AC 01 - Boundary Value Analysis + Negative Testing - A single selected Bulk Publish date excludes Draft lessons that are on the next Salesforce local date even when their UTC date still matches the selected UTC day.

**Preconditions:**

- HQ or CM Staff is logged in to the Salesforce org using GMT+9 timezone.
- SF Lesson Calendar is open at location Ngan_Location_001.
- Lesson A is Draft at location Ngan_Location_001 and starts at 2030-09-19 23:59 GMT+9.
- Lesson B is Draft at location Ngan_Location_001 and starts at 2030-09-20 00:00 GMT+9.
- Lesson C is Draft at location Ngan_Location_001 and starts at 2030-09-20 07:59 GMT+9.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Bulk Publish Lesson from SF Lesson Calendar. | Bulk Publish modal opens. | sf_timezone = GMT+9; selected_start_date = 2030-09-19; selected_end_date = 2030-09-19; correct_utc_range = [2030-09-18 15:00, 2030-09-19 15:00) |
| 2 | HQ or CM Staff enters Start Date `2030-09-19` and End Date `2030-09-19`. | Date range is accepted by the modal. | start_date = 2030-09-19; end_date = 2030-09-19 |
| 3 | HQ or CM Staff keeps Location as `Ngan_Location_001` and clicks Save. | Success message appears and the user returns to SF Lesson Calendar. | location = Ngan_Location_001 |
| 4 | HQ or CM Staff waits for the async job to finish and clicks Refresh on SF Lesson Calendar. | Calendar reloads lesson statuses from the server. | async_job = completed |
| 5 | HQ or CM Staff observes Lesson A, Lesson B, and Lesson C. | Lesson A is Published; Lesson B and Lesson C remain Draft because they belong to 2030-09-20 in Salesforce timezone. | Lesson A = 2030-09-19 23:59 GMT+9 (= 2030-09-19 14:59 UTC); Lesson B = 2030-09-20 00:00 GMT+9 (= 2030-09-19 15:00 UTC); Lesson C = 2030-09-20 07:59 GMT+9 (= 2030-09-19 22:59 UTC) |

**Severity:** critical
**Priority:** high

---

### Bulk Publish Lesson - Exact GMT+9 Boundaries - Lower Inclusive And Upper Exclusive Rule Applied

**Description:** AC 01 - Boundary Value Analysis - The selected Salesforce local date uses an inclusive lower boundary and exclusive next-day boundary after conversion to UTC.

**Preconditions:**

- HQ or CM Staff is logged in to the Salesforce org using GMT+9 timezone.
- SF Lesson Calendar is open at location Ngan_Location_001.
- Lesson A is Draft at location Ngan_Location_001 and starts at 2030-09-18 23:59 GMT+9.
- Lesson B is Draft at location Ngan_Location_001 and starts at 2030-09-19 00:00 GMT+9.
- Lesson C is Draft at location Ngan_Location_001 and starts at 2030-09-20 00:00 GMT+9.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Bulk Publish Lesson from SF Lesson Calendar. | Bulk Publish modal opens. | sf_timezone = GMT+9; lower_boundary = 2030-09-18 15:00 UTC; upper_boundary = 2030-09-19 15:00 UTC |
| 2 | HQ or CM Staff enters Start Date `2030-09-19` and End Date `2030-09-19`. | Date range is accepted by the modal. | start_date = 2030-09-19; end_date = 2030-09-19 |
| 3 | HQ or CM Staff keeps Location as `Ngan_Location_001` and clicks Save. | Success message appears and the user returns to SF Lesson Calendar. | location = Ngan_Location_001 |
| 4 | HQ or CM Staff waits for the async job to finish and clicks Refresh on SF Lesson Calendar. | Calendar reloads lesson statuses from the server. | async_job = completed |
| 5 | HQ or CM Staff observes Lesson A, Lesson B, and Lesson C. | Lesson B is Published; Lesson A and Lesson C remain Draft. | Lesson A = 2030-09-18 23:59 GMT+9 (= 2030-09-18 14:59 UTC) excluded; Lesson B = 2030-09-19 00:00 GMT+9 (= 2030-09-18 15:00 UTC) included; Lesson C = 2030-09-20 00:00 GMT+9 (= 2030-09-19 15:00 UTC) excluded |

**Severity:** critical
**Priority:** high

---

### Bulk Publish Lesson - Selected Students GMT+9 Range - Student And Timezone Scope Both Applied

**Description:** AC 01 - Decision Table + Boundary Value Analysis - When Apply to selected students is active, Bulk Publish applies selected-student scope and Salesforce timezone date boundaries together.

**Preconditions:**

- HQ or CM Staff is logged in to the Salesforce org using GMT+9 timezone.
- SF Lesson Calendar is open at location Ngan_Location_001.
- Bulk Publish With Student setting is enabled.
- Student A is selected in the SF Lesson Calendar student filter.
- Lesson A is Draft for Student A at location Ngan_Location_001 and starts at 2030-09-19 00:00 GMT+9.
- Lesson B is Draft for Student A at location Ngan_Location_001 and starts at 2030-09-20 00:00 GMT+9.
- Lesson C is Draft for Student B at location Ngan_Location_001 and starts at 2030-09-19 10:00 GMT+9.
- Lesson D is Draft for Student A at location Another_Location_001 and starts at 2030-09-19 10:00 GMT+9.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Bulk Publish Lesson from SF Lesson Calendar. | Bulk Publish modal opens and Apply to selected students checkbox is enabled. | sf_timezone = GMT+9; selected_student = Student A; selected_start_date = 2030-09-19; selected_end_date = 2030-09-19; correct_utc_range = [2030-09-18 15:00, 2030-09-19 15:00) |
| 2 | HQ or CM Staff enters Start Date `2030-09-19` and End Date `2030-09-19`. | Date range is accepted by the modal. | start_date = 2030-09-19; end_date = 2030-09-19 |
| 3 | HQ or CM Staff ticks Apply to selected students. | Checkbox becomes checked and Location is locked to `Ngan_Location_001`. | apply_to_selected_students = true; locked_location = Ngan_Location_001 |
| 4 | HQ or CM Staff clicks Save. | Success message appears and the user returns to SF Lesson Calendar. | location = Ngan_Location_001 |
| 5 | HQ or CM Staff waits for the async job to finish and clicks Refresh on SF Lesson Calendar. | Calendar reloads lesson statuses from the server. | async_job = completed |
| 6 | HQ or CM Staff observes Lesson A, Lesson B, Lesson C, and Lesson D. | Only Lesson A is Published; Lesson B remains Draft because it belongs to 2030-09-20 in Salesforce timezone; Lesson C remains Draft because Student B is not selected; Lesson D remains Draft because it is in another location. | Lesson A = Student A + selected date + selected location; Lesson B = Student A + next local date; Lesson C = unselected student; Lesson D = different location |

**Severity:** critical
**Priority:** high
