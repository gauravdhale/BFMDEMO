import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests
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
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Sidebar adjustments */
    [data-testid="stSidebar"] .css-1d391kg {  /* Adjust the sidebar font size */
        font-size: 0.9rem;
    }
    /* Main content adjustments */
    .stApp {
        background-color: #f5f7fa;
    }
    /* Header styles */
    h1, h2, h3, h4, h5, h6 {
        color: #2E586D;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Metric styles */
    .metric-label > div {
        font-size: 0.8rem;
    }
    .metric-value > div {
        font-size: 1.2rem;
    }
    /* Adjust dataframe font size */
    .dataframe {
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Divider
st.title("📊 Banking Sector Financial Dashboard")
st.markdown("<hr style='border:1px solid #e0e0e0;margin-top:-10px;'>", unsafe_allow_html=True)

# Sidebar Selection
selected_stock = st.sidebar.selectbox("Select a Bank", list(companies.keys()))

# Function to Fetch Stock Data
@st.cache_data
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

# Load Selected Data
@st.cache_data
def load_data(file_name):
    url = f"https://raw.githubusercontent.com/gauravdhale/BFMDEMO/main/{file_name}"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df.rename(columns={"Open": "Actual Price", "Predicted_Open": "Predicted Price"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", dayfirst=True, errors="coerce")
        df.set_index("Date", inplace=True)
        return df
    except Exception as e:
        st.error(f"Error reading {file_name}: {e}")
        return pd.DataFrame()

# Function to Plot Actual vs Predicted Prices
def plot_actual_vs_predicted(data, company_name):
    if data.empty:
        st.warning(f"No data available for {company_name}.")
        return
    required_columns = ["Actual Price", "Predicted Price"]
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        st.error(f"⚠ Missing columns in CSV: {missing_columns}")
        return
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index, y=data["Actual Price"], mode="lines",
        name="Actual Price", line=dict(color="#1f77b4")))
    fig.add_trace(go.Scatter(
        x=data.index, y=data["Predicted Price"], mode="lines",
        name="Predicted Price", line=dict(color="#ff7f0e", dash="dash")))
    fig.update_layout(
        title=f"{company_name} - Actual vs Predicted Prices",
        xaxis_title="Date", yaxis_title="Price", hovermode="x unified", height=350,
        margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)

# Function to Plot Correlation Heatmap
def plot_correlation_heatmap(data, company_name):
    if data.empty:
        st.warning(f"No data available for {company_name} to compute correlation matrix.")
        return
    corr = data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].corr()
    plt.figure(figsize=(5, 4))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title(f"{company_name} - Correlation Matrix", fontsize=12)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    st.pyplot(plt)

# Fetch Data
bank_nifty_data = fetch_stock_data(bank_nifty_ticker)
selected_stock_data = fetch_stock_data(companies[selected_stock])
selected_file = csv_files.get(selected_stock)
data = load_data(selected_file)

# Sidebar Metrics
st.sidebar.header("Key Metrics")
if not selected_stock_data.empty:
    latest_data = selected_stock_data.iloc[-1]
    metric_values = {
        "Open": latest_data["Open"],
        "Close": latest_data["Close"],
        "High": latest_data["High"],
        "Low": latest_data["Low"],
        "EPS": np.random.uniform(10, 50),
        "IPO Price": np.random.uniform(200, 1000),
        "P/E Ratio": np.random.uniform(5, 30),
        "Dividend": np.random.uniform(1, 5)
    }
    for label, value in metric_values.items():
        st.sidebar.write(f"**{label}:** {value:.2f}")
else:
    st.sidebar.warning(f"No stock data available for {selected_stock}.")

# Layout Adjustments
# First Row: Trends
st.markdown("### Market Trends")
row1_col1, row1_col2 = st.columns(2, gap="large")
with row1_col1:
    st.subheader("BankNifty Trend")
    if not bank_nifty_data.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=bank_nifty_data.index, y=bank_nifty_data['Close'], mode='lines',
            name='BankNifty Close', line=dict(color='#1f77b4')))
        fig.update_layout(
            title='BankNifty Close Price', height=350,
            margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for BankNifty.")
with row1_col2:
    st.subheader(f"{selected_stock} Trend")
    if not selected_stock_data.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=selected_stock_data.index, y=selected_stock_data['Close'], mode='lines',
            name=f'{selected_stock} Close', line=dict(color='#2ca02c')))
        fig.update_layout(
            title=f'{selected_stock} Close Price', height=350,
            margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No data available for {selected_stock}.")

# Second Row: Prediction vs Actual and Correlation Heatmap
st.markdown("### Analysis")
row2_col1, row2_col2 = st.columns(2, gap="large")
with row2_col1:
    st.subheader("Prediction vs Actual")
    plot_actual_vs_predicted(data, selected_stock)
with row2_col2:
    st.subheader("Correlation Heatmap")
    plot_correlation_heatmap(selected_stock_data, selected_stock)

# Third Row: Profit vs Revenue and Heatmap
st.markdown("### Financial Insights")
row3_col1, row3_col2 = st.columns(2, gap="large")
with row3_col1:
    st.subheader("Profit vs Revenue")
    profit_revenue_data = pd.DataFrame({
        "Year": np.arange(2015, 2025),
        "Total Revenue": np.random.randint(50000, 150000, 10),
        "Net Profit": np.random.randint(5000, 30000, 10)
    })
    fig_pr, ax_pr = plt.subplots(figsize=(5, 3))
    profit_revenue_data.set_index("Year").plot(kind="bar", ax=ax_pr, width=0.8, color=["#1f77b4", "#ff7f0e"])
    ax_pr.set_title("Total Revenue vs Net Profit", fontsize=12)
    ax_pr.set_xlabel("Year", fontsize=10)
    ax_pr.set_ylabel("Amount (INR in Lakhs)", fontsize=10)
    ax_pr.tick_params(axis='x', labelrotation=0, labelsize=8)
    ax_pr.tick_params(axis='y', labelsize=8)
    ax_pr.legend(fontsize=8)
    st.pyplot(fig_pr)
with row3_col2:
    st.subheader("Nifty Bank Composition")
    github_url = "https://raw.githubusercontent.com/gauravdhale/BFMDEMO/main/heatmap.csv"
    if github_url:
        try:
            df_heatmap = pd.read_csv(github_url, encoding='ISO-8859-1')
            if 'Company' in df_heatmap.columns and 'Weight(%)' in df_heatmap.columns:
                df_heatmap.set_index('Company', inplace=True)
                plt.figure(figsize=(5, 3))
                sns.heatmap(df_heatmap[['Weight(%)']], annot=True, cmap='YlGnBu', cbar=True, linewidths=0.5)
                plt.title('Nifty Bank Composition', fontsize=12)
                plt.xticks(fontsize=8)
                plt.yticks(fontsize=8)
                st.pyplot(plt)
            else:
                st.write("Heatmap data not available.")
        except Exception as e:
            st.write(f"An error occurred: {e}")
    else:
        st.write("Please enter a valid GitHub URL.")

# Spacer to adjust layout
st.markdown("<br>", unsafe_allow_html=True)

# Data Table in Expander
with st.expander("BankNifty Index Data Table"):
    if not bank_nifty_data.empty:
        st.dataframe(
            bank_nifty_data.tail(10).style.format(
                {"Close": "{:.2f}", "Open": "{:.2f}", "High": "{:.2f}", "Low": "{:.2f}"}),
            height=200)
    else:
        st.warning("No BankNifty data available.")

st.success("Analysis Completed!")
