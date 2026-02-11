---
name: app-packaging
description: Create portable Windows applications from web apps or Node.js projects.
---

# App Packaging Skill

This skill turns Web Applications (React, Vue, HTML/JS) and Node.js projects into standalone `.exe` files for Windows using the Portable App Kit.

## Capabilities

1.  **Portable App Creation**: Bundle a Node.js runtime and application code into a portable folder distro.
2.  **Customization**: Add custom icons, set window dimensions, and configure startup behavior.

## Tools & Usage

### Portable App Kit

Located at: `integrated_tools/portable_app_kit/`

**Prerequisites:**
- Node.js installed in the environment.
- Use `npm install` inside the directory first.

**Usage:**

1.  **Prepare your source**: Have a built web app (e.g., `build/` folder) or a Node code folder.
2.  **Run the script**:
    ```bash
    node integrated_tools/portable_app_kit/make_portable.js --source [path] --name [AppName]
    ```

**Arguments:**
- `--source`: Path to your application code/build.
- `--name`: Name of the output executable.
- `--icon`: (Optional) Path to `.ico` file.
- `--width`: (Optional) Window width (default: 1280).
- `--height`: (Optional) Window height (default: 800).
- `--node-version`: (Optional) Specific Node version to bundle.

## Resources

The template files used for packaging are located in `integrated_tools/portable_app_kit/resources/`. Advanced users can modify `main.js` there to change the electron container behavior.
