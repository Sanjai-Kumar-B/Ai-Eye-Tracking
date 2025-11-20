"""
Gesture Detector Module
Detects gaze-based gestures for scrolling and other actions.
Provides alternative control methods beyond blink patterns.
"""

import time

class GestureDetector:
    """Detects gaze-based gestures like edge dwelling for scrolling."""
    
    def __init__(self, screen_width, screen_height):
        """
        Initialize gesture detector.
        
        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Edge scroll settings
        self.edge_threshold = 50  # Pixels from edge to trigger scroll
        self.dwell_time = 0.8  # Seconds to dwell before scrolling
        self.scroll_interval = 0.3  # Seconds between scroll actions
        
        # State tracking
        self.edge_dwell_start = None
        self.last_scroll_time = 0
        self.current_edge = None  # 'top', 'bottom', 'left', 'right', or None
    
    def detect_edge_scroll(self, cursor_x, cursor_y):
        """
        Detect if cursor is dwelling at screen edge for scrolling.
        
        Args:
            cursor_x: Current cursor X position
            cursor_y: Current cursor Y position
        
        Returns:
            str: 'scroll_up', 'scroll_down', 'scroll_left', 'scroll_right', or None
        """
        current_time = time.time()
        edge = None
        
        # Detect which edge cursor is near
        if cursor_y <= self.edge_threshold:
            edge = 'top'
        elif cursor_y >= self.screen_height - self.edge_threshold:
            edge = 'bottom'
        elif cursor_x <= self.edge_threshold:
            edge = 'left'
        elif cursor_x >= self.screen_width - self.edge_threshold:
            edge = 'right'
        
        # Check if edge changed
        if edge != self.current_edge:
            self.current_edge = edge
            self.edge_dwell_start = current_time if edge else None
            return None
        
        # If at an edge and dwelling
        if edge and self.edge_dwell_start:
            dwell_duration = current_time - self.edge_dwell_start
            
            # Check if dwelled long enough and scroll interval passed
            if dwell_duration >= self.dwell_time:
                if current_time - self.last_scroll_time >= self.scroll_interval:
                    self.last_scroll_time = current_time
                    
                    # Return scroll action based on edge
                    if edge == 'top':
                        return 'scroll_up'
                    elif edge == 'bottom':
                        return 'scroll_down'
                    elif edge == 'left':
                        return 'scroll_left'
                    elif edge == 'right':
                        return 'scroll_right'
        
        return None
    
    def reset(self):
        """Reset gesture detection state."""
        self.edge_dwell_start = None
        self.current_edge = None
    
    def set_edge_threshold(self, threshold):
        """
        Set edge detection threshold.
        
        Args:
            threshold: Pixels from edge (default: 50)
        """
        self.edge_threshold = threshold
    
    def set_dwell_time(self, dwell_time):
        """
        Set time required to dwell before triggering action.
        
        Args:
            dwell_time: Seconds to dwell (default: 0.8)
        """
        self.dwell_time = dwell_time
