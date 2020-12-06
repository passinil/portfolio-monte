# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 22:45:55 2020

@author: lucas
"""
# Imports
import pandas as pd
import numpy as np
import yahooquery as yq

# Make a DataFrame with the adjclose from each day for each stock
def query_prices(stocks, periods):
    """
    stocks : list
        Tickers from stocks to analyze.
    periods : str
        period interesting for analysis: 1y, 2y, 5y, 10y, max
    Returns
    DataFrame with daily adjusted prices of stocks parsed.
    """
    df = pd.DataFrame()
    stocks.insert(0, '^BVSP')     # market benchmark index
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
    stock_prices = df.set_index('date')

    return stock_prices


def normalize(stock_prices):
    # Normalize df so all prices start at R$ 1
    return (stock_prices/stock_prices.iloc[0]*1)


def daily_returns(stock_prices):
    # Get daily returns in % from stocks in df
    df_dr = stock_prices.copy()
    for stock in stock_prices.columns:
        for day in range(1, len(stock_prices)):
            df_dr[stock][day] = ((stock_prices[stock][day] -
                                  stock_prices[stock][day-1]) /
                                  stock_prices[stock][day-1])*100
        df_dr[stock][0] = 0

    return df_dr


def calculate_betas(daily_rets):
    # Use daily returns to get beta between Bovespa and each stock
    return daily_rets.corr()['^BVSP'][1:]


def calculate_capm(rf, betas, daily_rets):
    # capital asset pricing model
    # risk free asset rf, e.g. selic, 10y bond US rates
    # betas
    # return market rm, return from bovespa calculated through daily_rets
    # return expected re, from stock accounting above vars
    rm = daily_rets['^BVSP'].mean() * 250   # ~ 250 days of open market
    # multiplying like that is not the ideal, but the result is pretty much the same
    re = rf + betas * (rm - rf)

    return re



# Get stock historical data from some stocks
stocks = ['WEGE3.SA', 'ITUB3.SA', 'ENBR3.SA', 'RAPT4.SA', 'ITSA4.SA']
# period interesting for analysis: 1y, 2y, 5y, 10y, max(?)
periods = '10y'
# risk free asset (rf) set to actual SELIC but maybe better average whole 9yrs
rf = 0.0914      # 9.14 % anual average return CDI


stock_prices = query_prices(stocks, periods)
normalized_prices = normalize(stock_prices)
df_dr = daily_returns(normalized_prices)
stocks_betas = calculate_betas(df_dr)
stocks_capm = calculate_capm(rf, stocks_betas, df_dr)



