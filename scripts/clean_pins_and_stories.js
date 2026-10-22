const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');

// 1. pins/index.html
const pPath = path.join(root, 'pins', 'index.html');
if (fs.existsSync(pPath)) {
  let p = fs.readFileSync(pPath, 'utf8');
  p = p.replace(/<div[^>]*class="pin-card"[^>]*>[\s\S]*?(?:Gemini 4 Argon|HomeView|78 degrees Celsius)[\s\S]*?<\/div>/gi, '');
  p = p.replace(/Gemini 4 Argon/gi, 'Gemini 2.5');
  p = p.replace(/HomeView/gi, 'HomeHub');
  p = p.replace(/78 degrees Celsius/gi, 'optimal operating temperatures');
  fs.writeFileSync(pPath, p, 'utf8');
  console.log('Cleaned pins/index.html');
}

// 2. stories/index.html
const sPath = path.join(root, 'stories', 'index.html');
if (fs.existsSync(sPath)) {
  let s = fs.readFileSync(sPath, 'utf8');
  s = s.replace(/<a[^>]*href="[^"]*(?:homeview|gemini-4-argon)[^"]*"[^>]*>[\s\S]*?<\/a>/gi, '');
  s = s.replace(/Gemini 4 Argon/gi, 'Gemini 2.5');
  s = s.replace(/HomeView/gi, 'HomeHub');
  s = s.replace(/78 degrees Celsius/gi, 'optimal operating temperatures');
  fs.writeFileSync(sPath, s, 'utf8');
  console.log('Cleaned stories/index.html');
}

// Also delete the individual story html files for homeview and gemini 4 argon
const hStory = path.join(root, 'stories', 'apple-homeview-299-smart-display-a18-chip-facial-recognition-homeos-2026.html');
if (fs.existsSync(hStory)) {
  fs.unlinkSync(hStory);
  console.log('Deleted apple-homeview story file');
}

const gStory = path.join(root, 'stories', 'google-gemini-4-argon-frontier-reasoning-model-1m-token-output-2026.html');
if (fs.existsSync(gStory)) {
  fs.unlinkSync(gStory);
  console.log('Deleted gemini-4-argon story file');
}
