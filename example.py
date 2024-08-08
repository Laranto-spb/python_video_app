from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os
import sys
import numpy
import csv

from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout,
                             QApplication, QPushButton, QSlider,
                             QFileDialog, QAction)

from imutils import face_utils
import threading
import queue
from imutils import face_utils
import threading
import queue
import utils
import cv2
import time
import imutils as im
from datetime import datetime


video_running = False
capture_thread = None
videoFlag = False
running = False



q_video = queue.Queue()


def grab( cam, queue, width, height, fps):
    global running
    global videoFlag
    global fname
    global sname
    global csvname
    global video_running
    global progress
    global quitFlag


    if videoFlag == False:
        capture = cv2.VideoCapture(cam)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        capture.set(cv2.CAP_PROP_FPS, fps)


        fourcc =0x7634706d
        now = datetime.now()
        time_str = now.strftime("%d%m%Y%H%M%S")
        name = 'Recorded'+time_str+'.mp4'
        out = cv2.VideoWriter(name, fourcc, fps, (640, 480), True)



    numFrames = 10
    numFramesCnt = 0
    seconds = 1
    printFlag =0
    start_time = time.time()

    frameCnt=0
    frameFlag =0
    prevFrame = 0


    while(running):
        if frameFlag==2:
            frameFlag=0

        frame = {}
        (grabbed, img) = capture.read()
        if grabbed == False:
            running=False
            break

        if videoFlag == False:
            out.write(img)

        if numFramesCnt<=numFrames:
            if numFramesCnt == numFrames:
                end = time.time()
                seconds = end - start
                print(seconds)
                fps = (numFrames/seconds)
                numFramesCnt =0

                printFlag = 1
            if numFramesCnt == 0:
                start = time.time()
            numFramesCnt += 1
        if printFlag==1:
            cv2.putText(img, "Frame Rate = " + str(fps), (1, 20), 2, .8, (0, 255, 0))
        else:
            cv2.putText(img, "Frame Rate = " + "Acquiring ... ", (1, 20), 2, .8, (0, 255,0))

        frame["img"] = img
        (h, w) = img.shape[:2]
        (B, G, R) = cv2.split(img)
        if queue.qsize() < 1:
            queue.put(frame)
        else:
            running=False

        if running == False :
            capture.release()
            quitFlag = True
            break


class OrangeImageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OrangeImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(633, 567)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.gridLayout = QtWidgets.QGridLayout()
		self.gridLayout.setObjectName("gridLayout")
		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(17, 16, 640, 480))
		self.label.setStyleSheet("border-color: rgb(0, 0, 0);")
		self.label.setText("")
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
		self.widget = QtWidgets.QWidget(self.centralwidget)
		self.widget.setObjectName("widget")
		self.gridLayout.addWidget(self.widget, 1, 0, 1, 1)
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton_2.setObjectName("pushButton_2")
		self.horizontalLayout.addWidget(self.pushButton_2)
		self.pushButton = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton.setObjectName("pushButton")
		self.horizontalLayout.addWidget(self.pushButton)
		self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
		self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 633, 22))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.pushButton.clicked.connect(self.startCapture)
		self.pushButton_2.clicked.connect(self.quitCapture)
		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		self.timer = QtCore.QTimer(MainWindow)
		self.timer.timeout.connect(self.update_frame)
		self.timer.start(1)
		self.image = None
		self.label.setStyleSheet("border: 1px solid black")
		w = self.label.width()
		h = self.label.height()
		self.label = OrangeImageWidget(self.label)
		self.label.resize(w, h)
		self.label.setMouseTracking(True)
		self.label.installEventFilter(MainWindow)
		self.cnt=0

	def startCapture(self):
		global video_running
		global running
		global progress
		self.pushButton.setEnabled(False)
		running = True
		video_running = True
		if self.cnt == 0:
		   capture_thread.start()
		   self.cnt =1

	def quitCapture(self):
		global running
		running=False
		print ("See you Again!")
		QtCore.QCoreApplication.quit()


	def update_frame(self):

		global video_running
		global videoFlag
		global progress
		if not q_video.empty() :
			if video_running == True:
				if videoFlag == False:
					self.pushButton.setText('Recording')

				frame = q_video.get()
				img = frame["img"]
				img = numpy.array(img)


				img_height, img_width, img_colors = img.shape


				scale_w = float(self.label.width()) / float(img_width)
				scale_h = float(self.label.height()) / float(img_height)
				scale = min([scale_w, scale_h])

				if scale == 0:
					scale = 1

				img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
				img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
				height, width, bpc = img.shape
				bpl = bpc * width
				image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888)
				self.label.setImage(image)


	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.pushButton_2.setText(_translate("MainWindow", "Quit"))
		self.pushButton.setText(_translate("MainWindow", "Start"))

capture_thread = threading.Thread(target=grab, args=(0, q_video, 640, 480, 33))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())