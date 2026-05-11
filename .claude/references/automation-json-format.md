# Automation JSON Format Specification

This file defines the standard JSON format for test cases used by `execute-test-cases` skill.

---

## JSON Structure

```json
[
  {
    "id": "TC-001",
    "title": "Short descriptive title",
    "severity": "critical",
    "role": "CM",
    "start_url": "/lesson-list",
    "preconditions": "Master data exists",
    "steps": [
      { "action": "click", "target": "Create Lesson button", "data": null, "expected": null },
      { "action": "fill", "target": "Lesson Name", "data": "Test 001", "expected": null },
      { "action": "click", "target": "Save", "data": null, "expected": "Lesson saved with Draft status" }
    ]
  }
]
```

## Test Case Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Unique ID: `TC-001`, `TC-002`, ... or Qase ID like `PX-1234` |
| `title` | yes | One-line test case title |
| `severity` | yes | `critical` / `major` / `normal` / `minor` |
| `role` | yes | Login role: `CM` / `HQ` / `Teacher` / `Staff` |
| `start_url` | no | Relative URL to navigate before steps |
| `preconditions` | no | Text description of required setup |
| `steps` | yes | Array of step objects |

## Step Fields

| Field | Required | Description |
|-------|----------|-------------|
| `action` | yes | One of the action types below |
| `target` | depends | Element label, field name, URL, or menu path |
| `data` | depends | Value to fill, key to press, or scroll pixels |
| `expected` | no | Expected result text. `null` = no verification needed |

## Action Types

| Type | `target` | `data` | Example |
|------|----------|--------|---------|
| `click` | Element label/name | null | `{"action":"click","target":"Save button","data":null}` |
| `fill` | Form field name | Value | `{"action":"fill","target":"Lesson Name","data":"Test 001"}` |
| `type` | Non-form element | Text | `{"action":"type","target":"Search box","data":"math"}` |
| `select` | Dropdown name | Option | `{"action":"select","target":"Teaching Medium","data":"Online"}` |
| `navigate` | URL or menu path | null | `{"action":"navigate","target":"/lesson-list","data":null}` |
| `press_key` | null | Key name | `{"action":"press_key","target":null,"data":"Enter"}` |
| `verify` | null | null | `{"action":"verify","target":null,"data":null,"expected":"Text visible"}` |
| `wait` | Element/text | null | `{"action":"wait","target":"Loading complete","data":null}` |
| `login` | null | null | `{"action":"login","target":null,"data":null}` (uses `role`) |
| `scroll` | `down`/`up` | Pixels | `{"action":"scroll","target":"down","data":"500"}` |

---

## NL-to-Action Mapping (for convert skill)

When converting natural language test steps to JSON, use these patterns:

| NL Pattern | Action Type |
|------------|-------------|
| "Click X", "Press X button", "Select X tab", "Tap X" | `click` |
| "Fill X with Y", "Enter Y in X", "Input Y into X" | `fill` |
| "Type Y in X" (non-form context) | `type` |
| "Select Y from X dropdown", "Choose Y in X" | `select` |
| "Navigate to X", "Go to X", "Open X" | `navigate` |
| "Press Enter/Tab/Escape" | `press_key` |
| "Verify X", "Check X", "User sees X", "X is displayed" | `verify` |
| "Wait for X", "X loads", "X appears" | `wait` |
| "Login as X", "Sign in as X" | `login` |
| "Scroll down/up" | `scroll` |

### Role extraction from preconditions

| NL Pattern | Role |
|------------|------|
| "Centre Manager", "CM account", "CM user" | `CM` |
| "HQ Admin", "HQ account", "HQ user" | `HQ` |
| "Teacher", "Teacher account" | `Teacher` |
| "Centre Staff", "Staff account" | `Staff` |
| Not specified | `CM` (default) |

### Severity inference (when not from Qase)

| Context | Severity |
|---------|----------|
| Login, core CRUD, critical path | `critical` |
| Main feature operations | `major` |
| Validation, boundary, error handling | `normal` |
| UI-only, cosmetic | `minor` |
