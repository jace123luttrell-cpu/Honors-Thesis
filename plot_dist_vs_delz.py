import pandas as pd
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

# Load CSV
dist_df = pd.read_csv("filteredmatches_100_plus_err.csv")
dist_df['mgii_targetid'] = dist_df['mgii_targetid'].astype(str)



# Open FITS file
fits_filename = "MgII-Absorbers-DR1.fits"
with fits.open(fits_filename) as hdul:
    data = hdul[1].data
    
    mgii_ids = data['TARGETID'].byteswap().newbyteorder().astype(str)
    z_mgii_err_low = data['Z_MGII_ERR_LOW'].byteswap().newbyteorder()
    z_mgii_err_high = data['Z_MGII_ERR_HIGH'].byteswap().newbyteorder()
    
    ew_df = pd.DataFrame({
        'mgii_targetid': mgii_ids,
        'Z_MGII_ERR_LOW': z_mgii_err_low,
        'Z_MGII_ERR_HIGH': z_mgii_err_high
    })

# Merge
merged_df = pd.merge(dist_df, ew_df, on='mgii_targetid', how='inner')

# Distance filter
dist_min = 0
dist_max = 100

filtered_df = merged_df[
    (merged_df['comoving_transverse_distance'] >= dist_min) &
    (merged_df['comoving_transverse_distance'] <= dist_max)
].copy()

# Validate required columns
required_cols = {'z_mgii', 'z_agnqso', 'Z_MGII_ERR_LOW', 'Z_MGII_ERR_HIGH', 'zerr'}
if not required_cols.issubset(filtered_df.columns):
    raise ValueError(f"Missing required columns: {required_cols - set(filtered_df.columns)}")

# Compute delta z
filtered_df['delta_z'] = filtered_df['z_mgii'] - filtered_df['z_agnqso']

# Drop NaNs
filtered_df = filtered_df.dropna(subset=['delta_z'])

#print(filtered_df.head())

# Compute error on delta z
filtered_df['delta_z_err_low'] = np.sqrt(filtered_df['zerr']**2 + filtered_df['Z_MGII_ERR_LOW']**2)

filtered_df['delta_z_err_high'] = np.sqrt(filtered_df['zerr']**2 + filtered_df['Z_MGII_ERR_HIGH']**2)

# Typical error
typical_delta_z_err_low = filtered_df['delta_z_err_low'].mean()
typical_delta_z_err_high = filtered_df['delta_z_err_high'].mean()

# Plot
plt.errorbar(
    filtered_df['delta_z'],
    filtered_df['comoving_transverse_distance'],
    xerr=[[typical_delta_z_err_low], [typical_delta_z_err_high]],
    fmt='o',
    ecolor='gray',
    capsize=5,
)

plt.axvline(0, color='gray', linestyle='--', label=r'$z_{MgII} = z_{galaxy}$')
plt.xlabel(r'$\Delta z = z_{MgII} - z_{galaxy}$')
plt.ylabel(' Transverse Distance (kpc)')
plt.title(r' Transverse Distance vs $\Delta z$ (<100 kpc)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
