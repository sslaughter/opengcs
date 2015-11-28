from GCSWidget import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gcs_state import *
import functools
import sys
from PyQt4 import QtCore

from PyQt4.QtCore import *
import sys

<<<<<<< HEAD

class GCSWidgetServos (GCSWidget):

    widgetName = "Servos"

<<<<<<< HEAD
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
=======
#Need to handle swarms
>>>>>>> Small changes before rebase w/ master

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
<<<<<<< HEAD
            try:
                self.state.focused_object.mav_param
                servo_Min = QPushButton("Set Low: %d" % (QString.number(self.state.focused_object.mav_param['RC%d_MIN' % (servo_num+5)])))
                servo_Min.clicked.connect(self.set_Servo(servo_num + 5,self.state.focused_object.mav_param['RC%d_Min' % (servo_num+5)]))
            except:
                servo_Min = QPushButton("Set Low: NO MAV!")

            servo_grid.addWidget(servo_Min, servo_num, 1)
=======
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


# Currently working on adding toolbar items - tracking certain mavs, settings
# Need to implement process_messages() - see HUD
# Need to handle swarms
#Think about possible way to better handle message forwarding
>>>>>>> Initial attempt at process_messages() implementation, incomplete toolbar addition
=======

>>>>>>> Small fixes, including to the self.numservos set, error ocurred in write/read settings functions

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
        self.set_datasource_allowable(WidgetDataSource.SINGLE | WidgetDataSource.SWARM)



        self.numServos = 7
        self.offset = 5
        self.servoList = {}
        self.init_ui()
<<<<<<< HEAD
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

=======

    def init_ui(self):

        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(16,16))
        '''
        self.action_focus_track = QAction('&Track     Main', self)
        self.action_focus_track.setStatusTip('Track Independent')
        self.action_focus_track.setToolTip('Toggle tracking main object')
        self.action_focus_track.setCheckable(True)
        self.action_focus_track.triggered.connect(self.on_action_focus_track)



        self.action_filter = QAction(QIcon(gcsfile('art/16x16/filter.png')), '&Filter', self)
        self.action_filter.setStatusTip('Filter messages by type')
        self.action_filter.setToolTip('Filter messages by type')
        self.action_filter.triggered.connect(self.on_button_filter)

        self.action_settings = QAction(QIcon(gcsfile('art/16x16/settings.png')), '&Settings', self)
        self.action_settings.setStatusTip('Edit widget settings')
        self.action_settings.setToolTip('Edit widget settings')
        self.action_settings.triggered.connect(self.on_button_settings)
        '''

        self.toolbar.addSeparator()
<<<<<<< HEAD
        self.toolbar.addAction(self.action_focus_track)
>>>>>>> Initial attempt at process_messages() implementation, incomplete toolbar addition
=======
#        self.toolbar.addAction(self.action_focus_track)
>>>>>>> Small bug fix in class call
        self.setWindowTitle("Mav Servos")
        self.refresh()


    def refresh(self):

        super(GCSWidgetServos, self).refresh()

<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> Moved to MAVServo class implementation
=======
        if self.servoList:
            self.servoList.clear()
=======

        if self.get_datasource() == WidgetDataSource.SINGLE:
            if self.servoList:
                self.servoList.clear()
        if self.get_datasource() == WidgetDataSource.SWARM:
            print ("Working")
>>>>>>> Small changes before rebase w/ master

>>>>>>> Small fixes, including to the self.numservos set, error ocurred in write/read settings functions
        mylayout = QWidget()
>>>>>>> Refine grid, add import into mainwindow.py to allow using the servos widget, add to default perspective to make it show up by default
        servo_grid = QGridLayout()
        servo_grid.setMenuBar(self.toolbar)
        mylayout.setLayout(servo_grid)
        self.setWidget(mylayout)


        for servo_num in range (self.offset, self.numServos+self.offset):

            new_servo = MAVServo(servo_num)
            try:
                if self.get_datasource() == WidgetDataSource.SINGLE:

                    self.state.focused_object.mav_param
                    new_servo.hasData = True
                    new_servo.maxValue = self.state.focused_object.mav_param['RC%d_MAX' % (servo_num+self.offset)]
                    new_servo.minValue = self.state.focused_object.mav_param['RC%d_MAX' % (servo_num+self.offset)]
                elif self.get_datasource() == WidgetDataSource.SWARM:
                    print ("working")
                    # Need to figure out what a SWARM object is
                    #self.state.focused_object.
                else:
                    print ("Workign")

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
<<<<<<< HEAD
        super(GCSWidgetServos, self).refresh()
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======

>>>>>>> Small changes before rebase w/ master
    def read_settings(self, settings):
        print("Reading settings")
        #self.numServos = settings.value('num_servos')
        #TODO read_settings

    def write_settings(self, settings):
        print("Writing settings")
        #settings.setValue('num_servos', self.numServos)
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

# Gets called by MainWindow.forward_packets_to_widgets through self.state.mav_network.on_mavlink_packet dictionary
# This widget is added based on self.state.focused object sys id
    def process_messages(self, m):

        mtype = m.get_type()

        if mtype == "SERVO_OUTPUT_RAW":

            if m.port == 1:
                if self.offset <= 8:
                    for servo_num in range(self.offset, 8):
                        valueName = "servo{}_raw".format(servo_num)
                        self.servoList[servo_num-self.offset].update_value(getattr(m, valueName))
                else:
                    pass
            elif m.port == 2:
                startPoint = 9
                if self.offset > 8:
                    startPoint = self.offset
                for servo_num in range(startPoint, self.numServos+(self.offset-1)):
                    valueName = "servo{}_raw".format(servo_num - 8)
                    self.servoList[servo_num-self.offset].update_value(getattr(m, valueName))
            else:
                pass
        else:
            pass








    def on_action_focus_track(self):

        if self.action_focus_track.isChecked():
            print("Now tracking main MAV")
        else:
            print("Now tracking independent MAV")



#Need to save the max/min value of each servo value, taken from parameters
#also need to be able to access labels attached to those servos
#Do we need to pass the mav object? - I don't think so

class MAVServo(QLabel):

    def __init__(self, servo_number):

        super(MAVServo, self).__init__()
        self.setText(QString.number(servo_number))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('color: green')

        self.hasData = False
        self.servoNUM = servo_number
        self.maxValue = None
        self.minValue = None
        self.currentValue = None



    def update_value(self, value):

        if value is not None:
            self.currentValue = value

        if not self.hasData and self.currentValue is not None:
            self.hasData = True

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
            print("No Mav, not updating, but I'm talking for servo: %d" % (self.servoNUM))


class SWARMServo(QLabel):

    def __init__(self, Swarm):

        super(MAVServo, self).__init__()
        self.setText(QString.number(servo_number))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('color: green')

        #Need to assign a SWARM object, likely won't need individual max/min lists
        #Does the swarm object have individual mavs saved, are their parameters accessible?
        #yes, it contains a list of Mav objects
        self.hasData = False
        self.maxValue = []
        self.minValue = []

        # Need to iterate over all servos in each mav
        for mav in Swarm.mavs:
            self.maxValue[mav] = Swarm.mavs[mav].mav_param




>>>>>>> Initial commit for servos widget file
