## Ninety Nine

This is a program which calculates the
[ninety-nine day high signal](http://boards.fool.com/Message.asp?mid=27442724),
described by mungofitch over at The Motley Fool investment message boards.

The basic premise is that when the S&P stops making new highs, investors
get pessimistic and stocks fall. When it starts making new highs again,
optimism takes over and bull markets stop. The ninety-nine day signal has 2
parts and coincidentally uses 99 days as the cut-off for both parts. It
looks at whether a new high has been made recently. It defines "high" as a
99 day high. It defines "recently" as 99 days. So, it looks for a new
99-day high within the last 99 days. The number is arbitrary. Hop over the
the Motley Fool boards to look how the dates have been tuned and pick
different ones, if you like.

I like this one, because it's simple, easy to calculate and doesn't have
many "signals", so you're not constantly buying and selling. It's, of
course, not perfect, but it would have gotten you out of most of the major
bear markets. 

### Required software

You need the ystockquote module from http://www.goldb.org/ystockquote.html

### How to use

Download the ystockquote module. Install it in the same directory as the
ninety-nine.py file (or somewhere on your python path). Then, run:

    $ python ninety-nine.py

    2010-06-07 1050.47 1219.8 1 16.1
    2010-06-08 1062.00 1219.8 1 14.9
    2010-06-09 1055.69 1219.8 1 15.5
    2010-06-10 1086.84 1219.8 1 12.2
    2010-06-11 1091.60 1219.8 1 11.7
    Current signal: Buy

Data is stored in a file called 99.pkl so that only new data is downloaded
each time you run the program.

Columns displayed are: 'Date', 'latest S&P level', '99 day high', 'Signal
(1=buy)', '% needed to rise to get new high'

### License

GPL

### Contact

vinod@kurup.com
 
