# Import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create the dataframe with the provided data
data = {
    'Company': ['HDFC Bank Ltd.', 'ICICI Bank Ltd.', 'Kotak Mahindra Bank Ltd.', 'State Bank of India', 
                'Axis Bank Ltd.', 'IndusInd Bank Ltd.', 'Federal Bank Ltd.', 'Bank of Baroda',
                'IDFC First Bank Ltd.', 'Punjab National Bank', 'Other'],
    'Weight(%)': [27.63, 25.05, 9.61, 8.43, 8.11, 4.78, 3.34, 2.90, 2.86, 2.54, 4.75]
}
df = pd.DataFrame(data)

# Set the Company as index for heatmap purposes
df.set_index('Company', inplace=True)

# Create a heatmap using seaborn. We need a matrix shape so we'll reshape the data.
# We can use a pivot table-like structure with a single column 'Weight(%)'.

# Plotting the heatmap
plt.figure(figsize=(6,8))
# The data is one-dimensional, we add a dummy dimension to make it 2D
heatmap_data = df[['Weight(%)']]
sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', cbar=True)
plt.title('Nifty Bank Composition Heatmap')
plt.ylabel('Company')
plt.xlabel('')
plt.tight_layout()
plt.show()

print('Heatmap generated for Nifty Bank composition.')
