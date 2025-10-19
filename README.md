🦷 Machine Learning Braces API

A Flask-based API powered by Roboflow and YOLOv8, deployed on Render, that detects teeth in an image and overlays braces filters for a realistic AR-style braces effect.

📖 Overview

This project uses machine learning (via Roboflow and YOLOv8) to detect teeth from user-uploaded images. It then applies digital braces overlays — metal or ceramic — with optional color customization.

Perfect for AI demos, AR filter apps, or educational ML projects.

⚙️ Features

✅ Teeth Detection via Roboflow API (YOLOv8 model)
✅ Braces Overlay (Metal or Ceramic) using OpenCV & Pillow
✅ Custom Bracket Colors – green, white, or brown (for metal type)
✅ Flask REST API for easy integration with mobile or web frontends
✅ CORS Enabled – ready for frontend calls
✅ Deployed on Render using Gunicorn

🧩 Tech Stack

Python 3.10+

Flask (API backend)

Roboflow API / YOLOv8

OpenCV (cv2)

Pillow (PIL)

Flask-CORS

Gunicorn (for Render deployment)

python-dotenv (for environment variables)

📁 Project Structure
Machine_learning_Braces/
│
├── assets/
│   ├── ceramic.png
│   ├── metal.png
│   ├── greenbraces.png
│   ├── whitebraces.png
│   └── brownbraces.png
│
├── main.py                  # Main Flask API
├── withbraces.py            # Braces overlay logic (optional helper)
├── requirement.txt          # Dependencies
├── .gitignore               # Hides .env and local files
├── .env                     # Contains API keys (not tracked in Git)
└── README.md

🚀 API Endpoints
1️⃣ /detect-teeth

POST – Detects teeth from a base64 image and returns their positions.

Request Body:

{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ..."
}


Response:

{
  "success": true,
  "teeth_count": 5,
  "teeth": [
    { "x": 130, "y": 210, "width": 60, "height": 45, "confidence": 0.92 }
  ],
  "image_dimensions": { "width": 720, "height": 480 }
}

2️⃣ /apply-brackets

POST – Applies braces overlay to the detected teeth.

Request Body:

{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ...",
  "bracket_type": "metal",
  "bracket_color": "green",
  "teeth": [
    { "x": 130, "y": 210, "width": 60, "height": 45 }
  ]
}


Response:

{
  "success": true,
  "processed_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ...",
  "teeth_count": 5,
  "bracket_type": "metal",
  "bracket_color": "green"
}

🧠 How It Works
graph TD;
A[Client Uploads Image] --> B[Flask API /detect-teeth]
B --> C[Roboflow Model Detects Teeth]
C --> D[/apply-brackets]
D --> E[Overlay Braces Using assets/ Images]
E --> F[Return Processed Image as Base64]

🧾 Installation
1️⃣ Clone the Repository
git clone https://github.com/tpcenter13/Machine_learning_Braces.git
cd Machine_learning_Braces

2️⃣ Install Dependencies
pip install -r requirement.txt

3️⃣ Create a .env File
API_KEY=your_roboflow_api_key
MODEL_ID=your_model_id
MODEL_VERSION=your_model_version

4️⃣ Run Locally
python main.py

5️⃣ Deploy on Render

Create a new Web Service

Link your GitHub repo

Set Build Command:

pip install -r requirement.txt


Set Start Command:

gunicorn main:app


Add environment variables in the Render Dashboard:

API_KEY=your_roboflow_api_key
MODEL_ID=your_model_id
MODEL_VERSION=your_model_version

📦 requirement.txt
requests
opencv-python-headless
python-dotenv
matplotlib
flask
flask-cors
gunicorn
Pillow

💡 Future Enhancements

🔴 Real-time webcam/live filter

🌈 More customizable bracket colors

📱 Integration with React Native frontend

👨‍💻 Author

Kurt Arciga — System Developer
