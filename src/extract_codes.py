import pandas as pd

# Read the Excel file with more strict parameters
df = pd.read_excel(
    'src/file-181f58e4-fa35-446d-9ebb-e75dcd0c726d.xlsx',
    skiprows=1,
    dtype=str,  # Force all columns to be read as strings
    na_filter=False  # Don't interpret empty cells as NaN
)

# Get the first column and clean the data
first_column = df.iloc[:, 0].astype(str).str.strip()

# Print first 10 values and their types for debugging
print("First 10 values and their types:")
for i, value in enumerate(first_column[:10]):
    print(f"Row {i+1}: {value} (Type: {type(value)})")

# Print total number of rows
print(f"\nTotal number of rows: {len(first_column)}")

# Save codes to output.txt, one per line
with open('output.txt', 'w', encoding='utf-8') as f:
    for code in first_column:
        f.write(f"{code}\n")

print("\nCodes have been successfully extracted to output.txt") 