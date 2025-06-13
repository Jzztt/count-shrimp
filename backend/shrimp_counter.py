import cv2
import numpy as np
import imutils
from pathlib import Path

class ShrimpCounter:
    def __init__(self):
        # Các tham số cho việc xử lý ảnh
        self.min_area = 500  # Diện tích tối thiểu của đối tượng
        self.max_area = 5000  # Diện tích tối đa của đối tượng
        
    def preprocess_image(self, image):
        """Tiền xử lý ảnh"""
        # Chuyển sang ảnh xám
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Làm mờ ảnh để giảm nhiễu
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        return blurred
    
    def detect_shrimps(self, image):
        """Phát hiện tôm trong ảnh"""
        # Tiền xử lý ảnh
        processed = self.preprocess_image(image)
        
        # Phân ngưỡng ảnh
        _, thresh = cv2.threshold(processed, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Tìm contours
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        
        # Lọc contours theo diện tích
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.min_area < area < self.max_area:
                valid_contours.append(contour)
        
        return valid_contours
    
    def count_shrimps(self, image_path):
        """Đếm số lượng tôm trong ảnh"""
        # Đọc ảnh
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Không thể đọc ảnh từ đường dẫn: {image_path}")
        
        # Phát hiện tôm
        shrimp_contours = self.detect_shrimps(image)
        
        # Vẽ kết quả
        result_image = image.copy()
        for contour in shrimp_contours:
            cv2.drawContours(result_image, [contour], -1, (0, 255, 0), 2)
        
        # Hiển thị số lượng tôm
        count = len(shrimp_contours)
        cv2.putText(result_image, f"So luong tom: {count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return result_image, count

def main():
    counter = ShrimpCounter()
    
    # Thư mục chứa ảnh đầu vào
    input_dir = Path("input_images")
    input_dir.mkdir(exist_ok=True)
    
    # Thư mục lưu kết quả
    output_dir = Path("output_images")
    output_dir.mkdir(exist_ok=True)
    
    print("Chuong trinh dem Tom")
    print("1. Dat anh can dem vao thu muc 'input_images'")
    print("2. Ket qua se duoc luu vao thu muc 'output_images'")
    
    # Xử lý tất cả ảnh trong thư mục input
    for image_path in input_dir.glob("*.jpg"):
        try:
            result_image, count = counter.count_shrimps(image_path)
            
            # Lưu ảnh kết quả
            output_path = output_dir / f"result_{image_path.name}"
            cv2.imwrite(str(output_path), result_image)
            
            print(f"Da xu ly anh {image_path.name}: {count} con tom")
        except Exception as e:
            print(f"Loi khi xu ly anh {image_path.name}: {str(e)}")

if __name__ == "__main__":
    main() 