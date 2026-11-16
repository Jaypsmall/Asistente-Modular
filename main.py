import threading
import time
import customtkinter as ctk

from acciones_pc import ejecutar_accion_pc
from audio_engine import MotorAudio
from gestor_voz import GestorVozAsync
from ollama_client import ClienteOllama

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AsistenteModularTallerPro(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Taller Central PRO — Centro de Comando IA")
        self.geometry("1020x720")
        self.minsize(920, 650)

        # Estado interno
        self.escuchando = False
        self.modo_actual = "desarrollador"
        self.velocidad_voz = 140

        # Instanciar motores externos
        self.audio = MotorAudio()
        self.ollama = ClienteOllama()
        self.voz = GestorVozAsync(
            cliente_ollama=self.ollama,
            velocidad=self.velocidad_voz,
            callback_log=self.log,
        )

        # Configurar Grid Principal (1 fila, 2 columnas: Sidebar + Área Principal)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._construir_sidebar()
        self._construir_area_principal()

        self.log("Sistema inicializado. Selecciona un modo en el panel izquierdo y pulsa 'INICIAR SISTEMA'.", "sistema")
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

    # =========================================================================
    # CONSTRUCCIÓN DE LA INTERFAZ (UI/UX PRO)
    # =========================================================================
    def _construir_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#16181d")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Logo / Título
        self.lbl_logo = ctk.CTkLabel(
            self.sidebar,
            text="⚡ TALLER CENTRAL",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff",
        )
        self.lbl_logo.pack(pady=(25, 2), padx=20, anchor="w")

        self.lbl_subtitulo = ctk.CTkLabel(
            self.sidebar,
            text="Multi-Módulo IA v2.0",
            font=ctk.CTkFont(size=12),
            text_color="#868e96",
        )
        self.lbl_subtitulo.pack(pady=(0, 20), padx=20, anchor="w")

        # Separador visual
        ctk.CTkFrame(self.sidebar, height=2, fg_color="#2b2f38").pack(fill="x", padx=15, pady=5)

        # Sección Modos
        ctk.CTkLabel(
            self.sidebar,
            text="MODOS DE OPERACIÓN",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#adb5bd",
        ).pack(pady=(15, 8), padx=20, anchor="w")

        self.btn_dev = ctk.CTkButton(
            self.sidebar,
            text="💻  Modo Desarrollador",
            command=lambda: self.cambiar_modo("desarrollador"),
            fg_color="#1c7ed6",
            hover_color="#1971c2",
            anchor="w",
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.btn_dev.pack(fill="x", padx=15, pady=4)

        self.btn_asistente = ctk.CTkButton(
            self.sidebar,
            text="⚙️  Modo Asistente PC",
            command=lambda: self.cambiar_modo("asistente"),
            fg_color="transparent",
            hover_color="#2b2f38",
            anchor="w",
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=13),
        )
        self.btn_asistente.pack(fill="x", padx=15, pady=4)

        self.btn_charla = ctk.CTkButton(
            self.sidebar,
            text="💬  Modo Charla Libre",
            command=lambda: self.cambiar_modo("charla"),
            fg_color="transparent",
            hover_color="#2b2f38",
            anchor="w",
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=13),
        )
        self.btn_charla.pack(fill="x", padx=15, pady=4)

        # Separador visual
        ctk.CTkFrame(self.sidebar, height=2, fg_color="#2b2f38").pack(fill="x", padx=15, pady=15)

        # Sección Ajustes Rápidos
        ctk.CTkLabel(
            self.sidebar,
            text="AJUSTES DE VOZ Y MEMORIA",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#adb5bd",
        ).pack(pady=(5, 5), padx=20, anchor="w")

        self.lbl_vel = ctk.CTkLabel(
            self.sidebar,
            text=f"Velocidad Voz: {self.velocidad_voz} wpm",
            font=ctk.CTkFont(size=12),
            text_color="#ced4da",
        )
        self.lbl_vel.pack(pady=(5, 0), padx=20, anchor="w")

        self.slider_vel = ctk.CTkSlider(
            self.sidebar,
            from_=100,
            to=220,
            number_of_steps=12,
            command=self._actualizar_velocidad,
        )
        self.slider_vel.set(self.velocidad_voz)
        self.slider_vel.pack(fill="x", padx=20, pady=(5, 15))

        self.btn_reset = ctk.CTkButton(
            self.sidebar,
            text="🧹  Resetear Memoria IA",
            command=self.resetear_memoria,
            fg_color="#2b2f38",
            hover_color="#e67e22",
            height=35,
            corner_radius=8,
        )
        self.btn_reset.pack(fill="x", padx=15, pady=5)

        self.btn_limpiar_log = ctk.CTkButton(
            self.sidebar,
            text="🗑️  Limpiar Consola",
            command=self.limpiar_consola,
            fg_color="#2b2f38",
            hover_color="#495057",
            height=35,
            corner_radius=8,
        )
        self.btn_limpiar_log.pack(fill="x", padx=15, pady=5)

        # Botones principales al fondo del Sidebar
        self.frame_power = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.frame_power.pack(side="bottom", fill="x", padx=15, pady=20)

        self.btn_iniciar = ctk.CTkButton(
            self.frame_power,
            text="▶  INICIAR SISTEMA",
            command=self.iniciar_asistente,
            fg_color="#2b8a3e",
            hover_color="#216a30",
            height=42,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.btn_iniciar.pack(fill="x", pady=4)

        self.btn_detener = ctk.CTkButton(
            self.frame_power,
            text="⏹  DETENER SISTEMA",
            command=self.detener_asistente,
            fg_color="#c92a2a",
            hover_color="#a61e1e",
            state="disabled",
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.btn_detener.pack(fill="x", pady=4)

    def _construir_area_principal(self):
        self.main_area = ctk.CTkFrame(self, fg_color="#1e2128", corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        # --- BARRA SUPERIOR (HUD DE ESTADO) ---
        self.top_bar = ctk.CTkFrame(self.main_area, height=70, fg_color="#252830", corner_radius=12)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.top_bar.grid_columnconfigure(0, weight=1)

        self.lbl_estado = ctk.CTkLabel(
            self.top_bar,
            text="● SISTEMA EN ESPERA  |  MODO: DESARROLLADOR",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#adb5bd",
        )
        self.lbl_estado.grid(row=0, column=0, padx=20, pady=(12, 4), sticky="w")

        self.btn_silenciar = ctk.CTkButton(
            self.top_bar,
            text="🔇 Callar Voz",
            command=self.silenciar_voz,
            fg_color="#3b5bdb",
            hover_color="#364fc7",
            width=120,
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.btn_silenciar.grid(row=0, column=1, rowspan=2, padx=20, pady=10)

        # Barra de actividad animada
        self.barra_actividad = ctk.CTkProgressBar(
            self.top_bar,
            height=4,
            mode="indeterminate",
            progress_color="#1c7ed6",
            fg_color="#16181d",
        )
        self.barra_actividad.grid(row=1, column=0, padx=20, pady=(0, 12), sticky="ew")
        self.barra_actividad.set(0)

        # --- CONSOLA CENTRAL CON COLORES ---
        self.txt_log = ctk.CTkTextbox(
            self.main_area,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="#131519",
            text_color="#e9ecef",
            border_width=1,
            border_color="#2f333d",
            corner_radius=12,
            wrap="word",
        )
        self.txt_log.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)

        # Configurar etiquetas de color en el widget interno de Tkinter
        self.txt_log._textbox.tag_config("sistema", foreground="#74c0fc")
        self.txt_log._textbox.tag_config("usuario", foreground="#69db7c")
        self.txt_log._textbox.tag_config("ia", foreground="#ffd43b")
        self.txt_log._textbox.tag_config("error", foreground="#ff6b6b")
        self.txt_log._textbox.tag_config("normal", foreground="#dee2e6")

        # --- BARRA INFERIOR: COMANDO POR TEXTO (MODO SILENCIOSO) ---
        self.bottom_bar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.bottom_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        self.bottom_bar.grid_columnconfigure(0, weight=1)

        self.entry_comando = ctk.CTkEntry(
            self.bottom_bar,
            placeholder_text="Escribe una orden directa aquí (o habla por el micrófono al iniciar)...",
            height=40,
            corner_radius=10,
            fg_color="#252830",
            border_color="#373b47",
            font=ctk.CTkFont(size=13),
        )
        self.entry_comando.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entry_comando.bind("<Return>", lambda event: self.enviar_comando_manual())

        self.btn_enviar = ctk.CTkButton(
            self.bottom_bar,
            text="Enviar ➤",
            command=self.enviar_comando_manual,
            width=100,
            height=40,
            corner_radius=10,
            fg_color="#1c7ed6",
            hover_color="#1971c2",
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.btn_enviar.grid(row=0, column=1)

    # =========================================================================
    # LÓGICA Y EVENTOS DE INTERFAZ
    # =========================================================================
    def _actualizar_velocidad(self, valor):
        self.velocidad_voz = int(valor)
        self.lbl_vel.configure(text=f"Velocidad Voz: {self.velocidad_voz} wpm")
        if hasattr(self.voz, "velocidad"):
            self.voz.velocidad = self.velocidad_voz

    def limpiar_consola(self):
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.configure(state="disabled")

    def cambiar_modo(self, nuevo_modo):
        self.voz.interrumpir()
        self.modo_actual = nuevo_modo

        # Resetear estilos botones
        for btn in (self.btn_charla, self.btn_asistente, self.btn_dev):
            btn.configure(fg_color="transparent", font=ctk.CTkFont(size=13))

        color_activo = "#1c7ed6"
        if nuevo_modo == "charla":
            self.btn_charla.configure(fg_color="#2b8a3e", font=ctk.CTkFont(size=13, weight="bold"))
            color_activo = "#2b8a3e"
        elif nuevo_modo == "asistente":
            self.btn_asistente.configure(fg_color="#e67e22", font=ctk.CTkFont(size=13, weight="bold"))
            color_activo = "#e67e22"
        elif nuevo_modo == "desarrollador":
            self.btn_dev.configure(fg_color="#1c7ed6", font=ctk.CTkFont(size=13, weight="bold"))
            color_activo = "#1c7ed6"

        self.barra_actividad.configure(progress_color=color_activo)
        self.actualizar_hud_estado()
        self.log(f"\n[SISTEMA] Modo cambiado a: {nuevo_modo.upper()}", "sistema")
        self.hablar(f"Modo {nuevo_modo} activado.")

    def actualizar_hud_estado(self):
        if self.escuchando:
            self.lbl_estado.configure(
                text=f"● ESCUCHANDO ACTIVO  |  MODO: {self.modo_actual.upper()}",
                text_color="#51cf66",
            )
        else:
            self.lbl_estado.configure(
                text=f"● SISTEMA EN ESPERA  |  MODO: {self.modo_actual.upper()}",
                text_color="#adb5bd",
            )

    def silenciar_voz(self):
        self.voz.interrumpir()
        self.log("[Voz silenciada manualmente]", "sistema")

    def resetear_memoria(self):
        self.voz.interrumpir()
        self.ollama.resetear_memoria("todos")
        self.log("\n[MEMORIA] Historiales de Dev y Charla reiniciados.", "sistema")
        self.hablar("Memoria reiniciada.")

    def hablar(self, texto):
        self.voz.decir_directo(texto)

    def log(self, mensaje, tipo="normal"):
        # Autodetección de color si viene desde callbacks externos
        if tipo == "normal":
            if "🎙️ Tú:" in mensaje:
                tipo = "usuario"
            elif "QWEN" in mensaje or "✅" in mensaje:
                tipo = "ia"
            elif "⚠️" in mensaje or "❌" in mensaje or "Aviso" in mensaje:
                tipo = "error"
            elif "===" in mensaje or "[" in mensaje:
                tipo = "sistema"

        def _insertar():
            self.txt_log.configure(state="normal")
            self.txt_log.insert("end", f"{mensaje}\n", tipo)
            self.txt_log.see("end")
            self.txt_log.configure(state="disabled")

        self.after(0, _insertar)

    def iniciar_asistente(self):
        self.escuchando = True
        self.btn_iniciar.configure(state="disabled")
        self.btn_detener.configure(state="normal")
        self.barra_actividad.start()
        self.actualizar_hud_estado()

        self.log(f"\n=== TALLER ACTIVADO [MODO: {self.modo_actual.upper()}] ===", "sistema")
        self.hablar("Taller activado.")

        threading.Thread(target=self.bucle_principal_escucha, daemon=True).start()

    def detener_asistente(self):
        self.escuchando = False
        self.voz.interrumpir()
        self.btn_iniciar.configure(state="normal")
        self.btn_detener.configure(state="disabled")
        self.barra_actividad.stop()
        self.barra_actividad.set(0)
        self.actualizar_hud_estado()

        self.log("=== ASISTENTE DETENIDO ===", "sistema")
        self.hablar("Asistente detenido.")

    def al_cerrar(self):
        self.escuchando = False
        self.voz.apagar()
        self.destroy()

    # =========================================================================
    # PROCESAMIENTO DE ÓRDENES (VOZ Y TEXTO)
    # =========================================================================
    def enviar_comando_manual(self):
        texto = self.entry_comando.get().strip()
        if not texto:
            return
        self.entry_comando.delete(0, "end")
        threading.Thread(target=self._procesar_orden, args=(texto, True), daemon=True).start()

    def _confirmar_orden_voz(self, orden_detectada):
        self.log(f"❓ ¿Confirmar orden?: '{orden_detectada}'", "sistema")
        self.hablar(f"He entendido: {orden_detectada}. ¿Lo lanzo o cancelo?")

        time.sleep(0.3)
        while self.voz.esta_hablando() and self.escuchando:
            time.sleep(0.1)

        if not self.escuchando:
            return False

        respuesta = self.audio.escuchar_frase(duracion=4).lower().strip()
        self.log(f"🎙️ Confirmación: '{respuesta}'", "usuario")

        palabras_si = ("sí", "si", "dale", "confirma", "confirmar", "adelante", "vale", "ok", "lanza", "ejecuta")
        if any(p in respuesta.split() or p in respuesta for p in palabras_si) and "no" not in respuesta.split():
            return True

        return False

    def _procesar_orden(self, texto, es_manual=False):
        prefijo = "⌨️ Tú:" if es_manual else "🎙️ Tú:"
        self.log(f"\n{prefijo} '{texto}'", "usuario")
        texto_lower = texto.lower()

        if "cállate" in texto_lower or "silencio" in texto_lower:
            self.voz.interrumpir()
            return

        if "apagar sistema" in texto_lower or "apagar asistente" in texto_lower:
            self.hablar("Apagando el taller.")
            self.after(0, self.detener_asistente)
            return

        # Cambio de modo por comando
        if any(f in texto_lower for f in ("modo charla", "pasa a charla", "cambia a charla", "activar charla")):
            self.after(0, lambda: self.cambiar_modo("charla"))
            return

        if any(f in texto_lower for f in ("modo asistente", "pasa a asistente", "cambia a asistente", "activar asistente")):
            self.after(0, lambda: self.cambiar_modo("asistente"))
            return

        if any(f in texto_lower for f in ("modo dev", "modo desarrollador", "pasa a dev", "cambia a desarrollador", "activar desarrollo")):
            self.after(0, lambda: self.cambiar_modo("desarrollador"))
            return

        # Enrutamiento según modo
        if self.modo_actual == "charla":
            self.voz.responder_charla(texto)

        elif self.modo_actual == "asistente":
            resultado = ejecutar_accion_pc(texto)
            self.log(f"⚙️ {resultado}", "ia")
            self.hablar("Acción ejecutada.")

        elif self.modo_actual == "desarrollador":
            # Si viene por teclado no hace falta confirmación por voz
            if not es_manual:
                if not self._confirmar_orden_voz(texto):
                    self.log("❌ Orden de código cancelada.", "error")
                    self.hablar("Cancelado, hermano. Dime de nuevo cuando quieras.")
                    return

            self.hablar("Procesando código, hermano.")
            contenido, estado_msg = self.ollama.consultar_modo_dev(texto)

            if estado_msg:
                self.log(
                    "\n🤖 QWEN DEV OUTPUT:\n"
                    + "=" * 55
                    + f"\n{contenido}\n"
                    + "=" * 55,
                    "ia",
                )
                self.log(f"✅ {estado_msg}", "sistema")
                self.hablar(
                    "Listo hermano, código generado y copiado en el portapapeles. Quedo a la espera de la siguiente orden."
                )
            else:
                self.log(f"⚠️ {contenido}", "error")
                self.hablar("Hubo un fallo generando el código.")

    def bucle_principal_escucha(self):
        while self.escuchando:
            try:
                if self.voz.esta_hablando():
                    time.sleep(0.15)
                    continue

                texto = self.audio.escuchar_frase(duracion=9)
                if not self.escuchando or not texto.strip():
                    continue

                self._procesar_orden(texto, es_manual=False)

            except Exception as e:
                self.log(f"[Aviso de Hilo - Recuperado]: {e}", "error")
                time.sleep(1)


if __name__ == "__main__":
    app = AsistenteModularTallerPro()
    app.mainloop()
