import requests
import pyperclip
import re

class ClienteOllama:
    def __init__(self, modelo="qwen2.5-coder:7b"):
        self.url_generate = "http://localhost:11434/api/generate"
        self.url_chat = "http://localhost:11434/api/chat"
        self.modelo = modelo
        
        # Memoria de conversación para el Modo Dev
        self.historial_dev = [
            {
                "role": "system",
                "content": (
                    "Eres un ingeniero senior experto en desarrollo Android nativo con Kotlin (sin root), "
                    "Rust (JNI), y Python. Conoces el ecosistema del usuario (HexRootScan, HexRootFuzz, "
                    "HexColor, Daltonic Assist Pro, DemoniTalk). "
                    "Cuando te pasen código o te pidan implementar una función, devuelve el código completo, "
                    "limpio, eficiente y sin recortes. Responde en español directo."
                )
            }
        ]

    def resetear_memoria(self):
        self.historial_dev = [self.historial_dev[0]]

    def consultar_charla(self, prompt):
        try:
            payload = {"model": self.modelo, "prompt": prompt, "stream": False}
            res = requests.post(self.url_generate, json=payload, timeout=30)
            if res.status_code == 200:
                return res.json().get("response", "").strip()
        except Exception as e:
            print(f"[Error Charla Ollama]: {e}")
        return "Error conectando con Ollama."

    def consultar_modo_dev(self, orden_voz):
        codigo_portapapeles = pyperclip.paste().strip()
        mensaje_completo = orden_voz

        if codigo_portapapeles:
            mensaje_completo += f"\n\nCódigo actual en mi editor:\n```\n{codigo_portapapeles}\n```"

        self.historial_dev.append({"role": "user", "content": mensaje_completo})

        try:
            payload = {
                "model": self.modelo,
                "messages": self.historial_dev,
                "stream": False,
                "options": {"num_ctx": 8192, "num_predict": 8192, "temperature": 0.2}
            }
            res = requests.post(self.url_chat, json=payload, timeout=120)
            
            if res.status_code == 200:
                contenido = res.json()["message"]["content"]
                self.historial_dev.append(res.json()["message"])

                # Extraer bloques de código Markdown o copiar todo
                bloques = re.findall(r"```(?:\w+)?\n(.*?)```", contenido, re.DOTALL)
                if bloques:
                    codigo_limpio = "\n\n".join(bloques)
                    pyperclip.copy(codigo_limpio)
                else:
                    pyperclip.copy(contenido)

                return contenido, "¡Script generado y copiado directo al portapapeles!"
            else:
                return "Error en la respuesta de Ollama.", False
        except Exception as e:
            return f"[Error Modo Dev]: {e}", False
