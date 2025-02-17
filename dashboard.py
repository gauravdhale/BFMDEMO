import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import seaborn as sns

# Define Banking Stocks and Bank Nifty Index
companies = {
    'HDFC Bank': 'HDFCBANK.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'State Bank of India': 'SBIN.NS',
    'Kotak Mahindra Bank': 'KOTAKBANK.NS',
    'Axis Bank': 'AXISBANK.NS',
    'Bank of Baroda': 'BANKBARODA.NS'
}

csv_files = {
    'HDFC Bank': 'HDFCBANK.csv',
    'ICICI Bank': 'ICICI_BANK.csv',
    'State Bank of India': 'SBI.csv',
    'Kotak Mahindra Bank': 'KOTAK.csv',
    'Axis Bank': 'AXIS.csv',
    'Bank of Baroda': 'BARODA.csv'
}
bank_nifty_ticker = "^NSEBANK"

# Streamlit Configuration
st.set_page_config(page_title="Banking Sector Dashboard", layout="wide")
st.title("📊 Banking Sector Financial Dashboard")
st.markdown("---")

# Sidebar Configuration
st.sidebar.header("📌 Key Metrics")
selected_bank = st.sidebar.selectbox("Select a bank", list(companies.keys()))

# Function to Format Market Cap
def format_market_cap(value):
    if value >= 1e12:
        return f"{value / 1e12:.2f}T"
    elif value >= 1e9:
        return f"{value / 1e9:.2f}B"
    elif value >= 1e6:
        return f"{value / 1e6:.2f}M"
    return str(value)

# Function to Retrieve Stock Data
def get_stock_data(tickers):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        data[ticker] = {
            "Open": info.get("open", "N/A"),
            "Close": info.get("previousClose", "N/A"),
            "High": info.get("dayHigh", "N/A"),
            "Low": info.get("dayLow", "N/A"),
            "Market Cap": format_market_cap(info.get("marketCap", "N/A")),
            "Beta (5Y Monthly)": info.get("beta", "N/A"),
            "Volume": info.get("volume", "N/A"),
            "EPS (TTM)": info.get("trailingEps", "N/A"),
            "PE Ratio (TTM)": info.get("trailingPE", "N/A"),
            "Forward Dividend & Yield": info.get("dividendYield", "N/A"),
            "Avg. Volume": info.get("averageVolume", "N/A"),
            "Profit Margin": f"{info.get('profitMargins', 0) * 100:.2f}%" if info.get("profitMargins") else "N/A",
            "Return on Assets (TTM)": f"{info.get('returnOnAssets', 0) * 100:.2f}%" if info.get("returnOnAssets") else "N/A",
            "Return on Equity (TTM)": f"{info.get('returnOnEquity', 0) * 100:.2f}%" if info.get("returnOnEquity") else "N/A"
        }
    return data

# Fetch Stock Data for Selected Bank
data = get_stock_data([companies[selected_bank]])
ticker = companies[selected_bank]

# Display Stock Metrics in Sidebar
st.sidebar.subheader(selected_bank)
for key, value in data[ticker].items():
    st.sidebar.write(f"{key}: {value}")

