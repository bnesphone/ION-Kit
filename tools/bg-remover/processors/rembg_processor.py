"""
Rembg processor - CPU-based background removal using rembg library.
"""

import io
from pathlib import Path
from PIL import Image
from typing import Optional, Callable


try:
    from rembg import remove, new_session
    rembg_available = True
except ImportError:
    rembg_available = False

from .base import BaseProcessor


class RembgProcessor(BaseProcessor):
    """Background removal using rembg with various ONNX models."""

    def __init__(self):
        self._session = None
        self._current_model = None

    def process(
        self,
        input_path: Path,
        output_path: Path,
        options: dict,
        status_callback: Optional[Callable[[str], None]] = None
    ) -> Image.Image:
        """
        Process image using rembg.
        """
        if not rembg_available:
            if status_callback:
                status_callback("WARNING: 'rembg' not available. Using basic color-based removal.")
            return self._heuristic_remove(input_path)

        model = options.get("model", "birefnet-general")

        # Get or create session
        if self._session is None or self._current_model != model:
            if status_callback:
                status_callback(f"Loading model: {model}...")
            self._session = new_session(model)
            self._current_model = model

        # Read input image
        with open(input_path, 'rb') as f:
            input_data = f.read()

        # Build kwargs
        if status_callback:
            status_callback("Removing background...")

        kwargs = {
            "session": self._session,
        }

        if options.get("alpha_matting", False):
            kwargs["alpha_matting"] = True
            kwargs["alpha_matting_foreground_threshold"] = options.get(
                "alpha_matting_foreground_threshold", 240
            )
            kwargs["alpha_matting_background_threshold"] = options.get(
                "alpha_matting_background_threshold", 10
            )
            kwargs["alpha_matting_erode_size"] = options.get(
                "alpha_matting_erode_size", 10
            )

        output_data = remove(input_data, **kwargs)

        # Load the processed image
        output_img = Image.open(io.BytesIO(output_data)).convert("RGBA")

        return output_img

    def _heuristic_remove(self, input_path: Path) -> Image.Image:
        """Fallback: OpenCV GrabCut -> Erode -> Feather."""
        import cv2
        import numpy as np
        
        # Load as BGR (GrabCut needs 3 channels)
        img = cv2.imread(str(input_path))
        if img is None:
             raise ValueError("Could not load image via OpenCV")
             
        # 1. Flood Fill Mask (High Tolerance to catch noise)
        # Create a mask for floodFill (h+2, w+2)
        h, w = img.shape[:2]
        mask_flood = np.zeros((h + 2, w + 2), np.uint8)
        
        # Seed points: corners
        seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
        tolerance = (50, 50, 50)
        flags = cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE | (255 << 8)
        
        for seed in seeds:
            if mask_flood[seed[1] + 1, seed[0] + 1] == 0:
                cv2.floodFill(img, mask_flood, seed, (0,0,0), tolerance, tolerance, flags)
        
        mask_flood = mask_flood[1:h+1, 1:w+1]
        mask_fg_flood = cv2.bitwise_not(mask_flood) # White = Object
        
        # 2. GrabCut Mask
        mask_grab = np.zeros((h, w), np.uint8)
        bgdModel = np.zeros((1,65), np.float64)
        fgdModel = np.zeros((1,65), np.float64)
        rect = (2, 2, w - 4, h - 4)
        
        try:
            cv2.grabCut(img, mask_grab, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        except:
            mask_grab = np.ones((h, w), np.uint8) * 3 # Fallback to all ProbFG
            
        mask_fg_grab = np.where((mask_grab==2)|(mask_grab==0), 0, 255).astype('uint8')
        
        # 3. Combine: Intersection
        final_mask = cv2.bitwise_and(mask_fg_flood, mask_fg_grab)
        
        # 4. Refine: Keep Largest Contour Only (Removes noise, Fills internal holes)
        contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Find largest contour (The Unit)
            c_max = max(contours, key=cv2.contourArea)
            
            # Create a clean mask with just the largest object filled
            # This fixes cases where FloodFill ate into the armor (holes)
            clean_mask = np.zeros_like(final_mask)
            cv2.drawContours(clean_mask, [c_max], -1, 255, -1) 
            final_mask = clean_mask
        
        # 5. Erode (Remove halo)
        kernel = np.ones((5,5), np.uint8)
        final_mask = cv2.erode(final_mask, kernel, iterations=1)
        
        # 6. Feather
        final_mask = cv2.GaussianBlur(final_mask, (5, 5), 1.0)
        
        # Apply to Alpha
        b, g, r = cv2.split(img)
        result = cv2.merge([b, g, r, final_mask])
        
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA)
        return Image.fromarray(result_rgb)

    def is_available(self) -> bool:
        return True

    def get_name(self) -> str:
        return "rembg" if rembg_available else "heuristic"

    def clear_session(self) -> None:
        """Clear the cached model session."""
        self._session = None
        self._current_model = None

