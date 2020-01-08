import unittest
from trader.binanceCom import BinanceCom

class TestBinanceCom(unittest.TestCase):

    def test_connect_to_account(self):
        bc = BinanceCom()
        self.assertIsNotNone(bc.connect_to_account(bc.default_Key, bc.default_Secret))
        self.assertRaises(ValueError, bc.connect_to_account, None, None)        
    
    def test_get_coin_info(self):
        bc = BinanceCom()
        client=bc.connect_to_account(bc.default_Key, bc.default_Secret)
        coin_info = bc.get_coin_info(client, "BTCUSDT")
        self.assertTrue('symbol' in coin_info)
        self.assertTrue('lastPrice' in coin_info)
        self.assertTrue('openPrice' in coin_info)
        self.assertTrue('volume' in coin_info)
        self.assertTrue('highPrice' in coin_info)
        self.assertTrue('lowPrice' in coin_info)
    
    
if __name__ == '__main__':
    unittest.main()