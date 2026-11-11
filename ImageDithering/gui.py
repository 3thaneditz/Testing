import customtkinter as ctk
from tkinter import filedialog
import os
from lowerVideoFPS import convertVideoFully
import shutil

videoPath = None

def selectVideo():
    global videoPath
    videoPath = filedialog.askopenfilename(title="Select a video", filetypes=[('MP4 Files', '*.mp4')])
    if videoPath:
        baseName = os.path.basename(videoPath)
        videoLabel.configure(text=baseName)

def convertVideo():
    print("Starting conversion...")
    if videoPath:
        convertVideoFully(videoPath, updateProgress)
    
def updateProgress(value, message):
    root.after(0, lambda: progressBar.set(value))
    root.after(0, lambda: statusLabel.configure(text=message))

def downloadVideo():
    if not os.path.exists("video.bin"):
        return

    savePath = filedialog.asksaveasfilename(title="Save converted video",defaultextension=".bin", filetypes=[("Binary files", "*.bin")])

    if savePath:
        shutil.copy2("video.bin", savePath)
        statusLabel.configure(text="File saved!")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()

root.title("OLED Video Converter")
root.geometry("800x500")

text = ctk.CTkLabel(root, text="MP4 To SSD1306 Display Buffer", font=ctk.CTkFont(size=28, weight="bold"))
text.grid(pady=10)

button = ctk.CTkButton(root, text="Select Video To Convert", command=selectVideo)
button.grid(pady=10)

videoLabel = ctk.CTkLabel(root, text="No video selected", font=ctk.CTkFont(size=16))
videoLabel.grid()

convertButton = ctk.CTkButton(root, text="Convert Video", command=convertVideo)
convertButton.grid(pady=10)

progressBar = ctk.CTkProgressBar(root)
progressBar.grid(pady = 5)

progressBar.set(0)

statusLabel = ctk.CTkLabel(root, text="...", font=ctk.CTkFont(size=16))
statusLabel.grid()

downloadButton = ctk.CTkButton(root, text="Download .Bin", command=downloadVideo)
downloadButton.grid(pady=5)

root.grid_columnconfigure(0, weight=1)
root.mainloop()