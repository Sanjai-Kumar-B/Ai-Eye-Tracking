"""
Voice Assistant Module
Provides voice command recognition and text-to-speech feedback.
Enables hands-free typing and application control.
"""

import speech_recognition as sr
import pyttsx3
import pyautogui
import threading
import time
import os
import subprocess

class VoiceAssistant:
    """Handles voice commands for hands-free control."""
    
    def __init__(self):
        """Initialize voice assistant with speech recognition and TTS."""
        # Speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Text-to-speech - Use dummy driver to avoid threading issues
        try:
            self.engine = pyttsx3.init('sapi5')  # Windows SAPI5
        except:
            self.engine = pyttsx3.init()
        
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.8)  # Volume level
        
        # State
        self.is_enabled = False
        self.is_listening = False
        self.typing_mode = False
        self.tts_enabled = False  # Disable TTS by default to avoid threading issues
        
        # Adjust for ambient noise
        print("Voice Assistant: Adjusting for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Voice Assistant: Ready!")
    
    def speak(self, text, blocking=False):
        """
        Speak text using text-to-speech.
        Disabled by default to avoid threading issues.
        
        Args:
            text: Text to speak
            blocking: If True, wait for speech to finish
        """
        if not self.tts_enabled:
            return
            
        try:
            if blocking:
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception as e:
            print(f"TTS error: {e}")
    
    def listen(self):
        """
        Listen for voice command and return recognized text.
        
        Returns:
            str: Recognized text or None if failed
        """
        if not self.is_enabled:
            return None
        
        try:
            with self.microphone as source:
                print("Listening...")
                self.is_listening = True
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                self.is_listening = False
                
            # Recognize speech
            print("Recognizing...")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            print("No speech detected")
            self.is_listening = False
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            self.is_listening = False
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            self.is_listening = False
            return None
    
    def process_command(self, text):
        """
        Process voice command and execute action.
        
        Args:
            text: Command text (lowercase)
        
        Returns:
            str: Action performed or None
        """
        if not text:
            return None
        
        # Voice typing mode toggle
        if "start typing" in text or "begin typing" in text:
            self.typing_mode = True
            self.speak("Typing mode activated")
            return "typing_mode_on"
        
        if "stop typing" in text or "end typing" in text:
            self.typing_mode = False
            self.speak("Typing mode deactivated")
            return "typing_mode_off"
        
        # If in typing mode, type everything except stop command
        if self.typing_mode:
            self.type_text(text)
            return "typed"
        
        # Application launcher
        if text.startswith("open "):
            app_name = text.replace("open ", "").strip()
            self.open_application(app_name)
            return "open_app"
        
        # Text typing
        if text.startswith("type "):
            content = text.replace("type ", "").strip()
            self.type_text(content)
            return "type_text"
        
        # Window controls
        if "close window" in text or "close this" in text:
            pyautogui.hotkey('alt', 'f4')
            self.speak("Window closed")
            return "close_window"
        
        if "minimize" in text:
            pyautogui.hotkey('win', 'down')
            self.speak("Minimized")
            return "minimize"
        
        if "maximize" in text:
            pyautogui.hotkey('win', 'up')
            self.speak("Maximized")
            return "maximize"
        
        # Keyboard shortcuts
        if "copy" in text:
            pyautogui.hotkey('ctrl', 'c')
            self.speak("Copied")
            return "copy"
        
        if "paste" in text:
            pyautogui.hotkey('ctrl', 'v')
            self.speak("Pasted")
            return "paste"
        
        if "undo" in text:
            pyautogui.hotkey('ctrl', 'z')
            self.speak("Undone")
            return "undo"
        
        if "select all" in text:
            pyautogui.hotkey('ctrl', 'a')
            self.speak("Selected all")
            return "select_all"
        
        # Scrolling
        if "scroll down" in text:
            pyautogui.scroll(-3)
            return "scroll_down"
        
        if "scroll up" in text:
            pyautogui.scroll(3)
            return "scroll_up"
        
        # Web search
        if text.startswith("search for ") or text.startswith("google "):
            query = text.replace("search for ", "").replace("google ", "").strip()
            self.web_search(query)
            return "web_search"
        
        # Volume control
        if "volume up" in text:
            pyautogui.press('volumeup')
            self.speak("Volume up")
            return "volume_up"
        
        if "volume down" in text:
            pyautogui.press('volumedown')
            self.speak("Volume down")
            return "volume_down"
        
        if "mute" in text:
            pyautogui.press('volumemute')
            self.speak("Muted")
            return "mute"
        
        # Special keys
        if "enter" in text or "new line" in text:
            pyautogui.press('enter')
            return "enter"
        
        if "backspace" in text:
            pyautogui.press('backspace')
            return "backspace"
        
        if "delete" in text:
            pyautogui.press('delete')
            return "delete"
        
        if "tab" in text:
            pyautogui.press('tab')
            return "tab"
        
        # If no command matched
        self.speak("Command not recognized")
        return None
    
    def type_text(self, text):
        """
        Type text using keyboard.
        
        Args:
            text: Text to type
        """
        try:
            pyautogui.write(text, interval=0.05)
            print(f"Typed: {text}")
        except Exception as e:
            print(f"Error typing text: {e}")
    
    def open_application(self, app_name):
        """
        Open application by name.
        
        Args:
            app_name: Name of application to open
        """
        # Common application paths for Windows
        app_paths = {
            'chrome': [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe')
            ],
            'firefox': [
                r'C:\Program Files\Mozilla Firefox\firefox.exe',
                r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
            ],
            'edge': ['msedge'],  # Edge can be opened via command
            'notepad': ['notepad'],
            'calculator': ['calc'],
            'paint': ['mspaint'],
            'explorer': ['explorer'],
            'word': [
                r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
                r'C:\Program Files (x86)\Microsoft Office\Office16\WINWORD.EXE'
            ],
            'excel': [
                r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
                r'C:\Program Files (x86)\Microsoft Office\Office16\EXCEL.EXE'
            ],
            'powerpoint': [
                r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE',
                r'C:\Program Files (x86)\Microsoft Office\Office16\POWERPNT.EXE'
            ],
            'outlook': [
                r'C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE',
                r'C:\Program Files (x86)\Microsoft Office\Office16\OUTLOOK.EXE'
            ],
            'vscode': [
                os.path.expandvars(r'%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe'),
                r'C:\Program Files\Microsoft VS Code\Code.exe'
            ],
            'spotify': [
                os.path.expandvars(r'%APPDATA%\Spotify\Spotify.exe')
            ],
            'vlc': [
                r'C:\Program Files\VideoLAN\VLC\vlc.exe',
                r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe'
            ],
        }
        
        # Normalize app name
        app_key = app_name.lower()
        
        # Handle aliases
        aliases = {
            'google chrome': 'chrome',
            'microsoft edge': 'edge',
            'file explorer': 'explorer',
            'vs code': 'vscode',
        }
        app_key = aliases.get(app_key, app_key)
        
        # Get possible paths for this app
        paths = app_paths.get(app_key, [app_name])
        
        try:
            # Try each possible path
            for path in paths:
                try:
                    if os.path.exists(path) if os.path.isabs(path) else True:
                        subprocess.Popen(path, shell=True)
                        print(f"Opened {app_name}")
                        self.speak(f"Opening {app_name}")
                        return
                except Exception as e:
                    continue
            
            # If no path worked, try as command
            subprocess.Popen(app_name, shell=True)
            print(f"Opened {app_name}")
        except Exception as e:
            print(f"Error opening {app_name}: {e}")
            self.speak(f"Could not open {app_name}")
    
    def web_search(self, query):
        """
        Perform web search in default browser.
        
        Args:
            query: Search query
        """
        import webbrowser
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        self.speak(f"Searching for {query}")
        print(f"Searching: {query}")
    
    def enable(self):
        """Enable voice assistant."""
        self.is_enabled = True
        self.speak("Voice assistant enabled")
        print("Voice Assistant: Enabled")
    
    def disable(self):
        """Disable voice assistant."""
        self.is_enabled = False
        self.typing_mode = False
        self.speak("Voice assistant disabled")
        print("Voice Assistant: Disabled")
    
    def toggle(self):
        """Toggle voice assistant on/off."""
        if self.is_enabled:
            self.disable()
        else:
            self.enable()
        return self.is_enabled
