import unittest
from datetime import date

import sys
sys.path.append("../src")

from libs.Person import Person
from libs.SocialSecurity import SocialSecurity

#FRA means Full Retirement Age

class SocialSecurityFRA67Test(unittest.TestCase):
  """ tests to verify that early/late SS payment calcs are correct """

  def test_FRA_calcs(self):
      #anyone born after Jan 1st 1960 FRA is 67
      _p=Person(Name="Jane", BirthDate=date(1963, 1, 1))
      _ss=SocialSecurity(FRAAmount=0, person=_p)
      self.assertEqual(_ss.calc_full_retirement_age(), 67)

      _p=Person(Name="Jane60", BirthDate=date(1960, 1, 1))
      _ss=SocialSecurity(FRAAmount=0, person=_p)
      self.assertEqual(_ss.calc_full_retirement_age(), 67)


      #anyone born before Jan 1st 1960 FRA is 66
      _p=Person(Name="Jane60", BirthDate=date(1959, 12, 31))
      _ss=SocialSecurity(FRAAmount=0, person=_p)
      self.assertEqual(_ss.calc_full_retirement_age(), 66)


  def test_benefits_by_age(self):
      _p=Person(Name="Jane", BirthDate=date(1963, 1, 1))
      _ss=SocialSecurity(FRAAmount=3000, person=_p)
      
      for _age, _amount in ((55, 0), (60, 0), (62, 2100), (63, 2250), (64, 2400), (65, 2600),
                            (66, 2800), (67, 3000), (68, 3240), (69, 3480), (70, 3720), (71, 3720)):
          self.assertEqual(_ss.calc_benefit_amount_by_age(_age), _amount)
      
      _ss1=SocialSecurity(FRAAmount=2500, person=_p)
      
      for _age, _amount in ((55, 0), (60, 0), (62, 1750), (63, 1875), (64, 2000), (65, 2167),
                            (66, 2333), (67, 2500), (68, 2700), (69, 2900), (70, 3100), (71, 3100)):
          self.assertEqual(_ss1.calc_benefit_amount_by_age(_age), _amount)


if __name__ == '__main__':
    unittest.main()