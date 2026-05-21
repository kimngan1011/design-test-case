# Syllabus PDF – Generate & Download

## 1. Overview

Aso wants to generate a PDF for the Syllabus information once they have registered (for every Academic Year).

- As HQ/Center Manager staff, I can generate and download a PDF from the Syllabus Master **detail page**.
- As HQ/Center Manager staff, I can generate and download PDFs of selected Syllabus Masters from the **list page**.

**Applicable user types:** HQ Staff, Center Manager (CM).  
**Not applicable:** Teacher Part-time, Teacher Full-time (no PDF download action in this epic).

**Reference:**
- PDF design and related objects: https://miro.com/app/board/uXjVJT59qZQ=/?moveToWidget=3458764643100832850&cot=14
- See more details: https://manabie.atlassian.net/wiki/spaces/PrTi/pages/1308886088/Aso+Curriculum+and+Syllubus

---

## 2. Permission & Access Control

### 2.1 Required Permission Sets

To use the PDF download feature, the user must have **both** of the following Permission Sets:

| Permission Set | Purpose |
| --- | --- |
| `Platform_View_Syllabus` | Allows the user to view Syllabus Master data |
| `Print_Aso_Syllabus_PDF` | Allows the user to perform the generate/download PDF action |

### 2.2 Behavior by Permission

| Scenario | Platform_View_Syllabus | Print_Aso_Syllabus_PDF | Result |
| --- | --- | --- | --- |
| Has both permissions | ✅ | ✅ | User sees the "Download" button and can click to generate/download PDF successfully |
| Missing Print permission | ✅ | ❌ | **Syllabus Master List page:** Download button is **not displayed**. **Syllabus Master Detail page:** Download button is **displayed but disabled** — clicking it shows the **"Insufficient Privileges"** error ("You do not have the level of access necessary to perform the operation you requested. Please contact the owner of the record or your administrator if access is necessary.") |
| Missing View permission | ❌ | ✅ or ❌ | User cannot access Syllabus Master data → cannot perform download |

---

## 3. User Flow – Download PDF

### 3.1 Method 1: Backoffice → Syllabus Master List → Select record → Download

1. User logs in to **Backoffice** successfully
2. Click **Lesson** on the Left Navigation Menu
3. Click **Syllabus Master** on the Left Navigation Menu
4. Access the Syllabus Master experience cloud (list page)
5. **Select** Syllabus Master record(s) from the list (tick checkbox)
6. Click the **"Download"** button
7. A draft PDF preview is displayed with 2 Japanese buttons:
   - **印刷** (Print)
   - **ダウンロード** (Download)
8. Click **ダウンロード** → the PDF file is downloaded to the local machine

### 3.2 Method 2: Backoffice → Syllabus Master List → Access record detail → Download

1. User logs in to **Backoffice** successfully
2. Click **Lesson** on the Left Navigation Menu
3. Click **Syllabus Master** on the Left Navigation Menu
4. Access the Syllabus Master experience cloud (list page)
5. Click on a Syllabus Master record to **access the detail page**
6. Click the **"Download"** button on the detail page
7. A draft PDF preview is displayed with 2 Japanese buttons:
   - **印刷** (Print)
   - **ダウンロード** (Download)
8. Click **ダウンロード** → the PDF file is downloaded to the local machine

### 3.3 Method 3: Salesforce → Syllabus Master Object → Select record → Download

1. User logs in to **Salesforce** successfully
2. Navigate to the **Syllabus Master** object
3. **Select** Syllabus Master record(s) from the list (tick checkbox)
4. Click the **"Download"** button
5. A draft PDF preview is displayed with 2 Japanese buttons:
   - **印刷** (Print)
   - **ダウンロード** (Download)
6. Click **ダウンロード** → the PDF file is downloaded to the local machine

### 3.4 Method 4: Salesforce → Syllabus Master Object → Access record detail → Download

1. User logs in to **Salesforce** successfully
2. Navigate to the **Syllabus Master** object
3. Click on a Syllabus Master record to **access the detail page**
4. Click the **"Download"** button on the detail page
5. A draft PDF preview is displayed with 2 Japanese buttons:
   - **印刷** (Print)
   - **ダウンロード** (Download)
6. Click **ダウンロード** → the PDF file is downloaded to the local machine

---

## 4. Functional Requirements

### 4.1 Download from Detail Page (Single PDF)

- If the user has the `Print_Aso_Syllabus_PDF` permission: display the **"Download"** button on the Syllabus Master detail page.
- Clicking "Download" → the system generates a PDF for that **single Syllabus Master**.
- A draft PDF preview is shown → the user selects **印刷** (Print) or **ダウンロード** (Download).

### 4.2 Download from List Page (Single or Bulk PDF)

#### 4.2.1 No records selected

- User does **not select** any record on the list → can still click the **"Download"** button.
- Result: Generates a PDF with **no field values**, only **field labels** in the PDF file with null/empty values.

