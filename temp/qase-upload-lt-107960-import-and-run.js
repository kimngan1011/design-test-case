const fs = require("fs");
const path = require("path");

const cfg = JSON.parse(fs.readFileSync(".vscode/mcp.json", "utf8"));
const token = cfg.servers.qase.env.QASE_API_TOKEN;
const base = cfg.servers.qase.env.QASE_BASE_URL || "https://api.qase.io/v1";
const project = cfg.servers.qase.env.QASE_PROJECT_CODE || "PX";

const suiteId = 257;
const csvPath =
  "epics/lesson/LT-107960-duplicate-lesson-duration-validation/test-cases/duplicate-lesson-duration-validation.csv";
const summaryPath = "temp/qase-upload-lt-107960-summary.json";
const existingCaseIds = [1207, 11708, 20708, 20734];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;

  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (char === '"' && next === '"') {
        field += '"';
        i += 1;
      } else if (char === '"') quoted = false;
      else field += char;
      continue;
    }
    if (char === '"') quoted = true;
    else if (char === ",") {
      row.push(field);
      field = "";
    } else if (char === "\n") {
      row.push(field);
      rows.push(row);
      row = [];
      field = "";
    } else if (char !== "\r") field += char;
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function splitNumberedSteps(value) {
  const items = [];
  for (const line of String(value || "").split("\n")) {
    const match = line.match(/^\s*\d+\.\s*"?([\s\S]*?)"?\s*$/);
    if (match) items.push(match[1].trim());
    else if (line.trim() && items.length) items[items.length - 1] += `\n${line.trim()}`;
  }
  return items;
}

function cleanText(value) {
  return String(value || "")
    .replace(/\\n|\/n/g, "\n")
    .replace(/\*\*/g, "")
    .trim();
}

function severityValue(value) {
  const normalized = String(value || "").toLowerCase();
  if (normalized === "critical") return 2;
  if (normalized === "major") return 3;
  if (normalized === "minor") return 5;
  if (normalized === "trivial") return 6;
  return 5;
}

function priorityValue(value) {
  const normalized = String(value || "").toLowerCase();
  if (normalized === "high" || normalized === "critical") return 3;
  if (normalized === "medium") return 3;
  if (normalized === "low") return 4;
  return 3;
}

async function qase(method, endpoint, payload) {
  const response = await fetch(`${base}${endpoint}`, {
    method,
    headers: {
      Token: token,
      "Content-Type": "application/json",
    },
    body: payload ? JSON.stringify(payload) : undefined,
  });
  const json = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(JSON.stringify({ method, endpoint, status: response.status, response: json }, null, 2));
  }
  return json.result;
}

async function findDuplicate(title) {
  const result = await qase(
    "GET",
    `/case/${project}?suite_id=${suiteId}&search=${encodeURIComponent(title)}&limit=100&offset=0`,
  );
  return (result.entities || []).find((item) => item.suite_id === suiteId && item.title === title);
}

function readCases() {
  const rows = parseCsv(fs.readFileSync(csvPath, "utf8"));
  const headers = rows[0];
  return rows
    .slice(1)
    .map((row) => Object.fromEntries(headers.map((header, index) => [header, row[index] || ""])))
    .filter((row) => row.title)
    .map((row) => {
      const actions = splitNumberedSteps(row.steps_actions);
      const results = splitNumberedSteps(row.steps_result);
      const data = splitNumberedSteps(row.steps_data);
      return {
        originalTitle: row.title,
        payload: {
          title: cleanText(row.title),
          description: cleanText(row.description),
          preconditions: cleanText(row.preconditions),
          postconditions: cleanText(row.postconditions),
          priority: priorityValue(row.priority),
          severity: severityValue(row.severity),
          type: 2,
          behavior: 1,
          automation: 0,
          status: 1,
          is_flaky: 0,
          layer: 1,
          tags: cleanText(row.tags)
            .split(/[;,]/)
            .map((tag) => tag.trim())
            .filter(Boolean),
          steps_type: "classic",
          steps: actions.map((action, index) => ({
            action,
            expected_result: results[index] || "",
            data: data[index] || "",
          })),
        },
      };
    });
}

