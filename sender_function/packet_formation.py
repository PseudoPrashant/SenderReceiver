# this file contains the packet formation function
# $ZEN 0xd7 hashkey 0xd6 enckey 0xd7 method 0xd7 [encrypted_payload] 0xd7 checksum 0xd1

from common.hasher import djb2_hash
from common.encrypt_decrypt import custom_xor_enc


def create_packet(config_dict: dict) -> str:
    hashkey = config_dict["hashkey"]
    enckey = config_dict["enckey"]
    method = config_dict["method"].lower()  # Ensure it's lowercase like "0xa1"
    payload_list = config_dict["payload"]

    # 1 build the payload string
    payload_parts = []
    for pair in payload_list:
        key_item, value_item = pair[0], pair[1]
        payload_parts.append(f"{key_item}0xd4{value_item}0xd5")

    raw_payload_string = "".join(payload_parts)

    # 2. encrypt the raw structured payload string
    encrypted_payload = custom_xor_enc(raw_payload_string, enckey)

    # 3 Generate the 8-bit DJB2 checksum over the ENCRYPTED payload data
    checksum_val = djb2_hash(encrypted_payload, hashkey)

    # 4. Assemble the packet.
    packet = (
        f"$ZEN 0xd7 {hashkey} 0xd6 {enckey} 0xd7 {method} 0xd7 "
        f"[{encrypted_payload}] 0xd7 {checksum_val} 0xd1"
    )

    return packet