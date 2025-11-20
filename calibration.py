"""
Calibration Module
Handles gaze calibration for accurate eye tracking.
Captures user's gaze range by showing targets at screen corners.
"""

import cv2
import numpy as np
import time
from screeninfo import get_monitors

class GazeCalibrator:
    """Manages gaze calibration process for accurate cursor control."""
    
    def __init__(self, blink_detector):
        """
        Initialize the calibrator.
        
        Args:
            blink_detector: BlinkDetector instance for detecting calibration blinks
        """
        self.blink_detector = blink_detector
        
        # Get screen dimensions
        try:
            monitor = get_monitors()[0]
            self.screen_width = monitor.width
            self.screen_height = monitor.height
        except:
            self.screen_width = 1920
            self.screen_height = 1080
        
        # Calibration data
        self.min_x_ratio = 0.0
        self.max_x_ratio = 1.0
        self.min_y_ratio = 0.0
        self.max_y_ratio = 1.0
        
        # Calibration points (screen positions and labels)
        self.calibration_points = [
            ((0.1, 0.1), "Top-Left"),
            ((0.9, 0.1), "Top-Right"),
            ((0.9, 0.9), "Bottom-Right"),
            ((0.1, 0.9), "Bottom-Left"),
            ((0.5, 0.5), "Center")
        ]
        
        # Collected gaze data
        self.calibration_data = []
        
        self.is_calibrated = False
    
    def start_calibration(self, cap, eye_tracker):
        """
        Start the calibration process.
        
        Args:
            cap: OpenCV video capture object
            eye_tracker: EyeTracker instance
        
        Returns:
            bool: True if calibration successful, False otherwise
        """
        print("\n" + "="*60)
        print("GAZE CALIBRATION MODE")
        print("="*60)
        print("Instructions:")
        print("1. Look at each target circle that appears")
        print("2. Keep your head still, only move your eyes")
        print("3. Blink when you're looking at the target")
        print("4. We'll calibrate 5 points: corners and center")
        print("="*60 + "\n")
        
        self.calibration_data = []
        
        for point_idx, (screen_pos, label) in enumerate(self.calibration_points):
            print(f"Calibration Point {point_idx + 1}/5: {label}")
            
            # Collect gaze data for this point
            gaze_ratio = self._capture_calibration_point(cap, eye_tracker, screen_pos, label)
            
            if gaze_ratio is None:
                print("Calibration failed or cancelled.")
                return False
            
            self.calibration_data.append({
                'screen_pos': screen_pos,
                'gaze_ratio': gaze_ratio,
                'label': label
            })
            
            print(f"✓ Captured {label}: Gaze ratio = ({gaze_ratio[0]:.3f}, {gaze_ratio[1]:.3f})")
            time.sleep(0.5)
        
        # Calculate calibration bounds
        self._calculate_calibration_bounds()
        
        self.is_calibrated = True
        print("\n" + "="*60)
        print("✓ CALIBRATION COMPLETE!")
        print(f"X Range: {self.min_x_ratio:.3f} to {self.max_x_ratio:.3f}")
        print(f"Y Range: {self.min_y_ratio:.3f} to {self.max_y_ratio:.3f}")
        print("="*60 + "\n")
        
        return True
    
    def _capture_calibration_point(self, cap, eye_tracker, screen_pos, label):
        """
        Capture gaze data for a single calibration point.
        
        Args:
            cap: Video capture object
            eye_tracker: EyeTracker instance
            screen_pos: (x, y) normalized screen position
            label: String label for the point
        
        Returns:
            tuple: (gaze_x, gaze_y) ratio or None if failed
        """
        # Calculate pixel position
        target_x = int(screen_pos[0] * self.screen_width)
        target_y = int(screen_pos[1] * self.screen_height)
        
        gaze_samples = []
        blink_detected = False
        start_time = time.time()
        timeout = 15  # 15 seconds timeout per point
        
        while not blink_detected and (time.time() - start_time) < timeout:
            ret, frame = cap.read()
            if not ret:
                continue
            
            frame = cv2.flip(frame, 1)
            
            # Process frame for eye tracking
            frame, landmarks = eye_tracker.process_frame(frame)
            
            if landmarks:
                # Get current gaze position
                gaze_ratio = eye_tracker.get_eye_position(landmarks, frame.shape)
                
                if gaze_ratio:
                    gaze_samples.append(gaze_ratio)
                    
                    # Keep only recent samples (last 30 frames = ~1 second)
                    if len(gaze_samples) > 30:
                        gaze_samples.pop(0)
                
                # Check for blink to confirm calibration point
                blink_actions = self.blink_detector.detect_blink(landmarks, frame.shape)
                if blink_actions.get('left_click') or blink_actions.get('right_click'):
                    if len(gaze_samples) >= 10:  # Need at least 10 samples
                        blink_detected = True
            
            # Draw calibration interface
            self._draw_calibration_ui(frame, screen_pos, label, len(gaze_samples))
            
            # Create fullscreen calibration window
            cv2.namedWindow('Calibration', cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty('Calibration', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            
            # Create black background at screen resolution
            calibration_screen = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)
            
            # Draw target circle
            cv2.circle(calibration_screen, (target_x, target_y), 30, (0, 255, 0), -1)
            cv2.circle(calibration_screen, (target_x, target_y), 35, (255, 255, 255), 3)
            
            # Draw instructions
            instruction_text = f"Look at the {label} target and BLINK"
            cv2.putText(calibration_screen, instruction_text, (50, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            samples_text = f"Samples: {len(gaze_samples)}/10 (Blink to confirm)"
            cv2.putText(calibration_screen, samples_text, (50, 100),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            point_text = f"Point {self.calibration_points.index((screen_pos, label)) + 1}/{len(self.calibration_points)}"
            cv2.putText(calibration_screen, point_text, (50, 150),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            # Show camera feed in corner
            small_frame = cv2.resize(frame, (320, 240))
            calibration_screen[20:260, self.screen_width-340:self.screen_width-20] = small_frame
            
            cv2.imshow('Calibration', calibration_screen)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # Q or ESC to cancel
                cv2.destroyWindow('Calibration')
                return None
        
        cv2.destroyWindow('Calibration')
        
        if not blink_detected:
            print(f"Timeout waiting for blink at {label}")
            return None
        
        # Average the collected gaze samples
        avg_gaze_x = np.mean([s[0] for s in gaze_samples])
        avg_gaze_y = np.mean([s[1] for s in gaze_samples])
        
        return (avg_gaze_x, avg_gaze_y)
    
    def _draw_calibration_ui(self, frame, screen_pos, label, sample_count):
        """Draw calibration UI elements on the camera frame."""
        h, w = frame.shape[:2]
        
        # Draw instructions
        cv2.putText(frame, f"Look at: {label}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Samples: {sample_count}/10", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(frame, "Blink to confirm", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    def _calculate_calibration_bounds(self):
        """Calculate min/max gaze ratios from collected calibration data."""
        if len(self.calibration_data) < 4:
            print("Warning: Insufficient calibration data. Using defaults.")
            return
        
        # Extract all gaze ratios
        all_x_ratios = [data['gaze_ratio'][0] for data in self.calibration_data]
        all_y_ratios = [data['gaze_ratio'][1] for data in self.calibration_data]
        
        # Find min and max with some margin for comfort
        margin_x = 0.05
        margin_y = 0.05
        
        self.min_x_ratio = max(0.0, min(all_x_ratios) - margin_x)
        self.max_x_ratio = min(1.0, max(all_x_ratios) + margin_x)
        self.min_y_ratio = max(0.0, min(all_y_ratios) - margin_y)
        self.max_y_ratio = min(1.0, max(all_y_ratios) + margin_y)
        
        # Ensure valid range
        if self.max_x_ratio - self.min_x_ratio < 0.1:
            self.min_x_ratio = 0.2
            self.max_x_ratio = 0.8
        
        if self.max_y_ratio - self.min_y_ratio < 0.1:
            self.min_y_ratio = 0.2
            self.max_y_ratio = 0.8
    
    def get_calibration_data(self):
        """
        Get the calibration bounds.
        
        Returns:
            dict: Calibration parameters or None if not calibrated
        """
        if not self.is_calibrated:
            return None
        
        return {
            'min_x': self.min_x_ratio,
            'max_x': self.max_x_ratio,
            'min_y': self.min_y_ratio,
            'max_y': self.max_y_ratio,
            'calibrated': True
        }
    
    def load_calibration(self, calibration_data):
        """
        Load previously saved calibration data.
        
        Args:
            calibration_data: Dictionary with calibration parameters
        """
        if calibration_data and calibration_data.get('calibrated'):
            self.min_x_ratio = calibration_data['min_x']
            self.max_x_ratio = calibration_data['max_x']
            self.min_y_ratio = calibration_data['min_y']
            self.max_y_ratio = calibration_data['max_y']
            self.is_calibrated = True
            print("Calibration data loaded successfully.")
        else:
            print("No valid calibration data to load.")
    
    def reset_calibration(self):
        """Reset calibration to defaults."""
        self.min_x_ratio = 0.0
        self.max_x_ratio = 1.0
        self.min_y_ratio = 0.0
        self.max_y_ratio = 1.0
        self.calibration_data = []
        self.is_calibrated = False
        print("Calibration reset to defaults.")
