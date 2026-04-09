import numpy
from astropy.cosmology import WMAP9 as cosmo
import matplotlib.pyplot as plt
import pandas as pd

# Load data
df_all = pd.read_csv('galaxy_matches.csv', low_memory=False)

# Base quality cut (apply once)
base_mask = (df_all['LOGM'] > 0) & (df_all['LOGSFR_ERR'] < 1)

# Define distance bins (kpc)
distance_bins = [(0, 60), (60, 200), (200, 1000)]

# Store binned data
binned = {}

for dmin, dmax in distance_bins:
    df_bin = df_all[
        base_mask &
        (df_all['comoving_transverse_distance'] >= dmin) &
        (df_all['comoving_transverse_distance'] < dmax)
    ]
    
    binned[(dmin, dmax)] = {
        "logm": df_bin['LOGM'].values,
        "logsfr": df_bin['LOGSFR'].values,
        "logm_err": df_bin['LOGM_ERR'].values,
        "logsfr_err": df_bin['LOGSFR_ERR'].values,
    }
    

    print(f"{dmin}-{dmax} kpc: {len(df_bin)} galaxies")
    
# draw speagle main sequence
logMstar_array = [7.7,7.9,8.1,8.3,8.5,8.7,8.9,9.1,9.3,9.5,9.7,9.9,10.1,10.3,10.5,10.7,10.9,11.1,11.3,11.5,11.7,11.9,12.1]
redshift_array = [0.4]

for redshift in redshift_array:
    logSFR_array = []
    logsSFR_array = []
    #print("redshift=",redshift)
    age_at_z = cosmo.age(redshift)
    slope = 0.84 - 0.026 * age_at_z.value
    intercept = -6.51 + 0.11 * age_at_z.value
    #print("slope=",slope,"intercept=",intercept)
    #print("age_at_z=",redshift,"= ",age_at_z)
    age_in_Gyears = age_at_z.value 
    #print("printing logM*,logSFR:")
#   logSFR vs. logM*:
    for logMstar in logMstar_array:
        logSFR = slope*logMstar + intercept
        logSFR_array.append(logSFR)
        #print("logMstar,logSFR=",logMstar,logSFR)
#   logsSFR vs. logM*:
    for logMstar in logMstar_array:
        new_slope = slope - 1
        logsSFR = new_slope*logMstar + intercept
        logsSFR_array.append(logsSFR)
        #print("printing logM*,logsSFR:")
        #print("logM*,logsSFR=",logMstar,logsSFR)
        
a0 = 2.693
a1 = -0.186
a2 = 10.85
a3 = -0.0729
a4 = 0.99
        
logMstar_array2 = [7.7,7.9,8.1,8.3,8.5,8.7,8.9,9.1,9.3,9.5,9.7,9.9,10.1,10.3,10.5,10.7,10.9,11.1,11.3,11.5,11.7,11.9,12.1]
redshift_array2 = [0.3]

for redshift2 in redshift_array2:
    logSFR_array2 = [ ]
    logsSFR_array2 = [ ]
    #print("redshift=",redshift)
    age_at_z_2 = cosmo.age(redshift2)
    #print("age_at_z=",redshift,"= ",age_at_z)
    age_in_Gyears_2 = age_at_z_2.value 
    for logMstar2 in logMstar_array2:
        logSFR2 = (a0 + a1*age_in_Gyears_2) - numpy.log10(1 + ((10.0**logMstar2)/10.0**(a2+a3*age_in_Gyears_2))**(-1.0*a4))
        logSFR_array2.append(logSFR2)
        logsSFR2 = logSFR2 - logMstar2
        logsSFR_array2.append(logsSFR2)
        

fig, axes = plt.subplots(1, len(binned), figsize=(18,6), sharey=True)

for ax, ((dmin, dmax), data) in zip(axes, binned.items()):
    # Scatter points for this bin
    ax.errorbar(
       data["logm"],
       data["logsfr"],
       xerr=data["logm_err"],
       yerr=data["logsfr_err"],
       fmt='o',
       markersize=6,
       markeredgecolor='k',
       markerfacecolor='C0',
       ecolor='gray',
       alpha=0.7,
       capsize=3
    )
    
    # Overplot Speagle and Popesso lines
    ax.plot(
        logMstar_array, logSFR_array,
        color='black',
        linestyle='--',
        linewidth=2,
        label='Speagle et al (2014)'
    )
    ax.plot(
        logMstar_array2, logSFR_array2,
        color='black',
        linestyle='dotted',
        linewidth=2,
        label='Popesso et al (2023)'
    )

    # Titles and axis labels
    ax.set_title(f"{dmin}-{dmax} kpc")
    ax.set_xlabel(r'log M* ($M_\odot$)')

    # Legend in each subplot
    ax.legend()

# Only set ylabel on the first subplot
axes[0].set_ylabel(r'log SFR ($M_{\odot}\,yr^{-1}$)')

fig.tight_layout()
plt.show()
