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
        if 'Company' in df.columns and 'Weight(%)' in df.columns:
            df.set_index('Company', inplace=True)

            # Plotting the heatmap
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
            # Skip heatmap generation if required columns are not present
            st.write("Error: Required columns 'Company' and 'Weight(%)' not found in the CSV file.")

    except Exception as e:
        st.write(f"An error occurred: {e}")
else:
    st.write("Please upload a CSV file or enter a valid GitHub URL.")
