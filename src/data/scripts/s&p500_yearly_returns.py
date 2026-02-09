import urllib.request
#from bs4 import BeautifulSoup
#import datetime

def get_data():
    _url="https://www.slickcharts.com/sp500/returns/history.csv"

    with urllib.request.urlopen(_url) as f:
         data = f.read().decode('utf-8')

    with open("../sp500_yearly_returns.csv", "w") as f:
         f.write(data)
         
get_data()