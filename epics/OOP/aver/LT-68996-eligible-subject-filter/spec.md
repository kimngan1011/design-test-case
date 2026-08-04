---
ticket_id: LT-68996
ticket_url: https://manabie.atlassian.net/browse/LT-68996
title: A.ver | Custom config for eligible subject filter
module: scheduling
bucket: OOP/aver
status: Done
internal_uat_date: null
production_release_date: null
last_updated: 2026-07-23
---

# LT-68996: A.ver eligible-subject filter

## Scope

For tenant A.ver, teacher eligibility filtering changes from an **OR** match to an **AND** match when multiple subjects are selected. A teacher is eligible only when the teacher is eligible for every selected subject. The change applies to Add Teacher, the Teacher list, and the Calendar filter.

## Acceptance criteria

- AC 01: In A.ver, a multi-subject selection returns teachers eligible for all selected subjects.
- AC 02: A teacher eligible for only a subset of selected subjects is excluded.
- AC 03: A single selected subject retains normal eligible-teacher filtering.
- AC 04: The AND rule is applied consistently in Add Teacher, Teacher list, and Calendar filter.
- AC 05: The customization is scoped to A.ver; non-A.ver tenants retain the existing OR behavior.
