#!/usr/bin/python3

#IMPORTING LIBRARIES

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtGui import QPixmap

# Import your generated UI file
# Make sure the paste.txt file is saved as a .py file (e.g., ui_mainwindow.py)
from extwindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Initialize video player
        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        
        # Replace the graphicsView_2 with video widget for video display
        # Get the parent layout or container
        parent = self.ui.graphicsView_2.parent()
        geometry = self.ui.graphicsView_2.geometry()
        
        # Hide the original graphics view
        self.ui.graphicsView_2.hide()
        
        # Set up video widget with same geometry
        self.video_widget.setParent(parent)
        self.video_widget.setGeometry(geometry)
        self.video_widget.show()
        
        # Connect media player to video widget
        self.media_player.setVideoOutput(self.video_widget)
        
        # Video file paths - replace with your actual video files
        self.video_paths = [
            "path/to/rgb_camera_feed.mp4",
            "path/to/lidar_visualization.mp4", 
            "path/to/trajectory_2d.mp4",
            "path/to/trajectory_3d.mp4"
        ]
        
        # Connect radio buttons to video selection
        self.ui.rgbdbutton.toggled.connect(lambda checked: self.select_video(0) if checked else None)  # RGB-D Camera
        self.ui.lidarbutton.toggled.connect(lambda checked: self.select_video(1) if checked else None)  # 3D-LiDAR Vision
        self.ui.traject2dbutton.toggled.connect(lambda checked: self.select_video(2) if checked else None)    # Trajectory 2D Vision
        self.ui.traject3dbutton.toggled.connect(lambda checked: self.select_video(3) if checked else None)  # Trajectory 3D Vision
        
        # Connect control buttons
        self.ui.start.clicked.connect(self.play_video)     # Start
        self.ui.pause.clicked.connect(self.pause_video)    # Pause
        self.ui.stop.clicked.connect(self.stop_video)     # Stop
        
        # Connect directional buttons
        self.ui.pushButton_7.clicked.connect(self.move_forward)   # Forward
        self.ui.pushButton_8.clicked.connect(self.move_backward)  # Backward
        self.ui.pushButton_9.clicked.connect(self.move_left)      # Left
        self.ui.pushButton_10.clicked.connect(self.move_right)    # Right
        
        # Connect sliders to update display
        self.ui.horizontalSlider.valueChanged.connect(self.update_max_speed)
        self.ui.horizontalSlider_2.valueChanged.connect(self.update_angular_speed)
        self.ui.horizontalSlider_3.valueChanged.connect(self.update_min_speed)
        
        # Set initial values
        self.setup_initial_values()
        
    def setup_initial_values(self):
        """Set initial values for sliders and displays"""
        # Set slider ranges
        self.ui.horizontalSlider.setRange(0, 100)      # Max speed slider (0-10 m/s scaled to 0-100)
        self.ui.horizontalSlider_2.setRange(0, 314)    # Angular speed slider (0-3.14 rad/s scaled to 0-314)
        self.ui.horizontalSlider_3.setRange(0, 50)     # Min speed slider (0-5 m/s scaled to 0-50)
        
        # Set initial values
        self.ui.horizontalSlider.setValue(50)
        self.ui.horizontalSlider_2.setValue(157)
        self.ui.horizontalSlider_3.setValue(10)
        
        # Update displays
        self.update_max_speed()
        self.update_angular_speed()
        self.update_min_speed()
        
        # Set initial LCD values (simulated sensor readings)
        self.ui.lcdNumber.display(12.5)    # Front Left Motor
        self.ui.lcdNumber_2.display(12.3)  # Front Right Motor
        self.ui.lcdNumber_3.display(12.4)  # Back Right Motor
        self.ui.lcdNumber_4.display(12.6)  # Back Left Motor
        self.ui.lcdNumber_5.display(5.2)   # Jetson Module
        self.ui.lcdNumber_6.display(5.1)   # Arduino Module
        self.ui.lcdNumber_7.display(24.1)  # LiDAR Module
        self.ui.lcdNumber_8.display(24.8)  # Battery
        self.ui.lcdNumber_9.display(30)    # FPS
        
        # Initial robot status
        self.ui.lcdNumber_10.display(0.0)  # Speed
        self.ui.lcdNumber_11.display(0.0)  # Angular Speed
        self.ui.lcdNumber_12.display(0.0)  # Heading
        
    def select_video(self, index):
        """Select and load video based on radio button selection"""
        if 0 <= index < len(self.video_paths):
            print(f"Selected video: {self.video_paths[index]}")
            # Note: Replace with actual video file paths
            # self.media_player.setSource(QUrl.fromLocalFile(self.video_paths[index]))
            
    def play_video(self):
        """Start video playback"""
        self.media_player.play()
        print("Video started")
        
    def pause_video(self):
        """Pause video playback"""
        self.media_player.pause()
        print("Video paused")
        
    def stop_video(self):
        """Stop video playback"""
        self.media_player.stop()
        print("Video stopped")
        
    def move_forward(self):
        """Handle forward movement"""
        print("Moving forward")
        self.ui.lcdNumber_10.display(2.5)  # Update speed display
        
    def move_backward(self):
        """Handle backward movement"""
        print("Moving backward")
        self.ui.lcdNumber_10.display(-2.5)  # Update speed display
        
    def move_left(self):
        """Handle left movement"""
        print("Turning left")
        self.ui.lcdNumber_11.display(0.5)  # Update angular speed display
        
    def move_right(self):
        """Handle right movement"""
        print("Turning right")
        self.ui.lcdNumber_11.display(-0.5)  # Update angular speed display
        
    def update_max_speed(self):
        """Update max speed display from slider"""
        value = self.ui.horizontalSlider.value() / 10.0  # Convert to m/s
        print(f"Max speed: {value} m/s")
        
    def update_min_speed(self):
        """Update min speed display from slider"""
        value = self.ui.horizontalSlider_3.value() / 10.0  # Convert to m/s
        print(f"Min speed: {value} m/s")
        
    def update_angular_speed(self):
        """Update angular speed display from slider"""
        value = self.ui.horizontalSlider_2.value() / 100.0  # Convert to rad/s
        print(f"Max angular speed: {value} rad/s")

def main():
    # Create application
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()