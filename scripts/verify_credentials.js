// verify_credentials.js – simple check that Google ADC can be loaded
// ---------------------------------------------------------------
// Run with: node scripts/verify_credentials.js
// ---------------------------------------------------------------

const path = require('path');
const fs = require('fs');
const { google } = require('googleapis');

const CREDENTIALS_PATH = path.resolve(__dirname, 'credentials.json');

(async () => {
  try {
    const auth = new google.auth.GoogleAuth({
      scopes: ['https://www.googleapis.com/auth/indexing'],
      keyFile: fs.existsSync(CREDENTIALS_PATH) ? CREDENTIALS_PATH : undefined,
    });
    const client = await auth.getClient();
    console.log('✅ Credentials loaded successfully from:', CREDENTIALS_PATH);
  } catch (e) {
    console.error('❌ Failed to load credentials:', e.message);
  }
})();
