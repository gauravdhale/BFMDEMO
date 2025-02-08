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
st.set_page_config(
    page_title="Banking Sector Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS styles to enhance visual appeal
st.markdown(
    """
    <style>
    /* Main background */
    .main {
        background-color: #f0f2f6;
    }
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #1f4e79;
        color: white;
    }
    .sidebar .sidebar-content a, .sidebar .sidebar-content a:hover {
        color: #f0f2f6;
    }
    /* Header styling */
    .stHeader {
        background-color: #1f4e79;
    }
    /* Metric text color */
    [data-testid="stMetricValue"] {
        color: #f0f2f6;
    }
    /* Center align the title */
    .css-10trblm {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Banking Sector Financial Dashboard")
st.markdown("---")

# Selection Dropdown
selected_stock = st.sidebar.selectbox("🔍 **Select a Bank**", list(companies.keys()))

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

# Fetch Data
bank_nifty_data = fetch_stock_data(bank_nifty_ticker)
selected_stock_data = fetch_stock_data(companies[selected_stock])

# Display Metrics if Data is Available
st.sidebar.header("📌 **Key Metrics**")
if not selected_stock_data.empty:
    latest_data = selected_stock_data.iloc[-1]

    # Ensure that each metric is a scalar value
    metric_values = {
        "Open": float(latest_data["Open"]),
        "Close": float(latest_data["Close"]),
        "High": float(latest_data["High"]),
        "Low": float(latest_data["Low"]),
        "EPS": float(np.random.uniform(10, 50)),
        "IPO Price": float(np.random.uniform(200, 1000)),
        "P/E Ratio": float(np.random.uniform(5, 30)),
        "Dividend": float(np.random.uniform(1, 5))
    }
    for label, value in metric_values.items():
        st.sidebar.metric(label=f"**{label}**", value=f"{value:.2f}")
else:
    st.sidebar.warning(f"No stock data available for {selected_stock}.")

# BankNifty and Stock Overview
st.header("📈 **Market Overview**")
col1, col2 = st.columns([1, 1])

# BankNifty Trend Graph
with col1:
    st.subheader("**BankNifty Trend**")
    if not bank_nifty_data.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=bank_nifty_data.index,
            y=bank_nifty_data['Close'],
            mode='lines',
            name='BankNifty Close',
            line=dict(color='#1f77b4', width=2)
        ))
        fig.update_layout(
            title="BankNifty Closing Prices",
            xaxis_title="Date",
            yaxis_title="Price",
            hovermode="x unified",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for BankNifty.")

# Selected Stock Trend Graph
with col2:
    st.subheader(f"**{selected_stock} Trend**")
    if not selected_stock_data.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=selected_stock_data.index,
            y=selected_stock_data['Close'],
            mode='lines',
            name=f"{selected_stock} Close",
            line=dict(color='#ff7f0e', width=2)
        ))
        fig.update_layout(
            title=f"{selected_stock} Closing Prices",
            xaxis_title="Date",
            yaxis_title="Price",
            hovermode="x unified",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No data available for {selected_stock}.")

# Financial Analysis Section
st.header("📊 **Financial Analysis**")

# Create two columns for better layout
col4, col5 = st.columns([2, 1])

# 🔹 Profit vs Revenue Comparison Graph
with col4:
    st.subheader("📈 **Profit vs Revenue Comparison**")

    profit_revenue_data = pd.DataFrame({
        "Year": np.arange(2015, 2025),
        "Total Revenue": np.random.randint(50000, 150000, 10),
        "Net Profit": np.random.randint(5000, 30000, 10)
    })

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=profit_revenue_data['Year'],
        y=profit_revenue_data['Total Revenue'],
        name='Total Revenue',
        marker_color='#1f77b4'
    ))
    fig.add_trace(go.Bar(
        x=profit_revenue_data['Year'],
        y=profit_revenue_data['Net Profit'],
        name='Net Profit',
        marker_color='#ff7f0e'
    ))
    fig.update_layout(
        barmode='group',
        title="Total Revenue vs Net Profit",
        xaxis_title="Year",
        yaxis_title="Amount (INR in Lakhs)",
        legend_title="Metrics",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# 🔹 BankNifty Index Data Table
with col5:
    st.subheader("📋 **BankNifty Index Data**")

    if not bank_nifty_data.empty:
        styled_data = bank_nifty_data.tail(10)[['Open', 'High', 'Low', 'Close']]
        st.dataframe(
            styled_data.style.set_properties(**{'background-color': '#f0f2f6', 'color': '#000'})
            .format("{:.2f}")
        )
    else:
        st.warning("No BankNifty data available.")

# Function to get the list of CSV files from GitHub (cached)
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

# Load Selected Data (cached)
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

selected_file = csv_files.get(selected_stock)
data = load_data(selected_file)

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
        x=data.index,
        y=data["Actual Price"],
        mode="lines",
        name="Actual Price",
        line=dict(color='#2ca02c', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["Predicted Price"],
        mode="lines",
        name="Predicted Price",
        line=dict(color='#d62728', dash="dash", width=2)
    ))
    fig.update_layout(
        title=f"{company_name} - Actual vs Predicted Prices",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# Plot Data
if selected_file:
    st.header(f"📈 **Prediction vs Actual - {selected_file.split('.')[0]}**")
    plot_actual_vs_predicted(data, selected_file.split('.')[0])
else:
    st.warning("No CSV file selected for the chosen stock.")

# Adding Heatmap Section
st.header("🌡️ **Nifty Bank Composition Heatmap**")

# Text input for GitHub URL
github_url = st.text_input(
    "Enter the GitHub CSV file URL:",
    value="https://raw.githubusercontent.com/gauravdhale/BFMDEMO/main/heatmap.csv"
)

if github_url:
    try:
        # Read CSV file from GitHub
        df = pd.read_csv(github_url, encoding='ISO-8859-1')

        # Set 'Company' as index for heatmap
        if 'Company' in df.columns:
            df.set_index('Company', inplace=True)
        else:
            st.error("Error: 'Company' column not found in the CSV file.")

        # Plotting the heatmap
        if 'Weight(%)' in df.columns:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(
                df[['Weight(%)']],
                annot=True,
                cmap='YlGnBu',
                cbar=True,
                linewidths=0.5,
                linecolor='white',
                fmt='.2f'
            )
            ax.set_title('Nifty Bank Composition Heatmap', fontsize=14)
            plt.xticks(rotation=0)
            plt.yticks(rotation=0)
            st.pyplot(fig)
        else:
            st.error("Required column 'Weight(%)' not found in the CSV file.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please enter a valid GitHub CSV file URL.")

st.markdown("---")
st.success("✅ **Dashboard enhanced successfully!**")
