import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging
from .parser import CriminalCodeParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CriminalCodeScraper:
    BASE_URL = "https://laws-lois.justice.gc.ca/eng/acts/c-46/FullText.html"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; CriminalCodeBot/1.0; +https://github.com/NobleBarnicle/app2.0)'
        })
    
    def fetch_page(self, url: Optional[str] = None) -> Optional[BeautifulSoup]:
        """Fetch and parse a page from the Criminal Code website."""
        try:
            url = url or self.BASE_URL
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except requests.RequestException as e:
            logger.error(f"Error fetching page {url}: {str(e)}")
            return None
    
    def extract_structure(self) -> dict:
        """Extract the basic structure of the Criminal Code."""
        soup = self.fetch_page()
        if not soup:
            return {}
        
        structure = {
            'title': self._extract_title(soup),
            'parts': self._extract_parts(soup)
        }
        return structure
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the title of the Criminal Code."""
        title_elem = soup.find('h1')
        return title_elem.text.strip() if title_elem else "Criminal Code"
    
    def _extract_parts(self, soup: BeautifulSoup) -> list:
        """Extract all parts of the Criminal Code."""
        parts = []
        parser = CriminalCodeParser()
        
        # Find all part elements in the document
        part_elements = soup.find_all('div', class_='part')
        
        # Parse each part using our existing parser
        for part_element in part_elements:
            part_data = parser.parse_part(part_element)
            if part_data:  # Only add if parsing was successful
                parts.append(part_data)
        
        return parts