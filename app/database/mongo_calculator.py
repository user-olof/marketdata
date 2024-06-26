from app.database import mongo_manager
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from datetime import datetime
from dateutil.relativedelta import relativedelta

def average_price(high_price: Series, low_price: Series):
    return high_price.add(low_price).multiply(0.5)


def total_volume(turnover: Series, average: Series):
    return turnover.div(average).astype('int64')

def get_date_range(df: DataFrame, from_date: datetime, to_date: datetime):
    res = df.loc[from_date.strftime("%Y-%m-%d"):to_date.strftime("%Y-%m-%d") ]
    return res

def get_time_difference(from_date: datetime, to_date: datetime):
    return relativedelta(to_date, from_date)

def time_difference_in_years(from_date: datetime, to_date: datetime):
    time_diff = to_date - from_date
    years = float(time_diff.days) / 365.2425
    return years 

def annualized_stock_price_return(stock_price_return: np.float64, from_date: datetime, to_date: datetime):
    years = time_difference_in_years(from_date, to_date)
    return np.power(stock_price_return, 1/years) - 1.0


def stock_price_return(col_name: str, from_date: datetime, to_date: datetime):
    res = mongo_manager.get_all(col_name)
    tmp = list(res)
    df = pd.DataFrame(tmp)
    df = df.set_index('Date')
    p1 = df.loc[from_date]
    p2 = df.loc[to_date]
    res = (p2['Average price'] / p1['Average price']) - 1
    return res
