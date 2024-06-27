from datetime import datetime, date
from PyQt6.QtWidgets import QLineEdit, QWidget, QComboBox, QHBoxLayout, QLabel
from PyQt6.QtGui import QIntValidator, QDoubleValidator
# from PyQt6.QtGui.QDoubleValidator import StandardNotation


class MinWidthLabel(QLabel):
    def __init__(self, text):
        super(MinWidthLabel, self).__init__(text)
        self.setFixedWidth(self.sizeHint().width())


class Entry(QLineEdit):
    def __init__(self, parent=None, limit_size: int = None):
        super(Entry, self).__init__(parent)

        if limit_size is not None:
            self.setFixedWidth(limit_size)

        self.setStyleSheet(
            'QLineEdit[readOnly="true"] {color: #808080; background-color: #F0F0F0;}'
        )
        self.setStyleSheet('*[invalid="true"]{background-color:red;}')

    def text(self):
        if super().text() is None:
            return ""

        return super().text()

    def setText(self, t):
        if t is None:
            super().setText("")
        else:
            super().setText(str(t))


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
        self.setFixedWidth(80)


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

        # self.setMaxLength(4)
        self.setFixedWidth(30)
        # self.setValidator(QDoubleValidator(min, max, num_decimal_places))
        # _dv=QDoubleValidator(0.0, 9.9, 1)
        _dv = QDoubleValidator(min, max, num_decimal_places)
        _dv.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.setValidator(_dv)


class DateEntry(QWidget):
    def __init__(self, parent):
        super(DateEntry, self).__init__(parent)

        _layout = QHBoxLayout()
        self._month = QComboBox()
        self._month.addItems(
            [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
        )
        _layout.addWidget(self._month)

        _now = datetime.now()

        self._year = QComboBox()
        for _i in range(_now.year - 90, _now.year - 20):
            self._year.addItem(str(_i))
        self._year.setCurrentIndex(45)
        _layout.addWidget(self._year)

        self.setLayout(_layout)

    def get_date(self) -> date:
        _month = self._month.currentIndex() + 1
        _year = self._year.currentText()

        return date(int(_year), int(_month), 15)

    def set_date(self, dt: date):
        self._month.setCurrentIndex(dt.month - 1)
        self._year.setCurrentText(str(dt.year))

    def clear(self):
        self._month.setCurrentIndex(0)
        self._year.setCurrentIndex(45)
