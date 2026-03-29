from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout

from PyQt6.QtCore import Qt

from libs.gui.guihelpers.CustomTableWidgets import TransferSourceTableWidget
from libs.DataVariables import DataVariables, TransferRecord


class TransferInfoTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(TransferInfoTab, self).__init__(parent)

        self.BasicInfoTab = BasicInfoTab
        self.parent = parent

        _layout = QVBoxLayout()
        _layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.table = TransferSourceTableWidget(parent)
        self.table.addRow()

        _layout.addWidget(self.table)
        _layout.addStretch(3)
        self.setLayout(_layout)

    def validate_form(self) -> bool:
        return self.table.validate_form()

    def clear_form(self):
        self.table.clear()
        # self.table.setRowCount(0)
        # self.table.setHeader()

    def export_data(self, d: DataVariables):
        for (
            _descr,
            _src_acct,
            _tgt_acct,
            _amount,
            _cola,
            _person,
            _beginAge,
            _endAge,
        ) in self.table.getData():
            d.transfers.append(
                TransferRecord(
                    _descr,
                    _src_acct,
                    _tgt_acct,
                    _amount,
                    _cola,
                    _person,
                    _beginAge,
                    _endAge,
                )
            )

    def import_data(self, d: DataVariables):
        for _r in d.transfers:
            self.table.addRow(
                [
                    _r.descr,
                    _r.src_acct,
                    _r.tgt_acct,
                    _r.amount,
                    _r.COLA,
                    _r.person,
                    _r.beginAge,
                    _r.endAge,
                ]
            )
