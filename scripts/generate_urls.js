const fs = require('fs');
const path = require('path');

const dataFile = path.join(__dirname, '..', 'js', 'data.js');
const outFile = path.join(__dirname, '..', 'urls.txt');

const text = fs.readFileSync(dataFile, 'utf8');
const ids = [];
const idRegex = /"id"\s*:\s*"([^"]+)"/g;
let match;
while ((match = idRegex.exec(text)) !== null) {
  ids.push(match[1]);
}
// Take up to 200 URLs (Google Indexing API daily quota)
const urls = ids.slice(0, 200).map(id => `https://imtechboss.com/${id}/`);
fs.writeFileSync(outFile, urls.join('\n'), 'utf8');
console.log(`Generated ${urls.length} URLs to ${outFile}`);
