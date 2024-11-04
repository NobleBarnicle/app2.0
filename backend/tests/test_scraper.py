import pytest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from app.scraper.scraper import CriminalCodeScraper
from app.scraper.models import CriminalCode

@pytest.fixture
def scraper():
    return CriminalCodeScraper()

def test_scraper_initialization(scraper):
    assert scraper.BASE_URL == "https://laws-lois.justice.gc.ca/eng/acts/c-46/FullText.html"
    assert 'User-Agent' in scraper.session.headers
    assert 'CriminalCodeBot' in scraper.session.headers['User-Agent']

@patch('requests.Session.get')
def test_fetch_page_success(mock_get, scraper):
    # Setup mock response
    mock_response = Mock()
    mock_response.text = "<html><body><h1>Criminal Code</h1></body></html>"
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    # Test the fetch
    result = scraper.fetch_page()
    assert result is not None
    assert isinstance(result, BeautifulSoup)
    assert result.find('h1').text == "Criminal Code"

@patch('requests.Session.get')
def test_fetch_page_failure(mock_get, scraper):
    # Setup mock to raise an exception
    mock_get.side_effect = Exception("Network error")
    
    # Test the fetch
    result = scraper.fetch_page()
    assert result is None

@patch('app.scraper.scraper.CriminalCodeScraper.fetch_page')
def test_fetch_and_parse_success(mock_fetch, scraper):
    # Setup mock response
    mock_fetch.return_value = BeautifulSoup("""
        <html>
            <h1 class="HeadTitle">Criminal Code</h1>
            <div class="part" id="part-1">
                <h2>Part I</h2>
            </div>
        </html>
    """, 'lxml')
    
    # Test the fetch and parse
    result = scraper.fetch_and_parse()
    assert isinstance(result, CriminalCode)
    assert result.title == "Criminal Code"

@patch('app.scraper.scraper.CriminalCodeScraper.fetch_page')
def test_fetch_and_parse_failure(mock_fetch, scraper):
    # Setup mock to return None
    mock_fetch.return_value = None
    
    # Test the fetch and parse
    result = scraper.fetch_and_parse()
    assert result is None