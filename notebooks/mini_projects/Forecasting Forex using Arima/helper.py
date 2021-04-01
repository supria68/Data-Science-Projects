"""
Filename: helper.py
Author: Supriya Sudarshan
Version: 20.03.2021

Description: This script consists of functions to 
            -check for time series stationarity 
            -plot pacf and acf for finding p,q values
            -evaluating predictions from arima model
            -diagostic testing with ljungbox

"""
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn import metrics


def check_stationarity(original, series, title):
    """
    ADF test for checking the stationarity of time series.
    """
    rolmean = series.rolling(window = 365).mean()
    rolstd = series.rolling(window = 365).std()

    #Plot rolling statistics:
    plt.figure(figsize = (8,6))
    orig = plt.plot(original, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title(title)
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

def plot_acf_pacf(series, lag_pacf, lag_acf):
    """
    Plot acf and pacf to get the p,q values for arima model
    """
    fig, [ax1,ax2] = plt.subplots(2,1, figsize = (12,8))
    plot_acf(series, lags = lag_acf, ax = ax1);
    plot_pacf(series, lags = lag_pacf, ax = ax2);
    plt.show()
    
def fit_arima_model(series, p, d, q):
    """
    for the given p,d,q; fit arima model on the split(80-20) dataset and
    evaluate predictions using mean square error!
    """
    
    X = series.values
    size = int(len(X) * 0.8)
    train, test = X[:size], X[size:]
    history = [x for x in train]
    predictions = list()

    # fit the model and make predictions
    for t in range(len(test)):
        model = ARIMA(history, order=(p,d,q))
        model_fit = model.fit(disp=0)
        #print(model_fit.summary())
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        err = abs(yhat - obs)
        print("Predicted: %.3f, Expected: %.3f, Error: %.3f" % (yhat, obs, err))

    # print summary and graph results
    error = metrics.mean_squared_error(test, predictions)
    print("Mean Square Error: %.3f" % (error))
    plt.plot(test, label='actual rates')
    plt.plot(predictions, label='predicted rates')
    plt.title('Arima model for predicting the exchange rates')
    plt.legend()
    plt.show()

def ljungbox_test(model):
    """
    Check if the fitted model is good enough for forecasting
    """
    ljung_box, p_value = acorr_ljungbox(model)
    print(f'Ljung-Box test: {ljung_box[:10]}')
    print(f'p-value: {p_value[:10]}')
    plot_pacf(model);
    plot_acf(model);
    plt.show()
