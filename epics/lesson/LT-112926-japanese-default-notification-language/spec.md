---
ticket_id: LT-112926
ticket_url: https://manabie.atlassian.net/browse/LT-112926
title: Core | Send notifications & emails in Japanese by default instead of depending on System Admin language
module: lesson
bucket: lesson
status: Done
internal_uat_date: null
production_release_date: 2026-11-02
last_updated: 2026-10-14
---

# LT-112926 — Japanese default notification language

## Scope verified from source

All cases in this pack verify the language used in the delivered payload, rather than the language selected in the acting Salesforce Admin's profile. The org-level setting is `Lesson_Custom_Settings__c.Notification_Language__c`.

| Flow | Channel / recipient | Source path |
|---|---|---|
| Bulk publish lesson | Email to lesson teacher; no teacher Chatter; student/parent push regression | `LessonBulkMasterQueueExecutor.cls`, `LessonHandler.cls` |
| Publish lesson | Student/parent push; Chatter post mentioning teacher | `LessonHandler.cls`, `ChatterPostHandler.cls` |
| Send lesson report | Push to student and default parent | `LessonReportHandler.cls`, `SendLessonReportNotificationParam.cls` |
| Lesson time changed | Push to active allocated students | `UpdateLessonHandler.cls` |
| Lesson submit attendance | Push to default parent | `StudentSessionsHandler.cls` |
| Nichibei cancellation booking | Chatter post mentioning resolved Centre Manager(s) | `LessonPlatformEventHandler.cls`, `ChatterPostHandler.cls` |

## Language contract

- `ja`, `jp`, and Japanese locale variants resolve to Japanese.
- `en`, `us`, and English locale variants resolve to `en_US`.
- Blank, unsupported, or malformed values resolve to Japanese.
- The language of the Admin who triggers the action, an async job, or who views the Chatter post must not alter the generated payload.

## Source observation to track

Bulk publishing deliberately sets `LessonToggle.bypassPublishTeacherChatterNotification = true` before updating lessons. It therefore sends the teacher email instead of posting teacher Chatter; this is verified by LANG-002.

`LessonBulkMasterQueueExecutor` requests Japanese labels for the bulk-publish student/parent push when the configuration is Japanese. At the reviewed revision, `packages/i18n/main/default/translations/ja.translation-meta.xml` contains no translations for `notification_bulk_publish_lesson_title` or `notification_bulk_publish_lesson_content`. Case LANG-008 is intentionally retained as a release blocker/regression test until those translations are present and deployed.
