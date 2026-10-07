# Test Coverage: LT-112611 — Event screens for non-admin staff after new event fields

Run every case below with the non-admin test users from `spec.md` (Center Staff PSG, Center Manager PSG), not with admin or HQ users. Teacher PSG users cannot log in to Salesforce, so Salesforce screens are out of scope for them.

## Coverage Matrix

| Area | Source ticket | Existing Qase cases | New cases (this epic) |
|---|---|---|---|
| Activity Event Edit dialog | LT-101742 / incident | PX-691 (automated, HQ user), PX-3823 (Calendar SF) | PX-29532 Edit – Center Staff PSG; PX-29536 Edit – Reservation Deadline on |
| Activity Event Duplicate dialog | LT-101742 / incident | PX-19035 (Draft only) | PX-29534 Duplicate – Center Staff PSG |
| New Activity Event from list (Event Master lookup) | LT-101742 | — | PX-29537 New from list – Center Staff PSG |
| Create Activity Event from Event Master | LT-101742 | PX-11285 (automated, HQ user) | PX-29538 Create from Event Master – Center Staff PSG |
| Open Booking System dialog | LT-101742 | PX-19162, PX-4925 | PX-29539 Open Booking System – Center Staff PSG |
| Learner app event list and reservation | LT-101742 | PX-3961, PX-3962, PX-3964, PX-3969, PX-3970, PX-3972, PX-3977, PX-3978 | — |
| External booking form | LT-101742 | PX-4002, PX-4048, PX-4014, PX-4015, PX-4016 | — |
| Target Segment duplicate prevention | LT-102792 | PX-19067, PX-19069, PX-19070, PX-19071, PX-28644, PX-28646, PX-28647, PX-28648 (run with Center Staff PSG user) | — |
| Event Master import buttons | LT-101739 | PX-28146, PX-28148, PX-28151, PX-28154, PX-28155, PX-28156, PX-28157, PX-28160, PX-28161 | — |
| Event Bulk Collect Attendance | LT-102368 | PX-3830, PX-3831, PX-3835 (Calendar SF), PX-28127, PX-28133, PX-28134 (Calendar BO) — PX-3835, PX-28133, PX-28134 outdated, update to "overwrite every row" | — |

## Not covered (needs an answer first)

- Centre Manager PSG access to Activity Events — Open Question 1 in `spec.md`.
- `event-ext` screens (Add Master Participant, Add Master Staff, New Target Location, Send notification to event staff) — not deployed on Nozomi intUAT yet; see `test-plan.md` section F.

## Suggested Test Suite Structure

- `Activity Event – Non-admin Staff Access` (Qase suite 3700, under 2594 Activity event)
