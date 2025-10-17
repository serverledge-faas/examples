# pip install ultralytics pillow numpy
import base64
import io
from PIL import Image

def resize_base64_image(base64_string, max_size=500):
    """
    Resize a base64-encoded image to fit within max_size x max_size while preserving aspect ratio.
    
    Args:
        base64_string (str): Base64-encoded image string
        max_size (int): Maximum width or height in pixels (default: 500)
    
    Returns:
        str: Base64-encoded string of the resized image
    """
    # Remove data URL prefix if present
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    # Decode base64 to image
    img_bytes = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_bytes))
    
    # Get original dimensions
    original_width, original_height = img.size
    print(f"Original size: {original_width}x{original_height}")
    
    # Calculate new dimensions preserving aspect ratio
    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    new_width, new_height = img.size
    print(f"Resized to: {new_width}x{new_height}")
    
    # Convert back to base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=95)
    img_bytes = buffer.getvalue()
    resized_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return resized_base64


def handler (params, context):
    if not "img" in params:
        return {}
    img = params["img"]

    response = {}
    response["img"] = resize_base64_image(img)

    return response

