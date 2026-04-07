# Event Master – Create/Edit Form (Consolidated Spec)

> **Last updated:** 2026-04-05 (updated with Slack thread #camp-b clarifications)
> **Purpose:** Tổng hợp tất cả spec/ticket/PR liên quan đến Event Master form để làm cơ sở update test case.

---

## Nguồn tham chiếu

| # | Nguồn | Mô tả |
|---|---|---|
| 1 | [Confluence: US 01-03 CRUD Event Master](https://manabie.atlassian.net/wiki/spaces/ERP/pages/950632503) | Spec gốc tạo Event Master (2024) |
| 2 | [Confluence: Core \| Paid Event](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/1307476016) (Epic LT-56276) | Thêm fields cho Paid Event + Participant Settings |
| 3 | Spec LT-94674 / PBT-1697: Cancel Booked Event (App) | Thêm Cancellation Settings, Reminders & Notifications, Booking Settings |
| 4 | Spec LT-90578 / PBT-1771: Auto Create Application for Event Participants | Thêm "Create Application at the Booking" checkbox |
| 5 | [Confluence: US 07-16 Event Master Record Page](https://manabie.atlassian.net/wiki/spaces/ERP/pages/959316025) | Cấu trúc Record Page / View |
| 6 | Bug LT-85088: Negative max events per student | Fix validation số âm |
| 7 | Jira LT-76359: Update Event Master form (Create/Edit) | Task cập nhật form cho Paid Event |
| 8 | Slack thread #camp-b (Feb 27 – Mar 26) | Clarifications: bỏ 2 cancel fields → 1, response label changes, skip deadline popup, Create Application editable, Booking Start Date migration |

---

## Event Master – CREATE/EDIT FORM

### Section 1: General Info

| # | Field | API Name | Type | Required | Default | Business Rule |
|---|---|---|---|---|---|---|
| 1 | **Event Name** | `Name` | Free text | **Yes** | — | Max 80 characters |
| 2 | **Event Type** | `Event_Type__c` | Picklist: `Free`, `Paid` | **Yes** | — | Copy to all Activity Events khi tạo (read-only on AE). Nếu Paid → AE hiện thêm Product Offering field |
| 3 | **Description** | `Description__c` | Long Text Area (Rich text) | No | — | Allow attach file. Edit ở master KHÔNG sync xuống Activity Event đã tạo |

### Section 2: Participant Settings

| # | Field | API Name | Type | Required | Default | Business Rule |
|---|---|---|---|---|---|---|
| 4 | **Send To** | `Send_To__c` | Picklist: `Student & Parent`, `Student only`, `Parent only` | **Yes** | — | Tooltip: *"This settings is automatically applied to all activity events"*. Copy 1 lần khi tạo AE; edit sau không ảnh hưởng AE đã tạo |
| 5 | **Who Can Reserve** | `Who_Can_Reserve__c` | Picklist | **Yes** | — | Tooltip: *"This settings is used for booking systems and automatically applied to all activity events"*. Logic: Nếu Send To = `Student & Parent` → hiện cả 2 option để chọn. Nếu `Student only` / `Parent only` → pre-filled, not editable. Copy 1 lần khi tạo AE |
| 6 | **Reminders** | `Reminders__c` | Number (days) | No | — | Tooltip: *"This settings is automatically applied to all activity events"*. Copy 1 lần khi tạo AE |
| 7 | **Max Event Per Student** | `Max_Event_Per_Student__c` | Number (integer) | No | null | Tooltip: *"Defines the maximum number of activity events a student can book"*. null = không giới hạn. Không chấp nhận số âm (bug LT-85088 đã fix) |

### Section 3: Cancellation Settings (from LT-94674)

> **⚠️ Slack clarification (Feb 27):** Spec gốc có 2 fields Allow Cancellation (Direct + Booked). Angelica xác nhận "Ah no need" — chỉ dùng **1 cancellation rule chung** cho tất cả participants, KHÔNG tách 2 fields.

| # | Field | API Name | Type | Required | Default | Business Rule |
|---|---|---|---|---|---|---|
| 8 | ~~**Allow Cancellation (Directly Added Participants)**~~ | ~~`Allow_Cancel_Direct__c`~~ | ~~Checkbox~~ | — | — | **REMOVED** — Không cần tách riêng, dùng 1 rule chung |
| 9 | ~~**Allow Cancellation (Booking System Participants)**~~ | ~~`Allow_Cancel_Booked__c`~~ | ~~Checkbox~~ | — | — | **REMOVED** — Không cần tách riêng, dùng 1 rule chung |
| 10 | **Cancellation Type** | `Cancellation_Type__c` | Picklist: `Do not allow`, `Cancel`, `Cancellation Request` | **Yes** | Enabled by default | Single select only. `Do not allow` → ẩn Cancel button trên mobile + disable các field cancel liên quan. `Cancel` → immediate removal. `Cancellation Request` → keep participant in list, status = Cancel Requested |
| 11 | **Cancellation Deadline (Hours)** | `Cancellation_Deadline_Hours__c` | Number (integer, 0–4 digits) | No | 0 | Disabled by default. Enabled khi Cancellation Type = Cancel hoặc Cancellation Request. Đơn vị: giờ trước Event Start DateTime. 0 hoặc null = deadline = event date. Luôn evaluate theo **Event timezone** |

**Cancellation Deadline – Update Rules:**

> **⚠️ Slack clarification (Mar 2–3):** Angelica xác nhận: *"Skip this prompt/message but implement the logic."* → **Không hiện popup**, chỉ implement logic recompute silently.

- Khi user update Cancellation Deadline & event đang in-progress (current date >= bất kỳ activity event date):
  - ~~Hiện warning popup~~ → **Không hiện popup** (confirmed by PO)
  - Silently recompute deadline **chỉ cho unstarted activities** (activities chưa đến date)
  - Activities đã started → không bị ảnh hưởng
- Khi chưa start → recompute bình thường

### Section 4: Reminders & Notifications (from LT-94674)

| # | Field | API Name | Type | Required | Default | Business Rule |
|---|---|---|---|---|---|---|
| 12 | **Reminders** | (moved here) | Number (days) | No | — | Trước đây nằm riêng, giờ gom vào section này |
| 13 | **Response Notification** | `Response_Notification_Setting__c` | Picklist: `none`, `Cancel` | No | `none` | Tooltip: *"Send a Salesforce notification when the mobile app user submits a response."* Cancel notification áp dụng cho cả Cancel và Cancellation Request. Nếu Cancel Notification set nhưng Cancel Type = Do not allow → **không trigger notification**. Admin/manual updates và imports **không trigger** notification |

### Section 5: Booking Settings (config qua "Open to Booking" dialog)

| # | Field | Type | Required | Default | Business Rule |
|---|---|---|---|---|---|
| 14 | **Booking Start Date** | Date | No | — | Khi current date < booking start date → disable Reserve button + show message trên mobile/web: *"This event will be available for booking from \<Start Date\>"*. **Migration (Slack Mar 26):** If `Open To Booking System = True` → `start date = event created date`; If `False` → leave empty |
| 15 | **Booking End Date** (trước là Expiration Date) | Date | No | — | Khi expire (Expiration date < today) → auto close booking system |
| 16 | **Create Application when Booked** | Checkbox | No | — | Hiện trong "Open to Booking System" popup. Khi true → auto tạo Enrollment Application khi student book event qua Booking system. Tooltip EN: *"Create Enrollment Application for a new student who books via the Booking system"*. Tooltip JP: *"予約システムを通じて新規作成された生徒の所属先申請も同時に作成します"*. **⚠️ Slack clarification (Mar 9):** Giữ **editable** (không read-only) as planned in LT-90578 |
| 17 | **Who Can Reserve** | (read-only in popup) | — | — | Fetched from Event Master, không editable trong Open to Booking popup |

---

## Compact Layout (Record Page Header)

- Event Name
- Event Type
- Who Can Reserve
- Max Event Per Student

---

## Record Page View – Sections

1. **General Info** — Event Name, Event Type
2. **Description** — Rich text
3. **Participant Settings** — Send To, Who Can Reserve, Reminders, Max Event Per Student
4. **Cancellation Settings** — Allow Cancel Direct, Allow Cancel Booked, Cancellation Type, Cancellation Deadline
5. **Reminders & Notifications** — Reminders, Response Notification
6. **Booking Settings** — Booking info (read-only), Create Application when Booked
7. **Notes & Attachments**
8. **System Information** — Record history

---

## Key Business Rules (Tổng hợp)

| # | Rule | Source |
|---|---|---|
| 1 | Event Type copy xuống Activity Event 1 lần khi tạo, không editable trên AE | Paid Event PRD |
| 2 | Send To, Who Can Reserve, Reminders copy 1 lần khi tạo AE → edit sau trên Master không ảnh hưởng AE đã tạo | Paid Event PRD |
| 3 | Max Event Per Student = null → no limit; không chấp nhận số âm | Paid Event PRD + Bug LT-85088 |
| 4 | Cancellation Type = "Do not allow" → ẩn Cancel button trên mobile + disable Cancellation Deadline | LT-94674 |
| 5 | Cancellation Deadline tính theo Event timezone; 0/null = deadline = event date | LT-94674 |
| 6 | Update Cancellation Deadline khi event in-progress → **no popup** (bỏ warning), silently recompute chỉ cho unstarted activities | LT-94674 + Slack Mar 3 |
| 7 | Response Notification = Cancel nhưng Cancel Type = Do not allow → no notification triggered | LT-94674 |
| 8 | Notification chỉ trigger cho mobile-initiated actions; không trigger cho admin/manual/import updates | LT-94674 |
| 9 | Booking Start Date > current date → disable Reserve, show message | LT-94674 |
| 10 | Expiration Date < today → auto close booking system | Paid Event PRD |
| 11 | Create Application when Booked = true → auto tạo Enrollment Application cho new student book qua Booking system | PBT-1771 |
| 12 | Delete Event Master → confirm message → xóa luôn tất cả Activity Events liên quan | CRUD Event Master spec |
| 13 | Edit Description trên master KHÔNG sync xuống AE đã tạo | CRUD Event Master spec |
| 14 | ~~Allow Cancel Direct / Allow Cancel Booked~~ → **REMOVED**: Chỉ dùng 1 cancellation rule chung, không tách 2 fields | LT-94674 + Slack Feb 27 |
| 15 | Cancellation Type enabled by default, single select only | LT-94674 |
| 16 | Migration: Cancel Config ON → Cancel Type = Cancel; Cancel Config OFF → Cancel Type = Do not allow | LT-94674 |
| 17 | Cancel button visibility trên mobile controlled bởi Cancellation Type | LT-94674 (updated AC 01.1) |
| 18 | **Response label changes**: Accept → **Attend** (Planning to attend), Declined → **Absent** (Planning to be absent). Label only, all functions retained | Slack Feb 27 |
| 19 | **Booking Start Date migration**: Open To Booking = True → start date = event created date; False → empty | Slack Mar 26 |
| 20 | **Create Application checkbox**: Giữ editable, không chuyển read-only (dù có conflict với LT-90578) | Slack Mar 9 |

---

## Cancellation Reason Options (for Participants – reference)

Khi participant cancel qua mobile, phải chọn 1 trong 8 reasons:
1. Schedule conflict
2. Not feeling well / Health reason
3. School event / Exam
4. Family reason
5. Transportation issue
6. Forgot / Mistaken booking
7. No longer interested
8. Other (→ yêu cầu nhập detail, max 255 chars)

---

## Lưu ý: Event Master form vs Activity Event form

**Event Master form** (tài liệu này) dùng để tạo/edit **master** — là template dùng cho nhiều Activity Events.

**Activity Event form** (Create Activity Event dialog) có thêm các field riêng:
- Event Master (lookup)
- Location (lookup)
- Event Capacity (number)
- Event Medium (picklist: Offline/Online)
- Event Classrooms (multi-select lookup)
- Date, Start Time, End Time
- Activity Event Status: `Draft`, `Published` (default = Published) — from LT-96096
- Conference (checkbox)
- Counseling (checkbox)
- Product Offering (lookup, only khi Event Type = Paid)
- Product Price (formula, read-only)
- Order Location (lookup, optional)

---

## Related Jira Tickets

| Key | Summary | Status |
|---|---|---|
| LT-56276 | [SF Event] CRUD Paid Event and link with Order | Done |
| LT-76359 | [SF] Update Event Master form (Create/Edit) | Done |
| LT-76360 | [SF] Validate Logic import Event Master | Done |
| LT-76361 | [SF] Add new field to target location table under Event Master Record page | Done |
| LT-94674 | Koyu Core 524 - Cancel Booked Event (App) | In Progress |
| PBT-1771 | [koyu] Core 514 - Auto Create Application for Event Participants | In Development |
| LT-96096 | Draft Status to Activity Event | Done |
| LT-85088 | Event Master can be created with negative max events per student | Closed |
| LT-76332 | [QA] Read document and write testcase for create event master on Qase | Done |
