# LT-107175 — Test Coverage

Source of truth: [spec.md](spec.md)  
Prepared: 2026-08-17  
Scope: Renseikai — Remote attendance status and response across SF, BO, Calendar, Learner App, and existing attendance notifications.

## 1. Business Rules Extracted

| BR ID | AC | Business rule | Logic type |
|---|---|---|---|
| BR-01 | 01.1 | `Attendance_Status__c = Remote` is the Calendar source of truth; a staff-set Remote status must show as Remote. | State / data integrity |
| BR-02 | 01.1 | In group Calendar views, Remote shows a Remote indicator using the defined priority over other indicators. | Conditional display |
| BR-03 | 01.1 | In individual Calendar views, Remote shows a Remote indicator using the defined priority over other indicators. | Conditional display |
| BR-04 | 01.1 | Indicator precedence is `Remote > New > Trial > Seasonal > Reallocated > Absent`. | Ordering / Sort |
| BR-05 | 01.2 | When no relevant Remote status is present, no Remote dot is shown and existing indicators remain unchanged. | Conditional display / regression |
| BR-06 | 01.3 | A Remote tag displays beside the learner name in Calendar lesson detail. | Display completeness |
| BR-07 | 01.4 | Calendar legend includes the localized Remote label and defined Indigo/40 visual token. | Display completeness / exact text |
| BR-08 | 01.5 | Salesforce lesson detail displays and allows the localized `Remote` attendance status. | Display completeness / state update |
| BR-09 | 01.6 | BO lesson detail displays and allows the localized `Remote` attendance status. | Display completeness / state update |
| BR-10 | 01.7 | Learner App displays the Remote attendance value defined by the PRD. | Display completeness |
| BR-11 | 02.1 | Salesforce displays `Attendance_Response__c = Attended Remotely` as `Option (Remark)`. | Display completeness / data mapping |
| BR-12 | 02.2 | BO displays `Attendance_Response__c = Attended Remotely` as `Option (Remark)`. | Display completeness / data mapping |
| BR-13 | 03.1 | Every BO Collect Attendance entry point offers the exact option `Remote`; existing Draft-disabled behavior remains unchanged. | Display completeness / regression |
| BR-14 | 03.2 | BO saving `Remote` persists `Attendance_Status__c = Remote` and survives reread/reopen. | State / data integrity |
| BR-15 | 04.1 | Learner App offers `Attended Remotely`; existing Student/Parent audience and Published/upcoming eligibility rules do not change. | Display completeness / permissions |
| BR-16 | 04.2 | App submission persists `Attendance_Response__c = Attended Remotely`; the latest valid update wins. | State / data integrity / concurrency |
| BR-17 | 04.3 | Remote attendance uses the established attendance-notification behavior documented in Qase PX suite 3276. | Cross-system / notification routing |
| BR-18 | 05.1 | A valid App remote submission automatically sets the corresponding attendance status to `Remote` and is reflected in SF/BO/Calendar/App. | Cross-system synchronization |
| BR-19 | 03.2 | When a user directly selects Remote in BO, Attendance Reason is shown and can be selected before saving. Attendance Notice visibility and stored-value clearing are not implied. | Display completeness / state transition |

## 2. Logic-Type Categorization

| Logic type | Applicable rules | Why |
|---|---|---|
| Conditional display | BR-02, BR-03, BR-05 | Remote coexists with other learner flags and is absent when no relevant Remote status is present. |
| Ordering / Sort | BR-04 | The Calendar has an explicit indicator-precedence rule. |
| Display completeness / exact text | BR-06–BR-13, BR-15, BR-19 | Multiple screens must expose the newly introduced values and labels, including the confirmed BO Attendance Reason selector. |
| State / data integrity | BR-01, BR-08, BR-09, BR-14, BR-16, BR-19 | Status/response values are written by several entry points and must remain internally consistent. |
| Permissions / eligibility | BR-15 | No new permissions are intended; existing Student/Parent configuration remains controlling. |
| Concurrency / latest-write behavior | BR-16 | Product decision is that the latest valid update wins. |
| Cross-system synchronization | BR-17, BR-18 | An App write affects Student Session data, consumer surfaces, and notifications. |
| Regression / unchanged behavior | BR-05, BR-13, BR-15 | Existing indicators, Draft guard, and App audience/eligibility must not change. |

