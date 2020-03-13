import pandas as pd

# btc = pd.read_csv("multiMarket/BTC-USD.csv")
# sNp = pd.read_csv("multiMarket/^GSPC.csv")
# dow_jones = pd.read_csv("multiMarket/^DJI.csv")
# nasdaq = pd.read_csv("multiMarket/^IXIC.csv")
# # print(btc)
# print(btc.shape, sNp.shape, dow_jones.shape, nasdaq.shape)
# # exit()

# nbtc = {"Date":[], "Open":[], "High":[], "Low":[], "Close":[], "Adj Close":[], "Volume":[]}
# for index in range(sNp.shape[0]):
#     key = sNp["Date"][index]
#     item = btc.loc[btc["Date"]==key]
#     item = item.to_numpy()
#     # print(item, "\t\t", key, "\t\t", len(item), nbtc)
#     # exit()
#     nbtc["Date"].append(item[0][0])
#     nbtc["Open"].append(item[0][1])
#     nbtc["High"].append(item[0][2])
#     nbtc["Low"].append(item[0][3])
#     nbtc["Close"].append(item[0][4])
#     nbtc["Adj Close"].append(item[0][5])
#     nbtc["Volume"].append(item[0][6])
#     # print(f"DATE: {btc['Date'][index]} BTC: {btc['Close'][index]} S&P: {sNp['Close'][index]} DOW: {dow_jones['Close'][index]} NASDAQ: {nasdaq['Close'][index]}")
# nbtc = pd.DataFrame(data=nbtc)
# print(nbtc)
# nbtc.to_csv("multiMarket/BTCUSD.csv")


# data = []
# with open("multiMarket/BTCUSD.csv", "r") as f:
#     btc = f.readlines()
#     # print(btc)
#     for item in btc:
#         i = item.split(",")
#         i.pop(0)
#         si = ""
#         for s in i:
#             si+=str(s)+","
#         si = si[:-1]
#         data.append(si)
#     print(data)

# sdata = ""
# for item in data:
#     sdata+=item

# with open("multiMarket/BTC_USD.csv", "w") as f:
#     f.write(sdata)

btc = pd.read_csv("multiMarket/BTC_USD.csv")
sNp = pd.read_csv("multiMarket/^GSPC.csv")
dow_jones = pd.read_csv("multiMarket/^DJI.csv")
nasdaq = pd.read_csv("multiMarket/^IXIC.csv")
print(btc.shape, sNp.shape, dow_jones.shape, nasdaq.shape)