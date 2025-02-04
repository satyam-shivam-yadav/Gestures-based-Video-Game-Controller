import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import cv2
import subprocess
import webview
import pygame

# Compatibility for older Pillow versions
if hasattr(Image, "Resampling"):
    Resampling = Image.Resampling
else:
    Resampling = Image.ANTIALIAS



# Initialize pygame mixer
pygame.mixer.init()

class HoverButton(tk.Button):
    def __init__(self, master, video_path=None, hover_sound=None, **kwargs):
        super().__init__(master, **kwargs)
        self.video_path = video_path
        self.hover_sound = hover_sound
        self.video_capture = None
        self.is_hovering = False

        # Store the original image
        self.original_image = self.cget("image")

        # Bind hover events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)  # Bind click event

    def on_enter(self, event):
        """When the mouse enters the button, start playing the video and sound."""
        self.is_hovering = True
        if self.video_path:
            self.video_capture = cv2.VideoCapture(self.video_path)
            self.play_video()
        if self.hover_sound:
            pygame.mixer.music.load(self.hover_sound)  # Load the sound file
            pygame.mixer.music.play()  # Play the sound

    def on_leave(self, event):
        """When the mouse leaves the button, stop the video and reset the button."""
        self.is_hovering = False
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        if self.hover_sound:
            pygame.mixer.music.stop()  # Stop the sound
        self.reset_button()

    def on_click(self, event):
        """When the button is clicked, stop the sound and reset the button."""
        if self.hover_sound:
            pygame.mixer.music.stop()  # Stop the sound
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        self.reset_button()

    def reset_button(self):
        """Reset the button to its original image."""
        self.config(image=self.original_image)  # Reset to the original image

    def play_video(self):
        """Loop through the video frames while hovering."""
        if self.is_hovering and self.video_capture:
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.winfo_width(), self.winfo_height()))
                img = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.config(image=img)
                self.image = img  # Keep a reference to avoid garbage collection
            else:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the video
            self.after(30, self.play_video)  # Adjust the delay for smoother playback

# Functions to render websites in a Tkinter window
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

def open_application(app_path):
    subprocess.Popen([app_path])  # Replace app_path with the actual path to the application

# Initialize Tkinter window
root = tk.Tk()
root.title("Game Center")
root.geometry("900x720+100+100")

# Video background
video_path = r"C:\Users\asus\Downloads\pixel-city-wallpaperwaifu-com.mp4"  # Replace with your video file
cap = cv2.VideoCapture(video_path)

# Create canvas for the video background
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill=tk.BOTH, expand=True)

# Function to update the video background on canvas
def update_background():
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (1280, 720))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        canvas.create_image(0, 0, anchor="nw", image=img)
        canvas.image = img
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video
    canvas.after(10, update_background)  # Keep updating the video

# Function to load images compatible with Tkinter
def load_image(path, size=None):
    try:
        img = Image.open(path)  # Load the image
        if size:  # Resize if size is provided
            img = img.resize(size, Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)  # Convert to Tkinter-compatible format
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

# Load images for buttons
icon1 = load_image(r"C:\Users\asus\Downloads\subway icon.webp", size=(250, 250))  # Adjust size as needed
icon2 = load_image(r"C:\Users\asus\Downloads\stickman icon.jpg", size=(120, 120))
icon3 = load_image(r"C:\Users\asus\Downloads\redball icon.png", size=(240, 240))
icon4 = load_image(r"C:\Users\asus\Downloads\dreadhead-parkour icon.webp", size=(120, 120))
icon5 = load_image(r"C:\Users\asus\Downloads\stupid-zombies icon.png", size=(200, 200))
icon6 = load_image(r"C:\Users\asus\Downloads\bubble-shooter icon.webp", size=(120, 120))
icon7 = load_image(r"C:\Users\asus\Downloads\level-devil icon.webp", size=(100, 100))
icon8 = load_image(r"C:\Users\asus\Downloads\water-color-sort icon.jpg", size=(120, 120))
icon_app = load_image(r"C:\Users\asus\Downloads\asphalt 8 logo.jpg", size=(245, 245))  # Adjust path
icon_manual = load_image(r"C:\Users\asus\Downloads\manualicon.png", size=(40, 40))  # Adjust path