## 3. Technique Selection

| Logic type | Selected techniques | Application |
|---|---|---|
| Conditional display | Decision table, pairwise combinations | Remote together with each competing learner indicator in group and individual layouts. |
| Ordering / Sort | Scenario matrix with two or more learners having different indicator keys | Assert the relative precedence, not only a single Remote state. |
| Display completeness / exact text | UI field inventory, localization assertions, state-based display checks | Assert every required label, value, tag, dot, legend, and Collect Attendance choice. |
| State / data integrity | Transition coverage, round-trip persistence, negative persistence checks | Write status/response from each producer then reread from independent consumers. |
| Permissions / eligibility | Role/audience matrix, eligibility regression scenarios | Cover staff access and existing Student/Parent configuration combinations. |
| Concurrency / latest-write behavior | Rapid-repeat and competing-update scenarios | Establish a final value after ordered valid submissions. |
| Cross-system synchronization | Downstream-effect inventory, producer/consumer readback matrix | Confirm matching Student Session status/response and notifications after App submission. |
| Regression / unchanged behavior | Focused regression scenarios | Exercise the existing indicator, Draft, and eligibility controls alongside Remote. |

## 4. Structured Coverage Strategy

| AC | Logic type | Coverage target and technique | Risk | Depth | Expected evidence |
|---|---|---|---:|---|---|
| 01.1 | State / data integrity; Conditional display; Display completeness | Set `Attendance_Status__c` to Remote manually in staff surfaces; verify Student Session persistence and both group and individual Calendar indicators. Use decision table with Remote and each competing indicator. | High | Deep | Stored status is Remote; Calendar selects Remote for both view modes. |
| 01.1 | Ordering / Sort | Create at least two learners with differing indicator keys and assert `Remote > New > Trial > Seasonal > Reallocated > Absent`. | High | Deep | Remote is selected whenever present; each non-Remote priority remains correct when Remote is absent. |
| 01.2 | Display completeness; Regression | Create lessons with no Remote status but existing New, Trial, Seasonal, Reallocated, or Absent indicators; assert no Remote dot is shown and the applicable existing indicator remains. | High | Deep | No false Remote dot is created; established indicator behavior is unchanged. |
| 01.3 | Display completeness | Inspect lesson-detail learner rows for the Remote tag beside the correct learner name; include a mixed Remote/non-Remote roster. | Medium | Standard | Tag is visible only for the correct Remote learner and is not duplicated. |
| 01.4 | Display completeness / exact text | Assert the Calendar legend contains `Remote` / `リモート参加` as applicable and uses Vibrant/Indigo/40. | Medium | Standard | Legend text and visual token match the PRD. |
| 01.5 | Display completeness; State update | Verify SF Lesson Detail status field and available choice; set and reread Remote. Apply all-staff-user update/view matrix. | High | Deep | Localized Remote is selectable, saved, and shown on reread. |
| 01.6 | Display completeness; State update | Verify BO Lesson Detail status field and available choice; set and reread Remote. Apply all-staff-user update/view matrix. | High | Deep | Localized Remote is selectable, saved, and shown on reread. |
| 01.7 | Display completeness | Verify the Learner App presents Remote using the PRD-defined value, after staff-set and App-set Remote. | Medium | Standard | App shows the current Remote status without introducing an alternative label. |
| 02.1 | Display completeness; Data mapping | Seed or submit `Attendance_Response__c = Attended Remotely` and verify SF renders it as `Option (Remark)`. | Medium | Standard | Value and remark format are correctly mapped. |
| 02.2 | Display completeness; Data mapping | Seed or submit `Attendance_Response__c = Attended Remotely` and verify BO renders it as `Option (Remark)`. | Medium | Standard | Value and remark format are correctly mapped. |
| 03.1 | Display completeness | Verify the exact option `Remote` in all BO Collect Attendance entry points: Lesson Detail, Report, Lesson Report Detail, and Calendar Bulk Update Attendance. | High | Deep | Each entry point exposes Remote and can select it. |
| 03.1 | Regression / disabled state | Verify the existing Draft-disabled guard remains in every applicable BO Collect Attendance entry point. | High | Deep | Remote does not bypass existing Draft restrictions. |
| 03.2 | State / data integrity | Save Remote from each BO entry point, reopen/read from a different BO surface and Calendar, and confirm status remains Remote. | High | Deep | Round-trip persistence and downstream readback agree. |
| 03.2 | Display completeness; State transition | In every BO Collect Attendance entry point, select Remote and assert Attendance Reason is shown; choose an existing reason and save. Do not assert Attendance Notice visibility or stored-value clearing. | High | Deep | Attendance Reason is selectable before save, and the saved Remote status plus selected reason are available on reread. |
| 04.1 | Display completeness; Permissions / eligibility | Verify the App option `Attended Remotely` for existing eligible Student and Parent audiences, and absence for existing ineligible/unpublished/non-upcoming conditions according to unchanged baseline rules. | High | Deep | New option follows existing audience and eligibility controls; no new configuration is required. |
| 04.2 | State / data integrity; Cross-system synchronization | Submit `Attended Remotely`, inspect persisted response as `Option (Remark)` in SF/BO, and verify status/response belong to the same Student Session. | Critical | Deep | Correct session receives response; no cross-learner or partial data update. |
| 04.2 | Concurrency / latest-write behavior | Use rapid repeat submission and conflicting valid updates in sequence; assert the latest valid value is the final persisted value across readers. | Critical | Deep | Latest valid write wins and views converge; no duplicate/partial state. |
| 04.2 | State / data integrity; Identity isolation | On one shared device, switch from Student A to Student B in the same lesson; separately repeat with one parent switching selected learners. Submit different values and assert each Student Session stores only its own response and resulting status. | Critical | Deep | Student A and Student B retain their distinct response/status values; no value crosses to the other learner. |
| 04.3 | Display completeness; Cross-system / notification routing | Reuse Qase PX suite 3276 notification routing expectations for Remote: Notification Center and SF Chatter; teacher delivery independent of CM location; Centre Manager routing by lesson location, the Location's Brand, and CM affiliation. | High | Deep | Remote notification recipients/channels follow established attendance-notification behavior. |
| 05.1 | Cross-system synchronization | Submit App `Attended Remotely`, then read status in SF, BO, Calendar group/individual/detail, and Learner App. Repeat after changing from another attendance state and after a newer valid update. | Critical | Deep | App submission automatically produces Remote status and all consumer surfaces converge on the latest value. |
| 05.1 | Display completeness; State transition | After App submission produces Remote, open the relevant Collect Attendance display and assert Attendance Notice and Attendance Reason are not shown. Do not assert that any stored value is cleared. | High | Deep | Both fields are absent from the UI for this Remote state; test remains limited to the PdM-confirmed visibility contract. |

