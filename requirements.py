from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
# from kiteconnect import KiteConnect, KiteTicker
import pdb
import pandas as pd
import datetime
import os
import logging


api_k = "7lw9pi12k4k5d9pw"  # api_key
api_s = "8a5339s6pm1g05b9gvloauwdtggpkrkr"  # api_secret
filename = str(datetime.datetime.now().date()) + ' token' + '.txt'


def read_access_token_from_file():
    file = open(filename, 'r+')
    access_token = file.read()
    file.close()
    return access_token


def send_access_token_to_file(access_token):
    file = open(filename, 'w')
    file.write(access_token)
    file.close()


def get_login(api_k, api_s):
    global kws, kite
    kite = KiteConnect(api_key=api_k)
    print('Loggin into zerodha')

    if filename not in os.listdir():
        print("[*] Generate access Token : ", kite.login_url())
        request_tkn = input("[*] Enter Your Request Token Here : ")
        data = kite.generate_session(request_tkn, api_secret=api_s)
        access_token = data["access_token"]
        kite.set_access_token(access_token)
        kws = KiteTicker(api_k, access_token)
        send_access_token_to_file(access_token)

    elif filename in os.listdir():
        print('You have alread logged in for today')
        access_token = read_access_token_from_file()
        kite.set_access_token(access_token)
        kws = KiteTicker(api_k, access_token)

    return kite


kite = get_login(api_k, api_s)


def get_good_values(name):
    zrd_name = 'NSE:' + name
    data = kite.quote([zrd_name])

    ltp = data[zrd_name]['last_price']
    openx = data[zrd_name]['ohlc']['open']
    high = data[zrd_name]['ohlc']['high']
    low = data[zrd_name]['ohlc']['low']
    close = data[zrd_name]['ohlc']['close']
    volume = data[zrd_name]['volume']

    return ltp, openx, high, low, close, volume


def get_data(name, segment, delta, interval, continuous, oi):
    df = []
    try:
        token = kite.ltp([segment + name])[segment + name]['instrument_token']
        to_date = datetime.datetime.now().date()
        from_date = to_date - datetime.timedelta(days=delta)

        data = kite.historical_data(instrument_token=token, from_date=from_date,
                                    to_date=to_date, interval=interval, continuous=False, oi=False)
        df = pd.DataFrame(data)
        # df = df.set_index(df[data])
    except Exception as e:
        pass
    return df


def order_place(name, order_type):
    transaction_type = 'kite.TRANSACTION_TYPE_'+order_type,
    try:
        kite.place_order(variety=kite.VARIETY_REGULAR,  # VARIETY_REGULAR/VARIETY_CO
                         exchange=kite.EXCHANGE_NSE,
                         tradingsymbol=name,
                         transaction_type=transaction_type,
                         quantity=1,
                         price=0.001,
                         order_type=kite.ORDER_TYPE_MARKET,  # ORDER_TYPE_MARKET/ORDER_TYPE_LIMIT
                         product=kite.PRODUCT_CNC  # PRODUCT_CNC/PRODUCT_CO
                         )
        order_status = order_type + ' order placed in ' + name
    except Exception as e:
        order_status = "Order placement failed: {}".format(e)
        pass
    return order_status
