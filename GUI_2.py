import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import tkinter.font as tkFont
import datetime

class App:
    def __init__(self, root):

        # (0,0) točka sistema je zgoraj levo

        #setting title
        root.title("Main")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

                        # Create Canvas widget
                # Draw a vertical line at x=380 from top to bottogitm
        canvas = tk.Canvas(root)
        canvas.place(x=0, y=0, width=width, height=height)

        # Draw a vertical line at x=380 from top to bottom
        canvas.create_line(380, 0, 380, height, fill="black")

        # Draw horizontal lines
        canvas.create_line(380, 35, width, 35, fill="black")  # Horizontal line at y=35 from x=380 to the right edge
        canvas.create_line(380, 200, width, 200, fill="black") # Horizontal line at y=200 from x=380 to the right edge
        canvas.create_line(0, 390, width, 390, fill="black")   # Horizontal line at y=390 from left to right edge

        # Connect button for kamera 2
        GButton_101=tk.Button(root)
        GButton_101["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_101["font"] = ft
        GButton_101["fg"] = "#000000"
        GButton_101["justify"] = "center"
        GButton_101["text"] = "Conenct"
        GButton_101.place(x=470,y=160,width=70,height=25)
        GButton_101["command"] = self.GButton_101_command

        # label for komunikacija area
        GLabel_520=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_520["font"] = ft
        GLabel_520["fg"] = "#333333"
        GLabel_520["justify"] = "center"
        GLabel_520["text"] = "Komunikacija"
        GLabel_520.place(x=470,y=20,width=70,height=25)

        # label for title Kamera 2 area
        GLabel_445=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_445["font"] = ft
        GLabel_445["fg"] = "#333333"
        GLabel_445["justify"] = "center"
        GLabel_445["text"] = "Kamera 2"
        GLabel_445.place(x=470,y=50,width=70,height=25)

        # label for port dropdown menu in Kamera 2 area
        GLabel_647=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_647["font"] = ft
        GLabel_647["fg"] = "#333333"
        GLabel_647["justify"] = "center"
        GLabel_647["text"] = "Port"
        GLabel_647.place(x=420,y=130,width=70,height=25)

        # label for baudrate dropdown menu in kamera 2 area
        GLabel_848=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_848["font"] = ft
        GLabel_848["fg"] = "#333333"
        GLabel_848["justify"] = "center"
        GLabel_848["text"] = "Baudrate"
        GLabel_848.place(x=420,y=90,width=70,height=25)

        # dropwdon menue in kamera 2 area
        self.baudrate_var = tk.StringVar()
        GCombobox_baudrate = ttk.Combobox(root, textvariable=self.baudrate_var, state='readonly')
        GCombobox_baudrate['values'] = ("9600", "4800")
        GCombobox_baudrate.current(0)  # set selection
        GCombobox_baudrate.place(x=500, y=260, width=80, height=25)

        # label in kalibrator area - title
        GLabel_240=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_240["font"] = ft
        GLabel_240["fg"] = "#333333"
        GLabel_240["justify"] = "center"
        GLabel_240["text"] = "Kalibrator"
        GLabel_240.place(x=470,y=220,width=70,height=25)

        # kalibrator area - title label
        GLabel_558=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_558["font"] = ft
        GLabel_558["fg"] = "#333333"
        GLabel_558["justify"] = "center"
        GLabel_558["text"] = "Baudrate"
        GLabel_558.place(x=410,y=260,width=70,height=25)

        # Kalibrator area - label for port dropdown menu
        GLabel_647=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_647["font"] = ft
        GLabel_647["fg"] = "#333333"
        GLabel_647["justify"] = "center"
        GLabel_647["text"] = "Port"
        GLabel_647.place(x=410,y=300,width=70,height=25)

        # kalibrator - connect button
        GButton_113=tk.Button(root)
        GButton_113["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_113["font"] = ft
        GButton_113["fg"] = "#000000"
        GButton_113["justify"] = "center"
        GButton_113["text"] = "Connect"
        GButton_113.place(x=470,y=350,width=70,height=25)
        GButton_113["command"] = self.GButton_113_command

        """GListBox_956=tk.Listbox(root)
        GListBox_956["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_956["font"] = ft
        GListBox_956["fg"] = "#333333"
        GListBox_956["justify"] = "center"
        GListBox_956.place(x=500,y=90,width=80,height=25)
        GListBox_956["selectmode"] = "extended"""
        # kalibrator area - dropdown menu
        self.baudrate_var = tk.StringVar()
        GCombobox_baudrate = ttk.Combobox(root, textvariable=self.baudrate_var, state='readonly')
        GCombobox_baudrate['values'] = ("9600", "4800")
        GCombobox_baudrate.current(0)  # set selection
        GCombobox_baudrate.place(x=500,y=90,width=80,height=25)
        



        """GListBox_555=tk.Listbox(root)
        GListBox_555["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_555["font"] = ft
        GListBox_555["fg"] = "#333333"
        GListBox_555["justify"] = "center"
        GListBox_555.place(x=500,y=120,width=80,height=25)"""

        # kamera 2 area - dropdown menu for port
        self.baudrate_var = tk.StringVar()
        GCombobox_baudrate = ttk.Combobox(root, textvariable=self.baudrate_var, state='readonly')
        GCombobox_baudrate['values'] = ("COM3", "COM4")
        GCombobox_baudrate.current(0)  # set selection
        GCombobox_baudrate.place(x=500,y=120,width=80,height=25)

       

        """GListBox_559=tk.Listbox(root)
        GListBox_559["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_559["font"] = ft
        GListBox_559["fg"] = "#333333"
        GListBox_559["justify"] = "center"
        GListBox_559.place(x=490,y=300,width=80,height=25)"""

        # kalibrator area - dropdonw menu
        self.baudrate_var = tk.StringVar()
        GCombobox_baudrate = ttk.Combobox(root, textvariable=self.baudrate_var, state='readonly')
        GCombobox_baudrate['values'] = ("COM3", "COM4")
        GCombobox_baudrate.current(0)  # set selection
        GCombobox_baudrate.place(x=500,y=300,width=80,height=25)
        

        # time
        GLabel_843=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_843["font"] = ft
        GLabel_843["fg"] = "#333333"
        GLabel_843["anchor"] = "w" # Use anchor 'w' for left alignment within the provided space
        GLabel_843["text"] = "Time"
        GLabel_843.place(x=460,y=410,width=100,height=25)

        # date
        GLabel_187=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_187["font"] = ft
        GLabel_187["fg"] = "#333333"
        GLabel_187["anchor"] = "w" # Use anchor 'w' for left alignment within the provided space
        GLabel_187["text"] = "Date"
        GLabel_187.place(x=460,y=440,width=100,height=25)

        # location 
        GLabel_395=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_395["font"] = ft
        GLabel_395["fg"] = "#333333"
        GLabel_395["anchor"] = "w" # Use anchor 'w' for left alignment within the provided space
        GLabel_395["text"] = "Lokacija: Ljubljana"
        GLabel_395.place(x=460,y=470,width=140,height=25)  # Increased width to prevent wrapping

        # kalibracija area - area title
        GLabel_830=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_830["font"] = ft
        GLabel_830["fg"] = "#333333"
        GLabel_830["justify"] = "center"
        GLabel_830["text"] = "Kalibracija"
        GLabel_830.place(x=170,y=410,width=70,height=25)

        # kalibracija area  - 
        GLabel_253=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_253["font"] = ft
        GLabel_253["fg"] = "#333333"
        GLabel_253["justify"] = "center"
        GLabel_253["text"] = "Temperatura"
        GLabel_253.place(x=90,y=450,width=70,height=25)

        # FIX IT
        GLineEdit_385=tk.Entry(root)
        GLineEdit_385["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_385["font"] = ft
        GLineEdit_385["fg"] = "#333333"
        GLineEdit_385["justify"] = "center"
        GLineEdit_385["text"] = ""
        GLineEdit_385.place(x=210,y=450,width=70,height=25)

    def GButton_101_command(self):
        print("command")


    def GButton_113_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
