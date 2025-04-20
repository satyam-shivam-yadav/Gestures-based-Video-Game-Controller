import traceback
import os
from PIL import Image, ImageTk
import cv2
import webview
import pygame
import tkinter as tk
from tkinter import PhotoImage

pygame.mixer.init()

class VideoBackground:
    def __init__(self, root, video_path):
        self.root = root
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise FileNotFoundError(f"Could not open video: {video_path}")
        
        self.canvas = tk.Canvas(root, width=900, height=720)
        self.canvas.pack()
        self.update_background()

    def update_background(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (900, 720))
            self.img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.root.after(30, self.update_background)

    def release(self):
        self.cap.release()

class HoverButton(tk.Button):
    def __init__(self, master, video_path=None, hover_sound=None, **kwargs):
        super().__init__(master, **kwargs)
        self.video_path = video_path
        self.hover_sound = hover_sound
        self.video_capture = None
        self.is_hovering = False
        self.original_image = self.cget("image")

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_enter(self, event):
        self.is_hovering = True
        if self.video_path:
            self.video_capture = cv2.VideoCapture(self.video_path)
            self.play_video()
        if self.hover_sound:
            pygame.mixer.music.load(self.hover_sound)
            pygame.mixer.music.play()

    def on_leave(self, event):
        self.is_hovering = False
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        if self.hover_sound:
            pygame.mixer.music.stop()
        self.reset_button()

    def on_click(self, event):
        if self.hover_sound:
            pygame.mixer.music.stop()
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        self.reset_button()

    def reset_button(self):
        self.config(image=self.original_image)

    def play_video(self):
        if self.is_hovering and self.video_capture:
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.winfo_width(), self.winfo_height()))
                img = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.config(image=img)
                self.image = img
            else:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.after(30, self.play_video)

def load_image(path, size=None):
    try:
        img = Image.open(path)
        if size:
            img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

def open_website_in_tkinter(url):
    webview.create_window("Game", url)
    webview.start()

def open_manual():
    manual_text = """This is your manual. 
    1. Click the web buttons to open respective pages.
    2. Click the app button to open the application.
    3. Enjoy!"""
    manual_window = tk.Toplevel()
    manual_window.title("Manual")
    manual_label = tk.Label(manual_window, text=manual_text, wraplength=400, justify="left")
    manual_label.pack(padx=10, pady=10)

def open_asphalt8():
    os.system("start shell:AppsFolder\\GAMELOFTSA.Asphalt8Airborne_0pp20fcewvvtj!App")

