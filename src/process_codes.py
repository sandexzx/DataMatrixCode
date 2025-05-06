import pandas as pd
import os
from pylibdmtx.pylibdmtx import encode
from PIL import Image

def extract_codes():
    """Extract codes from Excel file and save them to output.txt"""
    print("Extracting codes from Excel file...")
    
    # Read the Excel file with more strict parameters
    df = pd.read_excel(
        'src/file-181f58e4-fa35-446d-9ebb-e75dcd0c726d.xlsx',
        skiprows=1,
        dtype=str,  # Force all columns to be read as strings
        na_filter=False  # Don't interpret empty cells as NaN
    )

    # Get the first column and clean the data
    first_column = df.iloc[:, 0].astype(str).str.strip()

    # Print total number of rows
    print(f"Total number of codes found: {len(first_column)}")

    # Save codes to output.txt, one per line
    with open('output.txt', 'w', encoding='utf-8') as f:
        for code in first_column:
            f.write(f"{code}\n")

    print("Codes have been successfully extracted to output.txt")
    return len(first_column)

def create_datamatrix_directory():
    """Create a directory for Data Matrix images if it doesn't exist."""
    if not os.path.exists('datamatrix_codes'):
        os.makedirs('datamatrix_codes')

def generate_datamatrix(code, filename):
    """Generate a Data Matrix code and save it as an image."""
    # Encode the data into a Data Matrix code
    encoded = encode(code.encode('utf-8'))
    
    # Convert to PIL Image
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    
    # Resize image to make it larger (optional)
    img = img.resize((encoded.width * 5, encoded.height * 5), Image.Resampling.NEAREST)
    
    # Save the image
    img.save(f'datamatrix_codes/{filename}.png')

def generate_datamatrix_codes():
    """Generate Data Matrix codes from the extracted codes"""
    print("\nGenerating Data Matrix codes...")
    
    # Create directory for Data Matrix codes
    create_datamatrix_directory()
    
    # Read codes from output.txt
    with open('output.txt', 'r', encoding='utf-8') as f:
        codes = [line.strip() for line in f if line.strip()]
    
    # Generate Data Matrix codes
    for i, code in enumerate(codes, 1):
        try:
            generate_datamatrix(code, f'code_{i:04d}')
            if i % 100 == 0:
                print(f"Processed {i} codes...")
        except Exception as e:
            print(f"Error generating code for {code}: {str(e)}")
    
    print("\nData Matrix codes have been generated in the 'datamatrix_codes' directory")

def main():
    # Step 1: Extract codes from Excel
    total_codes = extract_codes()
    
    # Step 2: Generate Data Matrix codes
    if total_codes > 0:
        generate_datamatrix_codes()
    else:
        print("No codes were extracted. Skipping Data Matrix generation.")

if __name__ == "__main__":
    main() 