import pytest
from app.scraper.parser import parse_section

def test_parse_base_section(example_sections, get_example):
    # Get the example for this test
    example = get_example('test_parse_base_section', example_sections)
    
    # Parse the example HTML
    section = parse_section(example['html'])
    
    # Compare against expected components
    assert section.marginal_note.text == example['components']['Marginal Note'].strip('"')
    assert section.id == example['components']['Section ID'].strip('"')
    assert section.number == example['components']['Section Number'].strip('"')
    assert section.text == example['components']['Content'].strip('"')
    assert section.historical_notes[0].text == example['components']['Historical Note'].strip('"')