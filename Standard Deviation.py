import yfinance as yf
import matplotlib.pyplot as plt
import talib
import pandas as pd
import mplfinance as mpl
import statistics as st
from collections import Counter

# Data collection
data = yf.download("^GDAXI", period="1d", interval="1m")
# data = yf.download("^GSPC", period="1d", interval="1m")
# data = yf.download("^OMX", period="1d", interval="1m")
# data = yf.download("EURUSD=X", start="2018-12-07", end="2020-12-08", interval="1d")
#data = yf.download("^GSPC", start="2018-12-07", end="2020-12-14", interval="1d")
#data = yf.download("^GDAXI", start="2020-12-15", end="2020-12-16", interval="1m")


ema5 = talib.EMA(data['Close'], timeperiod=25)
ema10 = talib.EMA(data['Close'], timeperiod=10)
ma10 = talib.MA(data['Close'], timeperiod=10)
ema50 = talib.MA(data['Close'], timeperiod=10)
rsi = talib.RSI(data['Close'], timeperiod=14)
n = 0

shortDate = []
shortValue = []
longDate = []
longValue = []
closeLongDate = []
closeLongValue = []
closeShortDate = []
closeShortValue = []
barShort = []
barLong = []

# all open short, and long positions are stored in these arrays
openLong = []
openShort = []
mean = []

# win, lose, total trades & profit
win = 0
lose = 0
total = 0
profit = 0

meanData = 0
stData1 = []
stData2 = []
stData3 = []
stData4 = []
stData5 = []
stData6 = []
stData7 = []
stData8 = []
stData9 = []
stData10 = []

stopLong = 0
stopShort = 0
longStd = 0
shortStd = 0
openOrder = 0

res = []
sup = []

singularValue = []
singularDate = []

diff = []
vol = abs(data['Close'] - data['Open']).mean()
volstd = abs(data['Close'] - data['Open']).std()


st7Mean = []
vpoccounter = []
vpoc = []

dfc = data['Close'].value_counts()

# start algorithm
for row in rsi:
    # equilibrium price calculation
    meanData += float(data['Close'][n])
    vpoccounter.append(int(round(data['Close'][n])))
    vpoc.append(Counter(vpoccounter).most_common(1)[0][0])
    if n > 0:
        mean.append(meanData / (n + 1))
        diff.append(abs(data['Close'][n] - mean[n]))
        std = st.stdev(diff)
        # print(std)
        stData1.append(mean[n] - st.stdev(diff))
        stData2.append(mean[n] - 2 * st.stdev(diff))
        stData3.append(mean[n] - 3 * st.stdev(diff))
        stData4.append(mean[n] - 4 * st.stdev(diff))
        stData9.append(mean[n] - 5 * st.stdev(mean))
        stData5.append(mean[n] + st.stdev(diff))
        stData6.append(mean[n] + 2 * st.stdev(diff))
        stData7.append(mean[n] + 3 * st.stdev(diff))
        stData8.append(mean[n] + 4 * st.stdev(diff))
        stData10.append(mean[n] + 5 * st.stdev(mean))
    if n == 0:
        diff.append(0)
        stData1.append(meanData)
        stData2.append(meanData)
        stData3.append(meanData)
        stData4.append(meanData)
        stData5.append(meanData)
        stData6.append(meanData)
        stData7.append(meanData)
        stData8.append(meanData)
        stData9.append(meanData)
        stData10.append(meanData)
        print(meanData)
        mean.append(meanData)

    if n > 1:
        # if conditions are met opens short position
        if len(openShort) < 1:
            if data['Close'][n] - std > vpoc[n]:
                if data['Close'][n - 1] > stData7[n - 1] and data['Close'][n] < stData7[n]:
                    shortDate.append(ema10.index[n])
                    shortValue.append(data['Close'][n])
                    stopShort = stData8[n]

                    # remembers short position
                    openShort.append(data['Close'][n])

        # if conditions are met opens long position
        if len(openLong) < 1:
            if data['Close'][n] + std < vpoc[n]:
                if data['Close'][n - 1] < stData3[n - 1] and data['Close'][n] > stData3[n]:
                    longDate.append(ema10.index[n])
                    longValue.append(data['Close'][n])
                    stopLong = stData4[n]
                    # remembers long position
                    openLong.append(data['Close'][n])

        # checks if there is an open long position and if conditions are met closes it
        if len(openLong) > 0 and data['Close'][n] > mean[n] or len(openLong) > 0 and data['Close'][n] < stData3[n]:
            closeLongDate.append(ema10.index[n])
            closeLongValue.append(data['Close'][n])

            # subtract closing price from all open long positions stored in a list
            openLong = [data['Close'][n] - x for x in openLong]
            profit += sum(openLong)

            # total long trades, won long trades, lost long trades
            total += len(openLong)
            win += len([i for i in openLong if i >= 0])
            lose += len([i for i in openLong if i < 0])
            openLong = []

        # Checks if there is an open short position and if conditions are met closes it
        if len(openShort) > 0 and data['Close'][n] < mean[n] or len(openShort) > 0 and data['Close'][n] > stData7[n]:
            closeShortDate.append(ema10.index[n])
            closeShortValue.append(data['Close'][n])

            # subtract closing price from all open short positions stored in a list
            openShort = [x - data['Close'][n] for x in openShort]
            profit += sum(openShort)

            # total short trades, won short trades, lost short trades
            total += len(openShort)
            win += len([i for i in openShort if i >= 0])
            lose += len([i for i in openShort if i < 0])
            openShort = []

        # index incrementing
    print("Current profit (not including fees):", profit, "$")
    n += 1

    if n == len(ema10):
        print("Current open long trades:", len(openLong))
        print("Current open short trades:", len(openShort))
        if len(openLong) > 0:
            # mark long close on chart
            closeLongDate.append(ema10.index[n - 1])
            closeLongValue.append(data['Close'][n - 1])

            # subtract closing price from all open long positions stored in a list
            openLong = [data['Close'][n - 1] - x for x in openLong]
            profit += sum(openLong)

            # total long trades, won long trades, lost long trades
            total += len(openLong)
            win += len([i for i in openLong if i >= 0])
            lose += len([i for i in openLong if i < 0])
            openLong = []

        if len(openShort) > 0:
            # mark short close on chart
            closeShortDate.append(ema10.index[n - 1])
            closeShortValue.append(data['Close'][n - 1])

            # subtract closing price from all open short positions stored in a list
            openShort = [x - data['Close'][n - 1] for x in openShort]
            profit += sum(openShort)

            # total short trades, won short trades, lost short trades
            total += len(openShort)
            win += len([i for i in openShort if i >= 0])
            lose += len([i for i in openShort if i < 0])
            openShort = []

