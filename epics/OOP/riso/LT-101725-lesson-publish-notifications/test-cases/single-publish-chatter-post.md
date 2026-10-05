# Test Cases: LT-101725 — Riso Lesson Publish Notifications to Teachers

## Suite: [Riso] Single Publish – Chatter Post

### [Riso] Lesson Publish – Chatter Post – Draft lesson published – Chatter post appears in Lesson Detail Chatter section

**Description:** AC-01, BR-01 — State Transition — Happy path: publishing a Draft lesson triggers the SF Flow Builder to create exactly 1 Chatter post in the Lesson Detail Chatter section.

**Preconditions:**
- Riso Salesforce org with Lesson Publish Notification config flag = ON
- A lesson named "English Class A" exists in Draft status
- Lesson Teacher "Tanaka Kenji" (working_status=Available, working_type=Full Time) is assigned to the lesson
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open lesson "English Class A" in the SF Lesson Detail page | Lesson Detail page opens; lesson status = Draft | lesson_name="English Class A" |
| 2 | Change the lesson status to Published | Status updates to Published | "" |
| 3 | Navigate to the Chatter section of the Lesson Detail page | Chatter section is visible | "" |
| 4 | Observe the Chatter section content | Exactly 1 new Chatter post is visible in the Chatter section | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Publish – Chatter Post – Published lesson transitioned to Completed – No Chatter post triggered

**Description:** AC-01, BR-01 — State Transition negative — Transitioning a Published lesson to Completed does not trigger a new Chatter post.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A lesson exists in Published status with 1 Available Lesson Teacher assigned
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Published lesson in SF Lesson Detail | Lesson status = Published | "" |
| 2 | Note the current number of Chatter posts in the Chatter section | Baseline Chatter post count recorded | "" |
| 3 | Change the lesson status to Completed | Status updates to Completed | "" |
| 4 | Navigate to the Chatter section | Chatter post count is unchanged — no new post was added on the Published → Completed transition | baseline_count = count before Completed |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Publish – Chatter Post – Published lesson moved to Draft – No Chatter post triggered

**Description:** AC-01, BR-01 — State Transition negative — Unpublishing a lesson (Published → Draft) does not trigger a Chatter post.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A lesson exists in Published status with 1 Available Lesson Teacher assigned
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Published lesson in SF Lesson Detail | Lesson status = Published | "" |
| 2 | Note the current number of Chatter posts in the Chatter section | Baseline Chatter post count recorded | "" |
| 3 | Change the lesson status back to Draft (unpublish) | Status updates to Draft | "" |
| 4 | Navigate to the Chatter section | Chatter post count is unchanged — no new post created on unpublish | baseline_count = count before Draft |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Publish – Chatter Post – Lesson republished after unpublishing – New Chatter post created alongside existing post

**Description:** AC-01, BR-02 — State Transition — Republishing a lesson (Published → Draft → Published) creates a new Chatter post; the old post remains visible alongside it.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A lesson previously published (1 Chatter post already in Chatter section), then moved back to Draft
- 1 Available Lesson Teacher assigned (working_status=Available, working_type=Full Time)
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Draft lesson (previously published once) in SF Lesson Detail | Lesson status = Draft; Chatter section shows 1 existing post from the previous publish | previous_publish_count=1 |
| 2 | Change the lesson status to Published again | Status updates to Published | "" |
| 3 | Navigate to the Chatter section | 2 Chatter posts are now visible — the old post AND a newly created post | "" |
| 4 | Observe both posts | Old Chatter post remains visible; new Chatter post appears with fresh @mention and publish notification text | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Publish – Teacher Filter – Available Full-Time teacher – @mentioned in Chatter post body

**Description:** AC-02.1, BR-04 — Decision Table — A Lesson Teacher with working_status=Available and working_type=Full Time is included in the Chatter post @mention.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A Draft lesson with 1 Lesson Teacher: name="Tanaka Kenji", working_status=Available, working_type=Full Time
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Publish the lesson (change status Draft → Published) | Status = Published | "" |
| 2 | Navigate to the Chatter section of the Lesson Detail page | Chatter section shows 1 new post | "" |
| 3 | Read the Chatter post body | The post body contains "@Tanaka Kenji" as an active SF @mention | working_status=Available; working_type=Full Time |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Publish – Teacher Filter – Available Part-Time teacher – @mentioned in Chatter post body

