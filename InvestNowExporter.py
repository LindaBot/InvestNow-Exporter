import re
import json
import csv
from NameDecoder import decodeMarketName

class InvestNowExporter:
    def __init__(self, json_file_name, output_csv_name):
        self.investmentJSON = self.load_JSON(json_file_name)
        self.output_csv_name = output_csv_name
        self.__write_to_CSV(self.get_investment_detail())
    
    def load_JSON(self, json_file_name):
        with open(json_file_name) as investmentFile:
            # Deserializing the data
            return json.load(investmentFile)

    def get_investment_detail(self):
        transaction_details = []
        for row in self.investmentJSON:
            detail = []
            detail.append(row['date'])
            detail.extend(self.__deconstruct_description(row))
            transaction_details.append(detail)
        
        return(transaction_details)

    def __deconstruct_description(self, row):
        """Deconstruct a cryptic descrption string given by investnow to instrument_code, market_code, quantity, price and transaction_type
        I hate InvestNow JSON too.
        Args:
            row ([JSON]): [One row of the transaction JSON]
        """        
        # TODO: Optimize this so it doesn't need to compile on every run.
        pattern = r'(Buy|Sell)\s([0-9]?.?[0-9]+)\s(.+)\sat\s([0-9]+\.?[0-9]+)'
        compiled_regex = re.compile(pattern)
        match = compiled_regex.match(row['description'])

        [instrument_code, market_code, quantity, price, transaction_type] = [None, None, None, None, None]
        try:
            [_, transaction_type, quantity, name, price] = [match[0], match[1], match[2], match[3], match[4]]
            [instrument_code, market_code] = decodeMarketName(name.strip())
        except Exception as exception:
            if (type(exception) == ValueError):
                raise exception
            else:
                [instrument_code, market_code, quantity, price, transaction_type] = self.__deconstruct_dumb_description(row)

        return instrument_code, market_code, round(float(quantity), 2), round(float(price), 2), transaction_type

    def __deconstruct_dumb_description(self, row):
        # TODO: Optimize this so it doesn't need to compile on every run.
        pattern = r'(Buy|Sell)\s(.+)\sat\s([0-9]+\.?[0-9]+)'
        compiled_regex = re.compile(pattern)
        match = compiled_regex.match(row['description'])

        [_, transaction_type, name, price] = [match[0], match[1], match[2], float(match[3])]
        [instrument_code, market_code] = decodeMarketName(name)
        quantity = round(float(row['amount']) / float(price), 2)

        return (instrument_code, market_code, quantity, price, transaction_type)

    def __write_to_CSV(self, transactions):
        with open(self.output_csv_name, "w+", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(["Trade Date", "Instrument Code", "Market Code", "Quantity", "Price", "Transaction Type"])
            for transaction in transactions:
                writer.writerow(transaction)

if __name__ == "__main__":
    exporter = InvestNowExporter("investment.json", "investment.csv")