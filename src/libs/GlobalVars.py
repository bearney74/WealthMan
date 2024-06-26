from .EnumTypes import AccountType, FederalTaxStatusType


class GlobalVars:
    def __init__(
        self,
        InflationRate: float,
        SocialSecurityCOLA: float,
        AssetWithdrawOrderByType: list(AccountType),
        YearsToForecast: int,
        FederalTaxStatus: FederalTaxStatusType,
    ):
        self.InflationRate = InflationRate
        self.SocialSecurityCOLA = SocialSecurityCOLA
        self.AssetWithdrawOrderByType = AssetWithdrawOrderByType
        self.YearsToForecast = YearsToForecast
        self.FederalTaxStatus = FederalTaxStatus  # does this need to be here??
