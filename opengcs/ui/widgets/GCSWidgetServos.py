from GCSWidget import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gcs_state import *
import functools
import sys
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

class GCSWidgetServos (GCSWidget):

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

    def init_ui(self):


        self.setWindowTitle("Mav Servos")
        self.refresh()


    def refresh(self):

        super(GCSWidgetServos, self).refresh()

        mylayout = QWidget()
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




    def read_settings(self, settings):
        print("Reading settings")
        self.numServos = settings.value('num_servos')
        #TODO read_settings

    def write_settings(self, settings):
        print("Writing settings")
        settings.setValue('num_servos', self.numServos)
        #TODO write_settings


    def set_Servo(self, servo, value):

        # set servo value

        print("Setting Servo: %d, to value: %d" % (servo, value))



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