**Description:** AC-02.1, BR-04 — Decision Table — A Lesson Teacher with working_status=Available and working_type=Part Time is also included in the Chatter post @mention.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A Draft lesson with 1 Lesson Teacher: name="Yamamoto Yuki", working_status=Available, working_type=Part Time
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Publish the lesson (change status Draft → Published) | Status = Published | "" |
| 2 | Navigate to the Chatter section | 1 new Chatter post visible | "" |
| 3 | Read the Chatter post body | The post body contains "@Yamamoto Yuki" as an active SF @mention | working_status=Available; working_type=Part Time |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Publish – Teacher Filter – Unavailable teacher assigned to lesson – Not @mentioned in Chatter post

**Description:** AC-02.1, BR-04 — Decision Table negative — A Lesson Teacher with working_status=Unavailable is excluded from the Chatter post @mention.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A Draft lesson with 2 Lesson Teachers:
  - "Tanaka Kenji": working_status=Available, working_type=Full Time
  - "Sato Hiroshi": working_status=Unavailable, working_type=Full Time
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Publish the lesson | Status = Published | "" |
| 2 | Navigate to the Chatter section | 1 new Chatter post visible | "" |
| 3 | Read the Chatter post body | Post body contains "@Tanaka Kenji" | Teacher A: Available; Teacher B: Unavailable |
| 4 | Search the post body for "@Sato Hiroshi" | "@Sato Hiroshi" is NOT present in the Chatter post body | working_status=Unavailable → excluded |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Publish – Teacher Filter – Lesson with multiple Available teachers – Single Chatter post with all teachers @mentioned

**Description:** AC-02.1, AC-04, BR-05, BR-09 — CRUD — All Available teachers are @mentioned in a single Chatter post; the system does not create one post per teacher.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A Draft lesson with 3 Available Lesson Teachers:
  - "Tanaka Kenji" (Full Time, Available)
  - "Yamamoto Yuki" (Part Time, Available)
  - "Nakamura Hana" (Full Time, Available)
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Publish the lesson | Status = Published | 3 Available teachers assigned |
| 2 | Navigate to the Chatter section | Chatter section is visible | "" |
| 3 | Count the number of Chatter posts in the section | Exactly 1 Chatter post exists (not 3 separate posts) | expected: 1 post for all 3 teachers |
| 4 | Read the single Chatter post body | Post body contains "@Tanaka Kenji", "@Yamamoto Yuki", and "@Nakamura Hana" — all 3 teachers @mentioned in the same post | teacher_1=Tanaka Kenji; teacher_2=Yamamoto Yuki; teacher_3=Nakamura Hana |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Publish – Chatter Post Content – English post body – All required text and @mentions rendered

**Description:** AC-05, BR-10 — Component — The EN Chatter post body contains the exact required text with resolved teacher @mention and lesson name hyperlink.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A Draft lesson with lesson_name="English Class A" and 1 Available teacher "Tanaka Kenji" (Full Time)
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Publish the lesson | Status = Published | lesson_name="English Class A"; teacher="Tanaka Kenji" |
| 2 | Navigate to the Chatter section | 1 new Chatter post visible | "" |
| 3 | Read the post body in full | Post body reads: "@Tanaka Kenji — English Class A has been published. Click to see more details." where "English Class A" is a hyperlink | EN post; expected text per BR-10 |
| 4 | Confirm "@Tanaka Kenji" appears as an active SF @mention | "@Tanaka Kenji" is highlighted as an SF @mention link, not plain text | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Publish – Chatter Post Content – Japanese post body – All required text and @mentions rendered

**Description:** AC-05, BR-11 — Component — The JP Chatter post body contains the exact required Japanese text with resolved teacher @mention and lesson name hyperlink.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A Draft lesson with lesson_name="英語クラスA" and 1 Available teacher with display name "田中健二" (Full Time)
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Publish the lesson | Status = Published | lesson_name="英語クラスA"; teacher="田中健二" |
| 2 | Navigate to the Chatter section | 1 new Chatter post visible | "" |
| 3 | Read the post body in full | Post body reads: "@田中健二 — 英語クラスAが公開されました。詳細はこちらをクリックしてください。" where "英語クラスA" is a hyperlink | JP post; expected text per BR-11 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Publish – Chatter Post Content – Lesson Name in post body – Hyperlinked to BO Lesson Detail page

**Description:** AC-05, BR-12 — Component — The Lesson Name in the Chatter post body is a clickable hyperlink pointing to the BO Lesson Detail page for the same lesson.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A Draft lesson with lesson_name="English Class A" published; Chatter post visible in Chatter section
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to the Chatter section of the published lesson | Chatter post is visible | lesson_name="English Class A" |
| 2 | Locate the lesson name "English Class A" in the post body | "English Class A" appears as a hyperlink (underlined or styled as a clickable link) | "" |
| 3 | Click the "English Class A" hyperlink | BO Lesson Detail page for "English Class A" opens in a new browser tab | expected: new tab, correct BO lesson |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Publish – Chatter Post – Lesson Name hyperlink clicked – BO Lesson Detail opens in new browser tab