### Coverage-depth definitions

- **Deep:** positive and negative paths, state transition/readback, relevant role or configuration variants, and downstream effects.
- **Standard:** positive and representative negative/state variations on each distinct UI surface.

## 5. High-Risk Areas

| Risk | Level | Failure impact | Mitigation coverage |
|---|---:|---|---|
| App submission writes response and automatically changes attendance status across systems. | Critical | Student Session can show a response/status mismatch or stale Calendar/App data. | AC 04.2, 05.1 persistence, cross-surface readback, latest-write and partial-update checks. |
| Latest-valid-value rule under rapid or competing updates. | Critical | A prior submission may overwrite a newer decision or leave surfaces inconsistent. | AC 04.2 concurrency scenarios and final-state readback. |
| Shared-device or parent learner switch. | Critical | Attendance for one student can be written to another student's Student Session. | AC 04.2 Student/Parent identity-isolation scenarios. |
| Calendar indicator precedence. | High | Remote could be obscured by another badge or an incorrect learner indicator shown. | AC 01.1 priority decision table with multiple learners/statuses. |
| BO Collect Attendance across all entry points. | High | A path may omit Remote, fail to save it, or inadvertently enable Draft changes. | AC 03.1–03.2 entry-point matrix and Draft regression. |
| Notification recipient routing. | High | Teachers/Centre Managers may miss attendance updates or unintended users receive them. | AC 04.3 reuse of PX 3276 location, Location-Brand, affiliation, and channel variants. |
| Existing App audience/eligibility behavior. | High | New option could be exposed to unauthorized or ineligible audiences. | AC 04.1 baseline audience and Published/upcoming regression. |
| BO Remote dependent-field availability. | High | Staff could be unable to select an Attendance Reason after selecting Remote in BO. | AC 03.2 selector, save, and reread coverage. |

