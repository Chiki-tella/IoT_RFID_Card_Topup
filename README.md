# RFID Card Top-Up System

 
**Team ID:** its_ace  

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

 