from datetime import date, datetime


class Person:
    def __init__(
        self,
        name:str,
        birthDate:date,
        retirementAge:int=None,
        lifeSpanAge:int=None,
        relationship=None,
    ):
        assert isinstance(name, str)
        self.name = name

        assert isinstance(birthDate, date)
        self.birthDate = birthDate  # date of birth

        assert isinstance(retirementAge, int)
        self.retirementAge = retirementAge
        
        assert isinstance(lifeSpanAge, int)
        self.lifeSpanAge= lifeSpanAge  # date of death (Dec 31st of year)
        #todo..
        self.relationship = relationship

    #def set_BirthDate_by_age(self, age: int):
    #    assert isinstance(age, int)
    #    _now = datetime.now()
    #    self.BirthDate = date(
    #        _now.year - age, _now.month, _now.day
    #    )  # set to today - age

    def calc_date_by_age(self, age:int) -> date:
        return date(self.birthdate.year + age, self.birthdate.month, self.birthdate.day)
    
    def calc_age_by_date(self, dt: date) -> int:
        """returns the number of years between two dates"""
        assert isinstance(self.birthDate, date)
        return (
            dt.year
            - self.birthDate.year
            - ((dt.month, dt.day) < (self.birthDate.month, self.birthDate.day))
        )

    def calc_age_by_year(self, year: int) -> int:
        """returns the age of person on Dec 31st of year"""
        return self.calc_age_by_date(dt=date(year, 12, 31))
