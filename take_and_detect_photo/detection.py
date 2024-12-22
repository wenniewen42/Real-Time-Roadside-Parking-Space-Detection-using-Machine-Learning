import os
from flask import Flask, request, jsonify
from pyngrok import ngrok
import uuid
import requests
from roboflow import Roboflow
from PIL import Image, ImageDraw, ImageFont

# 初始化 Flask 應用
app = Flask(__name__)

# 設置上傳目錄
UPLOAD_FOLDER = './received_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 設置允許的圖片格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 判斷文件擴展名是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 初始化 Roboflow API
rf = Roboflow(api_key="rz6p8Cn7xhg4M8MbHp0M")
project = rf.workspace().project("parking-space-detection-sfq4x")
model = project.version(1).model

@app.route('/upload', methods=['POST'])
def upload_file():
    # 確保請求中包含文件
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    # 確保請求中包含 point_id 並進行檢查
    point_id = request.form.get('point_id')
    if not point_id or not point_id.isdigit():
        return jsonify({"error": "Invalid or missing point_id"}), 400
    point_id = int(point_id)

    # 儲存文件
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # 執行檢測並傳遞 point_id
    output_folder='detected_images' # 結果保存文件夾
    detect_parking_spaces(filepath, output_folder, point_id)

    return jsonify({"message": f"File {filename} uploaded successfully!", "point_id": point_id}), 200


def detect_parking_spaces(image_path, output_path, point_id):
    # 推理圖片並獲取 JSON 結果
    results = model.predict(image_path, confidence=50, overlap=30).json()

    # 計算不同類別的停車位數量
    parking_spot_count = sum(1 for p in results['predictions'] if p['class'] == 'parking spot')

    print(f"Detected parking spots: {parking_spot_count}")

    # 打開原始圖片
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # 確保儲存資料夾存在
    os.makedirs(output_path, exist_ok=True)

    # 根據原始圖片名稱生成儲存的檔案路徑
    base_name = os.path.basename(image_path)
    name_without_ext = os.path.splitext(base_name)[0]
    save_path = os.path.join(output_path, f"{name_without_ext}_detected.jpg")

    # 字體設定
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 36)
    except:
        font = ImageFont.load_default()

    # 繪製檢測框和標籤
    for prediction in results['predictions']:
        x, y, width, height = prediction['x'], prediction['y'], prediction['width'], prediction['height']
        class_name = prediction['class']
        left = x - width / 2
        top = y - height / 2
        right = x + width / 2
        bottom = y + height / 2

        box_color = (255, 0, 0) if class_name == "parking spot" else (0, 255, 0)
        draw.rectangle([left, top, right, bottom], outline=box_color, width=3)
        draw.text((left, top - 20), class_name, fill=box_color, font=font)

    # 在圖片上顯示總數
    summary_text = f"Parking Spots: {parking_spot_count}"
    draw.text((10, 10), summary_text, fill=(255, 255, 255), font=font)

    # 保存圖片
    image.save(save_path, format="JPEG")
    print(f"Prediction successfully saved to {save_path}")

    # 構建傳送到後端的資料
    output_data = {
        "point_id": point_id,  # 使用接收到的 point_id
        "parking_spots": parking_spot_count
    }

    # 發送資料到後端
    try:
        print("Sending data to backend:", output_data)
        response = requests.post("http://127.0.0.1:5000/update_parking_status", json=output_data)
        if response.status_code == 200:
            print("結果已成功傳送到後端！")
        else:
            print(f"傳送失敗，狀態碼：{response.status_code}, 回應內容：{response.text}")
    except Exception as e:
        print(f"傳送到後端失敗：{e}")

@app.route('/')
def home():
    return "Welcome to the homepage!"



# 啟動 ngrok
def start_ngrok(port):
    # 使用 pyngrok 啟動 ngrok 隧道，指定端口
    public_url = ngrok.connect(port)
    print(f"ngrok public URL: {public_url}")
    return public_url

# 獲取 ngrok 公網 URL
def get_ngrok_url():
    try:
        # 請求 ngrok API 獲取隧道信息
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        data = response.json()
        public_url = data['tunnels'][0]['public_url']
        return public_url
    except Exception as e:
        print("Error fetching ngrok URL:", e)
        return None

# 啟動 Flask 後端服務
def start_flask(port):
    app.run(port=port)

# 主程式，啟動後端和 ngrok
def main():
    # 設定新的端口，例如5001
    port = 5001

    # 啟動 ngrok 隧道
    public_url = start_ngrok(port)

    # 獲取 ngrok 公網 URL
    ngrok_url = get_ngrok_url()
    if ngrok_url:
        print(f"Ngrok public URL: {ngrok_url}")
    else:
        print("Could not fetch ngrok URL")

    # 在 ngrok 啟動後啟動 Flask 後端服務
    print("Starting Flask app...")
    start_flask(port)

if __name__ == '__main__':
    main()
