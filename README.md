# SenderReciever

This is a basic Python project for sending and receiving a custom packet using socket programming.

In this project there are two main programs:

- Sender
- Receiver

The sender reads data from a JSON file, converts it into a custom frame, encrypts the payload, adds a checksum, and sends it to the receiver using TCP socket.

The receiver listens for the sender, receives the packet, checks if the packet is valid, verifies the checksum, decrypts the payload, and prints the final data.

## Project Structure

```text
aaSenderReciever/
├── data.json
├── .env
├── __init__.py
├── ProtocolReceiver.spec
├── ProtocolSender.spec
├── project_flow.drawio
├── project_flow_clean.drawio
│
├── common/
│   ├── __init__.py
│   ├── constants.py
│   ├── logger.py
│   ├── encrypt_decrypt.py
│   └── hasher.py
│
├── sender_function/
│   ├── __init__.py
│   ├── sender.py
│   └── packet_formation.py
│
├── receiver_function/
│   ├── __init__.py
│   ├── receiver.py
│   └── parse_data.py
│
├── dist/
│   ├── ProtocolSender.exe
│   └── ProtocolReceiver.exe
│
└── build/
    ├── ProtocolSender/
    └── ProtocolReceiver/
```

## Main Files

### sender_function/sender.py

This file runs the sender side.

It reads the JSON data from `data.json`, creates the packet, connects to the receiver, and sends the packet.

### sender_function/packet_formation.py

This file creates the final packet.

It does these steps:

1. Reads hash key, encryption key, method, and payload.
2. Converts payload into custom format.
3. Encrypts the payload.
4. Creates checksum.
5. Creates the final frame.

### data.json

This file contains the data which is sent by the sender.

Example:

```json
{
    "hashkey": "1234",
    "enckey": "5678",
    "method": "0xA1",
    "payload": [
        ["name", "Prashant"],
        ["age", "22"],
        ["city", "Delhi"]
    ]
}
```

### receiver_function/receiver.py

This file runs the receiver side.

It creates a socket server, waits for the sender, receives the packet, and sends it to parser.

### receiver_function/parse_data.py

This file parses the received packet.

It checks:

- frame start and end
- hash key and encryption key
- checksum
- encrypted payload

After that it decrypts the payload and converts it back into readable data.

### common/encrypt_decrypt.py

This file contains custom XOR encryption and decryption functions.

### common/hasher.py

This file contains DJB2 hash logic which is used for checksum.

### sender_function/crc8.py

This file has CRC8 checksum code, but currently the main project is using DJB2 hash from `common/hasher.py`.

## Environment File

The `.env` file is used for socket host and port.

```env
SOCKET_HOST=127.0.0.1
SOCKET_PORT=65432
```

Both sender and receiver use this file.

## Packet Format

The custom packet format is:

```text
$ZEN 0xd7 method 0xd7 [encrypted_payload] 0xd7 checksum 0xd1
```

Meaning:

- `$ZEN` is starting flag
- `0xd7` is main separator
- encrypted payload is kept inside `[ ]`
- checksum is used to check data integrity
- `0xd1` is ending flag

Note: `hashkey` and `enckey` are now securely loaded from the `.env` file instead of being transmitted over the network in plaintext.

## How To Run

First start the receiver:

```bash
python receiver_function/receiver.py
```

Then open another terminal and run the sender:

```bash
python sender_function/sender.py
```

The receiver should show the received packet and parsed data.

## How It Works

Basic flow:

```text
data.json
   ↓
sender.py
   ↓
packet_formation.py
   ↓
encrypt payload
   ↓
create checksum
   ↓
send packet using socket
   ↓
receiver.py
   ↓
parse_data.py
   ↓
verify checksum
   ↓
decrypt payload
   ↓
print final data
```

## Output Files

The `dist` folder contains executable files:

- `ProtocolSender.exe`
- `ProtocolReceiver.exe`

These are created using PyInstaller.

The `.spec` files are used by PyInstaller for creating these executables.

## Notes

- Receiver should be started before sender.
- Sender and receiver must use the same host and port.
- If receiver is not running, sender will show connection error.
- This project is mainly for learning socket communication, custom packet framing, hashing, and simple encryption.

# SenderReceiver
