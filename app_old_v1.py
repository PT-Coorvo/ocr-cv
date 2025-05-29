from flask import Flask, request, jsonify
import easyocr
import numpy as np
from PIL import Image
import io
import os
from dotenv import load_dotenv
import mimetypes
from pdf2image import convert_from_bytes

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_data, file_ext):
    """Process the image or PDF and extract text using EasyOCR."""
    try:
        if file_ext == 'pdf':
            images = convert_from_bytes(image_data, poppler_path=r"E:\Projects\lib-py\poppler-24.08.0\Library\bin")
            all_results = []
            for page_num, image in enumerate(images, 1):
                image_np = np.array(image)
                results = reader.readtext(image_np)
                page_data = []
                for (bbox, text, prob) in results:
                    # Convert NumPy numeric types to native Python types
                    bbox_list = [[float(x) for x in point] for point in bbox]
                    page_data.append({
                        'text': text,
                        'confidence': float(prob),
                        'position': bbox_list
                    })
                all_results.append({'page': page_num, 'data': page_data})
            return all_results
        else:
            image = Image.open(io.BytesIO(image_data))
            image_np = np.array(image)
            results = reader.readtext(image_np)
            extracted_data = []
            for (bbox, text, prob) in results:
                # Convert NumPy numeric types to native Python types
                bbox_list = [[float(x) for x in point] for point in bbox]
                extracted_data.append({
                    'text': text,
                    'confidence': float(prob),
                    'position': bbox_list
                })
            return extracted_data
    except Exception as e:
        return str(e)

@app.route('/ocr', methods=['POST'])
def ocr_endpoint():
    """API endpoint for OCR processing."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400
    
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    
    try:
        # Read the image file
        image_data = file.read()
        
        # Process the image
        results = process_image(image_data, file_ext)
        
        return jsonify({
            'success': True,
            'data': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 