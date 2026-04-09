import pandas as pd

def filter_concatenated_csvs_strip_units(filepath, target_column, max_value):
    df = pd.read_csv(filepath, on_bad_lines='skip')

    # Drop repeated header rows (where target column equals the header name
    df = df[df[target_column] != target_column]

    # Remove units, e.g. "850 kpc" -> "850"
    # This removes any non-numeric characters after the number, including spaces and units
    df[target_column] = df[target_column].astype(str).str.extract(r'([\d\.]+)', expand=False)

    # Convert to numeric, coercing errors to NaN
    df[target_column] = pd.to_numeric(df[target_column], errors='coerce')

    # Filter rows where target_column <= max_value
    filtered_df = df[df[target_column] <= max_value]

    return filtered_df.reset_index(drop=True)


filtered = filter_concatenated_csvs_strip_units("closepairsfinal.csv", target_column="comoving_transverse_distance", max_value=1000)
print(filtered)

outname = f'filteredmatches>100.csv'
pairs_df = pd.DataFrame(filtered, columns=['mgii_targetid', 'agnqso_targetid', 'angular_sep', 'z_mgii', 'z_agnqso', 'z_avg', 'proper_distance', 'comoving_transverse_distance'])
pairs_df.to_csv(outname, index=False)
print(f"{len(filtered)} matches saved to {outname}")
