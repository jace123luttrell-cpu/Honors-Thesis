import numpy as np
import matplotlib.pyplot as plt
from astropy.cosmology import Planck18 as cosmo
from astropy.coordinates import SkyCoord
import astropy.units as u
import pandas as pds
import time
import sys

# === Configurable chunk size ===
chunk_size = 136197
index = int(sys.argv[1])  # Passed in as an argument like: python3 script.py 0
start_row = chunk_size * index

## === Load MgII data ===
df = pds.read_csv('filtered_mgii_absorbers.csv')
df.columns = df.columns.str.strip()
df = df.dropna(subset=['Z_MGII', 'TARGETID', 'RA', 'DEC']).reset_index(drop=True)

z1_arr = df['Z_MGII'].values
ra1_arr = df['RA'].values
dec1_arr = df['DEC'].values

# === Load AGN/QSO data chunk ===
filename = 'filtered_agnqso.csv'
skip_indices = list(range(1, start_row + 1))  # Skip header + previous rows

try:
    df2 = pds.read_csv(filename, low_memory=False, skiprows=skip_indices, nrows=chunk_size)
except pds.errors.EmptyDataError:
    print(f"[{index}] No data returned after skipping rows")
    sys.exit()

df2.columns = df2.columns.str.strip()

# Check for required columns
required_cols = ['z', 'targetid', 'target_ra', 'target_dec']
for col in required_cols:
    if col not in df2.columns:
        print(f"[{index}] Missing column: {col}")
        print(f"Columns present: {df2.columns.tolist()}")
        sys.exit()

df2 = df2.dropna(subset=required_cols).reset_index(drop=True)

#df2 = df2.sample(n=500).reset_index(drop=True)

z2_arr = df2['z'].values
ra2_arr = df2['target_ra'].values
dec2_arr = df2['target_dec'].values

start_time = time.time()

# === Astropy coordinate & distance setup ===
coords1 = SkyCoord(ra=ra1_arr * u.deg, dec=dec1_arr * u.deg)
coords2 = SkyCoord(ra=ra2_arr * u.deg, dec=dec2_arr * u.deg)

# === Loop through all combinations and compute separations ===
close_pairs_guess = []
dist = []

for i2, (z2, coord2) in enumerate(zip(z2_arr, coords2)):
    for i1, (z1, coord1) in enumerate(zip(z1_arr, coords1)):

        del_z = abs(z1 - z2)
        if del_z > 0.007:
           continue

        # Angular separation (radians)
        theta = coord1.separation(coord2).radian
        if theta > 0.005:
         continue

        # Transverse distance
        z_avg = (z1 + z2) / 2
        D_M = cosmo.angular_diameter_distance(z_avg).to(u.kpc)
        D_xy = theta * D_M
#        print(D_M, theta, D_xy)

        pd = D_M / (1 + z_avg)
#        print(pd)
#        break

#        if D_M <= 1000 * u.kpc:
        id1 = df.iloc[i1]['TARGETID']
        id2 = df2.iloc[i2]['targetid']
        close_pairs_guess.append((id1, id2, theta, z1, z2, z_avg, pd, D_xy,))
#        print(close_pairs_guess)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"{elapsed_time:.6f} seconds")

#        dist.append(pd.value if hasattr(pd, 'value') else pd)  # Ensure pd is a number
# === Save close pairs ===
outname = f'close_pairs_guess_{index}.csv'
pairs_df = pds.DataFrame(close_pairs_guess, columns=['mgii_targetid', 'agnqso_targetid', 'angular_sep', 'z_mgii', 'z_agnqso', 'z_avg', 'proper_distance', 'comoving_transverse_distance'])
pairs_df.to_csv(outname, index=False)
print(f"[{index}] {len(close_pairs_guess)} close pairs saved to {outname}")

