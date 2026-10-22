const { execSync } = require('child_process');
const path = require('path');

console.log('Running static generator script: python scripts/build_static.py...');
try {
  const output = execSync('python scripts/build_static.py', {
    cwd: __dirname,
    encoding: 'utf8',
    stdio: 'inherit'
  });
} catch (e) {
  process.exit(e.status || 1);
}
