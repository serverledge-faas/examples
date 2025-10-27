import base64
import json


def encode_image_to_base64(image_path):
    """
    Encode an image file to base64 string.
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        str: Base64-encoded string of the image
    """
    with open(image_path, 'rb') as img_file:
        img_bytes = img_file.read()
        base64_string = base64.b64encode(img_bytes).decode('utf-8')
    
    return base64_string


def encode_image_with_data_url(image_path):
    """
    Encode an image file to base64 with data URL prefix.
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        str: Base64-encoded string with data URL prefix (e.g., data:image/jpeg;base64,...)
    """
    # Determine MIME type from extension
    extension = image_path.lower().split('.')[-1]
    mime_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'bmp': 'image/bmp',
        'webp': 'image/webp'
    }
    mime_type = mime_types.get(extension, 'image/jpeg')
    
    with open(image_path, 'rb') as img_file:
        img_bytes = img_file.read()
        base64_string = base64.b64encode(img_bytes).decode('utf-8')
    
    return f"data:{mime_type};base64,{base64_string}"


if __name__ == "__main__":
    import sys

    image_path = sys.argv[1] if len(sys.argv) > 1 else "image.jpg"
    
    # Encode image to base64
    base64_str = encode_image_to_base64(image_path)
    
    # Create JSON object
    json_data = {
        "img": base64_str
    }
    
    # Save to input.json
    with open("input.json", "w") as f:
        json.dump(json_data, f, indent=2)
    
    print(f"✓ Image encoded successfully!")
    print(f"✓ Base64 length: {len(base64_str)} characters")
    print(f"✓ JSON saved to 'input.json'")
    
    # Preview the JSON structure
    print(f"\nJSON structure preview:")
    print(f'{{"img": "{base64_str[:50]}..."}}')
