# Hệ Thống Đếm Tôm

Đây là một ứng dụng web để đếm số lượng tôm trong ảnh sử dụng kỹ thuật xử lý ảnh, được xây dựng với React (Frontend) và Flask (Backend).

## Cấu trúc dự án

```
project/
├── web_app/          # Frontend React application
└── backend/          # Backend Flask API
```

## Yêu cầu hệ thống

### Frontend (React)
- Node.js 14.0 trở lên
- npm hoặc yarn

### Backend (Flask)
- Python 3.7 trở lên
- OpenCV
- NumPy
- Imutils

## Cài đặt

### Frontend
1. Di chuyển vào thư mục web_app:
```bash
cd web_app
```

2. Cài đặt dependencies:
```bash
npm install
# hoặc
yarn install
```

3. Chạy ứng dụng React:
```bash
npm start
# hoặc
yarn start
```

### Backend
1. Di chuyển vào thư mục backend:
```bash
cd backend
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

4. Chạy Flask server:
```bash
python app.py
```

## Cách sử dụng

1. Truy cập ứng dụng web tại `http://localhost:3000`
2. Tải lên ảnh cần đếm tôm
3. Hệ thống sẽ tự động xử lý và hiển thị kết quả

## Các tính năng

- Giao diện web thân thiện với người dùng
- Tự động phát hiện và đếm số lượng tôm trong ảnh
- Hiển thị kết quả trực quan với đường viền xanh quanh mỗi con tôm
- Hiển thị số lượng tôm được đếm trên ảnh kết quả
- Xử lý được nhiều ảnh cùng lúc

## API Endpoints

### `/api/count-shrimp`
- Method: POST
- Content-Type: multipart/form-data
- Parameter: image (file)

### Response format:
```json
{
    "success": true,
    "shrimp_count": 10,
    "live_shrimp": 6,
    "cooked_shrimp": 4,
    "debug_info": {
        // Thông tin debug chi tiết
    }
}
```

## Lưu ý

- Ảnh đầu vào nên có độ phân giải tốt và độ tương phản rõ ràng
- Các con tôm không nên chồng lấn lên nhau quá nhiều
- Hỗ trợ các file ảnh định dạng .jpg, .jpeg, .png
- API có thể phân biệt giữa tôm sống và tôm chín

# API Đếm Tôm

API này cung cấp khả năng đếm số lượng tôm từ ảnh sử dụng xử lý ảnh và computer vision.

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

## Chạy API

### Phát triển
```bash
python api.py
```

### Production với Gunicorn (Linux/Mac)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

### Production với Waitress (Windows)
```bash
waitress-serve --port=5000 api:app
```

## Sử dụng API

### Endpoint: `/api/count-shrimp`
- Method: POST
- Content-Type: multipart/form-data
- Parameter: image (file)

### Ví dụ sử dụng với cURL:
```bash
curl -X POST -F "image=@path/to/your/image.jpg" http://localhost:5000/api/count-shrimp
```

### Ví dụ sử dụng với Python:
```python
import requests

url = "http://localhost:5000/api/count-shrimp"
files = {"image": open("path/to/your/image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Response format:
```json
{
    "success": true,
    "shrimp_count": 10,
    "live_shrimp": 6,
    "cooked_shrimp": 4,
    "debug_info": {
        // Thông tin debug chi tiết
    }
}
```

## Lưu ý
- API chấp nhận các định dạng ảnh: JPG, JPEG, PNG
- Kích thước ảnh nên phù hợp để có kết quả tốt nhất
- API có thể phân biệt giữa tôm sống và tôm chín
- Thông tin debug được trả về để giúp điều chỉnh và tối ưu kết quả 