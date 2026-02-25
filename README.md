[![codecov](https://codecov.io/github/bearney74/WealthMan/graph/badge.svg?token=HEIDX9MMDN)](https://codecov.io/github/bearney74/WealthMan)

# WealthMan
This is a desktop application for Wealth Management.  This program generates simulations of future asset growth.
I am not a Certified Financial Planner (CFP), so take all results from this program with a grain of salt.
I am looking for individuals to test the output to see if the results are accurate.  Feel free to submit 
issues.

This applications should be able to run on Windows, Linux, and MacOS (just about anywhere where Python 3 
and PyQt can run)

## Description
Users can enter basic personal information, income sources, expenses, and basic 
asset information. Certain assumptions such as inflation rate, and asset rate of 
return per account can be entered by the user.

From the inputted valies, projections (forecasts) can be made for several years in 
the future showing how income, assets, and expenses affect a person's net worth.

Currently, users can output the projection data in csv format, that can be imported 
into a spreadsheet application (Excel, Libre Calc) for further analysis.

Charts can be generated for each projection variable, as well as custom charts for 
asset totals, income totals and asset contribution totals.

## How to run..
Install the modules in the requirements.txt file:

pip install -r requirements.txt

Start the gui:

python src/main.py

## Future Plans / Development
I plan on using historic market returns, as well as Monte Carlo simulations to 
calculate risk.

I would also like to create an interface for "what if" scenarios, which will include possible
cost savings if roth conversions are done, etc.


FYI.   This project is still under HEAVY development and is not ready for production.  All generated
output should be checked and double checked for accuracy.
I am interested in feedback.  Please submit any issues/bugs, feature requests to the issues tab above.

## Screenshots

### Basic Info
![Basic Info](../README/media/basic_info_v0_2.jpg)

### Income Tab
![Income Tab](../README/media/income_v0_2.jpg)

### Expenses Tab
![Expenses Tab](../README/media/expenses_v0_2.jpg)

### Assets Tab 
![Assets Tab](../README/media/assets_v0_2.jpg)

### Global Variables
![Global Variables Tab](../README/media/globalvariables_v0_2.jpg)

### Output (Details)
![Details Tab](../README/media/details_v0_2.jpg)

### CSV Output
[details.csv](../README/media/details_v0_2.csv)

### Asset Total Chart
![Asset Total Chart](../README/media/charts_asset_total_v0_2.jpg)

### Asset Total Chart (By Assets)
![Asset Total Chart By Assets](../README/media/custom_charts_asset_totals_v0_2.jpg)
