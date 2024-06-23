from datetime import date, datetime


class Person:
    def __init__(
        self,
        Name,
        BirthDate,
        RetirementDate=None,
        LifeExpectancy=None,
        Relationship=None,
    ):
        self.Name = Name

        assert isinstance(BirthDate, date)
        self.BirthDate = BirthDate  # date of birth

        self.RetirementDate = RetirementDate
        self.LifeExpectancy = LifeExpectancy  # date of death (Dec 31st of year)
        self.Relationship = Relationship

    def set_BirthDate_by_age(self, age: int):
        assert isinstance(age, int)
        _now = datetime.now()
        self.BirthDate = date(
            _now.year - age, _now.month, _now.day
        )  # set to today - age

    def set_LifeExpectancy_by_age(self, age: int):  # DOD = Date of Death
        assert isinstance(age, int)
        assert isinstance(self.BirthDate, date)
        if age is not None:
            self.LifeExpectancy = date(
                self.BirthDate.year + age, 12, 31
            )  # set to Dec 31st of year
        else:
            self.LifeExpectancy = None

    def set_Retirement_by_age(self, age: int):
        assert isinstance(age, int)
        assert isinstance(self.BirthDate, date)
        if age is not None:
            self.RetirementDate = date(
                self.BirthDate.year + age, 12, 31
            )  # set to Dec 31st of year
        else:
            self.Retirementdate = None

    def calc_age_by_date(self, dt: date) -> int:
        """returns the number of years between two dates"""
        assert isinstance(self.BirthDate, date)
        return (
            dt.year
            - self.BirthDate.year
            - ((dt.month, dt.day) < (self.BirthDate.month, self.BirthDate.day))
        )

    def calc_age_by_year(self, year: int) -> int:
        """returns the age of person on Dec 31st of year"""
        return self.calc_age_by_date(dt=date(year, 12, 31))
