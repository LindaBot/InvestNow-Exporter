from InvestNowExporter import *
from NameDecoder import *

def load_JSON():
    test_cases = [
        ["investment.json", "investment.csv"]
        ]
    for i, test_case in enumerate(test_cases):
        exporter = InvestNowExporter(test_cases[0][0], test_cases[0][1])
        assert exporter.investmentJSON != None, ("Load JSON failed")

def market_name_decoding():
    # Test case: [Name, instrument_code, market_code]
    test_cases = [["Vanguard Intl Shares Select Exclusions Index Fund - NZD Hedged", "VAN8287AU", "FundNZ"]]
    for i, test_case in enumerate(test_cases):
        [instrument_code, market_code] = decodeMarketName(test_case[0])
        assert [instrument_code, market_code] == [test_case[1], test_case[2]], ("Decode market name failed")

if __name__ == "__main__":
    load_JSON()
    market_name_decoding()
    print("All tests passed")