from datetime import datetime, date
from enum import Enum, StrEnum

from PyQt6.QtWidgets import QLineEdit, QWidget, QComboBox, QHBoxLayout, QLabel
from PyQt6.QtGui import QIntValidator, QDoubleValidator

from ...EnumTypes import (
    AccountOwnerType,
    PersonType,
    RelationStatusType,
    WithdrawOrderType,
    FederalTaxStatusType,
)


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

        self.setValidator(QIntValidator(parent))

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


class IntegerRangeEntry(IntegerEntry):
    def __init__(self, parent=None, min=0, max=99, limit_size=30):
        super(IntegerRangeEntry, self).__init__(parent=parent)

        self.setFixedWidth(limit_size)
        self.setValidator(QIntValidator(bottom=min, top=max, parent=self))


class AgeEntry(IntegerEntry):
    def __init__(self, parent=None, min=0, max=99):
        super(AgeEntry, self).__init__(parent=parent)

        self.setFixedWidth(30)
        self.setValidator(QIntValidator(bottom=min, top=max, parent=self))


class YearEntry(IntegerEntry):
    def __init__(self, parent=None, min=1920, max=2099):
        super(YearEntry, self).__init__(parent=parent)

        self.setFixedWidth(60)
        self.setValidator(QIntValidator(bottom=min, top=max, parent=self))


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

    def set(self, value):
        self.setText(value)


class PercentEntry(FloatEntry):
    def __init__(self, parent=None, min=0.0, max=9.9, num_decimal_places: int = 1):
        super(PercentEntry, self).__init__(parent, min, max, num_decimal_places)

        self.setFixedWidth(30)
        _dv = QDoubleValidator(min, max, num_decimal_places)
        _dv.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.setValidator(_dv)


class EnumEntry(QWidget):
    def __init__(self, enum_type: StrEnum, parent=None, limit_size: int = None):
        # def __init__(self, parent, enum_type: Enum):
        super(EnumEntry, self).__init__(parent)

        if limit_size is not None:
            self.setFixedWidth(limit_size)

        _layout = QHBoxLayout()
        self._widget = QComboBox()

        # print(enum_type)
        # assert isinstance(enum_type, StrEnum)
        self._enum = enum_type
        self._widget.addItems(self._list_members(self._enum))

        _layout.addWidget(self._widget)
        self.setLayout(_layout)

    @property
    def currentIndexChanged(self):
        return self._widget.currentIndexChanged

    def currentText(self) -> str:
        return self._widget.currentText()

    def setEnabled(self, flag: bool) -> None:
        self._widget.setEnabled(flag)

    def isEnabled(self) -> bool:
        return self._widget.isEnabled()

    def enumValue(self):
        """return the enum member value"""
        return self._enum(self._widget.currentText())

    def setCurrentIndex(self, index: int) -> None:
        self._widget.setCurrentIndex(index)

    def setCurrentText(self, member: StrEnum) -> None:
        if isinstance(member, str):
            self._widget.setCurrentText(member)
        else:
            self._widget.setCurrentText(member.name)

    def _list_members(self, enum: Enum) -> [str]:
        return [member.value for member in enum]

    def set(self, item: Enum) -> None:
        if isinstance(item, StrEnum):
            self._widget.setCurrentText(item.value)
        if isinstance(item, str):
            self._widget.setCurrentText(item)
        else:
            print(
                "EnumEntry: %s Error, invalid item (%s) for set function"
                % (self._enum, type(item))
            )

    def get(self) -> StrEnum:
        return self._enum(self._widget.currentText())

    def clear(self):
        self._widget.setCurrentIndex(0)


class RelationStatusTypeEntry(EnumEntry):
    def __init__(self, parent=None, limit_size: int = None):
        super(RelationStatusTypeEntry, self).__init__(
            RelationStatusType,
            parent=parent,
            limit_size=100 if limit_size is None else limit_size,
        )


class AccountOwnerTypeEntry(EnumEntry):
    def __init__(self, parent=None, limit_size: int = None):
        super(AccountOwnerTypeEntry, self).__init__(
            AccountOwnerType,
            parent=parent,
            limit_size=100 if limit_size is None else limit_size,
        )


class PersonTypeEntry(EnumEntry):
    def __init__(self, parent=None, limit_size: int = None):
        super(PersonTypeEntry, self).__init__(
            PersonType,
            parent=parent,
            limit_size=100 if limit_size is None else limit_size,
        )


class WithdrawOrderEntry(EnumEntry):
    def __init__(self, parent=None, limit_size: int = None):
        super(WithdrawOrderEntry, self).__init__(
            WithdrawOrderType,
            parent=parent,
            limit_size=250 if limit_size is None else limit_size,
        )


class FederalTaxStatusEntry(EnumEntry):
    def __init__(self, parent=None, limit_size: int = None):
        super(FederalTaxStatusEntry, self).__init__(
            FederalTaxStatusType,
            parent=parent,
            limit_size=200 if limit_size is None else limit_size,
        )


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
