#!/usr/bin/env python
#
#  Copyright (c) 2009, Vinod Kurup (vinod@kurup.com)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#

try:
    import ystockquote
except ImportError:
    print "Please download the ystockquote module from http://www.goldb.org/ystockquote.html"
    raise

import operator
import datetime
import pickle

symbol = '^GSPC'
start_date = '20060701'
end_date = datetime.date.today().strftime('%Y%m%d')
lookback = 99 # 99-day-high

def float_sorter(item):
    """
    Key function so that we can sort by day's high (index 2) casted to a float.
    """
    return float(operator.itemgetter(2)(item))

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
    new_start_date = datetime.date(tmp[0],tmp[1],tmp[2]) + datetime.timedelta(1)
    start_date = new_start_date.strftime('%Y%m%d')

# Get quotes
if start_date >= end_date:
    quotes = []
else:
    quotes = ystockquote.get_historical_prices(symbol, start_date, end_date)
    # remove header row
    del quotes[0]
    # sort by date ascending (Field 0 is date, Field 2 is high, Field 4 is close)
    quotes.sort(key=operator.itemgetter(0))

if data:
    first = data["first"]
    rest = quotes
    newhigh_row = sorted(first, key=float_sorter).pop()
    high = newhigh = float(newhigh_row[2])
    signal = data["signal"]
else:
    # split into 2 groups
    first, rest = quotes[0:lookback], quotes[lookback:]
    # Find the max of the first group and initialize the signal
    newhigh_row = sorted(first, key=float_sorter).pop()
    high = float(newhigh_row[2])
    signal = 0

while rest:
    # delete first quote (earliest date)
    del first[0]

    # copy the first element of the 'rest' to our first list
    first.append(rest.pop(0))

    # recalculate signal
    newhigh_row = sorted(first, key=float_sorter).pop()
    newhigh = float(newhigh_row[2])
    if newhigh > high:
        signal = 1
    elif newhigh < high:
        signal = 0
    else:
        pass # signal doesn't change

    high = newhigh
    close = float(first[-1][4])
    pct_to_rise = round((newhigh - close) / close * 100, 1)
    print first[-1][0], first[-1][4], newhigh, signal, pct_to_rise

if signal:
    print "Current signal: Buy"
    date_of_newhigh = newhigh_row[0]
    index_of_newhigh = [x[0] for x in first].index(date_of_newhigh)
    print "New high will reset in " + str(lookback - (len(first) - index_of_newhigh)) + " days."
else:
    print "Current signal: Sell"
    close = float(first[-1][4])
    pct_to_rise = str(round((newhigh - close) / close * 100, 1))
    print "Market needs to rise " + pct_to_rise + "% before signal changes."

data = {'first': first, 'signal': signal}
output = open('99.pkl', 'w')
pickle.dump(data, output)
output.close()
