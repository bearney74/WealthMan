import xml.etree.ElementTree as ET
from PyQt6.QtWidgets import QMainWindow


class Import:
    def __init__(self, xml):
        self._parser = None
        _root = ET.fromstring(xml)
        if _root.tag != "WealthMan":
            print("This is an invalid WealthMan xml file")

        if _root.attrib["Version"] == "0.1":
            from .Import0x1 import Import0x1

            self._parser = Import0x1(xml)

    def get_data(self):
        if self._parser is None:
            print("Something went wrong...")
            return {}

        return self._parser.get_data()

    def get_gui_data(self, mainWindow: QMainWindow):
        isinstance(mainWindow, QMainWindow)
        self._parser.get_gui_data(mainWindow)


if __name__ == "__main__":
    _i = Import("../../../TestCases/JohnJaneDoe.xml")
    print(_i.get_data())
