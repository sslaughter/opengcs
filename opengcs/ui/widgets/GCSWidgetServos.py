from GCSWidget import *
from PyQt4.QtGui import *
<<<<<<< HEAD
<<<<<<< HEAD
from PyQt4.QtCore import *
import sys
=======
from PyQt4 import QtCore
>>>>>>> Initial layout attempt, empty set servo method
from pymavlink import mavutil


# Nee
# Access parameters for focused MAV with self.focused_object.mav_param['RC5_MIN']
#Add column showing current PWM output value for each servo channel
#get this by watching for SERVO_OUTPUT_RAW messages in the widget's process process_messages() method
#Wire buttons to empty methods
#Need to compare current value of the servo to RCn_Max and change the color based on how close it is to the RC_Min/Max value
#Override __init(), call superconstructor
#override refresh(), call super constructor first line, called when data source changes, widget.self.datasource contains the current datasource object
#override read_settings() and write_settings(), call supersonctructor in first line
# saves/restore persistent values between user settings

"""
Implementation

 Grid layout for buttons, columns:

   ServoNumber  ServoMin   ServoMax  Current Value  Low   High  Toggle

New button class?
    It will know what row it's in, maybe row == servo #


    Buttons need to:

        Low - set value low
        High - set value high
        Toggle - check if it's high/low and toggle to other

    ServoNumber/ServoMin/ServoMax are static

    Current value needs to be updated as the serv value changes

Only needs to affect servo values for a particulare vehicle, doesn't need any knowledge of other vehicles



"""

<<<<<<< HEAD
=======


>>>>>>> Initial commit for servos widget file
=======
>>>>>>> Initial layout attempt, empty set servo method


class GCSWidgetServos (GCSWidget):

    widgetName = "Servos"

    def __init__(self, state, parent):
        super(GCSWidgetServos, self).__init__(state, parent)
        self.setObjectName("GCSWidgetServos")
        self.set_datasource_allowable(WidgetDataSource.SINGLE)
<<<<<<< HEAD
<<<<<<< HEAD
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


       # self.refresh()
        #self.show()
=======
        self.label_altitude = QLabel("0", self)
        self.label_airspeed = QLabel("0", self)
        self.label_throttle = QLabel("0", self)
        self.label_heading = QLabel("0", self)
        self.label_climbrate = QLabel("0", self)
=======
        servo_grid = QGridLayout()
        self.setLayout(servo_grid)


        for servo_num in range (0, self.numServos):

            servo_name = QLabel(servo_num, self)
            servo_grid.addWidget(servo_name, 0, servo_num)

            servo_Min = QPushButton("Set Low: %d" % (self.focused_object.mav_param['RC%d_MIN' % (servo_num+5)]))
            servo_Min.clicked().connect(self.set_Servo(servo_num + 5,self.focused_object.mav_param['RC%d_Min' % (servo_num+5)]))
            servo_grid.addWidget(servo_Min, 1, servo_num)

            servo_Max = QPushButton("Set High: %d" % (self.focused_object.mav_param['RC%d_MAX' % (servo_num+5)]))
            servo_Max.clicked().connect(self.set_Servo(servo_num + 5,self.focused_object.mav_param['RC%d_Min' % (servo_num+5)]))
            servo_grid.addWidget(servo_Max, 2, servo_num)

            servo_Current = QLabel("Waiting", self)
            servo_grid.addWidget(servo_Current, 3, servo_num)


>>>>>>> Initial layout attempt, empty set servo method
        self.refresh()
>>>>>>> Initial commit for servos widget file

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
>>>>>>> Initial layout attempt, empty set servo method
