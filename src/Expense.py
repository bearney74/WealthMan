from dataclasses import dataclass

@dataclass

class Expense:
   Name: str
   Amount: int
   AmountPeriod:str
   COLA: float = 0.0