"""
Blink Detector Module
Implements Eye Aspect Ratio (EAR) algorithm to detect blinks.
Triggers mouse clicks based on left/right eye blinks.
"""

import numpy as np
import time

class BlinkDetector:
    """Detects eye blinks using Eye Aspect Ratio (EAR) algorithm."""
    
    # MediaPipe landmark indices for eye points
    # Left eye: [33, 160, 158, 133, 153, 144]
    # Right eye: [362, 385, 387, 263, 373, 380]
    
    def __init__(self):
        """Initialize blink detector with thresholds and state tracking."""
        # EAR threshold (lower = more sensitive to blinks)
        self.ear_threshold = 0.20
        
        # Minimum consecutive frames for valid blink
        self.min_blink_frames = 2
        
        # State tracking for BOTH EYES blink detection
        self.both_eyes_blink_counter = 0
        
        # Blink sequence tracking for double/triple/quadruple blinks
        self.blink_sequence = []
        self.last_blink_time = 0
        self.blink_sequence_timeout = 1.5  # Time window for detecting multiple blinks (increased for 4-5 blinks)
        self.between_blink_min = 0.1  # Minimum time between blinks in a sequence
        self.between_blink_max = 0.7  # Maximum time between blinks in a sequence
        
        # Debouncing
        self.last_action_time = 0
        self.action_cooldown = 1.0  # Cooldown after any action (click/scroll/drag)
        
        # State for detecting blink completion
        self.in_blink = False
        self.blink_start_time = 0
    
    def calculate_ear(self, eye_landmarks):
        """
        Calculate Eye Aspect Ratio (EAR) for an eye.
        
        EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
        where p1-p6 are eye landmark points
        
        Args:
            eye_landmarks: Array of eye landmark coordinates [[x1,y1], [x2,y2], ...]
        
        Returns:
            float: Eye Aspect Ratio value
        """
        if len(eye_landmarks) < 6:
            return 1.0
        
        # Vertical distances
        v1 = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        v2 = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
        
        # Horizontal distance
        h = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
        
        # Avoid division by zero
        if h == 0:
            return 1.0
        
        # Calculate EAR
        ear = (v1 + v2) / (2.0 * h)
        
        return ear
    
    def detect_blink(self, face_landmarks, frame_shape):
        """
        Detect blinks from face landmarks and return actions.
        
        BLINK PATTERNS:
        - 2 blinks = RIGHT CLICK
        - 3 blinks = LEFT CLICK
        - 4 blinks = DRAG TOGGLE (start/stop drag)
        - 5 blinks = MIDDLE CLICK
        
        Args:
            face_landmarks: MediaPipe face landmarks
            frame_shape: Shape of the frame (height, width, channels)
        
        Returns:
            dict: {'left_click': bool, 'right_click': bool, 'scroll_up': bool, 
                   'scroll_down': bool, 'drag_toggle': bool, 'middle_click': bool}
        """
        default_result = {
            'left_click': False, 'right_click': False,
            'scroll_up': False, 'scroll_down': False,
            'drag_toggle': False, 'middle_click': False
        }
        
        if not face_landmarks:
            return default_result
        
        h, w = frame_shape[:2]
        
        # Extract eye landmarks
        left_eye_indices = [33, 160, 158, 133, 153, 144]
        right_eye_indices = [362, 385, 387, 263, 373, 380]
        
        left_eye = np.array([(face_landmarks.landmark[i].x * w,
                              face_landmarks.landmark[i].y * h)
                             for i in left_eye_indices])
        
        right_eye = np.array([(face_landmarks.landmark[i].x * w,
                               face_landmarks.landmark[i].y * h)
                              for i in right_eye_indices])
        
        # Calculate EAR for both eyes
        left_ear = self.calculate_ear(left_eye)
        right_ear = self.calculate_ear(right_eye)
        
        # Average EAR (both eyes must be closed for blink)
        avg_ear = (left_ear + right_ear) / 2
        
        current_time = time.time()
        
        # Detect when BOTH eyes are closed
        if avg_ear < self.ear_threshold:
            if not self.in_blink:
                # Start of a new blink
                self.in_blink = True
                self.blink_start_time = current_time
            self.both_eyes_blink_counter += 1
        else:
            # Eyes are open
            if self.in_blink and self.both_eyes_blink_counter >= self.min_blink_frames:
                # Valid blink completed
                self.in_blink = False
                self.both_eyes_blink_counter = 0
                
                # Add blink to sequence
                self._add_blink_to_sequence(current_time)
            else:
                self.in_blink = False
                self.both_eyes_blink_counter = 0
        
        # Check for blink patterns (2, 3, 4, or 5 blinks)
        result = self._check_blink_sequence(current_time)
        
        return result
    
    def _add_blink_to_sequence(self, current_time):
        """Add a completed blink to the sequence."""
        # Clean old blinks outside the time window
        self.blink_sequence = [t for t in self.blink_sequence 
                               if current_time - t < self.blink_sequence_timeout]
        
        # Check if enough time has passed since last blink
        if len(self.blink_sequence) == 0 or \
           (current_time - self.blink_sequence[-1]) >= self.between_blink_min:
            self.blink_sequence.append(current_time)
            print(f"Blink detected! Sequence count: {len(self.blink_sequence)}")
    
    def _check_blink_sequence(self, current_time):
        """
        Check if the blink sequence matches a pattern.
        
        Returns:
            dict: {'left_click': bool, 'right_click': bool, 'scroll_up': bool, 
                   'scroll_down': bool, 'drag_toggle': bool, 'middle_click': bool}
        """
        # Clean old blinks
        self.blink_sequence = [t for t in self.blink_sequence 
                               if current_time - t < self.blink_sequence_timeout]
        
        # Check cooldown
        if current_time - self.last_action_time < self.action_cooldown:
            return {
                'left_click': False, 'right_click': False, 
                'scroll_up': False, 'scroll_down': False,
                'drag_toggle': False, 'middle_click': False
            }
        
        result = {
            'left_click': False, 'right_click': False,
            'scroll_up': False, 'scroll_down': False,
            'drag_toggle': False, 'middle_click': False
        }
        
        # Check for 5 blinks (MIDDLE CLICK)
        if len(self.blink_sequence) >= 5:
            time_span = self.blink_sequence[-1] - self.blink_sequence[-5]
            if time_span <= self.blink_sequence_timeout:
                result['middle_click'] = True
                self.blink_sequence = []
                self.last_action_time = current_time
                print("✓ 5 BLINKS DETECTED -> MIDDLE CLICK")
                return result
        
        # Check for 4 blinks (DRAG TOGGLE - start/stop drag)
        if len(self.blink_sequence) >= 4:
            time_span = self.blink_sequence[-1] - self.blink_sequence[-4]
            if time_span <= self.blink_sequence_timeout:
                result['drag_toggle'] = True
                self.blink_sequence = []
                self.last_action_time = current_time
                print("✓ 4 BLINKS DETECTED -> DRAG TOGGLE")
                return result
        
        # Check for triple blink (LEFT CLICK)
        if len(self.blink_sequence) >= 3:
            time_span = self.blink_sequence[-1] - self.blink_sequence[-3]
            if time_span <= self.blink_sequence_timeout:
                # Wait to see if it's actually 4 or 5 blinks
                if current_time - self.blink_sequence[-1] > 0.5:
                    result['left_click'] = True
                    self.blink_sequence = []
                    self.last_action_time = current_time
                    print("✓ 3 BLINKS DETECTED -> LEFT CLICK")
                    return result
        
        # Check for double blink (RIGHT CLICK)
        elif len(self.blink_sequence) >= 2:
            time_between = self.blink_sequence[-1] - self.blink_sequence[-2]
            if self.between_blink_min <= time_between <= self.between_blink_max:
                # Wait to see if it's actually a triple blink
                if current_time - self.blink_sequence[-1] > 0.5:
                    result['right_click'] = True
                    self.blink_sequence = []
                    self.last_action_time = current_time
                    print("✓ 2 BLINKS DETECTED -> RIGHT CLICK")
                    return result
        
        return result
    
    def detect_double_blink(self, face_landmarks, frame_shape):
        """
        Deprecated: Now using detect_blink() for all blink patterns.
        Kept for backward compatibility.
        """
        return False
    
    def set_threshold(self, threshold):
        """
        Set EAR threshold for blink detection.
        
        Args:
            threshold: EAR threshold value (typically 0.15-0.25)
        """
        self.ear_threshold = threshold
        print(f"Blink threshold updated: {threshold}")
    
    def enable_double_blink_detection(self, enable=True):
        """
        Enable or disable double blink detection.
        
        Args:
            enable: Boolean to enable/disable double blink detection
        """
        self.enable_double_blink = enable
        print(f"Double blink detection: {'enabled' if enable else 'disabled'}")
    
    def reset(self):
        """Reset blink detection state."""
        self.left_blink_counter = 0
        self.right_blink_counter = 0
        self.left_blink_detected = False
        self.right_blink_detected = False
