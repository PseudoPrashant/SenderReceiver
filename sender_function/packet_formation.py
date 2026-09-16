import os
from common.hasher import djb2_hash
from common.encrypt_decrypt import custom_xor_enc
from common.constants import FRAME_START, FRAME_END, SEP_MAIN, SEP_PAYLOAD_K, SEP_PAYLOAD_V


def create_packet(config_dict: dict) -> str:
    # Read keys from environment to avoid sending them in plaintext
    hashkey = os.getenv("HASH_KEY", "1234")
    enckey = os.getenv("ENC_KEY", "5678")
    
    method = config_dict["method"].lower()  # Ensure it's lowercase like "0xa1"
    payload_list = config_dict["payload"]

    # 1 build the payload string
    payload_parts = []
    for pair in payload_list:
        key_item, value_item = pair[0], pair[1]
        payload_parts.append(f"{key_item}{SEP_PAYLOAD_K}{value_item}{SEP_PAYLOAD_V}")

    raw_payload_string = "".join(payload_parts)

    # 2. encrypt the raw structured payload string
    encrypted_payload = custom_xor_enc(raw_payload_string, enckey)

    # 3 Generate the 8-bit DJB2 checksum over the ENCRYPTED payload data
    checksum_val = djb2_hash(encrypted_payload, hashkey)

    # 4. Assemble the packet.
    packet = (
        f"{FRAME_START} {SEP_MAIN} {method} {SEP_MAIN} "
        f"[{encrypted_payload}] {SEP_MAIN} {checksum_val} {FRAME_END}"
    )

    return packet