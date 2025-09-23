import socket
import threading

HOST = "127.0.0.1"  # localhost
PORT = 5000

clients = []  # keep track of connected clients

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"[{addr}] {msg}")

            # broadcast message to all other clients
            for client in clients:
                if client != conn:
                    client.sendall(f"{addr}: {msg}".encode())
        except:
            break

    conn.close()
    clients.remove(conn)
    print(f"[DISCONNECTED] {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER LISTENING] {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
