import pytest
import pandas as pd 
from pandas import DataFrame, Series
import numpy as np


@pytest.fixture
def dataframe():
    file = "~/data/marketdata/data/ABB-1999-06-22-2024-04-30.csv"
    df = pd.read_csv(file)
    df = df.drop("Unnamed: 11", axis=1)
    df = df.convert_dtypes()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    return df

# @pytest.mark.usefixtures("df")
def test_load(dataframe):
    df = dataframe

    print(df.dtypes)
    

    # fill NA in Average price column
    fill_average_s = average_price(df['High price'], df['Low price'])
    df['Average price'] = df['Average price'].fillna(fill_average_s)
    # forward fill all dates that do not have any data
    df['Average price'] = df['Average price'].ffill()

    assert df['Average price'].hasnans == False

    # set opening price
    df['Opening price'] = df['Opening price'].fillna(df['Average price'])
    
    assert df['Opening price'].hasnans == False

    # Forward fill turnover
    df['Turnover'] = df['Turnover'].ffill()

    # check total_volume
    fill_volume_s = total_volume(df['Turnover'], df['Average price'])
    df['Total volume'] = df['Total volume'].fillna(fill_volume_s)


    assert df['Total volume'].hasnans == False

    print("Finished!")



def average_price(high_price: Series, low_price: Series):
    return high_price.add(low_price).multiply(0.5)

def total_volume(turnover: Series, average: Series):
    return turnover.div(average)
        

if __name__=="__main__":
    pytest.main()