import pandas as pd
from matplotlib import pyplot as plt

plt.style.use("seaborn")

data = pd.read_csv("../data/time_series.csv")

data["Date"] = pd.to_datetime(data["Date"])
data.sort_values("Date", inplace=True)

price_date = data["Date"]
price_close = data["Close"]

fig, ax = plt.subplots()

ax.plot_date(price_date, price_close, linestyle="solid")

plt.gcf().autofmt_xdate()

ax.set_title("Bitcoin Prices")
ax.set_xlabel("Date")
ax.set_ylabel("Closing Price")

plt.tight_layout()

plt.show()

fig.savefig("plots/time_series.png")
