from datetime import date

from Person import Person

# for now just assume the usual (most common case)
ULT={             72:27.4, 73:26.5, 74:25.5, 75:24.6, 76:23.7, 77:22.9, 78:22.0, 79:21.1,
80:20.2, 81:19.4, 82:18.5, 83:17.7, 84:16.8, 85:16.0, 86:15.2, 87:14.4, 88:13.7, 89:12.9,
90:12.2, 91:11.5, 92:10.8, 93:10.1,  94:9.5,  95:8.9,  96:8.4,  97:7.8,  98:7.3,  99:6.8,
100:6.4, 101:6.0, 102:5.6, 103:5.2, 104:4.9, 105:4.6, 106:4.3, 107:4.1, 108:3.9, 109:3.7,
110:3.5, 111:3.4, 112:3.3, 113:3.1, 114:3.0, 115:2.9, 116:2.8, 117:2.7, 118:2.5, 119:2.3,
120:2.0
}

# should this be moved to DateHelper class?
def calc_age(date1:date, date2:date) -> int:
    _diff=date1 - date2
    return int(abs((_diff.days + _diff.seconds/86400)/365.2425))


class RMD:
  def __init__(self, person1:Person, person2:Person):
      self.Person1=person1
      self.Person2=person2

      self._calc_init()

  def _calc_init(self):
      """ used to see which lookup table to use... """
      if self.Person2 is None:
         self._table=ULT
      else:  #need to check for age difference  (< 10 or > 10)?
         if calc_age(self.Person1.BirthDate, self.Person2.BirthDate) <= 10:
            self._table=ULT
         else:
            #TODO
            assert False, "RMD for spouses 10 years younger not implemented yet"

  def death_event(self, person):
      if person == self.Person1 and self.Person2 is not None:
         self.Person1=self.Person2
         self.Person2=None

      if person == self.Person2:
         self.Person2=None

      #TODO:do we need to start using another lookup table?
      #self._calc_init()

  def calc(self, currdate:date) -> float:
      _age=calc_age(self.Person1.BirthDate, currdate)
      if _age < 72:
         return 0.0
      if _age > 120:
         return 100.0/self._table[120]

      return 100.0/self._table[_age]
