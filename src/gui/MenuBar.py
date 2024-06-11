from PyQt6.QtGui import QAction, QIcon

class MenuBar:
  def __init__(self, parent):

      self.parent=parent
      self.menuBar=self.parent.menuBar()
      filemenu=self.menuBar.addMenu("&File")
      filemenu.addAction(self.file_open_action())
      
  def get_menubar(self):
      return self.menuBar
         
  def file_open_action(self):
      _action=QAction(QIcon(""), "&Open", self.parent)
      _action.setStatusTip("Open a file")
      _action.triggered.connect(self.openfile)
      
      return _action
         
  def openfile(self):
      pass
                  
  def file_new(self):
      pass

  def help_about(self):
      """brings up a dialog window displaying information about this app"""
      pass