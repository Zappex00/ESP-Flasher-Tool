
# ESP-Flasher-Tool

> **Aviso de Uso Responsable:** Las herramientas de auditoría y pruebas Wi-Fi deben utilizarse únicamente en dispositivos y redes propias o cuando se tenga autorización explícita para realizar pruebas de seguridad.

---

## Requisitos

[Python 3.14 o superior](https://www.python.org)
* **Hardware:** Dispositivo ESP32 compatible + Cable USB de datos
* **Software:** Firmware a instalar (`.bin`) y librería `esptool`

---

## 🐍 1. Instalación de Python

1. Descarga el instalador oficial desde [python.org/downloads](https.www.python.org/downloads/).
2. Durante la instalación, **asegúrate de marcar la casilla:**
   > `Add Python to PATH`

---

## 📦 2. Instalación de `esptool`

Abre tu terminal (CMD o PowerShell) y ejecuta los siguientes comandos:

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install esptool
