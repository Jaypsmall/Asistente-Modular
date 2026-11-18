# 🛠️ Taller Central - Asistente Modular Offline (Windows) 

Asistente de escritorio modular, 100% offline y diseñado para entornos de desarrollo de alto rendimiento en Windows (optimizado para equipos con 16 GB de RAM), utilizando modelos locales para mantener total privacidad y escapar de bloqueos de API en la nube.

<table width="100%">
  <tr>
    <td align="left" width="70%">
      <img src="https://github.com/Jaypsmall/Asistente-Modular/blob/040c702c1aed6295f9b0f644d4c3341c173a0862/assets/interfaz.jpg" width="100%" alt="Interfaz Taller Central">
    </td>
    <td align="center" width="30%">
      <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/windows8/windows8-original.svg" width="55%" alt="Windows">
      <br><br>
      <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="55%" alt="Python">
    </td>
  </tr>
</table>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/CustomTkinter-UI-0078D4?style=for-the-badge&logo=windows&logoColor=white" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/Ollama-Local_AI-121212?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama">
  <img src="https://img.shields.io/badge/Vosk-Speech_Offline-FF6F00?style=for-the-badge&logo=speaker&logoColor=white" alt="Vosk">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License MIT">
</p>

---

## 🚀 Arquitectura Modular (Anti-Crashes)

El proyecto está estructurado en varios archivos independientes para aislar los hilos en segundo plano y evitar que fallos de hardware o audio congelen la interfaz gráfica:

| Módulo | Descripción Técnica |
| :--- | :--- |
| **`main.py`** | Núcleo visual construido con **CustomTkinter**. Gestiona los modos, la consola de logs y los hilos seguros de ejecución. |
| **`audio_engine.py`** | Motor de reconocimiento de voz offline utilizando **Vosk** y `sounddevice` (carpeta `model-es`). |
| **`ollama_client.py`** | Cliente de integración local con **Ollama** (`Qwen 2.5 Coder`), chat, ventana ampliada de **8192 tokens** (`num_ctx`), lectura de portapapeles (`pyperclip`) y autoevaluación. |
| **`acciones_pc.py`** | Automatización y control de ventanas de Windows mediante **PyAutoGUI** y comandos del sistema. |

---

## 🎯 Modos de Operación

- **💬 Modo Charla**: Conversación fluida con la IA para resolución de dudas rápidas.
- **⚙️ Modo Asistente**: Control por voz de aplicaciones de Windows, carpetas y búsquedas web.
- **💻 Modo Desarrollador (Copiloto)**: Captura tu código copiado en el portapapeles con `Ctrl + C`, lo procesa con Qwen 2.5 Coder usando 8k tokens de contexto y te devuelve el script limpio directamente al portapapeles listo para pegar en Android Studio.

---

## 📋 Requisitos e Instalación

1. Tener instalado **Python** y **Ollama** corriendo localmente (`http://localhost:11434`) con el modelo `qwen2.5-coder:7b`.
2. Instalar las dependencias de Python necesarias ejecutando:
   ```bash
   pip install customtkinter sounddevice vosk pyperclip pyautogui requests
   ```
3. Asegurarte de tener la carpeta con el modelo de voz offline (`model-es`) en el directorio raíz.
4. Arrancar el taller ejecutando:
   ```bash
   python main.py
   ```

---

## 📂 Estructura del Proyecto

```text
Asistente-Modular-Taller/
│
├── 📄 main.py              # Núcleo visual (CustomTkinter)
├── 📄 audio_engine.py      # Motor de voz offline (Vosk)
├── 📄 ollama_client.py     # Conexión local con Ollama (Qwen 2.5 Coder)
├── 📄 acciones_pc.py       # Automatización de Windows (PyAutoGUI)
├── 📁 model-es/            # Carpeta con el modelo de voz en español de Vosk
└── 📄 README.md            # Documentación oficial del taller
```

---

## 📥 Clonar el Repositorio

Si quieres clonar este taller directamente en tu estación de trabajo, abre tu terminal y ejecuta:

```bash
git clone [https://github.com/Jaypsmall/Asistente-Modular.git](https://github.com/Jaypsmall/Asistente-Modular.git)
cd Asistente-Modular
```

---

## 👨‍💻 Autoría y Colaboración

<div align="center">

> **Proyecto creado y mantenido con pasión por [Jaypsmall](https://github.com/Jaypsmall)**  
> *Desarrollo modular open-source para entornos de alta eficiencia.*

[![GitHub Profile](https://img.shields.io/badge/GitHub-Jaypsmall-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Jaypsmall)
[![Pull Requests Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=for-the-badge&logo=git&logoColor=white)](https://github.com/Jaypsmall/Asistente-Modular/pulls)

*¡Las pull requests, optimizaciones de hilos y nuevas herramientas para este asistente offline son totalmente bienvenidas!* 🚀

</div>

---

## 📄 Licencia

Este proyecto se distribuye bajo los términos de la licencia **MIT**. Siéntete libre de usarlo, modificarlo y adaptarlo a tus necesidades en el taller.
