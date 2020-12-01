# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 22:45:55 2020

@author: lucas
"""
# Imports
import pandas as pd
import yahooquery as yq
from datetime import datetime, timedelta


# Make a DataFrame with the adjclose from each day for each stock
def query_prices(stocks, periods):
    """
    Parameters
    ----------
    stocks : list
        Tickers from stocks to analyze.
    periods : str
        DESCRIPTION.

    Returns
    -------
    DataFrame with daily adjusted prices of stocks parsed.
    """
    df = pd.DataFrame()

    for i, stock in enumerate(stocks):
        singular_stock = yq.Ticker(stock)
        df_singular = singular_stock.history(period=periods)['adjclose']
        df_singular = df_singular.reset_index()
        df_singular = df_singular.rename(columns = {'adjclose': stock})
        df_singular = df_singular.drop(columns = 'symbol')
        if i == 0:
            df = df_singular
        else:
            df = pd.merge(df, df_singular, on='date')

    return df


# Get stock historical data from some stocks
stocks = ['WEGE3.SA', 'ITUB3.SA', 'HGLG11.SA', 'ENBR3.SA']     # test
# period interesting for analysis: 1y, 2y, 5y, 10y, max(?)
periods = '10y'

df = query_prices(stocks, periods)