# Function to Fetch Stock Data
def fetch_stock_data(ticker, period="5y"):
    try:
        stock_data = yf.download(ticker, period=period, interval="1d")
        if stock_data.empty:
            return pd.DataFrame()
        stock_data['MA_20'] = stock_data['Close'].rolling(window=20).mean()
        stock_data['MA_50'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['Price_Change'] = stock_data['Close'].pct_change()
        return stock_data.dropna()
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

# Function to get the list of CSV files from GitHub
@st.cache_data
def get_csv_files():
    api_url = "https://api.github.com/repos/gauravdhale/BFMDEMO/contents"
    response = requests.get(api_url)
    if response.status_code == 200:
        files = [file["name"] for file in response.json() if file["name"].endswith(".csv")]
        return files
    else:
        st.error("Error fetching file list from GitHub")
        return []

# Load Selected Data
@st.cache_data
def load_data(file_name):
    url = f"https://raw.githubusercontent.com/gauravdhale/BFMDEMO/main/{file_name}"
    try:
        st.write(f"Loading data from: {url}")
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df.rename(columns={"Open": "Actual Price", "Predicted_Open": "Predicted Price", "%_error": "% Error"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", dayfirst=True, errors="coerce")
        df.set_index("Date", inplace=True)
        return df
    except Exception as e:
        st.error(f"Error reading {file_name}: {e}")
        return pd.DataFrame()

# Function to Plot Actual vs Predicted Prices with % Error
def plot_actual_vs_predicted(data, company_name):
    if data.empty:
        st.warning(f"No data available for {company_name}.")
        return

    required_columns = ["Actual Price", "Predicted Price", "% Error"]
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        st.error(f"⚠ Missing columns in CSV: {missing_columns}")
        return

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index, y=data["Actual Price"],
        mode="lines", name="Actual Price",
        line=dict(color="green")
    ))
    fig.add_trace(go.Scatter(
        x=data.index, y=data["Predicted Price"],
        mode="lines", name="Predicted Price",
        line=dict(color="blue", dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=data.index, y=data["% Error"],
        mode="lines", name="% Error",
        line=dict(color="red", dash="dot")
    ))
    
    fig.update_layout(
        title=f"{company_name} - Actual vs Predicted Prices with % Error",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        height=350,
        margin=dict(l=40, r=40, t=60, b=40),
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

# Function to Plot Correlation Heatmap
def plot_correlation_heatmap(data, company_name):
    if data.empty:
        st.warning(f"No data available for {company_name} to compute correlation matrix.")
        return
    corr = data.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=0.35, vmax=1.00, linewidths=0.5, ax=ax)
    ax.set_title(f"{company_name} - Correlation Matrix Heatmap")
    st.pyplot(fig)

# Fetch Data
bank_nifty_data = fetch_stock_data(bank_nifty_ticker)
selected_stock_data = fetch_stock_data(companies[selected_bank])
selected_file = csv_files.get(selected_bank)
data = load_data(selected_file)



# Layout Adjustments for Proper Alignment
st.markdown("## 📈 Market Trends")

# First Row: BankNifty Trend, Selected Bank Trend, Profit vs Revenue
with st.container():
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.subheader("BankNifty Trend")
        if not bank_nifty_data.empty:
            fig1, ax1 = plt.subplots(figsize=(5, 3))
            ax1.plot(bank_nifty_data.index, bank_nifty_data['Close'], label="BankNifty Close", color='blue')
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Close Price")
            ax1.legend()
            ax1.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig1)
        else:
            st.warning("No data available for BankNifty.")
        
    with col2:
        st.subheader(f"{selected_bank} Trend")
        if not selected_stock_data.empty:
            fig2, ax2 = plt.subplots(figsize=(5, 3))
            ax2.plot(selected_stock_data.index, selected_stock_data['Close'], label=f"{selected_bank} Close", color='red')
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Close Price")
            ax2.legend()
            ax2.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig2)
        else:
            st.warning(f"No data available for {selected_bank}.")
        
    with col3:
        st.subheader("Profit vs Revenue")
        profit_revenue_data = pd.DataFrame({
            "Year": np.arange(2015, 2025),
            "Total Revenue": np.random.randint(50000, 150000, 10),
            "Net Profit": np.random.randint(5000, 30000, 10)
        })
        fig_pr, ax_pr = plt.subplots(figsize=(5, 3))
        profit_revenue_data.set_index("Year").plot(kind="bar", ax=ax_pr, width=0.8, colormap="coolwarm")
        ax_pr.set_title("Total Revenue vs Net Profit")
        ax_pr.set_xlabel("Year")
        ax_pr.set_ylabel("Amount (INR in Lakhs)")
        ax_pr.grid(axis='y', linestyle="--", alpha=0.5)
        ax_pr.legend()
        st.pyplot(fig_pr)

# Second Row: Nifty Bank Composition Heatmap, Correlation Matrix, BankNifty Index Data Table
with st.container():
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.subheader("Nifty Bank Composition Heatmap")
        github_url = "https://raw.githubusercontent.com/gauravdhale/BFMDEMO/main/heatmap.csv"
        try:
            df_heatmap = pd.read_csv(github_url, encoding='ISO-8859-1')
            if 'Company' in df_heatmap.columns and 'Weight(%)' in df_heatmap.columns:
                df_heatmap.set_index('Company', inplace=True)
                fig_hm, ax_hm = plt.subplots(figsize=(5, 3))
                sns.heatmap(df_heatmap[['Weight(%)']], annot=True, cmap='YlGnBu', cbar=True, linewidths=0.5, ax=ax_hm)
                ax_hm.set_title('Nifty Bank Composition')
                st.pyplot(fig_hm)
            else:
                st.write("Heatmap data not available.")
        except Exception as e:
            st.write(f"An error occurred: {e}")
            
    with col2:
            st.subheader("BankNifty Correlation Matrix")
            if not bank_nifty_data.empty:
                image_url = "https://raw.githubusercontent.com/gauravdhale/BFMDEMO/main/heatmap.jpg"  # URL to the image in your GitHub repository
                st.image(image_url, caption="BankNifty Index Heatmap")
            else:
                st.warning("No BankNifty data available.")
        
    with col3:
        st.subheader("BankNifty Index Data Table")
        if not bank_nifty_data.empty:
            styled_df = bank_nifty_data.tail(10).style.format({
                "Close": "{:.2f}",
                "Open": "{:.2f}",
                "High": "{:.2f}",
                 "Low": "{:.2f}"
            })
            st.dataframe(styled_df)
         else:
            st.warning("No BankNifty data available.")

# Third Row: Prediction vs Actual
with st.container():
    st.subheader("Prediction vs Actual")
    plot_actual_vs_predicted(data, selected_bank)

st.markdown("---")

st.success("🎯 Analysis Completed!")
