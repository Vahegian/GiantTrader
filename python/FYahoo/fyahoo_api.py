import yfinance as yf

class FYahoo:
    def __init__(self):
        self.tickers = {}

    def open_ticker(self, ticker :str):
        if ticker in self.get_avalable_tickers():
            return True
        else:
            try:
                self.tickers.update({
                    ticker: yf.Ticker(ticker)
                })
                return True
            except Exception as e:
                print(e.with_traceback(e))
                return False

    def get_history(self, ticker :str, period :str = "max"):
        if ticker in self.get_avalable_tickers():
            return self.tickers[ticker].history(period=period)
        else:
            print("please open ticker first call 'open_ticker(*args)' ")
            return False

    def get_avalable_tickers(self):
        return list(self.tickers.keys())
            

if __name__ == "__main__":
    ticker = "BTC-USD"
    fy = FYahoo()
    fy.open_ticker(ticker)
    hist = fy.get_history(ticker, period="max") # 1mo, 1wk, 1m, 1d, max etc.
    print(hist, type(hist))
    print(f"last close: {hist['Close'][-1]}")
