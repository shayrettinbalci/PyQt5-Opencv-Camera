"""
In this example, we demonstrate how to create simple camera viewer using Opencv3 and PyQt5

Author: Berrouba.A
Last edited: 21 Feb 2018
"""

# import system module
import sys

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtCore import QTimer

# import Opencv module
import cv2

from ui_main_window import *


class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # icon
        self.setWindowIcon(QIcon('icon.png'))
        # create a timer
        self.viewTimer = QTimer()
        self.saveTimer = QTimer()
        # set timer timeout callback function
        self.viewTimer.timeout.connect(self.viewCam)
        self.saveTimer.timeout.connect(self.saveCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlView)
        self.ui.save_bt.clicked.connect(self.controlSave)
        # waring message box
        self.msg = QMessageBox()
        self.msg.setWindowIcon(QIcon('warning.png'))

    # view camera
    def viewCam(self):
        if not self.saveTimer.isActive():
            # read image in BGR format
            ret, image = self.cap.read()
            # get image infos
            height, width, channel = image.shape
            step = channel * width
            # create QImage from image
            qImg = QImage(image.data, width, height, step, QImage.Format_BGR888)
            # show image in img_label
            self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlSave(self):
        # if camera timer active
        if self.viewTimer.isActive():
            self.msg.setWindowTitle("Warning")
            self.msg.setText("Please stop the camera")
            self.msg.exec_()
        # if timer is stopped
        if not self.saveTimer.isActive():
            if not self.viewTimer.isActive():
                # create video capture
                self.cap = cv2.VideoCapture(0)
                # set video output
                self.out = cv2.VideoWriter("outpy.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (640, 480))
                # start timer
                self.saveTimer.start(30)
                # update save_bt text
                self.ui.save_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.saveTimer.stop()
            # release video capture
            self.cap.release()
            # update save_bt text
            self.ui.save_bt.setText("Save")
            self.ui.image_label.setText("Camera")

    def controlView(self):
        # if timer is stopped
        if self.saveTimer.isActive():
            self.msg.setWindowTitle("Warning")
            self.msg.setText("Please stop recording")
            self.msg.exec_()
        if not self.viewTimer.isActive():
            if not self.saveTimer.isActive():
                # create video capture
                self.cap = cv2.VideoCapture(0)
                # start timer
                self.viewTimer.start(30)
                # update control_bt text
                self.ui.control_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.viewTimer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")
            self.ui.image_label.setText("Camera")

    def saveCam(self):
        if not self.viewTimer.isActive():
            ret, image = self.cap.read()
            # get image infos
            height, width, channel = image.shape
            step = channel * width
            # write video
            self.out.write(image)
            # create QImage from image
            qImg = QImage(image.data, width, height, step, QImage.Format_BGR888)
            # show image in img_label
            self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
