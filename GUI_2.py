import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
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
                # Draw a vertical line at x=380 from top to bottom
        canvas = tk.Canvas(root)
        canvas.place(x=0, y=0, width=width, height=height)

        # Draw a vertical line at x=380 from top to bottom
        canvas.create_line(380, 0, 380, height, fill="black")

        # Draw horizontal lines
        canvas.create_line(380, 35, width, 35, fill="black")  # Horizontal line at y=35 from x=380 to the right edge
        canvas.create_line(380, 200, width, 200, fill="black") # Horizontal line at y=200 from x=380 to the right edge
        canvas.create_line(0, 390, width, 390, fill="black")   # Horizontal line at y=390 from left to right edge


        GButton_101=tk.Button(root)
        GButton_101["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_101["font"] = ft
        GButton_101["fg"] = "#000000"
        GButton_101["justify"] = "center"
        GButton_101["text"] = "Connect"
        GButton_101.place(x=470,y=160,width=70,height=25)
        GButton_101["command"] = self.GButton_101_command

        GLabel_520=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_520["font"] = ft
        GLabel_520["fg"] = "#333333"
        GLabel_520["justify"] = "center"
        GLabel_520["text"] = "Komunikacija"
        GLabel_520.place(x=470,y=20,width=70,height=25)

        GLabel_689=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_689["font"] = ft
        GLabel_689["fg"] = "#333333"
        GLabel_689["justify"] = "center"
        GLabel_689["text"] = ""
        GLabel_689.place(x=370,y=10,width=70,height=25)

        """GLabel_249=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_249["font"] = ft
        GLabel_249["fg"] = "#333333"
        GLabel_249["justify"] = "center"
        GLabel_249["text"] = "______________________________________________________________________________________________________________"
        GLabel_249.place(x=260,y=380,width=70,height=25)"""

        GLabel_445=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_445["font"] = ft
        GLabel_445["fg"] = "#333333"
        GLabel_445["justify"] = "center"
        GLabel_445["text"] = "Kamera 2"
        GLabel_445.place(x=470,y=50,width=70,height=25)

        GLabel_647=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_647["font"] = ft
        GLabel_647["fg"] = "#333333"
        GLabel_647["justify"] = "center"
        GLabel_647["text"] = "Port"
        GLabel_647.place(x=410,y=130,width=70,height=25)

        GLabel_848=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_848["font"] = ft
        GLabel_848["fg"] = "#333333"
        GLabel_848["justify"] = "center"
        GLabel_848["text"] = "Baudrate"
        GLabel_848.place(x=420,y=90,width=70,height=25)

        self.baudrate_var = tk.StringVar()
        GCombobox_baudrate = ttk.Combobox(root, textvariable=self.baudrate_var, state='readonly')
        GCombobox_baudrate['values'] = ("9600", "4800")
        GCombobox_baudrate.current(0)  # set selection
        GCombobox_baudrate.place(x=500, y=260, width=80, height=25)

        GLabel_240=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_240["font"] = ft
        GLabel_240["fg"] = "#333333"
        GLabel_240["justify"] = "center"
        GLabel_240["text"] = "Kalibrator"
        GLabel_240.place(x=470,y=220,width=70,height=25)

        GLabel_558=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_558["font"] = ft
        GLabel_558["fg"] = "#333333"
        GLabel_558["justify"] = "center"
        GLabel_558["text"] = "Baudrate"
        GLabel_558.place(x=410,y=260,width=70,height=25)

        GLabel_647=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_647["font"] = ft
        GLabel_647["fg"] = "#333333"
        GLabel_647["justify"] = "center"
        GLabel_647["text"] = "Port"
        GLabel_647.place(x=410,y=300,width=70,height=25)

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
        self.baudrate_var = tk.StringVar()
        GCombobox_baudrate = ttk.Combobox(root, textvariable=self.baudrate_var, state='readonly')
        GCombobox_baudrate['values'] = ("COM3", "COM4")
        GCombobox_baudrate.current(0)  # set selection
        GCombobox_baudrate.place(x=490,y=300,width=80,height=25)
        


        GMessage_843=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_843["font"] = ft
        GMessage_843["fg"] = "#333333"
        GMessage_843["justify"] = "center"
        GMessage_843["text"] = "Time"
        GMessage_843.place(x=460,y=410,width=80,height=25)

        GMessage_187=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_187["font"] = ft
        GMessage_187["fg"] = "#333333"
        GMessage_187["justify"] = "center"
        GMessage_187["text"] = "Date"
        GMessage_187.place(x=460,y=440,width=80,height=25)

        GMessage_395=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_395["font"] = ft
        GMessage_395["fg"] = "#333333"
        GMessage_395["justify"] = "center"
        GMessage_395["text"] = "Lokacija: Ljubljana"
        GMessage_395.place(x=480,y=460,width=80,height=25)

        GLabel_830=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_830["font"] = ft
        GLabel_830["fg"] = "#333333"
        GLabel_830["justify"] = "center"
        GLabel_830["text"] = "Kalibracija"
        GLabel_830.place(x=170,y=410,width=70,height=25)

        GLabel_253=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_253["font"] = ft
        GLabel_253["fg"] = "#333333"
        GLabel_253["justify"] = "center"
        GLabel_253["text"] = "Temperatura"
        GLabel_253.place(x=90,y=450,width=70,height=25)

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
