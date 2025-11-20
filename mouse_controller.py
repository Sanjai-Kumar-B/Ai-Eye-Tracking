"""
Mouse Controller Module
Handles cursor movement and click actions using pyautogui.
Converts eye coordinates to screen coordinates with smoothing.
"""

import pyautogui
import numpy as np
from screeninfo import get_monitors

class MouseController:
    """Controls mouse cursor movement and clicks."""
    
    def __init__(self):
        """Initialize mouse controller with screen dimensions and settings."""
        # Get screen dimensions
        try:
            monitor = get_monitors()[0]
            self.screen_width = monitor.width
            self.screen_height = monitor.height
        except:
            # Fallback to pyautogui's screen size detection
            self.screen_width, self.screen_height = pyautogui.size()
        
        print(f"Screen resolution: {self.screen_width}x{self.screen_height}")
        
        # PyAutoGUI settings
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = 0.01  # Small pause between actions
        
        # Movement settings for GAZE TRACKING
        self.smoothing_factor = 0.5  # Balanced smoothing for responsive gaze tracking
        self.prev_position = None
        
        # Calibration data (loaded from calibrator)
        self.calibration_data = None
        self.is_calibrated = False
        
        # Default calibration bounds (will be overridden after calibration)
        self.min_x_ratio = 0.0
        self.max_x_ratio = 1.0
        self.min_y_ratio = 0.0
        self.max_y_ratio = 1.0
        
        # Click debouncing
        self.last_click_time = {'left': 0, 'right': 0}
        self.click_cooldown = 0.5  # Minimum time between clicks (seconds)
    
    def load_calibration(self, calibration_data):
        """
        Load calibration data from the calibrator.
        
        Args:
            calibration_data: Dictionary with min_x, max_x, min_y, max_y, calibrated
        """
        if calibration_data and calibration_data.get('calibrated'):
            self.min_x_ratio = calibration_data['min_x']
            self.max_x_ratio = calibration_data['max_x']
            self.min_y_ratio = calibration_data['min_y']
            self.max_y_ratio = calibration_data['max_y']
            self.is_calibrated = True
            self.calibration_data = calibration_data
            print(f"Mouse controller calibration loaded:")
            print(f"  X range: {self.min_x_ratio:.3f} to {self.max_x_ratio:.3f}")
            print(f"  Y range: {self.min_y_ratio:.3f} to {self.max_y_ratio:.3f}")
        else:
            print("Warning: No calibration data loaded. Using defaults.")
            self.is_calibrated = False
    
    def move_cursor(self, gaze_ratio):
        """
        Move cursor based on calibrated gaze position (GAZE TRACKING MODE).
        
        This function maps the user's gaze ratio (relative eye position) to screen
        coordinates using the calibration data. The mapping formula is:
        
        screen_x_normalized = (gaze_x - min_x) / (max_x - min_x)
        
        Args:
            gaze_ratio: Tuple of (gaze_x_ratio, gaze_y_ratio) from eye tracker
                        where ratios represent relative position within eye socket
        """
        if not gaze_ratio:
            return
        
        gaze_x, gaze_y = gaze_ratio
        
        # Map gaze ratios to screen coordinates using calibration
        if self.is_calibrated:
            # Normalize gaze position to 0-1 range using calibration bounds
            screen_x_normalized = (gaze_x - self.min_x_ratio) / (self.max_x_ratio - self.min_x_ratio)
            screen_y_normalized = (gaze_y - self.min_y_ratio) / (self.max_y_ratio - self.min_y_ratio)
        else:
            # No calibration: use raw gaze ratios (less accurate)
            print("Warning: Operating without calibration. Please calibrate for better accuracy.")
            screen_x_normalized = gaze_x
            screen_y_normalized = gaze_y
        
        # Clamp to screen bounds (0-1 range)
        screen_x_normalized = np.clip(screen_x_normalized, 0, 1)
        screen_y_normalized = np.clip(screen_y_normalized, 0, 1)
        
        # Convert to pixel coordinates
        target_x = int(screen_x_normalized * self.screen_width)
        target_y = int(screen_y_normalized * self.screen_height)
        
        # Apply smoothing to compensate for saccades (rapid eye movements)
        if self.prev_position:
            prev_x, prev_y = self.prev_position
            target_x = int(self.smoothing_factor * prev_x + (1 - self.smoothing_factor) * target_x)
            target_y = int(self.smoothing_factor * prev_y + (1 - self.smoothing_factor) * target_y)
        
        self.prev_position = (target_x, target_y)
        
        # Move cursor
        try:
            pyautogui.moveTo(target_x, target_y, duration=0.05)
        except Exception as e:
            print(f"Error moving cursor: {e}")
    
    def left_click(self):
        """Perform a left mouse click with debouncing."""
        import time
        current_time = time.time()
        
        if current_time - self.last_click_time['left'] > self.click_cooldown:
            try:
                pyautogui.click()
                self.last_click_time['left'] = current_time
                print("Left click performed")
            except Exception as e:
                print(f"Error performing left click: {e}")
    
    def right_click(self):
        """Perform a right mouse click with debouncing."""
        import time
        current_time = time.time()
        
        if current_time - self.last_click_time['right'] > self.click_cooldown:
            try:
                pyautogui.rightClick()
                self.last_click_time['right'] = current_time
                print("Right click performed")
            except Exception as e:
                print(f"Error performing right click: {e}")
    
    def double_click(self):
        """Perform a double click."""
        try:
            pyautogui.doubleClick()
            print("Double click performed")
        except Exception as e:
            print(f"Error performing double click: {e}")
    
    def set_smoothing(self, smoothing_factor):
        """
        Adjust cursor smoothing.
        
        For gaze tracking, higher smoothing (0.8-0.9) is recommended to compensate
        for natural eye jitter and saccades.
        
        Args:
            smoothing_factor: Smoothing factor (0-1, higher = more smoothing)
        """
        self.smoothing_factor = np.clip(smoothing_factor, 0, 1)
        print(f"Smoothing updated: {self.smoothing_factor}")
    
    def get_calibration_status(self):
        """
        Get calibration status.
        
        Returns:
            bool: True if calibrated, False otherwise
        """
        return self.is_calibrated
