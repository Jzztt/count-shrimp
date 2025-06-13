from flask import Flask, request, jsonify
import cv2
import numpy as np
from shrimp_counter import process_image, enhance_image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Cấu hình upload
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/count-shrimp', methods=['POST'])
def count_shrimp():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    try:
        # Đọc và xử lý ảnh
        file_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Tăng cường chất lượng ảnh
        enhanced_image = enhance_image(image)
        
        # Đếm tôm
        result, debug_info = process_image(enhanced_image)
        
        return jsonify({
            'success': True,
            'shrimp_count': result['total_count'],
            'live_shrimp': result.get('live_count', 0),
            'cooked_shrimp': result.get('cooked_count', 0),
            'debug_info': debug_info
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 