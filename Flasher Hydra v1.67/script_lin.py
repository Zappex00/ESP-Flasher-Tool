import subprocess
import tkinter as tk

def flashear_esp32(port):

    if not port.strip():
        message_label.config(text="Error: Enter the port", fg="red")
        return False

    flash_command = [
        "esptool.py",
        "-p", f"{port}",
        "-b", "460800",
        "--before", "default_reset",
        "--after", "hard_reset",
        "--chip", "esp32",
        "write_flash",
        "--flash_mode", "dio",
        "--flash_size", "detect",
        "--flash_freq", "80m",
        "0x1000", "build/bootloader/bootloader.bin",
        "0x8000", "build/partition_table/partition-table.bin",
        "0x10000", "build/projecthydra-32.bin",
        "0x190000", "build/storage.bin"
    ]

    message_label.config(text=f"Flashing {port}...", fg="blue")

    flash_result = subprocess.run(flash_command, capture_output=True, text=True)

    if flash_result.returncode == 0:
        message_label.config(text="Flashing completed successfully", fg="green")
        return True
    
    else:
        message_label.config(text="Error: Flashing failed", fg="red")
        return False


def execute_flash_operation():
    puerto_actual = entry.get()
    flashear_esp32(puerto_actual)


root = tk.Tk()
root.title("Flasher Hydra Firmware")
root.geometry("340x190")
root.resizable(False, False)

label = tk.Label(root, text="Enter your USB port:")
label.pack(pady=(15, 5))

entry = tk.Entry(root)
entry.pack(pady=(0, 10))

button = tk.Button(root, text="Flashing the ESP32", command=execute_flash_operation)
button.pack(pady=(10, 10))

message_label = tk.Label(root, text="", fg="red", wraplength=280, justify="center")
message_label.pack(pady=(5, 0))

root.mainloop()
