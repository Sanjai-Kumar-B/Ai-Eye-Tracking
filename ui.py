"""
User Interface Module
Tkinter-based GUI for controlling the eye tracking application.
Provides start/pause/exit controls and status display.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Optional: Voice feedback
try:
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("Note: pyttsx3 not available. Voice feedback disabled.")

class EyeMouseGUI:
    """Graphical User Interface for Eye Mouse Controller."""
    
    def __init__(self, start_callback, pause_callback, exit_callback, calibrate_callback):
        """
        Initialize the GUI.
        
        Args:
            start_callback: Function to call when starting tracking
            pause_callback: Function to call when pausing tracking
            exit_callback: Function to call when exiting application
            calibrate_callback: Function to call when calibrating gaze
        """
        self.start_callback = start_callback
        self.pause_callback = pause_callback
        self.exit_callback = exit_callback
        self.calibrate_callback = calibrate_callback
        
        # Initialize voice engine if available
        self.voice_engine = None
        self.voice_available = VOICE_AVAILABLE
        if self.voice_available:
            try:
                self.voice_engine = pyttsx3.init()
                self.voice_engine.setProperty('rate', 150)  # Speed
                self.voice_engine.setProperty('volume', 0.8)  # Volume
            except Exception as e:
                print(f"Could not initialize voice engine: {e}")
                self.voice_available = False
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("AI Gaze-Controlled Mouse")
        self.root.geometry("550x650")
        self.root.resizable(True, True)
        
        # Set window icon (optional)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Configure style
        self.setup_styles()
        
        # Create widgets
        self.create_widgets()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configure ttk styles for better appearance."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button styles
        style.configure('Start.TButton', 
                       font=('Arial', 12, 'bold'),
                       foreground='green')
        style.configure('Pause.TButton', 
                       font=('Arial', 12, 'bold'),
                       foreground='orange')
        style.configure('Exit.TButton', 
                       font=('Arial', 12, 'bold'),
                       foreground='red')
    
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#2C3E50', height=80)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="🎯 AI Gaze-Controlled Mouse",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2C3E50'
        )
        title_label.pack(pady=20)
        
        # Main Content Frame
        content_frame = tk.Frame(self.root, bg='#ECF0F1')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Status Display
        status_frame = tk.LabelFrame(
            content_frame,
            text="Status",
            font=('Arial', 11, 'bold'),
            bg='#ECF0F1',
            fg='#2C3E50'
        )
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to Start",
            font=('Arial', 14, 'bold'),
            fg='blue',
            bg='#ECF0F1',
            pady=10
        )
        self.status_label.pack()
        
        # Instructions
        instructions_frame = tk.LabelFrame(
            content_frame,
            text="Instructions",
            font=('Arial', 11, 'bold'),
            bg='#ECF0F1',
            fg='#2C3E50'
        )
        instructions_frame.pack(fill=tk.X, pady=(0, 15))
        
        instructions_text = """
• Click "Calibrate Gaze" FIRST (required!)
• Follow on-screen targets and blink
• Then click "Start Tracking" to begin
• Look where you want the cursor to go
• Keep your HEAD STILL, move only EYES
• DOUBLE BLINK (both eyes) for RIGHT CLICK
• TRIPLE BLINK (both eyes) for LEFT CLICK
• Press 'Q' to hide camera window
        """
        
        instructions_label = tk.Label(
            instructions_frame,
            text=instructions_text,
            font=('Arial', 10),
            bg='#ECF0F1',
            fg='#34495E',
            justify=tk.LEFT
        )
        instructions_label.pack(padx=10, pady=10)
        
        # Button Frame
        button_frame = tk.Frame(content_frame, bg='#ECF0F1')
        button_frame.pack(fill=tk.X)
        
        # Calibrate Button (Primary action)
        self.calibrate_button = ttk.Button(
            button_frame,
            text="🎯 Calibrate Gaze",
            command=self.on_calibrate
        )
        self.calibrate_button.pack(fill=tk.X, pady=(0, 10))
        
        # Control Buttons Row
        control_frame = tk.Frame(button_frame, bg='#ECF0F1')
        control_frame.pack(fill=tk.X)
        
        # Start Button
        self.start_button = ttk.Button(
            control_frame,
            text="▶ Start Tracking",
            style='Start.TButton',
            command=self.on_start
        )
        self.start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Pause Button
        self.pause_button = ttk.Button(
            control_frame,
            text="⏸ Pause",
            style='Pause.TButton',
            command=self.on_pause,
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Exit Button
        self.exit_button = ttk.Button(
            control_frame,
            text="❌ Exit",
            style='Exit.TButton',
            command=self.on_exit
        )
        self.exit_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Calibration Status Label
        self.calibration_status = tk.Label(
            content_frame,
            text="⚠️ Not Calibrated - Please calibrate first",
            font=('Arial', 10, 'bold'),
            fg='red',
            bg='#ECF0F1'
        )
        self.calibration_status.pack(pady=(10, 0))
    
    def on_calibrate(self):
        """Handle Calibrate button click."""
        self.calibrate_button.config(state=tk.DISABLED)
        self.update_status("Calibrating...", "orange")
        self.speak("Starting gaze calibration")
        self.calibrate_callback()
    
    def on_start(self):
        """Handle Start button click."""
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.calibrate_button.config(state=tk.DISABLED)
        self.speak("Tracking started")
        self.start_callback()
    
    def on_pause(self):
        """Handle Pause button click."""
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.calibrate_button.config(state=tk.NORMAL)
        self.speak("Tracking paused")
        self.pause_callback()
    
    def on_exit(self):
        """Handle Exit button click."""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.speak("Goodbye")
            self.exit_callback()
    
    def on_closing(self):
        """Handle window close event."""
        self.on_exit()
    
    def update_calibration_status(self, is_calibrated):
        """
        Update the calibration status display.
        
        Args:
            is_calibrated: Boolean indicating if system is calibrated
        """
        if is_calibrated:
            self.calibration_status.config(
                text="✓ Calibrated - Ready to track",
                fg='green'
            )
            self.calibrate_button.config(state=tk.NORMAL)
        else:
            self.calibration_status.config(
                text="⚠️ Not Calibrated - Please calibrate first",
                fg='red'
            )
        self.root.update_idletasks()
    
    def update_status(self, status_text, color="blue"):
        """
        Update the status display.
        
        Args:
            status_text: Text to display
            color: Text color
        """
        self.status_label.config(text=status_text, fg=color)
        self.root.update_idletasks()
    
    def speak(self, text):
        """
        Speak text using text-to-speech if available.
        
        Args:
            text: Text to speak
        """
        if self.voice_engine and self.voice_available:
            try:
                self.voice_engine.say(text)
                self.voice_engine.runAndWait()
            except Exception as e:
                print(f"Voice error: {e}")
    
    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()
    
    def destroy(self):
        """Destroy the GUI window."""
        try:
            self.root.destroy()
        except:
            pass


# Test the GUI independently
if __name__ == "__main__":
    def test_start():
        print("Start clicked")
    
    def test_pause():
        print("Pause clicked")
    
    def test_exit():
        print("Exit clicked")
        sys.exit(0)
    
    gui = EyeMouseGUI(test_start, test_pause, test_exit)
    gui.run()
