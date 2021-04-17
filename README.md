# InvestNow Exporter

## Purpose 
The purpose of this project is to export [InvestNow](https://investnow.co.nz/)'s transaction to a format that can be imported by [Sharesight](https://www.sharesight.com/nz/)

## Pre-requisite
* Python3

## Note
Current the exporter only supports funds outlined in market_code.json. This is due to InvestNow's customizing the name of each fund, making it very difficult to find the instrument code and market code. 
* If you see some funds are missing (Chances are there are a lot, please submit a pull request to update the `market_code.json`) Automatic detection will hopefully done soon to remove the need for this market_code.json file.

## Instructions
* Open InvestNow and click on "Activity"
* Click on "Show all my investment transactions" and select "For the Year"
* Press F12 on Chrome to launch dev tools and clock on "Network" tab, ensure that you are on "XHR"
* Click on "Search" in the website
* You should see some new content being added in the XHR content, click on the one that says "activity?accountId=...."
* Click on "Preview" - this shows all of your investment activity over the past year
* Right click at the root level and click on copy object
* Paste it in investment.json in this repo
* Run `python3 InvestnowExporter.py`