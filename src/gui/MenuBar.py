from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QFileDialog

import os
import pickle
import sys

sys.path.append("..")

from libs.DataVariables import DataVariables

import logging

logger = logging.getLogger(__name__)


class MenuBar:
    def __init__(self, parent):
        self.parent = parent
        self._filename = None

        self.menuBar = self.parent.menuBar()
        filemenu = self.menuBar.addMenu("&File")
        filemenu.addAction(self.file_new_action())
        filemenu.addAction(self.file_open_action())
        filemenu.addAction(self.file_save_action())
        filemenu.addAction(self.file_save_as_action())
        filemenu.addAction(self.file_exit_action())

        help_menu = self.menuBar.addMenu("&Help")
        help_menu.addAction(self.toggle_logs_action())
        help_menu.addAction(self.help_about_action())

    def get_menubar(self):
        return self.menuBar

    def file_new_action(self):
        _action = QAction("&New", self.parent)
        _action.setStatusTip("Create a new file")
        _action.triggered.connect(lambda x: self.file_new())
        return _action

    def file_open_action(self):
        _action = QAction("&Open", self.parent)
        _action.setStatusTip("Open a file")
        _action.triggered.connect(lambda x: self.file_open())
        return _action

    def file_save_action(self):
        _action = QAction("&Save", self.parent)
        _action.setStatusTip("Save a file")
        _action.triggered.connect(lambda x: self.file_save())
        return _action

    def file_save_as_action(self):
        _action = QAction("Save as...", self.parent)
        _action.setStatusTip("Save as...")
        _action.triggered.connect(lambda x: self.file_save_as())
        return _action

    def file_exit_action(self):
        _action = QAction("Exit", self.parent)
        _action.setStatusTip("Exit WealthMan")
        _action.triggered.connect(lambda x: self.file_exit())
        return _action

    def file_open(self):
        logger.debug("open file")
        _fname, _type = QFileDialog.getOpenFileName(
            self.parent,
            "Open File",
            "",
            "WealthMan Data Files (*.wmd)",
        )
        logger.info("filename:%s" % _fname)
        if _fname == "":
            return

        with open(_fname, "rb") as _fp:
            dv = pickle.load(_fp)

        logger.info("__version__ = '%s'" % dv.__version__)
        self.parent.InputsTab.clear_forms()
        self.parent.InputsTab.BasicInfoTab.import_data(dv)
        self.parent.InputsTab.IncomeInfoTab.import_data(dv)
        self.parent.InputsTab.ExpenseInfoTab.import_data(dv)
        self.parent.InputsTab.AssetInfoTab.import_data(dv)
        self.parent.InputsTab.GlobalVariablesTab.import_data(dv)

        self.parent.setWindowTitle(
            "%s :%s" % (self.parent.title, os.path.basename(_fname))
        )
        # _import.get_gui_data(self.parent)
        self._filename = _fname

    def file_new(self):
        logger.debug("new file")
        self._filename = None
        self.parent.InputsTab.clear_forms()

    def file_save_as(self):
        self._filename = None
        self.file_save()

    def file_save(self):
        """this will retrieve the xml from the widgets and will save in an xml file somewhere"""

        logger.debug("save file '%s'" % self._filename)
        if self._filename is None:
            self._filename, _x = QFileDialog.getSaveFileName(self.parent, "Save File")
            logger.debug("using '%s' as filename.." % self._filename)

        if self._filename == "":
            return

        # for every tab in the inputs, we need to retrieve the fields and put in DataVariables (dv).
        dv = DataVariables()

        self.parent.InputsTab.BasicInfoTab.export_data(dv)
        self.parent.InputsTab.IncomeInfoTab.export_data(dv)
        self.parent.InputsTab.ExpenseInfoTab.export_data(dv)
        self.parent.InputsTab.AssetInfoTab.export_data(dv)
        self.parent.InputsTab.GlobalVariablesTab.export_data(dv)

        with open(self._filename, "wb") as _fp:
            pickle.dump(dv, _fp)

    def file_exit(self):
        logger.debug("file exit")
        self.parent.close()

    def help_about_action(self):
        _action = QAction("About", self.parent)
        _action.setStatusTip("About WealthMan")
        _action.triggered.connect(lambda x: self.help_about())

        return _action

    def help_about(self):
        """brings up a dialog window displaying information about this app"""
        d = QDialog()
        d.setWindowTitle("About WealthMan")
        _info = QLabel(
            "WealthMan is an open source financial planning tool that one day hopes to rival standard tools used by Certified Financial Planners (CFP) in the Financial planning field."
        )
        _info.setWordWrap(True)

        _layout = QVBoxLayout()
        _layout.addWidget(_info)

        _buttonbox = QDialogButtonBox(d)
        _buttonbox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        _buttonbox.accepted.connect(d.close)
        _layout.addWidget(_buttonbox)

        d.setLayout(_layout)
        d.setModal(True)
        d.exec()

    def toggle_logs_action(self):
        _action = QAction("Enable/Disable Logs", self.parent)
        _action.setStatusTip("Enable/Disable Logs")
        _action.triggered.connect(lambda x: self.toggle_logs())

        return _action

    def toggle_logs(self):
        self.parent.toggleLogTab()
