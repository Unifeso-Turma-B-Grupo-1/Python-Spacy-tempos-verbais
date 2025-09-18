from tkinter import *
from tkinter import messagebox
import os, psutil, subprocess

class Window:
    def __init__(self, title: str):
        self.proc = None
        self.main(title)

    def main(self, title: str) :
        win = self.create_window(title)
        self.add_default_stuff(win)
        win.mainloop()

    def open_cmd(self):
        if self.proc is None or self.proc.poll() is not None:
            self.proc = subprocess.Popen(
                ["cmd", "/K", "python", "main.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            messagebox.showerror(message="The program is already open", title="Error.")

    def add_default_stuff(self, win):
        # text
        label = Label(win, text="Hello! Welcome to our text analysis program.")
        label.pack()

        # button
        cmd_button = Button(win, text="Start Program", command=self.open_cmd)
        cmd_button.pack()

    def create_window(self, name: str):
        win = Tk()

        #title 
        win.title(name)

        # dimensions
        win_width = 500
        win_height = 200

        # monitor dimensions
        mon_width = win.winfo_screenwidth()
        mon_height = win.winfo_screenheight()

        # x and y positions
        x_pos = (mon_width // 2) - (win_width // 2)
        y_pos = (mon_height // 2) - (win_height // 2)

        win.geometry(f"{win_width}x{win_height}+{x_pos}+{y_pos}")
        win.resizable(False, False)
        win.iconbitmap("icons/pencil.ico")

        return win
    
Window("Analyzer")