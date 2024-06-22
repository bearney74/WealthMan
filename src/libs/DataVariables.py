from datetime import date

from .EnumTypes import RelationStatus


class IncomeRecord:
    def __init__(self, descr, amount, COLA, owner, begin_age, end_age):
        self._descr = descr
        self._amount = amount
        self._COLA = COLA
        self._owner = owner
        self._begin_age = begin_age
        self._end_age = end_age


class ExpenseRecord:
    def __init__(self, descr, amount, COLA, owner, begin_age, end_age):
        self._descr = descr
        self._amount = amount
        self._COLA = COLA
        self._owner = owner
        self._begin_age = begin_age
        self._end_age = end_age


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
