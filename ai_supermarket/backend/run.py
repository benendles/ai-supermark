import pandas as pd
import os

# Path to your suppliers CSV
SUPPLIER_CSV = "data/simulated_transport.csv"

if not os.path.exists(SUPPLIER_CSV):
    raise FileNotFoundError(f"Could not find {SUPPLIER_CSV}")

# Read the existing suppliers CSV
df = pd.read_csv(SUPPLIER_CSV)

# Strip whitespace on column names just in case
df.columns = df.columns.str.strip()

# Create or overwrite a supply_id column with a sequential ID
df['supply_id'] = range(1, len(df) + 1)

# Save back to CSV (overwrite)
df.to_csv(SUPPLIER_CSV, index=False)

print(f"Added `supply_id` to {len(df)} suppliers.")
print(df.head())