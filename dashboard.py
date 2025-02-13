import streamlit as st
import yfinance as yf

def get_stock_data(tickers):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        data[ticker] = {
            "EPS (TTM)": info.get("trailingEps", "N/A"),
            "PE Ratio (TTM)": info.get("trailingPE", "N/A"),
            "Forward Dividend & Yield": info.get("dividendYield", "N/A"),
            "Avg. Volume": info.get("averageVolume", "N/A"),
            "High": info.get("dayHigh", "N/A"),
            "Low": info.get("dayLow", "N/A")
        }
    return data

# List of bank tickers for Yahoo Finance
tickers = {
    "HDFC Bank": "HDFCBANK.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Bank of Baroda": "BANKBARODA.NS",
    "Axis Bank": "AXISBANK.NS",
    "State Bank of India": "SBIN.NS",
    "ICICI Bank": "ICICIBANK.NS"
}

st.title("Bank Stock Data Dashboard")
st.sidebar.header("Stock Metrics")

data = get_stock_data(tickers.values())

for bank, ticker in tickers.items():
    st.sidebar.subheader(bank)
    for key, value in data[ticker].items():
        st.sidebar.write(f"**{key}:** {value}")

st.write("### Select a bank to view details")
selected_bank = st.selectbox("Choose a bank", list(tickers.keys()))

st.write(f"## {selected_bank} Stock Data")
for key, value in data[tickers[selected_bank]].items():
    st.write(f"**{key}:** {value}")
