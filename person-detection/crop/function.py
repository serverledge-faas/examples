import base64
import time
import io
from PIL import Image


def extract_person_crops(base64_string, person_bboxes, padding=0):
    """
    Extract cropped images for each person bounding box from a base64-encoded image.
    
    Args:
        base64_string (str): Base64-encoded image string
        person_bboxes (list): List of bounding boxes in format [x1, y1, x2, y2]
                             or list of dicts with 'bbox' key
        padding (int): Extra pixels to add around each crop (default: 0)
    
    Returns:
        list: List of PIL Image objects, one for each person
    """
    # Remove data URL prefix if present
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    # Decode base64 to image
    img_bytes = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_bytes))
    img_width, img_height = img.size
    
    cropped_images = []
    
    for i, bbox_data in enumerate(person_bboxes):
        # Handle both list format and dict format
        if isinstance(bbox_data, dict):
            bbox = bbox_data['bbox']
        else:
            bbox = bbox_data
        
        x1, y1, x2, y2 = bbox
        
        # Add padding and ensure within image bounds
        x1 = max(0, int(x1 - padding))
        y1 = max(0, int(y1 - padding))
        x2 = min(img_width, int(x2 + padding))
        y2 = min(img_height, int(y2 + padding))
        
        # Crop the image
        cropped = img.crop((x1, y1, x2, y2))
        cropped_images.append(cropped)
        
        print(f"Person {i+1}: Cropped region ({x1}, {y1}) to ({x2}, {y2}), size: {x2-x1}x{y2-y1}")
    
    return cropped_images




def handler (params, context):
    if not "Img" in params or not "Detections" in params:
        return {"Status": False}

    img = params["Img"]
    boxes = []
    for d in params["Detections"]:
        box = [float(x) for x in d.split(",")]
        boxes.append(box)

    response = {}

    cropped_images = extract_person_crops(img, boxes, 10)
    encoded_images = []
    for ci in cropped_images:
        fmt = ci.format or "PNG"  # fallback to PNG if format is unknown
        buffer = io.BytesIO()
        ci.save(buffer, format=fmt)
        b64_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
        encoded_images.append(b64_string)

    response["Objects"] = encoded_images

    return response
