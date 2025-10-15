from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import cv2
import numpy as np
import base64
from PIL import Image, ImageDraw
import io

app = Flask(__name__)
CORS(app)




@app.route('/detect-teeth', methods=['POST'])
def detect_teeth():
    """
    Endpoint 1: Detects teeth in the image and returns their positions
    """
    try:
        data = request.json
        image_base64 = data.get('image')
        
        if not image_base64:
            return jsonify({'error': 'No image provided'}), 400
        
        # Remove data URL prefix if present
        if 'base64,' in image_base64:
            image_base64 = image_base64.split('base64,')[1]
        
        # Decode base64 to image
        image_bytes = base64.b64decode(image_base64)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        height, width = image.shape[:2]
        
        # Prepare API request to Roboflow
        url = f"https://detect.roboflow.com/{MODEL_ID}/{MODEL_VERSION}"
        params = {"api_key": API_KEY, "confidence": 40, "overlap": 30}
        
        # Convert to bytes
        _, encoded_image = cv2.imencode(".jpg", image)
        response = requests.post(
            url, 
            files={"file": encoded_image.tobytes()}, 
            params=params
        )
        
        result = response.json()
        predictions = result.get("predictions", [])
        
        if predictions:
            # Return teeth data for frontend processing
            teeth_data = []
            for pred in predictions:
                teeth_data.append({
                    'x': pred['x'],
                    'y': pred['y'],
                    'width': pred['width'],
                    'height': pred['height'],
                    'confidence': pred.get('confidence', 0)
                })
            
            return jsonify({
                'success': True,
                'teeth_count': len(predictions),
                'teeth': teeth_data,
                'image_dimensions': {
                    'width': width,
                    'height': height
                }
            })
        else:
            return jsonify({
                'success': False,
                'teeth_count': 0,
                'message': 'No teeth detected'
            })
            
    except Exception as e:
        print(f"Error in detect_teeth: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/apply-brackets', methods=['POST'])
def apply_brackets():
    """
    Endpoint 2: Applies bracket overlays to detected teeth
    This is where metal.png or ceramic.png gets overlaid on EACH tooth
    """
    try:
        data = request.json
        image_base64 = data.get('image')
        bracket_type = data.get('bracket_type')  # 'metal' or 'ceramic'
        teeth_data = data.get('teeth')  # List of detected teeth positions
        
        if not all([image_base64, bracket_type, teeth_data]):
            return jsonify({'error': 'Missing required data'}), 400
        
        # Decode image
        if 'base64,' in image_base64:
            image_base64 = image_base64.split('base64,')[1]
        
        image_bytes = base64.b64decode(image_base64)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to PIL for easier manipulation
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        
        # Load bracket image based on type (FROM YOUR ASSETS FOLDER)
        try:
            if bracket_type == 'metal':
                bracket_img = Image.open('assets/metal.png').convert('RGBA')
            elif bracket_type == 'ceramic':
                bracket_img = Image.open('assets/ceramic.png').convert('RGBA')
            else:
                return jsonify({'error': 'Invalid bracket type'}), 400
        except FileNotFoundError:
            return jsonify({'error': f'Bracket image not found: assets/{bracket_type}.png'}), 500
        
        # Convert main image to RGBA for transparency support
        if pil_image.mode != 'RGBA':
            pil_image = pil_image.convert('RGBA')
        
        # Create overlay layer
        overlay = Image.new('RGBA', pil_image.size, (0, 0, 0, 0))
        
        # THIS LOOP APPLIES BRACKET TO EACH INDIVIDUAL TOOTH
        for tooth in teeth_data:
            # Calculate bracket size (proportional to tooth size)
            bracket_width = int(tooth['width'] * 1.1)  # 90% of tooth width
            bracket_height = int(tooth['height'] * 1.1)  # 90% of tooth height
            
            # Resize bracket to fit this specific tooth
            resized_bracket = bracket_img.resize(
                (bracket_width, bracket_height), 
                Image.Resampling.LANCZOS
            )
            
            # Calculate position (center bracket on tooth)
            x = int(tooth['x'] - bracket_width // 2)
            y = int(tooth['y'] - bracket_height // 2)
            
            # Paste bracket with transparency on this tooth
            overlay.paste(resized_bracket, (x, y), resized_bracket)
        
        # Composite the images (combine original + overlays)
        result_image = Image.alpha_composite(pil_image, overlay)
        
        # Convert back to RGB for JPEG encoding
        result_image = result_image.convert('RGB')
        
        # Convert to base64 to send back to frontend
        buffered = io.BytesIO()
        result_image.save(buffered, format="JPEG", quality=95)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'processed_image': img_str,
            'teeth_count': len(teeth_data),
            'bracket_type': bracket_type
        })
        
    except Exception as e:
        print(f"Error in apply_brackets: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)