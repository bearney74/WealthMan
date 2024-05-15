import xml.etree.ElementTree as ET


class Import:
  def __init__(self, filename):
      self._parser=None
      _xml=ET.parse(filename)
      _root=_xml.getroot()
      if _root.tag != "WealthMan":
          print("This is an invalid WealthMan xml file")
      
      #print(_root.attrib["Version"])
      
      if _root.attrib["Version"] == "0.1":
          import Import0x1
          self._parser=Import0x1.Import0x1(filename)
      #print(_root.findall('WealthMan'))
      
  def get_data(self):
      if self._parser is None:
          print("Something went wrong...")
          return {}
        
      return self._parser.get_data()
    
if __name__ == '__main__':
    _i=Import("../../../TestCases/JohnJaneDoe.xml")
    print(_i.get_data())
    