# 🖱️ Virtual Mouse Control System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)

**A touchless computer control system powered by hand gesture recognition**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#%EF%B8%8F-configuration) • [Contributing](#-contributing)

</div>

---

## 📋 Overview

Virtual Mouse Control System is a Python-based hand gesture recognition application that enables **touchless computer interaction** using computer vision and real-time hand tracking. Control your cursor, perform clicks, scroll pages, and adjust system volume through intuitive hand gestures detected via your webcam.

### Why This Project?

- **Accessibility**: Enables hands-free control for users with limited mobility
- **Hygiene**: Touchless interaction for shared or public computers
- **Innovation**: Demonstrates practical computer vision and gesture recognition
- **Performance**: Optimized for real-time operation (20-30 FPS) with minimal latency

---

## ✨ Features

### Core Functionality

| Gesture | Action | Hand |
|---------|--------|------|
| 👆 Point with index finger | Move cursor | Any |
| 🤏 Index + Thumb pinch | Left click | Any |
| 🤏 Middle + Thumb pinch | Right click | Any |
| 👍 Thumbs up | Scroll down/up | Left/Right |
| 🙌 Both hands apart/together | Volume control | Both (macOS) |

### Performance Optimizations

- **⚡ Threaded Video Capture**: Non-blocking frame acquisition
- **🎯 Frame Skipping**: Processes every 3rd frame for better FPS
- **🎨 EMA Smoothing**: Eliminates cursor jitter with exponential moving average
- **🚀 Optimized Calculations**: Uses squared distances (no expensive sqrt operations)
- **📦 Minimal Buffer**: Single-frame buffer reduces input lag
- **🤖 Lightweight ML**: MediaPipe's fastest hand detection model (complexity 0)

---

## 🎬 Demo

