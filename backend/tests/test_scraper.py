import pytest, requests
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from app.scraper.scraper import CriminalCodeScraper
from app.scraper.models import CriminalCode, Part, Section  

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
    # Setup mock to raise a requests.RequestException instead of generic Exception
    mock_get.side_effect = requests.RequestException("Network error")
    
    # Test the fetch
    result = scraper.fetch_page()
    assert result is None

@patch('app.scraper.scraper.CriminalCodeScraper.fetch_page')
def test_fetch_and_parse_success(mock_fetch, scraper, example_sections):
    """Test successful fetch and parse workflow"""
    # Get base case example
    base_example = example_sections['Base Case Section']
    
    # Setup mock response with real structure from parsing_examples.md
    mock_fetch.return_value = BeautifulSoup(f"""
        <html>
            <head>
                <meta name="dcterms.title" content="Consolidated federal laws of Canada, Criminal Code" />
                <meta name="dcterms.creator" title="Department of Justice" content="Legislative Services Branch" />
                <meta name="dcterms.issued" title="W3CDTF" content="2024-01-14" />
                <meta name="dcterms.modified" title="W3CDTF" content="2024-01-14" />
                <meta name="dcterms.language" title="ISO639-2" content="eng" />
            </head>
            <body>
                <div class="part">
                    <h2 class="Part" id="h-115244"><span class="HTitleText1">Part I</span></h2>
                    <h3 class="Subheading" id="h-115245"><span class="HTitleText2">General</span></h3>
                    {base_example['html']}
                </div>
            </body>
        </html>
    """, 'lxml')
    
    # Test the fetch and parse
    result = scraper.fetch_and_parse()
    assert isinstance(result, CriminalCode)
    
    # Test metadata
    assert result.title == "Consolidated federal laws of Canada, Criminal Code"
    assert result.last_updated.strftime('%Y-%m-%d') == "2024-01-14"
    assert result.last_amended.strftime('%Y-%m-%d') == "2024-01-14"
    
    # Test part structure
    assert len(result.parts) == 1
    part = result.parts[0]
    assert isinstance(part, Part)
    assert part.id == "h-115244"
    assert part.number == "I"
    assert part.title == "Part I"
    assert part.subheading == "General"
    
    # Test section matches base example
    assert len(part.sections) == 1
    section = part.sections[0]
    assert isinstance(section, Section)
    assert section.id == "115611"
    assert section.number == "23.1"
    assert section.marginal_note.text == "Where one party cannot be convicted"
    assert section.text == "For greater certainty, sections 21 to 23 apply in respect of an accused notwithstanding the fact that the person whom the accused aids or abets, counsels or procures or receives, comforts or assists cannot be convicted of the offence."
    assert section.historical_notes[0].text == "R.S., 1985, c. 24 (2nd Supp.), s. 45"

@patch('app.scraper.scraper.CriminalCodeScraper.fetch_page')
def test_fetch_and_parse_failure(mock_fetch, scraper):
    """Test failed fetch and parse"""
    # Setup mock to return None (failed fetch)
    mock_fetch.return_value = None
    
    # Test the fetch and parse
    result = scraper.fetch_and_parse()
    assert result is None