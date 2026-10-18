import pandas as pd

print("Reading CSV (this might take a few seconds)...")
df = pd.read_csv("Expression_Data_subset.csv", index_col=0)

print("Converting to Parquet...")
df.to_parquet("Expression_Data.parquet")

print("Success! Expression_Data.parquet has been created.")
