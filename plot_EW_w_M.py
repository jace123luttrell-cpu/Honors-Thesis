import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr, ks_2samp

# Load the file
m_df = pd.read_csv("galaxy_matches.csv", dtype={'mgii_targetid': 'Int64'})
m_df = m_df.dropna(subset=['mgii_targetid'])
m_df['mgii_targetid'] = m_df['mgii_targetid'].astype(str)

# Open FITS file with EW data
fits_filename = "MgII-Absorbers-DR1.fits"
with fits.open(fits_filename) as hdul:
    data = hdul[1].data
    

    mgii_ids = data['TARGETID'].byteswap().newbyteorder().astype('int64').astype(str)
    ew_2803 = data['EW_2803'].byteswap().newbyteorder()
    ew_err_low = data['EW_2803_ERR_LOW'].byteswap().newbyteorder()
    ew_err_high = data['EW_2803_ERR_HIGH'].byteswap().newbyteorder()
    
    ew_df = pd.DataFrame({
        'mgii_targetid': mgii_ids,
        'EW_2803': ew_2803,
        'EW_2803_ERR_LOW' : ew_err_low,
        'EW_2803_ERR_HIGH' : ew_err_high
    })
    
# Merge your two dataframes on mgii_targetid
merged_df = pd.merge(m_df, ew_df, left_on='mgii_targetid', right_on='mgii_targetid', how='left')

# Drop rows missing EW or logSFR
merged_df = merged_df.dropna(subset=['EW_2803', 'LOGM'])

# Base mask on SFR_ERR
merged_df = merged_df[(merged_df['LOGM'] > 0) & (merged_df['LOGM_ERR']<1)]

# Filter by distance range
dist_min = 0
dist_max = 40

filtered_df = merged_df[
    (merged_df['comoving_transverse_distance'] >= dist_min) &
    (merged_df['comoving_transverse_distance'] <= dist_max)
]

# Typical ew error
typical_ew_err_low = filtered_df['EW_2803_ERR_LOW'].mean()
typical_ew_err_high = filtered_df['EW_2803_ERR_HIGH'].mean()

# Typical m error
typical_m_err = filtered_df['LOGM_ERR'].mean()

# Pearson correlation test
#r_value, p_value = pearsonr(
#    filtered_df['LOGM'],
#    filtered_df['EW_2803']
#)

#print(f"Pearson r = {r_value:.3f}")
#print(f"p-value = {p_value:.3e}")

# Two-sample K-S Test

#near = filtered_df[filtered_df['comoving_transverse_distance'] < 40]['EW_2803']
#far  = filtered_df[filtered_df['comoving_transverse_distance'] >= 40]['EW_2803']

#ks_stat, ks_p = ks_2samp(near, far)

#print(f"KS statistic = {ks_stat:.3f}")
#print(f"KS p-value = {ks_p:.3e}")

y_errors = np.array([filtered_df['EW_2803_ERR_LOW'], filtered_df['EW_2803_ERR_HIGH']])

# Plot
plt.errorbar(
    filtered_df['LOGM'],
    filtered_df['EW_2803'],
    xerr=filtered_df['LOGM_ERR'],
    yerr=y_errors,
    fmt='o',
    ecolor='gray',
    capsize=5,
    label=f'Mean EW Err: +{typical_ew_err_high:.2f} / -{typical_ew_err_low:.2f} $\\AA$\n'
          f'Mean Mass Err: $\\pm${typical_m_err:.2f}'
)

plt.ylim(0, 4)
plt.xlabel(r'log M* ($M_\odot$)')
plt.ylabel(r'Mg II 2803 Equivalent Width ($\AA$)')
plt.title(f'Mg II EW vs log M* (<{dist_max} kpc)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
