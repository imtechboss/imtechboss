const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, '../js/data.js');
const { initialArticles } = require('../js/data.js');

const newArticle = {
  "id": "nta-mdms-registration-nepal-online-guide-2026",
  "title": "NTA MDMS Registration Nepal 2026: Step-by-Step Online Process, Documents, Fees & IMEI Verification",
  "category": "Software & Tech",
  "tags": [
    "NTA MDMS",
    "MDMS Registration Nepal",
    "Mobile Device Management System",
    "IMEI Check Nepal",
    "Nepal Telecom",
    "Ncell MDMS",
    "Tribhuvan Airport Customs",
    "Nepal Tech",
    "Binod Bhatt"
  ],
  "author": {
    "name": "Binod Bhatt",
    "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80",
    "role": "Tech Policy & Hardware Analyst"
  },
  "date": "Sep 19, 2026",
  "timestamp": 1789806000000,
  "readTime": "6 min read",
  "image": "images/nta-mdms-registration-nepal.jpg",
  "excerpt": "Complete 2026 guide to Nepal Telecommunications Authority (NTA) MDMS mobile registration: how to check IMEI status online, register phones brought from abroad (personal, gift, or commercial), required documents, customs fee structure, and avoiding network deactivation.",
  "featured": false,
  "trending": true,
  "views": "4,210",
  "likes": 118,
  "content": `<p>If you have recently purchased a smartphone, received an iPhone as a gift from overseas, or returned home to Nepal through Tribhuvan International Airport (TIA), ensuring your device is officially registered under the <strong>Nepal Telecommunications Authority (NTA) Mobile Device Management System (MDMS)</strong> is mandatory. Unregistered devices face automatic cellular network barring across <strong>Nepal Telecom (Namaste)</strong>, <strong>Ncell</strong>, and <strong>Smart Cell</strong> networks.</p>

<p>Here is your comprehensive, step-by-step 2026 guide to verifying your device's status, understanding government customs regulations, and completing your online registration in under five minutes.</p>

<h2>1. What is NTA MDMS & Why is It Mandatory in Nepal?</h2>
<p>Implemented by the Government of Nepal and NTA, the <strong>Mobile Device Management System (MDMS)</strong> is a centralized high-security database that tracks all mobile handsets entering Nepal using their unique <strong>15-digit International Mobile Equipment Identity (IMEI)</strong> numbers.</p>
<p>The system was launched to achieve four vital objectives:</p>
<ul class="list-disc pl-5 my-4 space-y-2 text-xs sm:text-sm text-gray-700 dark:text-gray-300">
  <li><strong>Eliminate the Grey Market:</strong> Curb unauthorized imports and illegal smuggling of mobile devices that evade government customs duties and 13% VAT.</li>
  <li><strong>Theft Prevention &amp; Recovery:</strong> Enables law enforcement agencies and Nepal Police to blacklist, track, and disable stolen or lost phones nationwide.</li>
  <li><strong>Protect National Security:</strong> Prevent untraceable cellular hardware from being used in cybercrime, fraud, and illegal communication.</li>
  <li><strong>Consumer Safety:</strong> Ensure devices operating on Nepali frequency bands are genuine, certified hardware with active manufacturer warranties.</li>
</ul>

<h2>2. How to Check if Your Phone is Already Registered</h2>
<p>Before initiating registration, first check if your handset is already whitelisted in the government database:</p>

<div class="my-6 p-5 rounded-2xl bg-blue-50/70 dark:bg-slate-800/80 border border-blue-200 dark:border-slate-700">
  <h3 class="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider mb-3">🔍 Step-by-Step IMEI Verification:</h3>
  <ol class="list-decimal pl-5 text-xs sm:text-sm text-gray-700 dark:text-gray-300 space-y-2">
    <li>Open your smartphone's dialer app and dial <strong>*#06#</strong>.</li>
    <li>Your screen will display your device's <strong>IMEI 1</strong>, <strong>IMEI 2</strong> (for dual-SIM/e-SIM devices), and Serial Number. Copy or note down the 15-digit <strong>IMEI 1</strong>.</li>
    <li>Visit the official portal at <a href="https://mdms.nta.gov.np" target="_blank" rel="noopener" class="text-blue-600 dark:text-blue-400 font-bold underline">mdms.nta.gov.np</a>.</li>
    <li>Enter your 15-digit IMEI number into the <em>"Check Your Device Status"</em> search box and click <strong>Search</strong>.</li>
  </ol>
  <div class="mt-4 p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 text-xs">
    ✅ If it says <strong>"Your device is registered in MDMS"</strong>, you do not need to do anything! Your phone will run smoothly on all Nepali networks forever.<br>
    ⚠️ If it says <strong>"Your device is not registered in MDMS"</strong>, proceed with the online registration steps below.
  </div>
</div>

<h2>3. Nepal Customs Rules: Who Gets Free Registration?</h2>
<p>Under the latest Department of Customs guidelines, mobile devices brought into Nepal are classified into two categories:</p>

<div class="overflow-x-auto my-6">
  <table class="w-full text-xs text-left border border-gray-200 dark:border-slate-800 rounded-xl overflow-hidden">
    <thead class="bg-gray-100 dark:bg-slate-800 text-gray-900 dark:text-gray-100 font-bold">
      <tr>
        <th class="p-3">Category of Traveler</th>
        <th class="p-3">Allowance</th>
        <th class="p-3">Customs Fee</th>
        <th class="p-3">Required Documents</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-200 dark:divide-slate-800 text-gray-700 dark:text-gray-300">
      <tr>
        <td class="p-3 font-semibold text-blue-600 dark:text-blue-400">Returnee Migrant Workers (श्रम स्वीकृति लिएका)</td>
        <td class="p-3">Up to 2 Mobile Phones (1 in personal use + 1 sealed gift)</td>
        <td class="p-3 font-bold text-emerald-600">FREE (NPR 0)</td>
        <td class="p-3">Passport with departure &amp; arrival stamp, Valid Foreign Employment Labor Approval (Labor Permit), Boarding Pass</td>
      </tr>
      <tr>
        <td class="p-3 font-semibold">General Travelers, Students &amp; Tourists</td>
        <td class="p-3">1 Phone (personal hand carry)</td>
        <td class="p-3 font-bold text-emerald-600">FREE (NPR 0)</td>
        <td class="p-3">Passport / Citizenship, Boarding pass, Air ticket</td>
      </tr>
      <tr>
        <td class="p-3 font-semibold text-amber-600">Second Phone / Extra Gift Phone</td>
        <td class="p-3">Additional Smartphone / iPhone</td>
        <td class="p-3 font-bold text-amber-600">Customs Duty Fee</td>
        <td class="p-3">Customs Declaration Receipt (प्रज्ञापनपत्र) paid at TIA Customs Counter</td>
      </tr>
    </tbody>
  </table>
</div>

<h2>4. Official Government Customs Fee Structure (For Extra / Grey Phones)</h2>
<p>If you are registering an extra handset brought from abroad that does not qualify for free personal exemption, the Ministry of Finance has established the following flat customs duty rates:</p>

<ul class="list-disc pl-5 my-4 space-y-2 text-xs sm:text-sm text-gray-700 dark:text-gray-300">
  <li><strong>Apple iPhones &amp; Flagship Smartphones (Priced above NPR 100,000):</strong> Flat <strong>NPR 10,000</strong> per unit.</li>
  <li><strong>Mid-Range &amp; Budget Smartphones (Android handsets):</strong> Flat <strong>NPR 3,000</strong> per unit.</li>
  <li><strong>Basic Feature Phones (Bar/Keypad phones):</strong> Flat <strong>NPR 200</strong> per unit.</li>
</ul>

<h2>5. Step-by-Step Online Registration Process on MDMS Portal</h2>
<p>Follow these exact instructions to complete individual self-registration:</p>

<ol class="list-decimal pl-5 my-4 space-y-3 text-xs sm:text-sm text-gray-700 dark:text-gray-300">
  <li><strong>Visit the Portal:</strong> Navigate to <a href="https://mdms.nta.gov.np" target="_blank" rel="noopener" class="text-blue-600 font-bold underline">mdms.nta.gov.np</a> and click on the <strong>"Individual Application" (व्यक्तिगत दर्ता)</strong> button.</li>
  <li><strong>Choose Your Registration Type:</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-xs">
      <li><em>Traveler / Nepali Citizen Returning Abroad:</em> Choose this if you arrived via international flight with valid travel documents.</li>
      <li><em>Already in Nepal (Customs Paid):</em> Choose this if you have a customs receipt paid at airport customs or land borders.</li>
    </ul>
  </li>
  <li><strong>Enter Handset Details:</strong> Enter Device Brand (e.g. Apple, Samsung), Model (e.g. iPhone 18 Pro Max, Galaxy S26 Ultra), and both <strong>IMEI 1</strong> and <strong>IMEI 2</strong> numbers.</li>
  <li><strong>Upload Verification Documents:</strong> Attach clean photo or PDF scans (under 1MB each) of:
    <ul class="list-disc pl-5 mt-1 space-y-1 text-xs">
      <li>Passport copy (Bio page and Arrival immigration stamp page).</li>
      <li>Boarding Pass or Air Ticket.</li>
      <li>Foreign Employment Labor Approval card (for migrant workers claiming free 2nd phone).</li>
      <li>Airport Customs Payment Receipt / Pragyapanpatra (if applicable).</li>
    </ul>
  </li>
  <li><strong>Submit &amp; Track:</strong> Review all entered data and click <strong>Submit</strong>. You will receive an Application Tracking ID via SMS/Email. Approval typically takes between <strong>24 to 72 hours</strong>, after which your phone's IMEI will be permanently whitelisted!</li>
</ol>

<h2>6. Important Tips for Dual-SIM &amp; eSIM Users</h2>
<div class="p-4 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/40 text-xs text-amber-900 dark:text-amber-200 my-4">
  <strong>Always Register Both IMEIs:</strong> Modern smartphones (like iPhones and Samsung Galaxies) feature dual connectivity (Physical SIM + eSIM or Dual Nano-SIM). Each SIM slot has its own independent 15-digit IMEI number. When applying on the MDMS portal, <strong>always input both IMEI 1 and IMEI 2</strong>. If you only register IMEI 1, your second SIM or eSIM slot may get barred when you switch carrier SIM cards!
</div>

<h2>The Verdict</h2>
<p>NTA's MDMS system provides long-term security, legal peace of mind, and theft protection for your valuable investment. Whether you are using the latest iPhone or an affordable Android companion, verifying your registration guarantees uninterrupted 4G and 5G connectivity across all corners of Nepal.</p>

<p>Have questions about MDMS customs clearance or registration status? Share your query in the comments below, and our team will guide you through the process!</p>`
};

// Insert right after the top article (index 1) so Land Solution stays at index 0 and MDMS is right next to it
initialArticles.splice(1, 0, newArticle);
console.log("Inserted NTA MDMS article at index 1.");

// Write back to js/data.js
const updatedJs = `// Auto-generated from Binod Bhatt's Blogger archive (THE BOSS)
var initialArticles = ${JSON.stringify(initialArticles, null, 2)};

if (typeof module !== "undefined" && module.exports) {
  module.exports = { initialArticles };
}
if (typeof window !== "undefined") {
  window.initialArticles = initialArticles;
}
`;

fs.writeFileSync(dataPath, updatedJs, 'utf8');
console.log(`Successfully updated js/data.js. Total articles: ${initialArticles.length}`);