### Cursor Control & Clicking
![Cursor Demo](https://via.placeholder.com/600x300?text=Add+Your+Demo+GIF+Here)

### Scrolling & Volume Control
![Gesture Demo](https://via.placeholder.com/600x300?text=Add+Your+Gesture+Demo+Here)



---

## 🚀 Installation

### Prerequisites

- **Python**: 3.7 or higher
- **Webcam**: USB or built-in camera
- **OS**: macOS (full features), Windows/Linux (mouse & scroll only)

### Quick Start

1. **Clone the repository**
git clone https://github.com/naveen200401/virtual_mouse.git
cd virtual-mouse-control


2. **Install dependencies**
pip install -r requirements.txt


pip install opencv-python mediapipe pyautogui numpy


3. **Run the application**
python virtual_mouse.py


4. **Exit**: Press `q` to quit

---

## 📖 Usage

### Gesture Guide

#### 1️⃣ Cursor Movement
- **Gesture**: Extend your index finger and point
- **Tip**: Keep other fingers folded for best tracking
- **Range**: Move within 50px from frame edges for smooth control

#### 2️⃣ Left Click
- **Gesture**: Pinch index finger and thumb together
- **Tip**: Brief pinch to avoid accidental clicks
- **Cooldown**: 0.3s between clicks

#### 3️⃣ Right Click
- **Gesture**: Pinch middle finger and thumb together
- **Tip**: Keep index extended to differentiate from left click

#### 4️⃣ Scrolling
- **Gesture**: Thumbs-up (thumb extended, other fingers curled)
- **Left Hand**: Scroll down
- **Right Hand**: Scroll up
- **Continuous Mode**: Hold gesture for 1.5+ seconds

#### 5️⃣ Volume Control (macOS only)
- **Gesture**: Show both hands with wrists visible
- **Increase**: Move hands farther apart
- **Decrease**: Move hands closer together

---

## ⚙️ Configuration

Customize behavior by editing parameters in `virtual_mouse.py`:

### Performance Settings

FRAME_SKIP = 3 # Process every Nth frame (higher = faster)
SMOOTHENING_FACTOR = 0.65 # Cursor smoothness (0-1, higher = smoother)
ENABLE_MULTITHREADING = True # Async frame capture
SHOW_DEBUG_INFO = False # Display hand landmarks

### Camera Settings


CAMERA_WIDTH = 640 # Frame width (pixels)
CAMERA_HEIGHT = 480 # Frame height (pixels)
CAMERA_FPS = 30 # Target frames per second
CAMERA_BUFFER_SIZE = 1 # Minimal buffer for reduced lag

### Gesture Thresholds

LEFT_CLICK_DIST_SQ = 1600 # Click sensitivity (lower = more sensitive)
RIGHT_CLICK_DIST_SQ = 1600
CLICK_COOLDOWN = 0.3 # Min time between clicks (seconds)
SCROLL_COOLDOWN = 0.5 # Min time between scroll actions

---

## 🏗️ Architecture

┌─────────────────┐
│ Webcam Feed │
└────────┬────────┘
│
▼
┌─────────────────────┐
│ ThreadedCamera │ ← Async frame capture (30 FPS)
└────────┬────────────┘
│
▼
┌─────────────────────┐
│ Frame Processing │ ← Process every 3rd frame
│ - BGR to RGB │
│ - MediaPipe Hands │
└────────┬────────────┘
│
▼
┌─────────────────────┐
│ HandData Extract │ ← Cache 21 landmarks per hand
└────────┬────────────┘
│
▼
┌─────────────────────┐
│ Gesture Analysis │
│ - Cursor tracking │
│ - Pinch detection │
│ - Thumbs-up check │
│ - Two-hand volume │
└────────┬────────────┘
│
▼
┌─────────────────────┐
│ PyAutoGUI Actions │ ← System-level control
│ - moveTo() │
│ - click() │
│ - scroll() │
└─────────────────────┘

---


## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| **Jittery cursor** | Increase `SMOOTHENING_FACTOR` to 0.7-0.8<br>Ensure good lighting<br>Keep hand steady |
| **Clicks not registering** | Increase `LEFT_CLICK_DIST_SQ` value<br>Pinch fingers more clearly<br>Check `CLICK_COOLDOWN` isn't too long |
| **Slow performance** | Increase `FRAME_SKIP` value<br>Reduce resolution (`CAMERA_WIDTH`/`HEIGHT`)<br>Close other applications<br>Verify `ENABLE_MULTITHREADING = True` |
| **Hand not detected** | Improve lighting (avoid backlighting)<br>Position hand 1-3 feet from camera<br>Keep hands unobstructed<br>Lower MediaPipe confidence thresholds |
| **Volume control fails** | macOS-specific feature (uses AppleScript)<br>Check system permissions<br>Review terminal error messages |

---

## 📊 Performance Metrics

- **Frame Rate**: 20-30 FPS (mid-range hardware)
- **Latency**: 50-100ms cursor response time
- **CPU Usage**: 15-25% (modern multi-core processors)
- **Memory**: ~200-300MB footprint
- **Detection Range**: 1-3 feet from camera optimal

---

## 🧩 Tech Stack

- **Python 3.7+**: Core programming language
- **OpenCV**: Real-time computer vision processing
- **MediaPipe**: Google's hand tracking ML model
- **PyAutoGUI**: System-level mouse and keyboard control
- **NumPy**: Numerical computations and array operations

---

## 🚧 Limitations

- Volume control is macOS-specific (requires AppleScript)
- Requires consistent lighting conditions
- Hand must remain within camera frame
- Not suitable for precision tasks (e.g., graphic design)
- Performance depends on CPU capabilities

---

## 🗺️ Roadmap

- [ ] Cross-platform volume control (Windows/Linux)
- [ ] Drag-and-drop gesture support
- [ ] Double-click implementation
- [ ] Gesture customization GUI
- [ ] Multi-user calibration profiles
- [ ] GPU acceleration support
- [ ] Custom gesture training mode
- [ ] Mobile app integration

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Areas for Contribution

- Cross-platform volume control implementation
- Performance optimization for low-end systems
- Additional gesture patterns
- Enhanced error handling
- Documentation improvements
- Tutorial videos/GIFs

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **MediaPipe**: Google's hand tracking solution
- **OpenCV**: Computer vision library
- **PyAutoGUI**: Cross-platform GUI automation

---



Project Link: [https://github.com/naveen200401/virtual_mouse](https://github.com/naveen200401/virtual_mouse)



---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by [Naveen Chandu]

</div>
