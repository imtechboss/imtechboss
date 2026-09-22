const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, '../js/data.js');
const { initialArticles } = require('../js/data.js');

const newArticle = {
  "id": "land-solution-nepal-cadastral-calculator",
  "title": "Land Solution: Nepal's Premier Land Measurement, Cadastral Plotter & Kitta-Kaat Software",
  "category": "Software & Tech",
  "tags": [
    "Land Solution",
    "Land Solution App",
    "Nepal Land Measurement",
    "Ropani Aana Paisa Daam",
    "Bigha Kattha Dhur",
    "Kitta Kaat",
    "Cadastral Survey",
    "Napi Nepal",
    "GIS & Shapefile",
    "Binod Bhatt"
  ],
  "author": {
    "name": "Binod Bhatt",
    "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80",
    "role": "Lead Architect & Developer"
  },
  "date": "Sep 19, 2026",
  "timestamp": 1789805000000,
  "readTime": "7 min read",
  "image": "images/land-solution-showcase.jpg",
  "excerpt": "The definitive software suite for surveyors, civil engineers, Amin, and real estate professionals in Nepal: Discover Land Solution featuring precision R-A-P-D & B-K-D conversion, Cadastral Map Plotter Pro, Kitta-Kaat Polygon Splitting, MUTM projection coordinates, and GIS Shapefile (.shp) compatibility.",
  "featured": true,
  "trending": true,
  "views": "3,850",
  "likes": 142,
  "content": `<p>For decades, surveying, land administration, and property transactions in Nepal have grappled with the complexities of dual customary measurement systems, manual parcel boundary calculations, and cumbersome coordinate conversions. Developed by <strong>Binod Bhatt</strong>, <strong>Land Solution</strong> has emerged as the premier all-in-one software ecosystem designed specifically for survey engineers, Amin, real estate developers, local government palikas, and property owners across Nepal.</p>

<p>Whether you need rapid, error-free conversions between <strong>Ropani-Aana-Paisa-Daam</strong> and <strong>Bigha-Kattha-Dhur</strong>, full-fledged <strong>Cadastral Map Plotting</strong>, or automated <strong>Kitta-Kaat (Polygon Splitting)</strong> according to government survey guidelines, Land Solution provides unmatched mathematical precision on both <strong>Android</strong> mobile devices and <strong>Windows PC</strong> workstations.</p>

<h2>1. Dual Land Measurement Engines: Complete Mastery Over Nepali Units</h2>
<p>Nepal's topographical and administrative diversity relies on two distinct land measurement frameworks. Land Solution provides dual native calculating engines with instantaneous, micro-precision conversions:</p>

<div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
  <div class="p-5 rounded-2xl bg-blue-50/70 dark:bg-slate-800/80 border border-blue-200 dark:border-slate-700">
    <h3 class="text-sm font-bold text-blue-900 dark:text-blue-300 uppercase tracking-wider mb-2">🏔️ Pahad &amp; Valley: R-A-P-D System</h3>
    <ul class="text-xs text-gray-700 dark:text-gray-300 space-y-1.5 list-disc pl-4">
      <li><strong>1 Ropani</strong> = 16 Aana = 5,476.00 Sq. Feet (508.74 Sq. Meters)</li>
      <li><strong>1 Aana</strong> = 4 Paisa = 342.25 Sq. Feet (31.80 Sq. Meters)</li>
      <li><strong>1 Paisa</strong> = 4 Daam = 85.56 Sq. Feet (7.95 Sq. Meters)</li>
      <li><strong>1 Daam</strong> = 21.39 Sq. Feet (1.99 Sq. Meters)</li>
    </ul>
  </div>
  <div class="p-5 rounded-2xl bg-amber-50/70 dark:bg-slate-800/80 border border-amber-200 dark:border-slate-700">
    <h3 class="text-sm font-bold text-amber-900 dark:text-amber-300 uppercase tracking-wider mb-2">🌾 Terai &amp; Plains: B-K-D System</h3>
    <ul class="text-xs text-gray-700 dark:text-gray-300 space-y-1.5 list-disc pl-4">
      <li><strong>1 Bigha</strong> = 20 Kattha = 72,900.00 Sq. Feet (6,772.63 Sq. Meters)</li>
      <li><strong>1 Kattha</strong> = 20 Dhur = 3,645.00 Sq. Feet (338.63 Sq. Meters)</li>
      <li><strong>1 Dhur</strong> = 16 Kanwa = 182.25 Sq. Feet (16.93 Sq. Meters)</li>
      <li><strong>1 Kanwa</strong> = 11.39 Sq. Feet (1.06 Sq. Meters)</li>
    </ul>
  </div>
</div>

<p>Users can input raw field tape measurements in Feet, Inches, Meters, or Links, and Land Solution computes exact fractional units down to thousandths of a Daam or Kanwa with 100% mathematical consistency.</p>

<h2>2. Cadastral Map Plotter Pro &amp; Precision Kitta-Kaat (Polygon Splitting)</h2>
<div class="my-6 rounded-2xl overflow-hidden border border-gray-200 dark:border-slate-800 shadow-xl">
  <img src="images/land-solution-kitta-kaat.jpg" alt="Land Solution Cadastral Map Plotting and Polygon Splitting (Kitta Kaat) Module" class="w-full h-auto object-cover">
  <p class="text-[11px] text-gray-500 dark:text-gray-400 text-center py-2.5 px-4 bg-gray-50 dark:bg-slate-850 font-medium">Cadastral Map Plotting and automated Polygon Splitting (कित्ताकाट) inside Land Solution: Interactive vertex adjustment, offset lines, and live area balancing.</p>
</div>

<p>The hallmark capability of Land Solution is its cutting-edge <strong>Cadastral Plotter Pro</strong>. Instead of relying on expensive third-party CAD suites, surveyors and Amin can perform land parcel mapping directly in the field:</p>
<ul class="list-disc pl-5 my-4 space-y-2 text-xs sm:text-sm text-gray-700 dark:text-gray-300">
  <li><strong>Intelligent Polygon Splitting (कित्ताकाट):</strong> Effortlessly divide any irregular polygon parcel by desired target area (e.g., cut exactly 4 Aana or 10 Dhur), fixed frontage, or parallel offset lines. The software automatically calculates the exact coordinates of the dividing line.</li>
  <li><strong>Traverse &amp; Coordinate Geometry (COGO):</strong> Input bearing and distance (Azimuth) or total station point coordinates to construct parcel boundaries with automatic closing error analysis and Bowditch balancing.</li>
  <li><strong>Side Lengths &amp; Interior Angles:</strong> Displays all vertex angles, perimeter measurements, and side dimensions simultaneously in both metric and imperial units.</li>
</ul>

<h2>3. Advanced Geodesy: Nepal MUTM Grid &amp; GNSS Integration</h2>
<p>Nepal's official national grid is based on the <strong>Modified Universal Transverse Mercator (MUTM)</strong> projection referencing the Everest 1830 spheroid, divided into three central meridian zones:</p>
<ul class="list-disc pl-5 my-4 space-y-1.5 text-xs sm:text-sm text-gray-700 dark:text-gray-300">
  <li><strong>MUTM 81° CM:</strong> Covers Far-Western &amp; Mid-Western regions (Sudurpashchim &amp; Karnali Provinces).</li>
  <li><strong>MUTM 84° CM:</strong> Covers Western &amp; Central regions (Gandaki &amp; Lumbini Provinces).</li>
  <li><strong>MUTM 87° CM:</strong> Covers Kathmandu Valley, Bagmati, Madhesh, and Koshi Provinces.</li>
</ul>
<p>Land Solution features built-in forward and inverse geodetic transformation routines, converting WGS84 GPS Latitude/Longitude coordinates into official Nepal Survey Department Northing/Easting coordinates with sub-centimeter geoidal height correction via the <strong>EGM2008 Nepal Geoid Model</strong>.</p>

<h2>4. Napi Karyalaya &amp; LIS / SAEx Interoperability</h2>
<p>For professional surveyors working with the Government of Nepal's <strong>Survey Department (नापी विभाग)</strong>, seamless data transfer is essential. Land Solution is built to integrate directly with existing <strong>Land Information Systems (LIS)</strong> and <strong>Survey Automation Extension (SAEx)</strong> workflows:</p>
<ul class="list-disc pl-5 my-4 space-y-2 text-xs sm:text-sm text-gray-700 dark:text-gray-300">
  <li><strong>Shapefile (.shp) Import/Export:</strong> Read and write GIS shapefiles, ESRI spatial layers, and parcel attribute tables directly.</li>
  <li><strong>Spatial Database (.mdb) Compatibility:</strong> Connect seamlessly to standard LIS scratch and spatial data templates (BLANK81, BLANK84, BLANK87).</li>
  <li><strong>Preeti &amp; Nepali Font Printing:</strong> Generates official parcel trace sheets, field book schedules, and salary slips formatted in authentic Nepali Unicode and Preeti fonts for immediate legal and administrative submission.</li>
</ul>

<h2>5. Platform Availability: Android App &amp; Windows PC Edition</h2>
<p>Land Solution is built on modern high-performance Flutter architecture, delivering a fluid, unified user experience across devices:</p>
<div class="overflow-x-auto my-6">
  <table class="w-full text-xs text-left border border-gray-200 dark:border-slate-800 rounded-xl overflow-hidden">
    <thead class="bg-gray-100 dark:bg-slate-800 text-gray-900 dark:text-gray-100 font-bold">
      <tr>
        <th class="p-3">Platform</th>
        <th class="p-3">Latest Version</th>
        <th class="p-3">Key Highlights</th>
        <th class="p-3">System Requirements</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-200 dark:divide-slate-800 text-gray-700 dark:text-gray-300">
      <tr>
        <td class="p-3 font-semibold text-blue-600 dark:text-blue-400">Android APK</td>
        <td class="p-3">v2.8.5 (arm64 / v7a)</td>
        <td class="p-3">On-site GPS survey, offline area calculation, quick touch parcel drafting, WhatsApp export</td>
        <td class="p-3">Android 8.0 or higher</td>
      </tr>
      <tr>
        <td class="p-3 font-semibold text-indigo-600 dark:text-indigo-400">Windows PC Edition</td>
        <td class="p-3">v2.8.5 Desktop (ZIP)</td>
        <td class="p-3">High-resolution multi-monitor plotting, batch Shapefile import, DWG export, PDF print generator</td>
        <td class="p-3">Windows 10 / 11 (64-bit)</td>
      </tr>
    </tbody>
  </table>
</div>

<h2>Download Land Solution</h2>
<p>Empower your field surveying, property valuations, and engineering workflows with Nepal's most trusted cadastral companion. Choose your platform below to get started:</p>

<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 my-8 not-prose">
  <div class="p-6 rounded-3xl bg-gradient-to-br from-blue-600 to-indigo-700 text-white shadow-xl flex flex-col justify-between">
    <div>
      <span class="px-2.5 py-1 rounded-md bg-white/20 text-white text-[10px] uppercase font-bold tracking-widest inline-block mb-3">Mobile Edition</span>
      <h3 class="text-xl font-bold">Android APK (v2.8.5)</h3>
      <p class="text-xs text-blue-100 mt-2 leading-relaxed">
        Optimized for 64-bit and 32-bit Android smartphones. Field-ready with offline GPS satellite integration and instant unit conversion.
      </p>
    </div>
    <div class="mt-6">
      <a href="https://binodbhatt.com.np/downloads/BRB_Land_Calculator_v2.8.5_arm64.apk" class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white text-blue-900 hover:bg-blue-50 font-bold text-xs shadow-md transition-all">
        <span>📲 Download Android APK</span>
      </a>
    </div>
  </div>

  <div class="p-6 rounded-3xl bg-slate-900 border border-slate-800 text-white shadow-xl flex flex-col justify-between">
    <div>
      <span class="px-2.5 py-1 rounded-md bg-blue-500/20 text-blue-400 text-[10px] uppercase font-bold tracking-widest inline-block mb-3">Desktop Edition</span>
      <h3 class="text-xl font-bold">Windows PC (v2.8.5)</h3>
      <p class="text-xs text-gray-400 mt-2 leading-relaxed">
        Standalone desktop utility for office plotting, batch shapefile processing, AutoCAD DWG exports, and official report generation.
      </p>
    </div>
    <div class="mt-6">
      <a href="https://binodbhatt.com.np/downloads/BRB_Land_Calculator_v2.8.5_PC.zip" class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs shadow-md transition-all">
        <span>💻 Download Windows PC (.ZIP)</span>
      </a>
    </div>
  </div>
</div>

<div class="p-4 rounded-xl bg-blue-50 dark:bg-slate-800 border border-blue-100 dark:border-slate-700 text-xs text-gray-700 dark:text-gray-300 my-6">
  <strong>Technical Support &amp; Custom Features:</strong> Land Solution continues to receive regular updates based on feedback from Amin and surveyors across Nepal. Have an idea for a feature or need custom enterprise integration for your engineering consultancy? Contact <strong>Binod Bhatt</strong> directly through the contact portal or WhatsApp!
</div>`
};

// Check if article already exists
const existingIdx = initialArticles.findIndex(a => a.id === newArticle.id);
if (existingIdx !== -1) {
  initialArticles[existingIdx] = newArticle;
  console.log("Updated existing Land Solution article.");
} else {
  // Put at the very beginning (index 0)
  initialArticles.unshift(newArticle);
  console.log("Inserted Land Solution article at index 0.");
}

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
