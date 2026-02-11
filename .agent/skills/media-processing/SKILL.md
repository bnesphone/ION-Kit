---
name: media-processing
description: Process images and media, including AI-based background removal using local models.
---

# Media Processing Skill

This skill provides capabilities for processing media files, primarily focusing on AI-powered background removal for images. It integrates the "AI Toolkit Background Remover" and other utilities.

## Capabilities

1.  **Remove Background (Advanced)**: Uses generic or specific models (like SAM, U2Net) to remove backgrounds from images.
2.  **Batch Processing**: Process entire directories of images.
3.  **Transparent/Colored Backgrounds**: Replace background with transparency or solid colors.

## Tools & Usage

### 1. Advanced Background Remover (AI Toolkit)

Located at: `integrated_tools/background_remover/cli_remove_bg.py`

**Syntax:**
```bash
python integrated_tools/background_remover/cli_remove_bg.py [input_path] [output_path] [options]
```

**Common Options:**
- `--model_type`: Model architecture (default: 'u2net')
- `--alpha_matting`: Enable alpha matting for finer edge details (hair, fur)
