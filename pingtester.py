from src.system.ConnectionManager import ConnectionManager
import time



waiting = True
def callback(msg : dict):
    global waiting
    print(f"time in ms: {(time.time() - starttime) * 1000 / 2}")
    waiting = False

connectionManager = ConnectionManager(host="10.21.165.3", port=5000, callback=callback)
connectionManager.connect()

starttime = time.time()

msg = "print"
connectionManager.send(msg)
print("send")

while waiting:
    pass
