from dl import queryClient as qc
query = """
SELECT targetid, target_ra, target_dec, z, program, spectype, mgii_2796_flux, mgii_2796_flux_ivar,
mgii_2796_sigma, mgii_2803_flux, mgii_2803_flux_ivar, mgii_2803_sigma
FROM desi_dr1.agnqso
WHERE z BETWEEN 0.3 AND 0.4
AND spectype = 'GALAXY'
"""

result = qc.query(sql=query, fmt='pandas')
#print(len(result))
print(result)

#result.to_csv("filtered_agnqso.csv", index=False)
#print("Results saved to filtered_agnqso.csv")
