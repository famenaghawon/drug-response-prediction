import pandas as pd
import os

# --- 1. Load Target Cell Lines ---
print("Loading drug response data...")
resp_path = "data/raw/GDSC2_fitted_dose_response_27Oct23.xlsx"
df_resp = pd.read_excel(resp_path)
target_cell_lines = set(df_resp['CELL_LINE_NAME'].astype(str).str.strip().unique())
print(f"Target cell lines: {len(target_cell_lines)}")

# --- 2. Filter the Large CSV ---
input_path = "data/raw/Expression_Data.csv"
output_path = "data/raw/Expression_Data_subset.csv"

print("Filtering 6GB RNA-seq file in chunks (this will take a few minutes)...")
chunk_size = 1000000  # Read 1 million rows at a time
filtered_chunks = []

# We only need gene_symbol, model_name, and rsem_tpm
cols_to_use = ['model_name', 'gene_symbol', 'rsem_tpm']

for i, chunk in enumerate(pd.read_csv(input_path, chunksize=chunk_size, usecols=cols_to_use)):
    # Filter only rows where model_name is in our target list
    filtered = chunk[chunk['model_name'].astype(str).str.strip().isin(target_cell_lines)]
    if not filtered.empty:
        filtered_chunks.append(filtered)
    print(f"  Processed chunk {i+1}... found {len(filtered)} matching rows.")

print("Concatenating filtered data...")
df_long = pd.concat(filtered_chunks, ignore_index=True)
print(f"Total matching rows: {len(df_long)}")

# --- 3. Pivot to Wide Format ---
print("Pivoting to matrix format (Genes as rows, Cell Lines as columns)...")
df_wide = df_long.pivot_table(index='gene_symbol', columns='model_name', values='rsem_tpm', aggfunc='mean')

# Fill any missing values with 0
df_wide = df_wide.fillna(0)

# Save
print(f"Saving to {output_path}...")
df_wide.to_csv(output_path)
print(f"✅ Success! Subset shape: {df_wide.shape} (Genes x Cell Lines)")
