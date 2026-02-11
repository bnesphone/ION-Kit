const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// -- Configuration --
const RESOURCES_DIR = path.join(__dirname, 'resources');
const TARGET_DIR = process.argv[2] || process.cwd();

console.log(`\n📦 Portable App Konverter`);
console.log(`   Target: ${TARGET_DIR}\n`);

if (!fs.existsSync(path.join(TARGET_DIR, 'package.json'))) {
    console.error("❌ ERROR: No package.json found in target directory!");
    console.error("   Please run this tool inside a Node.js project folder.");
    process.exit(1);
}

console.log("Reading package.json...");
const pkgPath = path.join(TARGET_DIR, 'package.json');
const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));

// 1. Create electron folder
console.log("Creating electron directory...");
const electronDir = path.join(TARGET_DIR, 'electron');
if (!fs.existsSync(electronDir)) fs.mkdirSync(electronDir);

// 2. Copy Templates
console.log("Copying templates...");
fs.copyFileSync(path.join(RESOURCES_DIR, 'main.js'), path.join(electronDir, 'main.js'));
fs.copyFileSync(path.join(RESOURCES_DIR, 'preload.js'), path.join(electronDir, 'preload.js'));
fs.copyFileSync(path.join(RESOURCES_DIR, 'setup.bat'), path.join(TARGET_DIR, 'setup_portable.bat'));

// 3. Update package.json
console.log("Updating configuration...");

// Ensure devDependencies exist
if (!pkg.devDependencies) pkg.devDependencies = {};
pkg.devDependencies['concurrently'] = '^8.2.0';
pkg.devDependencies['electron'] = '^28.0.0';
pkg.devDependencies['electron-builder'] = '^24.9.1';
pkg.devDependencies['wait-on'] = '^7.2.0';

// Ensure scripts exist
if (!pkg.scripts) pkg.scripts = {};
pkg.scripts['electron'] = 'electron .';
pkg.scripts['electron-dev'] = 'concurrently "npm start" "wait-on http://localhost:3000 && electron ."';
pkg.scripts['dist'] = 'npm run build && electron-builder';

// Set Main Entry
pkg.main = 'electron/main.js';

// Add Build Config
pkg.build = {
    "appId": `com.portable.${pkg.name || 'app'}`,
    "productName": pkg.name ? pkg.name.charAt(0).toUpperCase() + pkg.name.slice(1) : "PortableApp",
    "extends": null,
    "asar": false,
    "directories": {
        "buildResources": "public"
    },
    "files": [
        "build/**/*",
        "electron/**/*",
        "server/**/*",
        "public/**/*",
        "package.json"
    ],
    "asarUnpack": ["server/**/*"],
    "win": {
        "target": ["portable", "nsis"]
    }
};

fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2));

console.log("\n✅ Success! App converted.");
console.log("   1. Run 'setup_portable.bat'");
console.log("   2. Select Option 1 (Install Dependencies)");
console.log("   3. Select Option 2 (Build)");
