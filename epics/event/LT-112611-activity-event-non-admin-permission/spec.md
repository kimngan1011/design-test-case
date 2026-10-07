---
ticket_id: LT-112611
ticket_url: https://manabie.atlassian.net/browse/LT-112611
title: "[ERPv2] [Activity Event] Existing data is blank on Edit and Duplicate dialogs for non-admin users on Activity Event detail"
module: scheduling
bucket: event
status: In Code Review
internal_uat_date: null
production_release_date: null
last_updated: 2026-10-06
---

# LT-112611: Event screens for non-admin staff after new event fields

## Summary

Incident MANACS-2648 (Nozomi PROD, 2026-10-06): non-admin staff saw blank values in the Activity Event **Edit** and **Duplicate** dialogs. Admin users were not affected.

Root cause: LT-101742 (Reservation Deadline) added `Activity_Event__c.Reservation_Deadline_Date__c` and `Event_Master__c.Reservation_Deadline_Hours__c` but granted field access only to the V2 permission sets (`center_level_edit_v2`, `full_access_v2`, `full_access_v2_restricted`). The event screens read these fields with user-mode queries, so a user without access to one field gets no data at all, even when the Reservation Deadline feature flag is OFF.

## Source Context

- Incident: MANACS-2648, Slack thread `G0BNWGYJNA0/p1791273143956149`.
- Impact list from dev (Loi Pham): LT-101742, LT-101739, LT-102792, LT-102368.
- Hotfix commit `a8a90c9026` adds Reservation Deadline field access to V1 permission sets. It adds `Activity_Event__c.Reservation_Deadline_Date__c` to `Platform_Edit_Activity_Events` but not `Event_Master__c.Reservation_Deadline_Hours__c`, which the Edit/Duplicate dialog also reads.
- `Unique_Target_Key__c` (LT-102792) is still granted only to V2 permission sets. It is written by a trigger in system mode, so creating targets is not expected to fail, but it needs confirmation with non-admin users.

## Screens that read the new fields

| Screen | Field read |
|---|---|
| Activity Event Edit / Duplicate dialog | Activity Event Reservation Deadline Date, Event Master Reservation Deadline Hours |
| New Activity Event — Event Master lookup | Event Master Reservation Deadline Hours |
| Event Master — Open Booking System dialog | Event Master Reservation Deadline Hours, Activity Event Reservation Deadline Date |
| Learner app — event list and reservation | Activity Event Reservation Deadline Date |
| External booking form | Activity Event Reservation Deadline Date |

## Test Users (Nozomi intUAT)

| User | PSG | Location |
|---|---|---|
| chauthuylinh.nguyen+nozomiuatteacherpsg@manabie.com | ManabieERP_Teacher_PSG | 目黒教室 (Teacher) — cannot log in to Salesforce |
| chauthuylinh.nguyen+nozomiuatcenterstaffpsg@manabie.com | ManabieERP_Center_Staff_PSG | 目黒教室 (Centre Staff) |
| chauthuylinh.nguyen+nozomiuatcentremanager@manabie.com | ManabieERP_Center_Manager_PSG | 目黒教室 (Centre Manager) |

## Open Questions

| # | Type | Question |
|---|---|---|
| 1 | Expected behavior | `Centre_Manager` PSG on Nozomi UAT has no event permission sets (Event Master read only, no Activity Event access). Is "no access to Activity Events" the intended behavior for this PSG? |
| 2 | Hotfix gap | Should `Platform_Edit_Activity_Events`, `Community_Edit_Activity_Events`, `Community_Edit_Event_Participant` also get read access to `Event_Master__c.Reservation_Deadline_Hours__c`? |
| 3 | Same pattern, upcoming | `event-ext` Apex classes (LT-104435, LT-102390: `EventParticipantControllerExt`, `EventStaffControllerExt`, `EventTargetLocationController`, `EventStaffNotificationController`, `EventFeatureTogglesController`, `LessonCustomSettingsController`) are granted only to V2 permission sets. Not deployed on Nozomi intUAT yet. |

## Resolved

- Mark all as Attend/Absent: overwriting every row is the intended behavior (LT-102367 release note; LT-102369 BO commit 64c1c0d8144 and LT-102368 SF commit bd20d0d2e8). The "only empty rows" rule in the LT-102367 spec (AC 02.1–02.3) was inferred from older BO code, so PX-28133, PX-28134 and PX-3835 are outdated.
- Center Staff Edit dialog blank / Event Master lookup "No results" on Nozomi intUAT (07/10, automation run 3664): caused by the muting permission set `Center Staff Muted` in `ManabieERP_Center_Staff_PSG`, which muted both Reservation Deadline fields. Admin unmuted them at 14:00–14:01 (+09:00); manual retest passed. Not a code bug — check the same muting permission set on PROD. Tracked in LT-112743.
- New cases in Qase suite 3700 (`Activity Event – Non-admin Staff Access`): PX-29532, PX-29534, PX-29536, PX-29537, PX-29538, PX-29539. The two Teacher PSG cases (PX-29533, PX-29535) were removed because Teacher PSG users cannot log in to Salesforce.
