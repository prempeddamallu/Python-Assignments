import sys
import requests
from bs4 import BeautifulSoup

def fetch_and_strip_html(url):
    try:
        # Download HTML content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract and return text without HTML tags
        return soup.get_text()
    
    except requests.RequestException as e:
        return f"Error fetching URL: {e}"
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python anti_html.py <URL>")
    
    else:
        url = sys.argv[1]
        cleaned_text = fetch_and_strip_html(url)
        print(cleaned_text)
