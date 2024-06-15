import logging
logger = logging.getLogger(__name__)
from PyQt6.QtWidgets import QMainWindow, QTabWidget
from PyQt6.QtWidgets import QToolBar, QStatusBar

from MenuBar import MenuBar
from Inputs import InputsTab
from Logs import Logs
from Analysis import AnalysisTab

class Main(QMainWindow):
  def __init__(self, parent=None):
      super(Main, self).__init__(parent)
      
      logger.debug("starting Main Window")
      tabWidget=QTabWidget()
      self.InputsTab=InputsTab()
      self.AnalysisTab=AnalysisTab()
      self.LogsTab=Logs()
      
      tabWidget.addTab(self.InputsTab, "Input")
      tabWidget.addTab(self.AnalysisTab, "Analysis")
      tabWidget.addTab(self.LogsTab, "Logs")

      self.setCentralWidget(tabWidget)
      
      self.setWindowTitle("Wealth Manager v0.1 alpha")
      self.resize(800, 600)
      
      #_toolbar=QToolBar("My main toolbar")
      #self.addToolBar(_toolbar)
      
      _statusbar=QStatusBar(self)
      self.setStatusBar(_statusbar)
      
      self._createMenuBar()
      self.show()
      logger.debug("ending Main Window")
      
  def _createMenuBar(self):
      _mb=MenuBar(self)
      self.menubar=_mb.get_menubar()
      
if __name__ == '__main__':
   import sys
   from PyQt6.QtWidgets import QApplication

   _app = QApplication(sys.argv)
   _main = Main()
   sys.exit(_app.exec())