from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# lưu dữ liệu mới nhất
latest_data = {
    "heartRate": 0,
    "fall": False
}

# API nhận dữ liệu từ ESP32
@app.route('/data', methods=['POST'])
def receive_data():
    global latest_data

    data = request.json

    # lấy dữ liệu
    heartRate = data.get("heartRate", 0)
    acc = data.get("acc", {})

    # logic phát hiện ngã đơn giản
    fall = False
    if acc.get("z", 0) > 2.5:
        fall = True

    # cập nhật dữ liệu
    latest_data = {
        "heartRate": heartRate,
        "fall": fall
    }

    return jsonify({"status": "ok"})


# API cho app lấy dữ liệu
@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify(latest_data)


# test server
@app.route('/')
def home():
    return "Server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)