import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


FIRMWARES = {
    "Hydra": {
        "folder": "Hydra",
        "files": [
            ("0x1000", "bootloader.bin"),
            ("0x8000", "partition-table.bin"),
            ("0x10000", "projecthydra-32.bin"),
            ("0x190000", "storage.bin"),
        ],
        "freq": "80m",
    },

    "Firmware 2": {
        "folder": "Firmware2",
        "files": [
            ("0x1000", "bootloader.bin"),
            ("0x8000", "partition-table.bin"),
            ("0x10000", "firmware.bin"),
        ],
        "freq": "40m",
    }
}


def detectar_puertos():
    try:
        import serial.tools.list_ports

        puertos = [
            p.device
            for p in serial.tools.list_ports.comports()
        ]

        combo_port["values"] = puertos

        if puertos:
            combo_port.current(0)
            estado.config(
                text=f"✓ {len(puertos)} puerto(s) detectado(s)",
                fg="green"
            )
        else:
            combo_port.set("")
            estado.config(
                text="No se encontraron puertos COM",
                fg="red"
            )

    except ImportError:
        estado.config(
            text="Instala pyserial",
            fg="red"
        )


def firmware_seleccionado():
    return FIRMWARES[combo_firmware.get()]


def obtener_archivos():
    firmware = firmware_seleccionado()

    archivos = []

    for direccion, nombre in firmware["files"]:
        ruta = os.path.join(
            BASE_DIR,
            firmware["folder"],
            nombre
        )

        archivos.append(
            (direccion, ruta)
        )

    return archivos


def comprobar_archivos():
    archivos = obtener_archivos()

    consola.delete(
        "1.0",
        tk.END
    )

    correcto = True

    consola.insert(
        tk.END,
        f"Firmware: {combo_firmware.get()}\n\n"
    )

    for direccion, archivo in archivos:

        if os.path.isfile(archivo):

            tamaño = os.path.getsize(archivo)

            consola.insert(
                tk.END,
                f"✓ {os.path.basename(archivo)} "
                f"({tamaño:,} bytes)\n"
            )

        else:

            consola.insert(
                tk.END,
                f"✗ FALTA: {archivo}\n"
            )

            correcto = False

    if correcto:

        estado.config(
            text="✓ Todos los archivos están presentes",
            fg="green"
        )

    else:

        estado.config(
            text="❌ Faltan archivos",
            fg="red"
        )

    return correcto


def cambiar_firmware(event=None):
    comprobar_archivos()


def iniciar_flash():
    threading.Thread(
        target=flashear,
        daemon=True
    ).start()


