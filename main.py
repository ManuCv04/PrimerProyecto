from core.event_bus import EventBus
from modules.ai_module import AIModule
from modules.voice_module import VoiceModule
from modules.vision_module import VisionModule
from modules.network_module import NetworkModule
from modules.db_module import MedicalDB
from ui.console_ui import ConsoleUI
import sys
sys.stdout.reconfigure(encoding='utf-8')
import threading
import time
import threading

class MedicalAssistantApp:
    def __init__(self):
        self.event_bus = EventBus()
        self.db = MedicalDB()
        self.db.seed_data()

        # 🔥 ESTO ES LO QUE TE FALTA O ESTÁ MAL
        self.ai = AIModule(self.db)
        self.voice = VoiceModule(self.event_bus)
        self.vision = VisionModule(self.event_bus)
        self.network = NetworkModule()
        self.ui = ConsoleUI(self.event_bus)

        self.event_bus.subscribe("voice_input", self.handle_input)

    def handle_input(self, text):
        result = self.ai.analyze(text)
        response = f"Posible: {result['diagnosis']} | Recomendación: {result['recommendation']}"
        self.ui.display(response)
        self.voice.speak(response)  
        self.network.broadcast(response)

    def run(self):
        threading.Thread(target=self.voice.listen, daemon=True).start()
        threading.Thread(target=self.network.listen, daemon=True).start()
        self.ui.run()

if __name__ == "__main__":
    app = MedicalAssistantApp()
    app.run()