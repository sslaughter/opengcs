from GCSWidget import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gcs_state import *
import functools
import sys
from pymavlink import mavutil




class GCSWidgetServos (GCSWidget):

    widget_name_plaintext = "Servos"

    def __init__(self, state, parent):
        super(GCSWidgetServos, self).__init__(state, parent)
        self.setObjectName("GCSWidgetServos")
        self.setWindowTitle("Servos")
        self.set_datasource_allowable(WidgetDataSource.SINGLE | WidgetDataSource.SWARM)



        self.numServos = 2
        self.offset = 2
        self.servoList = {}
        self.init_ui()

    def init_ui(self):

        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(16,16))

        self.action_focus_track = QAction('&Track     Main', self)
        self.action_focus_track.setStatusTip('Track Independent')
        self.action_focus_track.setToolTip('Toggle tracking main object')
        self.action_focus_track.setCheckable(True)
        self.action_focus_track.triggered.connect(self.on_action_focus_track)


        '''
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
        self.toolbar.addAction(self.action_focus_track)
        self.setWindowTitle("Mav Servos")
        self.refresh()


    def refresh(self):

        super(GCSWidgetServos, self).refresh()

        if self.servoList:
            self.servoList.clear()

        mylayout = QWidget()
        servo_grid = QGridLayout()
        servo_grid.setMenuBar(self.toolbar)
        mylayout.setLayout(servo_grid)
        self.setWidget(mylayout)
        #TODO ^^ figure out why I have to set that in the function


        for servo_num in range (self.offset, self.numServos+self.offset):

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
        #self.numServos = settings.value('num_servos')
        #TODO read_settings

    def write_settings(self, settings):
        print("Writing settings")
        #settings.setValue('num_servos', self.numServos)
        #TODO write_settings


    def set_Servo(self, servo, value):

        # set servo value

        print("Setting Servo: %d, to value: %d" % (servo, value))

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

    def __init__(self, servo_number, parent):

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






