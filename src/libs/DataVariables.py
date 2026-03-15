from dataclasses import dataclass, field
from marshmallow import Schema, fields, post_load
import datetime as dt

from .EnumTypes import (
    RelationStatusType,
    FederalTaxStatusType,
    WithdrawOrderType,
    PersonType,
)
from .Version import APP_VERSION, FILE_VERSION


@dataclass
class IncomeRecord:
    descr: str
    amount: int
    COLA: float | None
    owner: PersonType
    begin_age: int | None
    end_age: int | None


class IncomeRecordSchema(Schema):
    descr = fields.Str()
    amount = fields.Int()
    COLA = fields.Float(allow_none=True)
    owner = fields.Enum(PersonType)
    begin_age = fields.Int(allow_none=True)
    end_age = fields.Int(allow_none=True)

    @post_load
    def make_IncomeRecord(self, data, **kwargs):
        return IncomeRecord(**data)


@dataclass
class ExpenseRecord:
    descr: str
    amount: int
    COLA: float | None
    owner: PersonType
    begin_age: int | None
    end_age: int | None


class ExpenseRecordSchema(Schema):
    descr = fields.Str()
    amount = fields.Int()
    COLA = fields.Float(allow_none=True)
    owner = fields.Enum(PersonType)
    begin_age = fields.Int(allow_none=True)
    end_age = fields.Int(allow_none=True)

    @post_load
    def make_ExpenseRecord(self, data, **kwargs):
        return ExpenseRecord(**data)


@dataclass
class TransferRecord:
    descr: str

    src_acct: str
    tgt_acct: str

    amount: int
    COLA: float

    person: PersonType
    beginAge: int | None
    endAge: int | None


class TransferRecordSchema(Schema):
    descr = fields.Str()
    src_acct = fields.Str()
    tgt_acct = fields.Str()
    amount = fields.Int()
    COLA = fields.Float(allow_none=True)
    person = fields.Enum(PersonType)
    beginAge = fields.Int(allow_none=True)
    endAge = fields.Int(allow_none=True)

    @post_load
    def make_TransferRecord(self, data, **kwargs):
        return TransferRecord(**data)


@dataclass
class DataVariables:
    # BasicInfo
    clientName: str = None
    clientBirthDate: dt.date = None
    clientLifeSpanAge: int = None
    clientRetirementAge: int = None
    # fix me
    relationStatus: RelationStatusType = RelationStatusType.SINGLE

    __version__: str = FILE_VERSION
    _app_version: str = APP_VERSION
    _creation_date: dt.datetime = field(default_factory=dt.datetime.now)
    _modified_date: dt.datetime = field(default_factory=dt.datetime.now)

    spouseName: str = None
    spouseBirthDate: dt.date = None
    spouseLifeSpanAge: int = None
    spouseRetirementAge: int = None

    # Income Sources
    clientSSAmount: int = None
    clientSSBeginAge: int = None

    spouseSSAmount: int = None
    spouseSSBeginAge: int = None

    pension1Name: str = None
    pension1Amount: int = None
    pension1Cola: float = None
    pension1SurvivorBenefits: float = None
    pension1BeginAge: int = None
    pension1EndAge: int = None

    pension2Name: str = None
    pension2Amount: int = None
    pension2Cola: float = None
    pension2SurvivorBenefits: float = None
    pension2BeginAge: int = None
    pension2EndAge: int = None

    otherIncomes: list[IncomeRecord] = field(default_factory=list)

    # Expense Sources
    expenses: list[ExpenseRecord] = field(default_factory=list)

    # Transfers from one asset to another
    transfers: list[TransferRecord] = field(default_factory=list)

    # Assets
    clientIRABalance: int = None
    clientIRACola: float = None
    clientIRAContribution: int = None
    clientIRAContributionBeginAge: int = None
    clientIRAContributionEndAge: int = None

    clientRothBalance: int = None
    clientRothCola: float = None
    clientRothContribution: int = None
    clientRothContributionBeginAge: int = None
    clientRothContributionEndAge: int = None

    spouseIRABalance: int = None
    spouseIRACola: float = None
    spouseIRAContribution: int = None
    spouseIRAContributionBeginAge: int = None
    spouseIRAContributionEndAge: int = None

    spouseRothBalance: int = None
    spouseRothCola: float = None
    spouseRothContribution: int = None
    spouseRothContributionBeginAge: int = None
    spouseRothContributionEndAge: int = None

    regularBalance: int = None
    regularCola: float = None
    regularContribution: int = None
    regularContributionBeginAge: int = None
    regularContributionEndAge: int = None

    SurplusAccount: bool = True
    SurplusAccountInterestRate: float = None

    # Global Variables
    start_year: int = None  # should change name to startYear
    inflation: float = None
    ssCola: float = None
    # fix me.. use withdraw enum
    withdrawOrder: str = None
    forecastYears: int = None
    inTodaysDollars: bool = False
    federalFilingStatus: FederalTaxStatusType = FederalTaxStatusType.SINGLE
    federalFilingStatusOnceWidowed: FederalTaxStatusType = FederalTaxStatusType.SINGLE

    # Misc Variables
    # Monte Carlo
    numberOfRuns: int = None
    avgROR: float = None
    avgRORStdDev: float = None
    avgInflationRate: float = None
    avgInflationRateStdDev: float = None

    # historical analysis variables
    # fix me  (allow for multiple allocations based on periods of time???)
    # pctStocks
    # pctBonds


