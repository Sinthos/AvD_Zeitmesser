import glob
import sys
import tkinter as tk
from tkinter import ttk

import serial.tools.list_ports


def get_serial_ports():
    """ Listet alle verfügbaren seriellen Ports auf. """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    return result

def on_port_selected():
    selected_port = port_var.get()
    with open("selected_port.txt", "w") as file:
        file.write(selected_port)
    root.destroy()

root = tk.Tk()
root.title("Port Selector")
port_var = tk.StringVar()
available_ports = get_serial_ports()
port_dropdown = ttk.Combobox(root, textvariable=port_var, values=available_ports)
if available_ports:
    port_var.set(available_ports[0])  # Standardmäßig ersten Port wählen

port_dropdown.grid(row=0, column=0, padx=10, pady=10)
select_button = tk.Button(root, text="Select Port and Save", command=on_port_selected)
select_button.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()