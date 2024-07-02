from PyQt6.QtWidgets import QMainWindow, QTabWidget
from PyQt6.QtWidgets import QStatusBar
from PyQt6.QtGui import QIcon

from MenuBar import MenuBar
from Inputs import InputsTab
from Logs import Logs
from Analysis import AnalysisTab

import logging

logger = logging.getLogger(__name__)

__version__ = "0.1 alpha"


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.__version__ = __version__
        self.title = "Wealth Manager v%s" % self.__version__

        logger.debug("starting Main Window")
        self.tabs = QTabWidget()
        self.InputsTab = InputsTab(self)
        self.AnalysisTab = AnalysisTab(self)
        self.LogsTab = Logs(self)

        self.tabs.currentChanged.connect(self.onTabChange)
        self.tabs.addTab(self.InputsTab, "Input")
        self.tabs.addTab(self.AnalysisTab, "Analysis")
        self.tabs.addTab(self.LogsTab, "Logs")
        self.toggleLogTab()

        self.showAnalysisTab(False)
        self.setCentralWidget(self.tabs)

        self.setWindowTitle(self.title)
        self.resize(1024, 800)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self._createMenuBar()

        self.setWindowIcon(QIcon("resources/icons8-w-67.png"))

        self.show()
        logger.debug("ending Main Window")

    def toggleLogTab(self):
        self.tabs.setTabVisible(2, not self.tabs.isTabVisible(2))

    def showAnalysisTab(self, flag: bool):
        self.tabs.setTabEnabled(1, flag)

        if flag:
            self.AnalysisTab.reset()
            self.tabs.setCurrentIndex(1)
            self.AnalysisTab.tabs.setCurrentIndex(0)

    def _createMenuBar(self):
        self.menubar = MenuBar(self)
        _menubar = self.menubar.get_menubar()

    def onTabChange(self, i):
        _tabName = self.tabs.tabText(i)

        if _tabName == "Input":
            self.showAnalysisTab(False)

        self._previous_tab_name = _tabName


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    _app = QApplication(sys.argv)
    _main = Main()
    sys.exit(_app.exec())
