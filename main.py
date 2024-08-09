from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import cv2
import datetime
import sys

from screen_shot_handler import ScreenShotHandler

class ScreenshotApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.screen_shot_handler = ScreenShotHandler(self)
        self.initUI()

        # Initialize video label to display the video feed
        self.video_label = QtWidgets.QLabel(self)
        self.video_label.setFixedSize(400, 400)  # Set a fixed size for the video display
        self.video_label.move(300, 0)

        self.recoding_info = QtWidgets.QLabel(self)
        self.recoding_info.move(300, 0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.cap = None
        self.is_recording = False
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None

    def initUI(self):
        self.setWindowTitle("Glabix Video Recorder")
        self.setGeometry(50, 50, 1000, 500)

        text = QtWidgets.QLabel("Take a screenshot:", self)
        text.move(20, 0)
        text.adjustSize()

        start_button = QtWidgets.QPushButton("Entire screen", self)
        start_button.move(20, 50)
        start_button.clicked.connect(self.screen_shot_handler.take_screen_shot)
        start_button.adjustSize()

        video_text = QtWidgets.QLabel("Take a video:", self)
        video_text.move(20, 100)
        video_text.adjustSize()

        grab_btn = QtWidgets.QPushButton("Grab", self)
        grab_btn.move(20, 150)
        grab_btn.adjustSize()
        grab_btn.clicked.connect(self.grab_camera)

        rec_btn = QtWidgets.QPushButton("Record", self)
        rec_btn.move(20, 180)
        rec_btn.adjustSize()
        rec_btn.clicked.connect(self.capture_video)

        stop_btn = QtWidgets.QPushButton("Stop", self)
        stop_btn.move(20, 210)
        stop_btn.adjustSize()
        stop_btn.clicked.connect(self.stop_capture)

    def grab_camera(self):
        print("Camera grabbed")
        self.video_label.setVisible(True)
        print("Video Visible")

        if self.cap is None:
            self.cap = cv2.VideoCapture(0)  # Use 0 for the default camera
            print("timer start")
            self.timer.start(20)  # Update every 20 ms

    def update_frame(self):
        if self.cap is not None:
            print("update framing")
            ret, frame = self.cap.read()
            if ret:
                if self.is_recording:
                    if self.out is not None:
                        self.out.write(frame)  # Write the current frame to the video file

                # Convert frame to QImage and display it
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                q_img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
                self.video_label.setPixmap(QPixmap.fromImage(q_img))

                # Resize the image to fit the video_label size
                q_img = q_img.scaled(self.video_label.size(), aspectRatioMode=1)  # Keep aspect ratio
                self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def capture_video(self):
        print("Start record video...")
        if not self.is_recording:
            self.is_recording = True
            # Initialize VideoWriter only when starting to record
            if self.cap is not None:
                frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.out = cv2.VideoWriter(f'output_{datetime.datetime.now()}.mp4', self.fourcc, 20.0, (frame_width, frame_height))
        else:
            self.is_recording = False
            if self.out is not None:
                self.out.release()
                self.out = None

    def stop_capture(self):
        self.is_recording = False
        self.cap = None
        self.out = None

        self.timer.stop()
        print("Timer stopped")

        self.video_label.setVisible(False)
        print("Video invisible")

    def closeEvent(self, event):
        if self.cap is not None:
            self.cap.release()
            if self.is_recording and self.out is not None:
                self.out.release()
        event.accept()

def main():
    app = QApplication(sys.argv)
    ex = ScreenshotApp()
    ex.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) #always on top
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()