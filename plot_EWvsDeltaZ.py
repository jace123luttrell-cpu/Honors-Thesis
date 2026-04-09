import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

# Load the csv
z_dist_df = pd.read_csv("filteredmatches_100_plus_err.csv")  # must have mgii_targetid, z_mgii, z_agnqso, comoving_transverse_distance
z_dist_df['mgii_targetid'] = z_dist_df['mgii_targetid'].astype(str)

# Open FITS file with EW data
fits_filename = "MgII-Absorbers-DR1.fits"
with fits.open(fits_filename) as hdul:
    data = hdul[1].data
    

    mgii_ids = data['TARGETID'].byteswap().newbyteorder().astype(str)
    ew_2803 = data['EW_2803'].byteswap().newbyteorder()
    ew_2803_err_low = data['EW_2803_ERR_LOW'].byteswap().newbyteorder()
    ew_2803_err_high = data['EW_2803_ERR_HIGH'].byteswap().newbyteorder()
    z_mgii_err_low = data ['Z_MGII_ERR_LOW'].byteswap().newbyteorder()
    z_mgii_err_high = data ['Z_MGII_ERR_HIGH'].byteswap().newbyteorder()
    
    ew_df = pd.DataFrame({
        'mgii_targetid': mgii_ids,
        'EW_2803': ew_2803,
        'EW_2803_ERR_LOW' : ew_2803_err_low,
        'EW_2803_ERR_HIGH' : ew_2803_err_high,
        'Z_MGII_ERR_LOW' : z_mgii_err_low,
        'Z_MGII_ERR_HIGH' : z_mgii_err_high
    })

# Merge on mgii_targetid
merged_df = pd.merge(z_dist_df, ew_df, on='mgii_targetid', how='inner')

# Filter on comoving transverse distance
filtered_df = merged_df[merged_df['comoving_transverse_distance'] <= 100].copy()

# Validate required columns
required_cols = {'z_mgii', 'z_agnqso', 'EW_2803', 'zerr', 'Z_MGII_ERR_LOW', 'Z_MGII_ERR_HIGH', 'EW_2803_ERR_LOW', 'EW_2803_ERR_HIGH'}
if not required_cols.issubset(filtered_df.columns):
    raise ValueError(f"Missing required columns: {required_cols - set(filtered_df.columns)}")

# Compute delta z
filtered_df['delta_z'] = filtered_df['z_mgii'] - filtered_df['z_agnqso']

# Drop rows with missing data in EW_2803 or delta_z
filtered_df = filtered_df.dropna(subset=['EW_2803', 'delta_z'])

# Compute error on delta z
filtered_df['delta_z_err_low'] = np.sqrt(filtered_df['zerr']**2 + filtered_df['Z_MGII_ERR_LOW']**2)

filtered_df['delta_z_err_high'] = np.sqrt(filtered_df['zerr']**2 + filtered_df['Z_MGII_ERR_HIGH']**2)

# Typical error
typical_ew_err_low = filtered_df['EW_2803_ERR_LOW'].mean()
typical_ew_err_high = filtered_df['EW_2803_ERR_HIGH'].mean()
typical_delta_z_err_low = filtered_df['delta_z_err_low'].mean()
typical_delta_z_err_high = filtered_df['delta_z_err_high'].mean()

# Plot
plt.errorbar(
    filtered_df['delta_z'],
    filtered_df['EW_2803'],
    xerr=[[typical_delta_z_err_low], [typical_delta_z_err_high]],
    yerr=[[typical_ew_err_low], [typical_ew_err_high]],
    fmt='o',
    ecolor='gray',
    capsize=5,
)

plt.axvline(0, color='gray', linestyle='--', label=r'$z_{MgII} = z_{galaxy}$')
plt.xlabel(r'$\Delta z = z_{Mg-II} - z_{galaxy}$')
plt.ylabel(r'Mg II 2803 Equivalent Width ($\AA$)')
plt.title(r'Mg II EW vs. $\Delta z$ (Transverse Distance <100 kpc)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
