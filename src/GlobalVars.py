from dataclasses import dataclass
from EnumTypes import AccountType, FederalTaxStatusType

@dataclass
class GlobalVars:
    InflationRate: float
    SocialSecurityCOLA: float
    AssetWithdrawOrderByType: list(AccountType)
    YearsToForecast: int
    FederalTaxStatus: FederalTaxStatusType