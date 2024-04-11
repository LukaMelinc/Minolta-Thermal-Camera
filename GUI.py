import tkinter as tk
from tkinter import ttk
import datetime

# Function to display inputs
def display_inputs():
    print("Port:", port_var.get())
    print("Baudrate:", baudrate_var.get())
    print("Temperature:", temperature_var.get())
    print("Standard Deviation:", stddev_var.get())
    print("Emissivity:", emissivity_var.get())
    print("Temperature Difference:", temp_diff_var.get())
    # Here, you would add your code to handle these inputs, such as serial communication or calculations.

# Creating main window
root = tk.Tk()
root.title("Serial Communication GUI")

# Variables
port_var = tk.StringVar()
baudrate_var = tk.IntVar()
temperature_var = tk.DoubleVar()
stddev_var = tk.DoubleVar()
emissivity_var = tk.DoubleVar()
temp_diff_var = tk.DoubleVar()

# Layout
tk.Label(root, text="Port:").grid(row=0, column=0, sticky="w")
tk.Entry(root, textvariable=port_var).grid(row=0, column=1)

tk.Label(root, text="Baudrate:").grid(row=1, column=0, sticky="w")
tk.Entry(root, textvariable=baudrate_var).grid(row=1, column=1)

tk.Label(root, text="Temperature (°C):").grid(row=2, column=0, sticky="w")
tk.Entry(root, textvariable=temperature_var).grid(row=2, column=1)

tk.Label(root, text="Standard Deviation:").grid(row=3, column=0, sticky="w")
tk.Entry(root, textvariable=stddev_var).grid(row=3, column=1)

tk.Label(root, text="Emissivity:").grid(row=4, column=0, sticky="w")
tk.Entry(root, textvariable=emissivity_var).grid(row=4, column=1)

tk.Label(root, text="Temperature Difference (°C):").grid(row=5, column=0, sticky="w")
tk.Entry(root, textvariable=temp_diff_var).grid(row=5, column=1)

# Time and Date
time_date_label = ttk.Label(root, text=f"Time and Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
time_date_label.grid(row=6, column=0, columnspan=2)

# Button to display inputs
tk.Button(root, text="Submit", command=display_inputs).grid(row=7, column=0, columnspan=2)

root.mainloop()
