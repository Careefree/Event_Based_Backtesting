# Event_Based_Backtesting
Backtest three diffrent trading strategies SMA Cross, Momentum, and Mean reversion strategies.  

There are then two other strategies that can be used to execute trades are long only & long-short. This program contains a base file know as backtest_base.py which
will retrive and prepare data, helper/convenience functions, place orders, and close out trades. Both the long only & long-short classes inherant from backtest_base.py
Operation is simple choose to run backtest_long_only.py or backtest_long_short.py and performance information will be printed in the terminal.

* Note if using Bitstamp data the price action is too volitaile and dosent work well for this strategy please update backtest_base.py with the AUDUSD=X.csv to see
a better representation of this particular strategy 
