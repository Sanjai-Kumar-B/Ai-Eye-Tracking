"""
Eye Tracker Module
Uses MediaPipe FaceMesh to detect eyes and facial landmarks.
Tracks eye position and returns coordinates for mouse control.
"""

import cv2
import mediapipe as mp
import numpy as np

class EyeTracker:
    """Handles eye detection and tracking using MediaPipe FaceMesh."""
    
    # MediaPipe landmark indices for eyes
    LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
    LEFT_IRIS_INDICES = [468, 469, 470, 471, 472]
    RIGHT_IRIS_INDICES = [473, 474, 475, 476, 477]
    
    def __init__(self):
        """Initialize MediaPipe FaceMesh with optimized settings."""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,  # Enable iris landmarks
            min_detection_confidence=0.7,  # Increased for better stability
            min_tracking_confidence=0.7    # Increased for better stability
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        
        # For smoothing eye position with multiple frames
        self.prev_eye_position = None
        self.smoothing_factor = 0.3  # Lower for more responsive gaze
        
        # Multi-frame averaging for stability
        self.gaze_history = []
        self.history_size = 5  # Average last 5 frames
    
    def process_frame(self, frame):
        """
        Process a video frame to detect facial landmarks.
        
        Args:
            frame: OpenCV frame (BGR format)
        
        Returns:
            tuple: (annotated_frame, landmarks) where landmarks is None if no face detected
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame
        results = self.face_mesh.process(rgb_frame)
        
        # Draw landmarks on frame
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Draw the full face mesh
                self.mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing.DrawingSpec(
                        color=(80, 110, 10), thickness=1, circle_radius=1
                    )
                )
                
                # Draw eye contours
                self._draw_eye_landmarks(frame, face_landmarks)
                
                return frame, face_landmarks
        
        return frame, None
    
    def _draw_eye_landmarks(self, frame, face_landmarks):
        """Draw eye and iris landmarks on the frame."""
        h, w = frame.shape[:2]
        
        # Draw left eye
        for idx in self.LEFT_EYE_INDICES:
            landmark = face_landmarks.landmark[idx]
            x, y = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        
        # Draw right eye
        for idx in self.RIGHT_EYE_INDICES:
            landmark = face_landmarks.landmark[idx]
            x, y = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        
        # Draw left iris
        for idx in self.LEFT_IRIS_INDICES:
            landmark = face_landmarks.landmark[idx]
            x, y = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)
        
        # Draw right iris
        for idx in self.RIGHT_IRIS_INDICES:
            landmark = face_landmarks.landmark[idx]
            x, y = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)
    
    def get_eye_position(self, face_landmarks, frame_shape):
        """
        Calculate the relative gaze position within the eye socket (IMPROVED ACCURACY).
        
        Uses enhanced algorithm with better landmark selection and multi-frame averaging.
        
        Args:
            face_landmarks: MediaPipe face landmarks
            frame_shape: Shape of the frame (height, width, channels)
        
        Returns:
            tuple: (gaze_x_ratio, gaze_y_ratio) where:
                   - gaze_x_ratio: 0.0 (looking left) to 1.0 (looking right)
                   - gaze_y_ratio: 0.0 (looking up) to 1.0 (looking down)
                   Returns None if no face detected
        """
        if not face_landmarks:
            return None
        
        # Calculate gaze ratios for both eyes and average them
        left_gaze = self._calculate_single_eye_gaze(face_landmarks, is_left_eye=True)
        right_gaze = self._calculate_single_eye_gaze(face_landmarks, is_left_eye=False)
        
        if left_gaze is None or right_gaze is None:
            return None
        
        # Average both eyes for more stable gaze tracking
        avg_gaze_x = (left_gaze[0] + right_gaze[0]) / 2
        avg_gaze_y = (left_gaze[1] + right_gaze[1]) / 2
        
        # Add to history for multi-frame averaging
        self.gaze_history.append((avg_gaze_x, avg_gaze_y))
        if len(self.gaze_history) > self.history_size:
            self.gaze_history.pop(0)
        
        # Calculate average from history
        if len(self.gaze_history) > 0:
            avg_gaze_x = np.mean([g[0] for g in self.gaze_history])
            avg_gaze_y = np.mean([g[1] for g in self.gaze_history])
        
        # Apply exponential smoothing
        if self.prev_eye_position is not None:
            avg_gaze_x = self.smoothing_factor * self.prev_eye_position[0] + (1 - self.smoothing_factor) * avg_gaze_x
            avg_gaze_y = self.smoothing_factor * self.prev_eye_position[1] + (1 - self.smoothing_factor) * avg_gaze_y
        
        self.prev_eye_position = (avg_gaze_x, avg_gaze_y)
        
        return (avg_gaze_x, avg_gaze_y)
    
    def _calculate_single_eye_gaze(self, face_landmarks, is_left_eye=True):
        """
        Calculate the relative gaze position for a single eye (IMPROVED ACCURACY).
        
        Uses enhanced landmark selection with weighted center calculation.
        
        Args:
            face_landmarks: MediaPipe face landmarks
            is_left_eye: True for left eye, False for right eye
        
        Returns:
            tuple: (gaze_x_ratio, gaze_y_ratio) or None
        """
        if is_left_eye:
            # Left eye landmarks (more precise selection)
            iris_indices = self.LEFT_IRIS_INDICES
            inner_corner = 133  # Inner corner (closest to nose)
            outer_corner = 33   # Outer corner (away from nose)
            top_lid = 159       # Top eyelid center
            bottom_lid = 145    # Bottom eyelid center
            # Additional landmarks for better boundary detection
            upper_points = [159, 160, 161]
            lower_points = [145, 144, 153]
        else:
            # Right eye landmarks
            iris_indices = self.RIGHT_IRIS_INDICES
            inner_corner = 362  # Inner corner (closest to nose)
            outer_corner = 263  # Outer corner (away from nose)
            top_lid = 386       # Top eyelid center
            bottom_lid = 374    # Bottom eyelid center
            upper_points = [386, 385, 387]
            lower_points = [374, 373, 380]
        
        # Get iris center position (weighted average for better accuracy)
        iris_x = np.mean([face_landmarks.landmark[i].x for i in iris_indices])
        iris_y = np.mean([face_landmarks.landmark[i].y for i in iris_indices])
        
        # Get eye boundary positions with averaging
        inner_x = face_landmarks.landmark[inner_corner].x
        outer_x = face_landmarks.landmark[outer_corner].x
        
        # Average top and bottom points for more stable boundaries
        top_y = np.mean([face_landmarks.landmark[i].y for i in upper_points])
        bottom_y = np.mean([face_landmarks.landmark[i].y for i in lower_points])
        
        # Calculate horizontal gaze ratio with improved scaling
        eye_width = abs(outer_x - inner_x)
        if eye_width > 0:
            if is_left_eye:
                gaze_x_ratio = (iris_x - inner_x) / eye_width
            else:
                gaze_x_ratio = (iris_x - inner_x) / eye_width
            
            # Apply non-linear scaling for better edge detection
            # This helps cursor reach screen edges more easily
            gaze_x_ratio = self._apply_nonlinear_scale(gaze_x_ratio)
        else:
            gaze_x_ratio = 0.5
        
        # Calculate vertical gaze ratio with improved scaling
        eye_height = abs(bottom_y - top_y)
        if eye_height > 0:
            gaze_y_ratio = (iris_y - top_y) / eye_height
            gaze_y_ratio = self._apply_nonlinear_scale(gaze_y_ratio)
        else:
            gaze_y_ratio = 0.5
        
        # Clamp to valid range
        gaze_x_ratio = np.clip(gaze_x_ratio, 0.0, 1.0)
        gaze_y_ratio = np.clip(gaze_y_ratio, 0.0, 1.0)
        
        return (gaze_x_ratio, gaze_y_ratio)
    
    def _apply_nonlinear_scale(self, value):
        """
        Apply non-linear scaling to improve edge detection.
        
        This makes it easier to reach screen edges while maintaining
        precision in the center.
        """
        # Apply power function for edge enhancement
        if value < 0.5:
            # Left/up side
            return 0.5 * (2 * value) ** 0.8
        else:
            # Right/down side
            return 0.5 + 0.5 * (2 * (value - 0.5)) ** 0.8
    
    def get_eye_landmarks(self, face_landmarks, frame_shape):
        """
        Get eye landmark coordinates for blink detection.
        
        Args:
            face_landmarks: MediaPipe face landmarks
            frame_shape: Shape of the frame (height, width, channels)
        
        Returns:
            dict: Dictionary containing left and right eye landmarks
        """
        if not face_landmarks:
            return None
        
        h, w = frame_shape[:2]
        
        # Extract left eye landmarks
        left_eye = np.array([(face_landmarks.landmark[i].x * w, 
                              face_landmarks.landmark[i].y * h) 
                             for i in self.LEFT_EYE_INDICES])
        
        # Extract right eye landmarks
        right_eye = np.array([(face_landmarks.landmark[i].x * w, 
                               face_landmarks.landmark[i].y * h) 
                              for i in self.RIGHT_EYE_INDICES])
        
        return {
            'left_eye': left_eye,
            'right_eye': right_eye
        }
    
    def release(self):
        """Release MediaPipe resources."""
        self.face_mesh.close()