# print info
print("Profit/Loss (USD):", round(profit, 2) - 2 * total, "$")
print("Number of winning trades:", win)
print("Number of losing trades:", lose)
print("Number of executed trades:", total)
if total != 0:
    print("Hitrate:", round((win / total) * 100, 1), "%")

# turn mean into DataFrame
test0 = []
for i in range(len(data['Close'])):
    test0.append(i + 1)

dataM = {'Date': data['Close'], 'Mean': mean}
dataS = {'Date': data['Close'], 'Std1': stData1, 'Std5': stData5, 'Std2': stData2, 'Std6': stData6, 'Std3': stData3,
         'Std7': stData7, 'Std4': stData4, 'Std8': stData8}
dataV = {'Date': data['Close'], 'VPOC': vpoc}
dfMean = pd.DataFrame(data=dataM)
dfStD = pd.DataFrame(data=dataS)
dfVpoc = pd.DataFrame(data=dataV)
test = data['Close'].subtract(dfMean['Mean'])
test2 = test.pow(2)
test2 = test2.div(test0)
test2 = test2.add(data['Close'])
# test2 = test2.apply(numpy.sqrt)

stD = dfMean['Mean'].std()

# plot the graph
fig, axs = plt.subplots(2, gridspec_kw={'height_ratios': [3, 1]})
fig.suptitle('Screener')

# Dax Window
axs[0].plot(data['Close'], color="g")
axs[0].plot(data['Open'], color="b")
axs[0].plot(dfStD, linestyle=":")
axs[0].plot(ema50)
axs[0].plot(dfVpoc)
axs[0].axhline(data['Close'][0])

axs[0].plot(dfMean)
axs[0].set_title('OMX')
axs[0].legend()
axs[0].grid()
# axs[0].set_facecolor("#102A43")
axs[0].set_alpha(0.7)
axs[0].set_xlim([data['Close'].index[0], data['Close'].index[len(data['Close']) - 1]])

# short position markers
axs[0].plot(shortDate, shortValue, "rv")

# long position markers
axs[0].plot(longDate, longValue, "g^")
axs[0].plot(singularDate, singularValue, "mo")

# close long position
axs[0].plot(closeLongDate, closeLongValue, "gx")

# close short position
axs[0].plot(closeShortDate, closeShortValue, "rx")

# RSI
axs[1].plot(rsi)
axs[1].set_ylim([0, 100])
axs[1].set_xlim([data['Close'].index[0], data['Close'].index[len(data['Close']) - 1]])
# RSI Oversold, Overbought
axs[1].axhline(y=70, color='r', linestyle='dotted')
axs[1].axhline(y=30, color='r', linestyle='dotted')
plt.show()
