# [KOYU] Core | 514 – Auto Create Application for Event Participants

Jira Epic: PBT-1771  
Project: Product Backlog and Tasks (PBT)  
Type of System: ERP  
Component: Event Management  
Partner: Koyu  
Request Source: Req. List – No. 514  
Priority: Must-have  
Project Type: Core feature  
Delivery Type: Target  

- Jira epic: https://manabie.atlassian.net/browse/PBT-1771  
- Requirement spec: https://manabie.atlassian.net/wiki/spaces/PrTi/pages/1814003739/No.514_Manage+group+experiences+lesson+as+events  
- Koyu business requirements: https://manabie.atlassian.net/wiki/spaces/PRDM/pages/1927249935/Koyu+Requirements+-+July+2026  
- Attached design image (if any):  
  - https://api.media.atlassian.com/file/8f28d754-b021-4703-ae1e-94120965f10d/binary?token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJkM2FmZWViMi1jZjdkLTQxMjYtYjEyYi00Y2YzYzczN2ExM2EiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpmaWxlOjhmMjhkNzU0LWIwMjEtNDcwMy1hZTFlLTk0MTIwOTY1ZjEwZCI6WyJyZWFkIl19LCJleHAiOjE3NzI2MTk2NjksIm5iZiI6MTc3MjYxOTA2OX0.Uno_zPBZQjF1Hh4Xl3_W3rkRDa29r3UelRxADWqn2eQ&client=d3afeeb2-cf7d-4126-b12b-4cf3c737a13a&dl=true&name=image-20251125-040910.png  

---

## 1. Meta Information

- **Issue Key:** PBT-1771  
- **Summary:** [koyu] Core | 514 - Auto Create Application for Event Participants  
- **Issue Type:** Epic  
- **Status:** In Development  
- **Created:** 2025-10-02T00:53:18.751Z  
- **Updated:** 2026-02-17T09:31:41.412Z  

### 1.1. Ownership

- **Product Manager:** Maria Nawatani  
- **Tech Lead:** The Khuong Dang  
- **PRD Approver:** Itaru Kato  
- **Reporter:** Noritake Takamichi  
- **Assignee:** Maria Nawatani  
- **Commercial Stakeholder(s):** satoru.katsumata  

### 1.2. Timeline & Planning

- **Discovery Completion Date:** 2025-11-30  
- **Detailing Start Date:** 2025-11-25  
- **External UAT Date (committed):** 2026-04-01  
- **Target External UAT Date:** 2026-03-23  
- **Committed Production Release Date:** 2026-07-01  
- **Next Relevant Date:** 2026-04-01  

### 1.3. Estimation

- **Rough Estimation – Max Dev Effort:** 5.0 man-days  
- **Rough Estimation – Min Dev Effort:** (not specified)  
- **Rough Estimation – QA Effort:** (not specified)  

### 1.4. Classification

- **Project Type:** Core feature  
- **Delivery Type:** Target  
- **Type of System:** ERP  
- **Partner Name:** Koyu  
- **Component:** Event Management  
- **Partner Priority:** High  
- **Priority:** Must-have  
- **Request Source:** Req. List, No. 514  

### 1.5. Do or Not Do (Decision)

- **Do or Not Do: Remarks:**  
  > [included in the roadmap]  
  > 要件整理  
  > * 特定のイベントの登録があった際に、入会の申請を自動で立てる  
  >   * → coreで開発で良さそう  

  Translation (informal):  
  - When there is registration for a specific event, automatically create an enrollment application.  
  - It implement this in core.

---

## 2. Partner Remarks (Business Context)

> For a group trial, register the trial lesson as an event and issue an external reservation link. You can register the application from the event side.  
> 一斉体験の場合は、体験授業をイベントとして登録し、外部予約リンクを発行する。イベント側からAplicaitionを登録できる。

Interpretation:

- For group trial lessons, Koyu will:
  - Register the trial lesson as an **Event** in ERP.
  - Issue an **external booking link** for that event.
  - From the **event side**, staff should be able to register the **Enrollment Application** (now to be automated).

---

## 3. Background

From the epic description:

- **Partner:** Koyu  
- **Usage:** Koyu will use **Booking system** to manage **Trial Group lessons** for external students.
- **Business goal:** Automate booking workflow:
  - From opening available events,
  - To managing submitted bookings,
  - To creating **Order at the event’s Location** for the booker.

Reference documents:

- Detailed flows & specification:  
  - Manage group experiences lesson as events:  
    https://manabie.atlassian.net/wiki/spaces/PrTi/pages/1814003739/No.514_Manage+group+experiences+lesson+as+events  
  - Koyu Requirements – July 2026:  
    https://manabie.atlassian.net/wiki/spaces/PRDM/pages/1927249935/Koyu+Requirements+-+July+2026  

