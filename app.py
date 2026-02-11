from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt
import json
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# ===================== CONFIG =====================
TEAM_ID = "its_ace"
MQTT_BROKER = "157.173.101.159"  # your assignment broker
MQTT_PORT = 1883

STATUS_TOPIC  = f"rfid/{TEAM_ID}/card/status"
BALANCE_TOPIC = f"rfid/{TEAM_ID}/card/balance"
TOPUP_TOPIC   = f"rfid/{TEAM_ID}/card/topup"

# ===================== MQTT CLIENT =====================
mqtt_client = mqtt.Client(client_id=f"backend_{TEAM_ID}")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

def on_connect(client, userdata, flags, rc):
    print(f"MQTT connected with code {rc}")
    client.subscribe(STATUS_TOPIC)
    client.subscribe(BALANCE_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        topic = msg.topic
        print(f"MQTT received on {topic}: {payload}")

        # Push to all connected WebSocket clients
        socketio.emit('update', {'topic': topic, 'data': payload})
    except Exception as e:
        print("MQTT message error:", e)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.loop_start()  # background thread

# ===================== HTTP ENDPOINT =====================
@app.route('/topup', methods=['POST'])
def topup():
    data = request.get_json()
    uid = data.get('uid')
    amount = data.get('amount')

    if not uid or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Invalid uid or amount (>0 required)"}), 400

    payload = json.dumps({"uid": uid, "amount": amount})
    mqtt_client.publish(TOPUP_TOPIC, payload)
    print(f"Published top-up: {payload}")

    return jsonify({"success": True, "message": "Top-up sent"})

# ===================== WEBSOCKET (SocketIO) =====================
@socketio.on('connect')
def handle_connect():
    print("Dashboard connected via WebSocket")
    emit('update', {'message': 'Connected to real-time updates'})

# Serve dashboard
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9252, debug=False)