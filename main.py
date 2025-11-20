"""
AI Gaze-Controlled Mouse - Main Entry Point
Author: AI Assistant
Date: October 25, 2025

This is the main entry point that integrates all modules and controls the application flow.
Now includes GAZE TRACKING with calibration for high-accuracy cursor control.
"""

import cv2
import threading
import time
from eye_tracker import EyeTracker
from mouse_controller import MouseController
from blink_detector import BlinkDetector
from calibration import GazeCalibrator
from ui import EyeMouseGUI

class EyeMouseApp:
    """Main application controller that integrates all modules."""
    
    def __init__(self):
        """Initialize all components of the application."""
        self.eye_tracker = EyeTracker()
        self.mouse_controller = MouseController()
        self.blink_detector = BlinkDetector()
        self.calibrator = GazeCalibrator(self.blink_detector)
        
        self.is_tracking = False
        self.cap = None
        self.tracking_thread = None
        
        # Create GUI and pass control methods
        self.gui = EyeMouseGUI(
            start_callback=self.start_tracking,
            pause_callback=self.pause_tracking,
            exit_callback=self.exit_app,
            calibrate_callback=self.calibrate_gaze
        )
    
    
    def calibrate_gaze(self):
        """Run the gaze calibration process."""
        print("\n" + "="*60)
        print("STARTING GAZE CALIBRATION")
        print("="*60)
        
        # Initialize camera for calibration
        if not self.cap or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.gui.update_status("Error: Camera not found!", "red")
                self.gui.update_calibration_status(False)
                return
        
        # Run calibration
        success = self.calibrator.start_calibration(self.cap, self.eye_tracker)
        
        if success:
            # Load calibration data into mouse controller
            calibration_data = self.calibrator.get_calibration_data()
            self.mouse_controller.load_calibration(calibration_data)
            
            self.gui.update_status("Calibration Complete!", "green")
            self.gui.update_calibration_status(True)
            print("✓ Calibration successful! You can now start tracking.")
        else:
            self.gui.update_status("Calibration Failed", "red")
            self.gui.update_calibration_status(False)
            print("✗ Calibration failed. Please try again.")
        
        # Keep camera open for potential immediate tracking
        # Or release it if user wants to calibrate again
        time.sleep(1)
        self.gui.update_status("Ready to Start", "blue")
    
    def start_tracking(self):
        """Start the eye tracking and mouse control."""
        if self.is_tracking:
            return
        
        # Check if calibrated
        if not self.mouse_controller.get_calibration_status():
            self.gui.update_status("Please calibrate first!", "red")
            print("⚠️  Warning: System not calibrated. Please run calibration first.")
            return
        
        # Initialize camera
        if not self.cap or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            self.gui.update_status("Error: Camera not found!", "red")
            return
        
        self.is_tracking = True
        self.gui.update_status("Tracking Active", "green")
        
        # Start tracking in a separate thread
        self.tracking_thread = threading.Thread(target=self._tracking_loop, daemon=True)
        self.tracking_thread.start()
    
    def pause_tracking(self):
        """Pause the eye tracking."""
        if not self.is_tracking:
            return
        
        self.is_tracking = False
        self.gui.update_status("Paused", "orange")
        
        # Release camera
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
    
    def exit_app(self):
        """Exit the application."""
        self.is_tracking = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.gui.destroy()
    
    def _tracking_loop(self):
        """Main tracking loop that runs in a separate thread."""
        try:
            while self.is_tracking:
                ret, frame = self.cap.read()
                if not ret:
                    self.gui.update_status("Error: Cannot read from camera", "red")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process frame with eye tracker
                frame, landmarks = self.eye_tracker.process_frame(frame)
                
                if landmarks:
                    # Get gaze position (relative position within eye socket)
                    gaze_ratio = self.eye_tracker.get_eye_position(landmarks, frame.shape)
                    
                    if gaze_ratio:
                        # Move mouse cursor using calibrated gaze tracking
                        self.mouse_controller.move_cursor(gaze_ratio)
                        
                        # Display gaze info on frame
                        cv2.putText(frame, f"Gaze: ({gaze_ratio[0]:.2f}, {gaze_ratio[1]:.2f})", 
                                    (10, frame.shape[0] - 40), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                    
                    # Detect blink patterns and perform actions
                    blink_result = self.blink_detector.detect_blink(landmarks, frame.shape)
                    
                    # Handle different actions based on blink patterns
                    if blink_result['left_click']:
                        self.mouse_controller.left_click()
                        cv2.putText(frame, "3 BLINKS - LEFT CLICK", (30, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    elif blink_result['right_click']:
                        self.mouse_controller.right_click()
                        cv2.putText(frame, "2 BLINKS - RIGHT CLICK", (30, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
                    elif blink_result['drag_toggle']:
                        if self.mouse_controller.is_drag_active():
                            self.mouse_controller.end_drag()
                            cv2.putText(frame, "4 BLINKS - DROP", (30, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2)
                        else:
                            self.mouse_controller.start_drag()
                            cv2.putText(frame, "4 BLINKS - START DRAG", (30, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2)
                    
                    elif blink_result['middle_click']:
                        self.mouse_controller.middle_click()
                        cv2.putText(frame, "5 BLINKS - MIDDLE CLICK", (30, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                    
                    elif blink_result['scroll_up']:
                        self.mouse_controller.scroll_up()
                        cv2.putText(frame, "SCROLL UP", (30, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    
                    elif blink_result['scroll_down']:
                        self.mouse_controller.scroll_down()
                        cv2.putText(frame, "SCROLL DOWN", (30, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    
                    # Show blink count and drag status
                    blink_count = len(self.blink_detector.blink_sequence)
                    if blink_count > 0:
                        cv2.putText(frame, f"Blinks: {blink_count}", (30, 100), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    
                    # Show drag status
                    if self.mouse_controller.is_drag_active():
                        cv2.putText(frame, "DRAGGING...", (30, 140), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 165, 0), 2)
                
                # Display frame
                cv2.imshow('Gaze Tracker - Press Q to hide window', frame)
                
                # Break on 'q' key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
        except Exception as e:
            print(f"Error in tracking loop: {e}")
            self.gui.update_status(f"Error: {str(e)}", "red")
        
        finally:
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
    
    def run(self):
        """Start the GUI main loop."""
        self.gui.run()


if __name__ == "__main__":
    print("Starting AI Gaze-Controlled Mouse Application...")
    print("=" * 50)
    print("IMPORTANT: This is a GAZE TRACKER (not head tracker)")
    print("You must CALIBRATE before first use!")
    print("Keep your HEAD STILL, move only your EYES")
    print("Make sure your webcam is connected and functioning.")
    print("=" * 50)
    
    try:
        app = EyeMouseApp()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