Context:

- Koyu runs group trial lessons.
- External students (or parents) book trial lessons via a Booking system.
- When the booking is done:
  - Currently: a **Contact (Student)** is created and assigned to the **Activity Event**.
  - Desired: conditionally auto-create an **Enrollment Application** and link it to the event participation and to the appropriate Location, reusing Order team’s existing Application creation flow.

---

## 4. Core Requirements

The epic defines three main functional requirements plus additional clarifications from comments.

### 4.1. Requirement 1 – New Event Setting: “Create Application at the Booking”

> 1. Add new settings to Event Master page: “Create Application at the Booking”  
>     1. Set when open events to booking system (user click "open booking system" button -> show popup 'Open to booking system' -> exist checkbox "Create Application when booked" with helptext tooltip)

**Description:**

- On **Event Master** page in ERP, introduce a **new setting**:
  - A checkbox: `Create Application at the Booking`.
- This setting is defined when opening events to the Booking system.
- The flag controls whether an **Enrollment Application** is created automatically when a student books that event.

**Label and Help Text:**

The epic explicitly defines UI text in both English and Japanese:

| EN               | JP                               |
|------------------|----------------------------------|
| Checkbox label   | Create application when booked   | 予約時に所属先申請を作成する |
| Help text        | Create Enrollment Application for a new student who books via the Booking system | 予約システムを通じて新規作成された生徒の所属先申請も同時に作成します |

**Implications:**

- The Event configuration screen must:
  - Show this checkbox.
  - Show localized label and help text per UI language.
- The default state (true/false) is not explicitly given here; needs to be defined in design or implementation notes.
- The flag can be toggled by staff after event creation; behavior for existing bookings vs new bookings is an implementation detail but logically only affects future bookings.

---

### 4.2. Requirement 2 – Trigger Application Creation on Booking

> 2. Trigger create application event after creating student and assign him/her to the activity event, if the Create application flag is True  
>     1. If flag is False, same as the current, just create a contact and assign to the activity event.

**Behavior Overview:**

- When an **external student** applies to an **Activity Event** via the Booking system:

  1. A new **Student (Contact)** is created in Salesforce (if not already existing).
  2. The created Student is assigned to the **booked Activity Event** (Event Participant record).

- If `"Create Application at the Booking"` flag is **TRUE** for that event:

  3. The system triggers the **Application Creation API** with the necessary data:
     - (Booker) Student ID
     - Booked Activity Event
     - Activity Event's Location → Application Location

  4. Once the Application is created, store **Application ID** to **Event Participant**.
  5. Users can see **Application ID** from the Activity Event.

- If `"Create Application at the Booking"` flag is **FALSE**:

  - System behavior remains as current:
    - Create Contact (if new).
    - Assign Contact to Activity Event.
    - **No Application is created.**

**Technical Notes:**

- The epic states:  
  - “Communicate with Order team for Application API, they will also add new field to store activity event ID”
- There seems to be an **existing Application creation flow** already in use for the Order team, which should be **reused**:
  - For example: converting an Inquiry into a Student and creating an Application.
- For this epic:
  - The same Application Creation API should be invoked from the Booking → Event → Application flow.
  - A new field will be added on the Application to store the **Activity Event ID**.

---

### 4.3. Requirement 3 – Store and Expose Application ID on Event Participant

> 3. Store “Application ID” in Event Participant, so that users can see which Application is created by this event.  
>     1. Can show Application ID in Event Participant List or show in the different table like Order View.  
>     2. No need to have a function to recreate the application, unlike order.

**Description:**

- When an Application is successfully created from a booking:
  - The resulting **Application ID** must be:
    - Persisted on the corresponding **Event Participant** record.
- From the **Activity Event** UI:
  - Users must be able to see **which Application** was created from each participant’s booking.

**Display Options:**

- The epic suggests two UI patterns (one must be chosen in design, or both might be possible):
  1. Show **Application ID** directly in the **Event Participant List** (e.g., as a column).
  2. Show it in a **separate table**, similar to **Order View**.

**Explicit Non-Goal:**

- There is **no requirement** to provide a function to **recreate** the application from the Event screen, unlike existing Order functionality.
  - i.e., this is a **one-way creation**; if something fails, manual handling or other mechanisms apply (not specified here).

---

## 5. Detailed Booking Steps and Flow

From the epic description:

> ## Steps  
> External student apply to the activity event using Booking system:  
> 1. New Student (contact) is created in Salesforce.  
> 2. Created Student is assigned to the booked Activity Event.  
> 3. If  "Create Application at the Booking" flag is TRUE,  
>     1. trigger the Application Creation API with the necessary data:  
>         1. (Booker) Student ID  
>         2. booked Activity Event  
>         3. Activity Event's Location → Application Location  
> 4. Once Appplication is created, store Application ID to Event Participant  
> 5. Users can see Application ID from Activity Event  
> *Communicate with Order team for Application API, they will also add new field to store activity event ID*

