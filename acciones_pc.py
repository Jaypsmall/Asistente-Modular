import subprocess
import urllib.parse
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

APPS_EXTRAS = {
    "calculadora": "calc",
    "paint": "mspaint",
    "cmd": "cmd",
    "terminal": "wt",
    "android studio": "studio64.exe",
}

def ejecutar_accion_pc(cmd):
    cmd_lower = cmd.lower()
    
    if "busca" in cmd_lower:
        query = cmd_lower.split("busca", 1)[1].strip()
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        subprocess.run(["start", url], shell=True)
        return f"Buscando en Google: {query}"
        
    elif "abre" in cmd_lower:
        target = cmd_lower.split("abre", 1)[1].strip()
        if target in APPS_EXTRAS:
            subprocess.run(["start", APPS_EXTRAS[target]], shell=True)
        else:
            subprocess.run(["start", target], shell=True)
        return f"Abriendo: {target}"
        
    elif "pega" in cmd_lower or "pegar" in cmd_lower:
        pyautogui.hotkey("ctrl", "v")
        return "Pegando contenido (Ctrl+V)"
        
    return "Comando de PC no reconocido."
