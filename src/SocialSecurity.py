
@dataclass
class SocialSecurity:
    COLA: float = 2.0
    
    FRA: int = None
    benefit_amount: int
    benefit_reduction: float = None
    start_date: date
    end_date: date = None
    
  def calc_full_retirement_age(self, person:Person):
      if person.DOB > date(1940, 1, 1):
         return 67
      return 66
    
  def calc_end_date(self, person:Person):
      end_date = person.DOD