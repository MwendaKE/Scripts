'''
Searches PDF documents for specific text and returns all matching paragraphs with clean formatting and error handling.
'''

import PyPDF2
import re
from pathlib import Path

class PDFTextSearcher:
    """Searches PDF files for specific text and returns matching paragraphs"""
    
    def __init__(self, pdf_path):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    def extract_text(self):
        """Extract all text from the PDF document"""
        text = ""
        
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                    
        except Exception as e:
            print(f"Error reading PDF: {e}")
            
        return text
    
    def search_text(self, search_term, case_sensitive=False):
        """
        Search for paragraphs containing the specified text
        
        Args:
            search_term: Text to search for
            case_sensitive: Whether search should be case sensitive (default: False)
            
        Returns:
            List of paragraphs containing the search term
        """
        full_text = self.extract_text()
        
        if not case_sensitive:
            search_term = search_term.lower()
            full_text = full_text.lower()
        
        # Split into paragraphs (handle different paragraph separators)
        paragraphs = re.split(r'\n\s*\n|\n', full_text)
        
        # Filter paragraphs containing the search term
        matching_paragraphs = [
            para.strip() for para in paragraphs 
            if search_term in para and para.strip()
        ]
        
        return matching_paragraphs


def main():
    # Configuration
    PDF_FILE = "./A-Better-Way-To-Pray.pdf"
    
    print("PDF Text Search Tool")
    print("====================")
    
    try:
        # Initialize searcher
        searcher = PDFTextSearcher(PDF_FILE)
        
        # Get search term from user
        search_term = input("\nEnter text to search: ").strip()
        
        if not search_term:
            print("Please enter a search term.")
            return
        
        # Perform search
        results = searcher.search_text(search_term)
        
        # Display results
        if results:
            print(f"\nFound {len(results)} matching paragraph(s):")
            print("=" * 60)
            
            for i, paragraph in enumerate(results, 1):
                print(f"\n{i}. {paragraph}")
                print("-" * 40)
        else:
            print("\nNo results found for your search term.")
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()