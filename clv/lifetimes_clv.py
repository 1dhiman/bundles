import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

pd.set_option('max_columns', 50)
mpl.rcParams['lines.linewidth'] = 2

# %matplotlib inline

df = pd.read_excel('../dataset.xlsx', 1)
df.head()

from lifetimes.utils import summary_data_from_transaction_data

data = summary_data_from_transaction_data(df, 'UserId', 'OrderDate', 
                                          observation_period_end='2010-01-09',
                                         monetary_value_col='TotalCharges')
data.head()

from lifetimes import BetaGeoFitter

bgf = BetaGeoFitter(penalizer_coef=0.0001)
bgf.fit(data['frequency'], data['recency'], data['T'])

bgf

from lifetimes.plotting import plot_frequency_recency_matrix

plot_frequency_recency_matrix(bgf);

from lifetimes.plotting import plot_probability_alive_matrix

plot_probability_alive_matrix(bgf);

t = 1 # values from 0.1 to 1
data['predicted_purchases'] = bgf.conditional_expected_number_of_purchases_up_to_time(t, data['frequency'], data['recency'], data['T'])
data.sort_values(by='predicted_purchases').tail(10)

from lifetimes.plotting import plot_period_transactions
plot_period_transactions(bgf)

from lifetimes.utils import calibration_and_holdout_data

calibration_data = calibration_and_holdout_data(df, 'UserId', 'OrderDate',
                                              calibration_period_end='2009-12-15',
                                              observation_period_end='2010-01-09')
calibration_data.head()

from lifetimes.plotting import plot_calibration_purchases_vs_holdout_purchases

bgf.fit(calibration_data['frequency_cal'], calibration_data['recency_cal'], calibration_data['T_cal'])
plot_calibration_purchases_vs_holdout_purchases(bgf, calibration_data)

with_frequency = data[data['frequency']>0]
with_frequency.head()

with_frequency[['monetary_value', 'frequency']].corr()

from lifetimes import GammaGammaFitter

ggf = GammaGammaFitter(penalizer_coef = 0)
ggf.fit(with_frequency['frequency'], with_frequency['monetary_value'])

ggf

ggf.conditional_expected_average_profit(
    data['frequency'],
    data['monetary_value']
).head(20)

"Expected conditional average profit: %s, Average profit: %s" % (
    ggf.conditional_expected_average_profit(
        data['frequency'],
        data['monetary_value']
    ).mean(),
    data[data['frequency']>0]['monetary_value'].mean()
)

bgf.fit(data['frequency'], data['recency'], data['T'])

ggf.customer_lifetime_value(
    bgf, #the model to use to predict the number of future transactions
    data['frequency'],
    data['recency'],
    data['T'],
    data['monetary_value'],
    time=2, # months
    discount_rate=0.1 # monthly discount rate
).head(10)

