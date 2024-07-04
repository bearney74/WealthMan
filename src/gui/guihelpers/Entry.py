from datetime import datetime, date
from PyQt6.QtWidgets import QLineEdit, QWidget, QComboBox, QHBoxLayout, QLabel
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QValidator


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

    def get_int(self, Default=None):
        if self.text() is None or self.text().strip() == "":
            return Default

        if self.is_valid():
            return int(self.text())

        return None


class IntRangeValidator(QIntValidator):
    def __init__(self, parent, min, max):
        super(IntRangeValidator, self).__init__()
        self.parent = parent
        self.min = min
        self.max = max

    def validate(self, string, pos):
        try:
            _int = int(string)
            _ok = True
        except ValueError:
            _ok = False

        if pos < len("%s" % self.min) and pos < len("%s" % self.max):
            self.parent.setStyleSheet("color: red")
            return (QValidator.State.Intermediate, string, pos)

        if _ok and _int >= self.min and _int <= self.max:
            self.parent.setStyleSheet("color: black")
            return (QValidator.State.Acceptable, string, pos)

        return (QValidator.State.Invalid, string, pos)


class AgeEntry(IntegerEntry):
    def __init__(self, parent=None, min=0, max=99):
        super(AgeEntry, self).__init__(parent=parent)

        self.parent = parent
        self.setFixedWidth(30)
        self.setValidator(IntRangeValidator(self, min, max))


class MoneyEntry(IntegerEntry):
    # parts copied from https://github.com/yjg30737/pyqt-number-lineedit/blob/main/pyqt_number_lineedit/numberLineEdit.py
    def __init__(self, parent=None):
        super(MoneyEntry, self).__init__(parent, limit_size=80)
        self.setFixedWidth(80)

        self.__comma_enabled = True
        self.textEdited.connect(self.__textEdited)

    def __textEdited(self, text):
        if self.__comma_enabled:
            self.setCommaToText()

    def setComma(self, f: bool):
        self.__comma_enabled = f
        self.setCommaToText()

    def setCommaToText(self):
        text = IntegerEntry.text(self)
        cur_pos = self.cursorPosition()
        if text:
            if self.__comma_enabled:
                if text.startswith("$"):
                    text = text[1:]
                text = text.replace(",", "")
                if text.find(".") == -1:
                    if text == "":
                        IntegerEntry.setText(self, "")
                    else:
                        IntegerEntry.setText(self, "${:,}".format(int(text)))
                else:
                    pre_dot, post_dot = text.split(".")
                    text = "${:,}".format(int(pre_dot)) + "." + post_dot
                    IntegerEntry.setText(self, text)
                self.setCursorPosition(cur_pos + 1)
            else:
                self.setText(text.replace(",", ""))

    def setText(self, text):
        IntegerEntry.setText(self, text)
        self.setCommaToText()

    def text(self):
        _text = IntegerEntry.text(self)
        if _text.startswith("$"):
            _text = _text[1:]
        return _text.replace(",", "")


class FloatEntry(Entry):
    def __init__(
        self,
        parent=None,
        min=0.0,
        max=10.0,
        num_decimal_places=1,
        limit_size: int = None,
        Default: float = None,
    ):
        super(FloatEntry, self).__init__(parent)

        self.default = Default
        if limit_size is not None:
            self.setFixedWidth(limit_size)

        self.setValidator(QDoubleValidator(min, max, num_decimal_places))

    def is_valid(self):
        try:
            float(self.text())
            return True
        except ValueError:
            return False

    def get_float(self, Default=None):
        if self.text() is None or self.text().strip() == "":
            return Default

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
