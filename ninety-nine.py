#!/usr/bin/env python
#
#  Copyright (c) 2009, Vinod Kurup (vinod@kurup.com)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#

from alpha_vantage.timeseries import TimeSeries

import operator
import os
import datetime
import pickle

ALPHA_VANTAGE_API_KEY = os.environ['ALPHA_VANTAGE_API_KEY']

HIGH_KEY = '2. high'
CLOSE_KEY = '4. close'

symbol = 'SPY'
start_date = datetime.date(2016, 7, 1)
end_date = datetime.date.today()
lookback = 99 # 99-day-high

def float_sorter(item):
    """
    Key function so that we can sort by day's high casted to a float.
    """
    return float(operator.itemgetter(1)(item)[HIGH_KEY])

# Load the input file, if available
try:
    input = open('99.pkl', 'r')
    data = pickle.load(input)
    input.close()
except IOError:
    print "Input file not found, proceeding from scratch"
    data = None

if data:
    # make the date after last date in our input the new start_date
    old_end_date = data["first"][-1][0]
    tmp = [int(c) for c in old_end_date.split('-')]
    start_date = datetime.date(tmp[0], tmp[1], tmp[2]) + datetime.timedelta(1)

# Get quotes
if start_date >= end_date:
    quotes = []
else:
    ts = TimeSeries(ALPHA_VANTAGE_API_KEY)
    if end_date - start_date > datetime.timedelta(100):
        outputsize = 'full'
    else:
        outputsize = 'compact'
    quotes, metadata = ts.get_daily(symbol, outputsize=outputsize)
    quotes = sorted(quotes.items())


if data:
    first = data["first"]
    rest = quotes
    newhigh_row = sorted(first, key=float_sorter).pop()
    high = newhigh = float(newhigh_row[1][HIGH_KEY])
    signal = data["signal"]
else:
    # split into 2 groups
    first, rest = quotes[0:lookback], quotes[lookback:]
    # Find the max of the first group and initialize the signal
    newhigh_row = sorted(first, key=float_sorter).pop()
    high = float(newhigh_row[1][HIGH_KEY])
    signal = 0

while rest:
    # delete first quote (earliest date)
    del first[0]

    # copy the first element of the 'rest' to our first list
    first.append(rest.pop(0))
    # recalculate signal
    newhigh_row = sorted(first, key=float_sorter).pop()
    newhigh = float(newhigh_row[1][HIGH_KEY])
    if newhigh > high:
        signal = 1
    elif newhigh < high:
        signal = 0
    else:
        pass  # signal doesn't change

    high = newhigh
    close = float(first[-1][1][CLOSE_KEY])
    pct_to_rise = round((newhigh - close) / close * 100, 1)
    print first[-1][0], close, newhigh, signal, pct_to_rise

if signal:
    print "Current signal: Buy"
    date_of_newhigh = newhigh_row[0]
    index_of_newhigh = [x[0] for x in first].index(date_of_newhigh)
    print "New high will reset in " + str(lookback - (len(first) - index_of_newhigh)) + " days."
else:
    print "Current signal: Sell"
    close = float(first[-1][1][CLOSE_KEY])
    pct_to_rise = str(round((newhigh - close) / close * 100, 1))
    print "Market needs to rise " + pct_to_rise + "% before signal changes."

data = {'first': first, 'signal': signal}
output = open('99.pkl', 'w')
pickle.dump(data, output)
output.close()
