from GCSWidget import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from PyQt4 import QtCore

from PyQt4.QtCore import *
import sys


class GCSWidgetServos (GCSWidget):

    widgetName = "Servos"

    def __init__(self, state, parent):
        super(GCSWidgetServos, self).__init__(state, parent)
        self.setObjectName("GCSWidgetServos")
        self.set_datasource_allowable(WidgetDataSource.SINGLE)

        self.numServos = 7
=======
>>>>>>> Initial commit for servos widget file
=======
        self.numServos = 7
>>>>>>> Initial layout attempt, empty set servo method
        self.init_ui()

    def init_ui(self):

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        mylayout = QWidget()
        servo_grid = QGridLayout()
        #servo_grid.setHorizontalSpacing(1)
        mylayout.setLayout(servo_grid)

        self.setWidget(mylayout)
        self.setWindowTitle("Mav Servos")

        for servo_num in range (0, self.numServos):

            servo_name = QLabel(QString.number(servo_num + 5), self)
            servo_name.setAlignment(Qt.AlignCenter)
            servo_grid.addWidget(servo_name, servo_num, 0)

<<<<<<< HEAD
            try:
                self.state.focused_object.mav_param
                servo_Min = QPushButton("Set Low: %d" % (QString.number(self.state.focused_object.mav_param['RC%d_MIN' % (servo_num+5)])))
                servo_Min.clicked.connect(self.set_Servo(servo_num + 5,self.state.focused_object.mav_param['RC%d_Min' % (servo_num+5)]))
            except:
                servo_Min = QPushButton("Set Low: NO MAV!")

            servo_grid.addWidget(servo_Min, servo_num, 1)

            try:
                self.state.focused_object.mav_param
                servo_Max = QPushButton("Set High: %d" % (QString.number(self.state.focused_object.mav_param['RC%d_MAX' % (servo_num+5)])))
                servo_Max.clicked.connect(self.set_Servo(servo_num + 5,self.state.focused_object.mav_param['RC%d_Min' % (servo_num+5)]))
            except:
                servo_Max = QPushButton("Set High: NO MAV!")
=======
class GCSWidgetServos (GCSWidget):
>>>>>>> Initial commit for servos widget file

            servo_grid.addWidget(servo_Max, servo_num, 2)

            servo_Current = QLabel("Waiting", self)
            servo_grid.addWidget(servo_Current, servo_num, 3)


       # self.refresh()
        #self.show()
=======
        self.label_altitude = QLabel("0", self)
        self.label_airspeed = QLabel("0", self)
        self.label_throttle = QLabel("0", self)
        self.label_heading = QLabel("0", self)
        self.label_climbrate = QLabel("0", self)
=======
=======
        mylayout = QWidget()
>>>>>>> Refine grid, add import into mainwindow.py to allow using the servos widget, add to default perspective to make it show up by default
        servo_grid = QGridLayout()
        #servo_grid.setHorizontalSpacing(1)
        mylayout.setLayout(servo_grid)

        self.setWidget(mylayout)
        self.setWindowTitle("Mav Servos")

        for servo_num in range (0, self.numServos):

            servo_name = QLabel(QString.number(servo_num + 5), self)
            servo_name.setAlignment(Qt.AlignCenter)
            servo_grid.addWidget(servo_name, servo_num, 0)

            try:
                self.state.focused_object.mav_param
                servo_Min = QPushButton("Set Low: %d" % (QString.number(self.state.focused_object.mav_param['RC%d_MIN' % (servo_num+5)])))
                servo_Min.clicked.connect(self.set_Servo(servo_num + 5,self.state.focused_object.mav_param['RC%d_Min' % (servo_num+5)]))
            except:
                servo_Min = QPushButton("Set Low: NO MAV!")

            servo_grid.addWidget(servo_Min, servo_num, 1)

            try:
                self.state.focused_object.mav_param
                servo_Max = QPushButton("Set High: %d" % (QString.number(self.state.focused_object.mav_param['RC%d_MAX' % (servo_num+5)])))
                servo_Max.clicked.connect(self.set_Servo(servo_num + 5,self.state.focused_object.mav_param['RC%d_Min' % (servo_num+5)]))
            except:
                servo_Max = QPushButton("Set High: NO MAV!")

            servo_grid.addWidget(servo_Max, servo_num, 2)

            servo_Current = QLabel("Waiting", self)
            servo_grid.addWidget(servo_Current, servo_num, 3)


<<<<<<< HEAD
>>>>>>> Initial layout attempt, empty set servo method
        self.refresh()
>>>>>>> Initial commit for servos widget file
=======
       # self.refresh()
        #self.show()
>>>>>>> Refine grid, add import into mainwindow.py to allow using the servos widget, add to default perspective to make it show up by default


    def refresh(self):

        super(GCSWidgetServos, self).refresh()
<<<<<<< HEAD
<<<<<<< HEAD


    def set_Servo(self, servo, value):

        # set servo value

        print("Setting Servo: %d, to value: %d" % (servo, value))
=======
        w = self.geometry().width()
        h = self.geometry().height()
=======
>>>>>>> Initial layout attempt, empty set servo method


<<<<<<< HEAD
        self.setWindowTitle("GCSWidgetServos")
        self.setMinimumSize(200, 200)
>>>>>>> Initial commit for servos widget file
=======
    def set_Servo(self, servo, value):

        # set servo value

        print("Setting Servo: %d, to value: %d" % (servo, value))
<<<<<<< HEAD
>>>>>>> Initial layout attempt, empty set servo method
=======
        w = self.geometry().width()
        h = self.geometry().height()

        self.label_altitude.move(5, h/2-10)
        self.label_airspeed.move(w-25, h/2-10)
        self.label_throttle.move(5, 20)
        self.label_heading.move(w/2 - 10, 50)
        self.label_climbrate.move(w-25,20)

        self.setWindowTitle("GCSWidgetServos")
        self.setMinimumSize(200, 200)

>>>>>>> Initial commit for servos widget file
