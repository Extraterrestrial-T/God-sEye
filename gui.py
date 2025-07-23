import tkinter as tk
from tkinter import filedialog, messagebox
from config.settings import default_params
from motion.camera import VideoSource
from motion.detector import MotionDetector
from ai.gemma_runner import GemmaRunner

def run(src):
    params = default_params()
    detector = MotionDetector(**params)
    gemma = GemmaRunner()
    for frame in VideoSource(src):
        res = detector.check(frame)
        if res.detected:
            desc = gemma.describe_images(res.paths)
            messagebox.showinfo('Motion Alert', desc)
    VideoSource(src).cleanup()

root = tk.Tk(); root.title('God\'sEye Launcher')
entry = tk.Entry(root, width=50); entry.pack(padx=10,pady=5)
tk.Button(root, text='Browse', command=lambda: entry.insert(0, filedialog.askopenfilename())).pack()
tk.Button(root, text='Start', command=lambda: run(entry.get())).pack(pady=10)
root.mainloop()