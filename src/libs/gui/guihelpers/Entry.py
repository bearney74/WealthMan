from datetime import datetime, date
from enum import Enum, StrEnum

from PyQt6.QtWidgets import QLineEdit, QWidget, QComboBox, QHBoxLayout, QLabel
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import Qt

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
    # to deal with focus events, we have to do the following:
    # focusInSignal = QtCore.pyqtSignal()
    # focusOutSignal = QtCore.pyqtSignal()

    def __init__(
        self,
        name: str = None,
        parent=None,
        limit_size: int = None,
        required: bool = False,
    ):
        super(Entry, self).__init__(parent)

        if name is not None:
            self.setObjectName(name)

        self._required = (
            required  # is this input widget required for input, or is it optional?
        )
        self._dependencies = []

        # to deal with focus events, we have to do the following:
        # self.focusInSignal = QtCore.pyqtSignal()
        # self.focusOutSignal = QtCore.pyqtSignal()

        if limit_size is not None:
            self.setFixedWidth(limit_size)

        self.textEdited.connect(self._on_text_change)
        # self.focusInSignal.connect(self._on_text_change)
        # self.focusOutSignal.connect(self._on_text_change)
        # self.editingFinished.connect(self._on_text_change)
        # self.editingFinished.connect(self._on_text_change)

        if required:
            self.set_highlight(True)

    def isRequired(self) -> bool:
        return self._required

    def isEmpty(self) -> bool:
        return self.text() == ""

    def focusInEvent(self, event):
        super().focusInEvent(event)
        # self.focusInSignal.emit()
        self._on_text_change()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        # self.focusOutSignal.emit()
        self._on_text_change()

    def text(self):
        if super().text() is None:  # is this ever true??
            return ""

        return super().text()

    def setText(self, t):
        if t is None:
            super().setText("")
        else:
            super().setText(str(t))

        if self.isEmpty() and self.isRequired():
            self.set_highlight(True)
        # else:
        #    self.set_highlight(False)

    def add_dependencies(self, widgets):
        """these are other widgets that self needs to create valid input for some purpose"""
        self._dependencies += widgets

    def get_dependencies(self) -> list:
        return self._dependencies

    # def is_empty(self):
    #    return self.text() == ""

    def _on_text_change(self, **args):
        # print("%s : %s" % (type(self), list(args)))
        # if we have valid input for ourself...

        # print(type(self), self.is_empty(), _validated_text)

        if self.isEmpty():
            # check to see if all other dependencies are also blank.. if so remove highlight
            # _blank_flag=True
            for widget in self._dependencies:
                if not widget._required:
                    widget.set_highlight(not widget.has_valid_input())

            # if _blank_flag:
            # self.set_highlight(True)
            #   for widget in self._dependencies:
            #       if not widget._required:
            #           widget.set_highlight(False)

            # widget.set_valid(widget._valid_input(required=True))
            # return

        # _validated_text=self.has_valid_input()

        elif self.has_valid_input():
            # check that each dependency also has valid input, if not highlight this field..
            # print("%s has valid input" % type(self))
            for widget in self._dependencies:
                if not widget.has_valid_input():
                    widget.set_highlight(True)
                else:
                    widget.set_highlight(False)

            # this isinstance has valid text so no need to highlight it.
            self.set_highlight(False)
        else:
            # print("_valid_input(required=True) is False")
            # self.set_valid(False)
            # print("%s does not have valid input" % type(self))
            # if self._valid_input(required=False):
            #  #maybe check to see if the dependencies are also empty
            for widget in self._dependencies:
                if not widget.has_valid_input():
                    widget.set_highlight(True)
                else:
                    widget.set_highlight(False)

            #  self.set_valid(True)
            # else:
            #  self.set_valid(False)

    def set_highlight(self, flag: bool) -> None:
        """sets the background color of the Entry (QLineEdit)"""
        # print("set_highight:%s -> %s" % (type(self), flag))
        if not flag:
            self.setStyleSheet("background-color: white")
            return True

        self.setStyleSheet("background-color: #ffcccc;")  # light red
        # self.setStyleSheet("color: blue; background-color: yellow; selection-color: yellow; selection-background-color: blue;")
        return False

    def has_valid_input():
        pass


