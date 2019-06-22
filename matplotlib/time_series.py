import pandas as pd
from matplotlib import pyplot as plt

plt.style.use("seaborn")

data = pd.read_csv("../data/time_series.csv")

data["Date"] = pd.to_datetime(data["Date"])
data.sort_values("Date", inplace=True)

price_date = data["Date"]
price_close = data["Close"]

plt.plot_date(price_date, price_close, linestyle="solid")

plt.gcf().autofmt_xdate()

plt.title("Bitcoin Prices")
plt.xlabel("Date")
plt.ylabel("Closing Price")

plt.tight_layout()

plt.show()
