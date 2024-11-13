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

def test_parse_part(example_sections, get_example):
    """Test parsing a Part with optional subheadings"""
    # Get the example for this test
    example = get_example('test_parse_part', example_sections)
    
    # Create parser instance
    parser = CriminalCodeParser()
    
    # Convert HTML string to BeautifulSoup Tag
    soup = BeautifulSoup(example['html'], 'html.parser')
    part_elem = soup.find('h2', class_='Part')
    
    # Parse the part using parser method
    part = parser._parse_part(part_elem)
    
    # Verify the parsed Part object
    assert isinstance(part, Part)
    assert part.number == example['components']['Title'].split()[1]  # "Part I" -> "I"
    assert part.id == example['components']['IDs']['Part ID'].split('"')[1]
    
    # If there's a subheading, verify it
    if 'Subheading' in example['components']:
        assert part.subheading.text == example['components']['Subheading'].split('"')[1]
        assert part.subheading.id == example['components']['IDs']['Subheading ID'].split('"')[1]

def test_parse_section_with_subsection_definitions(example_sections, get_example):
    """Test parsing a section with subsections containing inline definitions"""
    # Get the example for this test
    example = get_example('test_parse_section_with_subsection_definitions', example_sections)
    
    # Create parser instance
    parser = CriminalCodeParser()
    
    # Convert HTML string to BeautifulSoup Tag
    soup = BeautifulSoup(example['html'], 'html.parser')
    section_elem = soup.find('ul', class_='Section')
    
    # Parse the section
    section = parser._parse_section(section_elem)
    
    # Verify base section properties
    assert section.marginal_note.text == "Sabotage"
    assert section.number == "52"
    assert section.id == "115955"
    
    # Verify subsections
    assert len(section.subsections) == 5
    
    # Check first subsection (1) and its nested structure
    sub1 = section.subsections[0]
    assert sub1.number == "(1)"
    assert sub1.id == "115957"
    assert "Every person is guilty of an indictable offence" in sub1.text
    assert "who does a prohibited act with the intent to endanger" in sub1.text
    
    # Verify paragraphs in subsection (1)
    paragraphs = sub1.paragraphs
    assert len(paragraphs) == 2
    assert paragraphs[0].id == "115958"
    assert paragraphs[0].text == "the safety, security or defence of Canada, or"
    assert paragraphs[1].id == "1201751"
    assert paragraphs[1].text == "the safety or security of the naval, army or air forces of any state other than Canada that are lawfully present in Canada."
    
    # Check second subsection (2) - definition of "prohibited act"
    sub2 = section.subsections[1]
    assert sub2.number == "(2)"
    assert sub2.id == "115961"
    assert "prohibited act" in sub2.text
    
    # Verify paragraphs in subsection (2)
    paragraphs = sub2.paragraphs
    assert len(paragraphs) == 2
    assert paragraphs[0].id == "115963"
    assert paragraphs[0].text == "impairs the efficiency or impedes the working of any vessel, vehicle, aircraft, machinery, apparatus or other thing; or"
    assert paragraphs[1].id == "115964"
    assert paragraphs[1].text == "causes property, by whomever it may be owned, to be lost, damaged or destroyed."
    
    # Check third subsection (3) with saving provisions
    sub3 = section.subsections[2]
    assert sub3.number == "(3)"
    assert sub3.id == "115965"
    assert "No person does a prohibited act within the meaning of this section by reason only that" in sub3.text
    
    # Verify paragraphs in subsection (3)
    paragraphs = sub3.paragraphs
    assert len(paragraphs) == 3
    assert paragraphs[0].id == "115967"
    assert "he stops work as a result of the failure of his employer and himself to agree" in paragraphs[0].text
    assert paragraphs[1].id == "115968"
    assert "bargaining agent" in paragraphs[1].text
    assert paragraphs[2].id == "115969"
    assert "combination of workmen" in paragraphs[2].text
    
    # Check fourth subsection (4)
    sub4 = section.subsections[3]
    assert sub4.number == "(4)"
    assert sub4.id == "115970"
    assert "dwelling-house" in sub4.text
    
    # Check fifth subsection (5)
    sub5 = section.subsections[4]
    assert sub5.number == "(5)"
    assert sub5.id == "1486981"
    assert "advocacy, protest or dissent" in sub5.text
    
    # Verify historical notes
    assert len(section.historical_notes) == 3
    assert "R.S., 1985, c. C-46, s. 52" in section.historical_notes[0].text
    assert "2019, c. 25, s. 6" in section.historical_notes[1].text
    assert "2024, c. 16, s. 60" in section.historical_notes[2].text

def test_parse_section_with_subsection_lists(example_sections, get_example):
    """Test parsing a section with subsections containing lists"""
    # Get the example for this test - using same example as subsection definitions
    example = get_example('test_parse_section_with_subsection_lists', example_sections)
    
    # Create parser instance
    parser = CriminalCodeParser()
    
    # Convert HTML string to BeautifulSoup Tag
    soup = BeautifulSoup(example['html'], 'html.parser')
    section_elem = soup.find('ul', class_='Section')
    
    # Parse the section
    section = parser._parse_section(section_elem)
    
    # Verify base section properties
    assert section.marginal_note.text == "Sabotage"
    assert section.number == "52"
    
    # Focus on testing the list structures in subsections
    
    # Test subsection (1)'s list structure
    sub1 = section.subsections[0]
    assert sub1.number == "(1)"
    paragraphs = sub1.paragraphs
    assert len(paragraphs) == 2  # Two items in list: (a) and (b)
    
    # Verify paragraph (a)
    assert paragraphs[0].label == "(a)"
    assert paragraphs[0].id == "115958"
    assert paragraphs[0].text == "the safety, security or defence of Canada, or"
    
    # Verify paragraph (b)
    assert paragraphs[1].label == "(b)"
    assert paragraphs[1].id == "1201751"
    assert paragraphs[1].text == "the safety or security of the naval, army or air forces of any state other than Canada that are lawfully present in Canada."
    
    # Test subsection (2)'s list structure
    sub2 = section.subsections[1]
    assert sub2.number == "(2)"
    paragraphs = sub2.paragraphs
    assert len(paragraphs) == 2  # Two items in list: (a) and (b)
    
    # Verify paragraph (a)
    assert paragraphs[0].label == "(a)"
    assert paragraphs[0].id == "115963"
    assert "impairs the efficiency" in paragraphs[0].text
    
    # Verify paragraph (b)
    assert paragraphs[1].label == "(b)"
    assert paragraphs[1].id == "115964"
    assert "causes property" in paragraphs[1].text
    
    # Test subsection (3)'s list structure
    sub3 = section.subsections[2]
    assert sub3.number == "(3)"
    paragraphs = sub3.paragraphs
    assert len(paragraphs) == 3  # Three items in list: (a), (b), and (c)
    
    # Verify all three paragraphs
    assert paragraphs[0].label == "(a)"
    assert paragraphs[0].id == "115967"
    
    assert paragraphs[1].label == "(b)"
    assert paragraphs[1].id == "115968"
    
    assert paragraphs[2].label == "(c)"
    assert paragraphs[2].id == "115969"