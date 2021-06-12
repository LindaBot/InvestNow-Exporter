import re
import json
import csv
import io
import argparse

class InvestNowExporter:

    def __init__(self, market_codes) -> None:
        self.market_codes = market_codes
    
    def export(self, rows):
        return [self._parse_row(row) for row in rows]

    def _parse_row(self, row):
        """Deconstruct a cryptic descrption string given by investnow to instrument_code, market_code, quantity, price and transaction_type
        I hate InvestNow JSON too.
        Args:
            row ([JSON]): [One row of the transaction JSON]
        """        
        # Example: Buy 1,234 Smartshares - Emerging Markets Equities ESG (EMG) at 2.36
        full_pattern = re.compile(
            r'(?P<transaction_type>Buy|Sell)\s'
            r'(?P<quantity>[0-9,]?.?[0-9]+)\s'
            r'(?P<name>.+)\s'
            r'at\s(?P<price>[0-9,]+\.?[0-9]+)'
        )
        
        # Example: Buy Smartshares - Emerging Markets Equities ESG (EMG) at 2.36
        sparse_pattern = re.compile(
            r'(?P<transaction_type>Buy|Sell)\s'
            r'(?P<name>.+)\s'
            r'at\s(?P<price>[0-9,]+\.?[0-9]+)'
        )
        
        full_match = full_pattern.match(row['description'])
        sparse_match = sparse_pattern.match(row['description'])
        if (full_match):
            name = full_match.group('name').strip()
            price = full_match.group('price').replace(',', '')
            quantity = full_match.group('quantity').replace(',', '')
            transaction_type = full_match.group('transaction_type')
        elif(sparse_match):
            name = sparse_match.group('name').strip()
            price = sparse_match.group('price').replace(',', '')
            # Infer quantity
            quantity = round(float(row['amount']) / float(price), 2)
            transaction_type = sparse_match.group('transaction_type')
        
        return {
            "Trade Date": row['date'],
            "Instrument Code": self.market_codes[name]['instrument_code'],
            "Market Code": self.market_codes[name]['market_code'],
            "Quantity": round(float(quantity), 2),
            "Price": round(float(price), 2),
            "Transaction Type": transaction_type
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converts Investnow activity JSON into Sharesight compatible CSV')
    parser.add_argument('jsonfile', type=str, help='Path to the JSON input file')
    parser.add_argument('--market-codes-file', type=str, help='Path to market codes', dest='marketcodesfile', default='data/market_codes.json')
    
    args = parser.parse_args()
    with open(args.jsonfile) as f:
        investnow_investments = json.load(f)

    with open(args.marketcodesfile) as f:
        market_codes = json.load(f)

    exporter = InvestNowExporter(market_codes)
    sharesight_investments = exporter.export(investnow_investments)
    
    output = io.StringIO()
    writer = csv.writer(output, delimiter=',')
    writer.writerow(sharesight_investments[0].keys())
    for sharesight_investment in sharesight_investments:
        writer.writerow(sharesight_investment.values())

    print(output.getvalue())