**Description:** AC-08, BR-15 — Component (Smoke) — Clicking the Lesson Name hyperlink opens the BO Lesson Detail page for the same lesson in a new tab, leaving the current tab open.

**Preconditions:**
- Riso Salesforce org
- A published lesson with a Chatter post visible in the Chatter section
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Chatter section of the published lesson | Chatter post visible with a clickable Lesson Name hyperlink | "" |
| 2 | Click the Lesson Name hyperlink in the Chatter post | A new browser tab opens | "" |
| 3 | Observe the new tab | The new tab displays the BO Lesson Detail page for the correct lesson | "" |
| 4 | Switch back to the original tab | The original Salesforce tab remains open and unchanged | "" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson Publish – Teacher Added from SF Lesson Detail – Recurring lesson – “Only this” – One new Chatter post triggered

**Description:** AC-01, BR-26 — State Transition — Adding one Available teacher to occurrence 2 from SF Lesson Detail with scope **“Only this”** assigns the teacher only to occurrence 2 and creates exactly one new Chatter post on that occurrence.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- today = 2026-06-23; a 3-occurrence recurring lesson is Published with dates 2026-06-30, 2026-07-07, and 2026-07-14 (all future dates)
- No Lesson Teachers are assigned to any occurrence
- Teacher "Tanaka Kenji" (working_status=Available, working_type=Full Time) exists in SF
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open occurrence 2 (2026-07-07) in SF Lesson Detail; record the Chatter post count for occurrences 1–3 | All occurrences are Published; baseline Chatter post counts are recorded | today=2026-06-23; occurrence_1=2026-06-30; occurrence_2=2026-07-07; occurrence_3=2026-07-14 |
| 2 | Navigate to the Teacher section and add "Tanaka Kenji" | The recurring-scope selector is displayed | working_status=Available; working_type=Full Time |
| 3 | Select **“Only this”** and save | "Tanaka Kenji" is assigned to occurrence 2 only | scope="Only this" |
| 4 | Verify teacher assignments and the Chatter section for occurrences 1–3 | Teacher is absent from occurrences 1 and 3; occurrence 2 has exactly 1 new post @mentioning "@Tanaka Kenji"; Chatter counts for occurrences 1 and 3 are unchanged | Only occurrence_2 is assigned and notified |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Publish – Teacher Added from SF Lesson Detail – Recurring lesson – “This and the following” – New Chatter post for each affected occurrence

**Description:** AC-01, BR-26 — State Transition — Adding one Available teacher to occurrence 2 from SF Lesson Detail with scope **“This and the following”** assigns the teacher to occurrences 2–3 and creates one new Chatter post on each affected future occurrence.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- today = 2026-06-23; a 3-occurrence recurring lesson is Published with dates 2026-06-30, 2026-07-07, and 2026-07-14 (all future dates)
- No Lesson Teachers are assigned to any occurrence
- Teacher "Yamamoto Yuki" (working_status=Available, working_type=Part Time) exists in SF
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open occurrence 2 (2026-07-07) in SF Lesson Detail; record the Chatter post count for occurrences 1–3 | All occurrences are Published; baseline Chatter post counts are recorded | occurrence_1=2026-06-30; occurrence_2=2026-07-07; occurrence_3=2026-07-14 |
| 2 | Navigate to the Teacher section and add "Yamamoto Yuki" | The recurring-scope selector is displayed | working_status=Available; working_type=Part Time |
| 3 | Select **“This and the following”** and save | "Yamamoto Yuki" is assigned to occurrences 2 and 3, but not occurrence 1 | scope="This and the following" |
| 4 | Verify teacher assignments and the Chatter section for occurrences 1–3 | Occurrence 1 has no new teacher or post; occurrences 2 and 3 each have exactly 1 new Chatter post @mentioning "@Yamamoto Yuki" | affected_occurrences=2,3 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Publish – Teacher Added – Available teacher added to Published past-date lesson – No Chatter post triggered

**Description:** AC-01, BR-26 — State Transition negative — Adding a teacher to a Published lesson whose date is in the past does not trigger a Chatter post.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- today = 2026-06-23; lesson_date = 2026-06-20 (3 days in the past)
- A lesson in Published status with lesson_date = 2026-06-20
- Teacher "Yamamoto Yuki" (working_status=Available, working_type=Part Time) exists in SF
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Published lesson (lesson_date = 2026-06-20) in SF Lesson Detail | Lesson status = Published; lesson_date = 2026-06-20; note current Chatter post count | today=2026-06-23; lesson_date=2026-06-20 (past) |
| 2 | Add "Yamamoto Yuki" as a Lesson Teacher | "Yamamoto Yuki" is added to the lesson | working_status=Available; working_type=Part Time |
| 3 | Navigate to the Chatter section | Chatter post count is unchanged — no new Chatter post created for a past-date lesson | lesson_date (2026-06-20) < today (2026-06-23) → no Chatter post |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Publish – Teacher Added – Published today's-date lesson – No Chatter post triggered

