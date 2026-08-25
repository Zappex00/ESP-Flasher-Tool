Herramienta para flashear diferentes firmwares en dispositivos ESP32 mediante una interfaz gráfica.

⚠️ Aviso: Las herramientas de pruebas Wi-Fi deben utilizarse únicamente en dispositivos y redes propias o cuando se tenga autorización expresa para realizar pruebas.

📋 Requisitos
Windows
Python 3.14 o superior
Un ESP32 compatible
Cable USB de datos
El firmware que se desea instalar
esptool
🐍 Instalar Python

Descarga Python desde:

https://www.python.org/downloads/

Durante la instalación, se recomienda activar la opción:

Add Python to PATH

📦 Instalar esptool

Después de instalar Python, abre CMD y ejecuta:

python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install esptool

Para comprobar que quedó instalado correctamente:

python -m esptool version

Si aparece la versión de esptool, ya está listo. ✅

🚀 Cómo utilizar el Flasher
1. Conectar el ESP32

Conecta el ESP32 a la computadora mediante un cable USB de datos.

2. Ejecutar el Flasher

Ejecuta el script de Python de la herramienta.

El programa debería detectar los puertos COM disponibles.

Selecciona el puerto COM correspondiente al ESP32.

3. Seleccionar el firmware

Selecciona la herramienta/firmware que deseas instalar, por ejemplo:

Hydra
WiFi Penetration Tool
4. Iniciar el flasheo

Presiona el botón:

FLASH

Si el ESP32 necesita entrar manualmente en modo de programación:

Mantén presionado el botón BOOT.
Inicia el proceso de flasheo.
Mantén BOOT durante unos segundos.
Suelta el botón cuando el proceso haya comenzado correctamente.

💡 Algunos modelos de ESP32 pueden entrar automáticamente en modo de programación, por lo que no siempre es necesario mantener presionado BOOT.

5. Esperar a que termine

No desconectes el ESP32 durante el proceso.

El proceso habrá terminado correctamente cuando aparezca un mensaje similar a:

Hard resetting via RTS pin...

Después puedes desconectar y volver a conectar el ESP32.

📡 Después del flasheo

Dependiendo del firmware instalado, el ESP32 puede iniciar un punto de acceso Wi-Fi para acceder a su interfaz web.

Por ejemplo, una instalación de Hydra puede crear una red denominada:

hydra

Y otra herramienta puede utilizar:

ManagementAP

Las credenciales y configuración exactas dependen de la versión del firmware que estés utilizando.

Una vez conectado a la red del dispositivo, algunas herramientas proporcionan una interfaz web accesible desde:

192.168.4.1

Puedes abrir esa dirección desde el navegador del teléfono o computadora.

⚠️ Uso responsable: las funciones de auditoría, captura de tráfico, desautenticación u otras pruebas de seguridad deben realizarse únicamente sobre redes y dispositivos donde tengas permiso para probar.

🛠️ Solución rápida de problemas
esptool no se reconoce

En lugar de ejecutar:

esptool

utiliza:

python -m esptool
El ESP32 no aparece

Prueba:

Otro cable USB.
Otro puerto USB.
Instalar el controlador USB correspondiente a tu placa.
Desconectar y volver a conectar el ESP32.
Mantener presionado BOOT mientras comienza el flasheo.
El flasheo se queda detenido

Comprueba que:

El puerto COM seleccionado sea el correcto.
Ningún otro programa esté utilizando el puerto.
El cable sea de datos, no solamente de carga.
El ESP32 esté en modo de programación.
✅ Resumen
1. Instalar Python
        ↓
2. Instalar esptool
        ↓
3. Conectar ESP32
        ↓
4. Ejecutar Flasher
        ↓
5. Seleccionar puerto COM
        ↓
6. Seleccionar firmware
        ↓
7. Presionar FLASH
        ↓
8. Usar BOOT si es necesario
        ↓
9. Esperar "Hard resetting via RTS pin..."
        ↓
10. ¡ESP32 flasheado! 🚀

Y listo: ESP32 preparado para ejecutar el firmware seleccionado. 🔥
