# RFID Card Top-Up System

**Assignment Submission**  
**Instructor:** Gabriel Baziramwabo  
**Team ID:** its_ace  
**Member:** Munezero Impano Christella  
**Course:** IoT / Embedded Networking  

**Keywords:** RFID Systems, IoT Architecture, MQTT Messaging, Publish-Subscribe Model, Edge Controllers, Cloud-Based Backend Services, Real-Time Web Communication, Embedded Networking

## Live Dashboard URL

**http://157.173.101.159:9252**

(The dashboard is hosted directly on the VPS at port 9252. It receives real-time balance updates via WebSocket and sends top-up requests via HTTP POST /topup.)

## Objective

Design and implement a complete RFID card top-up system using an ESP8266 (edge controller), a cloud backend (VPS at 157.173.101.159), and a web dashboard.

The system allows multiple teams to operate simultaneously on the same MQTT broker without interfering, using a unique team namespace: `rfid/its_ace/`.

## System Architecture

The implementation strictly follows the required architecture:

- **ESP8266 (Edge Controller)**
  - Reads and writes RFID card data (MFRC522 module)
  - Publishes card UID and balance via MQTT
  - Subscribes to top-up commands via MQTT
  - **Does NOT** use HTTP or WebSocket

- **Backend API Service (VPS)**
  - Receives user commands via HTTP POST /topup
  - Communicates with ESP8266 via MQTT
  - Pushes real-time updates to browsers via WebSocket

- **Web Dashboard (Browser)**
  - Sends top-up requests via HTTP
  - Receives balance updates via WebSocket
  - **Does NOT** communicate directly with MQTT

**MQTT Broker:** 157.173.101.159:1883 (shared broker)

**Topic Isolation Rule:** All topics are prefixed with `rfid/its_ace/` to avoid conflicts with other teams.

### Required MQTT Topics

- **Card status** (ESP8266 → Broker)  
  `rfid/its_ace/card/status`  
  Example payload:
  ```json
  {"uid": "56389904F3", "balance": 1000}

  **Forbidden Practices Avoided:**

No generic topics (rfid/card, rfid/topup, balance)
No wildcard subscriptions (rfid/#)
No publishing/subscribing to other teams' namespaces

Project Structure
textrfid-topup-its-ace/
├── esp8266/
│   ├── main.py              # MicroPython code for ESP8266
│   └── mfrc522.py           # MFRC522 RFID library
├── backend/
│   ├── app.py               # Flask backend (HTTP + MQTT + WebSocket)
│   └── index.html           # Beautiful web dashboard
└── README.md                # This file
Note: You can use either app.py (Flask/Python backend) or server.js (Node.js backend) — both implement the same functionality. The current deployment uses Flask (app.py) because it was easier to run on the VPS without Node.js installation.
Setup & Running Instructions
1. ESP8266 (Edge Controller)
Hardware:

ESP8266 (NodeMCU or similar)
MFRC522 RFID module
Wiring:
SDA/CS → D4 (GPIO2)
SCK → D5 (GPIO14)
MOSI → D7 (GPIO13)
MISO → D6 (GPIO12)
RST → D3 (GPIO0)
3.3V → 3V3, GND → GND


Software:

Flash MicroPython firmware (v1.27.0 or latest)
Upload mfrc522.py and main.py using Thonny
Board auto-runs main.py on boot

Dependencies: umqtt.simple (installed via upip)
MQTT Broker: 157.173.101.159:1883 (anonymous)
2. Backend (Flask on VPS)
Location: VPS at 157.173.101.59
Port: 9252
Live URL: http://157.173.101.159:9252
Run command (using nohup):
Bashnohup python3 app.py > rfid-backend.log 2>&1 &
Dependencies:
Bashpython3 -m pip install flask flask-socketio paho-mqtt eventlet
Features:

HTTP POST /topup → publishes to MQTT
Subscribes to status & balance topics
Pushes updates via SocketIO/WebSocket

Alternative (Node.js version):
If Node.js is available, you can use server.js instead:
Bashnohup node server.js > rfid-backend.log 2>&1 &
Both implement the same backend logic — choose based on what runs on your VPS.
3. Web Dashboard

Static HTML + Tailwind CSS + JavaScript
Hosted by Flask backend
URL: http://157.173.101.159:9252
Sends top-up via fetch POST
Receives real-time updates via WebSocket (no polling)

Compliance with Assignment Rules

MQTT Topic Isolation: Used unique prefix rfid/its_ace/
No direct MQTT/WebSocket from dashboard: Dashboard uses only HTTP + WebSocket to backend
Devices speak MQTT, users speak HTTP/WebSocket: Backend translates
No polling: Real-time updates via WebSocket
Public repo, well-structured, README.md present

Evaluation Notes

Complete end-to-end functionality: scan card → see balance → top-up → balance updates live
Tested in shared broker environment (no interference with other teams)
Code clarity & organization prioritized

Live Dashboard: http://157.173.101.159:9252
GitHub Repository: https://github.com/Chiki-tella/IoT_RFID_Card_Topup
(Replace YOUR_USERNAME with your actual GitHub username)
Thank you!
text