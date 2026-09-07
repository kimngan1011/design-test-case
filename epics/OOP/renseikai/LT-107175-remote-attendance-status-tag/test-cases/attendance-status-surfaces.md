# Test Cases: LT-107175 — Remote Attendance Status and Tag

## Suite: [Renseikai] Attendance Status — SF, BO & App Surfaces

### [Renseikai] Salesforce Lesson Detail – Attendance Status – English Remote selection – Saved value shown

**Description:** AC 01.5 — State Transition — Attendance Status shows `Remote` after reopening.

**Preconditions:**

- English locale is available.
- Student A status is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects `Remote` in Salesforce Lesson Detail and saves in English locale. | Attendance Status shows `Remote` after reopening | locale=EN; A: Attend→Remote |

**Severity:** major
**Priority:** high

---
### [Renseikai] Salesforce Lesson Detail – Attendance Status – Japanese Remote selection – Localized value shown

**Description:** AC 01.5 — Component — Attendance Status shows `リモート参加` and the picker includes that value.

**Preconditions:**

- Japanese locale is available.
- Student A status is Remote.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Salesforce Lesson Detail in Japanese locale. | Attendance Status shows `リモート参加` and the picker includes that value | locale=JP; A=Remote |

**Severity:** major
**Priority:** high

---
### [Renseikai] BO Student Tab – Attendance Status – English Remote value – Saved value shown

**Description:** AC 01.6 — State Transition — Attendance Status shows `Remote` after reopening.

**Preconditions:**

- English locale is available.
- Student A status is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Remote in BO Student Tab and saves in English locale. | Attendance Status shows `Remote` after reopening | locale=EN; A: Attend→Remote |

**Severity:** major
**Priority:** high

---
### [Renseikai] BO Student Tab – Attendance Status – Japanese Remote value – Localized value shown

**Description:** AC 01.6 — Component — Attendance Status shows `リモート参加`.

**Preconditions:**

- Japanese locale is available.
- Student A status is Remote.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens BO Student Tab in Japanese locale. | Attendance Status shows `リモート参加` | locale=JP; A=Remote |

**Severity:** major
**Priority:** high

---
### [Renseikai] Attendance Status – Staff access matrix – In-scope staff roles – Remote can be viewed and updated

**Description:** AC 01.5 / 01.6 — Permission Matrix — Each in-scope staff role can view and save Remote.

**Preconditions:**

- Accounts exist for HQ Staff, Centre Manager, and Centre Staff.
- The same learner session is editable for each role.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Each of HQ Staff, Centre Manager, and Centre Staff selects Remote and saves the same learner session. | Each in-scope staff role can view and save Remote | roles=HQ Staff,Centre Manager,Centre Staff; value=Remote |

**Severity:** major
**Priority:** high

---
### [Renseikai] Learner App – Lesson Detail – Staff-set Remote – Status value displayed

**Description:** AC 01.7 — Cross-system — Attendance Status displays `Remote` / `リモート参加` for the current locale.

**Preconditions:**

- Student A has status Remote set by staff
- lesson APP-101 is visible.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student opens lesson APP-101 in Learner App | Attendance Status displays `Remote` / `リモート参加` for the current locale | APP-101; source=staff; status=Remote |

**Severity:** minor
**Priority:** medium

---
### [Renseikai] Learner App – Lesson Detail – App-set Remote – Response value displayed

**Description:** AC 01.7 — Cross-system — Attendance Status is Remote and Attendance Response is Attended Remotely in the current locale.

**Preconditions:**

- Student A submitted Attended Remotely for APP-102.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student opens lesson APP-102 in Learner App | Attendance Status is Remote and Attendance Response is Attended Remotely in the current locale | APP-102; response=Attended Remotely |

**Severity:** minor
**Priority:** medium

---
### [Renseikai] Salesforce Lesson Detail – Attendance Response – Attended Remotely – Option and remark displayed

**Description:** AC 02.1 — Component — Response shows `Attended Remotely (Travel disruption)` in EN or `リモート参加 (Travel disruption)` in JP.

**Preconditions:**

- Student A response is Attended Remotely with remark `Travel disruption`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Salesforce Lesson Detail | Response shows `Attended Remotely (Travel disruption)` in EN or `リモート参加 (Travel disruption)` in JP | response=Attended Remotely; remark=Travel disruption |

**Severity:** minor
**Priority:** medium

---
### [Renseikai] BO Student Tab – Attendance Response – Attended Remotely – Option and remark displayed

**Description:** AC 02.2 — Component — Response shows `Attended Remotely (Travel disruption)` in EN or `リモート参加 (Travel disruption)` in JP.

**Preconditions:**

- Student A response is Attended Remotely with remark `Travel disruption`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens BO Student Tab | Response shows `Attended Remotely (Travel disruption)` in EN or `リモート参加 (Travel disruption)` in JP | response=Attended Remotely; remark=Travel disruption |

**Severity:** minor
**Priority:** medium

---
