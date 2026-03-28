from PyQt6.QtWidgets import QWidget
# from PyQt6 import QtCore

from libs.gui.guihelpers.Entry import Entry
from libs.gui.guihelpers.Popup import ShowPopup


class FormValidator(QWidget):
    def __init__(self, parent=None):
        super(FormValidator, self).__init__(parent)
        self.parent = parent

    def validateEntryWidget(self, variable: Entry) -> bool:
        assert isinstance(variable, Entry)  # or one of its descendants

        if variable.isRequired() and variable.isEmpty():
            ShowPopup(
                self,
                "Invalid Input",
                "Error: %s is a required variable" % variable.objectName(),
            )
            return False

        # since the variable contains data, see if any dependent EntryWidgets are empty, if so
        # produce a popup message stating that those Entry elements need data
        if not variable.isEmpty():
            _str = "Since %s contains data..\n" % variable.objectName()
            _flag = False
            for _dep in variable.get_dependencies():
                if _dep.text() == "":
                    _flag = True
                    _str += "  %s needs a value\n" % _dep.objectName()
            if _flag:
                ShowPopup(self, "Invalid Input", _str)
                return False

        # if we got here data looks okay.
        # ShowPopup(self, "Input verified", "Data looks okay")
        return True