#### 4.2.2 Select All on current page

- User can use **"Select All"** to select all records displayed on the current page.

#### 4.2.3 Multiple record selection (Bulk Generate)

- User can select **N** Syllabus Master records at once.
- **Upper bound limit: 200 records** maximum per generation.
- If more than 200 records are selected: the system must display a limit notification.

#### 4.2.4 Bulk Generate output

- The result is **a single PDF file** containing multiple sections.
- Each section contains the complete information of one Syllabus Master.
- Syllabus sections are placed consecutively in the PDF file (one after another).

### 4.3 Processing during PDF generation

- User **waits synchronously** on the screen — no background job / async processing.
- User should not navigate to another page while waiting.

### 4.4 Error Handling

| Scenario | Expected behavior |
| --- | --- |
| User missing `Print_Aso_Syllabus_PDF` permission, clicks Download on detail page | Display **"Insufficient Privileges"** error: "You do not have the level of access necessary to perform the operation you requested. Please contact the owner of the record or your administrator if access is necessary." |
| Entire job fails (bulk generate) | Display error message indicating PDF generation failure |
| Partial success (bulk generate — some records fail) | Must cover: display notification informing the user which records succeeded and which failed |
| More than 200 records selected | Display notification about the 200-record maximum limit |

---

## 5. PDF Content & Layout

### 5.1 General Rules

- All **field labels** on the PDF are always displayed in **Japanese** (JP).
- **Date format**: `YYYY/MM/DD` (Japanese standard — e.g., 2026/04/01).
- **Number format**: follows Japanese standard.
- Layout must be **stable** when printed on **A4** paper.
- **No special requirements** for logo or branding on the PDF (Aso is a partner, no such requirement).
- PDF format uses **fixed fields** — if a value exists, it is populated; if no value exists, it displays as **null/empty** (fields are never hidden on the PDF).

### 5.2 PDF Sections & Fields

The PDF contains the following sections, pulling data from related objects:

#### Section 1: Curriculum Subject (科目詳細 / かもくしょうさい)

Information from the **Curriculum Subject** record linked to the Syllabus Master.

| Field Label (JP) | Field Name | Data Type | Source Object |
| --- | --- | --- | --- |
| 科目名 | Curriculum Subject Name | Text | Curriculum Subject |
| カリキュラム | Curriculum | Picklist (Curriculum) | Curriculum Subject |
| 必須科目 | Mandatory | Boolean | Curriculum Subject |
| 主な授業形態 | Lesson Format | Picklist (Lecture / Exercise) | Curriculum Subject |
| 対象学年 | Target Grade | Picklist (Grade) | Curriculum Subject |
| 実施時期 | Semester | Picklist (First Semester / Second Semester / Whole year) | Curriculum Subject |
| 履修時間 | Hour | Numeric | Curriculum Subject |
| 履修単位 | Credit | Numeric | Curriculum Subject |

#### Section 2: Syllabus Master (シラバス情報)

Information from the **Syllabus Master** record.

| Field Label (JP) | Field Name | Data Type | Source Object |
| --- | --- | --- | --- |
| シラバス名 | Syllabus Name | Text | Syllabus Master |
| 科目概要 | Course Overview | Text (500) | Syllabus Master |
| iCDタスクコード | ICD Task Code | Text (255) | Syllabus Master |
| 実施年度 | Academic Year | Picklist | Syllabus Master |
| 実施時期 | Semester | (inherited from Curriculum Subject) | Curriculum Subject |
| 主な授業形態 | Lesson Format | (inherited from Curriculum Subject) | Curriculum Subject |
| 単位数 | Credit | Numeric | Curriculum Subject |
| 時間数 | Hour | Numeric | Curriculum Subject |
| 時間数（内） | Hour (internal) | Numeric | Curriculum Subject |
| 対象学科 | Target department/major | Text | Curriculum Subject |
| 対象学年 | Target Grade | Picklist | Curriculum Subject |
| 担当者 | Lecturer | Text (255) | Syllabus Master |
| 担当者実務経験 | Lecturer Experience | Text (255) | Syllabus Master |
| テキスト・教材・参考図書 | Textbook | Text (255) | Syllabus Master |
| 履修上の注意 | Notes on taking courses | Text (255) | Syllabus Master |
| ステータス | Status | Picklist (Draft / Publish) | Syllabus Master |

#### Section 3: Study Goals (到達目標)

Table displaying the list of **Study Goals** (child records of Syllabus Master), sorted by the `Sequence` (順番) field.

| Column (JP) | Field Name | Data Type |
| --- | --- | --- |
| 言語情報 | Linguistic Information | Checkbox (○ if checked) |
| 知的技能 | Intellectual Skills | Checkbox (○ if checked) |
| 運動技能 | Physical Skills | Checkbox (○ if checked) |
| 態度・意欲 | Attitude and Motivation | Checkbox (○ if checked) |
| その他 | Other | Checkbox (○ if checked) |
| 目標 | Goal | Text |

