from datetime import date

from .EnumTypes import RelationStatus, AccountOwnerType


class BaseRecord:
    def __init__(
        self,
        descr,
        amount,
        COLA,
        owner,
        begin_age,
        end_age,
        isSocialSecurity: bool = False,
    ):
        assert isinstance(descr, str)
        self._descr = descr
        assert isinstance(amount, int)
        self._amount = amount
        assert isinstance(COLA, float)
        self._COLA = COLA
        assert isinstance(owner, AccountOwnerType)
        self._owner = owner
        assert isinstance(begin_age, int) or begin_age is None
        self._begin_age = begin_age
        assert isinstance(end_age, int) or end_age is None
        self._end_age = end_age


class IncomeRecord(BaseRecord):
    def __init__(
        self,
        descr,
        amount,
        COLA,
        owner,
        begin_age,
        end_age,
        isSocialSecurity: bool = False,
    ):
        super(IncomeRecord, self).__init__(
            descr, amount, COLA, owner, begin_age, end_age
        )
        assert isinstance(isSocialSecurity, bool)
        self._isSocialSecurity = isSocialSecurity


class ExpenseRecord(BaseRecord):
    def __init__(self, descr, amount, COLA, owner, begin_age, end_age):
        super(ExpenseRecord, self).__init__(
            descr, amount, COLA, owner, begin_age, end_age
        )


class DataVariables:
    def __init__(self):
        self.__version__ = 0.1
        # BasicInfo

        self._clientName: str = ""
        self._clientBirthDate: date = None
        self._clientLifeSpanAge: int = None  # age
        self._clientRetirementAge: int = None
        self._relationStatus: RelationStatus = RelationStatus.Single

        self._spouseName: str = ""
        self._spouseBirthDate: date = None
        self._spouseLifeSpanAge: int = None
        self._spouseRetirementAge: int = None

        # Income Sources
        self._incomes: [IncomeRecord] = []

        # Expense Sources
        self._expenses: [ExpenseRecord] = []

        # Assets
        self._clientIRA: int = None
        self._clientRothIRA: int = None
        self._Regular: int = None

        self._spouseIRA: int = None
        self._spouseRothIRA: int = None
        # self._spouseRegular: int = None

        # Global Variables
        self._inflation: float = None
        self._withdrawOrder: str = None
        self._forecastYears: int = None
