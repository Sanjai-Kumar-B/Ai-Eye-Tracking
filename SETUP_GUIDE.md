# 🚀 Quick Setup Guide - Eye Mouse Controller

## For First-Time Users

Follow these simple steps to get the Eye Mouse running on your computer:

---

## ✅ Step 1: Install Python

1. **Download Python 3.12** (or 3.8+):
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.12.x"

2. **Install Python**:
   - ⚠️ **IMPORTANT**: Check ✅ "Add Python to PATH" during installation
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**:
   - Open Command Prompt (search "cmd" in Windows)
   - Type: `python --version`
   - Should show: `Python 3.12.x` or similar

---

## ✅ Step 2: Extract Project Files

1. **Extract the ZIP file** (if you received a ZIP)
2. **Keep all files together** in one folder
3. **Remember the folder location** (e.g., `C:\Users\YourName\Desktop\eye_mouse_project\`)

---

## ✅ Step 3: Install Dependencies (One-Time Setup)

1. **Open Command Prompt or PowerShell**:
   - Press `Windows + R`
   - Type: `cmd`
   - Press Enter

2. **Navigate to Project Folder**:
   ```bash
   cd C:\Users\YourName\Desktop\eye_mouse_project
   ```
   (Replace with your actual folder path)

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Wait for Installation** (2-5 minutes):
   - You'll see packages being downloaded and installed
   - Don't close the window until it says "Successfully installed..."

---

## ✅ Step 4: Run the Application

1. **In the same Command Prompt window**:
   ```bash
   python main.py
   ```

2. **The application window will open!** 🎉

---

## ✅ Step 5: First-Time Calibration

1. **Click "🎯 Calibrate Gaze"**

2. **Follow the calibration process**:
   - 5 targets will appear (corners + center)
   - Look at each target
   - Blink both eyes to confirm
   - Wait for "Calibration Complete!"

3. **Click "▶ Start Tracking"**

4. **Control your mouse with your eyes!**
   - Look around to move cursor
   - 2 blinks = Right click
   - 3 blinks = Left click
   - 4 blinks = Drag/Drop (grab item, move, release)
   - 5 blinks = Middle click (open in new tab)

---

## 🎯 Quick Command Reference

### First Time Setup:
```bash
# 1. Open Command Prompt
# 2. Navigate to project folder
cd path\to\eye_mouse_project

# 3. Install dependencies (ONE TIME ONLY)
pip install -r requirements.txt

# 4. Run application
python main.py
```

### Every Time After:
```bash
# Just navigate and run
cd path\to\eye_mouse_project
python main.py
```

---

## ⚠️ Common First-Time Issues

### ❌ "python is not recognized"
**Problem**: Python not added to PATH  
**Solution**: 
- Reinstall Python and CHECK ✅ "Add Python to PATH"
- OR add manually to system environment variables

### ❌ "pip is not recognized"  
**Problem**: pip not installed  
**Solution**:
```bash
python -m pip install --upgrade pip
```

### ❌ "No module named 'cv2'"
**Problem**: Dependencies not installed  
**Solution**:
```bash
pip install -r requirements.txt
```

### ❌ "Camera not found"
**Problem**: Webcam not detected  
**Solution**:
- Check webcam is connected
- Close other apps using webcam (Zoom, Skype)
- Try different USB port

---

## 📁 What Files Do You Need?

**Essential Files (MUST include all):**
```
eye_mouse_project/
├── main.py                 ✅ Main application
├── eye_tracker.py         ✅ Eye tracking module
├── mouse_controller.py    ✅ Cursor control
├── blink_detector.py      ✅ Blink detection
├── calibration.py         ✅ Calibration system
├── ui.py                  ✅ User interface
├── requirements.txt       ✅ Dependencies list
├── README.md              📖 Full documentation
├── SETUP_GUIDE.md         📖 This file
└── LICENSE                📄 License file
```

**Optional Documentation:**
```
├── GAZE_TRACKING_GUIDE.md      📖 Advanced guide
├── TECHNICAL_DOCUMENTATION.md  📖 Technical details
└── UPGRADE_SUMMARY.md          📖 Version history
```

---

## 💡 Usage Tips

### For Best Results:
- ✅ Use good lighting on your face
- ✅ Position 1-2 feet from webcam
- ✅ Calibrate before each use
- ✅ Keep head relatively still
- ✅ Take breaks every 15-20 minutes

### Controls:
- **Look**: Move cursor
- **2 Blinks**: Right click
- **3 Blinks**: Left click
- **4 Blinks**: Drag/Drop (grab and release)
- **5 Blinks**: Middle click
- **"Pause" Button**: Stop tracking
- **"Q" Key**: Close webcam window

---

## 🆘 Need Help?

1. **Read README.md** - Full documentation with troubleshooting
2. **Check Troubleshooting section** - Common issues and solutions
3. **Open GitHub Issue** - Report bugs or ask questions

---

## 🎊 You're All Set!

Your Eye Mouse Controller is ready to use. Enjoy hands-free computer control!

**Repository**: https://github.com/Sanjai-Kumar-B/Ai-Eye-Tracking

---

*Made with ❤️ for accessibility*
