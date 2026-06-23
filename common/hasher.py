# this is the hashing file which is DJB2 hashing algorithm
# receives and returns str

def djb2_hash(data_str: str, hashkey: str) -> str:
    # Convert your hashkey string (e.g., "1234") into an integer base-10 or base-16
    try:
        hash_value = int(hashkey, 16) if "0x" in hashkey.lower() else int(hashkey)
    except ValueError:
        hash_value = 19  # Fallback prime if parsing fails

    for char in data_str:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
        hash_value &= 0xFF  # Keep it 8-bit

    return f"{hash_value:02x}"