# Test Coverage Strategy – [LT-90578] Core | 514 – Koyu Auto Create Application for Event Participants

**Epic:** PBT-1771  
**Component:** Event Management  
**Partner:** Koyu  
**Date:** 2026-03-04  

---

## 1. Extracted Business Rules & Acceptance Criteria

| AC ID   | Description |
|---------|-------------|
| AC-01   | **New Event Setting checkbox** – Event Master page must display a new checkbox "Create Application when booked" inside the "Open to booking system" popup when staff clicks "Open booking system" button. |
| AC-02   | **Localized labels & help text** – Checkbox label and tooltip help text must be displayed in EN and JP per UI language setting. EN: "Create application when booked" / JP: "予約時に所属先申請を作成する". Help text: EN: "Create Enrollment Application for a new student who books via the Booking system" / JP: "予約システムを通じて新規作成された生徒の所属先申請も同時に作成します". |
| AC-03   | **Flag = TRUE → Trigger Application Creation** – When a student books an event and the "Create Application at the Booking" flag is TRUE, the system must trigger the Application Creation API after creating the student contact and assigning to the event. |
| AC-04   | **Flag = FALSE → No Application** – When the flag is FALSE, the system only creates the contact (if new) and assigns to the Activity Event. No Application is created (current behavior preserved). |
| AC-05   | **Application Creation API Data** – The API call must pass: (1) Student ID (Booker), (2) Activity Event ID, (3) Activity Event's Location → mapped to Application Location. |
| AC-06   | **Store Application ID on Event Participant** – Once the Application is successfully created, the returned Application ID must be persisted on the corresponding Event Participant record. |
| AC-07   | **Application ID Visibility** – Users must be able to see the Application ID from the Activity Event UI (either as a column in Event Participant List or in a separate table like Order View). |
| AC-08   | **Store Activity Event ID on Application** – A new field on the Application entity stores the Activity Event ID, enabling bi-directional traceability (Event → Application, Application → Event). |
| AC-09   | **No Recreate Function** – There is explicitly no requirement to recreate the Application from the Event screen. This is a one-way creation only. |
| AC-10   | **Channel-Agnostic Trigger** – Application creation must be triggered regardless of booking channel: Salesforce (internal staff), Manabie App, or External Booking Site. Behavior must be consistent across all channels. |
| AC-11   | **Student (Contact) Creation** – System must check if a Student (Contact) already exists for the booker. If not, create a new Contact before assigning to the event. |
| AC-12   | **Event Participant Record Creation** – System must always create an Event Participant record linking the Student to the Activity Event, regardless of the flag value. |
| AC-13   | **Reuse Existing Application Creation API** – Must reuse the existing Order team's Application Creation API/flow. No separate parallel Application creation logic should be built. |
| AC-14   | **Location Mapping** – Activity Event's Location must be correctly mapped to the Application's Location field. The Application is created at the event's Location. |
| AC-15   | **Error Handling on API Failure** – Behavior when the Application Creation API fails after Student and Event Participant are already created must be defined (graceful degradation, retry, manual fallback). |
| AC-16   | **Idempotency / Duplicate Prevention** – System must handle duplicate bookings and retries without creating duplicate Applications for the same student-event combination. |
| AC-17   | **Initial Admission Status** – The default Admission status for auto-created Applications must be defined and set consistently (open question in spec – needs PM confirmation). |

---

## 2. Business Rules Categorized by Logic Type

### 2.1 Validation Logic
| AC ID | Rule |
|-------|------|
| AC-05 | API payload must contain required fields: Student ID, Activity Event ID, Location. Missing fields should be rejected. |
| AC-11 | Student (Contact) existence check before assignment – validate booker identity. |
| AC-14 | Location mapping validation – Activity Event must have a valid Location before Application can be created. |

### 2.2 Boundary / Range Logic
| AC ID | Rule |
|-------|------|
| AC-16 | One Application per student-event combination – boundary of exactly 1 Application per Event Participant. |
| AC-06 | One-to-one mapping between Event Participant and Application ID – no many-to-one or one-to-many. |

### 2.3 Conditional Logic
| AC ID | Rule |
|-------|------|
| AC-03 | IF flag = TRUE → trigger Application Creation API. |
| AC-04 | IF flag = FALSE → skip Application creation, keep current behavior. |
| AC-10 | Application creation is triggered regardless of booking channel (SF / Manabie App / External). Flag is the sole conditional gate. |
| AC-11 | IF student exists → reuse existing Contact; IF not → create new Contact. |

