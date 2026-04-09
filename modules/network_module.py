import time

class NetworkModule:
    def __init__(self):
        self.peers = []

    def broadcast(self, message):
        print("📡 Broadcasting:", message)

    def listen(self):
        while True:
            time.sleep(10)
            print("📡 Escuchando nodos...")