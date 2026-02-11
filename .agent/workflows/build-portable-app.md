---
description: guide on how to package a web application or Node.js project into a portable Windows executable
---

# Build Portable App Workflow

This workflow guides you through creating a portable Windows application (`.exe`) from a web app or Node.js project using the Portable App Kit.

## Prerequisites
- Node.js installed
- A web app (HTML/JS) or Node.js project directory
- `app-packaging` skill enabled

## Steps

### 1. Prepare the Source
Ensure your web app or Node.js project is ready.
- If it's a web site, you need the `index.html` and assets.
- If it's a Node app, ensure `package.json` and entry point are clear.

### 2. Copy to Portable Kit
Copy your project files to `integrated_tools/portable_app_kit/app/`.
*Creating a subfolder is recommended.*

### 3. Configure the Build
Edit `integrated_tools/portable_app_kit/package.json` (if building a Node app) or prepare the `make_portable.js` arguments.

### 4. Run the Packager
Use the `app-packaging` skill script or run directly:

```bash
# Basic usage
node integrated_tools/portable_app_kit/make_portable.js --source [path_to_source] --name [AppName]
```

### 5. Customization
- **Icon**: Provide an `.ico` file using `--icon [path]`.
- **Window Size**: Set `--width` and `--height`.
- **Node Version**: Specify Node version if needed (default is usually bundled).

### 6. Verify Output
The portable executable will be generated in `integrated_tools/portable_app_kit/dist/` (or specified output directory).
Test the `.exe` on a fresh environment if possible.

## Example
```bash
# Package a React build folder
node integrated_tools/portable_app_kit/make_portable.js --source ./my-react-app/build --name "MyAwesomeApp" --icon ./assets/logo.ico
```