# Create buttons with hover video and sound
btn1 = HoverButton(
    root,
    image=icon1,
    video_path=r"C:\Users\asus\Downloads\Subwayvideo.mp4",  # Replace with your hover video
    hover_sound=r"C:\Users\asus\Downloads\Tokyo.mp3",  # Replace with your hover sound file
    command=lambda: open_website_in_tkinter("https://poki.com/en/g/subway-surfers")
)
btn2 = HoverButton(
    root,
    image=icon2,
    video_path=r"C:\Users\asus\Downloads\stickman video.mp4",
    hover_sound=r"C:\Users\asus\Downloads\stickman sound.mp3",
    command=lambda: open_website_in_tkinter("https://poki.com/en/g/stickman-hook")
)
btn3 = HoverButton(
    root,
    image=icon3,
    video_path=r"C:\Users\asus\Downloads\thumbnail.3x3.vp9 (1).mp4",
    hover_sound=r"C:\Users\asus\Downloads\01. Menu.mp3",
    command=lambda: open_website_in_tkinter("https://poki.com/en/g/red-ball-4")
)
btn4 = HoverButton(
    root,
    image=icon4,
    video_path=r"C:\Users\asus\Downloads\dreadhead parkour video.mp4",
    hover_sound=r"C:\Users\asus\Downloads\dreadhead autdio.mp3",
    command=lambda: open_website_in_tkinter("https://poki.com/en/g/dreadhead-parkour")
)
btn5 = HoverButton(
    root,
    image=icon5,
    video_path=r"C:\Users\asus\Downloads\stupid zombies video.mp4",
    hover_sound=r"C:\Users\asus\Downloads\stupidzombies autdio.mp3",
    command=lambda: open_website_in_tkinter("https://poki.com/en/g/stupid-zombies")
)
btn6 = HoverButton(
    root,
    image=icon6,
    video_path=r"C:\Users\asus\Downloads\bubble shooter video.mp4",
    hover_sound=r"C:\Users\asus\Downloads\Music Game - BUBBLE [TubeRipper.com].mp3",
    command=lambda: open_website_in_tkinter("https://poki.com/en/g/bubble-shooter-lak")
)
btn7 = HoverButton(
    root,
    image=icon7,
    video_path=r"C:\Users\asus\Downloads\level devil video.mp4",
    hover_sound=r"C:\Users\asus\Downloads\level devil.mp3",
    command=lambda: open_website_in_tkinter("https://poki.com/en/g/level-devil")
)
btn8 = HoverButton(
    root,
    image=icon8,
    video_path=r"C:\Users\asus\Downloads\water sort video.mp4",
    hover_sound=r"C:\Users\asus\Downloads\water color sort audio.mp3",
    command=lambda: open_website_in_tkinter("https://poki.com/en/g/water-color-sort")
)
btn_app = HoverButton(
    root,
    image=icon_app,
    video_path=r"C:\Users\asus\Downloads\asphalt video - Made with Clipchamp.mp4",
    hover_sound=r"C:\Users\asus\Downloads\asphalt video sound.mp3",
    command=lambda: open_application(r"C:\Program Files\WindowsApps\GAMELOFTSA.Asphalt8Airborne_8.1.104.0_x64__0pp20fcewvvtj\Asphalt8.exe")
)
btn_manual = HoverButton(
    root,
    image=icon_manual,
    video_path=r"C:\Users\asus\Downloads\lonely-homer-starry-night-sky-pixel-moewalls-com.mp4",
    hover_sound=r"C:\Users\asus\Downloads\Tokyo.mp3",
    command=open_manual
)

btn1.place(x=50, y=50, width=250, height=250)  # Set width and height explicitly
btn2.place(x=315, y=50, width=120, height=120)
btn3.place(x=450, y=50, width=240, height=240)
btn4.place(x=315, y=180, width=120, height=120)
btn5.place(x=310, y=310, width=200, height=200)
btn6.place(x=180, y=310, width=120, height=120)
btn7.place(x=520, y=310, width=100, height=100)
btn8.place(x=50, y=310, width=120, height=120)
btn_app.place(x=50, y=440, width=245, height=245)
btn_manual.place(x=850, y=670, width=40, height=40)

# Start the background video update
update_background()

# Run the Tkinter main loop
root.mainloop()