### 2.4 State Transition
| AC ID | Rule |
|-------|------|
| AC-17 | Application created with an initial Admission status → transitions through Admission workflow downstream. |
| AC-03 → AC-06 | Booking flow state: Event Created → Booking Received → Student Created/Found → Event Participant Created → Application Created → Application ID Stored. |

### 2.5 Permission Logic
| AC ID | Rule |
|-------|------|
| AC-01 | Only staff with access to Event Master and "Open to booking system" action can configure the checkbox. |
| AC-07 | Visibility of Application ID on Event UI may require Admission module permissions if clickable navigation is implemented. |

### 2.6 Data Integrity
| AC ID | Rule |
|-------|------|
| AC-06 | Application ID must be correctly stored on Event Participant record after successful creation. |
| AC-08 | Activity Event ID must be stored on the Application record (bi-directional reference). |
| AC-16 | No duplicate Applications for the same student-event booking. Idempotency must be guaranteed. |
| AC-12 | Event Participant record must always be created, regardless of flag or Application creation outcome. |

### 2.7 Cross-System Impact
| AC ID | Rule |
|-------|------|
| AC-13 | Reuses Order team's Application Creation API – changes here can impact Order/Admission modules. |
| AC-05 | Data flows from Booking system → Event Management → Application Creation API (Order team). |
| AC-08 | New field on Application entity affects Order/Admission data model. |
| AC-10 | Multiple booking channels (SF, Manabie App, External Site) must all trigger the same centralized logic. |
| AC-15 | API failure in Application creation must not corrupt Event Participant or Student data already persisted. |

### 2.8 Recurrence Logic
| AC ID | Rule |
|-------|------|
| — | Not applicable for this feature. Events are individual Activity Events, not recurring. |

---

## 3. Test Technique Mapping by Logic Type

| Logic Type | Applicable Test Techniques | Rationale |
|---|---|---|
| **Validation Logic** | Equivalence Partitioning, Boundary Value Analysis, Negative Testing | Validate required fields, valid/invalid payloads, missing data scenarios. |
| **Boundary / Range Logic** | Boundary Value Analysis, Negative Testing | Test exactly 1 Application per participant, edge cases of 0 and duplicates. |
| **Conditional Logic** | Decision Table, Equivalence Partitioning, Pairwise Testing | Flag ON/OFF × Channel × Student exists/new = combinatorial conditions. |
| **State Transition** | State Transition Testing, Regression Analysis | Booking flow has sequential states with possible failure at each step; verify full pipeline and partial failures. |
| **Permission Logic** | Permission Matrix, Negative Testing | Verify who can toggle the setting, who can view Application ID, unauthorized access attempts. |
| **Data Integrity** | CRUD Testing, Regression Analysis, Negative Testing | Verify create/read of Application ID on Event Participant, Activity Event ID on Application, no orphan records. |
| **Cross-System Impact** | Regression Analysis, Performance Testing, Negative Testing | API integration with Order team, multi-channel consistency, failure isolation between systems. |

---

## 4. Structured Coverage Strategy

