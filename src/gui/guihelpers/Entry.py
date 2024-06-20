from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QIntValidator, QDoubleValidator

class Entry(QLineEdit):
    def __init__(self, parent, limit_size: int = None):
        super(Entry, self).__init__(parent)
                
        if limit_size is not None:
           self.setFixedWidth(limit_size)
                 
        self.setStyleSheet('QLineEdit[readOnly="true"] {color: #808080; background-color: #F0F0F0;}')
        self.setStyleSheet('*[invalid="true"]{background-color:red;}')
      

class IntegerEntry(Entry):
    def __init__(self, parent=None, limit_size: int = None):
        super(IntegerEntry, self).__init__(parent)

        self.setValidator(QIntValidator())

    def is_valid(self):
        try:
            int(self.text())
            return True
        except ValueError:
            return False

    def get_int(self):
        if self.is_valid():
           return int(self.text())

        return None

class AgeEntry(IntegerEntry):
    def __init__(self, parent=None):
        super(AgeEntry, self).__init__(parent)

        self.setFixedWidth(30)
        self.setValidator(QIntValidator(0, 99))

        self.setStyleSheet('*[invalid="true"] {background-color:red;}')
      

class MoneyEntry(IntegerEntry):
    def __init__(self, parent=None):
        super(MoneyEntry, self).__init__(parent, limit_size=80)


class FloatEntry(Entry):
    def __init__(
        self,
        parent=None,
        min=0.0,
        max=10.0,
        num_decimal_places=1,
        limit_size: int = None,
    ):
        super(FloatEntry, self).__init__(parent)

        #self.setMaxLength(4)
        if limit_size is not None:
            self.setFixedWidth(limit_size)

        self.setValidator(QDoubleValidator(min, max, num_decimal_places))

    def is_valid(self):
        try:
            float(self.text())
            return True
        except ValueError:
            return False

    def get_float(self):
        if self.is_valid():
           return float(self.text())
        return None

class PercentEntry(FloatEntry):
    def __init__(self, parent=None, min=0.0, max=9.9, num_decimal_places: int = 1):
        super(PercentEntry, self).__init__(parent, min, max, num_decimal_places)

        self.setMaxLength(4)
        self.setFixedWidth(30)