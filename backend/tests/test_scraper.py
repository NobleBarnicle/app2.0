import pytest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from app.scraper.scraper import CriminalCodeScraper
from app.scraper.models import CriminalCode, Part, Section, MarginalNote

@pytest.fixture
def scraper():
    return CriminalCodeScraper()

def test_scraper_initialization(scraper):
    """Test basic scraper setup"""
    assert scraper.BASE_URL == "https://laws-lois.justice.gc.ca/eng/acts/c-46/FullText.html"
    assert 'User-Agent' in scraper.session.headers
    assert 'CriminalCodeBot' in scraper.session.headers['User-Agent']
    assert scraper.parser is not None

@patch('requests.Session.get')
def test_fetch_page_success(mock_get, scraper):
    """Test successful page fetch"""
    # Setup mock response with minimal valid HTML
    mock_response = Mock()
    mock_response.text = """
        <html>
            <head><title>Criminal Code</title></head>
            <body>
                <h1 class="HeadTitle">Criminal Code</h1>
                <div class="part">
                    <h2>Part I</h2>
                    <p class="Section">Test Section</p>
                </div>
            </body>
        </html>
    """
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    # Test the fetch
    result = scraper.fetch_page()
    assert result is not None
    assert isinstance(result, BeautifulSoup)
    assert result.find('h1', class_='HeadTitle').text == "Criminal Code"

@patch('requests.Session.get')
def test_fetch_page_failure(mock_get, scraper):
    """Test failed page fetch"""
    # Setup mock to raise an exception
    mock_get.side_effect = Exception("Network error")
    
    # Test the fetch
    result = scraper.fetch_page()
    assert result is None

@patch('app.scraper.scraper.CriminalCodeScraper.fetch_page')
def test_fetch_and_parse_success(mock_fetch, scraper, example_sections):
    """Test successful fetch and parse workflow"""
    # Get base case example
    base_example = example_sections['Base Case Section']
    
    # Setup mock response with real structure
    mock_fetch.return_value = BeautifulSoup(f"""
        <html>
            <head>
                <meta name="dcterms.modified" content="2024-01-14" />
                <meta name="dcterms.issued" content="2024-01-14" />
            </head>
            <body>
                <h1 class="HeadTitle">Criminal Code</h1>
                <div class="part" id="part-1">
                    <h2><span class="HTitleText1">Part I</span></h2>
                    <h3 class="Subheading"><span class="HTitleText2">General</span></h3>
                    {base_example['html']}
                </div>
            </body>
        </html>
    """, 'lxml')
    
    # Test the fetch and parse
    result = scraper.fetch_and_parse()
    assert isinstance(result, CriminalCode)
    assert result.title == "Criminal Code"
    assert len(result.parts) > 0
    assert isinstance(result.parts[0], Part)
    assert len(result.parts[0].sections) > 0
    
    # Test section content matches example
    section = result.parts[0].sections[0]
    assert isinstance(section, Section)
    assert section.id == base_example['components']['Section ID'].split('"')[1]
    assert section.number == base_example['components']['Section Number'].split('"')[1]
    assert section.text == base_example['components']['Content'].split('"')[1]

@patch('app.scraper.scraper.CriminalCodeScraper.fetch_page')
def test_fetch_and_parse_failure(mock_fetch, scraper):
    """Test failed fetch and parse"""
    # Setup mock to return None (failed fetch)
    mock_fetch.return_value = None
    
    # Test the fetch and parse
    result = scraper.fetch_and_parse()
    assert result is None