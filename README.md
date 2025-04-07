# Hand Gesture-Based Video Game Controller

<p align="center">
	A vision-powered input system that transforms your hand gestures into live game controls.
</p>

<p align="center">Built with the tools and technologies:</p>
<p align="center">
	<img src="https://img.shields.io/badge/OpenCV-5C3EE8.svg?style=default&logo=OpenCV&logoColor=white" alt="OpenCV">
	<img src="https://img.shields.io/badge/MediaPipe-FF6F00.svg?style=default&logo=MediaPipe&logoColor=white" alt="MediaPipe">
	<img src="https://img.shields.io/badge/PyAutoGUI-4B8BBE.svg?style=default&logo=Python&logoColor=white" alt="PyAutoGUI">
	<img src="https://img.shields.io/badge/Tkinter-FF69B4.svg?style=default&logo=Python&logoColor=white" alt="Tkinter">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=default&logo=Python&logoColor=white" alt="Python">
</p>

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Project Structure](#project-structure)
- [Project Roadmap](#project-roadmap)
- [Problems Encountered](#problems-encountered)
- [Future Plans](#future-plans)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

**Hand Gesture Controller** is an intuitive tool that utilizes your webcam and real-time hand tracking to convert gestures into key presses, allowing you to control games or applications using just your hand. This is done using **MediaPipe** for hand landmark detection and **PyAutoGUI** for input simulation.

Use-cases include:
- Playing lightweight games (e.g. Subway Surfer, Bubble Shooter and Asphalt 8 Airborne) without any keyboard/mouse.
- Accessibility enhancement for people with physical limitations.
- Fun and engaging way to interact with computers!

## Features

- 🖐️ **Real-Time Hand Detection** using MediaPipe
- 🎮 **Gesture Mappings to Game Controls** (e.g. move left, right, jump)
- 🎥 **Webcam Feed with Landmark Overlay**
- 🧠 **Custom Gesture Recognition** using angles, distances, or finger states
- ⌨️ **Simulates Keystrokes/Mouse Events** with PyAutoGUI
- ⚙️ **Easily Extendable for More Gestures & Controls**

## Getting Started

### Prerequisites

- Python 3.7 or above
- Webcam

### Installation

```bash
git clone https://github.com/Xeno725/Gestures-based-Video-Game-Controller.git
cd hand-gesture-game-controller
pip install -r requirements.txt
```

### Usage

To start the gesture controller:

```bash
python main.py
```

Ensure your webcam is connected. The script will display the video feed with hand landmarks and respond to predefined gestures.

## Project Structure

```
hand-gesture-game-controller/
│
├── main.py                 # Main application logic
├── gestures.py             # Gesture detection logic
├── controller.py           # Mapping gestures to keyboard/mouse actions
├── utils.py                # Utility functions
├── requirements.txt
└── README.md
```

## Project Roadmap

- [x] Hand landmark detection
- [x] Basic gesture recognition (fingers up/down)
- [x] Trigger key events using PyAutoGUI
- [ ] Create gesture configuration file for custom mapping
- [ ] Add UI interface to customize controls
- [ ] Optimize for FPS-sensitive games

## Problems Encountered

- **False Positives in Gesture Detection:**
  > Solved by averaging over frames and applying a confidence threshold.

- **Latency in Input Response:**
  > Optimized frame size and reduced processing steps.

- **Multi-Gesture Conflicts:**
  > Introduced state buffers and action cooldowns.

## Future Plans

- Add hand orientation-based controls (e.g. tilt to steer)
- Integrate voice commands alongside gestures
- Train a custom ML model to classify complex gestures
- Support multi-hand input (e.g. one hand for actions, one for movement)

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

<details>
<summary>Contributing Guidelines</summary>

1. Fork the Repository  
2. Clone the Project Locally  
3. Create a Feature Branch  
4. Commit Your Changes  
5. Push and Open a PR

</details>

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

## Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) for real-time hand tracking.
- [OpenCV](https://opencv.org/) for handling webcam and image processing.
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) for simulating keyboard/mouse input.
- Thanks to open-source communities and contributors that inspire interactive project development.

