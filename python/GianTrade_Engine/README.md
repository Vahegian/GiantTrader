# Trading Software 

### trader/BinanceCom usage:
```python
bc = BinanceCom()
# Create client which will send requests to exchange, default values will not enable trading.
isConected = bc.connect_to_account(bc.default_Key, bc.default_Secret)
# Get exchange request limits, values will be members of the class.
bc.update_request_limits()
# Get wallet content only assets with value will be presented.
print("\n",bc.get_wallet())
# Get open orders
oOrder = bc.get_open_orders()
print("\n", oOrder)
# Cancel an active order
print("\n", bc.cancel_order("BTCUSDT", oOrder['BTCUSDT']['orderId']))
#put sell limit order
print(bc.put_limit_order_sell("BTCUSDT", 1.6, 8000))
# get live update from web socket, all tickers
p = lambda msg: print(msg[0]['s'], msg[0]['p'])
bc.get_live_ticker_update(p)
#get historical OHLCV data
print("\n", bc.get_hist_data_day_interval("BTCUSDT", 3))
```

### db/connector usage:
```python
c = Connector()
c.connect("dbname","myuser","pass")
c.create_table("tname", '''id INT PRIMARY KEY NOT NULL,
                            name TEXT NOT NULL,
                            enc_pass CHAR(128)''')
c.insert_into_table("tname", "id, name, enc_pass", '''(1, 'name1', '9234708uj')''')
c.insert_into_table("tname", "id, name, enc_pass", '''(2, 'name2', '9254708uj')''')
print(c.select_from("tname", "*", "enc_pass>'92'", "name", dec=True, limit=1))
c.update_table("tname", "name='name3'", "id='1'")
print(c.select_from("tname", "*"))
c.delete_from("tname", "id='2'")
print(c.select_from("tname", "*"))
c.drop_table("tname")
c.disconnect()
```