function writeCsv(idsByTitle, suite) {
  const rows = parseCsv(fs.readFileSync(csvPath, "utf8"));
  const headers = rows[0];
  const titleIndex = headers.indexOf("title");
  const idIndex = headers.indexOf("v2.id");
  const suiteIdIndex = headers.indexOf("suite_id");
  const parentIndex = headers.indexOf("suite_parent_id");
  const suiteIndex = headers.indexOf("suite");

  for (const row of rows.slice(1)) {
    if (row[titleIndex] && idsByTitle.has(row[titleIndex])) row[idIndex] = String(idsByTitle.get(row[titleIndex]));
    row[suiteIdIndex] = String(suite.id);
    row[parentIndex] = String(suite.parent_id || "");
    row[suiteIndex] = suite.title;
  }

  function cell(value) {
    const text = String(value || "");
    return /[",\n\r]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
  }

  fs.writeFileSync(
    csvPath,
    rows.map((row) => headers.map((_, index) => cell(row[index] || "")).join(",")).join("\n") +
      "\n",
  );
}

async function main() {
  const suite = await qase("GET", `/suite/${project}/${suiteId}`);
  const cases = readCases();
  const idsByTitle = new Map();
  const created = [];
  const skippedDuplicates = [];

  for (const item of cases) {
    const payload = { ...item.payload, suite_id: suite.id };
    const duplicate = await findDuplicate(payload.title);
    if (duplicate) {
      skippedDuplicates.push({ id: duplicate.id, suite_id: suite.id, title: payload.title });
      idsByTitle.set(item.originalTitle, duplicate.id);
      console.log(`duplicate PX-${duplicate.id}: ${payload.title}`);
      continue;
    }

    const result = await qase("POST", `/case/${project}`, payload);
    created.push({ id: result.id, suite_id: suite.id, title: payload.title });
    idsByTitle.set(item.originalTitle, result.id);
    console.log(`created PX-${result.id}: ${payload.title}`);
  }

  writeCsv(idsByTitle, suite);

  const newCaseIds = [...created, ...skippedDuplicates].map((item) => item.id).sort((a, b) => a - b);
  const combinedCaseIds = [...new Set([...newCaseIds, ...existingCaseIds])].sort((a, b) => a - b);
  const existingCases = [];
  for (const id of existingCaseIds) {
    const testCase = await qase("GET", `/case/${project}/${id}`);
    existingCases.push({ id, title: testCase.title, url: `https://app.qase.io/case/${project}-${id}` });
  }

  const run = await qase("POST", `/run/${project}`, {
    title: "LT-107960 - Duplicate Lesson Duration Validation",
    description:
      "Manual QA run for LT-107960. Includes newly-created duplicate/edit/extend/drag-drop Duration validation cases plus existing Duplicate Lesson and Duration field visibility baselines.",
    cases: combinedCaseIds,
    include_all_cases: false,
  });

  const summary = {
    project,
    suite: {
      id: suite.id,
      title: suite.title,
      parent_id: suite.parent_id || null,
      url: `https://app.qase.io/project/${project}?suite=${suite.id}`,
    },
    csvPath,
    created,
    skippedDuplicates,
    newCaseIds,
    existingCaseIds,
    existingCases,
    combinedCaseIds,
    run: {
      id: run.id,
      url: `https://app.qase.io/run/${project}/dashboard/${run.id}`,
      caseCount: combinedCaseIds.length,
    },
  };

  fs.mkdirSync(path.dirname(summaryPath), { recursive: true });
  fs.writeFileSync(summaryPath, `${JSON.stringify(summary, null, 2)}\n`);
  console.log(JSON.stringify(summary, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
