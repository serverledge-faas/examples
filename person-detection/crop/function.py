import base64
import time
import io
from PIL import Image
import minioclient


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


def save_person_crops(base64_string, person_bboxes, output_prefix="person", padding=0):
    """
    Extract and save cropped images for each person bounding box.
    
    Args:
        base64_string (str): Base64-encoded image string
        person_bboxes (list): List of bounding boxes
        output_prefix (str): Prefix for output filenames (default: "person")
        padding (int): Extra pixels to add around each crop (default: 0)
    
    Returns:
        list: List of saved filenames
    """
    cropped_images = extract_person_crops(base64_string, person_bboxes, padding)

    minioclient.ensure_bucket()
    
    saved_files = []
    for i, crop in enumerate(cropped_images, 1):
        filename = f"{output_prefix}_{i}.jpg"
        crop.save(filename, quality=95)

        object_name=str(time.time())+".jpg"
        minioclient.upload_file(filename, object_name)
        saved_files.append(object_name)
        print(f"Saved: {object_name}")
    
    return saved_files


def handler (params, context):
    if not "Img" in params or not "Detections" in params:
        return {"Status": False}

    img = params["Img"]
    boxes = []
    for d in params["Detections"]:
        box = [float(x) for x in d.split(",")]
        boxes.append(box)

    response = {}

    objects = save_person_crops(img, boxes, output_prefix="person", padding=10)
    
    response["Objects"] = objects

    return response
