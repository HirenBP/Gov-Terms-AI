const fs = require('fs');
const path = require('path');

const srcDir = path.resolve(__dirname, '..', 'build');
const destDir = path.resolve(__dirname, '..', '..', 'docs');

async function exists(p) {
  try {
    await fs.promises.access(p);
    return true;
  } catch (e) {
    return false;
  }
}

async function emptyDir(dir) {
  if (!await exists(dir)) return;
  const entries = await fs.promises.readdir(dir);
  await Promise.all(entries.map(async (entry) => {
    const full = path.join(dir, entry);
    await fs.promises.rm(full, { recursive: true, force: true });
  }));
}

async function copyDir(src, dest) {
  await fs.promises.mkdir(dest, { recursive: true });
  const entries = await fs.promises.readdir(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      await copyDir(srcPath, destPath);
    } else {
      await fs.promises.copyFile(srcPath, destPath);
    }
  }
}

async function main() {
  if (!await exists(srcDir)) {
    console.error('Build directory not found. Run `npm run build` (react-scripts) first.');
    process.exit(1);
  }

  // Ensure docs folder exists and is emptied
  await fs.promises.mkdir(destDir, { recursive: true });
  await emptyDir(destDir);

  // Copy built files
  await copyDir(srcDir, destDir);
  console.log('Copied build/* -> docs/');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
