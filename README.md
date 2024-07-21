[![codecov](https://codecov.io/github/bearney74/WealthMan/graph/badge.svg?token=HEIDX9MMDN)](https://codecov.io/github/bearney74/WealthMan)

# WealthMan
This is a desktop application for financial planning.

## Description
Users can enter basic personal information, income sources, expenses, and basic 
asset information. Certain assumptions such as inflation rate, and asset rate of 
return can be entered by the user.

From that information, projections (forecasts) can be made for several years in 
the future showing how income, assets, and expenses affect a person's net worth.

Currently, users can output the projection data in csv format, that can be imported 
into a spreadsheet application (Excel, Libre Calc) for further analysis.

Charts can be generated for each projection variable, as well as custom charts for 
asset totals, income totals and asset contribution totals.

## How to run..
install the modules in the requirements.txt file
pip install -r requirements.txt

python src/main.py

## Future Plans / Development
I plan on using historic market returns, as well as Monte Carlo simulations to 
calculate risk.

I would also like to create an interface for "what if" scenarios, which will include possible
cost savings if roth conversions are done, etc.



FYI.   This project is still under HEAVY development and is not ready for use by end users.  
Developers and early adopters can use the program, but should be suspicious of any generated output.
I am interested in feedback.  Please submit any issues/bugs, feature requests to the issues tab above.

