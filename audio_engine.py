import os
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

class MotorAudio:
    def __init__(self, modelo_path="model-es"):
        self.fs = 16000
        self.modelo_path = modelo_path
        self.model = None
        self.rec = None
        self.cargar_modelo()

    def cargar_modelo(self):
        if not os.path.exists(self.modelo_path):
            print(f"[Error Audio] No se encuentra la carpeta '{self.modelo_path}' de Vosk.")
            return False
        try:
            self.model = Model(self.modelo_path)
            self.rec = KaldiRecognizer(self.model, self.fs)
            print("[Audio] Modelo Vosk cargado correctamente.")
            return True
        except Exception as e:
            print(f"[Error al cargar Vosk]: {e}")
            return False

    def escuchar_frase(self, duracion=6):
        if not self.model:
            return ""
        try:
            # Captura audio del micro
            grabacion = sd.rec(int(duracion * self.fs), samplerate=self.fs, channels=1, dtype="int16")
            sd.wait()

            if self.rec.AcceptWaveform(grabacion.tobytes()):
                resultado = json.loads(self.rec.Result())
                return resultado.get("text", "").lower()
            else:
                resultado = json.loads(self.rec.PartialResult())
                return resultado.get("partial", "").lower()
        except Exception as e:
            print(f"[Error de escucha]: {e}")
            return ""
