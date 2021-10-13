import yfinance as yf
import matplotlib.pyplot as plt
import talib as ta

# get data from yahoo finance API
data = yf.download("^GDAXI", period="1d", interval="1m")

# use TA-lib to calculate the RSI of the data
rsi = ta.RSI(data['Close'], timeperiod=14)

# lists used to store open positions
openLong = []
openShort = []

# lists used to store markers for graphic position open as close
shortDate = []
shortValue = []
longDate = []
longValue = []
closeLongDate = []
closeLongValue = []
closeShortDate = []
closeShortValue = []

# variables for printable data, like profit, win/loss and total amount of trades
total = 0
profit = 0
win = 0
lose = 0

# index variable
n = 0

# start for loop to test strategy
for val in rsi:
    # if conditions are met open long position
    if val < 30:
        # stores price points and index to mark on graph
        longValue.append(data['Close'][n])
        longDate.append(data['Close'].index[n])

        # remembers the long positions
        openLong.append(data['Close'][n])
    # if conditions are met open short position
    if val > 70:
        # stores price points and index to mark on graph
        shortValue.append(data['Close'][n])
        shortDate.append(data['Close'].index[n])

        # remembers the short positions
        openShort.append(data['Close'][n])

    # if conditions are met closes open long position
    if len(openLong) > 0 and val >= 55:
        closeLongDate.append(data['Close'].index[n])
        closeLongValue.append(data['Close'][n])

        # subtract closing price from all open long positions stored in a list
        openLong = [data['Close'][n] - x for x in openLong]
        profit += sum(openLong)

        # total long trades, won long trades, lost long trades
        total += len(openLong)
        win += len([i for i in openLong if i >= 0])
        lose += len([i for i in openLong if i < 0])

        # empties list of open positions since they are now closed
        openLong = []

    if len(openShort) > 0 and val <= 45:
        closeShortDate.append(data['Close'].index[n])
        closeShortValue.append(data['Close'][n])

        # subtract closing price from all open short positions stored in a list
        openShort = [x - data['Close'][n] for x in openShort]
        profit += sum(openShort)

        # total short trades, won short trades, lost short trades
        total += len(openShort)
        win += len([i for i in openShort if i >= 0])
        lose += len([i for i in openShort if i < 0])

        # empties list of open positions since they are now closed
        openShort = []

    # index incrementing
    n += 1

# print return from test

print("Total amount of orders executed:", total)
print("Number of winning trades", win)
print("Number of losing trades", lose)
if total != 0:
    print("Hitrate:", (win/total)*100, "%")
print("Profit:", profit, "$")

# plot graph and markers

# plot the graph
fig, axs = plt.subplots(2, gridspec_kw={'height_ratios': [3, 1]})
fig.suptitle('Screener')

# Main graph window
axs[0].plot(data['Close'], color="g")
axs[0].grid()
axs[0].set_xlim([data['Close'].index[0], data['Close'].index[len(data['Close']) - 1]])

# short position markers
axs[0].plot(shortDate, shortValue, "rv")

# long position markers
axs[0].plot(longDate, longValue, "g^")

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
