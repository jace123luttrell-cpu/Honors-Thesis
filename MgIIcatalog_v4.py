import astropy
from astropy.io import fits
from astropy.table import Table

file_path = "MgII-Absorbers-DR1.fits"
with fits.open(file_path) as hdul:
    data = Table(hdul[1].data)

required_columns = ['TARGETID', 'RA', 'DEC', 'Z_MGII', 'EW_2803']
if not all(col in data.colnames for col in required_columns):
    raise ValueError(f"FITS file must contain columns: {required_columns}")

z_min = 0.29
z_max = 0.4

filtered_data = data[(data['Z_MGII'] >= z_min) & (data['Z_MGII'] <= z_max)]

print(f"Found {len(filtered_data)} systems with {z_min} ≤ z ≤ {z_max}")

for i, row in enumerate(filtered_data):
    targetid, ra, dec, z = row['TARGETID'], row['RA'], row['DEC'], row['Z_MGII']
    print(f"MgII System {i+1} — ID: {targetid}, RA: {ra:.4f}, Dec: {dec:.4f}, z: {z:.4f}")
    
import pandas as pd
df = filtered_data.to_pandas()

# Save to CSV
df.to_csv("filtered_mgii_absorbers.csv", index=False)

print("Exported filtered results to filtered_mgii_absorbers.csv")
