# UDP Client-Server with Raspberry Pi & Ultrasonic Sensor

## Overview
This project demonstrates a simple UDP client-server communication system.  
The server runs on a Raspberry Pi connected to an HC-SR04 ultrasonic sensor to measure real-time distances.  
The client sends requests to the server over UDP and receives the measured distance.  
If an object is too close (below a set threshold), the server sends an alert message back to the client.

---

## How It Works

### Server (`serverRpUDP.py`)
- Runs on a Raspberry Pi.
- Uses the HC-SR04 ultrasonic sensor to measure distances in centimeters.
- Listens for incoming **UDP messages** from any client.
- When a message is received:
  1. Reads the current distance from the sensor.
  2. Sends the distance back to the client.
  3. If the distance is below **50 cm** (configurable), adds an **ALERT** message.
- Logs activity to a file (`udp_sensor_server_log.txt`) and prints to the terminal.
- Cleans up GPIO pins safely on shutdown.

---

### Client (`clientUDP.py`)
- Can run on the same Raspberry Pi, another Raspberry Pi, or a PC.
- Sends a "Hello" message to the server every second.
- Waits for a response:
  - Displays the measured distance.
  - Shows a warning if the server’s response contains "ALERT".
- Logs all activity in a file (`udp_client_log.txt`) and prints to the console.
- Uses a timeout to avoid waiting forever if the server is unreachable.

---

## Workflow
1. Start the server on the Raspberry Pi connected to the HC-SR04 sensor.
2. Start the client on another device (or the same Pi if testing locally).
3. The client sends requests → the server measures distance → the server sends results back.
4. If an object is too close, both the server and client log and display an **alert**.

---


