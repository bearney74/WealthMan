from PyQt6.QtWidgets import QWidget, QLabel, QFormLayout
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from gui.guihelpers.Entry import MoneyEntry


class AssetInfoTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(AssetInfoTab, self).__init__(parent)

        self.BasicInfoTab = BasicInfoTab

        _layout = QHBoxLayout()

        self._clientinfo = AssetInfoForm(parent, "Client")
        self._spouseinfo = AssetInfoForm(parent, "Spouse")
        self._spouseinfo.setEnabled(
            self.BasicInfoTab.client_is_married()
            #self.BasicInfoTab._clientinfo._status.currentText() == "Married"
        )

        _layout.addWidget(self._clientinfo)
        _layout.addWidget(self._spouseinfo)

        self.setLayout(_layout)

    def clear_form(self):
        self._clientinfo.clear_form()
        self._spouseinfo.clear_form()


class AssetInfoForm(QWidget):
    def __init__(self, parent, person_type):
        super(AssetInfoForm, self).__init__(parent)

        self._person_type = person_type
        # tk.Label(self, text="Client Information").grid(row=_row, column=0, columnspan=2, sticky='w')

        _vlayout = QVBoxLayout()
        _vlayout.addWidget(QLabel("<b>%s Asset Information</b>" % self._person_type))

        _layout = QFormLayout()
        self.IRA = MoneyEntry()
        _layout.addRow(QLabel("IRA:"), self.IRA)

        self.RothIRA = MoneyEntry()
        _layout.addRow(QLabel("Roth IRA:"), self.RothIRA)

        self.Regular = MoneyEntry()
        _layout.addRow(QLabel("Taxable (Regular):"), self.Regular)

        _vlayout.addLayout(_layout)
        _vlayout.addStretch()

        self.setLayout(_vlayout)
    
    def clear_form(self):
        self.IRA.setText("")
        self.RothIRA.setText("")
        self.Regular.setText("")
    
    def export_xml(self) -> str:
        _owner="0"
        if self._person == "Client":
            _owner="1"
        if self._person == "Spouse":
            _owner="2"
            
        _str="<Assets>\n"
        if self.IRA.text().strip() != "":
           _str+='<Account Name="IRA" Type="TaxDeferred" Balance="%s" ' % self.IRA.text().strip()
           _str+='    UnrealizedCapitalGains="" CapitalLossCarryOver="" Owner="%s">' % _owner 
           _str+='  <AllocationPeriods>'
           _str+='     <Allocation BeginDate="" EndDate="" PercentStocks="95" PercentBonds="5" PercentMoneyMarket="0" />' 
           _str+='  </AllocationPeriods>'
           _str+='</Account>\n'
      
        if self.RothIRA.text().strip() != "":
           _str+='<Account Name="Roth" Type="TaxFree" Balance="%s" ' % self.RothIRA.text().strip()
           _str+='    UnrealizedCapitalGains="" CapitalLossCarryOver="" Owner="%s">' % _owner 
           _str+='  <AllocationPeriods>'
           _str+='     <Allocation BeginDate="" EndDate="" PercentStocks="95" PercentBonds="5" PercentMoneyMarket="0" />'
           _str+='  </AllocationPeriods>'
           _str+='</Account>\n'
           
        if self.Regular.text().strip() != "":
           _str+='<Account Name="Regular" Type="Taxable" Balance="%s" ' % self.Regular.text().strip()
           _str+='    UnrealizedCapitalGains="" CapitalLossCarryOver="" Owner="%s">' % _owner 
           _str+='  <AllocationPeriods>'
           _str+='     <Allocation BeginDate="" EndDate="" PercentStocks="95" PercentBonds="5" PercentMoneyMarket="0" />'
           _str+='  </AllocationPeriods>'
           _str+='</Account>\n'
       
        _str+="</Assets>\n"
      
        return _str

    def import_data(self, IRA:int, RothIRA:int, Regular):
        if IRA is not None:
            self.IRA.setText(str(IRA))
        if RothIRA is not None:
            self.RothIRA.setText(str(RothIRA))
        if Regular is not None:
            self.Regular.setText(str(Regular))
        
    #def setEnable(self, value: bool):
    #    assert isinstance(value, bool)
    #    self.IRA.setReadOnly(value)
    #    self.RothIRA.setReadOnly(value)
    #    self.Regular.setReadOnly(value)
