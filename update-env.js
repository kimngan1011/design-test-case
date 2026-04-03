const fs = require('fs');
const path = require('path');
const envPath = path.join(__dirname, 'e2e', '.env');
let content = fs.existsSync(envPath) ? fs.readFileSync(envPath, 'utf8') : '';

const updates = {
  SF_BASE_URL: 'https://internal-manabie.my.salesforce.com',
  SF_USERNAME: 'kimngan.doan+hqstaff@manabie.com',
  SF_PASSWORD: 'Kimngan10@11',
  BO_BASE_URL: 'https://administration.manabie.net',
  BO_USERNAME: 'kimngan.doan+ptteachermanabie@manabie.com',
  BO_PASSWORD: '@Kimngan1011',
  QASE_TESTOPS_RUN_ID: '2255',
};

let lines = content.split('\n');
const written = new Set();

lines = lines.map(line => {
  const m = line.match(/^#?\s*([A-Z_]+)=/);
  const key = m && m[1];
  if (key && updates[key] !== undefined && written.has(key) === false) {
    written.add(key);
    return key + '=' + updates[key];
  }
  return line;
});

for (const [k, v] of Object.entries(updates)) {
  if (written.has(k) === false) { lines.push(k + '=' + v); }
}

fs.writeFileSync(envPath, lines.join('\n'));
console.log('Updated keys:', [...written].join(', '));
