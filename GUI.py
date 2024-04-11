import tkinter as tk
import tkinter.font as tkFont

class GUI:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_948=tk.Button(root)
        GButton_948["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_948["font"] = ft
        GButton_948["fg"] = "#000000"
        GButton_948["justify"] = "center"
        GButton_948["text"] = "Button"
        GButton_948.place(x=60,y=70,width=70,height=25)
        GButton_948["command"] = self.GButton_948_command

        GLabel_161=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_161["font"] = ft
        GLabel_161["fg"] = "#333333"
        GLabel_161["justify"] = "center"
        GLabel_161["text"] = "label"
        GLabel_161.place(x=60,y=30,width=70,height=25)

    def GButton_948_command(self):
        print("command")
