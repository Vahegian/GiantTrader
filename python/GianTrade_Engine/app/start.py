from trader.binanceCom import BinanceCom
import time


if __name__ == "__main__":
    bc = BinanceCom()
    client = bc.connect_to_account(bc.default_Key, bc.default_Secret)
    print(bc.get_coin_info(client, "BTCUSDT"))
    # engine = db.create_engine('postgres://user:pass@docker_db_1:5432/db')
    # print(engine)
    # while True:
    #     print("waited")
    