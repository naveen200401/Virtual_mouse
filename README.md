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

> **Note**: Replace placeholder images with actual screenshots or GIFs of your application in action

---

## 🚀 Installation

### Prerequisites

- **Python**: 3.7 or higher
- **Webcam**: USB or built-in camera
- **OS**: macOS (full features), Windows/Linux (mouse & scroll only)

### Quick Start

1. **Clone the repository**