class StringEntry(Entry):
    def __init__(
        self,
        name: str = None,
        parent=None,
        limit_size: int = None,
        required: bool = False,
    ):
        super(StringEntry, self).__init__(name=name, parent=parent, required=required)

        if limit_size is not None:
            self.setFixedWidth(limit_size)

    def has_valid_input(self, required: bool = False) -> bool:
        """returns False if the input is not valid"""

        return not self.isEmpty()


class IntegerEntry(Entry):
    def __init__(
        self,
        name: str = None,
        parent=None,
        min=None,
        max=None,
        limit_size: int = None,
        required: bool = False,
    ):
        super(IntegerEntry, self).__init__(name=name, parent=parent, required=required)

        if limit_size is not None:
            self.setFixedWidth(limit_size)

        if min is None:
            min = -100_000_000
        self._min = min

        if max is None:
            max = 100_000_000
        self._max = max

        assert self._min < self._max

        self.validator = QIntValidator(bottom=min, top=max, parent=parent)
        self.setValidator(self.validator)

        # self.textChanged.connect(self.check_input)

    # def is_valid(self, required:bool=False):
    #    """ checks that a field is valid, if not, highlight that field """
    #    return self.set_highlight(self._valid_input())

    def has_valid_input(self) -> bool:
        """returns False if the input is not valid"""
        """ when required variable is set to True, make sure a valid integer has been entered """
        """ when required variable is False, a '' or an integer is acceptable"""

        _text = self.text()
        # if (
        #    not required and _text.strip() == ""
        # ):  # a "" is a valid value for an optional field
        #    return True

        state, _, _ = self.validator.validate(_text, 0)

        if state == QIntValidator.State.Acceptable:
            # since IntValidator thinks this is an Acceptable value, lets turn it
            # into an int and check that it is betwen our max and min values
            try:
                _value = int(_text)
            except ValueError:
                return False

            return self._min <= _value <= self._max

        # this value is not acceptable
        return False

    def get_int(self, Default=None):
        _text = self.text()
        if _text is None or _text.strip() == "":
            return Default

        try:
            return int(_text)
        except ValueError:
            pass

        return None


class AgeEntry(IntegerEntry):
    def __init__(
        self,
        name: str = None,
        parent=None,
        min: int = 0,
        max: int = 99,
        required: bool = False,
        limit_size: bool = True,
    ):
        if limit_size:
            limit_size = 30
        else:
            limit_size = None
        super(AgeEntry, self).__init__(
            name=name,
            parent=parent,
            min=min,
            max=max,
            limit_size=limit_size,
            required=required,
        )


class YearEntry(IntegerEntry):
    def __init__(
        self,
        name: str = None,
        parent=None,
        min: int = 1920,
        max: int = 2099,
        required: bool = False,
    ):
        super(YearEntry, self).__init__(
            name=name, parent=parent, min=min, max=max, limit_size=60, required=required
        )


class MoneyEntry(IntegerEntry):
    # parts copied from https://github.com/yjg30737/pyqt-number-lineedit/blob/main/pyqt_number_lineedit/numberLineEdit.py
    def __init__(
        self,
        name: str = None,
        parent=None,
        min: int = 0,
        limit_size: int = 80,
        required: bool = False,
    ):
        super(MoneyEntry, self).__init__(
            name=name, parent=parent, min=min, limit_size=limit_size, required=required
        )
        # self.setFixedWidth(80)

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
                text = text.replace("$", "")
                # if text.startswith("$"):
                #    text = text[1:]
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
        name: str = None,
        parent=None,
        min: float = 0.0,
        max: float = 10.0,
        num_decimal_places: int = 1,
        limit_size: int = None,
        Default: float = None,
        required: bool = False,
    ):
        super(FloatEntry, self).__init__(name=name, parent=parent, required=required)

        self._min = min
        self._max = max
        self.default = Default
        if limit_size is not None:
            self.setFixedWidth(limit_size)

        self.validator = QDoubleValidator(min, max, num_decimal_places)
        self.setValidator(self.validator)

    # def is_valid(self, required:bool=False):
    #    return self.set_highlight(self._valid_input())

    def has_valid_input(self, required: bool = False):
        """returns False if the input is not valid"""

        _text = self.text()
        # if (
        #    not required and _text.strip() == ""
        # ):  # a "" is a valid value for an optional field
        #    return True

        state, _, _ = self.validator.validate(_text, 0)

        if state == QDoubleValidator.State.Acceptable:
            # since IntValidator thinks this is an Acceptable value, lets turn it
            # into an int and check that it is betwen our max and min values
            try:
                _value = float(_text)
            except ValueError:
                return False

            return self._min <= _value <= self._max

        # this value is not acceptable
        return False

    def get_float(self, Default=None):
        if self.text() is None or self.text().strip() == "":
            return Default

        try:
            return float(self.text())
        except ValueError:
            pass

        return None

    def set(self, value):
        self.setText(value)


