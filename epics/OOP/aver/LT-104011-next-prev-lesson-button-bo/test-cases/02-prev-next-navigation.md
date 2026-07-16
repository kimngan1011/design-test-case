# Test Cases: LT-104011 - Add Next and Prev lesson button in BO

## Suite: [Aver] BO Lesson Detail Navigation - Previous and Next Transitions

### [Aver] Lesson Detail Navigation - Previous transition - Middle recurring lesson - Previous lesson detail opened in same tab

**Description:** AC 01.2 - State Transition - Clicking `Previous Lesson` from a middle recurring lesson opens the immediately previous lesson detail in the same browser tab.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff with access to Aver lesson detail.
- Recurring lesson chain RC-1001 exists with LES-1001, LES-1002, LES-1003 in order.
- LES-1002 detail page is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Lesson Detail for LES-1002. | Lesson Detail page for LES-1002 loads. | source_lesson = LES-1002 |
| 2 | Click `Previous Lesson`. | Navigation starts from LES-1002 without opening a new browser tab. | action = Previous Lesson |
| 3 | Wait for the destination lesson detail to load. | BO displays Lesson Detail for LES-1001, the immediately previous lesson in RC-1001. | destination_lesson = LES-1001 |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Detail Navigation - Next transition - Middle recurring lesson - Next lesson detail opened in same tab

**Description:** AC 01.2 - State Transition - Clicking `Next Lesson` from a middle recurring lesson opens the immediately next lesson detail in the same browser tab.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff with access to Aver lesson detail.
- Recurring lesson chain RC-1001 exists with LES-1001, LES-1002, LES-1003 in order.
- LES-1002 detail page is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Lesson Detail for LES-1002. | Lesson Detail page for LES-1002 loads. | source_lesson = LES-1002 |
| 2 | Click `Next Lesson`. | Navigation starts from LES-1002 without opening a new browser tab. | action = Next Lesson |
| 3 | Wait for the destination lesson detail to load. | BO displays Lesson Detail for LES-1003, the immediately next lesson in RC-1001. | destination_lesson = LES-1003 |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Detail Navigation - Same-tab behavior - Previous then browser back - Prior lesson detail restored consistently

**Description:** AC 01.2 - Regression - Same-tab lesson navigation integrates with browser back-stack and restores the prior lesson detail consistently.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff with access to Aver lesson detail.
- Recurring lesson chain RC-1001 exists with LES-1001, LES-1002, LES-1003 in order.
- LES-1002 detail page is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Click `Previous Lesson` from LES-1002. | BO opens Lesson Detail for LES-1001 in the same tab. | source_lesson = LES-1002; destination_lesson = LES-1001 |
| 2 | Use browser or in-app back navigation once. | BO returns to Lesson Detail for LES-1002. | navigation = back_once |
| 3 | Observe the restored page header and route. | The restored page still identifies LES-1002 and is usable without blank state or route mismatch. | expected_lesson = LES-1002 |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Detail Navigation - Rapid repeated click - Single transition intent - Destination context remains stable

**Description:** AC 01.2 edge - Negative - Rapid repeated interaction with one lesson-navigation control resolves to a stable destination context without duplicate tab or mixed-content behavior.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff with access to Aver lesson detail.
- Recurring lesson chain RC-1001 exists with LES-1001, LES-1002, LES-1003 in order.
- LES-1002 detail page is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | On LES-1002 detail page, trigger `Next Lesson` twice rapidly. | BO accepts the interaction without opening a second browser tab or showing an error overlay. | action = Next Lesson x2 |
| 2 | Wait for the navigation outcome to settle. | BO shows one stable destination lesson detail rather than mixed source and destination content. | stable_destination = single_lesson_detail |
| 3 | Inspect the final page identity. | The final page identifies one valid recurring lesson in RC-1001 and remains interactive. | expected_state = no_duplicate_or_blank |

**Severity:** major
**Priority:** high
