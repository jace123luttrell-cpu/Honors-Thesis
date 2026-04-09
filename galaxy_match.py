import pandas as pd

agnqso = pd.read_csv('filteredmatches_1000.csv', low_memory=False)
gal_phys_prop = pd.read_csv('filtered_galaxy_physical_properties.csv')
print(agnqso.dtypes)
print(gal_phys_prop.dtypes)

matched_galaxies=pd.merge(agnqso,gal_phys_prop,how='inner', on='agnqso_targetid')

# Save to CSV
matched_galaxies.to_csv("galaxy_matches.csv", index=False)

print("Exported filtered results to galaxy_matches.csv")
