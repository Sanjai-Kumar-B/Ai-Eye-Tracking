# 👁️ AI Eye-Controlled Mouse - Accessibility Tool

<div align="center">

**An AI-powered desktop application that enables hands-free computer control using eye gaze tracking and blink detection for users with physical disabilities.**

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.21-orange.svg)

</div>

---

## 🎯 Overview

This project provides a complete **hands-free mouse control solution** using eye gaze tracking and blink detection. Built specifically for users with physical disabilities who cannot use traditional input devices.

### ✨ Key Features

- **👁️ Eye Gaze Tracking**: Control cursor by looking at different parts of the screen
- **👀 Blink Detection**: Perform clicks using eye blinks
  - **Double Blink** (both eyes) → Right Click
  - **Triple Blink** (both eyes) → Left Click
- **🎯 5-Point Calibration**: Personalized calibration for accurate tracking
- **🖱️ Smooth Cursor Control**: Advanced smoothing and deadzone to prevent jitter
- **🎨 User-Friendly GUI**: Simple interface with calibration and control buttons

---

## 📋 Table of Contents

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Quick Start (For Your Friend)](#quick-start-for-your-friend)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Configuration](#configuration)
- [License](#license)

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11
- **Python**: 3.8 or higher (tested on 3.12)
- **RAM**: 4GB minimum (8GB recommended)
- **Webcam**: Built-in or USB webcam (720p or higher recommended)
- **Processor**: Intel i3 or equivalent
- **Internet**: Required for initial dependency installation only

### Recommended Setup
- Good lighting on your face
- Stable seating position (headrest recommended)
- 1-2 feet distance from webcam
- No strong reflections on glasses (if worn)

---

## ⚡ Quick Start (For Your Friend)

### Option 1: Ready-to-Run Package (Easiest)

1. **Download the complete project folder**
   - Get the entire `eye_mouse_project` folder
   - Keep all files together in the same folder

2. **Install Python** (if not installed)
   - Download from: https://www.python.org/downloads/
   - During installation: ✅ **Check "Add Python to PATH"**
   
3. **Install Dependencies** (ONE-TIME SETUP)
   - Open Command Prompt or PowerShell
   - Navigate to project folder:
     ```bash
     cd path\to\eye_mouse_project
     ```
   - Run installation command:
     ```bash
     pip install -r requirements.txt
     ```
   - Wait for all packages to install (2-5 minutes)

4. **Run the Application**
   ```bash
   python main.py
   ```

5. **First Time Setup**
   - Click **"🎯 Calibrate Gaze"** button
   - Follow the calibration instructions
   - Click **"▶ Start Tracking"**
   - Control cursor with your eyes!

### Option 2: Virtual Environment (Recommended for Developers)

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

---

## 🔧 Key Technologies

- **MediaPipe FaceMesh v0.10.21**: 478 facial landmarks, iris tracking
- **OpenCV 4.12**: Video capture and image processing
- **PyAutoGUI 0.9.54**: Mouse cursor control and clicks
- **NumPy**: Mathematical calculations and smoothing
- **Tkinter**: Built-in Python GUI (no extra installation)

---

## 📦 Dependencies (Auto-Installed)

All required packages are listed in `requirements.txt`:

```
opencv-python      # Computer vision and webcam
mediapipe         # Face and eye landmark detection
pyautogui         # Mouse control
numpy             # Mathematical operations
pyttsx3           # Text-to-speech (optional)
screeninfo        # Multi-monitor support
Pillow            # Image processing
```

**Installation**: Run `pip install -r requirements.txt`

---

## 🚀 How to Use

### Step 1: Launch the Application

```bash
python main.py
```

A window will open with the control interface.

### Step 2: Calibrate Your Gaze (REQUIRED - First Time)

1. Click **"🎯 Calibrate Gaze"** button
2. A webcam window opens showing your face
3. **5 target circles** will appear one by one:
   - **Top-Left corner**
   - **Top-Right corner**
   - **Bottom-Right corner**
   - **Bottom-Left corner**
   - **Center**
4. For each target:
   - **Look directly at the target**
   - **Blink BOTH eyes** to confirm
   - Target turns green ✓
5. After all 5 points: **Calibration Complete!**

### Step 3: Start Eye Tracking

1. Click **"▶ Start Tracking"**
2. Webcam window opens with facial landmarks
3. **Look around** to move the cursor
4. **Blink to click**:
   - **Double blink** (both eyes, quick) = **RIGHT CLICK**
   - **Triple blink** (both eyes, quick) = **LEFT CLICK**

### Step 4: Control Tips

✅ **Best Practices:**
- Keep head relatively still (some movement is OK)
- Look at different screen areas to move cursor
- Perform deliberate, clear blinks for clicks
- Take breaks every 15-20 minutes

⏸️ **Pause Tracking**: Click "⏸ Pause" button  
❌ **Exit**: Click "❌ Exit" button or press 'Q' in webcam window

---

## 🔍 How It Works

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│  User's Face → Webcam → MediaPipe → Eye Landmarks      │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴──────────────┐
        │                           │
        ▼                           ▼
  ┌──────────┐              ┌─────────────┐
  │   Iris   │              │    Blink    │
  │ Position │              │  Detection  │
  │ Tracking │              │    (EAR)    │
  └────┬─────┘              └──────┬──────┘
       │                           │
       ▼                           ▼
  ┌─────────────┐           ┌─────────────┐
  │ Calibration │           │   Pattern   │
  │   Mapping   │           │   Matching  │
  └─────┬───────┘           └──────┬──────┘
        │                          │
        ▼                          ▼
  ┌──────────────┐          ┌─────────────┐
  │ Cursor Move  │          │   Clicks    │
  │  (PyAutoGUI) │          │ (PyAutoGUI) │
  └──────────────┘          └─────────────┘
```

### Eye Aspect Ratio (EAR) - Blink Detection

```
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 × ||p1 - p4||)

Where p1-p6 are eye landmarks
EAR < 0.21 → Eye is closed (blink detected)
```

### Calibration System

The 5-point calibration creates a mapping:
```
Iris Position (0.0 - 1.0) → Screen Coordinates (pixels)
```

This personalized mapping ensures accurate cursor control across your entire screen.

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### ❌ "Please calibrate first!" Error
**Problem**: Tried to start tracking without calibration  
**Solution**: Click "🎯 Calibrate Gaze" button before "▶ Start Tracking"

#### ❌ Camera Not Found
**Problem**: Webcam not detected  
**Solutions**:
- Check webcam is connected and working
- Close other apps using webcam (Zoom, Skype, etc.)
- Try different USB port
- Restart application

#### ❌ Calibration Times Out
**Problem**: Calibration doesn't detect blinks  
**Solutions**:
- Improve lighting on your face
- Remove glasses if they cause reflections
- Perform clear, deliberate blinks (close eyes fully)
- Look directly at target before blinking
- Ensure face is clearly visible in webcam

#### ❌ Cursor Doesn't Move or Moves Erratically
**Problem**: Poor tracking after calibration  
**Solutions**:
- **Recalibrate** in your actual working position
- Ensure good, even lighting
- Keep head relatively stable
- Check webcam is focused on your face
- Increase smoothing in settings (see Configuration)

#### ❌ Clicks Don't Work
**Problem**: Blinks not detected or false clicks  
**Solutions**:
- Perform clear, complete blinks (fully close eyes)
- **Double blink**: Close-open-close-open (quick)
- **Triple blink**: Close-open-close-open-close-open (quick)
- Wait for cooldown period between click attempts
- Adjust EAR threshold in `blink_detector.py`

#### ❌ Cursor Too Jittery
**Problem**: Cursor shakes too much  
**Solutions**:
- Edit `mouse_controller.py`:
  ```python
  self.smoothing_factor = 0.90  # Increase from 0.85
  ```
- Keep head more stable
- Improve lighting conditions

#### ❌ Cursor Too Slow/Laggy
**Problem**: Cursor feels unresponsive  
**Solutions**:
- Decrease smoothing:
  ```python
  self.smoothing_factor = 0.80  # Decrease from 0.85
  ```
- Close background applications
- Use better webcam if available

#### ❌ Dependencies Installation Failed
**Problem**: `pip install -r requirements.txt` errors  
**Solutions**:
- Update pip: `python -m pip install --upgrade pip`
- Install Visual C++ Build Tools (for some packages)
- Try installing packages individually:
  ```bash
  pip install opencv-python
  pip install mediapipe
  pip install pyautogui
  pip install numpy
  ```

---

## ⚙️ Configuration

### Adjusting Cursor Smoothing

Edit `mouse_controller.py`:

```python
class MouseController:
    def __init__(self):
        self.smoothing_factor = 0.85  # Default
        # Lower (0.70-0.80) = More responsive, more jitter
        # Higher (0.85-0.95) = Smoother, slower response
```

### Adjusting Blink Sensitivity

Edit `blink_detector.py`:

```python
class BlinkDetector:
    def __init__(self):
        self.ear_threshold = 0.21  # Default
        # Lower (0.18-0.20) = Easier to trigger (more sensitive)
        # Higher (0.22-0.25) = Harder to trigger (less sensitive)
        
        self.min_consecutive_frames = 3  # Frames to confirm blink
        # Lower = More responsive
        # Higher = More reliable, fewer false positives
```

### Adjusting Eye Position Smoothing

Edit `eye_tracker.py`:

```python
class EyeTracker:
    def __init__(self):
        self.smoothing_factor = 0.3  # Default (eye position)
        self.history_size = 5  # Average last N frames
        # Increase history_size for more stability
```

---

## 📁 Project Structure

```
eye_mouse_project/
│
├── main.py                    # Main application entry point
├── eye_tracker.py            # Eye/iris tracking with MediaPipe
├── mouse_controller.py       # Cursor movement and control
├── blink_detector.py         # Blink detection (EAR algorithm)
├── calibration.py            # 5-point calibration system
├── ui.py                     # Tkinter GUI interface
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── LICENSE                   # MIT License
│
└── Documentation/
    ├── GAZE_TRACKING_GUIDE.md
    ├── TECHNICAL_DOCUMENTATION.md
    └── UPGRADE_SUMMARY.md
```

---

## 🎁 Sharing with Friends

### What to Share:

1. **Entire project folder** (all files together)
2. **This README** for setup instructions
3. **Python 3.8+** installation requirement

### Setup Instructions for Recipient:

```bash
# 1. Install Python (if needed)
#    Download from python.org, check "Add to PATH"

# 2. Open terminal in project folder
cd path\to\eye_mouse_project

# 3. Install dependencies (one time)
pip install -r requirements.txt

# 4. Run application
python main.py

# 5. Calibrate and enjoy!
```

### Alternative: Create Executable (Advanced)

To create a standalone `.exe` file:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "EyeMouse" main.py

# Find .exe in dist/ folder
# Share the entire dist/ folder with dependencies
```

---

## 🎯 Usage Tips for Best Results

### 🟢 DO:
- ✅ Keep head relatively stable during use
- ✅ Calibrate in your actual working position
- ✅ Use good, even lighting on your face
- ✅ Position yourself 1-2 feet from webcam
- ✅ Take breaks every 15-20 minutes
- ✅ Recalibrate if you change seating position
- ✅ Close eyes fully for clear blinks

### 🔴 DON'T:
- ❌ Use in dim or uneven lighting
- ❌ Wear glasses with strong reflections
- ❌ Sit too close or too far from camera
- ❌ Make sudden head movements
- ❌ Skip calibration step
- ❌ Rush the calibration process


---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use allowed
- ✅ Modification allowed  
- ✅ Distribution allowed
- ✅ Private use allowed
- ⚠️ No warranty provided

---

## � Acknowledgments

- **MediaPipe** by Google - Excellent face and iris landmark detection
- **OpenCV** - Powerful computer vision library
- **PyAutoGUI** - Simple and effective GUI automation
- **Python Community** - Amazing ecosystem and support

---

## � Support & Contact

**Issues?** Open an issue on GitHub: https://github.com/Sanjai-Kumar-B/Ai-Eye-Tracking/issues

**Questions?** Check the Troubleshooting section above first!

---

<div align="center">

### 🌟 If this project helps you, please give it a ⭐ on GitHub!

**Built with ❤️ for accessibility and inclusion**

*Making technology accessible for everyone*

---

**Version**: 2.0 | **Last Updated**: November 2025

</div>