def flashear():

    puerto = combo_port.get()
    nombre_firmware = combo_firmware.get()

    if not puerto:

        root.after(
            0,
            lambda: estado.config(
                text="Selecciona un puerto COM",
                fg="red"
            )
        )

        return

    firmware = FIRMWARES[nombre_firmware]

    archivos = obtener_archivos()

    faltantes = [
        archivo
        for _, archivo in archivos
        if not os.path.isfile(archivo)
    ]

    if faltantes:

        root.after(
            0,
            lambda: estado.config(
                text="❌ Faltan archivos",
                fg="red"
            )
        )

        return

    comando = [
        sys.executable,
        "-m",
        "esptool",

        "--chip",
        "esp32",

        "-p",
        puerto,

        "-b",
        "115200",

        "--before",
        "default-reset",

        "--after",
        "hard-reset",

        "write-flash",

        "--flash-mode",
        "dio",

        "--flash-size",
        "detect",

        "--flash-freq",
        firmware["freq"]
    ]

    for direccion, archivo in archivos:
        comando.extend([
            direccion,
            archivo
        ])

    root.after(
        0,
        lambda: boton_flash.config(
            state="disabled"
        )
    )

    root.after(
        0,
        lambda: combo_firmware.config(
            state="disabled"
        )
    )

    root.after(
        0,
        lambda: combo_port.config(
            state="disabled"
        )
    )

    root.after(
        0,
        lambda: consola.delete(
            "1.0",
            tk.END
        )
    )

    root.after(
        0,
        lambda: estado.config(
            text=f"⚡ Flasheando {nombre_firmware}...",
            fg="blue"
        )
    )

    try:

        proceso = subprocess.Popen(
            comando,

            stdout=subprocess.PIPE,

            stderr=subprocess.STDOUT,

            text=True,

            encoding="utf-8",

            errors="replace",

            bufsize=1,

            cwd=BASE_DIR
        )

        for linea in proceso.stdout:

            root.after(
                0,
                lambda x=linea: consola.insert(
                    tk.END,
                    x
                )
            )

            root.after(
                0,
                lambda: consola.see(
                    tk.END
                )
            )

        codigo = proceso.wait()

        if codigo == 0:

            root.after(
                0,
                lambda: estado.config(
                    text=f"✅ {nombre_firmware} flasheado correctamente",
                    fg="green"
                )
            )

        else:

            root.after(
                0,
                lambda: estado.config(
                    text="❌ El flasheo falló",
                    fg="red"
                )
            )

    except Exception as error:

        root.after(
            0,
            lambda: consola.insert(
                tk.END,
                f"\nERROR: {error}\n"
            )
        )

        root.after(
            0,
            lambda: estado.config(
                text="❌ Error ejecutando esptool",
                fg="red"
            )
        )

    finally:

        root.after(
            0,
            lambda: boton_flash.config(
                state="normal"
            )
        )

        root.after(
            0,
            lambda: combo_firmware.config(
                state="readonly"
            )
        )

        root.after(
            0,
            lambda: combo_port.config(
                state="readonly"
            )
        )


# ============================================================
# INTERFAZ
# ============================================================

root = tk.Tk()

root.title(
    "ESP32 Toolkit"
)

root.geometry(
    "680x560"
)

root.resizable(
    False,
    False
)


titulo = tk.Label(
    root,
    text="⚡ ESP32 TOOLKIT",
    font=("Arial", 21, "bold")
)

titulo.pack(
    pady=(18, 4)
)


subtitulo = tk.Label(
    root,
    text="Firmware Flasher",
    font=("Arial", 10)
)

subtitulo.pack(
    pady=(0, 15)
)


# Firmware

tk.Label(
    root,
    text="Firmware:"
).pack()


combo_firmware = ttk.Combobox(
    root,
    values=list(FIRMWARES.keys()),
    state="readonly",
    width=30
)

combo_firmware.current(0)

combo_firmware.pack(
    pady=6
)

combo_firmware.bind(
    "<<ComboboxSelected>>",
    cambiar_firmware
)


# Puerto

tk.Label(
    root,
    text="Puerto COM:"
).pack(
    pady=(10, 0)
)


combo_port = ttk.Combobox(
    root,
    state="readonly",
    width=30
)

combo_port.pack(
    pady=6
)


# Actualizar

tk.Button(
    root,
    text="🔄 Actualizar puertos",
    command=detectar_puertos,
    width=25
).pack(
    pady=5
)


# Comprobar

tk.Button(
    root,
    text="📁 Comprobar archivos",
    command=comprobar_archivos,
    width=25
).pack(
    pady=5
)


# Flash

boton_flash = tk.Button(
    root,
    text="⚡ FLASH",
    command=iniciar_flash,
    width=30,
    height=2,
    font=("Arial", 12, "bold")
)

boton_flash.pack(
    pady=15
)


# Estado

estado = tk.Label(
    root,
    text="Listo",
    fg="blue"
)

estado.pack(
    pady=5
)


# Consola

tk.Label(
    root,
    text="Salida de esptool:"
).pack()


consola = tk.Text(
    root,
    width=82,
    height=15,
    font=("Consolas", 9)
)

consola.pack(
    padx=10,
    pady=8
)


# Inicio

detectar_puertos()
comprobar_archivos()


root.mainloop()