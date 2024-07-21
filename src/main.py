from PyQt6.QtWidgets import QMainWindow, QTabWidget
from PyQt6.QtWidgets import QStatusBar
from PyQt6.QtGui import QIcon

from gui.MenuBar import MenuBar
from gui.Inputs import InputsTab
from gui.Logs import Logs
from gui.Analysis import AnalysisTab

from libs.Version import APP_VERSION

# this will allow the app window under Windows OS to display a custom icon
try:
    from ctypes import windll  # Only exists on Windows.

    windll.shell32.SetCurrentProcessExplicitAppUserModelID("WealthMan")
except ImportError:
    pass

import os
import logging

logger = logging.getLogger(__name__)

basename = os.path.dirname(__file__)


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.__version__ = APP_VERSION
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

        # self.setWindowIcon(QIcon("resources/app.ico"))

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
    _app.setWindowIcon(QIcon(os.path.join(basename, "resources/app.ico")))

    _main = Main()
    if getattr(sys, "frozen", False):  # this is running via pyinstaller
        import pyi_splash

        pyi_splash.close()

    sys.exit(_app.exec())
