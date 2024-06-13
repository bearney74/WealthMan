from .EnumTypes import AccountType, FederalTaxStatusType

from gui.GlobalVariables import GlobalVariablesTab

class GlobalVars:
  def __init__(self, InflationRate: float, SocialSecurityCOLA:float,
               AssetWithdrawOrderByType: list(AccountType),
               YearsToForecast: int, FederalTaxStatus: FederalTaxStatusType):
      self.InflationRate = InflationRate
      self.SocialSecurityCOLA=SocialSecurityCOLA
      self.AssetWithdrawOrderByType=AssetWithdrawOrderByType
      self.YearsToForecast=YearsToForecast
      self.FederalTaxStatus=FederalTaxStatus  #does this need to be here??
    
  def gui_import_data(self, gvt:GlobalVariablesTab):
      assert isinstance(gvt, GlobalVariablesTab)
      gvt.import_data(str(self.InflationRate), str(self.SocialSecurityCOLA),
                      str(self.AssetWithdrawOrderByType),
                      str(self.YearsToForecast))