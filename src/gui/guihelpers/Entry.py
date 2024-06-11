from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, \
                            QFormLayout, QLineEdit, QComboBox
from PyQt6.QtGui import QIntValidator, QDoubleValidator

class AgeEntry(QLineEdit):
  def __init__(self, parent=None, limit_size:bool=True):
      super(AgeEntry, self).__init__(parent)
      
      self.setMaxLength(2)
      if limit_size:
          self.setFixedWidth(30)
      
      self.setValidator(QIntValidator())
      
class FloatEntry(QLineEdit):
  def __init__(self, parent=None, min=0.0, max=10.0, num_decimal_places=1, limit_size:bool=True):
      super(FloatEntry, self).__init__(parent)
      
      self.setMaxLength(4)
      if limit_size:
          self.setFixedWidth(30)
      
      self.setValidator(QDoubleValidator(min, max, num_decimal_places))
    