
# ESP-Flasher-Tool

> **Aviso de Uso Responsable:** Las herramientas de auditoría y pruebas Wi-Fi deben utilizarse únicamente en dispositivos y redes propias o cuando se tenga autorización explícita para realizar pruebas de seguridad.

## Requisitos

* [Python 3.14 o superior](https://www.python.org)  
* [Esptool](https://docs.espressif.com/projects/esptool/en/latest/esp32/<)


## Instalación de Esptool

Abre tu terminal y ejecuta los siguientes comandos:

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install esptool
```

## Cómo utilizarlo

1. **Conectar el ESP32**  
Conecta el ESP32 a la computadora mediante un cable USB de datos.

2. **Ejecutar el Flasher**  
Ejecuta el script de Python de la herramienta.  
El programa debería detectar los puertos COM disponibles.  
Selecciona el puerto COM correspondiente al ESP32.  

3. **Seleccionar el firmware**  
Selecciona la herramienta/firmware que deseas instalar, por ejemplo:  
Hydra
WiFi Penetration Tool

4. **Iniciar el flasheo**  
Presiona el botón:
FLASH



