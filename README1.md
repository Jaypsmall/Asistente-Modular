# 🛠️ Taller Central - Asistente Modular Local (Windows)

Asistente de escritorio modular para Windows que usa modelos locales de Ollama y Faster-Whisper. Una vez descargados los modelos, las conversaciones y el reconocimiento de voz se procesan en el equipo.

---

## 🚀 Arquitectura Modular (Anti-Crashes)

El proyecto está estructurado en varios archivos independientes para aislar los hilos en segundo plano y evitar que fallos de hardware o audio congelen la interfaz gráfica:

1. **`main.py`**: Interfaz **CustomTkinter**, modos, cola de eventos para mantener las actualizaciones de UI en el hilo principal y órdenes en segundo plano.
2. **`audio_engine.py`**: Reconocimiento de voz con **Faster-Whisper** y `sounddevice`. El modelo se carga al empezar a escuchar para que la ventana aparezca antes.
3. **`ollama_client.py`**: Conexión local a **Ollama** para charla, desarrollo y extracción de campos PDF mediante respuestas JSON.
4. **`pdf_engine.py`**: Lee campos AcroForm, sincroniza datos XFA cuando existen y guarda una copia; conserva el original.
5. **`gestor_voz.py`**: Síntesis de voz con un motor SAPI5 reutilizado durante la sesión.
6. **`acciones_pc.py`**: Comandos predefinidos de Windows con PyAutoGUI.

---

## 🎯 Modos de Operación

- **💬 Modo Charla**: Conversación fluida con la IA para resolución de dudas rápidas.
- **⚙️ Modo Asistente**: Control por voz de aplicaciones de Windows, carpetas y búsquedas web.
- **💻 Modo Desarrollador**: Puede usar el código del portapapeles como contexto y copia el resultado al portapapeles.
- **📄 Modo Rellenar PDF**: Selecciona un PDF interactivo, dicta o escribe los datos, elige por voz o en pantalla entre secciones duplicadas como Interesado y Representante, revisa la correspondencia y confírmala antes de guardar una copia `nombre_relleno.pdf`.

Cada modo de IA tiene instrucciones propias: desarrollo entrega código, charla responde para voz y PDF devuelve datos estructurados sin inventar información. El control del PC usa comandos directos.

El modo PDF necesita campos interactivos AcroForm. Para evitar asignaciones dudosas, la IA solo propone campos de texto con etiquetas legibles; casillas y opciones quedan intactas. El PDF escaneado o plano requiere OCR y posicionamiento de texto.

---

## 📋 Requisitos e Instalación

1. Instala **Python 3.10 o superior** y **Ollama**. Descarga el modelo configurado, por defecto `qwen2.5:latest`:
   `ollama pull qwen2.5:latest`
2. En una terminal abierta en el proyecto, instala las dependencias:
   `pip install -r requirements.txt`
3. Arranca el taller:
   `python main.py`

La primera ejecución de voz puede descargar el modelo `small` de Faster-Whisper si no está en la caché. Para usarlo sin conexión, inicia la aplicación y espera a que termine esa descarga antes de desconectar el equipo.

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
├── audio_engine.py      # Reconocimiento de voz (Faster-Whisper)
├── gestor_voz.py        # Síntesis de voz
├── ollama_client.py     # Modos IA y prompts por modo
├── pdf_engine.py        # Campos interactivos PDF AcroForm
├── acciones_pc.py       # Automatización de Windows (PyAutoGUI)
├── requirements.txt     # Dependencias Python
└── README.md            # Documentación oficial del taller
```

---

## 📥 Clonar el Repositorio

Si quieres clonar este taller directamente en el PC de tu estación de trabajo, abre tu terminal y ejecuta:

```text
git clone https://github.com/Jaypsmall/Asistente-Modular.git
cd Asistente-Modular
```
---

## 👨‍💻 Desarrollado por

Creado y mantenido por **Jaypsmall** ([GitHub](https://github.com/Jaypsmall)). 

¡El proyecto es de código abierto y totalmente modular! Si eres desarrollador y quieres meterle mejoras, optimizar hilos o implementar nuevas herramientas a este asistente offline, las pull requests y colaboraciones son totalmente bienvenidas. 🚀

---

## 📄 Licencia

Este proyecto se distribuye bajo los términos de la licencia **MIT**. Siéntete libre de usarlo, modificarlo y adaptarlo a tus necesidades en el taller.
