import unittest
from datetime import date

from libs.EnumTypes import AccountOwnerType
from libs.Person import Person

# from libs.SocialSecurity import SocialSecurity
from libs.IncomeSources import SocialSecurity

# FRA means Full Retirement Age


class SocialSecurityFRA67Test(unittest.TestCase):
    """tests to verify that early/late SS payment calcs are correct"""

    def test_FRA_calcs(self):
        # anyone born after Jan 1st 1960 FRA is 67
        _p = Person(name="Jane", birthDate=date(1963, 1, 1))
        _ss = SocialSecurity(
            Name="Janes SS",
            FRAAmount=0,
            Person=_p,
            BirthDate=_p.birthDate,
            Owner=AccountOwnerType.Client,
        )
        self.assertEqual(_ss.calc_full_retirement_age(), 67)

        _p = Person(name="Jane60", birthDate=date(1960, 1, 1))
        _ss = SocialSecurity(
            Name="Janes SS",
            FRAAmount=0,
            Person=_p,
            BirthDate=_p.birthDate,
            Owner=AccountOwnerType.Client,
        )
        self.assertEqual(_ss.calc_full_retirement_age(), 67)

        # anyone born before Jan 1st 1960 FRA is 66
        _p = Person(name="Jane60", birthDate=date(1959, 12, 31))
        _ss = SocialSecurity(
            Name="Janes SS",
            FRAAmount=0,
            Person=_p,
            BirthDate=_p.birthDate,
            Owner=AccountOwnerType.Client,
        )
        self.assertEqual(_ss.calc_full_retirement_age(), 66)

    def test_benefits_by_age(self):
        _p = Person(name="Jane", birthDate=date(1963, 1, 1))

        for _age, _amount in (
            (55, 0),
            (60, 0),
            (62, 2100),
            (63, 2250),
            (64, 2400),
            (65, 2600),
            (66, 2800),
            (67, 3000),
            (68, 3240),
            (69, 3480),
            (70, 3720),
            (71, 3720),
        ):
            _ss = SocialSecurity(
                Name="Janes SS",
                FRAAmount=3000,
                Person=_p,
                BirthDate=_p.birthDate,
                Owner=AccountOwnerType.Client,
                BeginAge=_age,
            )

            self.assertEqual(_ss.calc_benefit_amount_by_age(_age), _amount)

        for _age, _amount in (
            (55, 0),
            (60, 0),
            (62, 1750),
            (63, 1875),
            (64, 2000),
            (65, 2167),
            (66, 2333),
            (67, 2500),
            (68, 2700),
            (69, 2900),
            (70, 3100),
            (71, 3100),
        ):
            _ss1 = SocialSecurity(
                "Janes SS",
                FRAAmount=2500,
                Person=_p,
                BirthDate=_p.birthDate,
                Owner=AccountOwnerType.Client,
                BeginAge=_age,
            )

            self.assertEqual(_ss1.calc_benefit_amount_by_age(_age), _amount)


if __name__ == "__main__":
    unittest.main()
