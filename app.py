
import streamlit as st
import plotly.graph_objects as go
from pycoingecko import CoinGeckoAPI
import pandas as pd

# create a CoinGeckoAPI object
cg = CoinGeckoAPI()

# get the list of available coins and vs_currencies
coins_list = cg.get_coins_list()
coin_ids = sorted(set(coin['id'] for coin in coins_list))
vs_currencies = cg.get_supported_vs_currencies()

# create the widgets
coin_dropdown = st.selectbox('Select a coin:', coin_ids)
currency_dropdown = st.selectbox('Select a currency:', vs_currencies)

# retrieve the data from the API
data = cg.get_coin_market_chart_by_id(id=coin_dropdown, vs_currency=currency_dropdown, days=30)
price_data = data['prices']
df = pd.DataFrame(price_data, columns=['timestamp', 'price'])
df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
df.drop(columns='timestamp', inplace=True)

candlestick_data = df.groupby(df.date.dt.date).agg({'price': ['min', 'max', 'first', 'last']})

# plot the data using Streamlit's plotting functions
st.write(f"## {coin_dropdown} prices in the last 30 days")
fig = go.Figure(data=[go.Candlestick(x=candlestick_data.index,
                                     open=candlestick_data['price']['first'],
                                     high=candlestick_data['price']['max'],
                                     low=candlestick_data['price']['min'],
                                     close=candlestick_data['price']['last'])
                                     ])
fig.update_layout(
    yaxis_title='Price in '+currency_dropdown,
    xaxis_title='Date')
st.plotly_chart(fig)