# Real-Time Roadside Parking Space Detection System / 即時路邊停車位檢測系統

<div align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a>
</div>

---

<a name="english"></a>

# 🇺🇸 English

### **Abstract**
A real-time roadside parking detection system that integrates YOLO-based object detection and edge computing.  
By processing camera images locally and updating availability through a web interface, the system reduces parking search time, improves urban traffic flow, and enhances parking efficiency.  
The trained YOLOv7 model achieves **97.6% mAP50, 97.0% precision, and 94.0% recall** in real-world roadside testing.

---

## Features
- **Real-time parking space detection**
- **YOLO object detection**
- **Interactive Google Maps interface**
- **User authentication system**
- **English/Chinese bilingual UI**

---

## Tech Stack
- **Backend:** Flask, Flask-Login, Flask-SQLAlchemy, SQLite  
- **ML:** YOLOv7 (Roboflow), OpenCV, PIL  
- **Frontend:** Bootstrap 5, Google Maps API  
- **Tools:** ngrok, requests  

---

## System Architecture
- **Frontend Layer:** Web interface + map visualization  
- **Backend Layer:** User database + parking status database  
- **Edge Computing Layer:** Local YOLOv7 inference on images from roadside cameras  
- **Data Flow:** Edge devices upload results every minute; backend updates parking availability in real-time  

---

## Model Performance
- **Precision:** 97.0%  
- **Recall:** 94.0%  
- **mAP50:** 97.6%  
- 300 epochs of training with stable convergence and strong generalization ability.

---

## Installation
1. Clone the repository  
2. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```
3. Configure API keys (Roboflow, Google Maps) using environment variables

---

## Usage

```bash
python app.py                                   # Start backend
python take_and_detect_photo/detection.py       # Start detection service
```

Camera scripts run automatically to capture and process images.

---

## Project Structure

```
├── app.py                    # Backend service
├── models.py                 # Database models
├── templates/                # Frontend HTML
└── take_and_detect_photo/    # Detection & camera module
```
---

<a name="中文"></a>

# 🇹🇼 中文

### **摘要**
本系統結合 YOLO 物件偵測與邊緣運算技術，能即時辨識路邊停車位並在網頁地圖呈現可用空位資訊。  
透過本地影像推論降低延遲、提升查找效率，改善交通流量並提升停車使用率。  
YOLOv7 模型於實際路邊測試中達到 **mAP50 97.6%、Precision 97.0%、Recall 94.0%**。

---

## 功能特色
- **即時停車位檢測**
- **YOLO 物件偵測**
- **互動式 Google Maps 介面**
- **用戶認證系統**
- **中英文雙語介面**

---

## 技術棧
- **後端：** Flask, Flask-Login, Flask-SQLAlchemy, SQLite  
- **機器學習：** YOLOv7 (Roboflow), OpenCV, PIL  
- **前端：** Bootstrap 5, Google Maps API  
- **工具：** ngrok, requests  

---

## 系統架構
- **前端層：** 網頁介面 + 地圖視覺化  
- **後端層：** 用戶資料庫 + 停車狀態資料庫  
- **邊緣運算層：** 本地 YOLOv7 推論處理路邊攝影機影像  
- **資料流：** 邊緣裝置每分鐘上傳結果；後端即時更新停車位可用狀態  

---

## 模型效能
- **Precision：** 97.0%  
- **Recall：** 94.0%  
- **mAP50：** 97.6%  
- 訓練 300 個 epochs，具備穩定收斂與強健的泛化能力。

---

## 安裝步驟
1. 克隆專案  
2. 安裝依賴套件  
   ```bash
   pip install -r requirements.txt
   ```
3. 使用環境變數設定 API Key（Roboflow、Google Maps）

---

## 使用說明

```bash
python app.py                                   # 啟動後端服務
python take_and_detect_photo/detection.py       # 啟動檢測服務
```

攝影機腳本會自動執行拍攝與影像處理。

---

## 專案結構

```
├── app.py                    # 後端服務
├── models.py                 # 資料庫模型
├── templates/                # 前端 HTML
└── take_and_detect_photo/    # 檢測與攝影機模組
```
