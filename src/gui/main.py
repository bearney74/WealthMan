from PyQt6.QtWidgets import QMainWindow, QTabWidget
from PyQt6.QtWidgets import QStatusBar
from PyQt6.QtGui import QIcon

from MenuBar import MenuBar
from Inputs import InputsTab
from Logs import Logs
from Analysis import AnalysisTab

from libs.DataVariables import DataVariables
from libs.Projections import Projections

import logging

logger = logging.getLogger(__name__)


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.title="Wealth Manager v0.1 alpha"
        self.projectionData = None

        logger.debug("starting Main Window")
        self.tabs = QTabWidget()
        self.InputsTab = InputsTab(self)
        self.AnalysisTab = AnalysisTab(self)
        self.LogsTab = Logs(self)

        self.tabs.currentChanged.connect(self.onTabChange)
        self.tabs.addTab(self.InputsTab, "Input")
        self.tabs.addTab(self.AnalysisTab, "Analysis")
        self.tabs.addTab(self.LogsTab, "Logs")

        self.setCentralWidget(self.tabs)

        self.setWindowTitle(self.title)
        self.resize(1024, 800)

        _statusbar = QStatusBar(self)
        self.setStatusBar(_statusbar)

        self._createMenuBar()

        self.setWindowIcon(QIcon("resources/icons8-w-67.png"))

        self.show()
        logger.debug("ending Main Window")

    def _createMenuBar(self):
        _mb = MenuBar(self)
        self.menubar = _mb.get_menubar()

    def onTabChange(self, i):
        _tabName = self.tabs.tabText(i)
        # print(_tabName)
        if _tabName == "Analysis":
            dv = DataVariables()

            self.InputsTab.BasicInfoTab.export_data(dv)
            self.InputsTab.IncomeInfoTab.export_data(dv)
            self.InputsTab.ExpenseInfoTab.export_data(dv)
            self.InputsTab.AssetInfoTab.export_data(dv)
            self.InputsTab.GlobalVariablesTab.export_data(dv)
            _p = Projections(dv)
            self.projectionData = _p.execute()

        self._previous_tab_name = _tabName


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    _app = QApplication(sys.argv)
    _main = Main()
    sys.exit(_app.exec())
