from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtGui import QIntValidator

import sys
sys.path.append("guihelpers")
from Entry import AgeEntry


class AnalysisTab(QWidget):
  def __init__(self, parent=None):
      super(AnalysisTab, self).__init__(parent)
      
      self.tabs=QTabWidget()
      
      self.tabs.setTabPosition(QTabWidget.TabPosition.South)
      
      self.tabs.addTab(QWidget(), "Details")
      self.tabs.addTab(QWidget(), "Charts")
      
      layout=QVBoxLayout()
      layout.addWidget(self.tabs)
      
      self.setLayout(layout)
      
