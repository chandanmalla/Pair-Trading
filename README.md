# Pair-Trading
##### _About_ (Source: Wiki)
A pairs trade or pair trading is a market neutral trading strategy enabling traders to profit from virtually any market conditions: uptrend, downtrend, or sideways movement. The strategy monitors performance of two historically correlated securities. When the correlation between the two securities temporarily weakens, i.e. one stock moves up while the other moves down, the pairs trade would be to short the outperforming stock and to long the underperforming one, betting that the "spread" between the two would eventually converge. The divergence within a pair can be caused by temporary supply/demand changes, large buy/sell orders for one security, reaction for important news about one of the companies, and so on.

## 1) Data Collection

Step 1:
Ticker list of Indian Stock Market was collected from: https://docs.google.com/spreadsheets/d/1ymMHn4gE9Gjjtvw3bGVlD_9CbdfDm01_cLBRd5nRN_M/edit?usp=sharing

Step 2:
Delisted Tickers were Deleted, as were Tickers whose data was only partially available at Yahoo.

Step 3:
Remaining Tickers Data was collected from Yahoo using ```yfinance``` library from 2008 to 2021
```
def download_data(symbol, source, start_date, end_date):
    start = datetime.strptime(start_date, '%d-%m-%Y')
    end = datetime.strptime(end_date, '%d-%m-%Y')
    df = pdr.get_data_yahoo(symbol, data_source=source, start=start, end=end)
    return df
```
Step 4:
Only Closing Price Data was kept for each ticker for prediction

## 2) Data Pre-Processing
Step 1:
Use PCA to reduce the dimensions of Data of each ticker

Step 2:
Use DBScan to Cluster stocks similar to each other

Step 3:
Use T-Sne to visualize if Clustering done makes any sense or not

Step 4:
Because tickers within the same cluster would be related to each other, the cointegration test will be used to determine which are the best pairs among them.


