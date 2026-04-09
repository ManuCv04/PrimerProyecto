import threading
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyttsx3

class VoiceModule:
    def __init__(self, event_bus):
        self.event_bus = event_bus

        # 🎤 Cola de audio
        self.audio_queue = queue.Queue()

        # 🔊 Cola de voz
        self.tts_queue = queue.Queue()

        # Modelo VOSK (asegúrate que existe)
        self.model = Model("vosk-model-small-es-0.42")
        self.rec = KaldiRecognizer(self.model, 16000)

        # TTS
        self.tts = pyttsx3.init()

        # 🔥 HILO VOZ (hablar)
        threading.Thread(target=self._tts_worker, daemon=True).start()

    # =========================
    # 🔊 HABLAR (NO SE ROMPE)
    # =========================
    def _tts_worker(self):
        while True:
            text = self.tts_queue.get()
            try:
                self.tts.stop()
                self.tts.say(text)
                self.tts.runAndWait()
            except Exception as e:
                print("Error TTS:", e)

    def speak(self, text):
        self.tts_queue.put(text)

    # =========================
    # 🎤 ESCUCHAR
    # =========================
    def callback(self, indata, frames, time, status):
        self.audio_queue.put(bytes(indata))

    def listen(self):
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self.callback
        ):
            print("🎤 Escuchando...")

            while True:
                data = self.audio_queue.get()

                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "")

                    if text:
                        print("Usuario:", text)
                        self.event_bus.publish("voice_input", text)