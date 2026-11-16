import threading
import time
import customtkinter as ctk
import pyttsx3

from audio_engine import MotorAudio
from ollama_client import ClienteOllama
from acciones_pc import ejecutar_accion_pc

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class AsistenteModularTaller(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Taller Central - Asistente Modular Definitivo")
        self.geometry("780x800")
        self.resizable(False, False)

        self.escuchando = False
        self.modo_actual = "desarrollador"

        # Instanciar motores externos
        self.audio = MotorAudio()
        self.ollama = ClienteOllama()

        # --- INTERFAZ GRÁFICA ---
        self.lbl_titulo = ctk.CTkLabel(
            self, text="Taller Central (Multi-Módulo)", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_titulo.pack(pady=(15, 5))

        self.lbl_estado = ctk.CTkLabel(
            self, text="Estado: Detenido | Modo: Desarrollador", font=ctk.CTkFont(size=14, weight="bold"), text_color="#1c7ed6"
        )
        self.lbl_estado.pack(pady=2)

        # Botones de Modos
        self.frame_modos = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_modos.pack(pady=5)

        self.btn_charla = ctk.CTkButton(
            self.frame_modos, text="💬 Modo Charla", command=lambda: self.cambiar_modo("charla"),
            fg_color="#495057", width=130, height=30
        )
        self.btn_charla.pack(side="left", padx=5)

        self.btn_asistente = ctk.CTkButton(
            self.frame_modos, text="⚙️ Modo Asistente", command=lambda: self.cambiar_modo("asistente"),
            fg_color="#495057", width=130, height=30
        )
        self.btn_asistente.pack(side="left", padx=5)

        self.btn_dev = ctk.CTkButton(
            self.frame_modos, text="💻 Modo Dev", command=lambda: self.cambiar_modo("desarrollador"),
            fg_color="#1c7ed6", width=130, height=30
        )
        self.btn_dev.pack(side="left", padx=5)

        # Botones de Control Principal
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.pack(pady=10)

        self.btn_iniciar = ctk.CTkButton(
            self.frame_botones, text="Iniciar Asistente", command=self.iniciar_asistente,
            fg_color="#2b8a3e", hover_color="#216a30", width=140, height=35
        )
        self.btn_iniciar.pack(side="left", padx=5)

        self.btn_detener = ctk.CTkButton(
            self.frame_botones, text="Detener Asistente", command=self.detener_asistente,
            fg_color="#c92a2a", hover_color="#962020", state="disabled", width=140, height=35
        )
        self.btn_detener.pack(side="left", padx=5)

        self.btn_reset = ctk.CTkButton(
            self.frame_botones, text="Reset Memoria Dev", command=self.resetear_memoria,
            fg_color="#e67e22", hover_color="#d35400", width=150, height=35
        )
        self.btn_reset.pack(side="left", padx=5)

        # Consola de Logs
        self.txt_log = ctk.CTkTextbox(self, width=720, height=540, font=ctk.CTkFont(family="Consolas", size=13))
        self.txt_log.pack(pady=10, padx=20)

        self.log("Taller listo. Elige modo arriba y presiona 'Iniciar Asistente'.")
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

    def cambiar_modo(self, nuevo_modo):
        self.modo_actual = nuevo_modo
        self.btn_charla.configure(fg_color="#495057")
        self.btn_asistente.configure(fg_color="#495057")
        self.btn_dev.configure(fg_color="#495057")

        if nuevo_modo == "charla":
            self.btn_charla.configure(fg_color="#2b8a3e")
        elif nuevo_modo == "asistente":
            self.btn_asistente.configure(fg_color="#e67e22")
        elif nuevo_modo == "desarrollador":
            self.btn_dev.configure(fg_color="#1c7ed6")

        self.log(f"\n[Modo Cambiado]: {nuevo_modo.upper()}")
        self.lbl_estado.configure(text=f"Estado: {'Escuchando...' if self.escuchando else 'Detenido'} | Modo: {nuevo_modo.capitalize()}")
        self.hablar(f"Modo {nuevo_modo} activado.")

    def resetear_memoria(self):
        self.ollama.resetear_memoria()
        self.log("\n[Memoria Dev] Historial de código limpiado.")
        self.hablar("Memoria de desarrollo reiniciada.")

    def hablar(self, texto):
        def _voz():
            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", 170)
                for voz in engine.getProperty("voices"):
                    if "spanish" in voz.name.lower() or "es" in voz.id.lower():
                        engine.setProperty("voice", voz.id)
                        break
                engine.say(texto)
                engine.runAndWait()
            except Exception:
                pass
        threading.Thread(target=_voz, daemon=True).start()

    def log(self, mensaje):
        self.after(0, lambda: (
            self.txt_log.configure(state="normal"),
            self.txt_log.insert("end", f"{mensaje}\n"),
            self.txt_log.see("end"),
            self.txt_log.configure(state="disabled")
        ))

    def iniciar_asistente(self):
        self.escuchando = True
        self.btn_iniciar.configure(state="disabled")
        self.btn_detener.configure(state="normal")
        self.lbl_estado.configure(text=f"Estado: Escuchando... | Modo: {self.modo_actual.capitalize()}")
        self.log(f"\n=== Taller Activado [Modo: {self.modo_actual.upper()}] ===")
        self.hablar("Taller activado.")
        
        threading.Thread(target=self.bucle_principal_escucha, daemon=True).start()

    def detener_asistente(self):
        self.escuchando = False
        self.btn_iniciar.configure(state="normal")
        self.btn_detener.configure(state="disabled")
        self.lbl_estado.configure(text=f"Estado: Detenido | Modo: {self.modo_actual.capitalize()}")
        self.log("=== Asistente Detenido ===")
        self.hablar("Asistente detenido.")

    def al_cerrar(self):
        self.escuchando = False
        self.destroy()

    def bucle_principal_escucha(self):
        while self.escuchando:
            try:
                texto = self.audio.escuchar_frase(duracion=6)
                if not self.escuchando or not texto.strip():
                    continue

                self.log(f"\n🎙️ Tú: '{texto}'")

                if "apagar sistema" in texto or "apagar asistente" in texto:
                    self.hablar("Apagando el taller.")
                    self.after(0, self.detener_asistente)
                    break

                # Enrutamiento según el modo activo
                if self.modo_actual == "charla":
                    respuesta = self.ollama.consultar_charla(texto)
                    self.log(f"🤖 IA Charla: {respuesta}")
                    self.hablar(respuesta[:150])
                    
                elif self.modo_actual == "asistente":
                    resultado = ejecutar_accion_pc(texto)
                    self.log(f"⚙️ {resultado}")
                    self.hablar("Acción ejecutada.")
                    
                elif self.modo_actual == "desarrollador":
                    self.hablar("Procesando código, hermano.")
                    contenido, estado_msg = self.ollama.consultar_modo_dev(texto)
                    self.log("\n🤖 QWEN DEV OUTPUT:\n" + "="*50 + f"\n{contenido}\n" + "="*50)
                    self.log(f"✅ {estado_msg}")
                    self.hablar("Listo hermano, código generado y copiado en el portapapeles.")

            except Exception as e:
                self.log(f"[Aviso de Hilo - Recuperado]: {e}")
                time.sleep(1)


if __name__ == "__main__":
    app = AsistenteModularTaller()
    app.mainloop()
