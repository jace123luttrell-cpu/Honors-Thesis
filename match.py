import pandas as pd

# Load the CSV files into DataFrames
df_main = pd.read_csv('filteredmatches>100.csv') # The file you want to remove entries from
df_filter = pd.read_csv('filteredmatches_10-100.csv') # The file containing entries to remove

# Perform an anti-join to exclude rows with matching agnqso_targetid and mgii_targetid
df_result = df_main.merge(
    df_filter[['agnqso_targetid', 'mgii_targetid']],
    on=['agnqso_targetid', 'mgii_targetid'],
    how='left',
    indicator=True
)

# Keep only the rows that did not match
df_result = df_result[df_result['_merge'] == 'left_only'].drop(columns=['_merge'])

# Save the result to a new CSV file
df_result.to_csv('filteredmatches_1000.csv', index=False)
