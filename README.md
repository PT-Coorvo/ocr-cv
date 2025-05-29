# CV OCR System

This is a Flask-based OCR system that uses EasyOCR to extract text from CV/resume images.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. OCR Processing
- **Endpoint**: `/ocr`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameter**: `file` (image file)
- **Response**: JSON containing extracted text and confidence scores

Example using curl:
```bash
curl -X POST -F "file=@path/to/your/cv.jpg" http://localhost:5000/ocr
```

### 2. Health Check
- **Endpoint**: `/health`
- **Method**: GET
- **Response**: JSON with server status

## Response Format

The OCR endpoint returns data in the following format:
```json
{
    "success": true,
    "data": [
        {
            "text": "extracted text",
            "confidence": 0.95,
            "position": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        }
    ]
}
```

## Error Handling

The API returns appropriate error messages in case of:
- Missing file
- Invalid file format
- Processing errors

## Environment Variables

Create a `.env` file to configure:
- `PORT`: Server port (default: 5000) 