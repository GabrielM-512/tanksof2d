import socket
import threading
import json

class ChatClient:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        self.buffer = ""  # for accumulating partial data

    def connect(self):
        """Connects to the server and starts listening for messages."""
        self.sock.connect((self.host, self.port))
        self.running = True
        threading.Thread(target=self._receive_loop, daemon=True).start()

    def _receive_loop(self):
        """Continuously listens for messages from the server."""
        while self.running:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    self.running = False
                    break

                # accumulate into buffer
                self.buffer += data
                # split into complete messages
                while "\n" in self.buffer:
                    line, self.buffer = self.buffer.split("\n", 1)
                    if line.strip():
                        self.on_message(line.strip())
            except (ConnectionResetError, OSError):
                self.running = False
                break

    def on_message(self, msg: str):
        """Callback for handling received messages (raw JSON string)."""
        try:
            data = json.loads(msg)
            print("Received JSON:", data)
        except json.JSONDecodeError:
            print("Invalid JSON:", msg)

    def send(self, obj):
        """Send a JSON-serializable object to the server."""
        if not self.running:
            raise RuntimeError("Client is not connected.")
        try:
            msg = json.dumps(obj) + "\n"  # NDJSON format
            self.sock.sendall(msg.encode())
        except (BrokenPipeError, OSError):
            print("Failed to send message. Connection may be closed.")
            self.close()

    def close(self):
        """Gracefully close the connection."""
        self.running = False
        try:
            self.sock.close()
        except:
            pass


if __name__ == "__main__":
    client = ChatClient()
    client.connect()

    # Example usage: send a move command
    client.send({"action": "move", "player_id": 1, "x": 42, "y": 17})

    import time
    time.sleep(3)
    client.close()
