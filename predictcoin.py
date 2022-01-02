from fbprophet import Prophet
import pyupbit

class PredictCoin:

    def __init__(self, event):
        self.event = event
        self.model = None
        self.forecast = None

    def getData(self):
        #BTC 최근 200시간의 데이터 불러옴
        df = pyupbit.get_ohlcv(self.event, interval="minute60")

        #시간(ds)와 종가(y)값만 남김
        df = df.reset_index()
        df['ds'] = df['index']
        df['y'] = df['close']
        data = df[['ds','y']]
        return data
    
    # 학습하기 
    def educate(self):
        self.model = Prophet()
        self.model.fit(self.getData())

    # 24시간 미래 예측 
    def predict(self):
        future = self.model.make_future_dataframe(periods=24, freq='H')
        self.forecast = self.model.predict(future)
        
    #매수 시점의 가격 
    def getNowPrice(self):
        nowValue = pyupbit.get_current_price(self.event)
        return nowValue

    #종가 가격 
    def getClosePrice(self):
        data = self.getData()
        #현재 시간이 자정 이전
        closeDf = self.forecast[self.forecast['ds'] == self.forecast.iloc[-1]['ds'].replace(hour=9)]
        #현재 시간이 자정 이후
        if len(closeDf) == 0:
            closeDf = self.forecast[self.forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]

        #최종 당일 종가
        closeValue = closeDf['yhat'].values[0]
        return closeValue


if __name__ == "__main__":

    event = "KRW-BTC"
    pc = PredictCoin(event)
    pc.educate()
    pc.predict()

    #구체적인 가격
    print("현재 시점 가격: ", pc.getNowPrice())
    print("종가의 가격: ", pc.getClosePrice())
