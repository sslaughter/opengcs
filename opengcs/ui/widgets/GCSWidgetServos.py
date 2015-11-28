from GCSWidget import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gcs_state import *
import functools
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

<<<<<<< HEAD
            servo_grid.addWidget(servo_Max, servo_num, 2)

            servo_Current = QLabel("Waiting", self)
            servo_grid.addWidget(servo_Current, servo_num, 3)
=======
    widget_name_plaintext = "Servos"

    def __init__(self, state, parent):
        super(GCSWidgetServos, self).__init__(state, parent)
        self.setObjectName("GCSWidgetServos")
        self.setWindowTitle("Servos")
        self.set_datasource(True)
        self.set_datasource_allowable(WidgetDataSource.SINGLE | WidgetDataSource.SWARM)
        self.numServos = 7
        self.offset = 5
        self.servoList = {}
        self.init_ui()
>>>>>>> Moved to MAVServo class implementation


<<<<<<< HEAD
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
=======

        self.setWindowTitle("Mav Servos")
        self.refresh()


    def refresh(self):

        super(GCSWidgetServos, self).refresh()

>>>>>>> Moved to MAVServo class implementation
        mylayout = QWidget()
>>>>>>> Refine grid, add import into mainwindow.py to allow using the servos widget, add to default perspective to make it show up by default
        servo_grid = QGridLayout()
        mylayout.setLayout(servo_grid)
        self.setWidget(mylayout)
        self.numServos = 7
        #TODO ^^ figure out why I have to set that in the function


        for servo_num in range (0,self.numServos):

            new_servo = MAVServo(servo_num, self)
            try:
                self.state.focused_object.mav_param
                new_servo.hasData = True
                new_servo.maxValue = self.state.focused_object.mav_param['RC%d_MAX' % (servo_num+self.offset)]
                new_servo.minValue = self.state.focused_object.mav_param['RC%d_MAX' % (servo_num+self.offset)]

            except:
                new_servo.hasData = False


            servo_grid.addWidget(new_servo, servo_num, 0)


            if new_servo.hasData:
                servo_Min = QPushButton("Set Low: %d" % new_servo.minValue)
                servo_Max = QPushButton("Set High: %d" % new_servo.maxValue)


            else:
                servo_Min = QPushButton("Set Low: NO MAV!")
                servo_Max = QPushButton("Set High: NO MAV!")


            servo_Min.clicked.connect(functools.partial(new_servo.update_value, new_servo.minValue))
            servo_Max.clicked.connect(functools.partial(new_servo.update_value, new_servo.maxValue))



            servo_grid.addWidget(servo_Min, servo_num, 1)
            servo_grid.addWidget(servo_Max, servo_num, 2)

            servo_Current = QLabel("Waiting", self)
            servo_grid.addWidget(servo_Current, servo_num, 3)

            self.servoList[servo_num] = new_servo

<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> Initial layout attempt, empty set servo method
        self.refresh()
>>>>>>> Initial commit for servos widget file
=======
       # self.refresh()
        #self.show()
>>>>>>> Refine grid, add import into mainwindow.py to allow using the servos widget, add to default perspective to make it show up by default
=======
>>>>>>> Moved to MAVServo class implementation



<<<<<<< HEAD
        super(GCSWidgetServos, self).refresh()
<<<<<<< HEAD
<<<<<<< HEAD
=======
    def read_settings(self, settings):
        print("Reading settings")
        self.numServos = settings.value('num_servos')
        #TODO read_settings

    def write_settings(self, settings):
        print("Writing settings")
        settings.setValue('num_servos', self.numServos)
        #TODO write_settings
>>>>>>> Moved to MAVServo class implementation


    def set_Servo(self, servo, value):

        # set servo value

        print("Setting Servo: %d, to value: %d" % (servo, value))
<<<<<<< HEAD
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
=======
>>>>>>> Moved to MAVServo class implementation



#Need to save the max/min value of each servo value, taken from parameters
#also need to be able to access labels attached to those servos
#Do we need to pass the mav object? - I don't think so

class MAVServo(QLabel):

    def __init__(self, servo_number, parent):

        super(MAVServo, self).__init__()
        self.setText(QString.number(servo_number+parent.offset))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('color: green')

        self.hasData = False
        self.servoNUM = servo_number
        self.maxValue = None
        self.minValue = None
        self.currentValue = None



    def update_value(self, value):

        if value != None:
            self.currentValue = value


        if self.hasData:
            if self.currentValue >= self.maxValue-200:
                if self.currentValue >= self.maxValue - 50:
                    self.setStyleSheet('color: red')
                    return
                self.setStyleSheet('color:yellow')
            elif self.currentValue <= self.minValue+200:
                if self.currentValue <= self.minValue + 50:
                    self.setStyleSheet('color: red')
                    return
                self.setStyleSheet('color:yellow')
        else:
            print("No Mav, not updating, but I'm talking for servo: %d" % (self.servoNUM+5))






>>>>>>> Initial commit for servos widget file
