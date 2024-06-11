from PyQt6.QtWidgets import QMainWindow, QTabWidget
from PyQt6.QtWidgets import QToolBar, QStatusBar

from MenuBar import MenuBar
from Inputs import Inputs
from Logs import Logs
from Analysis import AnalysisTab

class Main(QMainWindow):
  def __init__(self, parent=None):
      super(Main, self).__init__(parent)
      
      tabWidget=QTabWidget()
      self.Inputs=Inputs()
      tabWidget.addTab(self.Inputs, "Input")
      tabWidget.addTab(AnalysisTab(), "Analysis")
      tabWidget.addTab(Logs(), "Logs")

      self.setCentralWidget(tabWidget)
      
      self.setWindowTitle("Wealth Manager v0.1 alpha")
      self.resize(800, 600)
      
      _toolbar=QToolBar("My main toolbar")
      self.addToolBar(_toolbar)
      
      _statusbar=QStatusBar(self)
      self.setStatusBar(_statusbar)
      
      self._createMenuBar()
      self.show()
      
  def _createMenuBar(self):
      _mb=MenuBar(self)
      self.menubar=_mb.get_menubar()
      
if __name__ == '__main__':
   from PyQt6.QtWidgets import QApplication
   import sys
   
   _app = QApplication(sys.argv)
   _main = Main()
   sys.exit(_app.exec())