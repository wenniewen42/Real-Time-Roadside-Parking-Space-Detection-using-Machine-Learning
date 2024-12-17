import requests
import os
import uuid
import cv2
import time

# 設置 ngrok 公網 URL 和上傳端點
NGROK_URL = "https://4f4e-140-118-154-191.ngrok-free.app/upload"  # 更改為你的 ngrok 公網 URL
UPLOAD_FOLDER = "uploads"  # 保存圖片的資料夾

# 創建圖片保存資料夾（如果不存在）
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 開啟攝像頭並拍攝圖片
def capture_image():
    # 打開攝像頭
    cap = cv2.VideoCapture(0)
    
    # 檢查攝像頭是否正常打開
    if not cap.isOpened():
        print("Error: Camera not accessible")
        return None
    
    # 讀取一幀圖像
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        cap.release()  # 確保資源被釋放
        return None
    
    # 生成唯一文件名並保存圖片
    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    cv2.imwrite(filepath, frame)
    
    # 釋放攝像頭資源
    cap.release()
    return filepath

# 上傳圖片到 ngrok URL
def upload_image(filepath):
    try:
        with open(filepath, 'rb') as file:
            # 添加圖片和表單數據到請求
            files = {'file': (os.path.basename(filepath), file)}
            data = {'point_id': 1}  # 添加 point_id

            # 發送 POST 請求
            response = requests.post(NGROK_URL, files=files, data=data)
            
        if response.status_code == 200:
            print(f"Image {filepath} uploaded successfully!")
        else:
            print(f"Failed to upload image {filepath}, status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error during upload: {e}")

# 每分鐘自動拍攝並上傳
def auto_capture_and_upload():
    try:
        while True:
            print("Capturing image...")
            image_path = capture_image()
            if image_path:
                print(f"Uploading image {image_path}...")
                upload_image(image_path,1)
            
            # 等待1分鐘後再次執行
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting gracefully.")

# 開始自動拍攝和上傳
if __name__ == "__main__":
    auto_capture_and_upload()
