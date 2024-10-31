import pytest
from app.scraper.scraper import CriminalCodeScraper
from unittest.mock import patch
from bs4 import BeautifulSoup

@pytest.fixture
def scraper():
    return CriminalCodeScraper()

def test_scraper_initialization(scraper):
    assert scraper.BASE_URL == "https://laws-lois.justice.gc.ca/eng/acts/c-46/FullText.html"
    assert 'User-Agent' in scraper.session.headers

@patch('requests.Session.get')
def test_fetch_page(mock_get, scraper):
    mock_get.return_value.text = "<html><body><h1>Criminal Code</h1></body></html>"
    mock_get.return_value.status_code = 200
    
    soup = scraper.fetch_page()
    assert soup is not None
    assert soup.find('h1').text == "Criminal Code" 

def test_extract_parts(scraper):
    html = """
    <html>
        <body>
            <div class="part" id="part-1">
                <h2>PART I - General</h2>
                <div class="section" id="section-1">
                    <h3>Definitions</h3>
                    <div class="provision">In this Act,</div>
                    <div class="subsection" id="subsection-1">
                        "Act" includes...
                    </div>
                </div>
            </div>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, 'lxml')
    parts = scraper._extract_parts(soup)
    
    assert len(parts) == 1
    assert parts[0]['part_number'] == '1'
    assert parts[0]['title'] == 'PART I - General'
    assert len(parts[0]['sections']) == 1