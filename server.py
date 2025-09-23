import socket
import threading
import json

HOST = "192.168.178.60"
PORT = 5000

clients = []  # track connected clients

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")
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
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER LISTENING] {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    start_server()
