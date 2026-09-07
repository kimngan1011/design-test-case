# Test Cases: LT-94105 — Riso Location Closed Date and Holiday

## Suite: Learner Calendar Holiday Display

### [Riso] Learner Calendar – Date states – Regular week – Required colors and Closed Date pattern render

**Description:** AC 01.3 — Component — Confirms all independently specified calendar date treatments render from populated Riso data.

**Preconditions:**
- Logged in as a Riso student enrolled at Riso Center A.
- today = `2026-07-01`; the July 2026 ACI has Holiday `2026-07-05`, Closed Date `2026-07-06`, and no special type on Saturday `2026-07-04` or Sunday `2026-07-12`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Learner Calendar for July 2026. | The month contains dates `2026-07-04`, `2026-07-05`, `2026-07-06`, and `2026-07-12`. | today = 2026-07-01; month = 2026-07 |
| 2 | View Saturday `2026-07-04` and Sunday `2026-07-12`. | Saturday date text is blue; Sunday date text is `#295ACB`. | Saturday = 2026-07-04; Sunday = 2026-07-12 |
| 3 | View Holiday `2026-07-05` and Closed Date `2026-07-06`. | Holiday date text is `#295ACB`; Closed Date is gray and has diagonal lines. | Holiday = 2026-07-05; Closed Date = 2026-07-06 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Learner Calendar – Selected state – Closed Date selected – Light-blue background retains diagonal lines

**Description:** AC 01.3 — Component — Confirms the selected Closed Date combines both specified visual treatments.

**Preconditions:**
- Logged in as a Riso student enrolled at Riso Center A.
- today = `2026-07-01`; `2026-07-06` is a Closed Date in the learner's current-AY ACI.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open July 2026 in the Learner Calendar. | `2026-07-06` is gray with diagonal lines before selection. | target_date = 2026-07-06 |
| 2 | Select `2026-07-06`. | The date cell background becomes `#DEEBFF`. | selected_date = 2026-07-06 |
| 3 | Inspect the selected date cell. | Diagonal lines remain visible on the `#DEEBFF` selected Closed Date cell. | expected state = selected + closed date |

**Severity:** minor
**Priority:** medium

---

### [Riso] Learner Calendar – Today state – Closed Date today – Today circle overlays the Closed Date cell

**Description:** AC 01.3 — Decision Table — Confirms the documented Today precedence on a Closed Date.

**Preconditions:**
- Logged in as a Riso student enrolled at Riso Center A.
- today = `2026-07-06`; `2026-07-06` is a Closed Date in the current-AY ACI.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Learner Calendar for July 2026. | `2026-07-06` is identified as today and as a Closed Date. | today = 2026-07-06; target_date = 2026-07-06 |
| 2 | Inspect the `2026-07-06` date cell. | The date text is bold white within a `#395AD2` circle. | expected today token = #395AD2 |
| 3 | Inspect the Closed Date treatment beneath the Today state. | The Today state is displayed on the Closed Date cell rather than hiding the date. | expected precedence = Today on Closed Date |

**Severity:** minor
**Priority:** medium

---

### [Riso] Learner Calendar – Today state – Selected today – Today circle overlays selected treatment

**Description:** AC 01.3 — Decision Table — Confirms the documented Today precedence on a selected date.

**Preconditions:**
- Logged in as a Riso student enrolled at Riso Center A.
- today = `2026-07-07`; no Closed Date is configured for that date.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open July 2026 and select `2026-07-07`. | The date is selected and is today. | today = 2026-07-07; selected_date = 2026-07-07 |
| 2 | Inspect the date cell. | The date text is bold white within a `#395AD2` circle. | expected today token = #395AD2 |
| 3 | Navigate away and return to July 2026. | The Calendar continues to identify `2026-07-07` as today. | month = 2026-07 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Learner Calendar – Day detail – Holiday selected – Japanese label is shown next to the date

**Description:** AC 01.3 — Component — Confirms the Holiday-only detail label uses the exact required Japanese text.