#### Section 4: Syllabus Detail / Teaching Plan (授業計画（単元一覧）)

Table displaying the list of **Syllabus Detail** (child records of Syllabus Master), sorted by the `Lesson Code` (回数) field.

| Column (JP) | Field Name | Data Type |
| --- | --- | --- |
| 回数 | Lesson Code | Numeric |
| 授業項目・内容 | Topic | Text (255) |
| 授業外学修指示 | Teaching Material | Text (255) |

#### Section 5: Evaluation Criteria (評価方法)

Table displaying the list of **Evaluation Criteria / Judging Subject** (child records of Syllabus Master), sorted by the `Sequence` (順番) field.

| Column (JP) | Field Name | Data Type |
| --- | --- | --- |
| (Row header — evaluation method name) | — | Text |
| 言語情報 | Linguistic Information | Picklist (−/〇/◎) |
| 知的技能 | Intellectual Skills | Picklist (−/〇/◎) |
| 運動技能 | Physical Skills | Picklist (−/〇/◎) |
| 態度・意欲 | Attitude and Motivation | Picklist (−/〇/◎) |
| その他 | Other | Picklist (−/〇/◎) |
| 評価割合 | Ratio | Numeric (%) |

#### Section 6: Curriculum Subject Explanation (成績評価基準)

Detailed text explaining the evaluation methodology, placed at the end of the PDF. This content belongs to the Curriculum Subject.

### 5.3 PDF Preview Buttons

When the PDF is generated, a draft PDF is displayed with 2 buttons:

| Button (JP) | Function |
| --- | --- |
| **印刷** | Print directly |
| **ダウンロード** | Download the PDF file to the local machine |

---

## 6. Data Validation on PDF

The data displayed on the PDF must be verified to be **accurate** compared to the data in the system:

### 6.1 Field-level Data Accuracy

| Check | Description |
| --- | --- |
| Curriculum Subject fields | All fields from Curriculum Subject display correct values on the PDF |
| Syllabus Master fields | All fields from Syllabus Master display correct values on the PDF |
| Study Goals | Correct number of rows, ordered by Sequence, checkbox marks (○) are correct, Goal text is correct |
| Syllabus Detail | Correct number of rows, ordered by Lesson Code, Topic and Teaching Material text are correct |
| Evaluation Criteria | Correct number of rows, ordered by Sequence, marks (−/〇/◎) are correct, Ratio (%) is correct |
| Curriculum Subject Explanation | Evaluation methodology explanation text is displayed fully and accurately |

### 6.2 Format & Display Rules

| Check | Description |
| --- | --- |
| Japanese field labels | All field labels on the PDF are always displayed in Japanese, regardless of user language |
| Date format | Must follow `YYYY/MM/DD` format |
| Number format | Must follow Japanese standard |
| Null/Empty value | If a field has no value → displayed as blank (field still appears on PDF, never hidden) |
| Checkbox display | Study Goals: ○ for checked, blank for unchecked |
| Picklist display (Evaluation Criteria) | Must display correct symbols: −, 〇, ◎ |

### 6.3 Bulk PDF Data Accuracy

| Check | Description |
| --- | --- |
| Correct number of sections | Number of sections in the PDF = number of selected records |
| No data mixing | Each section contains data only from its corresponding Syllabus Master, no cross-contamination between records |
| Section order | Sections are arranged in the correct order matching the selected records |

---

## 7. Constraints & Non-functional Requirements

| Item | Requirement |
| --- | --- |
| Max bulk selection | 200 records |
| PDF page size | A4 — layout must be stable when printed |
| Processing mode | Synchronous — user waits on the screen |
| Language on PDF | Japanese (JP) for all field labels |
| Branding | No special logo/branding requirement |
| Date format | YYYY/MM/DD |
| Field visibility | Fixed — all fields are always displayed; populated if value exists, null/empty otherwise |

---

## 8. Related Objects (Entity Relationship)

```
Curriculum (1) → (n) Curriculum Subject (1) → (1) Syllabus Master
                                                      ├── (1:n) Syllabus Detail
                                                      ├── (1:n) Study Goals
                                                      └── (1:n) Evaluation Criteria (Judging Subject)
```

All data from the objects above is aggregated into the PDF.

---

## 9. Related Links

- Miro (PDF design and objects): https://miro.com/app/board/uXjVJT59qZQ=/?moveToWidget=3458764643100832850&cot=14
- Confluence (Aso Curriculum and Syllabus): https://manabie.atlassian.net/wiki/spaces/PrTi/pages/1308886088/Aso+Curriculum+and+Syllubus
- Epic PBT-1745: https://manabie.atlassian.net/browse/PBT-1745
- Epic PBT-1936 (2027 Approval Flow): https://manabie.atlassian.net/browse/PBT-1936 