**Description:** AC-01, BR-26 — BVA — Boundary case: lesson_date = today does not trigger a Chatter post when a teacher is added.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- today = 2026-06-23; lesson_date = 2026-06-23 (today's date — exact boundary)
- A lesson in Published status with lesson_date = 2026-06-23 and no Lesson Teachers assigned
- Teacher "Nakamura Hana" (working_status=Available, working_type=Full Time) exists in SF
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Published lesson (lesson_date = 2026-06-23 = today) in SF Lesson Detail | Lesson status = Published; lesson_date = today | today=2026-06-23; lesson_date=2026-06-23 (boundary: lesson_date = today) |
| 2 | Note the current Chatter post count in the Chatter section | Baseline Chatter post count recorded | "" |
| 3 | Add "Nakamura Hana" as a Lesson Teacher | "Nakamura Hana" added to the lesson | working_status=Available; working_type=Full Time |
| 4 | Navigate to the Chatter section | Chatter post count is unchanged — no new Chatter post created for a today's-date lesson. | BVA: lesson_date = today (exact boundary) |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Publish – Teacher Added from SF Lesson Calendar – Recurring lesson – “Only this” – One new Chatter post triggered

**Description:** AC-01, BR-26 — State Transition — Adding one Available teacher to occurrence 2 from SF Lesson Calendar with scope **“Only this”** assigns the teacher only to occurrence 2 and creates exactly one new Chatter post on that occurrence.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- today = 2026-06-23; a 3-occurrence recurring lesson is Published with dates 2026-06-30, 2026-07-07, and 2026-07-14 (all future dates)
- No Lesson Teachers are assigned to any occurrence
- Teacher "Nakamura Hana" (working_status=Available, working_type=Full Time) exists in SF
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to the SF Lesson Calendar, locate occurrence 2 (2026-07-07), and record the Chatter post count for occurrences 1–3 | Calendar view shows all three Published future occurrences; baseline Chatter post counts are recorded | occurrence_1=2026-06-30; occurrence_2=2026-07-07; occurrence_3=2026-07-14 |
| 2 | Select occurrence 2, choose to edit, and add "Nakamura Hana" as a Lesson Teacher | The recurring-scope selector is displayed | working_status=Available; working_type=Full Time |
| 3 | Select **“Only this”** and save | "Nakamura Hana" is assigned to occurrence 2 only | scope="Only this" |
| 4 | Verify teacher assignments and the Chatter section for occurrences 1–3 | Teacher is absent from occurrences 1 and 3; occurrence 2 has exactly 1 new post @mentioning "@Nakamura Hana"; Chatter counts for occurrences 1 and 3 are unchanged | Only occurrence_2 is assigned and notified |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Publish – Teacher Added from SF Lesson Calendar – Recurring lesson – “This and the following” – New Chatter post for each affected occurrence

**Description:** AC-01, BR-26 — State Transition — Adding one Available teacher to occurrence 2 from SF Lesson Calendar with scope **“This and the following”** assigns the teacher to occurrences 2–3 and creates one new Chatter post on each affected future occurrence.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- today = 2026-06-23; a 3-occurrence recurring lesson is Published with dates 2026-06-30, 2026-07-07, and 2026-07-14 (all future dates)
- No Lesson Teachers are assigned to any occurrence
- Teacher "Yamamoto Yuki" (working_status=Available, working_type=Part Time) exists in SF
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to the SF Lesson Calendar, locate occurrence 2 (2026-07-07), and record the Chatter post count for occurrences 1–3 | Calendar view shows all three Published future occurrences; baseline Chatter post counts are recorded | occurrence_1=2026-06-30; occurrence_2=2026-07-07; occurrence_3=2026-07-14 |
| 2 | Select occurrence 2, choose to edit, and add "Yamamoto Yuki" as a Lesson Teacher | The recurring-scope selector is displayed | working_status=Available; working_type=Part Time |
| 3 | Select **“This and the following”** and save | "Yamamoto Yuki" is assigned to occurrences 2 and 3, but not occurrence 1 | scope="This and the following" |
| 4 | Verify teacher assignments and the Chatter section for occurrences 1–3 | Occurrence 1 has no new teacher or post; occurrences 2 and 3 each have exactly 1 new Chatter post @mentioning "@Yamamoto Yuki" | affected_occurrences=2,3 |

**Severity:** major
**Priority:** high

---
