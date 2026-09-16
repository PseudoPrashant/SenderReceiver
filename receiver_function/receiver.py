import os
import socket
from dotenv import load_dotenv
from receiver_function.parse_data import parse_packet
from common.logger import get_logger

load_dotenv()
logger = get_logger("RECEIVER")


def run_receiver():
    host = os.getenv("SOCKET_HOST", "127.0.0.1")
    port = int(os.getenv("SOCKET_PORT", 65432))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        logger.info(f"Online. Listening closely on {host}:{port}...")

        from common.constants import FRAME_END
        conn, addr = server_socket.accept()
        with conn:
            logger.info(f"Connection line open from: {addr}")
            
            buffer = ""
            while True:
                received_bytes = conn.recv(2048)
                if not received_bytes:
                    break
                
                buffer += received_bytes.decode('utf-8')
                
                if FRAME_END in buffer:
                    packet_string, buffer = buffer.split(FRAME_END, 1)
                    packet_string += FRAME_END
                    
                    logger.debug(f"Received Raw Stream Data:\n{packet_string}")

                    parsed_json = parse_packet(packet_string)
                    if parsed_json:
                        logger.info(f"Success! Authenticated Frame Dictionary:\n{parsed_json}")
                    else:
                        logger.warning("Packet drop command triggered due to validation failure.")
                    break


if __name__ == "__main__":
    run_receiver()
    input("Program finished. Press Enter to exit...")