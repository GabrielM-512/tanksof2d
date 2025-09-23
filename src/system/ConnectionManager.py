import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(msg)
        except:
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # start thread to receive messages
    threading.Thread(target=receive, args=(client,), daemon=True).start()

    # send messages from input
    while True:
        msg = input()
        client.sendall(msg.encode())

if __name__ == "__main__":
    start_client()