![alt text](https://i.imgur.com/6Aj3cKg.png)

![alt text](https://i.imgur.com/9X4BxT4.png)

## 3) Cointegration Test

Step 1:
Get the residuals on each ticker that is part of the same cluster.

Step2:
Perform the test 

Step 3:
Get the top Best pairs in each cluster for Pair Trading

## 4) Feature Engineering

**Features Developed:**

- Leading Indicators: They inform about the future trend in time series
- Lagging Indicators: They are used to confirm the leading indicators

1. RSI - Relative Strength Index:
[Calculation Example](https://i.imgur.com/2fnvS7K.png)
    - It is leading **momentum** indicator which helps in identifying trend reversal of time series
    - It oscillates b/w 0 and 100.
    - Formula
         - RSI = 100 -  100/(1 + RS)
        - RS = Average points Gain over a fixed period by stock(at least 14 days) / Average points loss over a fixed period by stock(at least 14 days)
 
    - When 0<=RSI <=20, Stock is supposed to be oversold and ready for a upward correction(buying will start)
    - When 80<=RSI<=100, Stock is supposed to be overbought and ready for downward correction(selling will start)

2. Stochastic RSI:
[Calculation Example](https://i.imgur.com/BJvUSiB.png)
[Reference](https://www.investopedia.com/terms/s/stochrsi.asp#:~:text=The%20Stochastic%20RSI%20(StochRSI)%20is,than%20to%20standard%20price%20data.)
     - It is a leading **momentum** indicator based on RSI
    - In Practice RSI is a slow moving indicator, to fix the slowness Stochastic RSI moves rapidly from overbought to oversold.
     - Formula
        - t' StochRSI = (t'-period RSI - Lowest Low RSI in t' period) / (Highest High RSI in t'period - Lowest Low RSI in t' period)

    - 0 <= Stochastic-RSI <= 1
    - A StochRSI reading above 0.8 is considered overbought, while a reading below 0.2 is considered oversold
    - Overbought doesn't necessarily mean the price will reverse lower, just like oversold doesn't mean the price will reverse higher. Rather the overbought and oversold conditions simply alert traders that the RSI is near the extremes of its recent readings.
    - When the StochRSI is above 0.50, the security may be seen as trending higher and vice versa when it's below 0.50.


3. Money Flow Index:
[Calculation Example](https://i.imgur.com/tgNhIoA.png)
    - It is leading **volume** based indicator and it does the same job as RSI
    - While RSI consider the price, MFI considers both price and Volume
    - It is also called weighted Volume RSI
    - It oscillates b/w 0 and 100
    - Formula
        - MFI = 100 - 100/(1+ MFR)
        - MFR(Money flow Ratio) = t-Period Positive Money flow / t-Period Negative Money Flow, where t = 14 typically
        - Money Flow = Typical Price * Volume traded on that day
        - Typical Price = (High + Low + Close) / 3
 
    - When 0<=MFI<=20, Stock is supposed to be oversold and ready for a upward correction(buying will start)
    - When 80<=MFI<=100, Stock is supposed to be overbought and ready for downward correction(selling will start)
4. Accumulation/Distribution Index/Indicator
[Calculation Example](https://i.imgur.com/8fZJYGy.png)
    - It is a **cumulative** indicator and uses **Volume** and Price both to identify whether a Stock is being Accumulated(bought) or Distributed(Sold)
    - Or it can be said it identifies the cumulative flow of money into and out of stock and helps in identifying trend reversal
    - If ADL line is going downward but stock is going up, then it is a indicator of downward correction,as it is possible someone sold lots of volume of stocks and vice - versa
    - Formula
        - Money Flow Multiplier = [(Close  -  Low) - (High - Close)] /(High - Low) 
        - 0<=MFM<=1 is +ve when Close = Upper half of candle stick chart ( When it is in upper half it is an indicator of **buying pressure > selling pressure**)
        - 0<=MFM<=1 is -ve when Close = Lower half of candle stick chart( When it is in lower half it is an indicator of **buying pressure < selling pressure**)
        - Money Flow Volume = Money Flow Multiplier x Volume for the Period
        - ADL = Previous ADL + Current Period's Money Flow Volume
    - Whether ADL indicator goes upwards or downwards depends on sign of MF

5. Average True Range
[Calculation Example](https://i.imgur.com/T0kfVoJ.png) ,
[Reference](https://school.stockcharts.com/doku.php?id=technical_indicators:average_true_range_atr)
    - The average true range is a price **volatility** indicator showing the average price variation of assets    within a given time period. 
    - It is generally calculated on 14 day periods of True Range
    - Formula
        - ATR = (13 x Previous Day ATR + Current TR ) / 14
        - TR = MAX( ( Today_High - Today_low) , ABS(Today_High - Previous_Close) , ABS( Today_Low -    Previous_Close) )
    - True range takes the gap b/w price from current from previous day to identify the movement of price
    - ATR only measures the volatility, it does not measure direction of price movement
    - Higher the ATR value, higher is the volatility and vice versa
 

6. Bollinder Bands
[Calculation Example](https://i.imgur.com/MPobbmQ.png)
    - Bollinger Bands are envelopes plotted at a standard deviation level above and below a simple moving average    of the price. Because the distance of the bands is based on standard deviation
    - When the bands tighten during a period of low volatility, it raises the likelihood of a sharp price move in    either direction.
    - When the bands separate by an unusual large amount, volatility increases and any existing trend may be    ending.
    - Formula:
        - Middle Band = 20-day simple moving average (SMA)
        - Upper Band = 20-day SMA + (20-day standard deviation of price x 2) 
        - Lower Band = 20-day SMA - (20-day standard deviation of price x 2)
    [Band Example](https://i.imgur.com/HJkiO1B.png)
 

7. Exponential Moving Average
    [Calculation Example](https://i.imgur.com/BZEQgOG.png)
    - They are lagging indicator confirming the trend
    - more weightage is given to recent prices while taking average
    - Formula
    
        - Initial EMA: 10-period sum / 10
        - Multiplier: (2 / (Time periods + 1) ) = (2 / (10 + 1) ) = 0.1818 (18.18%)
        - EMA: {Close - EMA(previous day)} x multiplier + EMA(previous day). 
8. Moving Average Convergence Divergence Indicator
    - As the name suggests, MACD is all about the convergence and divergence of the two moving averages. Convergence occurs when the two moving averages move towards each other, and divergence occurs when the moving averages move away.
    - Formula
        - MACD = 12 day EMA - 26 day EMA(Exponential Moving average)
    - The sign associated with the MACD just indicates the direction of the stock’s move. '+' for upward move and '-' for downward move.
        - positive sign is only possible if 12 day EMA> 26 day EMA and if that is the case then as we know EMA depends more on recent values, so price must be trending in upward direction.
    - Magnitude of MACD signifies the strength of upward and downward trend.
    [MACD line GRAPH](https://www.notion.so/Case-Study-1-a0d7bc10144845da932368fee4fd2f9f#0d1b9cfd663640e59a42d62fc3a2ce15)
    - When the MACD Line crosses the centerline from the negative territory to positive territory, it means there    is a divergence between the two averages. This is a sign of increasing bullish momentum; therefore, one should    look at buying opportunities and vice versa
 
9. Log Return
    - Formula
     - Log(current_price / previous_price)
10. Residual/Spread
    - We will use linear regression to fit both Stocks and calculate the resdual and use it as a feature here.
    - As this pair passed through cointegration test, residual should come as stationery 
11. Y_Pred
    - Price of next day is set as Y_Pred
12. FFT:
    - All Feature Engineered Data (except Test Data and Y_pred) was smoothen out using Fast Fourier Transform.

## 5) Pair Trading using ARIMA
Step 1:
Get the Residuals/Spread for best Pairs from cointegration test

Step 2:
Model the next day Residual/Spread using ARIMA

[Reference_1](https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/#:~:text=ARIMA%2C%20short%20for%20'Auto%20Regressive,used%20to%20forecast%20future%20values.)
[Reference_2](https://www.youtube.com/watch?v=zMWeOBBa24Y)
- Arima uses its own lags and the lagged forecast errors to predict future values in time series
- ARIMA is divided in  parts, Auto Regression, Integrated, Moving Average.
- **Auto Regression**
    -  it is a linear regression model that uses its own lags as predictor
    -  a Linear regression model should be free of correlation.
![image.png](https://i.imgur.com/3zPfLDe.png)

- **Integrated**
    - To remove correlation or to make the time series stationary in lagged time series, difference of current value from previous value is performed, it is to be done multiple times if required
- **Moving Average**
    - It is a linear regression model that uses lagged forecast errors from *Auto Regression* to forecast errors
![image-2.png](https://i.imgur.com/9jo3Zl6.png)

ARIMA Equation:
![image-3.png](https://i.imgur.com/4oFLI8Y.png)

- Only Hyperparameters in ARIMA is the number of lag to be used in *Auto Regression*, *Moving Average* and number of times the *differencing*(Integrated) is to be performed
- Number of lags in Auto Regression can be found by studying *partial auto correlation plot*
- Number of lags in Moving Average and Differences required can be identified using *auto correlation plot* and *ADF test* to determine whether it is stationary or not

**ARIMA Result:**


![image.png](https://i.imgur.com/G19Egk4.png)

## 6) Pair Trading using Machine Learning

For prediction in ARIMA, just residual data of pairs was necessary, however in this section, we will use every feature produced in the feature engineering section.

**Part 1: Using Random Forest**
![image.png](https://i.imgur.com/T2WqcE7.png)

**Part 2: Using Elastic Regression**
![image.png](https://i.imgur.com/vb6STP3.png)

## 7) Trading Strategy

Step 1:
Calculate Z-Score using mu=60 day moving average of residual, sigma = 60 day standard deviation of residual and x = current day residual

Step 2:
Generate Sell and Buy signals using Z-score calculated in Step-1 for the pairs
![image.png](https://i.imgur.com/uhY6Ftd.png)

Step 3:
Create a trading method which triggers sell and buy whenever the signal is observed.
```
def trade(EQ_1, EQ_2, Residual,test_data_len ,share_multiplier,window=60):
    ratios_mavg = Residual.rolling(window=window,
                               center=False).mean()[-test_data_len-1:][0:test_data_len] ##Taking 60 day mean initially from train data and then add each day of test data to it

    std = Residual.rolling(window=window,
                        center=False).std()[-test_data_len-1:][0:test_data_len] ##Taking 60 day mean initially from train data and then add each day of test data to it
    x = Residual[-test_data_len:].reset_index(drop=True)
    mu = ratios_mavg60.reset_index(drop=True)
    sigma = std_60.reset_index(drop=True)
    z_score = (x - mu)/sigma
    z_score = z_score.reset_index(drop=True)
    EQ_1 = EQ_1.reset_index(drop=True)
    EQ_2 = EQ_2.reset_index(drop=True)
    money = 0
    countEQ1 = 0
    countEQ2 = 0

    eq1bought = 0
    eq1sold = 0 

    eq2bought = 0
    eq2sold = 0
    for i in range(test_data_len):
        # Sell short 
        if z_score[i] > 1:

            money += share_multiplier*(EQ_2[i]* x[i] - EQ_1[i]  )
            countEQ2 -= x[i]*share_multiplier
            countEQ1 += 1*share_multiplier
            
#             print('Buy EQ1:',money,EQ_1[i],x[i])
#             print('Sell EQ2:',money,countEQ2)
#             print('\n')
        
        elif z_score[i] < -1:
            
            money+=  share_multiplier*(EQ_1[i] - EQ_2[i]* x[i])           
            countEQ2 += x[i]*share_multiplier
            countEQ1 -= 1*share_multiplier
            
#             print('Sell EQ1:',EQ_1[i] * x[i],EQ_1[i],x[i])
#             print('Buy EQ2:',EQ_2[i],countEQ2)
#             print('Money',money)
#             print('\n')
        
        elif abs(z_score[i]) < 0.5:
            money += countEQ2 * EQ_2[i] + EQ_1[i] * countEQ1
            countEQ1 = 0
            countEQ2 = 0
    return money

```

## 8) Results:
While Random Forest and Elastic Regression produced similar results but both produced superior Results to ARIMA

```
Profit at  Predicted Price of next day using ARIMA: 		 6337.889865173798
Profit at Predicted Price of next day using LR:  11304.181844212108
Profit at Predicted Price of next day using RF:  12496.581864440399

```
