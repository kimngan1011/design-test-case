# Test Cases: LT-102422 - Publish lesson menu in Lesson Calendar

## Suite: Publish Lesson Menu in Lesson Calendar

### Lesson Calendar - Right Menu - Draft Lesson - Publish Lesson Item - Visible

**Description:** AC 01.1 - Decision Table - Draft lesson shows Publish Lesson action in the right-side calendar menu.

**Preconditions:**
- Logged in as HQ or CM Staff on Salesforce calendar.
- A lesson with status Draft exists on calendar day view.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson Calendar and select a Draft lesson card. | Lesson detail side menu opens for the selected lesson. | lesson_status = Draft |
| 2 | Open the right-side lesson menu actions. | Publish Lesson action is visible in the menu. | menu_context = lesson_card |

**Severity:** major
**Priority:** high

---

### Lesson Calendar - Right Menu - Published Lesson - Publish Lesson Item - Hidden

**Description:** AC 01.2 - Decision Table - Published lesson does not show Publish Lesson action in the right-side calendar menu.

**Preconditions:**
- Logged in as HQ or CM Staff on Salesforce calendar.
- A lesson with status Published exists on calendar day view.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson Calendar and select a Published lesson card. | Lesson detail side menu opens for the selected lesson. | lesson_status = Published |
| 2 | Open the right-side lesson menu actions. | Publish Lesson action is not present in the menu. | menu_context = lesson_card |

**Severity:** major
**Priority:** high

---

### Lesson Calendar - Right Menu - Completed Lesson - Publish Lesson Item - Hidden

**Description:** AC 01.3 - Decision Table - Completed lesson does not show Publish Lesson action in the right-side calendar menu.

**Preconditions:**
- Logged in as HQ or CM Staff on Salesforce calendar.
- A lesson with status Completed exists on calendar day view.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson Calendar and select a Completed lesson card. | Lesson detail side menu opens for the selected lesson. | lesson_status = Completed |
| 2 | Open the right-side lesson menu actions. | Publish Lesson action is not present in the menu. | menu_context = lesson_card |

**Severity:** minor
**Priority:** medium

---

### Lesson Calendar - Right Menu - Cancelled Lesson - Publish Lesson Item - Hidden

**Description:** AC 01.4 - Decision Table - Cancelled lesson does not show Publish Lesson action in the right-side calendar menu.

**Preconditions:**
- Logged in as HQ or CM Staff on Salesforce calendar.
- A lesson with status Cancelled exists on calendar day view.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson Calendar and select a Cancelled lesson card. | Lesson detail side menu opens for the selected lesson. | lesson_status = Cancelled |
| 2 | Open the right-side lesson menu actions. | Publish Lesson action is not present in the menu. | menu_context = lesson_card |

**Severity:** minor
**Priority:** medium
