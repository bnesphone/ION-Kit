---
description: detailed guide on how to remove backgrounds from images using the integrated AI tools
---

# Remove Background Workflow

This workflow guides you through removing backgrounds from images using the AI Toolkit Background Remover.

## Prerequisites
- Images to process (supported formats: PNG, JPG, JPEG, WEBP, BMP, TIFF)
- `media-processing` skill enabled

## Steps

### 1. Identify the Task
Determine if you need to process a single image or a bulk directory.

### 2. Select the Tool
- For **Single Image** or specific cases, use the CLI tool:
  `python integrated_tools/background_remover/cli_remove_bg.py [input_path] [output_path]`
- For **Bulk Processing**, the CLI also supports directory inputs:
  `python integrated_tools/background_remover/cli_remove_bg.py [input_dir] [output_dir]`

### 3. Choose the Model (Optional)
The default model (`u2net`) works well for general use. For specific needs:
- `isnet-general-use`: High accuracy for general objects
- `isnet-anime`: Best for anime/cartoon characters
- `sam`: Segment Anything Model (slower, but controllable)

Add `--model_type [model_name]` to the command.

### 4. Advanced Options
- **Alpha Matting**: For hair/fur details, add `--alpha_matting`.
  Note: This increases processing time.
- **Background Color**: To replace the background instead of making it transparent, use `--bgcolor "R,G,B,A"`.

### 5. Verification
Check the output directory. The result images will typically have `_no_bg` suffix unless specified otherwise.

## Example
```bash
# Remove background from a single image using ISNet model with alpha matting
python integrated_tools/background_remover/cli_remove_bg.py "C:/Photos/product.jpg" "C:/Photos/Processed/product.png" --model_type isnet-general-use --alpha_matting
```
