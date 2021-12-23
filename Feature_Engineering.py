#!/usr/bin/python


def residual(Y,X):
    '''
    Function to Calculate Residual using Linear Regression
    
    ================Arguments===============
    Y- Response Variable
    X- Dependent Variable
    
    ================Return==================
    res- Residual
    '''

    ##Getting better results without intercept
    clf = StandardScaler()
    Y = clf.fit_transform(np.array(Y).reshape(-1,1))
    X = clf.fit_transform(np.array(X).reshape(-1,1))
    model = sm.OLS(Y,X)
    clf = model.fit()
    beta = clf.params[0]
    res = Y - X * beta
    return res





def feature_engineering(data):
    
    '''
    Function to create time series features in dataset
    
    '''
    
    ###https://github.com/bukosabino/ta
    
    
    #Momentum
    #1) RSI
    data['EQ_1_rsi'] = ta.momentum.rsi(data['EQ_1_close'],window=14,fillna=False)
    data['EQ_2_rsi'] = ta.momentum.rsi(data['EQ_2_close'],window=14,fillna=False)
    
    #2) SRSI
    data['EQ_1_srsi'] = ta.momentum.stochrsi(data['EQ_1_close'],window=14,fillna=False)
    data['EQ_2_srsi'] = ta.momentum.stochrsi(data['EQ_2_close'],window=14,fillna=False)
    
    #Volume Indicator
    
    #3) MFI
    data['EQ_1_mfi'] = ta.volume.money_flow_index(data['EQ_1_high'],data['EQ_1_low'],data['EQ_1_close'],data['EQ_1_vol'],window=14)
    data['EQ_2_mfi'] = ta.volume.money_flow_index(data['EQ_1_high'],data['EQ_1_low'],data['EQ_1_close'],data['EQ_2_vol'],window=14)
    
#     #4) ADL
#     data['EQ_1_adl'] = ta.volume.acc_dist_index(data['EQ_1_high'],data['EQ_1_low'],data['EQ_1_close'],data['EQ_1_vol'])
#     data['EQ_2_adl'] = ta.volume.acc_dist_index(data['EQ_2_high'],data['EQ_2_low'],data['EQ_2_close'],data['EQ_2_vol'])
    
    #Volatility
    
    #ATR
    data['EQ_1_atr']  = ta.volatility.average_true_range(data['EQ_1_high'],data['EQ_1_low'],data['EQ_1_close'],window=14)
    data['EQ_2_atr']  = ta.volatility.average_true_range(data['EQ_2_high'],data['EQ_2_low'],data['EQ_2_close'],window=14)
    
    #Bollinger Bands
    data['EQ_1_bb'] = ta.volatility.bollinger_mavg(data['EQ_1_close'],window=20)
    data['EQ_2_bb'] = ta.volatility.bollinger_mavg(data['EQ_2_close'], window=20)
    
    #Trend Indicator
    
    #EMA
    data['EQ_1_ema'] = ta.trend.ema_indicator(data['EQ_1_close'], window=14)
    data['EQ_2_ema'] = ta.trend.ema_indicator(data['EQ_1_close'], window=14)
    
    #MACD
    data['EQ_1_macd'] = ta.trend.macd(data['EQ_1_close'], window_fast=12, window_slow=26)
    data['EQ_2_macd'] = ta.trend.macd(data['EQ_2_close'], window_fast=12, window_slow=26)
    
    #Others
    
    #Daily log return
    data['EQ_1_dlr'] = ta.others.daily_log_return(data['EQ_1_close'])
    data['EQ_2_dlr'] = ta.others.daily_log_return(data['EQ_2_close'])
    
    ##Residual
    data['Res_open'] = residual(data['EQ_2_open'],data['EQ_1_open'])
    
    data['Res_close'] = residual(data['EQ_2_close'],data['EQ_1_close'])
    
    data['Res_high'] = residual(data['EQ_2_high'],data['EQ_1_high'])
    
    data['Res_low'] = residual(data['EQ_2_low'],data['EQ_1_low'])
    
    data = data.dropna()## Dropping NAN rows
    data = data.reset_index(drop=True)

    return data


    
    
def response_variable(df,window =1):
    '''
    Function to create Response Variable for prediction
    
    ====Argument====
    df     : Data-set on which predicition is to be done
    window : Period in future for which prediction is to be done
    
    ====Return======
    data_Y: size =(len(df) - window) 5 days in future prediction list
    '''
    data_Y = []
    for i in range(len(df)-window):
        data_Y.append(float(df[i+window:i+1+window]))
    return data_Y
