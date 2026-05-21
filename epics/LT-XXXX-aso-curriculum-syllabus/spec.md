# Aso Curriculum and Syllubus

## 1. Target of this project

These are the target of Aso 2026 scope:

- Currently, Aso staff spend a significant amount of time manually managing curriculum, syllabus, and Grade (credit) information in Excel sheets.
- By storing that information in the Manabie system, make those activities easier:
  - Manage the data and make sure everything is always up-to-date.
  - Collect all necessary information in one system so that everybody can access them.
  - Achieve credit conversion (the most data-sensitive computation) operation efficiently and accurately.

---

## 2. Summary – Core Concepts

The main concepts (objects) of this project.

### 2.1 Curriculum

- Curriculum is a set of Curriculum Subjects that define the Curriculum Subject(s) that enrolled students in a given Academic Year and Location must take and gain credits to graduate.
- One curriculum is assigned to each student at the time of enrollment (when submitting the application).

### 2.2 Curriculum Subject

- Created for each curriculum and conceptually similar to the Course Master in Manabie.
- However, as of the 2026 development phase:
  - Curriculum Subject **will not** be linked to Course Master yet.
  - Curriculum Subject will be a record that each school staff can create at their discretion (to fit current local operations).

### 2.3 Syllabus Master and Syllabus Details

- For each Curriculum Subject, Syllabus Master includes:
  - Subject outline.
  - Details for each lesson session during the Academic Year.
- The project will use and refine the existing Syllabus features in Manabie.

### 2.4 Syllabus Report

- Similar to a Lesson Report:
  - Each teacher records what was actually taught in a lesson for each Syllabus Detail (lesson plan).
- Because Syllabus and Curriculum Subject are not yet linked to the course system:
  - For each lesson, the teacher must search for and specify:
    - Syllabus Master.
    - Syllabus Detail.
  - Then record the actual lesson content.

### 2.5 Study Goals and Evaluation Criteria

- Study Goals: TBD (Grade team).
- Evaluation Criteria: TBD (Grade team).
- They are separate child objects of Syllabus Master with 1:N relationship.

### 2.6 Credit Conversion

