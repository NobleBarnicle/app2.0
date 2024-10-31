import pytest
import json
from bs4 import BeautifulSoup
from unittest.mock import patch, Mock
from scripts.scrape_criminal_code import main

@pytest.fixture
def mock_html():
    return """
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
    """

@patch('app.scraper.scraper.CriminalCodeScraper.fetch_page')
def test_main_script(mock_fetch):
    # Setup mock
    mock_fetch.return_value = BeautifulSoup(mock_html(), 'lxml')
    
    # Run main function
    main()
    
    # Assert file was created with correct content
    with open('data/criminal_code.json', 'r') as f:
        data = json.load(f)
        assert data['title'] == 'Criminal Code'
        assert len(data['parts']) > 0
        assert data['parts'][0]['part_number'] == '1'