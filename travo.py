import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock ML Demo", layout="wide")

# ---------------- Sidebar Inputs ----------------
st.sidebar.header("Stock Settings")
ticker = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# ---------------- Data Collection ----------------
st.title("📈 Data to Deployment: Stock ML Demo")
st.write("This demo shows how to go from **data → preprocessing → modeling → deployment** with Streamlit.")

@st.cache_data
def load_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

df = load_data(ticker, start_date, end_date)

if df.empty:
    st.error("No data found. Please check ticker or date range.")
    st.stop()

st.subheader("Raw Data")
st.dataframe(df.tail())

# ---------------- Feature Engineering ----------------
df["SMA_20"] = df["Close"].rolling(20).mean()
df["SMA_50"] = df["Close"].rolling(50).mean()
df["Volatility"] = (df["High"] - df["Low"]) / df["Open"]

# RSI calculation
def compute_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

df["RSI"] = compute_rsi(df["Close"])
df["Target"] = df["Close"].shift(-1)
df = df.dropna()

# ---------------- Visualization ----------------
st.subheader("Stock Price with Moving Averages")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df.index, df["Close"], label="Close", color="blue")
ax.plot(df.index, df["SMA_20"], label="SMA 20", color="orange")
ax.plot(df.index, df["SMA_50"], label="SMA 50", color="red")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
st.pyplot(fig)

# ---------------- ML Modeling ----------------
X = df[["SMA_20", "SMA_50", "Volatility", "RSI"]]
y = df["Target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

st.subheader("Model Performance")
st.write(f"**R² Score:** {r2:.4f}")
st.write(f"**RMSE:** {rmse:.4f}")

# ---------------- Prediction ----------------
latest_features = df[["SMA_20", "SMA_50", "Volatility", "RSI"]].iloc[-1].values.reshape(1, -1)
predicted_price = model.predict(latest_features)[0]

st.subheader("Tomorrow's Prediction")
st.success(f"📊 Predicted Closing Price for next day: **{predicted_price:.2f} USD**")

