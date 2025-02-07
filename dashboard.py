import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Title of the app
st.title("Nifty Bank Composition Heatmap")

# Text input for GitHub URL
github_url = st.text_input("Enter the GitHub CSV file URL", value="https://raw.githubusercontent.com/gauravdhale/BFMDEMO/main/heatmap.csv")

if github_url:
    try:
        # Read CSV file from GitHub with specified encoding
        df = pd.read_csv(github_url, encoding='ISO-8859-1')

        # Set the Company as index for heatmap purposes
        if 'Company' in df.columns:
            df.set_index('Company', inplace=True)
        else:
            st.write("Error: 'Company' column not found in the CSV file.")
        
        # Create a heatmap using seaborn. We need a matrix shape so we'll reshape the data.
        # We can use a pivot table-like structure with a single column 'Weight(%)'.

        # Plotting the heatmap
        if 'Weight(%)' in df.columns:
            plt.figure(figsize=(6,8))
            # The data is one-dimensional, we add a dummy dimension to make it 2D
            heatmap_data = df[['Weight(%)']]
            sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', cbar=True)
            plt.title('Nifty Bank Composition Heatmap')
            plt.ylabel('Company')
            plt.xlabel('')
            plt.tight_layout()
            st.pyplot(plt)
        else:
            st.write("HEAT MAP ")

    except Exception as e:
        st.write(f"An error occurred: {e}")
else:
    st.write("Please upload a CSV file or enter a valid GitHub URL.")
