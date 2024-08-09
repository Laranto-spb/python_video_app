from PyQt5.QtGui import QImage, QPixmap
import cv2
import datetime

class WebcamHandler:
      def __init__(self, parent):
        self.parent = parent

        self.cap = None
        self.is_recording = False
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None

      def grab_camera(self):
        print("Camera grabbed")
        self.parent.video_label.setVisible(True)
        print("Video Visible")

        if self.cap is None:
            self.cap = cv2.VideoCapture(0)  # Use 0 for the default camera
            print("timer start")
            self.parent.timer.start(20)  # Update every 20 ms

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
                  self.parent.video_label.setPixmap(QPixmap.fromImage(q_img))

                  # Resize the image to fit the video_label size
                  q_img = q_img.scaled(self.parent.video_label.size(), aspectRatioMode=1)  # Keep aspect ratio
                  self.parent.video_label.setPixmap(QPixmap.fromImage(q_img))

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

          self.parent.timer.stop()
          print("Timer stopped")

          self.parent.video_label.setVisible(False)
          print("Video invisible")

      def closeEvent(self, event):
          if self.cap is not None:
              self.cap.release()
              if self.is_recording and self.out is not None:
                  self.out.release()
          event.accept()