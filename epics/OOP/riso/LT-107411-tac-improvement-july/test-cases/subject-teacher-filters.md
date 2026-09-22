# Test Cases: LT-107411 — Subject & Teacher Filters

## Suite: [Riso] TAC — Subject & Teacher Filters

### [Riso] TAC – Subject Filter – Empty search – No suggestions shown
**Description:** AC 01 — Decision Table — Empty Subject search does not imply a partial catalog.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens the Subject filter. | The Subject search input opens with no subject suggestions. | search_term = "" |
**Severity:** minor
**Priority:** medium

### [Riso] TAC – Subject Filter – Matching text – Matching subject selectable
**Description:** AC 01 — Equivalence Partitioning — A matching Subject remains searchable and selectable.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- Subject `Mathematics` exists.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `Math` in the Subject filter. | `Mathematics` is shown as a matching result. | search_term = Math |
| 2 | HQ or CM Staff selects `Mathematics`. | The Subject filter shows `Mathematics` as selected. | subject = Mathematics |
**Severity:** major
**Priority:** high

### [Riso] TAC – Subject Filter – Unmatched text – No subject selected
**Description:** AC 01 — Negative — An unmatched Subject search does not select stale data.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `NoSuchSubject` in the Subject filter. | No matching Subject is shown or selected. | search_term = NoSuchSubject |
**Severity:** minor
**Priority:** medium

### [Riso] TAC – Teacher Filter – Teacher Name – Matching teacher shown
**Description:** AC 02 — Equivalence Partitioning — Teacher Name is searchable.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- Teacher `Yamada Taro` exists.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `Yamada` in the Teacher filter. | `Yamada Taro` is shown as a matching teacher. | teacher_name = Yamada Taro |
**Severity:** major
**Priority:** high

### [Riso] TAC – Teacher Filter – Phonetic Name – Matching teacher shown
**Description:** AC 02 — Equivalence Partitioning — Phonetic Name is searchable.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- Teacher `Yamada Taro` has Phonetic Name `ヤマダ タロウ`.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `ヤマダ` in the Teacher filter. | `Yamada Taro` is shown as a matching teacher. | phonetic_name = ヤマダ タロウ |
**Severity:** major
**Priority:** high

### [Riso] TAC – Teacher Filter – External User ID – Matching teacher shown
**Description:** AC 02 — Equivalence Partitioning — External User ID is searchable.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- Teacher `Yamada Taro` has External User ID `T-1001`.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `T-1001` in the Teacher filter. | `Yamada Taro` is shown as a matching teacher. | external_user_id = T-1001 |
**Severity:** major
**Priority:** high

### [Riso] TAC – Teacher Filter – English locale – Placeholder shown
**Description:** AC 02 — Component — English placeholder matches the PBT text.
**Preconditions:**
- HQ or CM Staff is logged in with English locale.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens the Teacher filter. | The placeholder shows `Search Teacher Name, External User ID`. | locale = en |
**Severity:** minor
**Priority:** medium

### [Riso] TAC – Teacher Filter – Japanese locale – Placeholder shown
**Description:** AC 02 — Component — Japanese placeholder matches the PBT text.
**Preconditions:**
- HQ or CM Staff is logged in with Japanese locale.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens the Teacher filter. | The placeholder shows `講師名、外部IDで検索`. | locale = ja |
**Severity:** minor
**Priority:** medium
