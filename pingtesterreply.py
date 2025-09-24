from src.system.ConnectionManager import ConnectionManager

def reply(connectionManager, msg):
    connectionManager.send(msg)

def callback(msg : dict):
    global connectionManager
    reply(connectionManager, msg)

connectionManager = ConnectionManager(host="10.21.165.3", port=5000, callback=callback)
connectionManager.connect()

while True:
    pass