class DataVariablesSchema(Schema):
    __version__ = fields.Str(dump_default=FILE_VERSION)
    _app_version = fields.Str(dump_default=APP_VERSION)
    # _creation_date = field(default_factory=dt.datetime.now)
    # _modified_date = fields.DateTime(default_factory=dt.datetime.now)

    # BasicInfo
    clientName = fields.Str(allow_none=True)
    clientBirthDate = fields.Date(allow_none=True)
    clientLifeSpanAge = fields.Int(allow_none=True)
    clientRetirementAge = fields.Int(allow_none=True)
    # fix me
    relationStatus = fields.Enum(RelationStatusType)
    spouseName = fields.Str(allow_none=True)
    spouseBirthDate = fields.Date(allow_none=True)
    spouseLifeSpanAge = fields.Int(allow_none=True)
    spouseRetirementAge = fields.Int(allow_none=True)

    # Income Sources
    clientSSAmount = fields.Int(allow_none=True)
    clientSSBeginAge = fields.Int(allow_none=True)

    spouseSSAmount = fields.Int(allow_none=True)
    spouseSSBeginAge = fields.Int(allow_none=True)

    pension1Name = fields.Str(allow_none=True)
    pension1Amount = fields.Str(allow_none=True)
    pension1Cola = fields.Float(allow_none=True)
    pension1SurvivorBenefits = fields.Float(allow_none=True)
    pension1BeginAge = fields.Int(allow_none=True)
    pension1EndAge = fields.Int(allow_none=True)

    pension2Name = fields.Str(allow_none=True)
    pension2Amount = fields.Int(allow_none=True)
    pension2Cola = fields.Float(allow_none=True)
    pension2SurvivorBenefits = fields.Float(allow_none=True)
    pension2BeginAge = fields.Int(allow_none=True)
    pension2EndAge = fields.Int(allow_none=True)

    otherIncomes = fields.Nested(IncomeRecordSchema, many=True)

    # Expense Sources
    expenses = fields.Nested(ExpenseRecordSchema, many=True)  #: [ExpenseRecord] = []

    # Transfers from one asset to another
    transfers = fields.Nested(TransferRecordSchema, many=True)

    # Assets
    clientIRABalance = fields.Int(allow_none=True)
    clientIRACola = fields.Float(allow_none=True)
    clientIRAContribution = fields.Int(allow_none=True)
    clientIRAContributionBeginAge = fields.Int(allow_none=True)
    clientIRAContributionEndAge = fields.Int(allow_none=True)

    clientRothBalance = fields.Int(allow_none=True)
    clientRothCola = fields.Float(allow_none=True)
    clientRothContribution = fields.Int(allow_none=True)
    clientRothContributionBeginAge = fields.Int(allow_none=True)
    clientRothContributionEndAge = fields.Int(allow_none=True)

    spouseIRABalance = fields.Int(allow_none=True)
    spouseIRACola = fields.Float(allow_none=True)
    spouseIRAContribution = fields.Int(allow_none=True)
    spouseIRAContributionBeginAge = fields.Int(allow_none=True)
    spouseIRAContributionEndAge = fields.Int(allow_none=True)

    spouseRothBalance = fields.Int(allow_none=True)
    spouseRothCola = fields.Float(allow_none=True)
    spouseRothContribution = fields.Int(allow_none=True)
    spouseRothContributionBeginAge = fields.Int(allow_none=True)
    spouseRothContributionEndAge = fields.Int(allow_none=True)

    regularBalance = fields.Int(allow_none=True)
    regularCola = fields.Float(allow_none=True)
    regularContribution = fields.Int(allow_none=True)
    regularContributionBeginAge = fields.Int(allow_none=True)
    regularContributionEndAge = fields.Int(allow_none=True)

    SurplusAccount = fields.Bool(allow_none=True)
    SurplusAccountInterestRate = fields.Float(allow_none=True)

    # Global Variables
    start_year = fields.Int(allow_none=True)  # should change name to startYear
    inflation = fields.Float(allow_none=True)
    ssCola = fields.Float(allow_none=True)
    # fix me.. use withdraw enum
    withdrawOrder = fields.Enum(WithdrawOrderType)
    forecastYears = fields.Int(allow_none=True)
    inTodaysDollars = fields.Bool(allow_none=True)
    federalFilingStatus = fields.Enum(FederalTaxStatusType)
    federalFilingStatusOnceWidowed = fields.Enum(FederalTaxStatusType)

    # Misc Variables
    # Monte Carlo
    numberOfRuns = fields.Int(allow_none=True)
    avgROR = fields.Float(allow_none=True)
    avgRORStdDev = fields.Float(allow_none=True)
    avgInflationRate = fields.Float(allow_none=True)
    avgInflationRateStdDev = fields.Float(allow_none=True)

    @post_load
    def make_instance(self, data, **kwargs):
        return DataVariables(**data)
