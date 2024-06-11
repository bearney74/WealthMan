from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox

class MenuBar:
  def __init__(self, parent):

      self.parent=parent
      self.menuBar=self.parent.menuBar()
      filemenu=self.menuBar.addMenu("&File")
      filemenu.addAction(self.file_open_action())
      filemenu.addAction(self.file_save_action())
      filemenu.addAction(self.file_exit_action())

      help_menu=self.menuBar.addMenu("&Help")
      help_menu.addAction(self.help_about_action())
      
  def get_menubar(self):
      return self.menuBar
         
  def file_open_action(self):
      _action=QAction("&Open", self.parent)
      _action.setStatusTip("Open a file")
      _action.triggered.connect(self.file_open)
      return _action
         
  def file_save_action(self):
      _action=QAction("&Save", self.parent)
      _action.setStatusTip("Save a file")
      _action.triggered.connect(lambda: self.file_save())
      return _action
    
  def file_exit_action(self):
      _action=QAction("Exit", self.parent)
      _action.setStatusTip("Exit WealthMan")
      _action.triggered.connect(lambda: self.file_exit())
      return _action
    
  def file_open(self):
      print("open file")
                  
  def file_new(self):
      pass
    
  def file_save(self):
      """ this will retrieve the xml from the widgets and will save in an xml file somewhere"""
      
      #for every tab in the inputs, we need to retrieve the xml and save them.
      print(self.parent.Inputs.GlobalVars_tab.export_xml())
      
  def file_exit(self):
      self.parent.close()
      
  def help_about_action(self):
      _action=QAction("About", self.parent)
      _action.setStatusTip("About WealthMan")
      _action.triggered.connect(lambda: self.help_about())

      return _action

  def help_about(self):
      """brings up a dialog window displaying information about this app"""
      d=QDialog()
      d.setWindowTitle("About WealthMan")
      _info=QLabel("WealthMan is an open source financial planning tool that one day hopes to rival standard tools used by Certified Financial Planners (CFP), and other individuals in the Financial field.")
      _info.setWordWrap(True)
      
      _layout=QVBoxLayout()
      _layout.addWidget(_info)
     # b1=QDialogButtonBox(QDialogButtonBox.Ok)
      #b1.move(50,50)
      _buttonbox=QDialogButtonBox(d)
      _buttonbox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
      _buttonbox.accepted.connect(lambda: d.close())
      _layout.addWidget(_buttonbox)
      d.setLayout(_layout)
      d.setModal(True)
      #d.setWindowModality(Qt.ApplicationModal)
      d.exec()
      