## F. Mandatory Edge-Case Assessment

| Area | Applicability | Coverage decision |
|---|---|---|
| A. Configurable thresholds / limits | N/A | No new numeric or date threshold is introduced. Existing audience configuration is covered as a decision matrix, not BVA. |
| B. Date / time / timezone | N/A | This change introduces no new date calculation. Existing Published/upcoming eligibility remains unchanged and receives regression coverage under AC 04.1. |
| C. Concurrent updates | Applicable | Test rapid repeat App submissions, ordered conflicting valid updates, and shared-device/parent learner switching; final state must remain tied to the correct Student Session (AC 04.2, 05.1). |
| D. Permissions / tenant access | Applicable | Verify all in-scope staff users can view/update Remote, while Student/Parent App visibility continues to follow baseline audience configuration (AC 01.5, 01.6, 04.1). |
| E. State updates / transitions | Applicable | Cover staff-set Remote, BO Reason selection/save/reopen, App submission auto-status update, Remote-to-other-status regression, and response/status consistency (AC 01.1, 03.2, 04.2, 05.1). |
| F. Cross-system synchronization | Applicable | Verify SF, BO, Calendar, App, Notification Center, and SF Chatter from each write producer. Include no-partial-state checks where a submission fails (AC 04.2–05.1). |

## G. Downstream Effects Inventory

| Primary action | Expected downstream effects | Strategy mapping |
|---|---|---|
| Staff manually sets status to Remote in SF or BO | Student Session stores Remote; Calendar group/individual indicator and detail tag update; SF/BO/App read the current status. | AC 01.1, 01.3, 01.5–01.7, 03.2 |
| BO Collect Attendance saves Remote | User selects Attendance Reason, Student Session stores Remote and the selected reason; every BO entry point, SF, and Calendar reread the status; Draft guard is unchanged. | AC 03.1–03.2, 01.1, 01.5–01.6 |
| App submits Attended Remotely | Response stores `Attended Remotely` on the selected student's session only; status becomes Remote; SF/BO/Calendar/App converge; the relevant Collect Attendance UI hides Attendance Notice and Attendance Reason; existing attendance notifications route to recipients/channels. | AC 02.1–02.2, 04.2–04.3, 05.1 |
| Newer valid attendance update replaces an earlier one | Persisted response/status and every consumer show the latest valid value; no duplicate/partial final state. | AC 04.2, 05.1 |
| Remote is changed to another attendance state | Remote indicator/tag is removed and the applicable existing indicator behavior resumes. No behavior for showing or clearing Attendance Notice/Reason after a later non-Remote update is specified. | AC 01.1–01.3, 03.2 |

No new allocation, reporting, or child-record side effects are specified in the PRD; they are out of scope unless implementation inspection identifies one.

## H. Display-Completeness Inventory

| UI surface | Required element | Condition / variation | Coverage mapping |
|---|---|---|---|
| Calendar group lesson card | Remote dot/indicator | `Attendance_Status__c = Remote`; precedence against New, Trial, Seasonal, Reallocated, Absent | AC 01.1 Ordering / Sort |
| Calendar individual lesson card | Remote dot/indicator | `Attendance_Status__c = Remote`; precedence against competing indicators | AC 01.1 Ordering / Sort |
| Calendar lesson detail learner list | Remote tag beside learner name | Mixed Remote and non-Remote learners; tag removed after a non-Remote update | AC 01.3 Display completeness |
| Calendar legend | `Remote` / `リモート参加`, Vibrant/Indigo/40 | Locale and visual-token assertion | AC 01.4 Display completeness / exact text |
| Salesforce Lesson Detail | Attendance Status `Remote` | Display, select, save, reread; all staff users | AC 01.5 Display completeness |
| BO Lesson Detail / Student Tab | Attendance Status `Remote` | Display, select, save, reread; all staff users | AC 01.6 Display completeness |
| Salesforce attendance response display | `Attended Remotely` as `Option (Remark)` | App-produced or seeded response | AC 02.1 Display completeness |
| BO attendance response display | `Attended Remotely` as `Option (Remark)` | App-produced or seeded response | AC 02.2 Display completeness |
| BO Collect Attendance forms | Exact option `Remote` | Lesson Detail, Report, Lesson Report Detail, Calendar Bulk Update; Draft state | AC 03.1 Display completeness / regression |
| BO Collect Attendance after a direct BO Remote selection | Attendance Reason selector is shown and accepts a reason | BO user selects Remote; Attendance Notice visibility is outside the confirmed update | AC 03.2 Display completeness |
| Learner App lesson display | PRD-defined Remote value | Staff-set and App-set Remote | AC 01.7 Display completeness |
| Learner App Submit Attendance | `Attended Remotely` option | Existing eligible/ineligible Student and Parent audience states | AC 04.1 Display completeness / permissions |
| Notification Center and SF Chatter | Attendance notification record | Teacher and Centre Manager routing variants from PX suite 3276 | AC 04.3 Display completeness / cross-system |