- Requirements to be defined (Grade team).
- Epic: [PBT-1739 – Curriculum Credit Management](https://manabie.atlassian.net/browse/PBT-1739)

---

## 3. Overview

### 3.1 Acceptance Criteria and Epics

Users’ permissions: for each object, users are separated into **edit** vs **view-only** via Permission Sets.

| Description | PBT/PRD | Team / PM |
| --- | --- | --- |
| **Curriculum**<br>- HQ Staff can create and edit Curriculum in SF.<br>- HQ Staff can duplicate a specific AY’s Curriculum in SF (2027 improvement). | - [PBT-1203 – Curriculum & Curriculum Subject](https://manabie.atlassian.net/browse/PBT-1203)<br>- [PBT-1791 – Duplicate Curricula (2027)](https://manabie.atlassian.net/browse/PBT-1791) | Grade – [Yanjun Wang](/people/712020:4a9b0122-35da-4560-a4f3-52d9fbdc3e03) |
| **Curriculum Subject & Syllabus**<br>- Staff and Teachers can CRU(D) Curriculum Subject and Syllabus on SF/BO.<br>- HQ Staff can confirm contents and update Syllabus status.<br>- HQ Staff can download Syllabus PDFs. | - [PBT-1745 – Syllabus Master and Syllabus Detail](https://manabie.atlassian.net/browse/PBT-1745)<br>- [PBT-1936 – Syllabus Approval Flow 2027](https://manabie.atlassian.net/browse/PBT-1936) | Scheduling – [Maria Nawatani](/people/61c3b17749f195006991f4e0)<br>Grade – [Yanjun Wang](/people/712020:4a9b0122-35da-4560-a4f3-52d9fbdc3e03) |
| **Syllabus Report**<br>- Teacher can search and select relevant Syllabus Master from Lesson Report on BO and edit Syllabus Report. | [PBT-1746 – Syllabus Report](https://manabie.atlassian.net/browse/PBT-1746) | Scheduling – [Maria Nawatani](/people/61c3b17749f195006991f4e0) |
| **Syllabus in App**<br>- Students can search for and view published Syllabus Master in the app.<br>- When submitting enrollment application, student must be linked to appropriate Curriculum. | [PBT-1296 – Syllabus in Learner App](https://manabie.atlassian.net/browse/PBT-1296) | Scheduling – [Maria Nawatani](/people/61c3b17749f195006991f4e0) |
| **Student Curriculum**<br>- When submitting an enrollment application, student must be linked to the appropriate Curriculum. | [PBT-1747 – Student Curriculum](https://manabie.atlassian.net/browse/PBT-1747) | Order – [John July Tacda](/people/61d2973cbce5e000691dd133) |
| **Credit Conversion**<br>- Staff can input each student’s grade and get computation result based on Evaluation Criteria. | [PBT-1739 – Curriculum Credit Management](https://manabie.atlassian.net/browse/PBT-1739) | Grade – [Yanjun Wang](/people/712020:4a9b0122-35da-4560-a4f3-52d9fbdc3e03) |

Full Jira list:  
https://manabie.atlassian.net/issues/?jql=key%20in%20%28PBT-1203%2C%20PBT-1791%2C%20PBT-1745%2C%20PBT-1936%2C%20PBT-1746%2C%20PBT-1296%2C%20PBT-1747%2C%20PBT-1739%29

### 3.2 Object relationship

- **Curriculum and Exam**  
  Miro diagram: https://miro.com/app/board/uXjVJT59qZQ=/?moveToWidget=3458764643100832850&cot=14

- **Curriculum and Syllabus**  
  Same Miro board: https://miro.com/app/board/uXjVJT59qZQ=/?moveToWidget=3458764643100832850&cot=14

High‑level from the diagram (image1):

- `Student` –(1:1)→ `Curriculum`
- `Curriculum` –(1:n)→ `Curriculum Subject`
- `Curriculum Subject` –(1:n)→ `Syllabus Master`
- `Syllabus Master` –(1:n)→ `Syllabus Detail`
- `Curriculum` –(1:n)→ `Master Exam Curriculum`
- `Curriculum Subject` –(1:n)→ `Exam`
- `Exam` –(1:n)→ `Exam Subject`
- `Syllabus Master` –(1:n)→ `Study Goals`
- `Curriculum Subject` –(1:n)→ `Evaluation Criteria (Judging Subject)`
- `Evaluation Criteria` –(1:1)→ `Exam Subject`

Example annotations from the diagram:

- Sample Curriculum Subject: 情報I  
- Linked Study Goals: “Webアプリケーションについての〇〇ができる” (etc.)  
- Linked Evaluation Criteria for that subject, with percentage = 40%.

### 3.3 User Flows

Miro: https://miro.com/app/board/uXjVJT59qZQ=/?moveToWidget=3458764642702185396&cot=14

### 3.4 Mockups

Miro: https://miro.com/app/board/uXjVJT59qZQ=/?moveToWidget=3458764642702185424&cot=14

### 3.5 Design

Figma:  
https://www.google.com/url?q=https://www.figma.com/design/tDGR2PZqkMYxG6LTVj4CaJ/Manabie-Curriculum?node-id%3D0-1%26p%3Df%26t%3DMDLTzzuz3EC5NlVR-0&sa=D&source=calendar&ust=1761973636977946&usg=AOvVaw3-LjJ6nz24G-HOgm3Kk0LB

---

## 4. User Stories

User stories are maintained in separate Confluence pages and Jira epics:

- PRD section:  
  https://manabie.atlassian.net/wiki/spaces/PrTi/pages/1308886088/Aso+Curriculum+and+Syllubus#User-Stories
- SF/BO Curriculum & Syllabus Detail:  
  https://manabie.atlassian.net/wiki/spaces/PrTi/pages/1544683574/SF+BO+Curriculum+and+Syllabus+Detail
- App Syllabus view:  
  https://manabie.atlassian.net/wiki/spaces/PrTi/pages/1515814976/App+Syllabus+view

---

## 5. Object Details

### 5.1 Curriculum

**Concept:**

- A Curriculum has **Location** and **Academic Year**.
- It can be assigned to a student who enrolled at a specific Location in a given Academic Year.
- In Aso, Location ≈ department / faculty / major.

**Examples:**

- Example 1: A student in the Computer Programming Course in the Department of Systems Engineering in 2025 has Curriculum A.
- Example 2: A student in the Computer Programming Course in the Department of Systems Engineering in 2026 has Curriculum B.
- Example 3: Students in the Advanced Systems Course in the Department of Systems Engineering in 2025 have Curriculum C.

**Assignment timing:**

- Curriculum is assigned at:
  - Enrollment application submission, or
  - Manually updated later.

**Open point:**

- **[TBU]** Grade Rank settings must be defined at the Curriculum level (Grade team).

#### 5.1.1 Curriculum – Field Definition

| Field Label      | JP          | Data Type                | Required | Description | Remarks |
| ---------------- | ----------- | ------------------------ | -------- | ----------- | ------- |
| Curriculum Name  | カリキュラム名 | Text                     | ☑️       |             |         |
| Enrollment Year  | 入学年度       | Picklist (Academic Year) | ☑️       |             |         |
| Location         | 拠点         | Picklist (Location)      | ☑️       |             |         |

---

### 5.2 Curriculum Subject

**Concept:**

- A student receives credit and certification **per Curriculum Subject**, based on their Curriculum.

**Link with Course Master:**

- Intended: Curriculum Subject ↔ Course Master.
- 2026 phase:
  - “Curriculum – Curriculum Subject – Syllabus Master” and “Course Master – Lesson” are managed **separately**.

#### 5.2.1 Curriculum Subject – Field Definition

| Field Label            | JP             | Data Type                 | Required | Description | Remarks |
| ---------------------- | -------------- | ------------------------- | -------- | ----------- | ------- |
| Curriculum Subject Name | 科目名          | Text                      | ☑️       |             |         |
| Curriculum             | カリキュラム      | Picklist (Curriculum)     | ☑️       |             |         |
| Mandatory              | 必須科目         | Boolean                   |          |             |         |
| Lesson Format          | 主な授業形態       | Picklist: Lecture / 講義; Exercise / 演習 |          |             |         |
| Target Grade           | 対象学年         | Picklist (Grade)          |          |             |         |
| Semester               | 実施時期         | Picklist: First Semester / 前期; Second Semester / 後期; Whole year / 通年 |          |             |         |
| Hour                   | 履修時間         | Numeric value            |          |             |         |
| Credit                 | 履修単位         | Numeric value            |          |             |         |

**Sample Curriculum Subject + Syllabus Master UI (from image2)**

For curriculum subject “Webプログラミング演習ⅢA”:

- Course Overview (科目概要):  
  > SpringフレームワークによるWebアプリシステム開発技術を習得する。
- iCDタスクコード:  
  > DV08.1.1, DV08.1.2, DV08.1.3, DV08.1.4, DV08.1.5, DV08.2.1, DV08.2.2, DV08.2.3, DV08.2.4
- 実施年度 (Academic Year): 2024年度  
- 実施時期 (Semester): 前期  
- 主な授業形態 (Lesson Format): 演習  
- 単位数 (Credit): 8単位  
- 時間数（内） (Hours): 120時間  
- 対象学科 (Target department/major): 情報システム専攻科システムエンジニア専攻アドバンスコース  
- 対象学年 (Target grade): 2学年  
- 担当者 (Lecturer): 川野 啓祐, 前園 勝栄, 村上 善代  
- 担当者実務経験 (Lecturer experience): (blank in screenshot)  
- テキスト・教材・参考図書 (Textbook etc.):  
  > Spring Framework超入門 やさしくわかるWebアプリ開発（技術評論社）  
- 履修上の注意 (Notes on taking courses):  
  > PCを利用する。

---

### 5.3 Syllabus Master

**Concept:**

- Registered for each Curriculum Subject.
- Reuses existing **Syllabus Master** object (Core).
- Aso links Syllabus Master to Curriculum Subject, not to Course Master.

#### 5.3.1 Syllabus Master – Field Definition

| Field Label         | JP                   | Data Type                   | Required | Description | Remarks |
| ------------------- | -------------------- | --------------------------- | -------- | ----------- | ------- |
| Syllabus Name       | シラバス名              | Text                        | ☑️       |             |         |
| Curriculum Subject  | 科目                   | Lookup (Curriculum Subject) | ☑️       |             | (original text said Picklist; PM confirmed Lookup) |
| Course Overview     | 科目概要                | Text (500)                  |          | Similar to course description. |         |
| iCD Task Code       | iCDタスクコード          | Text (255)                  |          | Custom field. Shown on public PDFs, not in app. | Not unique. |
| Academic Year       | 実施年度                | Picklist (Academic Year)    |          | When the lesson is scheduled to take place. |         |
| Lecturer            | 担当者                 | Text (255)                  |          | Free text, not linked to Staff. |         |
| Lecturer Experience | 担当者実務経験            | Text (255)                  |          | Free text, not linked to Staff. |         |
| Textbook            | テキスト・教材・参考図書       | Text (255)                  |          | e.g. `[Text Book Name][Publisher]`. |         |
| Notes on taking courses | 履修上の注意         | Text (255)                  |          | Similar to “Course Purpose”. |         |
| Status              | ステータス               | Picklist: Draft / Publish   | ☑️       | Default: Draft. Only “Draft” and “Publish” in 2026. | 2027: add approval flow – [PBT-1936](https://manabie.atlassian.net/browse/PBT-1936) |

---

### 5.4 Syllabus Detail

- Uses existing **Syllabus Detail** (Core). Only JP translation adjustments needed.

#### 5.4.1 Syllabus Detail – Field Definition

| Field Label    | JP        | Data Type | Required | Description | Remarks |
| -------------- | --------- | --------- | -------- | ----------- | ------- |
| Syllabus Name  | シラバス名   | Text     | ☑️       |             |         |
| Lesson Code    | 回数        | Numeric  | ☑️       | Used to match with lesson code in Lesson to define content per lesson. | Core field label “Syllabus Code” can be reused. |
| Topic          | 授業項目     | Text (255) |          | The context for each lesson. | JP translation should be fine-tuned. |
| Detail         | 詳細        | Text (255) |          | Further detail of lesson. | JP translation fine-tune. |
| Teaching Material | 教材     | Text (255) |          | Instructions / materials for additional study outside lesson. |         |

**Sample Syllabus Detail table (from image3)**

Teaching plan (授業計画（単元一覧）) for “Webプログラミング演習ⅢA”:

| 回数 (Lesson Code) | 授業項目・内容 (Topic / Content) |
| --- | --- |
| 1 | (1–4) 開発環境の構築、Java復習 |
| 2 | (5–8) Webのしくみ、オブジェクト指向復習 |
| 3 | (9–12) SpringFrameworkのコア機能(1) DIコンテナ |
| 4 | (13–16) SpringFrameworkのコア機能(2) アノテーション、AOP |
| 5 | (17–20) SpringFrameworkのコア機能(3) Initializr、MySQL設定 |
| 6 | (21–24) コア機能を利用した演習問題 |
| 7 | (25–27) MVCモデル |
| 8 | (28) MVCモデル確認テスト |
| 9 | (29–32) MVCモデルを利用した演習問題 |
| 10 | (33–36) テンプレートエンジン（1） |
| 11 | (37–40) テンプレートエンジン（2） |
| 12 | (41–44) リクエストパラメータの取得（1） |
| 13 | (45–48) リクエストパラメータの取得（2） |
| 14 | (49–52) 総合演習A(1) DBを利用したミニアプリ作成 |
| 15 | (53–56) 総合演習A(2) |
| 16 | (57) 総合演習A(3)、確認テスト |
| 17 | (58–60) 総合演習A |

Column “授業外学修指示” (extra study) is present but blank in this screenshot.

---

### 5.5 Study Goal

Relationship: Syllabus Master : Study Goals = 1 : N. One Study Goal is one row.

#### 5.5.1 Study Goal – Field Definition

| Field Label        | JP       | Data Type                 | Required | Description | Remarks |
| ------------------ | -------- | ------------------------- | -------- | ----------- | ------- |
| Syllabus Master    | シラバス    | Picklist (Syllabus Master) | ☑️       |             |         |
| Linguistic Information | 言語情報 | Checkbox                  |          |             |         |
| Intellectual Skills | 知的機能   | Checkbox                  |          |             |         |
| Physical Skills    | 運動技能    | Checkbox                  |          |             |         |
| Attitude and Motivation | 態度・意欲 | Checkbox              |          |             |         |
| Other              | その他     | Checkbox                  |          |             |         |
| Goal               | 目標      | Text                      |          |             |         |
| Sequence           | 順番      | Number                    | ☑️       | Display order. |         |

**Sample Study Goals table (from image4)**

Columns: 言語情報 / 知的技能 / 運動技能 / 態度・意欲 / その他 / 目標.

Sample rows (○ indicates checked category):

1.  
   - 知的技能: ○  
   - 目標:  
     > Webアプリケーションについての用語を説明できる。
2.  
   - 知的技能: ○  
   - 目標:  
     > Webアプリケーションの開発環境を作成することができる。
3.  
   - 知的技能: ○  
   - 目標:  
     > SpringMVCについて説明できる。
4.  
   - 知的技能: ○  
   - 目標:  
     > DIとAOPの仕組みを理解して、DBと連携したWebアプリケーションを作成することができる。

(Other category columns are empty for these rows.)

---

### 5.6 Evaluation Criteria (Judging Subject)

Relationship: Syllabus Master : Evaluation Criteria = 1 : N. Each criterion is one record.

#### 5.6.1 Evaluation Criteria – Field Definition

| Field Label            | JP       | Data Type                   | Required | Description | Remarks |
| ---------------------- | -------- | --------------------------- | -------- | ----------- | ------- |
| Syllabus Master        | シラバス    | Picklist (Syllabus Master)   | ☑️       |             |         |
| Linguistic Information | 言語情報   | Picklist: `-` / `〇` / `◎` |          |             |         |
| Intellectual Skills    | 知的機能   | Picklist: `-` / `〇` / `◎` |          |             |         |
| Physical Skills       | 運動技能    | Picklist: `-` / `〇` / `◎` |          |             |         |
| Attitude and Motivation | 態度・意欲 | Picklist: `-` / `〇` / `◎` |          |             |         |
| Other                 | その他     | Picklist: `-` / `〇` / `◎` |          |             |         |
| Ratio                 | 評価割合    | Numeric                    |          |             |         |
| Sequence              | 順番      | Number                     | ☑️       | Display order. |         |

**Sample Evaluation Criteria table (from image5)**

Header row: 評価方法 (Evaluation Method) + 言語情報 / 知的技能 / 運動技能 / 態度・意欲 / その他 / 評価割合.

Rows:

1. 定期試験（筆記）  
   - 知的技能: ◎  
   - 評価割合: 30%

2. 課題  
   - 知的技能: ◎  
   - 態度・意欲: ○  
   - 評価割合: 40%

3. 確認テスト  
   - 知的技能: ◎  
   - 評価割合: 20%

4. 受講状況  
   - 態度・意欲: ◎  
   - 評価割合: 10%

Below table (Curriculum subject explanation text – from image5):

> (1) 定期試験（筆記）を実施する。  
> (2) 課題を数回実施する。  
> (3) 確認テストを数回実施する。  
> (4) 受講状況を評価する。  
> 以上を下記の観点・割合で評価する。  
> 成績評価基準は、S（90点以上）・A（80点以上）・B（70点以上）・C（60点以上）・D（59点以下）とする。

This text belongs logically to Curriculum Subject / Evaluation Criteria explanation.

---

## 6. Appendix

### 6.1 PS Documents (JP only)

- Aso: 2026 要件まとめ (Google Doc – JP)  
  https://docs.google.com/document/d/109weLVjG_XiXD7chtEYh9DIkg1VXPeV_QGLbBjw_0-g/edit?tab=t.0#heading=h.1jtg9bk02ddc
- PS slide:  
  https://docs.google.com/presentation/d/1qzBwCo6R1Ux78W0exDHMNvj9SXtAMLR7/edit?slide=id.g2e2fab77ae4_1_216#slide=id.g2e2fab77ae4_1_216

### 6.2 Prerequisite knowledge

General definitions and characteristics of Curriculum vs Syllabus are unchanged from the original page (see Confluence):  
https://manabie.atlassian.net/wiki/spaces/PrTi/pages/1308886088/Aso+Curriculum+and+Syllubus

---

## 7. Attachments / References

- Original PRD page:  
  https://manabie.atlassian.net/wiki/spaces/PrTi/pages/1308886088/Aso+Curriculum+and+Syllubus
- Curriculum Structure (Grade team):  
  https://manabie.atlassian.net/wiki/spaces/PRDM/pages/1927413775/Curriculum+Structure+Curriculum+Curriculum+Subjects
- Aso ERP 2026 Launch timeline:  
  https://manabie.atlassian.net/wiki/spaces/PrTi/pages/1212317764/Aso-Juku+ERP+2026+Launch#Timeline
- Example diagram attachment:  
  https://manabie.atlassian.net/wiki/pages/viewpageattachments.action?pageId=1308886088&preview=%2F1308886088%2F1926922249%2Fimage-20251028-023438.png