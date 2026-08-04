# Test Cases: LT-105359 — Auto-Create Location Course When Product Location Is Added

## Suite: Location Course – Auto-Create – Trigger

### [Renseikai] Location Course – Auto-Create – One-Time Product – Product Location Added – Location Course Created

**Description:** AC 01.1 — Decision Table — Adding a Product Location to a One-Time product triggers automatic creation of a Location Course linked to the corresponding Course Master and Location.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Product "AutoLC_Onetime" with Product Type = One-time exists and is linked to Course Master "AutoLC_Onetime"
- Location "Location_H001" exists in the system
- No Location Course exists for Course Master "AutoLC_Onetime" at Location_H001

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Product record "AutoLC_Onetime" | Detail page opens; Product Location related list shows 0 items for Location_H001 | "" |
| 2 | Add "Location_H001" to the **Product Location** related list and save | Product Location record is saved and linked to Location_H001 | "Location = Location_H001" |
| 3 | Navigate to **Master > Location Course** and search for "AutoLC_Onetime" | A Location Course record "AutoLC_Onetime - Location_H001" appears in the list, linked to Course Master = AutoLC_Onetime and Account = Location_H001 | "" |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Location Course – Auto-Create – Slot-Based Product – Product Location Added – Location Course Created

**Description:** AC 01.2 — Decision Table — Adding a Product Location to a Slot-Based product triggers automatic creation of a Location Course linked to the corresponding Course Master and Location.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Product "AutoLC_Slot" with Product Type = Slot-based exists and is linked to Course Master "AutoLC_Slot"
- Location "Location_H001" exists in the system
- No Location Course exists for Course Master "AutoLC_Slot" at Location_H001

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Product record "AutoLC_Slot" | Detail page opens; Product Location related list shows 0 items for Location_H001 | "" |
| 2 | Add "Location_H001" to the **Product Location** related list and save | Product Location record is saved and linked to Location_H001 | "Location = Location_H001" |
| 3 | Navigate to **Master > Location Course** and search for "AutoLC_Slot" | A Location Course record "AutoLC_Slot - Location_H001" appears in the list, linked to Course Master = AutoLC_Slot and Account = Location_H001 | "" |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Location Course – Auto-Create – Scheduled Product – Product Location Added – Location Course Created

**Description:** AC 01.3 — Decision Table — Adding a Product Location to a Scheduled product triggers automatic creation of a Location Course linked to the corresponding Course Master and Location.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Product "AutoLC_Scheduled" with Product Type = Scheduled exists and is linked to Course Master "AutoLC_Scheduled"
- Location "Location_H001" exists in the system
- No Location Course exists for Course Master "AutoLC_Scheduled" at Location_H001

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Product record "AutoLC_Scheduled" | Detail page opens; Product Location related list shows 0 items for Location_H001 | "" |
| 2 | Add "Location_H001" to the **Product Location** related list and save | Product Location record is saved and linked to Location_H001 | "Location = Location_H001" |
| 3 | Navigate to **Master > Location Course** and search for "AutoLC_Scheduled" | A Location Course record "AutoLC_Scheduled - Location_H001" appears in the list, linked to Course Master = AutoLC_Scheduled and Account = Location_H001 | "" |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Location Course – Auto-Create – Frequency Product – Product Location Added – Location Course Created

**Description:** AC 01.4 — Decision Table — Adding a Product Location to a Frequency product triggers automatic creation of a Location Course linked to the corresponding Course Master and Location.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Product "AutoLC_Frequency" with Product Type = Frequency exists and is linked to Course Master "AutoLC_Frequency"
- Location "Location_H001" exists in the system
- No Location Course exists for Course Master "AutoLC_Frequency" at Location_H001

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Product record "AutoLC_Frequency" | Detail page opens; Product Location related list shows 0 items for Location_H001 | "" |
| 2 | Add "Location_H001" to the **Product Location** related list and save | Product Location record is saved and linked to Location_H001 | "Location = Location_H001" |
| 3 | Navigate to **Master > Location Course** and search for "AutoLC_Frequency" | A Location Course record "AutoLC_Frequency - Location_H001" appears in the list, linked to Course Master = AutoLC_Frequency and Account = Location_H001 | "" |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Location Course – Auto-Create – Multiple Locations for Same Product – Two Distinct Location Courses Created

