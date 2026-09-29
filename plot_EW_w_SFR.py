import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr, ks_2samp

# Load the file
sfr_df = pd.read_csv("galaxy_matches.csv", dtype={'mgii_targetid': 'Int64'})
sfr_df = sfr_df.dropna(subset=['mgii_targetid'])
sfr_df['mgii_targetid'] = sfr_df['mgii_targetid'].astype(str)

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
merged_df = pd.merge(sfr_df, ew_df, left_on='mgii_targetid', right_on='mgii_targetid', how='left')

# Drop rows missing EW or logSFR
merged_df = merged_df.dropna(subset=['EW_2803', 'LOGSFR'])

# Base mask on SFR_ERR
merged_df = merged_df[merged_df['LOGSFR_ERR'] < 0.5]

print("Distance stats:\n", merged_df['comoving_transverse_distance'].describe())

# Filter by distance range
dist_min = 0
dist_max = 40

filtered_df = merged_df[
    (merged_df['comoving_transverse_distance'] >= dist_min) &
    (merged_df['comoving_transverse_distance'] <= dist_max)
]

# Check initial sizes
print(f"Rows in CSV: {len(sfr_df)}")
print(f"Rows in FITS: {len(ew_df)}")

# Check ID formatting samples
print(f"Sample CSV ID: {repr(sfr_df['mgii_targetid'].iloc[0])}")
print(f"Sample FITS ID: {repr(ew_df['mgii_targetid'].iloc[0])}")

# 1. Test the Merge
merged_df = pd.merge(sfr_df, ew_df, on='mgii_targetid', how='inner') # Switch to inner to see matches
print(f"Rows after INNER merge: {len(merged_df)}")

if len(merged_df) == 0:
    print("❌ ERROR: Merge failed completely. The IDs do not match exactly. Check for whitespace differences.")
    # Try stripping whitespace if they look like strings:
    # ew_df['mgii_targetid'] = ew_df['mgii_targetid'].str.strip()

# 2. Test Dropna
dropped_df = merged_df.dropna(subset=['EW_2803', 'LOGSFR'])
print(f"Rows after dropna: {len(dropped_df)}")

# 3. Test Distance Filter
final_filtered = dropped_df[
    (dropped_df['comoving_transverse_distance'] >= 0) & 
    (dropped_df['comoving_transverse_distance'] <= 40)
]
print(f"Rows after distance filter (<40): {len(final_filtered)}")

# Typical ew error
typical_ew_err_low = filtered_df['EW_2803_ERR_LOW'].mean()
typical_ew_err_high = filtered_df['EW_2803_ERR_HIGH'].mean()

# Typical sfr error
typical_sfr_err = filtered_df['LOGSFR_ERR'].mean()

# Pearson correlation test
#r_value, p_value = pearsonr(
#    filtered_df['LOGSFR'],
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
    filtered_df['LOGSFR'],
    filtered_df['EW_2803'],
    xerr=filtered_df['LOGSFR_ERR'],
    yerr=y_errors,
    fmt='o',
    ecolor='gray',
    capsize=5,
    label=f'Mean EW Err: +{typical_ew_err_high:.2f} / -{typical_ew_err_low:.2f} $\\AA$\n'
          f'Mean SFR Err: $\\pm${typical_sfr_err:.2f}'
)

plt.ylim(0, 4)
plt.xlabel(r'log SFR ($M_{\odot}\,yr^{-1}$)')
plt.ylabel(r'Mg II 2803 Equivalent Width ($\AA$)')
plt.title(f'Mg II EW vs log SFR (<{dist_max} kpc)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
