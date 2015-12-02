from GCSWidget import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gcs_state import *
import functools
import sys
from pymavlink import mavutil

#TODO Need to refresh after all parameters are fetched, maybe skip until they're fetched too.
#MAV data objects have parameter self.param_fetched that tells if the parameters are all fetched, can be checked before initialization
#TODO Need to figure out where messages for servos 9-16 are...
#TODO Not reading value for servo 9 in the list
#TODO implement setValue() function for us setting the servo value, will have to output mavlink message
#TODO Think about how to handle the swarms and where to make that differentiation
#TODO Think more about when/why we want to refresh the screen and what needs to happen on a refresh



class GCSWidgetServos (GCSWidget):

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
#        self.toolbar.addAction(self.action_focus_track)
        self.setWindowTitle("Mav Servos")
        self.refresh()


    def refresh(self):

        super(GCSWidgetServos, self).refresh()


        if isinstance(self._datasource, MAV):
            if self.servoList:
                self.servoList.clear()
        elif isinstance(self._datasource, Swarm):
            print ("Working")
        else:
            print ("No object")

        mylayout = QWidget()
        servo_grid = QGridLayout()
        servo_grid.setMenuBar(self.toolbar)
        mylayout.setLayout(servo_grid)
        self.setWidget(mylayout)


        for servo_num in range (self.offset, self.numServos+self.offset):

            new_servo = MAVServo(servo_num)

            # This doesn't work right now
            if isinstance(self._datasource, MAV):
                if self._datasource.param_fetched:
                    try:
                        new_servo.maxValue = self.state.focused_object.mav_param['RC%d_MAX' % (servo_num)]
                        new_servo.minValue = self.state.focused_object.mav_param['RC%d_MIN' % (servo_num)]
                        new_servo.hasData = True

                    except:
                        print ("Try failed, focused object:")
                        print self.state.focused_object
                        new_servo.hasData = False
                else:
                    print ("Parameters not yet fetched")
            elif isinstance(self._datasource, Swarm):
                print ("working")
                    # Need to figure out what a SWARM object is
                    #self.state.focused_object.
            else:
                    print ("No Object")


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

            #Need to add the current Qlabel to the class stuff so I can reference/change it's value
            new_servo.currentvalueLabel = QLabel("Waiting", self)
            servo_grid.addWidget(new_servo.currentvalueLabel, servo_num, 3)

            self.servoList[servo_num] = new_servo


    def read_settings(self, settings):
        print("Reading settings")
        #self.numServos = settings.value('num_servos')
        #TODO read_settings

    def write_settings(self, settings):
        print("Writing settings")
        #settings.setValue('num_servos', self.numServos)
        #TODO write_settings

    def check_param_initialized(self):
        print ("Parameters have been initialized, updating servo information")


       # self.refresh()
        #self.show()

# Gets called by MainWindow.forward_packets_to_widgets through self.state.mav_network.on_mavlink_packet dictionary
# This widget is added based on self.state.focused object sys id
    def process_messages(self, m):
        mtype = m.get_type()
        #print mtype

        if mtype == "SERVO_OUTPUT_RAW":
            if m.port == 0:
                print ("m.port = 0")
                if self.offset <= 8:
                    for servo_num in range(self.offset, 9):
                        valueName = "servo{}_raw".format(servo_num)
                        self.servoList[servo_num].update_value(getattr(m, valueName))
                        print valueName
                        print getattr(m, valueName)

                else:
                    pass
            elif m.port == 1:
                print ("m.port = 1")
                startPoint = 9
                if self.offset > 8:
                    startPoint = self.offset
                for servo_num in range(startPoint, self.numServos+(self.offset-1)):
                    valueName = "servo{}_raw".format(servo_num - 8)
                    self.servoList[servo_num].update_value(getattr(m, valueName))
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
        self.currentvalueLabel = QLabel()



    def update_value(self, value):
# It breaks here because there is no max value being set

        if self.hasData:
            if value is not None:
                self.currentValue = value
                self.currentvalueLabel.setText("{}".format(value))

            if not self.hasData and self.currentValue is not None:
                self.hasData = True

            if self.hasData:
                if self.currentValue >= self.maxValue-200:
                    if self.currentValue >= self.maxValue - 50:
                        print self.currentValue
                        self.setStyleSheet('color: red')
                        return
                    self.setStyleSheet('color:yellow')
                elif self.currentValue <= self.minValue+200:
                    if self.currentValue <= self.minValue + 50:
                        self.setStyleSheet('color: red')
                        return
                    self.setStyleSheet('color:yellow')
                else:
                    self.setStyleSheet('color: green')
            else:
                print("No Mav, not updating, but I'm talking for servo: %d" % (self.servoNUM))
        else:
            print ("No min/max data, not updating")

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