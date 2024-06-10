from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget

from Inputs import Inputs
from Logs import Logs

class Main(QMainWindow):
  def __init__(self, parent=None):
      super(Main, self).__init__(parent)
      #self.menubar=MenuBar(self)
      
      tabWidget=QTabWidget()
      tabWidget.addTab(Inputs(), "Input")
      tabWidget.addTab(QWidget(), "Analysis")
      tabWidget.addTab(Logs(), "Logs")

      self.setCentralWidget(tabWidget)
      
      self.setWindowTitle("Wealth Manager")
      self.resize(800, 600)
      
if __name__ == '__main__':
   from PyQt6.QtWidgets import QApplication
   import sys
   
   _app = QApplication(sys.argv)
   _main = Main()
   _main.show()
   sys.exit(_app.exec())