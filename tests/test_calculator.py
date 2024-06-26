import pytest
import pandas as pd
import app.database.mongo_calculator as mc
from datetime import datetime
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

def test_stock_price_return(dataframe):
    from_date = datetime(2022, 6, 22)
    to_date = datetime(2024, 4, 30)
    res = mc.stock_price_return(dataframe, from_date, to_date)
    
    assert np.round(res, 2) == float(1.05)

if __name__ == '__main__':
    pytest.main()