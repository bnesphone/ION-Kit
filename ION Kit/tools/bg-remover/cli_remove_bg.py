#!/usr/bin/env python3
"""
CLI Background Remover - Command-line interface for AI platforms
Usage: python cli_remove_bg.py <input_image> [options]

Examples:
    python cli_remove_bg.py photo.jpg
    python cli_remove_bg.py photo.jpg --output result.png
    python cli_remove_bg.py photo.jpg --model birefnet-portrait --background white
    python cli_remove_bg.py input/ --batch --output output/
"""

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageFilter
from typing import Optional
import json

from processors.rembg_processor import RembgProcessor
from core.constants import REMBG_MODELS, BACKGROUND_OPTIONS, VALID_EXTENSIONS


def remove_background(
    input_path: str,
    output_path: Optional[str] = None,
    model: str = "birefnet-general",
    background: str = "transparent",
    alpha_matting: bool = False,
    auto_crop: bool = False,
    crop_margin: int = 10,
    sticker_mode: bool = False,
    sticker_color: str = "#ffffff",
    sticker_width: int = 5,
    verbose: bool = False
) -> str:
    """
    Remove background from an image.
    
    Args:
        input_path: Path to input image
        output_path: Path for output image (auto-generated if None)
        model: AI model to use (see REMBG_MODELS)
        background: Background type ('transparent', 'white', 'black')
        alpha_matting: Enable alpha matting for better edges
        auto_crop: Crop to subject bounds
        crop_margin: Margin around subject when cropping
        sticker_mode: Add outline around subject
        sticker_color: Outline color (hex)
        sticker_width: Outline width in pixels
        verbose: Print status messages
    
    Returns:
        Path to output file
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if input_file.suffix.lower() not in VALID_EXTENSIONS:
        raise ValueError(f"Unsupported file format: {input_file.suffix}")
    
    # Generate output path if not provided
    if output_path is None:
        output_path = input_file.parent / f"{input_file.stem}_nobg.png"
    else:
        output_path = Path(output_path)
    
    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Status callback for verbose mode
    def status_cb(msg: str):
        if verbose:
            print(f"[INFO] {msg}")
    
    # Initialize processor
    processor = RembgProcessor()
    
    # Build options
    options = {
        "model": model,
        "alpha_matting": alpha_matting,
        "alpha_matting_foreground_threshold": 240,
        "alpha_matting_background_threshold": 10,
        "alpha_matting_erode_size": 10,
    }
    
    # Process image
    status_cb(f"Processing {input_file.name}...")
    output_img = processor.process(input_file, output_path, options, status_cb)
    
    # Apply background
    if background != "transparent":
        bg_color = BACKGROUND_OPTIONS[background][1]
        if bg_color:
            bg_img = Image.new("RGB", output_img.size, bg_color)
            bg_img.paste(output_img, (0, 0), output_img)
            output_img = bg_img
    
    # Auto-crop if enabled
    if auto_crop:
        status_cb("Auto-cropping...")
        bbox = output_img.getbbox()
        if bbox:
            x1, y1, x2, y2 = bbox
            x1 = max(0, x1 - crop_margin)
            y1 = max(0, y1 - crop_margin)
            x2 = min(output_img.width, x2 + crop_margin)
            y2 = min(output_img.height, y2 + crop_margin)
            output_img = output_img.crop((x1, y1, x2, y2))
    
    # Sticker mode (add outline)
    if sticker_mode:
        status_cb("Adding sticker outline...")
        # Create a stroke/outline
        # Get alpha channel
        r, g, b, a = output_img.split()
        
        # Dialate alpha channel to create outline
        # Simple approach: Composite multiple shifted copies or use max filter
        # Using MaxFilter for dilation
        from PIL import ImageFilter
        outline = a.filter(ImageFilter.MaxFilter(sticker_width * 2 + 1))
        
        # Create solid color image for outline
        sticker_bg = Image.new("RGBA", output_img.size, sticker_color)
        sticker_bg.putalpha(outline)
        
        # Paste original on top
        sticker_bg.paste(output_img, (0, 0), output_img)
        output_img = sticker_bg

    # Save final result
    output_img.save(output_path)
    status_cb(f"Saved to {output_path}")
    
    return str(output_path)

def main():
    parser = argparse.ArgumentParser(description="Remove background from images")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("--output", "-o", help="Output path")
    parser.add_argument("--model", "-m", default="birefnet-general", choices=REMBG_MODELS.keys())
    parser.add_argument("--bg", "-b", dest="background", default="transparent", choices=BACKGROUND_OPTIONS.keys())
    parser.add_argument("--alpha", "-a", action="store_true", help="Enable alpha matting")
    parser.add_argument("--crop", "-c", action="store_true", help="Auto crop")
    parser.add_argument("--sticker", "-s", action="store_true", help="Sticker mode")
    parser.add_argument("--sticker-color", default="#ffffff", help="Sticker color")
    parser.add_argument("-v", "--verbose", action="store_true")
    
    args = parser.parse_args()
    
    try:
        result = remove_background(
            args.input,
            args.output,
            model=args.model,
            background=args.background,
            alpha_matting=args.alpha,
            auto_crop=args.crop,
            sticker_mode=args.sticker,
            sticker_color=args.sticker_color,
            verbose=args.verbose or True 
        )
        print(f"Success: {result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
