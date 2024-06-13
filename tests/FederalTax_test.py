import unittest

import sys
sys.path.append("../src")
from libs.FederalTax import FederalTax
from libs.EnumTypes import FederalTaxStatusType

Year=2024
class FederalTaxTest(unittest.TestCase):
  """ tests to verify that basic calcs from Federal Tax Brackets are correct... """

  def test_single_standard_tax_deduction(self):
      _ft=FederalTax(FileStatus=FederalTaxStatusType.Single, Year=Year)
      self.assertEqual(14600, _ft.StandardDeduction)

  def test_marriedjointly_standard_tax_deduction(self):
      _ft=FederalTax(FileStatus=FederalTaxStatusType.MarriedJointly, Year=Year)
      self.assertEqual(29200, _ft.StandardDeduction)

  def test_marriedseparate_standard_tax_deduction(self):
      _ft=FederalTax(FileStatus=FederalTaxStatusType.MarriedSeparate, Year=Year)
      self.assertEqual(14600, _ft.StandardDeduction)

  def test_HeadOfHousehold_standard_tax_deduction(self):
      _ft=FederalTax(FileStatus=FederalTaxStatusType.HeadOfHousehold, Year=Year)
      self.assertEqual(21900, _ft.StandardDeduction)

  def test_single_calcs(self):
      _tax=FederalTax(FileStatus=FederalTaxStatusType.Single, Year=Year)
          
      for _amount, _taxes in ((100, 10), (20000, 2168), (47150, 5426),  ):
          self.assertEqual(_tax.calc_taxes(_amount), _taxes, "Taxable Income=$%s, expected taxes=$%s" % (_amount, _taxes))
          
  def test_marriedjointly_calcs(self):
      _tax=FederalTax(FileStatus=FederalTaxStatusType.MarriedJointly, Year=Year)
          
      for _amount, _taxes in ((100, 10), (20000, 2000), (47150, 5194), (150000, 23106)  ):
          self.assertEqual(_tax.calc_taxes(_amount), _taxes, "Taxable Income=$%s, expected taxes=$%s" % (_amount, _taxes))
      

if __name__ == '__main__':
    unittest.main()