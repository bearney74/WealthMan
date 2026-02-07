import urllib.request
from bs4 import BeautifulSoup
import datetime
import csv

def get_data():
    _url="https://www.multpl.com/s-p-500-historical-prices/table/by-month"

    with urllib.request.urlopen(_url) as f:
         html = f.read().decode('utf-8')

    with open("../temp/sp500_returns.html", "w") as f:
         f.write(html)

def parse_data():
    with open("../temp/sp500_returns.html", "r") as f:
         _data=f.read()

    soup = BeautifulSoup(_data, 'html.parser')

    d={}
    _table=soup.find(id="datatable")
    for _row in _table.find_all('tr'):
        _tds=_row.find_all('td')
        if _tds != []:
           #print(_tds)
           assert len(_tds) == 2
           _date=str(_tds[0].string)
           _dt=datetime.datetime.strptime(_date, "%b %d, %Y")

           #remove junk from number
           _number=str(_tds[1].string).replace('\n\u2002\n', '')
           _number=_number.replace("\n", "")
           _number=_number.replace(",", "")
           _number=float(_number)
           d[_dt]=_number

    return d

def process_data(dict):
    _dates=list(dict.keys())
    #print(_dates)
    #the dates should be sorted, but do it just in case..
    _dates.sort()
    #_dates=_dates[:100]
    #_dates.reverse()
    
    #calculate percent of returns per month
    _previous=None
    _percents={}
    for _date in _dates:
        if _previous is not None:
            _value=dict[_date]
            _percents[_date]="%6.4f" % (100.0 * (_value - _previous)/_previous)
        else:
            _percents[_date]="0.0"
        _previous=dict[_date]

    #write out date, value, and percent
    _dates=list(_percents.keys())
    _dates.sort()
    with open("../s&p500_monthly_returns.csv", "w") as f:
         _csv=csv.writer(f)
         for _date in _dates:
             _csv.writerow([_date.strftime("%Y-%m-%d"), dict[_date], _percents[_date]])
            

#get_data()
_dict=parse_data()
process_data(_dict)
