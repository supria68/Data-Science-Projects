"""
Filename: statistical_forecast.py
Author: Supriya Sudarshan
Version: 14.03.2021

Description: This script uses ARIMA model to forecast the foreign currency
(particularly Indian Rupee/ Euro) for the next 3 years.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from datetime import date 
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
#from helper import arima_research

def check_stationarity(series):
    rolmean = series.rolling(window = 365).mean()
    rolstd = series.rolling(window = 365).std()

    #Plot rolling statistics:
    plt.figure(figsize = (8,6))
    orig = plt.plot(ind_data['IndRupee/Euro'], color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

    # ADF test
    test_result = adfuller(series)

    print('\nTest Statistic: {}'.format(test_result[0]))
    print('P value: {}'.format(test_result[1]))
    print('Critical Values: {}'.format(test_result[4]))

    if test_result[1] > 0.05:
        print('\nSeries is not Stationary, accept NULL hypothesis')
    else:
        print('\nSeries is Stationary')

if __name__ == "__main__":
    # Loading the data
    data = pd.read_excel('Foreign_Exchange_Rates.xlsx')
    print('Dataset has {} rows and {} columns'.format(data.shape[0], data.shape[1]))
    print('List all columns of dataset: \n{}'.format(data.columns))

    # Data Cleaning
    data = data.rename(columns = {'Time Serie':'Date'})
    data.set_index('Date',inplace = True)
    data = data.replace('ND', np.nan)
    data = data.bfill().ffill() #handling missing values
    data = data.astype('float')
    data.index = pd.to_datetime(data.index) #change index to datetime format
    print('\nCheck for NUll values in the dataset:\n{}'.format(data.isna().sum()))

    val = ( date(2020, 1, 1) - date(2000 , 1, 3)) .days # check for any missing dates 
    print('\n{} dates are missing in the time series dataset'.format(val))
    fix_date = {} #fix all the missing dates
    fix_date['Date'] = pd.date_range("2000-01-03" , "2019-12-31" , freq = "D")
    df = pd.DataFrame(fix_date)
    df.set_index('Date', inplace = True)

    df = df.merge(data ,left_index = True , right_index = True , how = "left")
    df = df.bfill().ffill() # handle missing values!

    for dtype in df.dtypes:
        df = df.astype('float') #convert all columns dtype to float

    print("\nMaximum exchange rate for respective currencies :\n" , df.max())
    print("\n\n Minimum exchange rate for respective currencies : \n" ,df.min())

    # Data Visualization
    countries_names = df.columns    # taking all the countries - currencies  name 
    countries_names= countries_names.str.wrap(3) 
    plotting_point = data.iloc[(len(data)-1)]
    plt.figure(figsize = (15,5))
    plt.scatter(countries_names , plotting_point)
    plt.title("Foreign Exchange rates until 2019-12-31")
    plt.show()

    # Feature Engineering
    ind_data = pd.DataFrame(df['INDIA - INDIAN RUPEE/US$'], index = df.index)
    ind_data['IndRupee/Euro'] = ind_data['INDIA - INDIAN RUPEE/US$'] / df['EURO AREA - EURO/US$']
    ind_data.columns = ['IndRupee/Dollar', 'IndRupee/Euro'] # Indian Rupee to Euro and US Dollar

    fig, [ax1,ax2] = plt.subplots(1, 2, figsize = (20,6))
    ind_data['IndRupee/Euro'].plot(ax = ax1)
    ind_data['IndRupee/Dollar'].plot(ax = ax2)
    ax1.set_title('Indian Rupee / Euro')
    ax2.set_title('Indian Rupee/ Dollar')

    data_2019 = ind_data['2019'] # Let's see the variation by month for the year 2019
    data_2019.plot(subplots = True, figsize = (8,6)) 
    plt.title('Indian Rupee/Euro variations for the year 2019')
    plt.show()

    # Test for Stationarity
    print('\nCheck for stationarity of the time series')
    check_stationarity(ind_data['IndRupee/Euro'])
    print('Time series has a increasing trend for the mean.')

    ind_data['half_yr_shift'] = ind_data['IndRupee/Euro'] - ind_data['IndRupee/Euro'].shift(180) #shift by half-year
    print('\nTry to make the series weakly stationary by means of shift() or diff() or applying log transformations')
    check_stationarity(ind_data['half_yr_shift'].dropna())
    print('Time series is weakly stationary after a half year shift!')
    
    fig, [ax1,ax2] = plt.subplots(2,1, figsize = (12,8))
    plot_acf(ind_data['half_yr_shift'].dropna(), lags = 180, ax = ax1);
    plot_pacf(ind_data['half_yr_shift'].dropna(), lags = 40, ax = ax2);
    plt.show()
    print('\nFrom the plots acf and pacf, p = 5 and q = 1. Lets fit the ARIMA model')

    # ARIMA with p=5,d=1,q=1
    model = ARIMA(ind_data['IndRupee/Euro'],order=(5,1,1)).fit()
    print(model.summary())
    print("\nLet's check if the fitted ARIMA model is good enough to forecast using Ljung-Box test") 
    ljung_box, p_value = acorr_ljungbox(model.resid)
    print(f'Ljung-Box test: {ljung_box[:10]}')
    print(f'p-value: {p_value[:10]}')
    plot_pacf(model.resid);
    plot_acf(model.resid);
    plt.show()
    print('\np-values are > 0.05, hence we accept NULL hypothesis! i.e., residuals are not correlated. Since plots resemble that of a white noise, model is good enough to use for forecasting!')

    # Forecasting for next 3 years
    future_date = pd.date_range(start = ind_data.index[-1], periods = 1095)
    pred_df = pd.DataFrame(index = future_date[:], columns = ind_data.columns)
    predictions = model.forecast(steps = 1095) # next 3 yrs
    pred_df['predictions'] = predictions[0]
    lower = pd.Series(predictions[2][:, 0], index = pred_df.index)
    upper = pd.Series(predictions[2][:, 1], index = pred_df.index)

    plt.figure(figsize = (10,10))
    plt.plot(ind_data['IndRupee/Euro'], label = 'Original')
    plt.plot(pred_df['predictions'], color = 'darkgreen', label = 'Predictions')
    plt.fill_between(pred_df.index,lower, upper, color = 'gray', alpha = 0.2, label = 'Confidence interval')
    plt.legend(loc = 0)
    plt.title('Forecasting Forex (Indian Rupee/Euros) rates for the next 3 years')
    plt.show()



