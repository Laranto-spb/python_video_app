from PyQt5.QtWidgets import QFileDialog
import sys
import os
import subprocess

class SaveFile:
    def __init__(self, parent):
        self.parent = parent

    def save_file(self, screenshot):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save Screenshot", "", "JPEG Files (*.jpg);;All Files (*)", options=options)
        if file_name:
            if not file_name.lower().endswith('.jpg'):
                file_name += '.jpg'
            screenshot.save(file_name, 'jpg')
            if sys.platform == "darwin":
                subprocess.run(["open", file_name])
            elif sys.platform == "win32":
                os.startfile(file_name)
            else:
                subprocess.run(["xdg-open", file_name])