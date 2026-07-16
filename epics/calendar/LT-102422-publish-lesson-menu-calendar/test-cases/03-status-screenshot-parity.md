# Test Cases: LT-102422 - Publish lesson menu in Lesson Calendar

## Suite: Publish Lesson Menu in Lesson Calendar

### Lesson Calendar - Draft Lesson - Right Menu - Matches PBT-2340 Draft Screenshot

**Description:** Validate that menu layout, status presentation, and action set for Draft lesson match the Draft screenshot attached in PBT-2340.

**Preconditions:**
- Logged in as HQ or CM Staff on Salesforce calendar.
- A lesson with status Draft exists on calendar day view.
- PBT-2340 ticket attachments are accessible for visual reference.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open PBT-2340 and identify the Draft-status screenshot in attachments. | Draft reference screenshot is opened and usable as expected baseline. | source = PBT-2340 attachment (Draft) |
| 2 | Open Lesson Calendar and select a Draft lesson card, then open right-side menu. | Right-side menu for Draft lesson is displayed in calendar context. | lesson_status = Draft |
| 3 | Compare actual menu/status display with attachment baseline. | Menu composition and status presentation match Draft screenshot baseline; Publish Lesson is visible. | compare_mode = visual_parity |

**Severity:** major
**Priority:** high

---

### Lesson Calendar - Published Lesson - Right Menu - Matches PBT-2340 Published Screenshot

**Description:** Validate that menu layout, status presentation, and action set for Published lesson match the Published screenshot attached in PBT-2340.

**Preconditions:**
- Logged in as HQ or CM Staff on Salesforce calendar.
- A lesson with status Published exists on calendar day view.
- PBT-2340 ticket attachments are accessible for visual reference.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open PBT-2340 and identify the Published-status screenshot in attachments. | Published reference screenshot is opened and usable as expected baseline. | source = PBT-2340 attachment (Published) |
| 2 | Open Lesson Calendar and select a Published lesson card, then open right-side menu. | Right-side menu for Published lesson is displayed in calendar context. | lesson_status = Published |
| 3 | Compare actual menu/status display with attachment baseline. | Menu composition and status presentation match Published screenshot baseline; Publish Lesson is hidden. | compare_mode = visual_parity |

**Severity:** major
**Priority:** high

---

### Lesson Calendar - Completed Lesson - Right Menu - Matches PBT-2340 Completed Screenshot

**Description:** Validate that menu layout, status presentation, and action set for Completed lesson match the Completed screenshot attached in PBT-2340.

**Preconditions:**
- Logged in as HQ or CM Staff on Salesforce calendar.
- A lesson with status Completed exists on calendar day view.
- PBT-2340 ticket attachments are accessible for visual reference.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open PBT-2340 and identify the Completed-status screenshot in attachments. | Completed reference screenshot is opened and usable as expected baseline. | source = PBT-2340 attachment (Completed) |
| 2 | Open Lesson Calendar and select a Completed lesson card, then open right-side menu. | Right-side menu for Completed lesson is displayed in calendar context. | lesson_status = Completed |
| 3 | Compare actual menu/status display with attachment baseline. | Menu composition and status presentation match Completed screenshot baseline; Publish Lesson is hidden. | compare_mode = visual_parity |

**Severity:** medium
**Priority:** medium

---

### Lesson Calendar - Cancelled Lesson - Right Menu - Matches PBT-2340 Cancelled Screenshot

**Description:** Validate that menu layout, status presentation, and action set for Cancelled lesson match the Cancelled screenshot attached in PBT-2340.

**Preconditions:**
- Logged in as HQ or CM Staff on Salesforce calendar.
- A lesson with status Cancelled exists on calendar day view.
- PBT-2340 ticket attachments are accessible for visual reference.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open PBT-2340 and identify the Cancelled-status screenshot in attachments. | Cancelled reference screenshot is opened and usable as expected baseline. | source = PBT-2340 attachment (Cancelled) |
| 2 | Open Lesson Calendar and select a Cancelled lesson card, then open right-side menu. | Right-side menu for Cancelled lesson is displayed in calendar context. | lesson_status = Cancelled |
| 3 | Compare actual menu/status display with attachment baseline. | Menu composition and status presentation match Cancelled screenshot baseline; Publish Lesson is hidden. | compare_mode = visual_parity |

**Severity:** medium
**Priority:** medium
