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
from flask_cors import CORS
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
CORS(app)

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

# def detect_shrimp_traditional(image_path):
#     """
#     Detect shrimp using traditional computer vision methods
#     """
#     try:
#         # Read image
#         img = cv2.imread(image_path)
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
#         # Preprocessing
#         # Apply Gaussian blur to reduce noise
#         blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
#         # Enhance contrast using CLAHE
#         clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#         enhanced = clahe.apply(blurred)
        
#         # Thresholding
#         _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
#         # Morphological operations to remove noise
#         kernel = np.ones((3,3), np.uint8)
#         opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
#         # Find contours
#         contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
#         # Filter contours based on area and shape
#         shrimp_contours = []
#         shrimp_features = []
        
#         for contour in contours:
#             area = cv2.contourArea(contour)
#             perimeter = cv2.arcLength(contour, True)
            
#             # Filter based on area (adjust these thresholds based on your images)
#             if 100 < area < 5000:  # Adjust these values based on your shrimp size
#                 # Calculate shape features
#                 if perimeter > 0:
#                     thinness_ratio = 4 * np.pi * area / (perimeter * perimeter)
                    
#                     # Only keep contours with reasonable thinness ratio
#                     if 0.1 < thinness_ratio < 0.8:  # Adjust based on your shrimp shape
#                         shrimp_contours.append(contour)
#                         shrimp_features.append([area, perimeter, thinness_ratio])
        
#         # Draw results
#         result_img = img.copy()
#         for contour in shrimp_contours:
#             cv2.drawContours(result_img, [contour], -1, (0, 255, 0), 2)
            
#             # Calculate and display features
#             M = cv2.moments(contour)
#             if M["m00"] != 0:
#                 cx = int(M["m10"] / M["m00"])
#                 cy = int(M["m01"] / M["m00"])
#                 area = cv2.contourArea(contour)
#                 perimeter = cv2.arcLength(contour, True)
#                 cv2.putText(result_img, f"A:{int(area)}", (cx-20, cy), 
#                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
#         # Add total count
#         cv2.putText(result_img, f"Shrimp Count: {len(shrimp_contours)}", (10, 30), 
#                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
#         # Save result image
#         timestamp = int(time.time())
#         result_filename = f'result_traditional_{timestamp}.jpg'
#         result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
#         cv2.imwrite(result_path, result_img)
        
#         # Prepare features for response
#         features = []
#         for i, contour in enumerate(shrimp_contours):
#             area = cv2.contourArea(contour)
#             perimeter = cv2.arcLength(contour, True)
#             features.append({
#                 'id': i+1,
#                 'area': int(area),
#                 'perimeter': int(perimeter)
#             })
        
#         return len(shrimp_contours), result_filename, features
        
#     except Exception as e:
#         print(f"Error in traditional detection: {str(e)}")
#         return 0, None, []

def detect_shrimp_traditional(image_path):
    """
    Phát hiện và đếm ấu trùng tôm bằng adaptive threshold, đơn giản hóa từ phiên bản Jupyter.
    
    Parameters:
    - image_path: đường dẫn ảnh

    Returns:
    - shrimp_count: số lượng ấu trùng
    - result_filename: tên file kết quả đã lưu
    - features: danh sách dict các đặc trưng {id, area, perimeter}
    """
    try:
        # Đọc ảnh
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Không thể đọc ảnh!")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        # Adaptive threshold
        thresh = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            15, 3
        )

        # Tìm contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Lọc theo diện tích
        min_area = 10
        max_area = 100
        shrimp_count = 0
        features = []
        result_img = image.copy()

        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if min_area < area < max_area:
                shrimp_count += 1
                perimeter = cv2.arcLength(contour, True)
                features.append({
                    'id': shrimp_count,
                    'area': int(area),
                    'perimeter': int(perimeter)
                })
                cv2.drawContours(result_img, [contour], -1, (0, 255, 0), 1)

        # Ghi chú số lượng tôm lên ảnh
        cv2.putText(result_img, f'Shrimp Larvae Count: {shrimp_count}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Lưu ảnh kết quả
        timestamp = int(time.time())
        result_filename = f'result_traditional_{timestamp}.jpg'
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
        cv2.imwrite(result_path, result_img)

        return shrimp_count, result_filename, features

    except Exception as e:
        print(f"Lỗi phát hiện ấu trùng: {str(e)}")
        return 0, None, []

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

@app.route('/classic-process', methods=['POST'])
def process_image_traditional():
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
            # Use traditional method for detection
            count, result_filename, features = detect_shrimp_traditional(filepath)
            
            # Clean up old result files
            for old_file in os.listdir(app.config['UPLOAD_FOLDER']):
                if old_file.startswith('result_traditional_') and old_file != result_filename:
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_file))
                    except:
                        pass
            
            return jsonify({
                'count': count,
                'result_image': result_filename,
                'features': features
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    # Create static folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True) 