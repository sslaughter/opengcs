from GCSWidget import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
import fnmatch

# TODO need a clear architecture for reloading data, refreshing view, applyin filter and conditional formatting
# TODO move filter and buttons from an hbox into a toolbar (see GCSWidgetMAVNetwork)
# TODO Hide grid row number
# TODO Does not populate with values when a mav is first connected and parameter download completes


class GCSWidgetParameterList (GCSWidget):

    widget_name_plaintext = "ParameterList"

    def __init__(self, state, parent):

        super(GCSWidgetParameterList, self).__init__(state, parent)
        self.setWindowTitle("Parameter List")
        self.setMinimumSize(150, 150)
        self.set_datasource_allowable(WidgetDataSource.SINGLE)

        self.all_params = []
        self.filtered_params = []

        self.init_ui()
        self.refresh()

    def init_ui(self):

        self.table_params = QTableWidget(0,2,self)
        self.table_params.setHorizontalHeaderLabels(['Parameter','Value'])
        self.table_params.horizontalHeader().setResizeMode(0,QHeaderView.Stretch)
        self.table_params.horizontalHeader().setResizeMode(1,QHeaderView.ResizeToContents)
        self.table_params.verticalHeader().setVisible(False)

        self.lineedit_filter = QLineEdit()
        self.lineedit_filter.textChanged.connect(self.on_filter_changed)
        self.button_settings = QPushButton('...')

        # Create toolbar
        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QtCore.QSize(16,16))
        self.toolbar.addWidget(self.lineedit_filter)
        self.toolbar.addWidget(self.button_settings)

        vbox = QVBoxLayout()
        vbox.addWidget(self.table_params)
        vbox.setMenuBar(self.toolbar)

        mylayout = QWidget()
        mylayout.setLayout(vbox)
        self.setWidget(mylayout)

        return

    def on_filter_changed(self):

        self.apply_filter()

    def refresh(self):

        super(GCSWidgetParameterList, self).refresh()

        self.table_params.clearContents()

        if self._datasource is None:
            return

        mav = self._datasource
        self.all_params = mav.mav_param

        self.table_params.setRowCount(mav.mav_param_count)
        row = 0
        for key in mav.mav_param:
            self.table_params.setItem(row,0,QTableWidgetItem(key))
            self.table_params.setItem(row,1,QTableWidgetItem(str(mav.mav_param[key])))
            row = row + 1

        self.table_params.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def apply_filter(self):
        pattern = str(self.lineedit_filter.text())

        if self.table_params.rowCount() == 0:
            return
        for i in range(0,self.table_params.rowCount()):
            if len(fnmatch.filter([self.table_params.item(i,0).text()], pattern)) > 0:
                self.table_params.setRowHidden(i, False)
            else:
                self.table_params.setRowHidden(i,True)


    # def mav_changed(self):
    #     mav = self.state.focused_mav
    #     mav.on_params_initialized.append(self.refresh)
    #     self.refresh()