**Description:** AC 01.5 — Scenario — Adding two different Product Locations to the same product creates two distinct Location Courses, one per location.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Product "MultiLoc_TC" with Product Type = One-time exists and is linked to Course Master "MultiLoc_TC"
- Location_H001 and Location_H002 exist in the system
- No Location Course exists for Course Master "MultiLoc_TC"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Product "MultiLoc_TC" and add Location_H001 to the **Product Location** related list | Product Location record for Location_H001 is created; a Location Course "MultiLoc_TC - Location_H001" is auto-created | "Location = Location_H001" |
| 2 | Add Location_H002 to the **Product Location** related list and save | Product Location record for Location_H002 is created; a Location Course "MultiLoc_TC - Location_H002" is auto-created | "Location = Location_H002" |
| 3 | Navigate to **Master > Location Course** and search for "MultiLoc_TC" | Two Location Course records exist: "MultiLoc_TC - Location_H001" and "MultiLoc_TC - Location_H002", each linked to its corresponding location | "" |

**Severity:** major
**Priority:** high

---

## Suite: Location Course – Auto-Create – Record Content

### [Renseikai] Location Course – Auto-Create – Name Format – Course Master Name Hyphen Location Name Applied

**Description:** AC 02.1 — Scenario — The auto-created Location Course name strictly follows the format `<Course Master Name> - <Location Name>`.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Product "NameCheck_TC" with Product Type = Scheduled exists and is linked to Course Master "NameCheck_TC"
- Location "Location_H002" exists in the system
- No Location Course exists for Course Master "NameCheck_TC" at Location_H002

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Product "NameCheck_TC" and add Location_H002 to the **Product Location** related list and save | Product Location record is created | "Course Master = NameCheck_TC; Location = Location_H002" |
| 2 | Navigate to **Master > Location Course** and search for "NameCheck_TC" | A Location Course record "NameCheck_TC - Location_H002" appears in the list | "" |
| 3 | Open the Location Course detail page | Name field shows "NameCheck_TC - Location_H002"; Account = Location_H002; Course Master = NameCheck_TC | "" |

**Severity:** major
**Priority:** high

---

### [Renseikai] Location Course – Auto-Create – Record Linking – Course Master and Account Correctly Referenced

**Description:** AC 02.2 — Component — Auto-created Location Course correctly references the Course Master linked to the product and the Account corresponding to the location.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Product "LinkCheck_TC" with Product Type = Frequency exists and is linked to Course Master "LinkCheck_TC"
- Location "Location_H003" exists in the system with Account = "Location_H003"
- No Location Course exists for Course Master "LinkCheck_TC" at Location_H003

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Product "LinkCheck_TC" and add Location_H003 to the **Product Location** related list and save | Product Location record is created | "Location = Location_H003" |
| 2 | Navigate to **Master > Location Course**, search for and open "LinkCheck_TC - Location_H003" | Detail page opens | "" |
| 3 | Inspect the **Information** section | Course Master = "LinkCheck_TC"; Account = "Location_H003"; Name = "LinkCheck_TC - Location_H003" | "" |

**Severity:** major
**Priority:** high

---

## Suite: Location Course – Auto-Create – Duplicate Prevention

### [Renseikai] Location Course – Auto-Create – Same Product Location Added Again – No Duplicate Location Course Created

**Description:** AC 03.1 — Negative — Attempting to add the same location to a product a second time does not result in a duplicate Location Course being created.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Product "DupLC_TC" with Product Type = One-time exists and is linked to Course Master "DupLC_TC"
- A Product Location for Location_H001 already exists on this Product
- Exactly 1 Location Course "DupLC_TC - Location_H001" already exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Product "DupLC_TC" | Product Location related list shows Location_H001 already added | "" |
| 2 | Attempt to add Location_H001 again to the **Product Location** related list | System shows an error or the duplicate addition is blocked; no second Product Location record is created | "Location = Location_H001 (duplicate)" |
| 3 | Navigate to **Master > Location Course** and search for "DupLC_TC" | Exactly 1 Location Course record "DupLC_TC - Location_H001" exists; no duplicate was created | "" |

**Severity:** major
**Priority:** high

---

### [Renseikai] Location Course – Auto-Create – Location Course Pre-Exists Manually – Product Location Added – No Duplicate Created

**Description:** AC 03.2 — Negative — When a Location Course already exists for a Course Master + Location combination (created manually via Generate Courses), adding a Product Location for the same combination does not create a duplicate.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Product "ManualLC_TC" with Product Type = Slot-based exists and is linked to Course Master "ManualLC_TC"
- A Location Course "ManualLC_TC - Location_H001" already exists (created manually via the Generate Courses button on Course Master)
- No Product Location for Location_H001 exists on this Product yet

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to **Master > Location Course** and search for "ManualLC_TC" | 1 Location Course record "ManualLC_TC - Location_H001" is visible (manually created) | "" |
| 2 | Open Product "ManualLC_TC" and add Location_H001 to the **Product Location** related list and save | Product Location record is created | "Location = Location_H001" |
| 3 | Navigate to **Master > Location Course** and search for "ManualLC_TC" | Still exactly 1 Location Course record "ManualLC_TC - Location_H001"; the auto-create mechanism did not generate a duplicate | "" |

**Severity:** major
**Priority:** high

---
