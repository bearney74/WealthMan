import xml.etree.ElementTree as ET
from datetime import datetime, date
#from inspect import currentframe
import sys
sys.path.append("../..")

from GlobalVars import GlobalVars
from Account import Account, AllocationPeriod, AssetClass, AssetClassPeriod
from Person import Person
from IncomeSources import IncomeSource, SocialSecurity
from Expense import Expense
from EnumTypes import IncomeType, AmountPeriodType, AccountType


class Import0x1(ImportHelper):
  def __init__(self, filename):
      _xml=ET.parse(filename)
      self._root=_xml.getroot()
      assert self._root.tag == "WealthMan"
      assert self._root.attrib["Version"] == "0.1"
      
      self._ss_cola=None
      
  def get_data(self):
      return {
              'GlobalVars': self._get_globalvars_data(),
              'Persons': self._get_people_data(),
              'IncomeSources': self._get_income_data(self._ss_cola),
              'Expenses': self._get_expense_data(),
              'Assets': self._get_assets_data()
      }
  
  def _get_tag_text(self, xml, tag):
      _tag=xml.findall(tag)
      assert len(_tag) == 1
      return _tag[0].text
  
  def _get_globalvars_data(self):
      _gv = self._root.findall("./GlobalVars")
      assert len(_gv)==1
      
      _inflation_rate=self.str2float(self._get_tag_text(_gv[0], "InflationRate"))
      self._ss_cola=self.str2float(self._get_tag_text(_gv[0], "SocialSecurityCOLA"))
      #print("ss cola=%s"  % self._ss_cola)
      _ordertype = self._get_tag_text(_gv[0], "AssetWithdrawOrderByType")
      _years_to_forecast = self.str2int(self._get_tag_text(_gv[0], "YearsToForecast"))
      
      return GlobalVars(InflationRate=_inflation_rate, SocialSecurityCOLA=self._ss_cola,
                        AssetWithdrawOrderByType=_ordertype, YearsToForecast=_years_to_forecast)
      
  def _get_people_data(self):
      _people = self._root.findall("./People")
      assert len(_people) == 1
      
      _people=_people[0]   #get single item in list
      _relationstatus=_people.attrib["RelationStatus"]
      assert _relationstatus in ["Married", "Single"]
      
      #print(_relationstatus)
      
      #get person info:
      #<People RelationStatus="Married">
      #  <Person Num="1" Name="John" BirthDate="02/02/1970" Relationship="Spouse"
      #          LifeExpectancy="02/02/2060" RetirementDate="06/30/2030"/>
      #  <Person Num="2" Name="Jane" BirthDate="03/03/1971" Relationship="Spouse"
      #          LifeExpectancy="03/03/2066" RetirementDate="05/31/2030"/>
      #</People>
      _persons=_people.findall("./Person")
      assert len(_persons) > 0
      
      if _relationstatus == "Married":
          assert len(_persons) > 1
          
      #print(_persons)
    
      _person_dict={}
      for _person in _persons:
          _dict={}
          _error_flag=False
          for _attr in ["Name", "Num", "BirthDate", "RetirementDate",
                        "Relationship", "LifeExpectancy"]:
              if _attr in _person.attrib:
                 _dict[_attr]=_person.attrib[_attr]
              else:
                  _error_flag=True
                  print("Person Attribute '%s' is required" % _attr)
          if not _error_flag:
              if _dict["Num"] in _person_dict:
                  print("Error 2 people should not have the same Num value")
                  _error_flag=True
              else:
                 _person_dict[_dict["Num"]] = Person(Name=_dict["Name"], BirthDate=self.str2date(_dict["BirthDate"]),
                                                     RetirementDate=self.str2date(_dict["RetirementDate"]),
                                                     LifeExpectancy=self.str2date(_dict["LifeExpectancy"]), Relationship=_dict["Relationship"])
                 
                  
      if _error_flag:
          print("Import Errors found.  Terminating program")
          sys.exit()
          
      return _person_dict

  def _get_income_data(self, ss_cola):
      #<Income>
      # ie, Income types such as Employment, Pension, and Social Security..
      #</Income>
      
      _incomes=[]
      _income_xml = self._root.findall("./Income")
      assert len(_income_xml) == 1
      
      _incomes+=self._get_income_employment_data(_income_xml[0])
      _incomes+=self._get_income_pension_data(_income_xml[0])
      _incomes+=self._get_income_socialsecurity_data(_income_xml[0], ss_cola)
      
      return _incomes

  def _get_income_employment_data(self, income_xml):
      #  <Employment Name="John's FT Job" Amount="90000" AmountPeriod="Annual" 
      #              EndDate="05/31/2030" COLA="2.0" Taxable="Yes" Owner="1"/>
      #  <Employment Name="Jane's FT Job" Amount="60000" AmountPeriod="Annual" 
      #              EndDate="05/31/2030" COLA="3.0" Taxable="Yes" Owner="2"/>
      #  <Employment Name="John's PT Job" Amount="" AmountPeriod="Annual"
      #              BeginDate="01/01/2031" EndDate="12/31/2035" Taxable="Yes"
      #              COLA="" Owner="1"/>
      
      _employment=[]
      _emp_xml=income_xml.findall("./Employment")
      
      for _emp in _emp_xml:
          # required attributes
          _dict={}
          for _attr in ['Name', 'Amount', 'AmountPeriod', 'EndDate', 'COLA', 'Taxable', 'Owner']:
              _dict[_attr]=_emp.attrib[_attr]
              
          #optional attributes    
          for _attr in ['BeginDate', 'COLA', 'SurvivorPercent']:
              if _attr in _emp.attrib:
                 _dict[_attr]=_emp.attrib[_attr]
              elif _attr in ['BeginDate']:
                  _dict[_attr]=None
              elif _attr in ['COLA', 'SurvivorPercent']:
                  _dict[_attr]="0.0"
          
          _begin_date = self.str2date(_dict['BeginDate'])
          _end_date = self.str2date(_dict['EndDate'])
          # verify that the begin date comes before the end date
          if _begin_date is not None and _end_date is not None:
             assert _begin_date <= _end_date
          
          _inc=IncomeSource(Name=_dict['Name'], IncomeSource=IncomeType.Employment,
                            Amount=self.str2int(_dict['Amount']), AmountPeriod=AmountPeriodType[_dict['AmountPeriod']],
                            BeginDate=_begin_date, EndDate=_end_date,
                            COLA=self.str2float(_dict['COLA']), SurvivorPercent=self.strpct2float(_dict['SurvivorPercent']),
                            Taxable=_dict['Taxable'], Owner=_dict['Owner'])
          _employment.append(_inc)

      return _employment

  def _get_income_pension_data(self, income_xml):
      #  <Pension Name="John's Pension" Amount="60000" AmountPeriod="Annual" BeginDate="06/01/2030" 
      #           EndDate="Death" SurvivorPercent="100%"
      #           COLA="0" Taxable="Yes" Owner="1"/>
      
      _pensions=[]
      _emp_xml=income_xml.findall("./Pension")
      
      for _emp in _emp_xml:
          # required attributes
          _dict={}
          for _attr in ['Name', 'Amount', 'AmountPeriod', 'BeginDate', 'EndDate', 'SurvivorPercent', 'COLA', 'Taxable', 'Owner']:
              _dict[_attr]=_emp.attrib[_attr]
              
        
          _begin_date = self.str2date(_dict['BeginDate'])
          if _dict['EndDate'] == "Death":
              ## to do.. fix me
              #for now, just sent to None
              _end_date=None
          else:
             _end_date = self.str2date(_dict['EndDate'])
          # verify that the begin date comes before the end date
          if _begin_date is not None and _end_date is not None:
             assert _begin_date <= _end_date
          
          _inc=IncomeSource(Name=_dict['Name'], IncomeSource=IncomeType.Pension,
                            Amount=self.str2int(_dict['Amount']), AmountPeriod=AmountPeriodType[_dict['AmountPeriod']],
                            BeginDate=_begin_date, EndDate=_end_date, SurvivorPercent=self.strpct2float(_dict['SurvivorPercent']),
                            COLA=self.strpct2float(_dict['COLA']), Taxable=_dict['Taxable'], Owner=_dict['Owner'])
          _pensions.append(_inc)

      return _pensions

  def _get_income_socialsecurity_data(self, income_xml, COLA):
      #<SocialSecurity Name="John's SS" FRA="67" FRAAmount="50000" BeginDate="02/02/2032" 
      #                Amount="30000" Owner="1"/>
      #<SocialSecurity Name="Jane's SS" FRA="67" FRAAmount="40000" BeginDate="03/03/2033" 
      #                Amount="20000" Owner="2"/>
      
      _ss=[]
      _ss_xml=income_xml.findall("./SocialSecurity")
      
      for _emp in _ss_xml:
          # required attributes
          _dict={}
          for _attr in ['Name', 'FRA', 'FRAAmount', 'Amount', 'BeginDate', 'Owner']:
              _dict[_attr]=_emp.attrib[_attr]
          
          _begin_date = self.str2date(_dict['BeginDate'])
          
          _inc=SocialSecurity(Name=_dict['Name'], FRA=self.str2float(_dict['FRA']),
                            FRAAmount=self.str2float(_dict['FRAAmount']),
                            Amount=self.str2float(_dict['Amount']),
                            BeginDate=_begin_date, Owner=_dict['Owner'], COLA=COLA)
          _ss.append(_inc)

      return _ss

  def _get_expense_data(self):
      #<Expenses>
      #  <Expense Name="Annual Expenses" Period="Annual" Amount="36000" />
      #  <Expense Name="Health Care" Period="Annual" Amount="1200" 
      #           COLA="4"/>
      #</Expenses>

      _expenses=[]
      _expenses_xml = self._root.findall("./Expenses")
      assert len(_expenses_xml) == 1
      
      _exp_xml=_expenses_xml[0].findall("./Expense")
      
      for _exp in _exp_xml:
          # required attributes
          _dict={}
          for _attr in ['Name', 'Amount', 'AmountPeriod']:
              _dict[_attr]=_exp.attrib[_attr]
      
          for _attr in ['COLA', "BeginDate", "EndDate"]:
              if _attr in _exp.attrib:
                  _dict[_attr]=_exp.attrib[_attr]
              elif _attr in ['COLA']:
                  _dict[_attr]="0.0"
              elif _attr in ['BeginDate', 'EndDate']:
                  _dict[_attr]=None
                  
          _expense=Expense(Name=_dict['Name'], Amount=self.str2int(_dict['Amount']),
                           AmountPeriod=AmountPeriodType[_dict['AmountPeriod']],
                           BeginDate=self.str2date(_dict['BeginDate']), EndDate=self.str2date(_dict['EndDate']),
                           COLA=self.str2float(_dict['COLA']))

          _expenses.append(_expense)
          
      return _expenses
    
  def _get_assets_data(self):
      #<Assets>
      # <Account Name="Brokerage" Type="Regular" Balance="120000"
      #         UnrealizedCapitalGains="" CapitalLossCarryOver="" Owner="0">
      #   <AllocationPeriods>
      #       <Allocation BeginDate="" EndDate="05/31/2030" 
      #          PercentStocks="95" PercentBonds="5" PercentMoneyMarket="0" /> 
      #       <Allocation BeginDate="06/01/2030" EndDate="02/02/2032" 
      #          PercentStocks="60" PercentBonds="30" PercentMoneyMarket="10" />
      #       <Allocation BeginDate="02/03/2032" EndDate="" 
      #          PercentStocks="80" PercentBonds="10" PercentMoneyMarket="10" /> 
      #   </AllocationPeriods>
      # </Account>
      # <Account Name="401k" Type="TaxDeferred" Balance="300000" Owner="1">
      #   <AllocationPeriods>
      #       <Allocation BeginDate="" EndDate="" 
      #           PercentStocks="90" PercentBonds="10" PercentMoneyMarket="" /> 
      #   </AllocationPeriods>
      # </Account>
      # <Account Name="401k" Type="TaxDeferred" Balance="200000" Owner="2">
      #   <AllocationPeriods>
      #       <Allocation BeginDate="" EndDate="" 
      #           PercentStocks="90" PercentBonds="10" PercentMoneyMarket="" /> 
      #   </AllocationPeriods>
      # </Account>
      # <Account Name="John's Roth" Type="TaxFree" Balance="50000" Owner="1">
      #   <AllocationPeriods>
      #       <Allocation BeginDate="" EndDate="" 
      #          PercentStocks="85" PercentBonds="15" PercentMoneyMarket="" /> 
      #   </AllocationPeriods>
      # </Account>
      # <Account Name="Jane's Roth" Type="TaxFree" Balance="60000" Owner="2">
      #   <AllocationPeriods>
      #       <Allocation BeginDate="" EndDate="" 
      #           PercentStocks="100" PercentBonds="0" PercentMoneyMarket="" /> 
      #   </AllocationPeriods>
      # </Account>
      #</Assets>
    
      _asset_classes=self._get_assetclass_data()
      #print(_asset_classes)
      assert(len(_asset_classes) > 0)
    
      _assets=[]
      _assets_xml = self._root.findall("./Assets")
     
      assert(len(_assets_xml) == 1)
      _account_xml = _assets_xml[0].findall("./Account")
      
      for _account in _account_xml:
          #print(_account)
          # required attributes
          _dict={}
          for _attr in ['Name', 'Balance', 'Owner']:
              _dict[_attr]=_account.attrib[_attr]
      
          _dict['Type'] = AccountType[_account.attrib['Type']]
          
          for _attr in ['COLA']:
              if _attr in _account.attrib:
                  _dict[_attr]=_account.attrib[_attr]
              elif _attr in ['COLA']:
                  _dict[_attr]="0.0"
                  
          _acc=Account(Name=_dict['Name'], Type=_dict['Type'], Balance=self.str2float(_dict['Balance']), Owner=_dict['Owner'],
                       COLA=self.str2float(_dict['COLA']))

          _aps=self._get_account_allocation_periods(_account)
          _acc.set_AllocationPeriods(_aps)
          _acc.set_AssetClasses(_asset_classes)
          _assets.append(_acc)
          
      return _assets
    
  def _get_account_allocation_periods(self, xml):
      #   <AllocationPeriods>
      #       <Allocation BeginDate="" EndDate="05/31/2030" 
      #          PercentStocks="95" PercentBonds="5" PercentMoneyMarket="0" /> 
      #       <Allocation BeginDate="06/01/2030" EndDate="02/02/2032" 
      #          PercentStocks="60" PercentBonds="30" PercentMoneyMarket="10" />
      #       <Allocation BeginDate="02/03/2032" EndDate="" 
      #          PercentStocks="80" PercentBonds="10" PercentMoneyMarket="10" /> 
      #   </AllocationPeriods>

      _periods=[]
      _periods_xml = xml.findall('./AllocationPeriods')
      #print(_periods_xml)
      assert len(_periods_xml) == 1
      
      _period_xml = _periods_xml[0].findall('./Allocation')
      assert len(_period_xml) > 0
      
      for _period in _period_xml:
          _dict={}
          for _attr in ["Name", "BeginDate", "EndDate"]:
              if _attr in _period.attrib:
                 _dict[_attr]=self.str2date(_period.attrib[_attr])
              elif _attr in ["BeginDate", "EndDate"]:
                  _dict[_attr]=None
              else:
                 _dict[_attr]=""
              
          for _attr in ['PercentStocks', 'PercentBonds', 'PercentMoneyMarket']:
              if _attr in _period.attrib: 
                 _pct = _period.attrib[_attr]
                 _dict[_attr]=self.strpct2float(_pct)
              else:
                 _dict[_attr]=0.0
          
          _ap=AllocationPeriod(Name=_dict['Name'], BeginDate=_dict['BeginDate'], EndDate=_dict['EndDate'],
                           PercentStocks=_dict['PercentStocks'], PercentBonds=_dict['PercentBonds'],
                           PercentMoneyMarket=_dict['PercentMoneyMarket'])
          _periods.append(_ap)
    
      return _periods
    
  def _get_assetclass_data(self):
      # <AssetClasses>
      #   <Period BeginDate="" EndDate="12/31/2030">
      #      <Stocks RateOfReturn="5.0" StandardDeviation="20%" />
      #      <Bonds  RateOfReturn="2.0" StandardDeviation="7.5%" />
      #      <MoneyMarket RateOfReturn="-2.0%" StandardDeviation="0.1%" />
      #   </Period>
      #   <Period BeginDate="01/01/2031" EndDate="12/31/2040">
      #      <Stocks RateOfReturn="6.0" StandardDeviation="25%" />
      #      <Bonds  RateOfReturn="1.0" StandardDeviation="7%" />
      #      <MoneyMarket RateOfReturn="-3.0%" StandardDeviation="0.1%" />
      #   </Period>
      #   <Period BeginDate="01/01/2041" EndDate="">
      #     <Stocks RateOfReturn="5.0" StandardDeviation="30%" />
      #     <Bonds  RateOfReturn="3.0" StandardDeviation="10%" />
      #     <MoneyMarket RateOfReturn="-3.0%" StandardDeviation="0.1%" />
      #   </Period>
      # </AssetClasses>
  
      _ac=self._root.findall('./AssetClasses')
      assert(len(_ac) == 1)
      
      _periods=_ac[0].findall('Period')
      
      _list=[]
      for _period in _periods:
          _begin_date=self.str2date(_period.attrib["BeginDate"])
          _end_date=self.str2date(_period.attrib["EndDate"])
      
          _classes={}
          for _class in ["Stocks", "Bonds", "MoneyMarket"]:
              _c=_period.findall('./%s' % _class)
              assert(len(_c) in (0, 1))
              if len(_c) == 1:
                 _ror=self.strpct2float(_c[0].attrib["RateOfReturn"])
                 _sd=self.strpct2float(_c[0].attrib["StandardDeviation"])
              else:
                 _ror=0.0
                 _sd=0.0
              
              _classes[_class]=AssetClass(_ror, _sd)
        
          _acp=AssetClassPeriod(_classes["Stocks"], _classes["Bonds"], _classes["MoneyMarket"], BeginDate=_begin_date, EndDate=_end_date)      
          _list.append(_acp)
           
      return _list