**Preconditions:**
- Logged in as a Riso student enrolled at Riso Center A.
- today = `2026-07-01`; `2026-07-05` is Holiday in the learner's current-AY ACI.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open July 2026 and select `2026-07-05`. | The Holiday date is selected. | target_date = 2026-07-05; Type = Holiday |
| 2 | Open the day detail section. | The date text is followed by `祝日`. | expected label = 祝日 |
| 3 | Read the visible label. | The label is exactly `祝日`; no `Closed Date` label replaces it. | exact text = 祝日 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Learner Calendar – Day detail – Closed Date selected – Existing body content remains unchanged

**Description:** AC 01.3 — Regression — Confirms the Holiday feature does not alter the existing Closed Date detail content.

**Preconditions:**
- Logged in as a Riso student enrolled at Riso Center A.
- today = `2026-07-01`; `2026-07-06` is Closed Date named `Center maintenance`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open July 2026 and select `2026-07-06`. | The Closed Date is selected. | target_date = 2026-07-06; Type = Closed Date |
| 2 | Open the day detail section. | The body shows the existing Closed Date name `Center maintenance`. | expected body name = Center maintenance |
| 3 | Inspect text next to the date. | The Holiday-only label `祝日` is absent. | expected label = absent |

**Severity:** minor
**Priority:** medium

---

### [Riso] Learner Calendar – Location and academic year – Contrasting records – Enrolled location Type is used

**Description:** AC 01.3 — Decision Table / Regression — Confirms the lookup uses the enrolled learner's location and current academic year.

**Preconditions:**
- Logged in as a learner enrolled at Riso Center A.
- today = `2026-07-01`; Center A 2026 has Holiday `2026-07-08`; Center B 2026 has Closed Date `2026-07-08`; Center A 2025 has Closed Date `2026-07-08`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open July 2026 in the Learner Calendar. | `2026-07-08` is rendered as Holiday. | enrolled location = Center A; current AY = 2026 |
| 2 | Open day detail for `2026-07-08`. | The date detail contains `祝日`. | expected Type source = Center A 2026 Holiday |
| 3 | Compare the configured control records. | Center B and Center A 2025 Closed Date records do not change Center A 2026's result. | control Types = Closed Date |

**Severity:** major
**Priority:** high

---

### [Riso] Learner Calendar – Timezone boundary – JST date differs from UTC date – Holiday is resolved by JST

**Description:** AC 01.3 — Boundary / Regression — Confirms date classification follows the business date at the JST–UTC boundary.

**Preconditions:**
- Logged in as a Riso student enrolled at Riso Center A.
- today (JST) = `2026-07-10 00:30 Asia/Tokyo`; today (UTC) = `2026-07-09 15:30 UTC`; Center A 2026 has Holiday `2026-07-10` only.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Learner Calendar with the stated device/session clocks. | The Calendar opens using business date `2026-07-10`. | JST = 2026-07-10 00:30; UTC = 2026-07-09 15:30 |
| 2 | Inspect `2026-07-10`. | The date is rendered as Holiday with `#295ACB` text. | target_date = 2026-07-10; Type = Holiday |
| 3 | Open day detail for `2026-07-10`. | The detail contains `祝日`, not the `2026-07-09` data. | expected label = 祝日 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Learner Calendar – Day rollover – Holiday after midnight – Calendar refreshes to the new JST date

**Description:** AC 01.3 — State Transition — Confirms a calendar left open across midnight reads the next JST date and its Type.

**Preconditions:**
- Logged in as a Riso student enrolled at Riso Center A.
- device time transitions from `2026-07-09 23:58 Asia/Tokyo` to `2026-07-10 00:01 Asia/Tokyo`; Center A has Holiday `2026-07-10`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Learner Calendar at `2026-07-09 23:58 JST`. | The Calendar identifies `2026-07-09` as today. | before = 2026-07-09 23:58 JST |
| 2 | Keep the Calendar open until `2026-07-10 00:01 JST` and refresh it. | The Calendar identifies `2026-07-10` as today. | after = 2026-07-10 00:01 JST |
| 3 | Inspect `2026-07-10`. | The Holiday treatment is shown for the new JST date. | target_date = 2026-07-10; Type = Holiday |

**Severity:** minor
**Priority:** medium
