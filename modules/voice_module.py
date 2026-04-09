import threading
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyttsx3


class VoiceModule:
    def __init__(self, event_bus):
        self.event_bus = event_bus

        # Banderas de estado
        self.is_speaking = False

        # 🎤 Cola de audio
        self.audio_queue = queue.Queue()

        # 🔊 Cola de voz
        self.tts_queue = queue.Queue()

        # Modelo VOSK (asegúrate que existe)
        self.model = Model("vosk-model-small-es-0.42")
        self.rec = KaldiRecognizer(self.model, 16000)

        #MOTOR TTS
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 1.0)

        # 🔥 HILO VOZ (hablar)
        threading.Thread(target=self._tts_worker, daemon=True).start()

    # =========================
    # 🔊 HABLAR (NO SE ROMPE)
    # =========================
    def _tts_worker(self):
        while True:
            text = self.tts_queue.get()

        try:
            self.is_speaking = True
            self.tts_say(text)
            self.tts.runAndWait()
        except Exception as e:
            print("Error en TTS:", e)
        finally:
            self.is_speaking = False


    def speak(self, text):
        print("Speak llamado:", text)
        partes = text.split("\n")
        for parte in partes:
            if parte.strip():
                self.tts_queue.put(parte.strip())  # Agrega un punto para mejorar la entonación

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
            device=1,
            callback=self.callback
        ):
            print("🎤 Escuchando...")

            while True:
                data = self.audio_queue.get()

                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "")

                    if text and not self.is_speaking:
                        print("Usuario:", text)
                        self.event_bus.publish("voice_input", text)