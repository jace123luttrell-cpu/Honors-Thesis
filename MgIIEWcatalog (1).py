import pandas as pd
import numpy as np
import astropy
from astropy.io import fits
from astropy.table import Table

# Load TARGETIDs from CSV and remove duplicates
csv_path = "filteredmatches>100.csv"  # replace with your actual path
target_id_df = pd.read_csv(csv_path)

# Make sure the column name matches; assume it's 'TARGETID' or adjust if needed
if 'mgii_targetid' not in target_id_df.columns:
    raise ValueError("CSV must contain a column named 'mgii_targetid'")

# Remove duplicates
unique_target_ids = target_id_df['mgii_targetid'].drop_duplicates().values

# Load FITS file
file_path = "MgII-Absorbers-DR1.fits"
with fits.open(file_path) as hdul:
    data = Table(hdul[1].data)

# Verify required columns
required_columns = ['TARGETID', 'RA', 'DEC', 'Z_MGII', 'EW_2803', 'EW_2803_ERR_LOW', 'EW_2803_ERR_HIGH', 'AMP_2803', 'STDDEV_2803']
if not all(col in data.colnames for col in required_columns):
    raise ValueError(f"FITS file must contain columns: {required_columns}")

# Filter FITS data using the unique target IDs
mask = np.isin(data['TARGETID'], unique_target_ids)
filtered_data = data[mask]

# Print summary
print(f"Found {len(filtered_data)} matching systems from {len(unique_target_ids)} unique TARGETIDs.")

# Optional: Display or export results
for i, row in enumerate(filtered_data):
    print(f"{i+1}: ID {row['TARGETID']} — z = {row['Z_MGII']:.4f}, EW_2803 = {row['EW_2803']:.2f} Å")

# Save filtered data to CSV
df = filtered_data.to_pandas()
df.to_csv("filtered_by_csv_targetids.csv", index=False)
print("Exported matched systems to filtered_by_csv_targetids.csv")
