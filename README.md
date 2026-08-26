
# ESP-Flasher-Tool

> **Aviso de Uso Responsable:** Las herramientas de auditoría y pruebas Wi-Fi deben utilizarse únicamente en dispositivos y redes propias o cuando se tenga autorización explícita para realizar pruebas de seguridad.

## Requisitos

* [Python 3.14 o superior](https://www.python.org)  
* [Esptool](https://docs.espressif.com/projects/esptool/en/latest/esp32/)

---

## Instalación de Esptool

Abre tu terminal y ejecuta los siguientes comandos:

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install esptool
```

---

## Cómo utilizarlo

1. **Conectar el ESP32**
   Conecta la placa a la computadora utilizando un cable USB de datos.

2. **Ejecutar el Flasher**
   Haz doble clic en el archivo `Tool_Kit.bat` para abrir la herramienta.

3. **Seleccionar el puerto COM**
   El programa detectará los puertos disponibles; selecciona el puerto que corresponde a tu ESP32.

4. **Seleccionar el firmware**
   Escoge la herramienta o firmware que deseas flashear en el dispositivo.

5. **Iniciar el proceso**
   Presiona el botón **FLASH** para comenzar con la instalación del firmware.

   ---



