import time
import pyupbit
import datetime
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

access = os.getenv("access")
secret = os.getenv("secret")

# 변동성 돌파 전략 
def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

# 시작 시간 조회 
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

# 잔고 조회 
def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

# 현재가 조회 
def get_current_price(ticker):
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def get_kind_of_coin(ticker):
    return ticker.split('-')[1]


if __name__ == "__main__":

    event = "KRW-MBL"
    K = 0.4

    # 로그인
    upbit = pyupbit.Upbit(access, secret)
    print("현재 KRW:", upbit.get_balance("KRW")) 
    print("autotrade start")
    # 자동매매 시작
    while True:
        try:
            # 현재시간, 시작 시간, 끝나는 시간 
            now = datetime.datetime.now() 
            start_time = get_start_time(event) # 9
            end_time = start_time + datetime.timedelta(days=1) # 9 + 1
            if start_time < now < end_time - datetime.timedelta(seconds=10): # 8시 59분 50초까지
                target_price = get_target_price(event, K) # 매수 목표가 
                current_price = get_current_price(event)
                print("Target: {0}, Now: {1}".format(target_price, current_price))
                if target_price < current_price:
                    krw = get_balance("KRW")
                    if krw > 5000: # 최소 거래 금액 5000원 이상이면 
                        print("매수합니다.")
                        upbit.buy_market_order(event, krw*0.9995) # 수수료 0.05퍼센트 빼고
            else:
                # 전량 매도하기 
                coin = get_kind_of_coin(event)
                amount = get_balance(coin)
                if amount > 0.00008:
                    print("매도합니다.")
                    upbit.sell_market_order(event, amount*0.9995) # 수수료를 제외하고 매도 
            time.sleep(1)
            
        except Exception as e:
            print(e)
            time.sleep(1)