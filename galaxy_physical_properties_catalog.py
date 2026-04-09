import astropy
from astropy.io import fits
from astropy.table import Table

file_path = "IronPhysProp_v1.2.fits"
with fits.open(file_path) as hdul:
    data = Table(hdul[1].data)

required_columns = ['TARGETID', 'RA', 'DEC', 'Z', 'SPECTYPE', 'LOGM', 'LOGM_ERR', 'LOGSFR', 'LOGSFR_ERR']
if not all(col in data.colnames for col in required_columns):
    raise ValueError(f"FITS file must contain columns: {required_columns}")

z_min = 0.29
z_max = 0.4

filtered_data = data[(data['Z'] >= z_min) & (data['Z'] <= z_max)]

print(f"Found {len(filtered_data)} systems with {z_min} ≤ z ≤ {z_max}")

for i, row in enumerate(filtered_data):
    targetid, ra, dec, z, spectype, logm, logm_err, logsfr, logsfr_err = row['TARGETID'], row['RA'], row['DEC'], row['Z'], row['SPECTYPE'], row['LOGM'], row['LOGM_ERR'], row['LOGSFR'], row['LOGSFR_ERR']
    
import pandas as pd
df = filtered_data.to_pandas()
df = df.rename(columns={
    'TARGETID': 'agnqso_targetid',
    'RA': 'target_ra',
    'DEC': 'target_dec',
    'Z': 'z',
    'SPECTYPE' : 'spectype'
})

# Save to CSV
df.to_csv("filtered_galaxy_physical_properties.csv", index=False)

print("Exported filtered results to filtered_galaxy_physical_properties.csv")
