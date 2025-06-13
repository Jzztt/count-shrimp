import os
from flask import Flask, request, render_template, jsonify
import cv2
import numpy as np
from PIL import Image
import io
from roboflow import Roboflow
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)

# Cấu hình thư mục upload
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Roboflow
rf = Roboflow(api_key="iTdgWxNJUbh2PhmMYwHa")
project = rf.workspace().project("shrimp__coun")
model = project.version(3).model

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_shrimp_roboflow(image_path):
    """
    Detect shrimp using Roboflow model
    """
    try:
        # Predict on an image
        predictions = model.predict(image_path, confidence=40, overlap=30).json()
        
        # Draw predictions on image
        img = cv2.imread(image_path)
        count = len(predictions['predictions'])  # Get total predictions
        
        # Draw each prediction
        for prediction in predictions['predictions']:
            # Get bounding box coordinates
            x = prediction['x']
            y = prediction['y']
            width = prediction['width']
            height = prediction['height']
            confidence = prediction['confidence']
            
            # Convert coordinates to integers for drawing
            x1 = int(x - width/2)
            y1 = int(y - height/2)
            x2 = int(x + width/2)
            y2 = int(y + height/2)
            
            # Draw bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue color for Roboflow
            
            # Add confidence text
            conf_text = f"{confidence:.2f}"
            cv2.putText(img, conf_text, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        
        # Add total count text
        cv2.putText(img, f"Shrimp Count: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        # Generate unique filename with timestamp
        timestamp = int(time.time())
        result_filename = f'result_{timestamp}.jpg'
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
        cv2.imwrite(result_path, img)
        
        return count, result_filename
    except Exception as e:
        print(f"Error in Roboflow detection: {str(e)}")
        return 0, None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if file and allowed_file(file.filename):
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Use Roboflow for detection
            count, result_filename = detect_shrimp_roboflow(filepath)
            
            # Clean up old result files
            for old_file in os.listdir(app.config['UPLOAD_FOLDER']):
                if old_file.startswith('result_') and old_file != result_filename:
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_file))
                    except:
                        pass
            
            return jsonify({
                'count': count,
                'result_image': result_filename
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    # Create static folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True) 