## H.1 Spec–Figma Mismatch Report

| Figma target / PRD area | Checked fields | Result | Resolution |
|---|---|---|---|
| Node `13193:54004` — BO Calendar Lesson Detail / Calendar indicator and tag (US 01) | Remote dot/tag, legend, and priority behavior | No unresolved mismatch. Figma MCP confirmed the relevant Remote Attendance node and Calendar frames; the PRD explicitly defines the display contract. | ✅ User confirmed US 01 defines Calendar Remote presentation sufficiently; PRD is the test oracle. |
| Node `13193:54004` — BO Collect Attendance | Remote choice in Collect Attendance | No unresolved mismatch. Figma MCP confirmed the Remote Attendance node and Collect Attendance frame. | ✅ Covered by exact `Remote` option and all-entry-point strategy. |
| Detailed nested Figma states | Pixel-level nested frame inspection | Figma returned a rate-limit response after the initial MCP retrieval. This does not create a behavioral ambiguity because the user directed QA to focus on the PRD. | ✅ Accepted by user; no red/amber mismatch remains. |

## 6. Coverage Gaps vs Existing Test Cases

Existing Qase PX suite 3276 supplies the baseline notification routing assertions only. The following coverage is new or must be extended for LT-107175.

| Coverage gap | Existing coverage | LT-107175 action |
|---|---|---|
| Remote Calendar indicator in group and individual views | Not covered | ✅ New coverage |
| Explicit Remote indicator precedence | Not covered | ✅ New coverage |
| Remote tag and legend/localization token | Not covered | ✅ New coverage |
| SF/BO status field selection and persistence | Not covered | ✅ New coverage |
| SF/BO response `Option (Remark)` presentation | Not covered | ✅ New coverage |
| Remote in every BO Collect Attendance entry point | Not covered | ✅ New coverage |
| Draft-disabled regression with Remote | Not covered | ✅ New coverage |
| Learner App Remote display and `Attended Remotely` submission | Not covered | ✅ New coverage |
| Unchanged Student/Parent audience and eligibility rules | Existing baseline may exist; no Remote variant | ✅ Extend with Remote variant |
| Latest-valid-value behavior | Not covered | ✅ New coverage |
| Shared-device and parent learner-switch identity isolation | Not covered | ✅ New coverage |
| App response-to-status Remote synchronization | Not covered | ✅ New coverage |
| Remote notification channels and recipient routing | PX suite 3276 covers prior attendance notification behavior | ✅ Extend existing scenarios with Remote variant |
| BO Remote Attendance Reason selector and saved selection | Updated PdM behavior | ✅ New coverage |

## 7. Suggested Test Suite Structure

| Proposed suite / file | Scope | Estimated cases |
|---|---|---:|
| `calendar-remote-attendance` | **All Calendar-related cases only:** group/individual indicator, precedence, no-Remote regression, detail tag, legend, and Calendar readback after SF/BO/App updates | 13–16 |
| `attendance-status-surfaces` | SF/BO status controls, response presentation, staff view/update matrix, App display | 8–10 |
| `collect-attendance-remote` | All BO collection entry points, persistence/reread, Draft guard | 8–10 |
| `app-remote-submission-sync` | App option/audience eligibility, submission, latest-wins, shared-device/parent identity isolation, SF/BO/App synchronization, and hidden Notice/Reason state; Calendar checks belong only to `calendar-remote-attendance` | 11–14 |
| `remote-attendance-notifications` | PX suite 3276 notification-channel and recipient-routing variants for Remote | 6–8 |

Estimated executable cases: **45–58**. The generated set contains 55 cases; the later non-Remote transition behavior for Attendance Notice/Reason is not included because it was not specified by PdM.
