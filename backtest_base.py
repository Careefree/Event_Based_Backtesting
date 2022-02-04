"""Base class for event based backtesting."""


import numpy as np
import pandas as pd
from pylab import mpl, plt
plt.style.use("seaborn")
mpl.rcParams["font.family"] = "serif"


class BacktestBase():
    """Base class for event based backtesting."""

    """
    Attributes
    ==========
    start: str
        start date for data selection
    end: str
        end date for data selection
    amount: int, float
        amount to be invested at the beginning
    ftc: float
        fixed transaction costs per trade (buy or sell)
    ptc: float
        proportional transaction costs per trade (buy or sell)

    Methods
    =======
    get_data:
        retrieves and prepares the base data set
    plot_data:
        plots the closing price for the symbol
    get_data_price:
        returns the date and price for the given bar
    print_balance:
        prints out the current (cash) balance
    print_net_worth:
        prints current net worth
    place_buy_order:
        places a buy order
    place_sell_order:
        places a sell order
    close_out:
        closes out a long or short position
    """

    def __init__(self, start, end, amount, ftc=0.0, ptc=0.0, verbose=True):
        self.start = start
        self.end = end
        self.initial_amount = amount
        self.amount = amount
        self.ftc = ftc
        self.ptc = ptc
        self.units = 0
        self.position = 0
        self.trades = 0
        self.verbose = verbose
        self.get_data()

    def get_data(self):
        """Retrieve and prepares the data."""
        raw = pd.read_csv("Backtest_Class/Bitstamp_BTCUSD_rev1.csv", index_col=1
                            ,parse_dates=True).dropna()
        raw = pd.DataFrame(raw["close"])
        raw = raw.loc[self.start:self.end]
        # close = "Adj Close"
        # raw.rename(columns={close: "close"}, inplace=True)
        raw['return'] = np.log(raw / raw.shift(1))
        self.data = raw.dropna()

    def plot_data(self, cols=None):
        """Plot the closing prices of symbol."""
        if cols is None:
            cols = ["close"]
        self.data["close"].plot(figsize=(10, 6), title="Backtest")
        plt.show()

    def get_date_price(self, bar):
        """Return date and price for bar."""
        date = str(self.data.index[bar])[:10]
        price = self.data.close.iloc[bar]
        return date, price

    def print_balance(self, bar):
        """Print out current cash out balance info."""
        date, price = self.get_date_price(bar)
        print(f"{date}, current balance {self.amount:.2f}")

    def print_net_wealth(self, bar):
        """Print out current cash balance info."""
        date, price = self.get_data_price(bar)
        net_wealth = self.units * price + self.amount
        print(f"{date}, current net wealth {self.net_wealth:.2f}")

    def place_buy_order(self, bar, units=None, amount=None):
        """Place buy order."""
        date, price = self.get_date_price(bar)
        if units is None:
            units = int(amount / price)
        self.amount -= (units * price) * (1 + self.ptc) + self.ftc
        self.units += units
        self.trades += 1
        if self.verbose:
            print(f"{date} selling {units} units at {price:.2f}")
            self.print_balance(bar)
            self.print_net_wealth(bar)

    def place_sell_order(self, bar, units=None, amount=None):
        """Place sell order."""
        date, price = self.get_date_price(bar)
        if units is None:
            units = int(amount / price)
        self.amount += (units * price) * (1 - self.ptc) - self.ftc
        self.units -= units
        self.trades += 1
        if self.verbose:
            print(f"{date} selling {units} units at {price:.2f}")
            self.print_balance(bar)
            self.print_net_wealth(bar)

    def close_out(self, bar):
        """Close out a long or short position."""
        date, price = self.get_date_price(bar)
        self.amount += self.units * price
        self.units = 0
        self.trades += 1
        if self.verbose:
            print(f"{date} inventory {self.units} units at {price:.2f}")
            print('=' * 55)
        print("Final balance [$] {:.2f}".format(self.amount))
        perf = ((self.amount - self.initial_amount) /
                self.initial_amount * 100)
        print("Net Performance [%] {:.2f}".format(perf))
        print("Trades Executed [#] {}".format(self.trades))
        print('=' * 55)

if __name__ == '__main__':
    bb = BacktestBase("2010-1-1", "2019-12-31", 10000)
    print(bb.data.info())
    print(bb.data.tail())
    bb.plot_data()
