import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import platform

processes = {}
status_labels = {}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

scripts = {
    "snake": resource_path(os.path.join("LaunchPadDemos", "snake.py")),
    "toonblast": resource_path(os.path.join("LaunchPadDemos", "toonblast.py")),
    "tetris": resource_path(os.path.join("LaunchPadDemos", "tetris.py")),
    "flappybird": resource_path(os.path.join("LaunchPadDemos", "flappybird.py"))
}

def start_script(name):
    if name in processes and processes[name].poll() is None:
        messagebox.showinfo("Info", f"{name} is already running!")
        return

    try:
        cmd = ["python", scripts[name]]
        if platform.system() == "Windows":
            proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            proc = subprocess.Popen(cmd)
        processes[name] = proc
        status_labels[name].config(text="Running", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Error starting {name}:\n{e}")

from pygame import time
import launchpad_py

def stop_script(name):
    if name in processes and processes[name].poll() is None:
        processes[name].terminate()
        processes[name].wait() 
        status_labels[name].config(text="Stopped", fg="red")
    else:
        messagebox.showinfo("Info", f"{name} is not running!")

    #Launchpad S Setup
    lp = launchpad_py.Launchpad()
    lp.Open(0)
    lp.Reset()

    lp.Close()

def create_gui():
    root = tk.Tk()
    root.title("MIDI Game Launcher")
    root.geometry("400x250")
    
    for name in scripts.keys():
        frame = tk.Frame(root)
        frame.pack(pady=5)
        
        name_label = tk.Label(frame, text=name, width=15, anchor="w")
        name_label.pack(side="left")
        
        status_labels[name] = tk.Label(frame, text="Stopped", fg="red", width=10)
        status_labels[name].pack(side="left")
        
        start_btn = tk.Button(frame, text="Start", command=lambda n=name: start_script(n))
        start_btn.pack(side="left", padx=5)
        
        stop_btn = tk.Button(frame, text="Stop", command=lambda n=name: stop_script(n))
        stop_btn.pack(side="left")
    
    root.mainloop()

if __name__ == '__main__':
    create_gui()

#pyinstaller --onefile --noconsole --add-data "LaunchPadDemos;LaunchPadDemos" GameLauncher.py