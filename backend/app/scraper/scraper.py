import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging
from .parser import CriminalCodeParser
from .models import CriminalCode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CriminalCodeScraper:
    BASE_URL = "https://laws-lois.justice.gc.ca/eng/acts/c-46/FullText.html"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; CriminalCodeBot/1.0; +https://github.com/NobleBarnicle/app2.0)'
        })
        self.parser = CriminalCodeParser()
    
    def fetch_and_parse(self) -> Optional[CriminalCode]:
        """Fetch and parse the Criminal Code into a structured object"""
        html_content = self.fetch_page()
        if not html_content:
            return None
            
        try:
            return self.parser.parse_html(str(html_content))
        except Exception as e:
            logger.error(f"Error parsing Criminal Code: {str(e)}")
            return None
    
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