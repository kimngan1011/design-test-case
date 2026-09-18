const fs = require("fs");

const cfg = JSON.parse(fs.readFileSync(".vscode/mcp.json", "utf8"));
const token = cfg.servers.qase.env.QASE_API_TOKEN;
const base = cfg.servers.qase.env.QASE_BASE_URL || "https://api.qase.io/v1";
const project = cfg.servers.qase.env.QASE_PROJECT_CODE || "PX";

const parentSuiteId = 2717;
const suiteName = "Add Subject Code in Subject Master (LT-101718 / PBT-3075)";
const csvPath =
  "epics/OOP/riso/LT-101718-subject-code-subject-master/test-cases/subject-code-subject-master.csv";
const summaryPath = "temp/qase-upload-lt-101718-summary.json";
const impactedCaseIds = [23042, 23045, 23046, 23048];

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
  const text = String(value || "").replace(/\\n|\/n/g, "\n").trim();
  if (!text) return [];

  const matches = [...text.matchAll(/(?:^|\n|\s)(\d+)\.\s+/g)];
  if (!matches.length) return [text];

  return matches
    .map((match, index) => {
      const start = match.index + match[0].length;
      const end = index + 1 < matches.length ? matches[index + 1].index : text.length;
      return text.slice(start, end).trim();
    })
    .filter(Boolean);
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
  if (normalized === "high" || normalized === "medium") return 3;
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

async function listSuites() {
  const suites = [];
  for (let offset = 0; ; offset += 100) {
    const result = await qase("GET", `/suite/${project}?limit=100&offset=${offset}`);
    const entities = result.entities || [];
    suites.push(...entities);
    if (entities.length < 100) return suites;
  }
}

async function resolveSuite() {
  const suites = await listSuites();
  const existing = suites.find((suite) => suite.title === suiteName && suite.parent_id === parentSuiteId);
  if (existing) return { suite: existing, created: false };

  const suite = await qase("POST", `/suite/${project}`, {
    title: suiteName,
    parent_id: parentSuiteId,
  });
  return { suite, created: true };
}

async function findDuplicate(suiteId, title) {
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
      const stepData = splitNumberedSteps(row.steps_data);
      return {
        csvTitle: row.title,
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
            data: stepData[index] || "",
          })),
        },
      };
    });
}

function writeCsv(idsByTitle, suiteId) {
  const rows = parseCsv(fs.readFileSync(csvPath, "utf8"));
  const headers = rows[0];
  const titleIndex = headers.indexOf("title");
  const idIndex = headers.indexOf("v2.id");
  const suiteIdIndex = headers.indexOf("suite_id");
  const parentIndex = headers.indexOf("suite_parent_id");
  const suiteIndex = headers.indexOf("suite");

  for (const row of rows.slice(1)) {
    if (idsByTitle.has(row[titleIndex])) row[idIndex] = String(idsByTitle.get(row[titleIndex]));
    row[suiteIdIndex] = String(suiteId);
    row[parentIndex] = String(parentSuiteId);
    row[suiteIndex] = suiteName;
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
  const { suite, created: suiteCreated } = await resolveSuite();
  const cases = readCases();
  const idsByTitle = new Map();
  const created = [];
  const skippedDuplicates = [];

  for (const testCase of cases) {
    const payload = { ...testCase.payload, suite_id: suite.id };
    const duplicate = await findDuplicate(suite.id, payload.title);
    if (duplicate) {
      skippedDuplicates.push({ id: duplicate.id, title: payload.title, suite_id: suite.id });
      idsByTitle.set(testCase.csvTitle, duplicate.id);
      console.log(`duplicate PX-${duplicate.id}: ${payload.title}`);
      continue;
    }

    const result = await qase("POST", `/case/${project}`, payload);
    created.push({ id: result.id, title: payload.title, suite_id: suite.id });
    idsByTitle.set(testCase.csvTitle, result.id);
    console.log(`created PX-${result.id}: ${payload.title}`);
  }

  const newCaseIds = [...created, ...skippedDuplicates].map((item) => item.id).sort((a, b) => a - b);
  const caseIds = [...new Set([...newCaseIds, ...impactedCaseIds])].sort((a, b) => a - b);
  writeCsv(idsByTitle, suite.id);

  const runTitle = "LT-101718 / PBT-3075 - Subject Code in Subject Master";
  const run = await qase("POST", `/run/${project}`, {
    title: runTitle,
    description:
      "Manual QA run for LT-101718 / PBT-3075. Covers new Subject Code cases plus impacted ATC student search, data integrity, and create lesson regression cases.",
    cases: caseIds,
    include_all_cases: false,
  });

  const verified = await qase("GET", `/run/${project}/${run.id}`);
  const summary = {
    project,
    parentSuiteId,
    suite: {
      id: suite.id,
      title: suite.title,
      url: `https://app.qase.io/project/${project}?suite=${suite.id}`,
      created: suiteCreated,
    },
    csvPath,
    totalNewCasesInCsv: cases.length,
    created,
    skippedDuplicates,
    newCaseIds,
    impactedCaseIds,
    run: {
      id: run.id,
      title: verified.title,
      url: `https://app.qase.io/run/${project}/dashboard/${run.id}`,
      caseIds,
      caseCount: caseIds.length,
    },
  };

  fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 2) + "\n");
  console.log(JSON.stringify(summary, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
