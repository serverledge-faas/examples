# pip install ultralytics pillow numpy
import base64
import io
from PIL import Image
import numpy as np
from ultralytics import YOLO


def detect_objects_from_base64(base64_string, model=None, model_path='yolov8n.pt', conf_threshold=0.25):
    """
    Detect objects in a base64-encoded image using YOLO.
    
    Args:
        base64_string (str): Base64-encoded image string
        model (YOLO, optional): Pre-loaded YOLO model instance. If None, loads from model_path
        model_path (str): Path to YOLO model weights (default: yolov8n.pt)
        conf_threshold (float): Confidence threshold for detections (default: 0.25)
    
    Returns:
        dict: Dictionary containing:
            - 'detections': List of detected objects with their properties
            - 'image': PIL Image object with detection boxes drawn
            - 'results': Raw YOLO results object
    """
    # Remove data URL prefix if present (e.g., "data:image/jpeg;base64,")
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    # Decode base64 to image
    img_bytes = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_bytes))
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Load YOLO model (use provided model or load from path)
    if model is None:
        model = YOLO(model_path)
    
    # Run inference
    results = model(img, conf=conf_threshold)

    # Get boxes
    result = results[0]
    boxes = result.boxes
    person_boxes = []
    
    # Iterate through each detection
    for box in boxes:
        # Get bounding box coordinates (xyxy format)
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        
        # Get class ID
        class_id = int(box.cls[0])
        
        # Get class name
        class_name = result.names[class_id]

        print(f"Class: {class_name}, Box: ({x1}, {y1}, {x2}, {y2})")

        if class_name.lower() == "person":
            person_boxes.append(f"{x1},{y1},{x2},{y2}")
    return person_boxes
        
    # Get annotated image
    #annotated_img = results[0].plot()
    #annotated_img = Image.fromarray(annotated_img)
    

def handler (params, context):
    if not "img" in params:
        return {}
    img = params["img"]

    response = {}

    person_boxes = detect_objects_from_base64(img)
    
    response["Count"] = len(person_boxes)
    response["Detections"] = person_boxes
    response["Img"] = img

    return response

