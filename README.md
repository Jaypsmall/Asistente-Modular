# 🛠️ Taller Central - Asistente Modular Offline (Windows)  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/windows8/windows8-original.svg" height="60" alt="Windows" />

Asistente de escritorio modular, 100% offline y diseñado para entornos de desarrollo de alto rendimiento en Windows (optimizado para equipos con 16 GB de RAM), utilizando modelos locales para mantener total privacidad y escapar de bloqueos de API en la nube.

---

## 🚀 Arquitectura Modular (Anti-Crashes)

El proyecto está estructurado en varios archivos independientes para aislar los hilos en segundo plano y evitar que fallos de hardware o audio congelen la interfaz gráfica:

1. **`main.py`**: Núcleo visual construido con **CustomTkinter**. Gestiona los modos, la consola de logs y los hilos seguros de ejecución.
2. **`audio_engine.py`**: Motor de reconocimiento de voz offline utilizando **Vosk** y `sounddevice` (carpeta `model-es`).
3. **`ollama_client.py`**: Cliente de integración local con **Ollama** (`Qwen 2.5 Coder`), soporte para chat, ventana de contexto ampliada de **8192 tokens** (`num_ctx`), lectura automática del portapapeles (`pyperclip`) y autoevaluación de scripts limpios.
4. **`acciones_pc.py`**: Automatización y control de ventanas de Windows mediante **PyAutoGUI** y comandos del sistema.

---

## 🎯 Modos de Operación

- **💬 Modo Charla**: Conversación fluida con la IA para resolución de dudas rápidas.
- **⚙️ Modo Asistente**: Control por voz de aplicaciones de Windows, carpetas y búsquedas web.
- **💻 Modo Desarrollador (Copiloto)**: Captura tu código copiado en el portapapeles con `Ctrl + C`, lo procesa con Qwen 2.5 Coder usando 8k tokens de contexto y te devuelve el script limpio directamente al portapapeles listo para pegar en Android Studio.

---

## 📋 Requisitos e Instalación

1. Tener instalado **Python** y **Ollama** corriendo localmente (`http://localhost:11434`) con el modelo `qwen2.5-coder:7b`.
2. Instalar las dependencias de Python necesarias ejecutando:
   `pip install customtkinter sounddevice vosk pyperclip pyautogui requests`
3. Asegurarte de tener la carpeta con el modelo de voz offline (`model-es`) en el directorio raíz.
4. Arrancar el taller ejecutando:
   `python main.py`

<p align="center">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" height="60" alt="Python" />
  &nbsp;&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/windows8/windows8-original.svg" height="60" alt="Windows" />
  &nbsp;&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/ollama/ollama-original.svg" height="60" alt="Ollama" />
</p>

---

## 📂 Estructura del Proyecto

Así es como debe organizarse el carpetado en tu PC para que todos los módulos se comuniquen perfectamente:

```text
Asistente-Modular-Taller/
│
├── main.py              # Núcleo visual (CustomTkinter)
├── audio_engine.py      # Motor de voz offline (Vosk)
├── ollama_client.py     # Conexión local con Ollama (Qwen 2.5 Coder)
├── acciones_pc.py       # Automatización de Windows (PyAutoGUI)
├── model-es/            # Carpeta con el modelo de voz en español de Vosk
└── README.md            # Documentación oficial del taller
```

---

## 📥 Clonar el Repositorio

Si quieres clonar este taller directamente en el PC de tu estación de trabajo, abre tu terminal y ejecuta:

```text
git clone https://github.com/illoquediC/Asistente-Modular.git
cd Asistente-Modular
```
---

## 👨‍💻 Desarrollado por

Creado y mantenido por **Jaypsmall** ([GitHub](https://github.com/Jaypsmall)). 

¡El proyecto es de código abierto y totalmente modular! Si eres desarrollador y quieres meterle mejoras, optimizar hilos o implementar nuevas herramientas a este asistente offline, las pull requests y colaboraciones son totalmente bienvenidas. 🚀

---

## 📄 Licencia

Este proyecto se distribuye bajo los términos de la licencia **MIT**. Siéntete libre de usarlo, modificarlo y adaptarlo a tus necesidades en el taller.
