from logging.handlers import RotatingFileHandler
import platform
import sys

from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QComboBox, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QT_VERSION_STR, PYQT_VERSION_STR, Qt

import logging
logger = logging.getLogger(__name__)

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

class Logs(QWidget):
  def __init__(self, parent=None):
      super(Logs, self).__init__(parent)
      
      self.logger=QTextEditLogger(self)
      self._formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s;%(module)s.%(funcName)s:%(lineno)s - %(message)s')
      self.logger.setFormatter(self._formatter)
      
      logging.getLogger().addHandler(self.logger)
      
      #also log to file just in case there is a segfault, etc..
      _file=RotatingFileHandler("logs.log", maxBytes=1024*1024, backupCount=9)
      _file.setFormatter(self._formatter)
      logging.getLogger().addHandler(_file)
      
      # You can control the logging level
      logging.getLogger().setLevel(logging.ERROR)

      mainLayout = QVBoxLayout()
      self._level=QComboBox()
      self._level.addItems(["All", "Debug", "Info", "Warning", "Error", "Critical"])
      self._level.setCurrentText("Error")
      self._level.currentIndexChanged.connect(self._levelChange)
      
      _clear=QPushButton("Clear", self)
      _clear.setFixedSize(60,30)
      _clear.clicked.connect(self.reset_log)
      
      _layout=QHBoxLayout()
      _layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
      _layout.addWidget(QLabel("Logging Level:"))
      _layout.addWidget(self._level)
      _layout.addStretch()
      _layout.addWidget(_clear)
     
      mainLayout.addLayout(_layout)
      mainLayout.addWidget(self.logger.widget)
      self.setLayout(mainLayout)
      
      self.reset_log()
      
  def _levelChange(self):
      _value=self._level.currentText().upper()
      if _value == "ALL":
         logging.getLogger().setLevel("NOTSET")
      else:
         logging.getLogger().setLevel(_value)
        
         #self.parent.setStatusText="Setting logging level to %s" % _value
     
  def reset_log(self):
      self.logger.widget.clear()
      _system_info="OS=%s\nPython Version=%s\nQt Version=%s\nPyQt Version=%s\n" % (platform.uname(), sys.version, QT_VERSION_STR, PYQT_VERSION_STR)
      logger.log(99, _system_info)
      