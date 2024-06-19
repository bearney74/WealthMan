from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt6.QtWidgets import QVBoxLayout, QGridLayout

from PyQt6.QtCore import Qt

# import sys
# sys.path.append("guihelpers")
from gui.guihelpers.Entry import MoneyEntry, PercentEntry, AgeEntry


class IncomeSourceTab(QWidget):
    def __init__(self, parent):
        super(IncomeSourceTab, self).__init__(parent)

        self.parent = parent
        self._descrs = []
        self._amounts = []
        self._percents = []
        self._begin_ages = []
        self._end_ages = []

        _layout = QVBoxLayout()
        _layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._add_income_button = QPushButton("Add Income", self)
        self._add_income_button.setFixedSize(120, 60)
        self._add_income_button.clicked.connect(self.add_row)
        _layout.addWidget(self._add_income_button)

        # Table will fit the screen horizontally

        self.gridLayout = QGridLayout()
        _layout.addLayout(self.gridLayout)
        self.setLayout(_layout)

    def add_row(self):
        if self._descrs == []:
            self.gridLayout.addWidget(QLabel("Description"), 0, 0)
            self.gridLayout.addWidget(QLabel("Annual Amount"), 0, 1)
            _temp = QLabel("Annual\nPercent\nIncrease", wordWrap=True)
            # _temp.setWordWrap(True)
            self.gridLayout.addWidget(_temp, 0, 2)
            self.gridLayout.addWidget(QLabel("Begin Age"), 0, 3)
            self.gridLayout.addWidget(QLabel("End Age"), 0, 4)

        _descr = QLineEdit()
        _descr.setMaximumWidth(300)
        self._descrs.append(_descr)
        self.gridLayout.addWidget(_descr, len(self._descrs), 0)

        _amount = MoneyEntry(self.parent)
        self._amounts.append(_amount)
        self.gridLayout.addWidget(_amount, len(self._amounts), 1)

        _percent = PercentEntry(self.parent)
        self._percents.append(_percent)
        self.gridLayout.addWidget(_percent, len(self._percents), 2)

        _begin_age = AgeEntry(self.parent)
        self._begin_ages.append(_begin_age)
        self.gridLayout.addWidget(_begin_age, len(self._begin_ages), 3)

        _end_age = AgeEntry(self.parent)
        self._end_ages.append(_end_age)
        self.gridLayout.addWidget(_end_age, len(self._end_ages), 4)
