# 👁️ AI Gaze-Controlled Mouse for Disabled Users

<div align="center">

**An AI-powered desktop application that enables users with physical disabilities to control their computer mouse using precise EYE GAZE and blinks - NO HEAD MOVEMENT REQUIRED.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![Version](https://img.shields.io/badge/Version-2.0%20Gaze%20Tracking-brightgreen.svg)

</div>

---

## ⚡ Version 2.0 - GAZE TRACKING MODE

**🎯 Major Upgrade**: This is now a **true gaze tracker**, not just a head tracker!

### What Changed:
- **OLD**: Move your head to control cursor (head tracking)
- **NEW**: Keep head still, move only your EYES (gaze tracking)
- **Requires**: Initial calibration for high accuracy
- **Perfect for**: Users with NO head movement capability

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Building Executable](#building-executable)
- [Troubleshooting](#troubleshooting)
- [Future Scope](#future-scope)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project provides a complete desktop solution for hands-free computer control using only eye movements and blinks. Built with Python and powered by AI/ML technologies, it's designed specifically for users with physical disabilities who cannot use traditional input devices.

### Key Technologies

- **MediaPipe FaceMesh**: Real-time facial landmark detection
- **OpenCV**: Video capture and processing
- **PyAutoGUI**: Mouse control automation
- **Tkinter**: User-friendly GUI
- **NumPy**: Mathematical operations

---

## ✨ Features

### Core Functionality

✅ **Gaze Tracking (NEW!)**
- True gaze direction detection (not head position)
- Relative iris position within eye socket
- Works without ANY head movement
- Calibration-based accurate mapping

✅ **5-Point Calibration System**
- One-time setup (or recalibrate anytime)
- Looks at screen corners + center
- Blink to confirm each point
- Personal gaze-to-screen mapping

✅ **Eye Tracking**
- Real-time eye and pupil detection using MediaPipe
- Accurate iris tracking for cursor control
- High smoothing (0.85) to compensate for saccades
- Smooth cursor movement with jitter reduction

✅ **Mouse Control**
- Gaze coordinates → Screen coordinates mapping
- Calibration-based direct mapping (no sensitivity needed)
- Full screen coverage after calibration

✅ **Blink Detection**
- Eye Aspect Ratio (EAR) algorithm implementation
- Left eye blink → Left Click
- Right eye blink → Right Click
- Intelligent debouncing to prevent accidental clicks

✅ **User Interface**
- Clean, accessible Tkinter GUI
- **Calibrate Gaze** button (primary action)
- Start/Pause/Exit controls
- Real-time status and calibration display
- Visual feedback on camera window

✅ **Advanced Features**
- Optional voice feedback (Text-to-Speech)
- Configurable smoothing settings
- Exception handling and error recovery
- Camera detection and validation
- Calibration save/load capability

---

## 🚀 Installation

### Prerequisites

- **Operating System**: Windows 10/11
- **Python**: 3.8 or higher
- **Webcam**: Built-in or USB webcam
- **RAM**: Minimum 4GB recommended

### Step-by-Step Installation

1. **Clone or Download the Project**
   ```bash
   cd eye_mouse_project
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python -c "import cv2, mediapipe, pyautogui; print('All dependencies installed successfully!')"
   ```

---

## 🎮 Usage

### First Time Setup (IMPORTANT!)

1. **Start the Application**
   ```bash
   python main.py
   ```

2. **Calibrate Your Gaze (REQUIRED)**
   - Click **"🎯 Calibrate Gaze"** button
   - Keep your HEAD STILL throughout calibration
   - Look at each target circle that appears:
     - Top-Left corner
     - Top-Right corner
     - Bottom-Right corner
     - Bottom-Left corner
     - Center
   - **Blink when you're looking directly at the target**
   - System captures your gaze range
   - Calibration complete! ✓

3. **Start Tracking**
   - Click **"▶ Start Tracking"**
   - The webcam window will open showing your face with landmarks
   - **Keep your HEAD STILL** (very important!)
   - Move your EYES to control the cursor
   - Blink left eye for left click
   - Blink right eye for right click
   - Click **"⏸ Pause"** to stop tracking
   - Click **"❌ Exit"** to close the application

4. **Keyboard Shortcuts**
   - Press **Q** in the camera window to hide it (tracking continues)

### Daily Use (After First Calibration)

```
1. Launch app
2. Click "Calibrate Gaze" (quick 2-minute recalibration)
3. Click "Start Tracking"
4. Look where you want cursor to go
5. Keep head still, move only eyes
6. Blink to click
```

### Tips for Best Performance

✅ **DO:**
- Keep head completely still (use headrest if possible)
- Position yourself 1-2 feet from webcam
- Ensure good, even lighting on your face
- Calibrate in the same position you'll use for tracking
- Recalibrate if camera or your position changes
- Take breaks every 15-20 minutes

❌ **DON'T:**
- Move your head while tracking
- Use in poor lighting
- Wear glasses with strong reflections
- Sit too close or too far from camera
- Skip calibration

---

## 🔧 How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                   (Application Controller)                   │
└────────────┬────────────────────────────────────────────────┘
             │
             ├─────► eye_tracker.py
             │       • MediaPipe FaceMesh
             │       • Facial landmark detection
             │       • Eye position calculation
             │
             ├─────► mouse_controller.py
             │       • Coordinate conversion
             │       • Cursor movement
             │       • Click actions
             │
             ├─────► blink_detector.py
             │       • EAR calculation
             │       • Blink detection
             │       • Click triggering
             │
             └─────► ui.py
                     • Tkinter GUI
                     • User controls
                     • Status display
```

### Eye Aspect Ratio (EAR) Algorithm

The blink detection uses the Eye Aspect Ratio formula:

```
EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
```

Where p1-p6 are the eye landmark points. When EAR drops below a threshold (~0.20), a blink is detected.

### Coordinate Mapping

```
Camera Space (0-1 normalized) → Screen Space (pixels)
  ↓
Apply Sensitivity & Smoothing
  ↓
Dead Zone Filter
  ↓
Screen Coordinates
  ↓
PyAutoGUI Movement
```

---

## ⚙️ Configuration

### Adjusting Smoothing (Most Common Adjustment)

Edit `mouse_controller.py`:

```python
# For gaze tracking, higher smoothing is recommended
self.smoothing_factor = 0.85  # Default for gaze tracking

# If cursor is too jittery: increase to 0.90
# If cursor feels slow: decrease to 0.80
```

### Adjusting Blink Threshold

Edit `blink_detector.py`:

```python
# Lower = more sensitive (easier to trigger)
# Higher = less sensitive (harder to trigger)
self.ear_threshold = 0.20  # Default
```

### Calibration Margin

Edit `calibration.py`:

```python
# Increase for wider cursor range
margin_x = 0.05  # Default (5% margin)
margin_y = 0.05  # Default (5% margin)
```

---

## 📦 Building Executable

To create a standalone `.exe` file that can run without Python installed:

### Using PyInstaller

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build the Executable**
   ```bash
   pyinstaller --noconfirm --onefile --windowed --icon=icon.ico main.py
   ```

3. **Find the Executable**
   - The `.exe` file will be in the `dist/` folder
   - Distribute this file to users

### Build Options Explained

- `--onefile`: Creates a single executable file
- `--windowed`: Hides the console window
- `--icon=icon.ico`: Sets application icon (optional)
- `--add-data`: Include additional files if needed

### Advanced Build Command

```bash
pyinstaller --noconfirm --onefile --windowed ^
    --name "EyeMouse" ^
    --icon=icon.ico ^
    --add-data "README.md;." ^
    main.py
```

---

## 🔍 Troubleshooting

### Common Issues

#### "Not Calibrated" Error
```
Error: Please calibrate first!
```
**Solution**: 
- Click "Calibrate Gaze" button before "Start Tracking"
- Complete all 5 calibration points
- Ensure you blinked at each target

#### Calibration Fails or Times Out
**Solution**:
- Ensure good lighting on face
- Look directly at targets
- Perform deliberate, clear blinks
- Remove glasses if causing reflections
- Position face clearly in camera view

#### Cursor Doesn't Reach Screen Edges
**Solution**:
- Recalibrate with more extreme eye movements
- Look as far as comfortable to corners
- Reduce margin in `calibration.py`:
  ```python
  margin_x = 0.02  # Smaller margin
  margin_y = 0.02
  ```

#### Cursor is Jittery
**Solution**:
- Increase smoothing in `mouse_controller.py`:
  ```python
  self.smoothing_factor = 0.90  # Higher smoothing
  ```
- Ensure head is completely still
- Check lighting (avoid shadows on face)
- Use headrest or neck support

#### Cursor Moves in Wrong Direction
**Solution**:
- Recalibrate completely
- Ensure camera is not mirrored
- Keep head straight during calibration
- Check landmarks are detected correctly

#### Camera Not Detected
```
Error: Camera not found!
```
**Solution**: 
- Check if webcam is connected and working
- Try different USB ports
- Close other applications using the camera
- Restart the application

#### Cursor Feels Slow or Laggy
**Solution**:
- Decrease smoothing to 0.80
- Reduce webcam resolution
- Close unnecessary background apps
- Check CPU usage

---

## 🚀 Future Scope

### Planned Features

- [ ] **Calibration Mode**: Personalized sensitivity calibration
- [ ] **Gesture Control**: Head movements for additional commands
- [ ] **Voice Commands**: Integration with speech recognition
- [ ] **Multi-Monitor Support**: Improved multi-display handling
- [ ] **Dwell Click**: Click by dwelling cursor for X seconds
- [ ] **Configuration GUI**: UI for adjusting settings without code
- [ ] **Usage Analytics**: Track and display usage statistics
- [ ] **Accessibility Profiles**: Pre-configured profiles for different disabilities
- [ ] **Remote Control**: Control other devices via network
- [ ] **Mobile App**: Smartphone as wireless eye tracker

### Potential Improvements

- Machine learning for adaptive sensitivity
- Support for Linux and macOS
- Integration with screen readers
- Custom cursor designs for better visibility
- Battery optimization for laptops
- Cloud sync for settings across devices

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue describing the problem
2. **Suggest Features**: Share your ideas for improvements
3. **Submit Pull Requests**: Contribute code improvements
4. **Documentation**: Help improve docs and tutorials
5. **Testing**: Test on different hardware and report results

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd eye_mouse_project

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dev dependencies
pip install -r requirements.txt
pip install pylint black pytest

# Run tests
pytest tests/

# Format code
black *.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👏 Acknowledgments

- **MediaPipe** by Google - For excellent face landmark detection
- **OpenCV** - For computer vision capabilities
- **PyAutoGUI** - For cross-platform GUI automation
- **Community Contributors** - For feedback and improvements

---

## 📞 Support

For help and support:

- **Issues**: Open an issue on GitHub
- **Email**: [your-email@example.com]
- **Documentation**: Read this README carefully

---

## 🌟 Star This Project

If you find this project helpful, please give it a ⭐ on GitHub!

---

<div align="center">

**Built with ❤️ for accessibility and inclusion**

Made with Python | Powered by AI | Designed for Everyone

</div>
