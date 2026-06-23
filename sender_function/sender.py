import os
import sys  # Added to access PyInstaller's system path variables
import json
import socket
from dotenv import load_dotenv
from sender_function.packet_formation import create_packet

load_dotenv()


def run_sender():
    # Detect if the program is running as a compiled PyInstaller executable binary or raw Python script
    if getattr(sys, 'frozen', False):
        # Running inside PyInstaller Bundle, assets are extracted directly at the root of sys._MEIPASS
        current_dir = sys._MEIPASS
        json_path = os.path.join(current_dir, "sender_function", "data.json")
    else:
        # Running as normal script locally
        current_dir = os.path.dirname(__file__)
        json_path = os.path.join(current_dir, "data.json")

    try:
        with open(json_path, "r") as file:
            json_config = json.load(file)
    except FileNotFoundError:
        print(f"[SENDER ERROR] Could not find {json_path}!")
        return

    packet = create_packet(json_config)
    print(f"[SENDER] Formatted Frame Out:\n{packet}\n")

    host = os.getenv("SOCKET_HOST", "127.0.0.1")
    port = int(os.getenv("SOCKET_PORT", 65432))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            print(f"[SENDER] Connecting dynamically to {host}:{port}...")
            client_socket.connect((host, port))
            client_socket.sendall(packet.encode('utf-8'))
            print("[SENDER] Packet successfully pushed over stream.")
        except ConnectionRefusedError:
            print("[SENDER ERROR] Could not connect. Is receiver.py running?")


if __name__ == "__main__":
    run_sender()
    print("\n" + "=" * 40)
    input("Program finished. Press Enter to exit...")