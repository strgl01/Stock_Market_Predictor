"""Feed updated data till today logic depends on that and run code on Buisness Days
 Download Data from https://www.nseindia.com/report-detail/eq_security
 Valid fo EQ series"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime


class TeachnicalAnalysis:
    def __init__(self, data):
        self.data = pd.read_csv(data)
        self.date = pd.to_datetime("today").date().strftime("%Y-%m-%d")
        self.clean_data = self.clean()
        self.close = self.clean_data.loc[
            pd.to_datetime(self.date) - pd.Timedelta(days=1)
        ]["Close Price"]
        self.predict = []
        if self.trend == "uptrend":
            self.predict.append(1)
        else:
            self.predict.append(0)
        if self.Volume == "Bullish":
            self.predict.append(1)
        else:
            self.predict.append(0)
        if self.Indicator == "RSI Buy" or self.Indicator == "MACD Buy":
            self.predict.append(1)
        else:
            self.predict.append(0)

    def clean(self):
        self.data.columns = self.data.columns.str.strip()
        self.data = self.data[self.data["Series"] == "EQ"]
        self.data["Date"] = pd.to_datetime(self.data["Date"])
        self.data.set_index("Date", inplace=True)
        self.data.drop(
            columns=["Last Price", "No. of Trades", "Turnover ₹"], inplace=True
        )
        self.data["Prev Close"] = self.data["Prev Close"].str.replace(",", "")
        self.data["Prev Close"] = self.data["Prev Close"].astype("Float64")
        self.data["Open Price"] = self.data["Open Price"].str.replace(",", "")
        self.data["Open Price"] = self.data["Open Price"].astype("Float64")
        self.data["High Price"] = self.data["High Price"].str.replace(",", "")
        self.data["High Price"] = self.data["High Price"].astype("Float64")
        self.data["Low Price"] = self.data["Low Price"].str.replace(",", "")
        self.data["Low Price"] = self.data["Low Price"].astype("Float64")
        self.data["Close Price"] = self.data["Close Price"].str.replace(",", "")
        self.data["Close Price"] = self.data["Close Price"].astype("Float64")
        self.data["Average Price"] = self.data["Average Price"].str.replace(",", "")
        self.data["Average Price"] = self.data["Average Price"].astype("Float64")
        self.data["Total Traded Quantity"] = self.data[
            "Total Traded Quantity"
        ].str.replace(",", "")
        self.data["Total Traded Quantity"] = self.data["Total Traded Quantity"].astype(
            "Float64"
        )
        self.data["Deliverable Qty"] = self.data["Deliverable Qty"].str.replace(",", "")
        self.data["Deliverable Qty"] = self.data["Deliverable Qty"].astype("Float64")
        self.data["% Dly Qt to Traded Qty"] = self.data[
            "% Dly Qt to Traded Qty"
        ].str.replace(",", "")
        self.data["% Dly Qt to Traded Qty"] = self.data[
            "% Dly Qt to Traded Qty"
        ].astype("Float64")
        return self.data

    def trend(self):
        # self.clean_data['Close Price'].plot(kind='line')
        # plt.show()

        # for 5 days trend need to handle weekends
        date_range = pd.date_range(
            start=pd.to_datetime(self.date) - pd.Timedelta(days=5),
            end=pd.to_datetime(self.date),
            freq="B",
        )
        # print(date_range)
        if (
            self.clean_data.loc[date_range[0]]["Close Price"]
            - self.clean_data.loc[date_range[-1]]["Close Price"]
            > 0
        ):
            return "uptrend"
        else:
            return "down trend"

        # for 15 days
        date_range = pd.date_range(
            start=pd.to_datetime(self.date) - pd.Timedelta(days=15),
            end=pd.to_datetime(self.date),
            freq="B",
        )
        print(date_range)
        if (
            self.clean_data.loc[date_range[0]]["Close Price"]
            - self.clean_data.loc[date_range[-1]]["Close Price"]
            > 0
        ):
            print("uptrend")
        else:
            print("down trend")

        # for 25 days
        date_range = pd.date_range(
            start=pd.to_datetime(self.date) - pd.Timedelta(days=25),
            end=pd.to_datetime(self.date),
            freq="B",
        )
        print(date_range)
        if (
            self.clean_data.loc[date_range[0]]["Close Price"]
            - self.clean_data.loc[date_range[-1]]["Close Price"]
            > 0
        ):
            print("25 days uptrend")
        else:
            print("25 day downtrend")

    def Supp_Res(self):
        # need to use trend fn to determine range of days from which trend change and use min/max value respectively to get Supp and res
        pass

    def Volume(self):
        curr_v = self.clean_data.loc[pd.to_datetime(self.date)]["Total Traded Quantity"]
        Avg_v = (
            self.clean_data.loc[
                pd.to_datetime(self.date)
                - pd.Timedelta(days=10) : pd.to_datetime(self.date)
            ]["Total Traded Quantity"].sum()
        ) / 10

        curr_p = self.clean_data.loc[pd.to_datetime(self.date)]["Close Price"]
        Avg_p = (
            self.clean_data.loc[
                pd.to_datetime(self.date)
                - pd.Timedelta(days=10) : pd.to_datetime(self.date)
            ]["Close Price"].sum()
        ) / 10
        if curr_v > Avg_v:
            if curr_p > Avg_p:
                return "Bullish"
            else:
                return "Bearish"
        if curr_v < Avg_v:
            if curr_p > Avg_p:
                return "Bullish-Doutfull"
            else:
                return "Bearish-Doubtfull"

    def MVA(self, day):
        MVA = (
            self.clean_data.loc[
                pd.to_datetime(self.date)
                - pd.Timedelta(days=day) : pd.to_datetime(self.date)
            ]["Close Price"].sum()
        ) / day
        return MVA
        if MVA < self.close:
            print("Buy")
        else:
            print("Do not buy")

    def Indicator(self):
        close_rsi = self.clean_data.loc[
            pd.to_datetime(self.date)
            - pd.Timedelta(days=14) : pd.to_datetime(self.date)
        ]["Close Price"]
        temp = close_rsi.reset_index()
        loss = [0]
        gain = [0]
        for i in range(close_rsi.shape[0]):
            if i == 0:
                continue
            if temp.iloc[i]["Close Price"] - temp.iloc[i - 1]["Close Price"] < 0:
                loss.append(
                    abs(temp.iloc[i]["Close Price"] - temp.iloc[i - 1]["Close Price"])
                )
            else:
                loss.append(0)

            if temp.iloc[i]["Close Price"] - temp.iloc[i - 1]["Close Price"] > 0:
                gain.append(
                    temp.iloc[i]["Close Price"] - temp.iloc[i - 1]["Close Price"]
                )
            else:
                gain.append(0)
        temp["loss"] = loss
        temp["gain"] = gain
        avg_l = temp["loss"].sum() / temp.shape[0]
        avg_p = temp["gain"].sum() / temp.shape[0]
        rs = avg_p / avg_l
        self.rsi = 100 - (100 / (1 + rs))
        if self.rsi > 0 and self.rsi <= 30:
            return "RSI Buy"
        elif self.rsi > 70 and self.rsi <= 100:
            return "RSI Sell"
        # else:
        #     return("RSI Hold")
        if self.MVA(12) - self.MVA(26) > self.MVA(9):
            return "MACD Buy"
        else:
            return "MACD Sell"


class SinglePattern(TeachnicalAnalysis):
    def __init__(self, data):
        super().__init__(data)
        self.Marubozu()
        self.doji()
        self.Paper_Umb()

    def Marubozu(self):
        temp_ser = self.clean_data.loc[self.date]
        if (
            temp_ser["Open Price"] == temp_ser["Low Price"]
            and temp_ser["Close Price"] == temp_ser["High Price"]
        ):
            # print("perfect Marubozu")
            self.predict.append(1)
        elif (
            temp_ser["Open Price"] - temp_ser["Low Price"] < 2
            and temp_ser["High Price"] - temp_ser["Close Price"] < 2
        ):
            # print("partial marubozu")
            self.predict.append(1)
        else:
            # print("no marubozu")
            self.predict.append(0)

    def doji(self):
        temp_ser = self.clean_data.loc[self.date]

        if temp_ser["Open Price"] == temp_ser["Close Price"]:
            # print("perfect Doji")
            self.predict.append(1)
        elif temp_ser["Open Price"] - temp_ser["Close Price"] < 2:
            # print("partial Doji")
            self.predict.append(1)
        else:
            # print("no Doji")
            self.predict.append(0)

    def Paper_Umb(self):
        temp_ser = self.clean_data.loc[self.date]
        if (
            temp_ser["Close Price"] == temp_ser["High Price"]
            and temp_ser["Low Price"] - temp_ser["Open Price"]
            == 2 * (temp_ser["Close Price"] - temp_ser["Open Price"])
            and self.trend() == "down trend"
        ):
            # print("perfect Hammer")
            self.predict.append(1)

        else:
            # print("Hanging Man")
            self.predict.append(0)

    def Buy_Sell(self):
        if self.predict.count(1) > self.predict.count(0):
            print("Buy")
        else:
            print("Sell")


result = SinglePattern("C:/Users/dell/Desktop/Stock_Market_Analysis/HDFC.csv")
result.Buy_Sell()
