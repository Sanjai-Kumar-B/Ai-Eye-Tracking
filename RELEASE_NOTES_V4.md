# 🚀 Release Notes - Version 4.0

## Head Tracking + Voice Assistant Edition
**Release Date:** November 20, 2025

---

## 🎉 Major Updates

### 1. **Switched to Head Tracking** 🎯
- **Previous:** Eye gaze tracking (iris position)
- **Now:** Head tracking (nose position)
- **Benefits:**
  - ✅ More reliable - no NaN errors
  - ✅ More natural - move your head freely
  - ✅ No need to keep head still
  - ✅ Easier to use for beginners
  - ✅ Works better with glasses

### 2. **Fully Functional Voice Assistant** 🎤
- **Status:** Working perfectly!
- **Features:**
  - Voice-to-text typing
  - Application launching (Chrome, Notepad, Calculator, etc.)
  - Keyboard shortcuts (copy, paste, undo, etc.)
  - Web searches
  - Window controls
  - Scroll commands
  - 20+ voice commands

### 3. **Fixed Application Paths** 🔧
- Smart path detection for common applications
- Checks multiple possible installation locations
- Works across different Windows configurations
- Supports:
  - Chrome, Firefox, Edge
  - Notepad, Calculator, Paint, File Explorer
  - Microsoft Office (Word, Excel, PowerPoint, Outlook)
  - VS Code, Spotify, VLC

### 4. **Fixed NaN Errors** ✅
- Added comprehensive safety checks in eye tracking
- No more "cannot convert float NaN to integer" errors
- Stable and reliable tracking

### 5. **Fixed Voice Threading Issues** ✅
- Removed problematic TTS background threads
- Disabled speech feedback by default
- Voice commands execute silently and reliably

---

## 📋 Complete Feature List

### Mouse Control
- ✅ Head movement → Cursor control
- ✅ 2 blinks → Right click
- ✅ 3 blinks → Left click
- ✅ 4 blinks → Drag/drop toggle
- ✅ 5 blinks → Middle click
- ✅ Smooth cursor movement with multi-frame averaging
- ✅ 5-point calibration system

### Voice Commands
- ✅ "type [text]" - Type without keyboard
- ✅ "open [app]" - Launch applications
- ✅ "copy" / "paste" / "undo" - Keyboard shortcuts
- ✅ "scroll up" / "scroll down" - Scroll pages
- ✅ "search for [query]" - Web search
- ✅ "close window" / "minimize" / "maximize" - Window controls
- ✅ "enter" / "backspace" / "delete" / "tab" - Special keys
- ✅ "volume up" / "volume down" / "mute" - Volume control

---

## 🔧 Technical Improvements

### Architecture Changes
- `EyeTracker` class now supports dual modes (head/gaze tracking)
- `use_head_tracking` parameter added to constructor
- Separate methods for head position (`_get_head_position`) and iris gaze (`_get_iris_gaze`)

### Voice Assistant Fixes
- Improved `open_application()` with smart path detection
- Multiple fallback paths for each application
- Better error handling and user feedback
- TTS disabled by default to prevent threading conflicts

### Bug Fixes
- Fixed calibration crash (updated for new blink detector return format)
- Fixed NaN values in gaze calculations
- Fixed voice assistant "run loop already started" error
- Fixed application launching errors

---

## 📦 Dependencies

### Updated Requirements
```
opencv-python==4.12.0.88
mediapipe==0.10.21
pyautogui==0.9.54
numpy==2.3.4
pyttsx3==2.98
SpeechRecognition==3.12.0
pyaudio==0.2.14
screeninfo==0.8.1
Pillow==11.0.0
```

### New Dependencies
- **SpeechRecognition** - Voice command recognition
- **pyaudio** - Audio input for voice commands

---

## 🎮 How to Use

### Initial Setup
1. Install Python 3.8+
2. Run: `pip install -r requirements.txt`
3. Launch: `python main.py`

### First-Time Calibration
1. Click "Calibrate Gaze"
2. Move your **head** to position nose at each target
3. Blink to confirm each point
4. Complete all 5 calibration points

### Using Head Tracking
1. Click "Start Tracking"
2. Move your head to control cursor
3. Blink patterns for mouse actions:
   - 2 blinks = Right click
   - 3 blinks = Left click
   - 4 blinks = Drag toggle
   - 5 blinks = Middle click

### Using Voice Assistant
1. Click "Enable Voice Assistant"
2. Click "🎤 Listen" button
3. Speak your command clearly
4. Command executes automatically

---

## 🐛 Known Issues

### Minor Issues
- MediaPipe warnings about feedback manager (harmless, can be ignored)
- Voice recognition requires internet connection (uses Google API)
- Some applications may require full path specification

### Workarounds
- All warnings are cosmetic and don't affect functionality
- Voice commands work offline for local actions (typing, shortcuts)
- Application paths can be customized in `voice_assistant.py`

---

## 🔮 Future Enhancements

### Planned for v4.1
- [ ] Option to switch between head/gaze tracking in GUI
- [ ] Custom voice command macros
- [ ] Offline voice recognition
- [ ] Configuration file for custom app paths

### Planned for v5.0
- [ ] On-screen keyboard integration
- [ ] Gesture-based scrolling (edge dwell)
- [ ] Multi-monitor optimization
- [ ] Machine learning for personalized tracking

---

## 🙏 Credits

- **MediaPipe** - Face mesh and landmark detection
- **OpenCV** - Video processing
- **Google Speech Recognition** - Voice command recognition
- **PyAutoGUI** - Mouse and keyboard control

---

## 📄 License

MIT License - Feel free to use, modify, and distribute!

---

**Enjoy complete hands-free computer control!** 🎉

For issues and feature requests, visit:
https://github.com/Sanjai-Kumar-B/Ai-Eye-Tracking/issues
