#!/usr/bin/env python3
import socket
import logging
import time

# --- Logging setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("udp_client_log.txt",
                                            encoding="utf-8"),
                        logging.StreamHandler()
                    ])

# --- Client configuration ---
# Set SERVER_IP accordingly. Use "127.0.0.1" if testing on the same machine,
# or the actual IP address of your Raspberry Pi if testing over the network.
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
ALERT_KEYWORD = "ALERT"


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Optional: set a timeout for recvfrom
    client_socket.settimeout(5.0)
    logging.info(f"Client started. Sending data to {SERVER_IP}:{SERVER_PORT}")

    try:
        while True:
            client_socket.sendto(b"Hello", (SERVER_IP, SERVER_PORT))
            try:
                data, _ = client_socket.recvfrom(1024)
                message = data.decode()
                logging.info(f"Received: {message}")
                print(f"Received: {message}")

                if ALERT_KEYWORD in message:
                    alert_msg = "WARNING: Obstacle too close!"
                    logging.info(alert_msg)
                    print(alert_msg)
            except socket.timeout:
                logging.info("No response from server (timeout).")
            except ConnectionResetError:
                logging.error(
                    "Connection was reset by the server. Waiting before retrying..."
                )
                time.sleep(2)
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Client stopped by user.")
    finally:
        client_socket.close()
        logging.info("Client socket closed.")


if __name__ == "__main__":
    main()
