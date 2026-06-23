import os
import socket
from dotenv import load_dotenv
from receiver_function.parse_data import parse_packet

load_dotenv()


def run_receiver():
    host = os.getenv("SOCKET_HOST", "127.0.0.1")
    port = int(os.getenv("SOCKET_PORT", 65432))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"[RECEIVER] Online. Listening closely on {host}:{port}...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"[RECEIVER] Connection line open from: {addr}")
            received_bytes = conn.recv(2048)

            if received_bytes:
                packet_string = received_bytes.decode('utf-8')
                print(f"\n[RECEIVER] Received Raw Stream Data:\n{packet_string}\n")

                parsed_json = parse_packet(packet_string)
                if parsed_json:
                    print(f"[RECEIVER] Success! Authenticated Frame Dictionary:\n{parsed_json}")
                else:
                    print("[RECEIVER] Packet drop command triggered due to validation failure.")


if __name__ == "__main__":
    run_receiver()
    print("\n" + "=" * 40)
    input("Program finished. Press Enter to exit...")  # Keeps console open