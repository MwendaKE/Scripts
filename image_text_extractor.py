'''
Extracts text from images using OCR with image preprocessing for 
better accuracy and offers text cleaning and file saving options.
'''

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import sys
import re
from pathlib import Path

class ImageTextExtractor:
    """Extracts text from images using OCR with optional image preprocessing"""
    
    def __init__(self):
        # Check if Tesseract is available
        try:
            pytesseract.get_tesseract_version()
        except pytesseract.TesseractNotFoundError:
            print("Error: Tesseract OCR is not installed or not in your PATH")
            print("Please install it from: https://github.com/tesseract-ocr/tesseract")
            sys.exit(1)
    
    def preprocess_image(self, image_path):
        """Enhance image to improve OCR accuracy"""
        try:
            image = Image.open(image_path)
            
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            # Apply slight blur to reduce noise
            image = image.filter(ImageFilter.MedianFilter())
            
            return image
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return Image.open(image_path)  # Return original if preprocessing fails
    
    def extract_text(self, image_path, preprocess=True):
        """Extract text from image using OCR"""
        try:
            if preprocess:
                image = self.preprocess_image(image_path)
            else:
                image = Image.open(image_path)
            
            # Use Tesseract to extract text
            text = pytesseract.image_to_string(image)
            
            # Clean up extracted text
            text = self.clean_text(text)
            
            return text
            
        except Exception as e:
            print(f"Error extracting text: {e}")
            return None
    
    def clean_text(self, text):
        """Clean and format extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common OCR errors
        replacements = {
            r'\b([Il1])\b': 'I',  # Common confusion between I, l, 1
            r'\b([O0])\b': 'O',   # Common confusion between O and 0
        }
        
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text)
        
        return text.strip()
    
    def save_text_to_file(self, text, output_path):
        """Save extracted text to a file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return True
        except Exception as e:
            print(f"Error saving text to file: {e}")
            return False
    
    def run(self):
        """Main method to run the text extraction interface"""
        print("Image Text Extractor")
        print("====================")
        print("Type 'quit' or 'q' to exit\n")
        
        while True:
            try:
                # Get image path from user
                image_path = input("Enter full path to image file: ").strip()
                
                # Check for exit command
                if re.match(r'^(q|quit)$', image_path, re.I):
                    print("Goodbye!")
                    break
                
                # Validate path
                image_file = Path(image_path)
                if not image_file.exists() or not image_file.is_file():
                    print("Error: File does not exist or is not a valid file!")
                    continue
                
                # Check if file is an image
                try:
                    Image.open(image_file)  # Try to open as image
                except:
                    print("Error: File is not a valid image format!")
                    continue
                
                # Ask about preprocessing
                preprocess = input("Preprocess image for better accuracy? (y/n): ").lower() == 'y'
                
                # Extract text
                print("\nExtracting text...")
                text = self.extract_text(image_file, preprocess)
                
                if text:
                    # Display results
                    print("\n" + "=" * 50)
                    print("EXTRACTED TEXT:")
                    print("=" * 50)
                    print(text)
                    print("=" * 50)
                    
                    # Ask to save to file
                    save = input("\nSave to text file? (y/n): ").lower() == 'y'
                    if save:
                        output_name = input("Enter output filename (or press Enter for default): ").strip()
                        if not output_name:
                            output_name = f"{image_file.stem}_extracted.txt"
                        
                        if self.save_text_to_file(text, output_name):
                            print(f"Text saved to: {output_name}")
                
                else:
                    print("No text could be extracted from the image.")
                
                print()  # Empty line for spacing
                
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")


# Run the application
if __name__ == "__main__":
    extractor = ImageTextExtractor()
    extractor.run()

'''
INSIGHT: To read text from an image using Python, 
you [can] use Optical Character Recognition (OCR). 
The most popular library for this task is Tesseract 
along with the Python wrapper Pytesseract.

With Tesseract and Pytesseract, you can easily 
extract text from images using Python. It works well 
for images with clear, high-contrast text, but for 
complex images, some preprocessing might be needed 
to improve accuracy.
'''