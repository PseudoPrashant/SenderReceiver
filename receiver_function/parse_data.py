import os
from common.hasher import djb2_hash
from common.encrypt_decrypt import custom_xor_dec
from common.constants import FRAME_START, FRAME_END, SEP_MAIN, SEP_PAYLOAD_K, SEP_PAYLOAD_V
from common.logger import get_logger

logger = get_logger("PARSER")


def parse_packet(packet_str: str) -> dict or None:
    try:
        if not packet_str.startswith(FRAME_START) or not packet_str.endswith(FRAME_END):
            logger.error("Invalid frame sequence flags.")
            return None

        parts = [p.strip() for p in packet_str.split(SEP_MAIN)]

        if len(parts) < 4:
            logger.error("Invalid frame segment count.")
            return None

        method = parts[1]
        hashkey = os.getenv("HASH_KEY", "1234")
        enckey = os.getenv("ENC_KEY", "5678")

        encrypted_payload = parts[2].lstrip('[').rstrip(']')
        received_checksum = parts[3].replace(FRAME_END, "").strip()

        calculated_checksum = djb2_hash(encrypted_payload, hashkey)
        if calculated_checksum != received_checksum:
            logger.error(f"Checksum Failed! (Got: {received_checksum}, Calc: {calculated_checksum})")
            return None

        decrypted_payload = custom_xor_dec(encrypted_payload, enckey)

        result_payload = []
        entries = [e for e in decrypted_payload.split(SEP_PAYLOAD_V) if e]

        for entry in entries:
            if SEP_PAYLOAD_K in entry:
                k, v = entry.split(SEP_PAYLOAD_K, 1)
                result_payload.append([k, v])

        return {
            "method": method.upper(),
            "payload": result_payload
        }

    except Exception as e:
        logger.error(f"Failed reading incoming raw array stream structures: {e}")
        return None