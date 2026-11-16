# 🛠️ Taller Central - Asistente Modular Offline (Windows)

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

<p align="left">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" height="40" alt="Python" />
  &nbsp;&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/windows8/windows8-original.svg" height="40" alt="Windows" />
  &nbsp;&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/ollama/ollama-original.svg" height="40" alt="Ollama" />
</p>

1. Tener instalado **Python** y **Ollama** corriendo localmente (`http://localhost:11434`) con el modelo `qwen2.5-coder:7b`.
2. Instalar las dependencias de Python necesarias ejecutando:
   `pip install customtkinter sounddevice vosk pyperclip pyautogui requests`
3. Asegurarte de tener la carpeta con el modelo de voz offline (`model-es`) en el directorio raíz.
4. Arrancar el taller ejecutando:
   `python main.py`
