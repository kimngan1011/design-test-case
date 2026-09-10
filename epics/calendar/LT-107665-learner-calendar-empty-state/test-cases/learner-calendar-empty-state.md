# LT-107665 - Learner App Calendar Empty-State Messages

## LT-107665-01 - All Tab Empty State Uses Items Copy

**Description:** AC-01 / BR-01 / BR-02 / BR-06. A date with no visible Lesson or Event shows the tab-specific All message in English and Japanese.

**Preconditions:**

- Learner A can sign in to Learner App.
- On 2030-10-14, Learner A has no visible Lesson and no visible Activity Event.
- Learner App supports English and Japanese.

| Step | Action | Expected result | Test data |
|---:|---|---|---|
| 1 | Sign in as Learner A and set application language to English. | Learner App opens in English. | learner = A; locale = en |
| 2 | Open Calendar, select 2030-10-14, and select the `All` tab. | No Lesson or Event card is displayed for the selected date. | date = 2030-10-14; tab = All |
| 3 | Read the empty-state text. | Text is exactly `There are no items scheduled for this date.` | locale = en |
| 4 | Change application language to Japanese without changing the selected date or tab. | Calendar remains on 2030-10-14 and `All`. | locale = ja |
| 5 | Read the empty-state text. | Text is exactly `この日の予定はありません。` | locale = ja |

## LT-107665-02 - Lesson Tab Empty State Uses Lessons Copy When Event Exists

**Description:** AC-02 / BR-01 / BR-03 / BR-06. The Lesson tab must not use the generic or Event copy when only an Event exists on the selected date.

**Preconditions:**

- Learner A can sign in to Learner App.
- A Published Activity Event `Event Only A` is visible to Learner A on 2030-10-15.
- Learner A has no visible Lesson on 2030-10-15.
- Learner App supports English and Japanese.

| Step | Action | Expected result | Test data |
|---:|---|---|---|
| 1 | Sign in as Learner A, set language to English, open Calendar, and select 2030-10-15. | Calendar opens for the selected date. | learner = A; locale = en; date = 2030-10-15 |
| 2 | Select the `All` tab. | `Event Only A` is displayed, proving the selected date is not globally empty. | tab = All; event = Event Only A |
| 3 | Select the `Lesson` tab. | No Lesson card is displayed. | tab = Lesson |
| 4 | Read the empty-state text. | Text is exactly `There are no lessons scheduled for this date.` It is not the All or Event message. | locale = en |
| 5 | Change language to Japanese without changing date or tab. | `Lesson` remains selected and no Lesson card appears. | locale = ja |
| 6 | Read the empty-state text. | Text is exactly `この日の授業はありません。` | locale = ja |

## LT-107665-03 - Event Tab Empty State Uses Events Copy When Lesson Exists

**Description:** AC-03 / BR-01 / BR-04 / BR-06. The Event tab must not use the generic or Lesson copy when only a Lesson exists on the selected date.

**Preconditions:**

- Learner A can sign in to Learner App.
- Published Lesson `Lesson Only A` is visible to Learner A on 2030-10-16.
- Learner A has no visible Activity Event on 2030-10-16.
- Learner App supports English and Japanese.

| Step | Action | Expected result | Test data |
|---:|---|---|---|
| 1 | Sign in as Learner A, set language to English, open Calendar, and select 2030-10-16. | Calendar opens for the selected date. | learner = A; locale = en; date = 2030-10-16 |
| 2 | Select the `All` tab. | `Lesson Only A` is displayed, proving the selected date is not globally empty. | tab = All; lesson = Lesson Only A |
| 3 | Select the `Event` tab. | No Event card is displayed. | tab = Event |
| 4 | Read the empty-state text. | Text is exactly `There are no events scheduled for this date.` It is not the All or Lesson message. | locale = en |
| 5 | Change language to Japanese without changing date or tab. | `Event` remains selected and no Event card appears. | locale = ja |
| 6 | Read the empty-state text. | Text is exactly `この日のイベントはありません。` | locale = ja |