def main():
    try:
        root = tk.Tk()
        root.title("Game Center")
        root.geometry("900x720+100+100")

        video_path = r"C:\Users\asus\Downloads\Untitled video - Made with Clipchamp (2).mp4"
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file missing: {video_path}")
        
        video_bg = VideoBackground(root, video_path)
        canvas = video_bg.canvas

        icon1 = load_image(r"C:\Hand gestures based video game controller\button images\subway icon.webp", (250, 250))
        icon2 = load_image(r"button images\stickman icon.jpg", (120, 120))
        icon3 = load_image(r"button images\redball icon.png", (240, 240))
        icon4 = load_image(r"button images\dreadhead-parkour icon.webp", (120, 120))
        icon5 = load_image(r"button images\stupid-zombies icon.png", (200, 200))
        icon6 = load_image(r"button images\bubble-shooter icon.webp", (120, 120))
        icon7 = load_image(r"button images\level-devil icon.webp", (100, 100))
        icon8 = load_image(r"button images\water-color-sort icon.jpg", (120, 120))
        icon_app = load_image(r"C:\Hand gestures based video game controller\button images\asphalt 8 logo.jpg", (245, 245))
        icon_manual = load_image(r"button images\manualicon.png", (40, 40))

        btn1 = HoverButton(
            canvas,
            image=icon1,
            video_path=r"button videos\Subwayvideo.mp4",
            hover_sound=r"C:\Users\asus\Downloads\Subway Surfers Soundtrack — Main Theme (www.lightaudio.ru).mp3",
            command=lambda: open_website_in_tkinter("https://poki.com/en/g/subway-surfers")
        )
        canvas.create_window(50, 50, anchor="nw", window=btn1, width=250, height=250)

        btn2 = HoverButton(
            canvas,
            image=icon2,
            video_path=r"button videos\stickman video.mp4",
            hover_sound=r"C:\Users\asus\Downloads\01. Stick Fight.mp3",
            command=lambda: open_website_in_tkinter("https://poki.com/en/g/stickman-hook")
        )
        canvas.create_window(315, 50, anchor="nw", window=btn2, width=120, height=120)

        btn3 = HoverButton(
            canvas,
            image=icon3,
            video_path=r"button videos\redball video.mp4",
            hover_sound=r"Audios folder\red ball audio.mp3",
            command=lambda: open_website_in_tkinter("https://poki.com/en/g/red-ball-4")
        )
        canvas.create_window(450, 50, anchor="nw", window=btn3, width=240, height=240)

        btn4 = HoverButton(
            canvas,
            image=icon4,
            video_path=r"button videos\dreadhead parkour video.mp4",
            hover_sound=r"C:\Users\asus\Downloads\Dreadhead Parkour Music [TubeRipper.com].mp3",
            command=lambda: open_website_in_tkinter("https://poki.com/en/g/dreadhead-parkour")
        )
        canvas.create_window(315, 180, anchor="nw", window=btn4, width=120, height=120)

        btn5 = HoverButton(
            canvas,
            image=icon5,
            video_path=r"button videos\stupid zombies video.mp4",
            hover_sound=r"C:\Users\asus\Downloads\Stupid zombies theme.mp3",
            command=lambda: open_website_in_tkinter("https://poki.com/en/g/stupid-zombies")
        )
        canvas.create_window(310, 310, anchor="nw", window=btn5, width=200, height=200)

        btn6 = HoverButton(
            canvas,
            image=icon6,
            video_path=r"button videos\bubble shooter video.mp4",
            hover_sound=r"C:\Users\asus\Downloads\bubble audio.mp3",
            command=lambda: open_website_in_tkinter("https://poki.com/en/g/bubble-shooter-lak")
        )
        canvas.create_window(180, 310, anchor="nw", window=btn6, width=120, height=120)

        btn7 = HoverButton(
            canvas,
            image=icon7,
            video_path=r"button videos\level devil video.mp4",
            hover_sound=r"C:\Users\asus\Downloads\level devil.mp3",
            command=lambda: open_website_in_tkinter("https://poki.com/en/g/level-devil")
        )
        canvas.create_window(520, 310, anchor="nw", window=btn7, width=100, height=100)

        btn8 = HoverButton(
            canvas,
            image=icon8,
            video_path=r"button videos\water sort video.mp4",
            hover_sound=r"Audios folder\red ball audio.mp3",
            command=lambda: open_website_in_tkinter("https://poki.com/en/g/water-color-sort")
        )
        canvas.create_window(50, 310, anchor="nw", window=btn8, width=120, height=120)

        btn_app = HoverButton(
            canvas,
            image=icon_app,
            video_path=r"button videos\\asphalt video - Made with Clipchamp.mp4",
            hover_sound=r"C:\Users\asus\Downloads\asphalt audio.mp3",
            command=open_asphalt8
        )
        canvas.create_window(50, 440, anchor="nw", window=btn_app, width=245, height=245)

        btn_manual = HoverButton(
            canvas,
            image=icon_manual,
            video_path=r"Background video\marvel-spiderman-miles-morales.1920x1080.mp4",
            hover_sound=r"",
            command=open_manual
        )
        canvas.create_window(850, 670, anchor="nw", window=btn_manual, width=40, height=40)

        def on_close():
            video_bg.release()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_close)
        root.mainloop()

    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
