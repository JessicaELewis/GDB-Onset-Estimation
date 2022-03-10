import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# from statsmodels.tsa.stattools import acf
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

import warnings


def jlcap_test_stationarity(timeseries):
    #Determing rolling statistics
    rolmean = timeseries.rolling(7).mean()
    rolstd = timeseries.rolling(7).std()
    #Plot rolling statistics:
    fig = plt.figure(figsize=(12, 8))
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')

    plt.axvline(pd.to_datetime('2021-05-01'), color='gray', label='med begin')
    
    plt.savefig('vis/stationarity.png', bbox_inches="tight")
    plt.show()
    
    # Dickey-Fuller test
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput) 
    
    

def jlcap_optimize_arima(y, ps, qs, d=1):
    warnings.filterwarnings("ignore")
    summary = []
    
    for p in ps:
        for q in qs:
            try:
                mod = ARIMA(y, order=(p, d, q))
                res = mod.fit()
                summary.append([(p, d, q), res.aic])
            except:
                summary.append([(p, d, q), None])
    
    summary_df = pd.DataFrame(summary)
    summary_df.columns = ['Order', 'AIC']
    summary_aic = summary_df[['Order', 'AIC']].sort_values('AIC').reset_index(drop=True)
    
    warnings.filterwarnings("default")
    
    return summary_aic[:3]