from core.event_bus import EventBus
from modules.ai_module import AIModule
from modules.voice_module import VoiceModule
from modules.vision_module import VisionModule
from modules.network_module import NetworkModule
from modules.db_module import MedicalDB
from modules.knowledge_loader import load_knowledge
from ui.console_ui import ConsoleUI

import sys
sys.stdout.reconfigure(encoding='utf-8')

import threading


class MedicalAssistantApp:
    def __init__(self):
        self.event_bus = EventBus()
        self.db = MedicalDB()
        self.db.seed_data()

        # 🔥 CARGAR CONOCIMIENTO
        knowledge = load_knowledge("knowledge")

        # 🔥 PASAR A LA IA
        self.ai = AIModule(self.db, knowledge)
        self.voice = VoiceModule(self.event_bus)
        self.vision = VisionModule(self.event_bus)
        self.network = NetworkModule()
        self.ui = ConsoleUI(self.event_bus)

        self.event_bus.subscribe("voice_input", self.handle_input)

    def handle_input(self, text):
        threading.Thread(target=self.process_ai, args=(text,), daemon=True).start()

    def process_ai(self, text):
        result = self.ai.analyze(text)
        response = result["diagnosis"]

        self.ui.display(response)

        # 🔊 VOZ
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(response)
        engine.runAndWait()

    def run(self):
        threading.Thread(target=self.voice.listen, daemon=True).start()
        threading.Thread(target=self.network.listen, daemon=True).start()
        self.ui.run()


if __name__ == "__main__":
    app = MedicalAssistantApp()
    app.run()