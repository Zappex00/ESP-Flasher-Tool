import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk


BASE_DIR = os.path.dirname(os.path.abspath(__file__))



# Firmwares organizados por grupo (listas separadas por grupo)
FIRMWARE_GROUPED = {
    "ESP32": {
        "Hydra": {
            "folder": "ESP32/Hydra",
            "files": [
                ("0x1000", "bootloader.bin"),
                ("0x8000", "partition-table.bin"),
                ("0x10000", "projecthydra-32.bin"),
                ("0x190000", "storage.bin"),
            ],
            "freq": "80m",
        },
        "GhostESP": {
            "folder": "ESP32/GhostESP",
            "files": [
                ("0x1000", "bootloader.bin"),
                ("0x8000", "partition.bin"),
                ("0x10000", "firmware.bin"),
            ],
            "freq": "40m",
        },
        "Wifi Penetration Tool": {
            "folder": "ESP32/Wifi Penetration Tool",
            "files": [
                ("0x1000", "bootloader.bin"),
                ("0x8000", "partition-table.bin"),
                ("0x10000", "firmware.bin"),
            ],
            "freq": "40m",
        },
        "ESP32 NAT Router": {
        "folder": "ESP32/ESP32-nat-router",
        "files": [
            ("0x1000", "bootloader.bin"),
            ("0x8000", "partition-table.bin"),
            ("0xe000", "ota_data_initial.bin"),
            ("0x10000", "esp32_nat_router.bin"),
        ],
        "freq": "40m",
    }
    },
    "ESP32 c5": {
        "GhostESP": {
            "folder": "ESP32-c5/GhostESP-c5",
            "files": [
                ("0x1000", "bootloader.bin"),
                ("0x8000", "partitions.bin"),
                ("0x10000", "firmware.bin"),
            ],
            "freq": "40m",
        },

        "ESP32 NAT Router": {
        "folder": "ESP32-c5/ESP32-c5-nat-router",
        "files": [
            ("0x1000", "bootloader.bin"),
            ("0x8000", "partition-table.bin"),
            ("0xe000", "ota_data_initial.bin"),
            ("0x10000", "esp32_nat_router.bin"),
        ],
        "freq": "40m",    

        }


    }
}


def detect_ports():
    try:
        import serial.tools.list_ports
        ports = [p.device for p in serial.tools.list_ports.comports()]

        combo_port["values"] = ports

        if ports:
            combo_port.current(0)
            status.config(
                text=f"✓ {len(ports)} port(s) detected",
                fg="green"
            )
        else:
            combo_port.set("")
            status.config(
                text="No COM ports found",
                fg="red"
            )

    except ImportError:
        status.config(
            text="Install pyserial",
            fg="red"
        )


def selected_firmware():
    group = combo_group.get() if 'combo_group' in globals() else list(FIRMWARE_GROUPED.keys())[0]
    return FIRMWARE_GROUPED.get(group, {}).get(combo_firmware.get(), {})


def get_files():
    firmware = selected_firmware()

    files = []

    for addr, name in firmware["files"]:
        path = os.path.join(BASE_DIR, firmware["folder"], name)
        files.append((addr, path))

    return files


def check_files():
    files = get_files()

    console.delete("1.0", tk.END)

    ok = True

    console.insert(tk.END, f"Firmware: {combo_firmware.get()}\n\n")

    for addr, filepath in files:
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            console.insert(
                tk.END,
                f"✓ {os.path.basename(filepath)} ({size:,} bytes)\n"
            )
        else:
            console.insert(tk.END, f"✗ MISSING: {filepath}\n")
            ok = False

    if ok:
        status.config(text="✓ All files are present", fg="green")
    else:
        status.config(text="❌ Missing files", fg="red")

    return ok


def change_firmware(event=None):
    check_files()


def change_group(event=None):
    group = combo_group.get()
    values = list(FIRMWARE_GROUPED.get(group, {}).keys())
    combo_firmware["values"] = values
    if values:
        combo_firmware.current(0)
    change_firmware()


def start_flash():
    threading.Thread(target=flash, daemon=True).start()


def flash():
    port = combo_port.get()
    firmware_name = combo_firmware.get()

    if not port:
        root.after(0, lambda: status.config(text="Select a COM port", fg="red"))
        return

    firmware = selected_firmware()

    files = get_files()

    missing = [f for _, f in files if not os.path.isfile(f)]

    if missing:
        root.after(0, lambda: status.config(text="❌ Missing files", fg="red"))
        return

    cmd = [
        sys.executable,
        "-m",
        "esptool",
        "--chip",
        "esp32",
        "-p",
        port,
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
        firmware["freq"],
    ]

    for addr, fpath in files:
        cmd.extend([addr, fpath])

    root.after(0, lambda: flash_button.config(state="disabled"))
    root.after(0, lambda: combo_firmware.config(state="disabled"))
    root.after(0, lambda: combo_port.config(state="disabled"))
    root.after(0, lambda: console.delete("1.0", tk.END))
    root.after(0, lambda: status.config(text=f"⚡ Flashing {firmware_name}...", fg="blue"))

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            cwd=BASE_DIR,
        )

        for line in proc.stdout:
            root.after(0, lambda x=line: console.insert(tk.END, x))
            root.after(0, lambda: console.see(tk.END))

        code = proc.wait()

        if code == 0:
            root.after(0, lambda: status.config(text=f"✅ {firmware_name} flashed successfully", fg="green"))
        else:
            root.after(0, lambda: status.config(text="❌ Flash failed", fg="red"))

    except Exception as error:
        root.after(0, lambda: console.insert(tk.END, f"\nERROR: {error}\n"))
        root.after(0, lambda: status.config(text="❌ Error running esptool", fg="red"))

    finally:
        root.after(0, lambda: flash_button.config(state="normal"))
        root.after(0, lambda: combo_firmware.config(state="readonly"))
        root.after(0, lambda: combo_port.config(state="readonly"))


root = tk.Tk()

root.title("ESP32 Toolkit")
root.geometry("680x560")
root.resizable(False, False)

title_label = tk.Label(root, text="⚡ ESP32 TOOLKIT", font=("Arial", 21, "bold"))
title_label.pack(pady=(18, 4))

subtitle_label = tk.Label(root, text="Firmware Flasher", font=("Arial", 10))
subtitle_label.pack(pady=(0, 15))

tk.Label(root, text="Versiones:").pack()
combo_group = ttk.Combobox(root, values=list(FIRMWARE_GROUPED.keys()), state="readonly", width=30)
combo_group.current(0)
combo_group.pack(pady=6)
combo_group.bind("<<ComboboxSelected>>", change_group)

tk.Label(root, text="Firmware:").pack()
combo_firmware = ttk.Combobox(root, values=[], state="readonly", width=30)
combo_firmware.pack(pady=6)
combo_firmware.bind("<<ComboboxSelected>>", change_firmware)

tk.Label(root, text="COM Port:").pack(pady=(10, 0))
combo_port = ttk.Combobox(root, state="readonly", width=30)
combo_port.pack(pady=6)

tk.Button(root, text="🔄 Refresh ports", command=detect_ports, width=25).pack(pady=5)

flash_button = tk.Button(root, text="⚡ FLASH", command=start_flash, width=30, height=2, font=("Arial", 12, "bold"))
flash_button.pack(pady=15)

status = tk.Label(root, text="Ready", fg="blue")
status.pack(pady=5)

tk.Label(root, text="Terminal Output:").pack()
console = tk.Text(root, width=82, height=15, font=("Consolas", 9))
console.pack(padx=10, pady=8)

detect_ports()
change_group()
check_files()

root.mainloop()
