from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QMessageBox

from PyQt5.QtGui import QScreen, QPainter, QPen
from PyQt5.QtCore import QRect, Qt
import time

import sys
import os
import subprocess

class OverlayWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.start_point = None
        self.end_point = None

    def paintEvent(self, event):
        if self.start_point and self.end_point:
            painter = QPainter(self)
            pen = QPen(Qt.red, 2, Qt.DashLine)
            painter.setPen(pen)
            rect = QRect(self.start_point, self.end_point).normalized()
            painter.drawRect(rect)


class ScreenshotApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        # cropping
        self.start_point = None
        self.end_point = None
        self.overlay_widget = None

    def initUI(self):
        self.setWindowTitle("Glabix Video Recorder")
        self.setGeometry(300, 300, 300, 300)

        start_button = QtWidgets.QPushButton("Screen Shot", self)
        start_button.move(0, 0)
        start_button.clicked.connect(self.take_screen_shot)
        start_button.adjustSize()

        crop_button = QtWidgets.QPushButton("Crop Screen Shot", self)
        crop_button.move(0, 100)
        crop_button.clicked.connect(self.start_crop_mode)
        crop_button.adjustSize()

        reset_button = QtWidgets.QPushButton("Reset Selection", self)
        reset_button.clicked.connect(self.reset_selection)
        reset_button.setGeometry(10, 50, 150, 30)


    def save_file(self, screenshot):
        # Prompt user for file save location
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "JPEG Files (*.jpg);;All Files (*)", options=options)

        if file_name:
            # Ensure the file has a .jpg extension
            if not file_name.lower().endswith('.jpg'):
                file_name += '.jpg'

            screenshot.save(file_name, 'jpg')

            # Open the screenshot using the default image viewer
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", file_name])
            elif sys.platform == "win32":  # Windows
                os.startfile(file_name)
            else:  # Linux or other platforms
                subprocess.run(["xdg-open", file_name])

    def take_screen_shot(self):
        # Hide the main window
        self.hide()

        # Allow the window to be hidden before taking a screenshot
        QtWidgets.QApplication.processEvents()

        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0)  # Capture the whole screen

        self.save_file(screenshot)

        time.sleep(0.7) # try to implement via QTimer
        self.show()

    def start_crop_mode(self):
        # Create and show overlay widget
        self.overlay_widget = OverlayWidget()
        self.overlay_widget.start_point = None
        self.overlay_widget.end_point = None
        self.overlay_widget.showFullScreen()  # Show overlay in full screen
        self.overlay_widget.raise_()       # Raise overlay above other windows

    def mousePressEvent(self, event):
        print("mouse")
        if event.button() == Qt.LeftButton and self.overlay_widget is not None:
            # Capture the starting point of the selection
            self.overlay_widget.start_point = event.globalPos()
            self.overlay_widget.end_point = event.globalPos()
            self.overlay_widget.update()  # Trigger repaint to show rectangle

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.overlay_widget is not None:
            # Update the end point of the selection while dragging
            self.overlay_widget.end_point = event.globalPos()
            self.overlay_widget.update()  # Trigger repaint to update rectangle

    def paintEvent(self, event):
        if self.start_point and self.end_point:
            painter = QPainter(self.overlay_widget)  # Draw on the overlay widget
            pen = QPen(Qt.red, 2, Qt.DashLine)
            painter.setPen(pen)
            self.rect = QRect(self.start_point, self.end_point).normalized()
            painter.drawRect(self.rect)

    def capture_screenshot(self):
      if self.rect.isValid():
          screen = QApplication.primaryScreen()
          screenshot = screen.grabWindow(0, self.rect.x(), self.rect.y(), self.rect.width(), self.rect.height())
          self.save_file(screenshot)

          time.sleep(0.5)  # Delay before showing the main window again
          self.show()

    def reset_selection(self):
        print("stoped")
        self.start_point = None
        self.end_point = None
        self.rect = QRect()
        self.overlay_widget.hide()  # Hide the overlay after capturing

def main():
    app = QApplication(sys.argv)
    ex = ScreenshotApp()
    ex.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) #always on top
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()