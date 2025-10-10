import socket
import threading
import json
import sys

modes = {
    0 : "PVP",
    1 : "PVE"
}

server = None

HOST = "0.0.0.0"
PORT = 5000

print(f"Server IP: {HOST}")
print("Server version 1.0")

clients = []  # track connected clients

try:
    mode = modes[min(max(int(input("Available Gamemodes:\n"
                                   " PVP: 0\n"
                                   " PVE: 1\n"
                                   "Select gamemode: ")), 0), 1)]
    print(f"Selected Mode: {mode}")

except ValueError:
    print("Invalid mode, set to PVE")
    mode = "PVE"


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")
    
    data = {
        "actions": ["connect"],
        "id": len(clients) - 1,
        "mode": mode
    }
    print(data)
    data = json.dumps(data) + "\n"
    conn.sendall(data.encode())


    buffer = ""  # accumulate partial data per client
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            buffer += data
            # extract full messages
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if line.strip():
                    try:
                        msg = json.loads(line.strip())
                        print(f"[RECEIVED from {addr}] {msg}")

                        # broadcast JSON to all other clients
                        broadcast(msg, sender=conn)
                    except json.JSONDecodeError:
                        print(f"[INVALID JSON from {addr}]: {line.strip()}")

        except (ConnectionResetError, OSError):
            break

    conn.close()
    if conn in clients:
        clients.remove(conn)
    print(f"[DISCONNECTED] {addr}")

def broadcast(msg, sender=None):
    """Send a JSON message to all clients except the sender."""
    data = json.dumps(msg) + "\n"
    for client in clients:
        if client != sender:
            try:
                client.sendall(data.encode())
            except:
                pass  # ignore broken clients

def start_server():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER LISTENING] {HOST}:{PORT}")

    server.settimeout(1.0)

    while True:
        try:
            conn, addr = server.accept()
            clients.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
        except socket.timeout:
            continue

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("exited from keyboard interrupt")
    finally:
        broadcast({"actions": ["disconnect"]})
        for c in clients:
            c.close()
        # noinspection PyUnresolvedReferences
        server.close()
    sys.exit(0)