class PercentEntry(FloatEntry):
    def __init__(
        self,
        name: str = None,
        parent=None,
        min: int = 0.0,
        max: int = 9.9,
        num_decimal_places: int = 1,
        required: bool = False,
    ):
        super(PercentEntry, self).__init__(
            name=name,
            parent=parent,
            min=min,
            max=max,
            num_decimal_places=num_decimal_places,
            required=required,
        )

        self.setFixedWidth(30)
        _dv = QDoubleValidator(min, max, num_decimal_places)
        _dv.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.setValidator(_dv)


class EnumEntry(QWidget):
    def __init__(
        self, enum_type: StrEnum, name: str = None, parent=None, limit_size: int = None
    ):
        super(EnumEntry, self).__init__(parent)

        if limit_size is not None:
            self.setFixedWidth(limit_size)

        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._widget = QComboBox()
        self._widget.setObjectName(name)

        # print(enum_type)
        # assert isinstance(enum_type, StrEnum)
        self._enum = enum_type
        self._widget.addItems(self._list_members(self._enum))

        self._layout.addWidget(self._widget)
        self.setLayout(self._layout)

    def objectName(self):
        return self._widget.objectName()

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
        elif isinstance(item, str):
            # print(item)
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


class AccountEntry(QComboBox):
    def __init__(self, name: str = None, parent=None, limit_size: int = None):
        super(AccountEntry, self).__init__(parent)
        self.parent = parent

        if limit_size is not None:
            self.setFixedWidth(limit_size)

        self.setObjectName(name)

        _accounts = [
            "Client Trad IRA",
            "Client Roth IRA",
            "Spouse Trad IRA",
            "Spouse Roth IRA",
            "Regular Taxable",
        ]

        self.addItems(_accounts)

    def enableSpouseAccount(self, enable: bool = True):
        _model = self.model()
        for _i in range(self.count()):
            if "Spouse" in self.itemText(_i):
                _item = _model.item(_i)
                if enable:
                    _item.setFlags(_item.flags() | Qt.ItemFlag.ItemIsEnabled)
                else:
                    _item.setFlags(_item.flags() & ~Qt.ItemFlag.ItemIsEnabled)

        if not enable and "Spouse" in self.currentText():
            self.setCurrentIndex(0)  # assuming client will always be first items.

    def isEmpty(self):
        """mostly for compatibility with other Entry objects.. Not really useful for ComboBox"""
        return self.count() > 0

    def set(self, text: str) -> None:
        self.setCurrentText(text)

    def get(self) -> str:
        return self.currentText()

    def clear(self):
        self.setCurrentIndex(0)


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

    def enableSpouse(self, enable: bool):
        # print("enableSpouse", enable)
        if not enable and "Spouse" == self._widget.currentText():
            self._widget.setCurrentText("Client")

        _model = self._widget.model()
        for _i in range(self._widget.count()):
            if "Spouse" in self._widget.itemText(_i):
                _item = _model.item(_i)
                if enable:
                    _item.setFlags(_item.flags() | Qt.ItemFlag.ItemIsEnabled)
                else:
                    _item.setFlags(_item.flags() & ~Qt.ItemFlag.ItemIsEnabled)


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
