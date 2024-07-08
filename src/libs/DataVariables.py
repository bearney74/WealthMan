from datetime import date

from .EnumTypes import RelationStatus, AccountOwnerType, FederalTaxStatusType
from .Version import APP_VERSION


class BaseRecord:
    def __init__(
        self,
        descr,
        amount,
        COLA,
        owner,
        begin_age,
        end_age,
        survivor_percent: float = None,
    ):
        assert isinstance(descr, str)
        self.descr = descr
        assert isinstance(amount, int)
        self.amount = amount
        assert isinstance(COLA, float)
        self.COLA = COLA
        assert isinstance(owner, AccountOwnerType)
        self.owner = owner
        assert isinstance(begin_age, int) or begin_age is None
        self.begin_age = begin_age
        assert isinstance(end_age, int) or end_age is None
        self.end_age = end_age

        assert isinstance(survivor_percent, float) or survivor_percent is None
        self.survivor_percent = survivor_percent


class IncomeRecord(BaseRecord):
    def __init__(
        self,
        descr,
        amount,
        COLA,
        owner,
        begin_age,
        end_age,
        survivor_benefit: float = None,
    ):
        super(IncomeRecord, self).__init__(
            descr, amount, COLA, owner, begin_age, end_age, survivor_benefit
        )
        # assert isinstance(isSocialSecurity, bool)
        # self._isSocialSecurity = isSocialSecurity


class ExpenseRecord(BaseRecord):
    def __init__(self, descr, amount, COLA, owner, begin_age, end_age):
        super(ExpenseRecord, self).__init__(
            descr, amount, COLA, owner, begin_age, end_age
        )


class DataVariables:
    def __init__(self):
        self.__version__ = APP_VERSION
        # BasicInfo

        self.clientName: str = ""
        self.clientBirthDate: date = None
        self.clientLifeSpanAge: int = None  # age
        self.clientRetirementAge: int = None
        self.relationStatus: RelationStatus = RelationStatus.Single

        self.spouseName: str = ""
        self.spouseBirthDate: date = None
        self.spouseLifeSpanAge: int = None
        self.spouseRetirementAge: int = None

        # Income Sources
        self.clientSSAmount: int = None
        self.clientSSCola: float = None
        self.clientSSBeginAge: int = None

        self.spouseSSAmount: int = None
        self.spouseSSCola: float = None
        self.spouseSSBeginAge: int = None

        self.pension1Name: str = None
        self.pension1Amount: int = None
        self.pension1Cola: float = None
        self.pension1SurvivorBenefits: float = None
        self.pension1BeginAge: int = None
        self.pension1EndAge: int = None

        self.pension2Name: str = None
        self.pension2Amount: int = None
        self.pension2Cola: float = None
        self.pension2SurvivorBenefits: float = None
        self.pension2BeginAge: int = None
        self.pension2EndAge: int = None

        self.otherIncomes: [IncomeRecord] = []

        # Expense Sources
        self.expenses: [ExpenseRecord] = []

        # Assets
        self.clientIRABalance: int = None
        self.clientIRACola: float = None
        self.clientIRAContribution: int = None
        self.clientIRAContributionBeginAge: int = None
        self.clientIRAContributionEndAge: int = None

        self.clientRothIRABalance: int = None
        self.clientRothIRACola: float = None
        self.clientRothContribution: int = None
        self.clientRothContributionBeginAge: int = None
        self.clientRothContributionEndAge: int = None

        self.spouseIRABalance: int = None
        self.spouseIRACola: float = None
        self.spouseIRAContribution: int = None
        self.spouseIRAContributionBeginAge: int = None
        self.spouseIRAContributionEndAge: int = None

        self.spouseRothIRABalance: int = None
        self.spouseRothIRACola: float = None
        self.spouseRothContribution: int = None
        self.spouseRothContributionBeginAge: int = None
        self.spouseRothContributionEndAge: int = None

        self.regularBalance: int = None
        self.regularCola: float = None
        self.regularContribution: int = None
        self.regularContributionBeginAge: int = None
        self.regularContributionEndAge: int = None

        # Global Variables
        self.inflation: float = None
        self.withdrawOrder: str = None
        self.forecastYears: int = None
        self.inTodaysDollars: bool = False
        self.federalFilingStatus: FederalTaxStatusType = None
        self.federalFilingStatusOnceWidowed: FederalTaxStatusType = None
