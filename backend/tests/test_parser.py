import pytest
from bs4 import BeautifulSoup
from app.scraper.parser import CriminalCodeParser
from app.scraper.models import Part

def test_parse_base_section(example_sections, get_example):
    # Get the example for this test
    example = get_example('test_parse_base_section', example_sections)
    
    # Create parser instance
    parser = CriminalCodeParser()
    
    # Convert HTML string to BeautifulSoup Tag
    soup = BeautifulSoup(example['html'], 'html.parser')
    section_elem = soup.find('p', class_='Section')
    
    # Parse the section using existing parser method
    section = parser._parse_section(section_elem)
    
    # Debug - print raw values
    print("\nMarginal Note from parser:", section.marginal_note.text)
    print("Marginal Note from example:", example['components']['Marginal Note'])
    
    # Extract just the quoted text from the example component
    expected_text = example['components']['Marginal Note']
    expected_text = expected_text.split('"')[1] if '"' in expected_text else expected_text
    
    # Compare against expected components
    assert section.marginal_note.text == expected_text
    assert section.id == example['components']['Section ID'].split('"')[1]
    assert section.number == example['components']['Section Number'].split('"')[1]
    assert section.text == example['components']['Content'].split('"')[1]
    assert section.historical_notes[0].text == example['components']['Historical Note'].split('"')[1]