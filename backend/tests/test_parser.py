import pytest
from app.scraper.parser import CriminalCodeParser
from bs4 import BeautifulSoup

@pytest.fixture
def parser():
    return CriminalCodeParser()

def test_parse_section(parser):
    html = """
    <div class="section" id="section-1">
        <h3>Murder</h3>
        <div class="provision">
            First degree murder is murder that is planned and deliberate.
        </div>
        <div class="subsection" id="subsection-1">
            Details about first degree murder.
        </div>
    </div>
    """
    soup = BeautifulSoup(html, 'lxml')
    result = parser.parse_section(soup)
    
    assert result['section_number'] == '1'
    assert result['title'] == 'Murder'
    assert 'planned and deliberate' in result['content']
    assert len(result['subsections']) == 1 