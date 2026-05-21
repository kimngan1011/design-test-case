# Test Cases: LT-96662 — Publish and Notify Student

## Suite: Publish and Notify Student – Notification Content

### Notification Content – English – Title and body match lesson details

**Description:** AC 02.1 — Equivalence Partitioning — The push notification title and body content match the defined EN template with the correct lesson name, date, start time, and end time.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published**:
  - Lesson name: "Science Basics – Session 3"
  - Lesson date: 2026-04-20 (Monday)
  - Start time: 09:00 | End time: 10:30
- Student G is assigned to the lesson; logged into the Learner App (EN locale) on Device 1 with push notifications enabled

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson | Lesson Detail page opens; status = "Published" | Lesson: "Science Basics – Session 3" |
| 2   | Click "Publish and notify student", then click "Send" | Modal closes | "" |
| 3   | On Device 1, open the Learner App and expand the received push notification | Notification title is exactly: **"Lesson Published"** | "" |
| 4   | Read the notification body text fully | Notification body is exactly: **"The schedule for Science Basics – Session 3 has been published. Lesson Date: 2026-04-20 \| 09:00 - 10:30. Tap the button below to view the lesson details."** | "" |

**Severity:** major
**Priority:** high

---

### Notification Content – Japanese – JP title and body match translation table

**Description:** AC 02.1 — Equivalence Partitioning — The push notification title and body content match the defined JP translation table for Renseikai (JP tenant).

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published**:
  - Lesson name: "数学基礎 – 第3回" (Math Basics – Session 3)
  - Lesson date: 2026-04-20
  - Start time: 09:00 | End time: 10:30
- Student H is assigned to the lesson; logged into the Learner App (JP locale) on Device 2 with push notifications enabled

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson | Lesson Detail page opens; status = "Published" | Lesson: "数学基礎 – 第3回" |
| 2   | Click "Publish and notify student", then click "Send" | Modal closes | "" |
| 3   | On Device 2 (JP locale), open the Learner App and expand the received push notification | Notification title is exactly: **"授業公開のおしらせ"** | "" |
| 4   | Read the notification body text fully | Notification body is exactly: **"数学基礎 – 第3回 の授業が公開されました。授業日: 2026-04-20 \| 09:00 - 10:30. 授業詳細を見るにはボタンをタップしてください。"** | "" |

**Severity:** normal
**Priority:** medium

---
