from PyQt5.QtWidgets import QApplication
from save_file import SaveFile
import time

class ScreenShotHandler:
    def __init__(self, parent):
        self.parent = parent
        self.save_file = SaveFile(parent)

    def take_screen_shot(self):
        self.parent.hide()
        QApplication.processEvents()
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0)
        self.save_file.save_file(screenshot)
        time.sleep(3)
        self.parent.show()