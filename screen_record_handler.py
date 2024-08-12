import pyautogui
import cv2
import numpy as np
import datetime

class ScreenRecordHandler:
    def __init__(self, parent):
        self.parent = parent
        self.out = None


    def capture_screen(self):
        print("capture")
        screen_size = pyautogui.size()
        print(screen_size)
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        filename = f'output_{datetime.datetime.now()}.mp4'
        fps = 20.0

        self.out = cv2.VideoWriter(filename, codec, fps, (1050, 1680))
        self.parent.screen_timer.start(60)

    def update_frame(self):
        if self.out is not None:
            print("update framing")
            img = pyautogui.screenshot()
            frame = np.array(img)
            final_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # do not create video from frames
            self.out.write(final_frame)

            # cv2.imshow('Screenshot', final_frame) # test that frames records

    def stop_capture(self):
        self.out.release()
        self.out = None
        self.parent.timer.stop()
        print("Timer stopped")