| AC ID | Logic Type | Test Technique(s) | Risk Level | Coverage Depth Required |
|-------|------------|-------------------|------------|------------------------|
| AC-01 | Validation Logic, Permission Logic | Equivalence Partitioning, Permission Matrix, Negative Testing | Medium | Standard – verify checkbox presence, toggle behavior, permission to access |
| AC-02 | Validation Logic | Equivalence Partitioning | Low | Basic – verify EN/JP labels and help text render correctly per locale |
| AC-03 | Conditional Logic, State Transition | Decision Table, State Transition Testing, Regression Analysis | **High** | Deep – this is the core trigger; test flag=TRUE across all channels, with new and existing students, verify full state flow |
| AC-04 | Conditional Logic | Decision Table, Negative Testing | **High** | Deep – verify NO Application is created when flag=FALSE; ensure current behavior is fully preserved (regression) |
| AC-05 | Validation Logic, Cross-System Impact | Equivalence Partitioning, Boundary Value Analysis, Negative Testing | **High** | Deep – validate all required API fields, test with missing/invalid data, verify Location mapping accuracy |
| AC-06 | Data Integrity, Boundary / Range Logic | CRUD Testing, Boundary Value Analysis, Negative Testing | **High** | Deep – verify 1:1 mapping, Application ID correctly stored, no null/stale values, verify after failures |
| AC-07 | Data Integrity, Permission Logic | CRUD Testing, Permission Matrix | Medium | Standard – verify Application ID is displayed, correct value, expected UI placement, permission checks if clickable |
| AC-08 | Data Integrity, Cross-System Impact | CRUD Testing, Regression Analysis | **High** | Deep – new field on Application entity; verify bi-directional traceability, no impact on existing Order flows |
| AC-09 | Conditional Logic | Negative Testing | Low | Basic – confirm no recreate button/function exists on Event screen |
| AC-10 | Conditional Logic, Cross-System Impact | Decision Table, Pairwise Testing, Regression Analysis | **High** | Deep – test all 3 channels × flag ON/OFF × new/existing student; verify consistent behavior across channels |
| AC-11 | Conditional Logic, Validation Logic | Decision Table, Equivalence Partitioning, Negative Testing | Medium | Standard – test existing student reuse, new student creation, invalid booker data |
| AC-12 | Data Integrity | CRUD Testing, Regression Analysis | Medium | Standard – verify Event Participant is always created regardless of flag or Application outcome |
| AC-13 | Cross-System Impact | Regression Analysis, Performance Testing | **High** | Deep – API integration testing with Order team's flow; verify no side-effects on existing Order/Admission functionality |
| AC-14 | Validation Logic, Data Integrity | Equivalence Partitioning, Negative Testing | **High** | Deep – verify correct Location mapping; test events with no Location, invalid Location, mismatched Location |
| AC-15 | Cross-System Impact, State Transition | State Transition Testing, Negative Testing, Regression Analysis | **Critical** | Exhaustive – test API failure at each step; verify Student and Event Participant remain intact; verify no partial/corrupt Application records |
| AC-16 | Data Integrity, Boundary / Range Logic | Boundary Value Analysis, Negative Testing, Performance Testing | **Critical** | Exhaustive – test concurrent bookings, retries, duplicate submissions; verify exactly 1 Application per student-event |
| AC-17 | State Transition | State Transition Testing, Equivalence Partitioning | Medium | Standard – verify initial Admission status is correct; verify downstream workflow compatibility |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 5.1 CRITICAL RISK

| Area | AC IDs | Why High Risk | Recommended Depth |
|------|--------|---------------|-------------------|
| **API Failure & Error Handling** | AC-15 | Application Creation API failure after Student and Event Participant are already created can lead to orphan records, inconsistent state, and user confusion. No recreate function exists (AC-09), so recovery is manual. | Exhaustive: test timeout, 4xx, 5xx, network failure, partial response. Verify rollback/compensation logic. Test at each step of the flow. |
| **Idempotency & Duplicate Prevention** | AC-16 | Concurrent bookings, retries, and race conditions could create duplicate Applications. Data integrity is critical for Admission/Order downstream processes. | Exhaustive: concurrent requests, rapid retries, same student booking same event via different channels simultaneously. Load testing. |

### 5.2 HIGH RISK

| Area | AC IDs | Why High Risk | Recommended Depth |
|------|--------|---------------|-------------------|
| **Core Conditional Trigger (Flag ON/OFF)** | AC-03, AC-04 | This is the primary business logic gate. A bug here means either missing Applications (lost enrollments) or unwanted Applications (data noise). Regression risk is high since it alters existing booking behavior. | Deep: Decision table covering all flag × channel × student-existence combinations. Regression suite for existing flag=OFF behavior. |
| **Cross-System API Integration** | AC-05, AC-13 | Reusing Order team's API introduces coupling. Changes on either side can break the integration. API contract (field names, required params, response format) must be validated. | Deep: Contract testing, schema validation, version compatibility. Test with real and mocked API responses. |
| **Channel-Agnostic Consistency** | AC-10 | Three different booking channels must produce identical outcomes. Any channel-specific bug creates inconsistent data and business process failures. | Deep: Pairwise matrix across channels. End-to-end tests per channel. |
| **Bi-Directional Data Linkage** | AC-06, AC-08 | Application ID on Event Participant AND Activity Event ID on Application must both be set correctly. Broken references cause traceability failures and impact reporting. | Deep: Verify both directions after creation. Test with invalid/null references. Verify under failure conditions. |
| **Location Mapping Accuracy** | AC-14 | Incorrect Location mapping means Applications are created at the wrong Location, which breaks downstream Admission/Order processes and business reporting. | Deep: Test with valid, missing, and invalid Locations. Test events with Location changes after flag is set. |

