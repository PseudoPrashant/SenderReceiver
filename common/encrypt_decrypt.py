# this file contains the encryption and decryption functions
# simple XOR operation in the ASCII of data_str and key characters is used

def custom_xor_enc(data_str: str, key: str) -> str:
    output = []
    key_length = len(key)

    for i, char in enumerate(data_str):
        key_char = key[i % key_length]
        cipher_byte = ord(char) ^ ord(key_char)
        output.append(f"{cipher_byte:02x}")

    return "".join(output)


def custom_xor_dec(hex_str: str, key: str) -> str:
    output = []
    key_length = len(key)

    bytes_list = [int(hex_str[i:i + 2], 16) for i in range(0, len(hex_str), 2)]

    for i, cipher_byte in enumerate(bytes_list):
        key_char = key[i % key_length]
        plain_byte = cipher_byte ^ ord(key_char)
        output.append(chr(plain_byte))

    return "".join(output)