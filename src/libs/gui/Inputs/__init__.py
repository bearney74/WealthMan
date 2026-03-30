from PyQt6.QtWidgets import (
    QTabWidget,
    QToolBar,
    QMainWindow,
    # QComboBox,
    QStyle,
    QProgressDialog,
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QThreadPool, Qt

from libs.DataVariables import DataVariables
from libs.Projections import Projections
from libs.TableData import TableData

from .BasicInfo import BasicInfoTab
from .GlobalVariables import GlobalVariablesTab
from .IncomeInfo import IncomeInfoTab
from .AssetInfo import AssetInfoTab
from .ExpenseInfo import ExpenseInfoTab
from .TransferInfo import TransferInfoTab
from .MiscInfo import MiscInfoTab


class InputsTab(QMainWindow):
    def __init__(self, parent=None):
        super(InputsTab, self).__init__(parent)

        self.parent = parent
        _toolbar = QToolBar("Inputs Toolbar")
        _toolbar.addAction(self.clear_forms_action())
        _toolbar.addAction(self.file_open_action())
        _toolbar.addAction(self.file_save_action())
        _toolbar.addAction(self.calculate_projection_action())
        self.addToolBar(_toolbar)

        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.onTabChange)
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)

        self.BasicInfoTab = BasicInfoTab(self)
        self.IncomeInfoTab = IncomeInfoTab(self, self.BasicInfoTab)
        self.AssetInfoTab = AssetInfoTab(self, self.BasicInfoTab)
        self.ExpenseInfoTab = ExpenseInfoTab(self, self.BasicInfoTab)
        self.TransferInfoTab = TransferInfoTab(self, self.BasicInfoTab)
        self.GlobalVariablesTab = GlobalVariablesTab(self)
        self.MiscInfoTab = MiscInfoTab(self)

        self.tabs.addTab(self.BasicInfoTab, "Basic Info")
        self.tabs.addTab(self.IncomeInfoTab, "Income")
        self.tabs.addTab(self.ExpenseInfoTab, "Expenses")
        self.tabs.addTab(self.AssetInfoTab, "Assets")
        self.tabs.addTab(self.TransferInfoTab, "Transfers")
        self.tabs.addTab(self.GlobalVariablesTab, "Global Variables")
        self.tabs.addTab(self.MiscInfoTab, "Misc")

        self.setCentralWidget(self.tabs)

        self.threadpool = QThreadPool()

    def onTabChange(self, i):
        _is_married = self.BasicInfoTab.client_is_married()

        match self.tabs.tabText(i):
            case "Assets":
                self.AssetInfoTab._spouseinfo.setEnabled(_is_married)
            case "Income":
                self.IncomeInfoTab.spouseSS.setEnabled(_is_married)
                self.IncomeInfoTab.pension1.Owner.enableSpouse(_is_married)
                self.IncomeInfoTab.pension2.Owner.enableSpouse(_is_married)

                self.IncomeInfoTab.table.enableSpouse(_is_married)
            case "Expenses":
                self.ExpenseInfoTab.table.enableSpouse(_is_married)
            case "Transfers":
                self.TransferInfoTab.table.enableSpouse(_is_married)
                pass
            case "Global Variables":
                self.GlobalVariablesTab._FilingStatusOnceWidowed.setEnabled(_is_married)
        # self._previous_tab_name = _tabName

    def clear_forms_action(self):
        _action = QAction("Clear forms", self)
        _pixmapi = QStyle.StandardPixmap.SP_DialogResetButton
        _action.setIcon(self.style().standardIcon(_pixmapi))
        _action.setStatusTip("Clear Forms")
        _action.triggered.connect(lambda x: self.clear_forms())
        return _action

    def file_open_action(self):
        _action = QAction("Open", self)
        _pixmapi = QStyle.StandardPixmap.SP_FileDialogStart
        _action.setIcon(self.style().standardIcon(_pixmapi))
        _action.setStatusTip("open")
        _action.triggered.connect(lambda x: self.file_open())
        return _action

    def file_save_action(self):
        _action = QAction("Save", self)
        _pixmapi = QStyle.StandardPixmap.SP_DialogSaveButton
        _action.setIcon(self.style().standardIcon(_pixmapi))
        _action.setStatusTip("Save")
        _action.triggered.connect(lambda x: self.file_save())
        return _action

    def calculate_projection_action(self):
        _action = QAction("Analysis", self)
        _pixmapi = QStyle.StandardPixmap.SP_FileDialogContentsView
        _action.setIcon(self.style().standardIcon(_pixmapi))
        _action.setStatusTip("Perform Data Analysis")
        _action.setToolTip("Perform Data Analysis")
        _action.triggered.connect(lambda x: self.create_analysis())
        return _action

    def clear_forms(self):
        self.BasicInfoTab.clear_form()
        self.AssetInfoTab.clear_form()
        self.IncomeInfoTab.clear_form()
        self.ExpenseInfoTab.clear_form()
        self.TransferInfoTab.clear_form()
        self.GlobalVariablesTab.clear_form()
        self.MiscInfoTab.clear_form()

    def validate_input_forms(self):
        if not self.BasicInfoTab.validate_form():
            # create a popup stating there is a problem with the input data on the BasicInfoTab...
            # print("create popup for Basic Info Tab")
            # ShowPopup(self, "Invalid Input", "Please enter missing information on the basic info tab")
            self.tabs.setCurrentWidget(self.BasicInfoTab)
            return False

        if not self.IncomeInfoTab.validate_form():
            # create popup error message
            # maybe auto select (display) IncomeInfoTab
            # ShowPopup(self, "Invalid Input", "Please enter missing information on the income info tab")
            self.tabs.setCurrentWidget(self.IncomeInfoTab)
            return False

        if not self.ExpenseInfoTab.validate_form():
            self.tabs.setCurrentWidget(self.ExpenseInfoTab)
            return False

        if not self.AssetInfoTab.validate_form():
            self.tabs.setCurrentWidget(self.AssetInfoTab)
            return False

        if not self.TransferInfoTab.validate_form():
            self.tabs.setCurrentWidget(self.TransferInfoTab)
            return False

        if not self.GlobalVariablesTab.validate_form():
            # print("create popup for Global Variables Tab")
            self.tabs.setCurrentWidget(self.GlobalVariablesTab)
            return False

        if not self.MiscInfoTab.validate_form():
            # print("create popup for Global Variables Tab")
            self.tabs.setCurrentWidget(self.MiscInfoTab)
            return False

        # all forms appear to have reasonable values..
        return True

    def create_analysis(self):
        if not self.validate_input_forms():
            return

        # if we got here the forms appear to be validated correctly..

        dv = DataVariables()

        self.BasicInfoTab.export_data(dv)
        self.IncomeInfoTab.export_data(dv)
        self.ExpenseInfoTab.export_data(dv)
        self.AssetInfoTab.export_data(dv)
        self.TransferInfoTab.export_data(dv)
        self.GlobalVariablesTab.export_data(dv)
        self.MiscInfoTab.export_data(dv)
        self.parent.AnalysisTab.MonteCarloTab.dataVariables = dv
        self.parent.AnalysisTab.HistoricalAnalysisTab.dataVariables = dv

        self.parent.statusbar.showMessage("Calculating projections")
        self.progressDialog = QProgressDialog("Projection in progress...", None, 0, 100)
        self.progressDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progressDialog.setMinimumDuration(0)
        self.progressDialog.setValue(0)
        self.progressDialog.setAutoClose(False)
        self.project = Projections(dv)
        self.project.signals.result.connect(self.populate_analysis_tab)
        self.threadpool.start(self.project)
        self.progressDialog.setValue(25)

        self.parent.AnalysisTab.HistoricalAnalysisTab.projections = self.project

    def populate_analysis_tab(self, data):
        self.progressDialog.setValue(50)
        self.parent.AnalysisTab.projectionData = data
        # self.parent.AnalysisTab.MonteCarloTab.projectionData= data
        self.parent.AnalysisTab.tableData = TableData(
            data,
            InTodaysDollars=self.project.InTodaysDollars,
            UseSurplusAccount=self.project.UseSurplusAccount,
        )

        self.progressDialog.setValue(75)
        self.parent.showAnalysisTab(True)
        self.progressDialog.hide()

    def file_open(self):
        self.parent.menubar.file_open()

    def file_save(self):
        self.parent.menubar.file_save()