### 5.3 MEDIUM RISK

| Area | AC IDs | Why Medium Risk | Recommended Depth |
|------|--------|-----------------|-------------------|
| **Event Participant Always Created** | AC-12 | Must guarantee Event Participant record exists regardless of Application outcome. Failure here breaks event management visibility. | Standard: verify participant exists when flag=ON (success and failure), flag=OFF. |
| **Application ID Visibility** | AC-07 | UI display issue; lower business impact but affects staff workflow and traceability. | Standard: verify correct display, correct value, UI placement. |
| **Student Contact Handling** | AC-11 | Existing vs. new student logic is well-established but needs validation in the new flow context. | Standard: test new student creation, existing student reuse, edge cases (duplicate contacts). |
| **Initial Admission Status** | AC-17 | Open question in spec. Once defined, verify it integrates with downstream Admission workflow. | Standard: verify status value, transition compatibility. |
| **Permission Controls** | AC-01 | Staff access to Event Master and checkbox control. Low complexity but important for security. | Standard: verify authorized and unauthorized access to settings. |

---

## 6. Decision Table – Core Conditional Logic (AC-03, AC-04, AC-10, AC-11)

This is the most critical combinatorial area and warrants a dedicated decision table:

| # | Flag | Channel | Student Exists | Expected: Contact Created | Expected: Event Participant | Expected: Application Created | Expected: App ID Stored |
|---|------|---------|---------------|--------------------------|----------------------------|------------------------------|------------------------|
| 1 | ON   | External Site | No  | Yes | Yes | Yes | Yes |
| 2 | ON   | External Site | Yes | No (reuse) | Yes | Yes | Yes |
| 3 | ON   | Salesforce    | No  | Yes | Yes | Yes | Yes |
| 4 | ON   | Salesforce    | Yes | No (reuse) | Yes | Yes | Yes |
| 5 | ON   | Manabie App   | No  | Yes | Yes | Yes | Yes |
| 6 | ON   | Manabie App   | Yes | No (reuse) | Yes | Yes | Yes |
| 7 | OFF  | External Site | No  | Yes | Yes | No  | N/A |
| 8 | OFF  | External Site | Yes | No (reuse) | Yes | No  | N/A |
| 9 | OFF  | Salesforce    | No  | Yes | Yes | No  | N/A |
| 10| OFF  | Salesforce    | Yes | No (reuse) | Yes | No  | N/A |
| 11| OFF  | Manabie App   | No  | Yes | Yes | No  | N/A |
| 12| OFF  | Manabie App   | Yes | No (reuse) | Yes | No  | N/A |

> **Note:** All 12 combinations should be explicitly tested. Rows 1–6 (flag=ON) are the primary new behavior. Rows 7–12 (flag=OFF) are regression verification.

---

## 7. State Transition – Booking-to-Application Flow (AC-03 → AC-06)

```
[Event Created] 
    → [Booking Received] 
        → [Student Checked]
            → (exists?) → [Existing Contact Found]
            → (not exists?) → [New Contact Created]
        → [Event Participant Created]
            → (flag = TRUE?) → [Application Creation API Called]
                → (success?) → [Application Created] → [App ID Stored on Participant]
                → (failure?) → [Error State – Participant exists, no App] ⚠️
            → (flag = FALSE?) → [Done – No Application]
```

**Key test points at each transition:**
- Verify forward transitions complete correctly
- Verify failure at each node does not corrupt prior state
- Verify terminal states are correct and observable in UI

---

## 8. Summary

| Metric | Count |
|--------|-------|
| Total Acceptance Criteria | 17 |
| Critical Risk ACs | 2 (AC-15, AC-16) |
| High Risk ACs | 6 (AC-03, AC-04, AC-05, AC-08, AC-10, AC-13, AC-14) |
| Medium Risk ACs | 6 (AC-01, AC-07, AC-11, AC-12, AC-17) |
| Low Risk ACs | 2 (AC-02, AC-09) |
| Decision Table Combinations | 12 |
| Logic Types Covered | 7 of 8 (Recurrence Logic not applicable) |
| Test Techniques Applied | 9 of 10 (all except Pairwise used standalone – it is combined with Decision Table) |

**Next step:** Generate detailed test cases based on this coverage strategy.
