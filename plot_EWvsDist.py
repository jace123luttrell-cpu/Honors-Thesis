import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

# Load the file
dist_df = pd.read_csv("filteredmatches_100.csv")
dist_df['mgii_targetid'] = dist_df['mgii_targetid'].astype(str)

# Open FITS file with EW data
fits_filename = "MgII-Absorbers-DR1.fits"
with fits.open(fits_filename) as hdul:
    data = hdul[1].data
    

    mgii_ids = data['TARGETID'].byteswap().newbyteorder().astype(str)
    ew_2803 = data['EW_2803'].byteswap().newbyteorder()
    ew_2803_err_low = data['EW_2803_ERR_LOW'].byteswap().newbyteorder()
    ew_2803_err_high = data['EW_2803_ERR_HIGH'].byteswap().newbyteorder()
    
    ew_df = pd.DataFrame({
        'mgii_targetid': mgii_ids,
        'EW_2803': ew_2803,
        'EW_2803_ERR_LOW' : ew_2803_err_low,
        'EW_2803_ERR_HIGH' : ew_2803_err_high
    })
    
# Merge your two dataframes on mgii_targetid
merged_df = pd.merge(dist_df, ew_df, left_on='mgii_targetid', right_on='mgii_targetid', how='left')

# Drop rows missing EW or distance
merged_df = merged_df.dropna(subset=['EW_2803', 'comoving_transverse_distance'])

# Filter by distance range
dist_min = 0
dist_max = 100

filtered_df = merged_df[
    (merged_df['comoving_transverse_distance'] >= dist_min) &
    (merged_df['comoving_transverse_distance'] <= dist_max)
]

# Typical error
typical_ew_err_low = filtered_df['EW_2803_ERR_LOW'].mean()
typical_ew_err_high = filtered_df['EW_2803_ERR_HIGH'].mean()

# Plot
plt.errorbar(
    filtered_df['comoving_transverse_distance'],
    filtered_df['EW_2803'],
    yerr=[[typical_ew_err_low], [typical_ew_err_high]],
    fmt='o',
    ecolor='gray',
    capsize=5,
)

plt.xlim(dist_min, dist_max)
plt.ylim(0, 4)
plt.xlabel('Transverse Distance (kpc)')
plt.ylabel(r'Mg II 2803 Equivalent Width ($\AA$)')
plt.title(f'Mg II EW vs. Transverse Distance (<100 kpc)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
