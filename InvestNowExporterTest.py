from InvestNowExporter import *
import unittest


class InvestNowExporterTest(unittest.TestCase):

    def _get_exporter(self):
        return InvestNowExporter({
            "Smartshares - Emerging Markets Equities ESG (EMG)": {
                "instrument_code": "EMG",
                "market_code": "NZX"
            },
            "Vanguard Intl Shares Select Exclusions Index Fund - NZD Hedged": {
                "instrument_code": "VAN8287AU",
                "market_code": "FundNZ"
            },
            "Vanguard International Shares Select Exclusions Index Fund": {
                "instrument_code": "VAN1579AU",
                "market_code": "FundNZ"
            }
        })

    def test_parses_full_description(self):
        data = [
            {
                "date": "2020-12-14T00:00:00+13:00",
                "description": "Buy 123 Smartshares - Emerging Markets Equities ESG (EMG) at 2.36",
                "amount": 522.88
            },
            {
                "date": "2020-12-14T00:00:00+13:00",
                "description": "Sell 4 Vanguard Intl Shares Select Exclusions Index Fund - NZD Hedged at 1.23",
                "amount": 123.45
            },
            {
                "date": "2020-12-14T00:00:00+13:00",
                "description": "Buy 579.98  Vanguard International Shares Select Exclusions Index Fund at 1.6073",
                "amount": 1000
            },
        ]
        exporter = self._get_exporter()
        result = exporter.export(data)

        self.assertEqual(
            {
                "Trade Date": "2020-12-14T00:00:00+13:00",
                "Instrument Code": "EMG",
                "Market Code": "NZX",
                "Quantity": 123,
                "Price": 2.36,
                "Transaction Type": "Buy"
            },
            result[0]
        )

        self.assertEqual(
            {
                "Trade Date": "2020-12-14T00:00:00+13:00",
                "Instrument Code": "VAN8287AU",
                "Market Code": "FundNZ",
                "Quantity": 4,
                "Price": 1.23,
                "Transaction Type": "Sell"
            },
            result[1]
        )

        self.assertEqual(
            {
                "Trade Date": "2020-12-14T00:00:00+13:00",
                "Instrument Code": "VAN1579AU",
                "Market Code": "FundNZ",
                "Quantity": 579.98,
                "Price": 1.61,
                "Transaction Type": "Buy"
            },
            result[2]
        )

    def test_parses_sparse_description(self):
        data = [
            {
                "date": "2020-12-14T00:00:00+13:00",
                "description": "Buy Smartshares - Emerging Markets Equities ESG (EMG) at 10.00",
                "amount": 500.00
            }
        ]
        exporter = self._get_exporter()
        result = exporter.export(data)

        self.assertEqual(
            {
                "Trade Date": "2020-12-14T00:00:00+13:00",
                "Instrument Code": "EMG",
                "Market Code": "NZX",
                "Quantity": 50,
                "Price": 10.00,
                "Transaction Type": "Buy"
            },
            result[0]
        )

    def test_handles_thousands_separators(self):
        data = [
            {
                "date": "2020-12-14T00:00:00+13:00",
                "description": "Buy 1,234 Smartshares - Emerging Markets Equities ESG (EMG) at 2.36",
                "amount": 522.88
            }
        ]
        exporter = self._get_exporter()
        result = exporter.export(data)
        self.assertEqual(result[0]['Quantity'], 1234)


if __name__ == "__main__":
    unittest.main()
