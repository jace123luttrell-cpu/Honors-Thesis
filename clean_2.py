import pandas as pd

# Load the CSV file
df = pd.read_csv('filteredmatches_1000_with_zerr.csv')

# 1. Sort by column 'B' so the lowest values are at the top
df_sorted = df.sort_values(by='comoving_transverse_distance', ascending=True)

# 2. Drop duplicates in 'A', keeping 'first' (which is now the lowest 'B')
df_clean = df_sorted.drop_duplicates(subset='mgii_targetid', keep='first')

# Save the cleaned data back to a new CSV file
df_clean.to_csv('cleaned_output_2_with_zerr.csv', index=False)
