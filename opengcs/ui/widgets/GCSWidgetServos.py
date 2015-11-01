from GCSWidget import *
from PyQt4.QtGui import *




class GCSWidgetServos (GCSWidget):

    widgetName = "Servos"

    def __init__(self, state, parent):
        super(GCSWidgetServos, self).__init__(state, parent)
        self.setObjectName("GCSWidgetServos")
        self.set_datasource_allowable(WidgetDataSource.SINGLE)
        self.init_ui()

    def init_ui(self):

        self.label_altitude = QLabel("0", self)
        self.label_airspeed = QLabel("0", self)
        self.label_throttle = QLabel("0", self)
        self.label_heading = QLabel("0", self)
        self.label_climbrate = QLabel("0", self)
        self.refresh()

    def refresh(self):

        super(GCSWidgetServos, self).refresh()
        w = self.geometry().width()
        h = self.geometry().height()

        self.label_altitude.move(5, h/2-10)
        self.label_airspeed.move(w-25, h/2-10)
        self.label_throttle.move(5, 20)
        self.label_heading.move(w/2 - 10, 50)
        self.label_climbrate.move(w-25,20)

        self.setWindowTitle("GCSWidgetServos")
        self.setMinimumSize(200, 200)
