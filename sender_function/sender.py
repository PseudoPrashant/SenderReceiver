import os
import sys
import json
import socket
from dotenv import load_dotenv
from sender_function.packet_formation import create_packet
from common.logger import get_logger

load_dotenv()
logger = get_logger("SENDER")


def run_sender():
    if getattr(sys, 'frozen', False):
        current_dir = sys._MEIPASS
        json_path = os.path.join(current_dir, "data.json")
    else:
        current_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(current_dir, "data.json")

    try:
        with open(json_path, "r") as file:
            json_config = json.load(file)
    except FileNotFoundError:
        logger.error(f"Could not find {json_path}!")
        return

    packet = create_packet(json_config)
    logger.info(f"Formatted Frame Out:\n{packet}")

    host = os.getenv("SOCKET_HOST", "127.0.0.1")
    port = int(os.getenv("SOCKET_PORT", 65432))

    import time
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Connecting dynamically to {host}:{port}... (Attempt {attempt + 1}/{max_retries})")
                client_socket.connect((host, port))
                client_socket.sendall(packet.encode('utf-8'))
                logger.info("Packet successfully pushed over stream.")
                break
            except ConnectionRefusedError:
                if attempt < max_retries - 1:
                    logger.warning("Connection refused. Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    logger.error("Could not connect after multiple attempts. Is receiver.py running?")


if __name__ == "__main__":
    run_sender()
    input("Program finished. Press Enter to exit...")