import socket
from threading import Lock  
import asyncio 

class ConnectionManager:
    def __init__(self):
        self.connections = {}
        self.lock = Lock()

    async def connect(self, address):
        reader, writer = await asyncio.open_connection(*address)
        async with self.lock:
            self.connections[address] = (reader, writer)

    async def disconnect(self, address):
        async with self.lock:
            if address in self.connections:
                reader, writer = self.connections.pop(address)
                writer.close()
                await writer.wait_closed()


    