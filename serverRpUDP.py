#!/usr/bin/env python3
"""
Student Surname: [Your Surname]
Student Name: [Your Name]
Student Number: [Your Student Number]
CSC311 2025 Group Practical 2 – UDP Sensor-Based Server

Description:
This server runs on a Raspberry Pi using a real HC-SR04 ultrasonic sensor 
to measure distance in real time. It listens for a UDP request from a client 
and then responds with the current measured distance. If the distance is below 
a critical threshold, an alert message is included.
"""

import socket
import time
import logging
import RPi.GPIO as GPIO

# --- Logging setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("udp_sensor_server_log.txt",
                                            encoding="utf-8"),
                        logging.StreamHandler()
                    ])

# --- GPIO setup for HC-SR04 sensor ---
TRIG = 23  # GPIO pin for Trigger
ECHO = 24  # GPIO pin for Echo

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def measure_distance():
    """
    Measures distance using the HC-SR04 sensor.
    Returns:
       distance (float): measured distance in centimeters.
    """
    # Ensure trigger is low
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    # Generate a 10µs pulse on the trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Record the pulse start time
    pulse_start = time.time()
    timeout = pulse_start + 0.04  # 40ms timeout
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        pulse_start = time.time()

    # Record pulse end time
    pulse_end = time.time()
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2  # Speed of sound = 34300 cm/s
    return distance


# --- UDP server configuration ---
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 5005  # UDP port to use
THRESHOLD = 50  # Alert threshold: if distance < 50 cm


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((UDP_IP, UDP_PORT))
    logging.info(f"UDP sensor server started on port {UDP_PORT}.")

    try:
        while True:
            # Wait for a client message (the server responds to the sender)
            server_socket.settimeout(10)
            try:
                data, client_address = server_socket.recvfrom(1024)
                logging.info(f"Received request from {client_address}.")
            except socket.timeout:
                logging.info("No client request received; waiting...")
                continue

            # Read sensor data
            distance = measure_distance()
            message = f"Distance: {distance:.2f} cm"
            if distance < THRESHOLD:
                message += " | ALERT: Obstacle too close!"

            # Send response to the client
            server_socket.sendto(message.encode(), client_address)
            logging.info(f"Sent to {client_address}: {message}")
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Server stopped by user.")
    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        server_socket.close()
        GPIO.cleanup()
        logging.info("Server socket closed and GPIO cleaned up.")


if __name__ == "__main__":
    main()
