from dataclass import dataclass
from datetime import date

@dataclass
class IncomeSource:
    name:str
    amount:int
    begin_date: date
    end_date: date