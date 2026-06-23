from common.hasher import djb2_hash
from common.encrypt_decrypt import custom_xor_dec


def parse_packet(packet_str: str) -> dict or None:
    try:
        # Sanity check frame headers and footers
        if not packet_str.startswith("$ZEN") or not packet_str.endswith("0xd1"):
            print("[PARSER ERROR] Invalid frame sequence flags.")
            return None

        # Standardize and clean parts by separating at '0xd7'
        parts = [p.strip() for p in packet_str.split("0xd7")]

        # parts[0] -> "$ZEN"
        # parts[1] -> "hashkey 0xd6 enckey"
        # parts[2] -> "method"
        # parts[3] -> "[encrypted_payload]"
        # parts[4] -> "checksum 0xd1"

        # Extract keys out of parts[1] split by '0xd6'
        hashkey, enckey = [k.strip() for k in parts[1].split("0xd6")]
        method = parts[2]

        # Strip string outer wrapping brackets '[' and ']' from payload data segment
        encrypted_payload = parts[3].lstrip('[').rstrip(']')

        # Isolate the clean 2-digit checksum field string
        received_checksum = parts[4].replace("0xd1", "").strip()

        # 1. Integrity Check: Verify local checksum matches incoming value
        calculated_checksum = djb2_hash(encrypted_payload, hashkey)
        if calculated_checksum != received_checksum:
            print(f"[PARSER ERROR] Checksum Failed! (Got: {received_checksum}, Calc: {calculated_checksum})")
            return None

        # 2. Decrypt Payload
        decrypted_payload = custom_xor_dec(encrypted_payload, enckey)

        # 3. Re-structure the customized payload back into a readable format
        result_payload = []
        # Split blocks using individual data block separators ('0xd5')
        entries = [e for e in decrypted_payload.split("0xd5") if e]

        for entry in entries:
            if "0xd4" in entry:
                k, v = entry.split("0xd4", 1)
                result_payload.append([k, v])

        # Return cleanly reconstructed dictionary format matching original object design layout
        return {
            "hashkey": hashkey,
            "enckey": enckey,
            "method": method.upper(),
            "payload": result_payload
        }

    except Exception as e:
        print(f"[PARSER ERROR] Failed reading incoming raw array stream structures: {e}")
        return None