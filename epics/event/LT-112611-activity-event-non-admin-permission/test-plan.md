# Test Plan: LT-112611 — Event scope with non-admin users (Nozomi intUAT)

Goal: no repeat of incident MANACS-2648. Every screen that reads a new field or calls a new Apex class is opened by every non-admin persona that uses it.

## Personas

| Code | User | PSG | Notes |
|---|---|---|---|
| T | chauthuylinh.nguyen+nozomiuatteacherpsg@manabie.com | ManabieERP_Teacher_PSG | contains `backoffice_teacher_v2`; **cannot log in to Salesforce** — Salesforce rows are N/A, only Back Office / Calendar BO rows apply |
| CS | chauthuylinh.nguyen+nozomiuatcenterstaffpsg@manabie.com | ManabieERP_Center_Staff_PSG | contains `center_level_edit_v2` |
| CM | chauthuylinh.nguyen+nozomiuatcentremanager@manabie.com | Centre_Manager | pure V1, no event permission sets |
| HQ | chauthuylinh.nguyen+nozomiinternaluatcm@manabie.com | HQwithoutApproval | runs the automation suite |
| P / S | learner app parent / student | — | |
| G | external booking (guest) | — | |

Legend: `M` = run manually · `A` = covered by automation (do not repeat manually) · `–` = not applicable · `?` = waiting for Open Question 1 (CM access)

## Run order

0. Gate check (no UI, ~5 min): field + Apex class access matrix per PSG (query in section G). Stop and report if any PSG with users lacks access.
1. Section A with flag Reservation Deadline OFF (Nozomi current setting).
2. Section A row A3 with flag ON.
3. Sections B → F.

## A. Activity Event form (LT-101742 — Reservation Deadline fields)

| # | Case | T | CS | CM | HQ |
|---|---|---|---|---|---|
| A1 | PX-29532 Edit dialog – existing values prefilled | – | M | ? | A (PX-691) |
| A2 | PX-29534 Duplicate dialog – existing values prefilled | – | M | ? | M |
| A3 | PX-29536 Edit dialog – Reservation Deadline ON – value prefilled | – | M | – | M |
| A4 | PX-29537 New from Activity Events list – Event Master lookup | – | M | ? | M |
| A5 | PX-29538 Create from Event Master detail | – | M | ? | A (PX-11285) |
| A6 | PX-3823 Edit Activity Event from Calendar SF | – | M | ? | M |

## B. Booking (LT-101742)

| # | Case | CS | HQ | P | S | G |
|---|---|---|---|---|---|---|
| B1 | PX-29539 Open Booking System dialog | M | M | – | – | – |
| B2 | PX-19162 Reservation Deadline tooltip and value (flag ON) | M | – | – | – | – |
| B3 | PX-3961, PX-3962, PX-3964 Student event list and reserve | – | – | – | M | – |
| B4 | PX-3969, PX-3970, PX-3972 Parent event list and reserve | – | – | M | – | – |
| B5 | PX-3977, PX-3978 Reserve fail | – | – | M | M | – |
| B6 | PX-4002, PX-4048 External booking form opens | – | – | – | – | M |

## C. Target Segment (LT-102792 — Unique Target Key)

| # | Case | T | CS | HQ |
|---|---|---|---|---|
| C1 | PX-19067 Add Target Location | – | M | A (PX-715) |
| C2 | PX-19069, PX-19070, PX-19071 Add Target School / Grade / Course | – | M | A (PX-735, PX-747, PX-759) |
| C3 | PX-28644 Duplicate Target Location blocked | – | M | M |
| C4 | PX-28646, PX-28647, PX-28648 Duplicate Grade / School / Course blocked | – | M | M |

## D. Import buttons (LT-101739)

| # | Case | T | CS | CM | HQ |
|---|---|---|---|---|---|
| D1 | PX-28146 Import buttons visible only with permission | – | M | M | M |
| D2 | PX-28148 Import Activity Event CSV | – | M | – | M |
| D3 | PX-28151 Import Event Participant CSV | – | M | – | M |
| D4 | PX-28155 Import Event Staff CSV | – | M | – | M |

## E. Bulk Collect Attendance (LT-102368 SF, LT-102369 BO)

Expected behavior (release note + code on develop): **Mark all as Attend / Absent overwrites every row**, and the other Mark-all button still works afterwards.
PX-28133, PX-28134 ("only empty rows filled") and PX-3835 ("nothing is changed") are outdated — update them before running.

| # | Case | T | CS | HQ |
|---|---|---|---|---|
| E1 | PX-3830 Mark all as Attend (SF) | – | M | – |
| E2 | PX-3831 Mark all as Absent (SF) | – | M | – |
| E3 | PX-3835 Mark all Attend then Absent — after update | – | M | – |
| E4 | PX-28127, PX-28133, PX-28134 (BO) — after update | M | – | – |

## F. Upcoming: `event-ext` package (not on Nozomi intUAT yet)

New Apex classes are granted only to V2 permission sets (`center_level_edit_v2`, `full_access_v2`, `full_access_v2_restricted`):
`EventParticipantControllerExt`, `EventStaffControllerExt`, `EventTargetLocationController`, `EventStaffNotificationController`, `EventFeatureTogglesController`, `LessonCustomSettingsController` (LT-104435, LT-102390).
Run this section on the first org where `event-ext` is deployed, before it reaches a V1 partner.

| # | Case | T | CS | CM | HQ |
|---|---|---|---|---|---|
| F1 | PX-19073, PX-19075 Add Master Participant | – | M | ? | A (PX-788) |
| F2 | PX-19077, PX-19079 Add Master Staff | – | M | ? | A (PX-3498) |
| F3 | PX-19067 New Target Location (moved to ext) | – | M | ? | A (PX-715) |
| F4 | PX-4938 Send notification to event staff | – | M | ? | M |

## G. Gate check query (read-only, any user with API access)

Field access per PSG — every PSG with Activity Event / Event Master read must show `Y` for both Reservation Deadline fields:

```
SELECT Parent.PermissionSetGroup.DeveloperName, Field, PermissionsRead
FROM FieldPermissions
WHERE Field IN ('MANAERP__Activity_Event__c.MANAERP__Reservation_Deadline_Date__c',
                'MANAERP__Event_Master__c.MANAERP__Reservation_Deadline_Hours__c')
```

Nozomi intUAT result on 2026-10-06 (before core hotfix): missing for Nozomi_PT (143 users), ManabieERP_Part_Time_Teacher_PSG (43), HQwithoutApproval (25), ManabieERP_Teacher_PSG (6), ManabieERP_Center_Staff_PSG (5), Centre_Manager (1).

## Open Questions

1. Centre_Manager has no event permission sets — is "no Activity Event access" intended? Rows marked `?` depend on this.
2. Hotfix `a8a90c9026` does not add `Event_Master__c.Reservation_Deadline_Hours__c` to `Platform_Edit_Activity_Events`, `Community_Edit_Activity_Events`, `Community_Edit_Event_Participant`, but the Edit/Duplicate dialog reads it.
3. `event-ext` classes granted only to V2 permission sets — same pattern as the incident.