### 5.1. End-to-End Flow (Happy Path)

1. **Event Setup:**
   - Staff configures an **Activity Event** in ERP.
   - Staff opens the event to the Booking system.
   - Staff sets `"Create Application at the Booking"` flag based on business needs.

2. **Booking:**
   - External student (or parent) books the event via the **Booking system**.
   - Booking data flows into Salesforce / ERP.

3. **Student Creation:**
   - System checks if a Student (Contact) exists for the booker.
   - If not, creates a **new Contact**.

4. **Event Participant Assignment:**
   - System creates an **Event Participant** record that links:
     - Student (Contact)
     - Activity Event
   - This is the same behavior as current system if flag is **FALSE**.

5. **Application Creation (conditional):**
   - If `"Create Application at the Booking"` = TRUE:
     - System calls the **Application Creation API** with:
       - Student ID
       - Activity Event (ID / ref)
       - Activity Event's Location mapped to **Application Location**
     - Order team’s Application API:
       - Creates an **Enrollment Application** for the student at that Location.
       - Adds a new field to store **Activity Event ID** on the Application.

6. **Storing Application ID:**
   - When the Application is successfully created:
     - System takes the returned **Application ID**.
     - Writes it into the **Event Participant** record (one-to-one mapping between participant and created application in this context).

7. **Visibility in Event Management:**
   - From the **Activity Event** screen:
     - Staff can see for each participant:
       - The **Application ID** (and possibly a clickable link to Admission module, depending on final design).
   - This allows:
     - Traceability from Event → Participant → Application / Admission.

---

## 6. Clarifications and Open Questions from Comments

The epic contains important clarifications from comments by Angelica that further define the scope.

### 6.1. Comment: UI and Flow Clarification

Source:  
https://manabie.atlassian.net/browse/PBT-1771?focusedCommentId=145632  

Author: Angelica Pitogo Abu  
Created: 2026-01-07T02:29:30.522Z  

Text:

> [Maria Nawatani](/people/61c3b17749f195006991f4e0)  
> * Do we have wireframe or design screen for areas that Application ID will be shown? Does it need to be clickable and therefore navigates to the Admission module of that student?  
> * Are we re-using an existing flow or create a new one? What is the admission status?  
> cc: [The Khuong Dang](/people/600655f5ea0e64006b581903)

**Key Points:**

1. **Wireframe / Design for Application ID display:**
   - Need clear design on:
     - Where on the UI the **Application ID** will appear (participant list, detail view, separate table, etc.).
     - How it will be presented (column, badge, etc.).

2. **Clickable behavior and navigation:**
   - Question: Should **Application ID** be **clickable** and navigate to the **Admission module** for that student?
     - If yes:
       - Need deep-link behavior and permission handling.
     - If no:
       - Display as plain text only.

3. **Reuse existing flow or create new:**
   - Clarification needed on whether:
     - The feature will reuse the **existing Application creation flow/API** used by Order team.
     - Or if a **separate, new flow** will be built for this use case.

4. **Admission status on creation:**
   - When the Application is auto-created from a booking:
     - What **initial Admission status** should be set?
     - This impacts downstream Admission / Order processes, reporting, and SLAs.

**Implications:**

- These items require alignment with:
  - Product (PM),
  - Tech (Tech Lead),
  - Design (if any),
  - Order/Admission stakeholders.
- Final answers influence:
  - UI implementation.
  - API integration.
  - Data model (statuses, link behavior).

---

### 6.2. Comment: Scope and Technical Reuse

Source:  
https://manabie.atlassian.net/browse/PBT-1771?focusedCommentId=145709  

Author: Angelica Pitogo Abu  
Created: 2026-01-07T10:24:01.096Z  

Text:

> [Angelica Pitogo Abu](/people/6304974fc3d536e44db0329b)  
> * Order is already using this.  
> * In addition, need to store the application id to event participants.  
> * Req: Create application whether the student booked from SF/manabie app or external site.

**Key Points:**

1. **“Order is already using this.”**
   - There is **already an existing mechanism** (API/flow) for **creating Applications** that is used by the **Order** process.
   - This epic must **reuse** that mechanism instead of building another parallel Application creation logic.

2. **Store application ID to event participants (emphasis).**
   - Reinforces Requirement 3:
     - After an Application is created, its **Application ID** must be:
       - Stored on the **Event Participant** record.
   - This ensures traceability from event participants to their Applications.

