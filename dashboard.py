import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Title of the app
st.title("Company Weights Heatmap")

# File uploader to upload CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read CSV file
    df = pd.read_csv(uploaded_file)

    # Display data
    st.write("Data from CSV file:")
    st.write(df)

    # Generate heatmap
    st.write("Heatmap:")
    fig, ax = plt.subplots()
    sns.heatmap(df[['Weight %']], annot=True, cmap='coolwarm', ax=ax, yticklabels=df['Company Name'])
    st.pyplot(fig)
