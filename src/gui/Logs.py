from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout
from PyQt6.QtCore import QT_VERSION_STR, PYQT_VERSION_STR

import sys

class Logs(QWidget):
  def __init__(self, parent=None):
      super(Logs, self).__init__(parent)
      
      self.log=QPlainTextEdit()
      
      mainLayout = QVBoxLayout()
      mainLayout.addWidget(self.log)
      self.setLayout(mainLayout)
      
      _str="Python Version=%s\nQt Version=%s\nPyQt Version=%s\n" % (sys.version, QT_VERSION_STR, PYQT_VERSION_STR)
      self.log.setPlainText(_str)
      
  def append(self, text):
      #fix me?
      _text=self.log.toPlainText()
      _text+=text
      self.log.setPlainText(_text)