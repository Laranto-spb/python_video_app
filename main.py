from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import QTimer
import cv2
import datetime
import sys

from screen_shot_handler import ScreenShotHandler
from webcam_handler import WebcamHandler
from screen_record_handler import ScreenRecordHandler

class ScreenshotApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.video_label = QtWidgets.QLabel(self)
        self.video_label.setFixedSize(400, 400)  # Set a fixed size for the video display
        self.video_label.move(300, 0)

        self.screen_shot_handler = ScreenShotHandler(self)
        self.webcam_handler = WebcamHandler(self)
        self.screen_record_handler = ScreenRecordHandler(self)

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.webcam_handler.update_frame)

        self.screen_timer = QTimer()
        self.screen_timer.timeout.connect(self.screen_record_handler.update_frame)

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
        grab_btn.clicked.connect(self.webcam_handler.grab_camera)

        rec_btn = QtWidgets.QPushButton("Record", self)
        rec_btn.move(20, 180)
        rec_btn.adjustSize()
        rec_btn.clicked.connect(self.webcam_handler.capture_video)

        stop_btn = QtWidgets.QPushButton("Stop", self)
        stop_btn.move(20, 210)
        stop_btn.adjustSize()
        stop_btn.clicked.connect(self.webcam_handler.stop_capture)

        start_screen_rec_btn = QtWidgets.QPushButton("Record", self)
        start_screen_rec_btn.move(20, 230)
        start_screen_rec_btn.adjustSize()
        start_screen_rec_btn.clicked.connect(self.screen_record_handler.capture_screen)

        stop_screen_rec_btn = QtWidgets.QPushButton("Stop", self)
        stop_screen_rec_btn.move(20, 250)
        stop_screen_rec_btn.adjustSize()
        stop_screen_rec_btn.clicked.connect(self.screen_record_handler.stop_capture)

def main():
    app = QApplication(sys.argv)
    ex = ScreenshotApp()
    ex.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) #always on top
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()