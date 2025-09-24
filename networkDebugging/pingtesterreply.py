from src.system.ConnectionManager import ConnectionManager

import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

def reply(connectionManager, msg):
    connectionManager.send(msg)

def callback(msg : dict):
    global connectionManager
    reply(connectionManager, msg)

connectionManager = ConnectionManager(host=hostname, port=5000, callback=callback)
connectionManager.connect()

while True:
    pass