3. **Channel-agnostic requirement:**
   - “Req: Create application whether the student booked from SF/manabie app or external site.”
   - The auto-creation of the Application is **not limited** to external Booking site bookings.
   - If conditions are met (e.g., event flag, business rules):
     - Application should be created for bookings that originate from:
       - Salesforce (internal staff creating bookings),
       - Manabie app,
       - External booking site.

**Implications:**

- The logic for Application creation should be **centralized and channel-agnostic**:
  - Triggered whenever a student is assigned to an event **under the auto-application condition**, regardless of booking origin.
- Testing and design must consider:
  - All booking channels.
  - Consistency of behavior across them.

---

### 6.3. Other Comment

Source:  
https://manabie.atlassian.net/browse/PBT-1771?focusedCommentId=134911  

Author: Noritake Takamichi  
Created: 2025-10-02T00:53:36.111Z  

Text:

> [Alexander Teo](/people/712020:4296cef7-cb14-4e06-b59f-7ccb81a93a49)  
> created ticket

- This is simply administrative: indicating that Alexander Teo created the initial ticket.

---

## 7. Open Questions / Decision Points

Based on the epic and comments, several items remain to be explicitly defined in design/implementation:

1. **UI Design for Application ID on Event:**
   - Exact placement in the **Event Management** UI:
     - Event Participant list column?
     - Participant detail pane?
     - Separate sub-table (similar to Order View)?
   - Final decision on:
     - Plain text vs. clickable link to Admission.

2. **Navigation Behavior:**
   - If Application ID is clickable:
     - Target screen (Admission module view, Application details).
     - URL/deeplink format.
     - Permission checks (who can open Admission).

3. **Initial Application Admission Status:**
   - What is the **default status** of auto-created Applications from Events?
   - How does it fit into current Admission / Order flows and reporting?

4. **Existing vs. New Application Creation Flow:**
   - Confirmed reuse of **existing Order team Application Creation API**:
     - How exactly to pass:
       - Student ID
       - Activity Event ID
       - Location
       - Other required fields for that API
   - Error handling strategy:
     - What happens if Application API fails after student & event participant are already created?

5. **Channel-Agnostic Implementation:**
   - Exact triggers for Application creation when booking originates from:
     - Salesforce
     - Manabie app
     - External booking site
   - Any channel-specific constraints.

6. **Idempotency / Duplicates:**
   - If the same student books multiple events with the flag on:
     - One application per event?
     - Or reuse an existing application depending on design?
   - How to avoid duplicate Applications for the same booking if retries happen.

---

## 8. Summary of Intended Behavior

- Koyu uses Booking system to manage trial group lessons.
- Each trial lesson is an **Event** in ERP, which can be opened for external booking.
- On each Event:
  - Staff can configure **Create application when booked** (checkbox).
- When a booking is made (via any channel: external, SF, Manabie app):

  - System will:
    - Ensure a **Student (Contact)** exists.
    - Create an **Event Participant** linking the student to the event.

  - If the event’s **Create Application** flag is ON:
    - System calls the **existing Application Creation API** used by Order:
      - Passes Student ID, Activity Event ID, and Location.
      - Creates an **Enrollment Application** at the event’s Location.
      - Stores **Activity Event ID** on the Application (new field).
    - System writes the **Application ID** into the **Event Participant** record.
    - Staff can **see the Application ID from the Event**, and possibly navigate to Admission depending on final UX.

  - If the flag is OFF:
    - System performs only:
      - Student creation (if needed).
      - Event Participant creation.
    - **No Application** is created.

---

## 9. Links

- Jira Epic PBT-1771:  
  - https://manabie.atlassian.net/browse/PBT-1771  

- Group Experience Lesson Spec (Req. No. 514):  
  - https://manabie.atlassian.net/wiki/spaces/PrTi/pages/1814003739/No.514_Manage+group+experiences+lesson+as+events  

- Koyu Requirements – July 2026:  
  - https://manabie.atlassian.net/wiki/spaces/PRDM/pages/1927249935/Koyu+Requirements+-+July+2026  

- Attachment (image):  
  - https://api.media.atlassian.com/file/8f28d754-b021-4703-ae1e-94120965f10d/binary?token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJkM2FmZWViMi1jZjdkLTQxMjYtYjEyYi00Y2YzYzczN2ExM2EiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpmaWxlOjhmMjhkNzU0LWIwMjEtNDcwMy1hZTFlLTk0MTIwOTY1ZjEwZCI6WyJyZWFkIl19LCJleHAiOjE3NzI2MTk2NjksIm5iZiI6MTc3MjYxOTA2OX0.Uno_zPBZQjF1Hh4Xl3_W3rkRDa29r3UelRxADWqn2eQ&client=d3afeeb2-cf7d-4126-b12b-4cf3c737a13a&dl=true&name=image-20251125-040910.png