import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Tuple, Optional


def resize_image(
    image_path: str,
    output_path: str,
    max_size: Tuple[int, int] = (800, 800),
    maintain_aspect_ratio: bool = True
) -> bool:
    """
    Resize an image

    Args:
        image_path: Path to input image
        output_path: Path to save resized image
        max_size: Maximum dimensions (width, height)
        maintain_aspect_ratio: Whether to maintain aspect ratio

    Returns:
        True if successful, False otherwise
    """
    try:
        img = Image.open(image_path)

        if maintain_aspect_ratio:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        else:
            img = img.resize(max_size, Image.Resampling.LANCZOS)

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        img.save(output_path, optimize=True, quality=85)
        return True

    except Exception as e:
        print(f"Error resizing image: {e}")
        return False


def extract_dominant_colors(image_path: str, n_colors: int = 3) -> list:
    """
    Extract dominant colors from an image using K-means clustering

    Args:
        image_path: Path to image
        n_colors: Number of dominant colors to extract

    Returns:
        List of RGB color tuples
    """
    try:
        # Read image
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Reshape image to be a list of pixels
        pixels = img.reshape(-1, 3)

        # Convert to float32
        pixels = np.float32(pixels)

        # Define criteria and apply K-means
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(
            pixels,
            n_colors,
            None,
            criteria,
            10,
            cv2.KMEANS_RANDOM_CENTERS
        )

        # Convert back to uint8
        centers = np.uint8(centers)

        # Get dominant colors
        colors = [tuple(color) for color in centers]

        return colors

    except Exception as e:
        print(f"Error extracting colors: {e}")
        return []


def color_name_from_rgb(rgb: Tuple[int, int, int]) -> str:
    """
    Get approximate color name from RGB values

    Args:
        rgb: RGB tuple (r, g, b)

    Returns:
        Color name string
    """
    r, g, b = rgb

    # Simple color mapping
    if r > 200 and g > 200 and b > 200:
        return "white"
    elif r < 50 and g < 50 and b < 50:
        return "black"
    elif r > g and r > b:
        if r > 200:
            return "red"
        else:
            return "brown"
    elif g > r and g > b:
        return "green"
    elif b > r and b > g:
        return "blue"
    elif r > 150 and g > 150:
        return "yellow"
    elif r > 150 and b > 150:
        return "purple"
    elif g > 150 and b > 150:
        return "cyan"
    elif r > 100 and g > 100 and b > 100:
        return "gray"
    else:
        return "multicolor"


def get_image_dominant_color_name(image_path: str) -> str:
    """
    Get the name of the dominant color in an image

    Args:
        image_path: Path to image

    Returns:
        Color name
    """
    colors = extract_dominant_colors(image_path, n_colors=1)
    if colors:
        return color_name_from_rgb(colors[0])
    return "unknown"


def crop_to_square(image_path: str, output_path: Optional[str] = None) -> bool:
    """
    Crop image to square (center crop)

    Args:
        image_path: Path to input image
        output_path: Path to save cropped image (if None, overwrites original)

    Returns:
        True if successful, False otherwise
    """
    try:
        img = Image.open(image_path)
        width, height = img.size

        # Calculate crop box
        if width > height:
            left = (width - height) // 2
            top = 0
            right = left + height
            bottom = height
        else:
            left = 0
            top = (height - width) // 2
            right = width
            bottom = top + width

        # Crop
        img_cropped = img.crop((left, top, right, bottom))

        # Save
        save_path = output_path or image_path
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        img_cropped.save(save_path)

        return True

    except Exception as e:
        print(f"Error cropping image: {e}")
        return False


def remove_background(image_path: str, output_path: str) -> bool:
    """
    Remove background from image (simple implementation using edge detection)
    Note: For production, consider using rembg library or ML-based solutions

    Args:
        image_path: Path to input image
        output_path: Path to save processed image

    Returns:
        True if successful, False otherwise
    """
    try:
        # Read image
        img = cv2.imread(image_path)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur to reduce noise
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply threshold
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create mask
        mask = np.zeros(img.shape[:2], dtype=np.uint8)

        if contours:
            # Draw largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            cv2.drawContours(mask, [largest_contour], -1, 255, -1)

        # Apply mask
        result = cv2.bitwise_and(img, img, mask=mask)

        # Save with alpha channel
        b, g, r = cv2.split(result)
        rgba = cv2.merge([b, g, r, mask])

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(output_path, rgba)

        return True

    except Exception as e:
        print(f"Error removing background: {e}")
        return False
