MgIIcatalog_v4.py is the script to collect all the Mg-II absorption systems from the value added catalog "MgII-Absorbers-DR1.fits" and filter them by redshift only keeping the ones with 0.3 <= z <= 0.4.

sql-query.py does the same as MgIIcatalog_v4.py but instead it sorts through the galaxies in the DESI main survey and it has to do this via a SQL query, I just wrote it in Python because I'm new to code.

masterlist_v6.py is the latest iteration of the code I used to combine the data from the the previous two codes and calculate the separation between each pair of Mg-II absorption systems and galaxies. It uses an astropy function to  accomplish this.

All of the plotting scripts uses the final list of galaxy-absorber pairs constructed using the masterlist_v6.py script. They construct different plots based on different physical properties of the galaxy-absorber pairs looking for correlations that we believe should line up with our current understanding of galaxy evolution.

main_sequence_plot.py has three parts, the first part uses another value added catalog of the physical properties of the galaxies in the DESI main survey to plot the logarithm of the star formation rate of the galaxy versus the logarithm of the stellar mass of the galaxy. This creates what's called the main sequence plot that we care about. The other two parts are two theoretical main sequence lines for galaxies at the redshift we look at in the paper. These come from Speagle et al from 2014 and Popesso et al from 2023.
