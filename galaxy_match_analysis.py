import numpy as np
import pandas as pd


df = pd.read_csv('galaxy_matches.csv', low_memory=False)

sfr_cutoff = -3

base_mask = df[(df['LOGSFR'] <= sfr_cutoff) & (df['LOGM'] > 0)].values

# Define distance bins (kpc)
#distance_bins = [(0, 60), (60, 200), (200, 1000)]

# Store binned data
#binned = {}

#for dmin, dmax in distance_bins:
    #df_bin = df[
        #base_mask &
        #(df['comoving_transverse_distance'] >= dmin) &
        #(df['comoving_transverse_distance'] < dmax)
    #]
    
    #binned[(dmin, dmax)] = {
     #   "logm": df_bin['LOGM'].values,
     #   "logsfr": df_bin['LOGSFR'].values
    #}

    #print(f"{dmin}-{dmax} kpc: {len(df_bin)} galaxies")


print(f'There are {len(base_mask)} pairs with log sfr cutoff={sfr_cutoff}')
