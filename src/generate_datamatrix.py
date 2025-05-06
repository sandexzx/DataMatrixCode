import os
from pylibdmtx.pylibdmtx import encode
from PIL import Image

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

def main():
    # Create directory for Data Matrix codes
    create_datamatrix_directory()
    
    # Read codes from output.txt
    with open('output.txt', 'r', encoding='utf-8') as f:
        codes = [line.strip() for line in f if line.strip()]
    
    print(f"Generating Data Matrix codes for {len(codes)} items...")
    
    # Generate Data Matrix codes
    for i, code in enumerate(codes, 1):
        try:
            generate_datamatrix(code, f'code_{i:04d}')
            if i % 100 == 0:
                print(f"Processed {i} codes...")
        except Exception as e:
            print(f"Error generating code for {code}: {str(e)}")
    
    print("\nData Matrix codes have been generated in the 'datamatrix_codes' directory")

if __name__ == "__main__":
    main() 