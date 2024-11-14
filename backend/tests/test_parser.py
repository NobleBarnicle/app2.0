import pytest
from bs4 import BeautifulSoup
from app.scraper.parser import CriminalCodeParser
from app.scraper.models import Part

def test_parse_part(parser_with_soup):
    """Test parsing a Part with optional subheadings"""
    parser, soup, example = parser_with_soup('test_parse_part')
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

def test_parse_section(parser_with_soup):
    """Test parsing a basic section structure"""
    parser, soup, example = parser_with_soup('test_parse_section')
    section_elem = soup.find('p', class_='Section')
    
    # Parse the section using existing parser method
    section = parser._parse_section(section_elem)
    
    # Debug - print raw values
    print("\nMarginal Note from parser:", section.marginal_note.text)
    print("Marginal Note from example:", example['components']['Marginal Note'])
    
    # Extract just the quoted text from the example component
    expected_text = example['components']['Marginal Note'].split('"')[1] if '"' in example['components']['Marginal Note'] else expected_text
    
    # Compare against expected components
    assert section.marginal_note.text == expected_text
    assert section.id == example['components']['Section ID'].split('"')[1]
    assert section.number == example['components']['Section Number'].split('"')[1]
    assert section.text == example['components']['Content'].split('"')[1]
    assert section.historical_notes[0].text == example['components']['Historical Note'].split('"')[1]

def test_parse_section_with_list(parser_with_soup):
    """Test parsing a section containing a nested provision list structure"""
    parser, soup, example = parser_with_soup('test_parse_section_with_list')
    section_elem = soup.find('p', class_='Section')
    
    # Parse the section
    section = parser._parse_section(section_elem)
    
    # Verify base section properties
    assert section.marginal_note.text == "Offences of negligence — organizations"
    assert section.number == "22.1"
    assert section.id == "115590"
    
    # Verify initial content
    assert "In respect of an offence that requires the prosecution to prove negligence" in section.text
    assert "an organization is a party to the offence if" in section.text
    
    # Verify list items structure
    list_items = section.list_items
    assert len(list_items) == 2
    
    # Test first item (a) and its subitems
    item_a = list_items[0]
    assert item_a.id == "115592"
    assert item_a.label == "(a)"
    assert "acting within the scope of their authority" in item_a.text
    
    # Verify subitems under (a)
    subitems_a = item_a.subitems
    assert len(subitems_a) == 2
    
    # Test subitem (i)
    assert subitems_a[0].id == "115593"
    assert subitems_a[0].label == "(i)"
    assert "one of its representatives is a party to the offence" in subitems_a[0].text
    
    # Test subitem (ii)
    assert subitems_a[1].id == "115594"
    assert subitems_a[1].label == "(ii)"
    assert "two or more of its representatives engage in conduct" in subitems_a[1].text
    assert "that representative would have been a party to the offence" in subitems_a[1].text
    
    # Test second item (b)
    item_b = list_items[1]
    assert item_b.id == "115595"
    assert item_b.label == "(b)"
    assert "the senior officer who is responsible for the aspect of the organization's activities" in item_b.text
    assert "could reasonably be expected to prevent a representative of the organization from being a party to the offence" in item_b.text
    
    # Verify historical note
    assert len(section.historical_notes) == 1
    assert section.historical_notes[0].text == "2003, c. 21, s. 2"

def test_parse_section_with_inline_definitions(parser_with_soup):
    """Test parsing a section containing inline definitions with multiple historical notes"""
    parser, soup, example = parser_with_soup('test_parse_section_with_inline_definitions')
    section_elem = soup.find('p', class_='Section')
    
    # Parse the section
    section = parser._parse_section(section_elem)
    
    # Verify base section properties
    assert section.marginal_note.text == "Further definitions — firearms"
    assert section.number == "2.1"
    assert section.id == "1487945"
    
    # Verify initial content
    assert "In this Act" in section.text
    
    # Verify defined terms
    defined_terms = [
        "ammunition", "antique firearm", "automatic firearm", "cartridge magazine",
        "cross-bow", "firearm part", "handgun", "imitation firearm", 
        "prohibited ammunition", "prohibited device", "prohibited firearm",
        "prohibited weapon", "replica firearm", "restricted firearm",
        "restricted weapon", "authorization", "licence", "registration certificate"
    ]
    
    # Check that all defined terms are present
    for term in defined_terms:
        assert any(def_term.term == term for def_term in section.definitions)
    
    # Verify that all terms reference subsection 84(1)
    assert "have the same meaning as in subsection 84(1)" in section.text
    
    # Verify historical notes
    assert len(section.historical_notes) == 2
    assert section.historical_notes[0].text == "2009, c. 22, s. 1"
    
    # Verify amendment note
    amendment = section.historical_notes[1]
    assert amendment.text == "2023, c. 32, s. 0.1"
    
    # Verify amendment details (if parser supports this)
    if hasattr(amendment, 'amendment_details'):
        assert amendment.amendment_details.section_number == "0.1"
        assert amendment.amendment_details.subsection_number == "(1)"
        assert "Section 2.1 of the Criminal Code is replaced by the following" in amendment.amendment_details.text

def test_parse_section_with_indented_definitions(parser_with_soup):
    """Test parsing a section with indented definition list structure"""
    parser, soup, example = parser_with_soup('test_parse_section_with_indented_definitions')
    section_elem = soup.find('p', class_='Section')
    
    # Parse the section
    section = parser._parse_section(section_elem)
    
    # Verify base section properties
    assert section.marginal_note.text == "Definitions"
    assert section.number == "118"
    assert section.id == "117789"
    
    # Verify initial content
    assert section.text == "In this Part,"
    
    # Verify all definitions
    assert len(section.definitions) == 6
    
    # Test "evidence" definition
    evidence_def = section.definitions[0]
    assert evidence_def.id == "117791"
    assert evidence_def.term == "evidence"
    assert "assertion of fact, opinion, belief or knowledge" in evidence_def.definition_text
    assert evidence_def.french_terms == ["témoignage", "déposition", "déclaration"]
    
    # Test "government" definition
    gov_def = section.definitions[1]
    assert gov_def.id == "117792"
    assert gov_def.term == "government"
    assert len(gov_def.list_items) == 3
    assert gov_def.list_items[0].id == "117793"
    assert "the Government of Canada" in gov_def.list_items[0].text
    assert gov_def.list_items[1].id == "117794"
    assert "the government of a province" in gov_def.list_items[1].text
    assert gov_def.list_items[2].id == "117795"
    assert "Her Majesty in right of Canada or a province" in gov_def.list_items[2].text
    assert gov_def.french_terms == ["gouvernement"]
    
    # Test "judicial proceeding" definition
    judicial_def = section.definitions[2]
    assert judicial_def.id == "117796"
    assert judicial_def.term == "judicial proceeding"
    assert len(judicial_def.list_items) == 5
    assert judicial_def.list_items[0].id == "117797"
    assert "in or under the authority of a court of justice" in judicial_def.list_items[0].text
    assert judicial_def.list_items[4].id == "117801"
    assert "before a tribunal by which a legal right or legal liability may be established" in judicial_def.list_items[4].text
    assert "whether or not the proceeding is invalid for want of jurisdiction" in judicial_def.continued_text
    assert judicial_def.french_terms == ["procédure judiciaire"]
    
    # Test "office" definition
    office_def = section.definitions[3]
    assert office_def.id == "117803"
    assert office_def.term == "office"
    assert len(office_def.list_items) == 3
    assert office_def.list_items[0].id == "117804"
    assert "an office or appointment under the government" in office_def.list_items[0].text
    assert office_def.french_terms == ["charge", "emploi"]
    
    # Test "official" definition
    official_def = section.definitions[4]
    assert official_def.id == "117807"
    assert official_def.term == "official"
    assert len(official_def.list_items) == 2
    assert official_def.list_items[0].id == "117808"
    assert "holds an office" in official_def.list_items[0].text
    assert official_def.french_terms == ["fonctionnaire"]
    
    # Test "witness" definition
    witness_def = section.definitions[5]
    assert witness_def.id == "117810"
    assert witness_def.term == "witness"
    assert "gives evidence orally under oath or by affidavit" in witness_def.definition_text
    assert "child of tender years who gives evidence" in witness_def.definition_text
    assert witness_def.french_terms == ["témoin"]
    
    # Verify historical notes
    assert len(section.historical_notes) == 3
    assert section.historical_notes[0].text == "R.S., 1985, c. C-46, s. 118"
    assert section.historical_notes[1].text == "R.S., 1985, c. 27 (1st Supp.), ss. 15, 203"
    assert section.historical_notes[2].text == "2007, c. 13, s. 2"

def test_parse_section_with_continued_text(parser_with_soup):
    """Test parsing a section with continued text after a provision list"""
    parser, soup, example = parser_with_soup('test_parse_section_with_continued_text')
    section_elem = soup.find('p', class_='Section')
    
    # Parse the section
    section = parser._parse_section(section_elem)
    
    # Verify base section properties
    assert section.marginal_note.text == "Inciting to mutiny"
    assert section.number == "53"
    assert section.id == "115974"
    
    # Verify initial content
    assert section.text == "Every one who"
    
    # Verify provision list structure
    paragraphs = section.paragraphs
    assert len(paragraphs) == 2
    
    # Verify paragraph (a)
    assert paragraphs[0].id == "115976"
    assert paragraphs[0].label == "(a)"
    assert "attempts, for a traitorous or mutinous purpose" in paragraphs[0].text
    assert "seduce a member of the Canadian Forces" in paragraphs[0].text
    assert "duty and allegiance to Her Majesty" in paragraphs[0].text
    
    # Verify paragraph (b)
    assert paragraphs[1].id == "115977"
    assert paragraphs[1].label == "(b)"
    assert "attempts to incite or to induce" in paragraphs[1].text
    assert "member of the Canadian Forces" in paragraphs[1].text
    assert "commit a traitorous or mutinous act" in paragraphs[1].text
    
    # Verify continued text after list
    assert section.continued_text.id == "115978"
    assert section.continued_text.text == "is guilty of an indictable offence and liable to imprisonment for a term not exceeding fourteen years."
    
    # Verify historical note
    assert len(section.historical_notes) == 1
    assert section.historical_notes[0].text == "R.S., c. C-34, s. 53"
    
    # Verify HTML structure
    if hasattr(section, 'html_structure'):
        # Verify the section has a ProvisionList
        assert 'ProvisionList' in section.html_structure.classes
        # Verify ContinuedSectionSubsection follows the list
        assert section.continued_text.html_class == 'ContinuedSectionSubsection'

def test_parse_section_with_subsections(parser_with_soup):
    """Test parsing a section with basic subsections structure"""
    parser, soup, example = parser_with_soup('test_parse_section_with_subsections')
    section_elem = soup.find('ul', class_='Section')
    
    # Parse the section
    section = parser._parse_section(section_elem)
    
    # Verify base section properties
    assert section.marginal_note.text == "Effect of judicial acts"
    assert section.number == "3.1"
    assert section.id == "115246"
    
    # Verify subsections
    assert len(section.subsections) == 2
    
    # Test first subsection (1)
    sub1 = section.subsections[0]
    assert sub1.number == "(1)"
    assert sub1.id == "1201744"
    assert "Unless otherwise provided or ordered" in sub1.text
    assert "anything done by a court, justice or judge is effective from the moment it is done" in sub1.text
    assert "whether or not it is reduced to writing" in sub1.text
    
    # Test second subsection (2)
    sub2 = section.subsections[1]
    assert sub2.number == "(2)"
    assert sub2.id == "1201745"
    assert sub2.marginal_note.text == "Clerk of the court"
    assert "Unless otherwise provided or ordered" in sub2.text
    assert "if anything is done from the bench by a court, justice or judge" in sub2.text
    assert "the clerk of the court may sign the writing" in sub2.text
    
    # Verify historical notes and amendments
    assert len(section.historical_notes) == 2
    
    # Check first historical note
    assert section.historical_notes[0].text == "2002, c. 13, s. 2"
    
    # Check amendment note
    amendment = section.historical_notes[1]
    assert amendment.text == "2019, c. 25, s. 3"
    
    # Verify amendment details (if parser supports this)
    if hasattr(amendment, 'amendment_details'):
        assert "Section 3.1 of the Act is renumbered as subsection 3.1(1)" in amendment.amendment_details.text
        assert "and is amended by adding the following" in amendment.amendment_details.text
        # Verify the amendment adds subsection (2)
        assert amendment.amendment_details.added_subsection.number == "(2)"
        assert amendment.amendment_details.added_subsection.marginal_note.text == "Clerk of the court"

def test_parse_section_with_subsection_lists(parser_with_soup):
    """Test parsing a section with subsections containing lists"""
    parser, soup, example = parser_with_soup('test_parse_section_with_subsection_lists')
    section_elem = soup.find('ul', class_='Section')
    
    # Parse the section
    section = parser._parse_section(section_elem)
    
    # Verify base section properties
    assert section.marginal_note.text == "Fraud"
    assert section.number == "380"
    assert section.id == "122425"
    
    # Verify subsections
    assert len(section.subsections) == 3
    
    # Test subsection (1) and its nested list structure
    sub1 = section.subsections[0]
    assert sub1.number == "(1)"
    assert sub1.id == "122427"
    assert "Every one who, by deceit, falsehood or other fraudulent means" in sub1.text
    assert "defrauds the public or any person" in sub1.text
    
    # Verify paragraphs in subsection (1)
    paragraphs = sub1.paragraphs
    assert len(paragraphs) == 2
    
    # Test paragraph (a)
    para_a = paragraphs[0]
    assert para_a.id == "122428"
    assert para_a.label == "(a)"
    assert "is guilty of an indictable offence" in para_a.text
    assert "imprisonment not exceeding fourteen years" in para_a.text
    assert "where the subject-matter of the offence is a testamentary instrument" in para_a.text
    
    # Test paragraph (b) and its subparagraphs
    para_b = paragraphs[1]
    assert para_b.id == "122429"
    assert para_b.label == "(b)"
    assert para_b.text == "is guilty"
    
    # Verify subparagraphs under (b)
    subparas = para_b.subitems
    assert len(subparas) == 2
    
    # Test subparagraph (i)
    assert subparas[0].id == "122430"
    assert subparas[0].label == "(i)"
    assert "of an indictable offence" in subparas[0].text
    assert "imprisonment for a term not exceeding two years" in subparas[0].text
    
    # Test subparagraph (ii)
    assert subparas[1].id == "122431"
    assert subparas[1].label == "(ii)"
    assert "of an offence punishable on summary conviction" in subparas[1].text
    
    # Verify continued text after subparagraphs
    assert "where the value of the subject-matter of the offence does not exceed five thousand dollars" in para_b.continued_text
    
    # Test subsection (1.1)
    sub2 = section.subsections[1]
    assert sub2.number == "(1.1)"
    assert sub2.id == "122433"
    assert sub2.marginal_note.text == "Minimum punishment"
    assert "When a person is prosecuted on indictment" in sub2.text
    assert "minimum punishment of imprisonment for a term of two years" in sub2.text
    assert "total value of the subject-matter of the offences exceeds one million dollars" in sub2.text
    
    # Test subsection (2)
    sub3 = section.subsections[2]
    assert sub3.number == "(2)"
    assert sub3.id == "122435"
    assert sub3.marginal_note.text == "Affecting public market"
    assert "Every one who, by deceit, falsehood or other fraudulent means" in sub3.text
    assert "affects the public market price of stocks, shares, merchandise" in sub3.text
    assert "imprisonment for a term not exceeding fourteen years" in sub3.text
    
    # Verify historical notes
    assert len(section.historical_notes) == 6
    assert section.historical_notes[0].text == "R.S., 1985, c. C-46, s. 380"
    assert section.historical_notes[1].text == "R.S., 1985, c. 27 (1st Supp.), s. 54"
    assert section.historical_notes[2].text == "1994, c. 44, s. 25"
    assert section.historical_notes[3].text == "1997, c. 18, s. 26"
    assert section.historical_notes[4].text == "2004, c. 3, s. 2"
    assert section.historical_notes[5].text == "2011, c. 6, s. 2"

def test_parse_section_with_subsection_inline_definitions(parser_with_soup):
    """Test parsing a section with subsections containing inline definitions"""
    parser, soup, example = parser_with_soup('test_parse_section_with_subsection_inline_definitions')
    section_elem = soup.find('ul', class_='Section')
    
    # Parse the section
    section = parser._parse_section(section_elem)
    
    # Verify base section properties
    assert section.marginal_note.text == "Sabotage"
    assert section.number == "52"
    assert section.id == "115955"
    
    # Verify subsections
    assert len(section.subsections) == 5
    
    # Test first subsection (1)
    sub1 = section.subsections[0]
    assert sub1.number == "(1)"
    assert sub1.id == "115957"
    assert "Every person is guilty of an indictable offence" in sub1.text
    assert "liable to imprisonment for a term of not more than 10 years" in sub1.text
    
    # Verify paragraphs in subsection (1)
    paragraphs = sub1.paragraphs
    assert len(paragraphs) == 2
    assert paragraphs[0].id == "115958"
    assert paragraphs[0].text == "the safety, security or defence of Canada, or"
    assert paragraphs[1].id == "1201751"
    assert paragraphs[1].text == "the safety or security of the naval, army or air forces of any state other than Canada that are lawfully present in Canada."
    
    # Test second subsection (2) with definition
    sub2 = section.subsections[1]
    assert sub2.number == "(2)"
    assert sub2.id == "115961"
    assert sub2.marginal_note.text == "Definition of prohibited act"
    
    # Verify defined term
    assert "prohibited act" in sub2.text
    assert len(sub2.paragraphs) == 2
    assert sub2.paragraphs[0].id == "115963"
    assert "impairs the efficiency or impedes the working of any vessel" in sub2.paragraphs[0].text
    assert sub2.paragraphs[1].id == "115964"
    assert "causes property, by whomever it may be owned, to be lost, damaged or destroyed" in sub2.paragraphs[1].text
    
    # Test third subsection (3) with saving provisions
    sub3 = section.subsections[2]
    assert sub3.number == "(3)"
    assert sub3.id == "115965"
    assert sub3.marginal_note.text == "Saving"
    assert "No person does a prohibited act within the meaning of this section by reason only that" in sub3.text
    
    # Verify paragraphs in subsection (3)
    assert len(sub3.paragraphs) == 3
    assert sub3.paragraphs[0].id == "115967"
    assert "he stops work as a result of the failure of his employer and himself to agree" in sub3.paragraphs[0].text
    assert sub3.paragraphs[1].id == "115968"
    assert "bargaining agent" in sub3.paragraphs[1].text
    assert sub3.paragraphs[2].id == "115969"
    assert "combination of workmen" in sub3.paragraphs[2].text
    
    # Test fourth subsection (4)
    sub4 = section.subsections[3]
    assert sub4.number == "(4)"
    assert sub4.id == "115970"
    assert sub4.marginal_note.text == "Idem"
    assert "dwelling-house" in sub4.text
    assert "obtaining or communicating information" in sub4.text
    
    # Test fifth subsection (5)
    sub5 = section.subsections[4]
    assert sub5.number == "(5)"
    assert sub5.id == "1486981"
    assert sub5.marginal_note.text == "For greater certainty"
    assert "advocacy, protest or dissent" in sub5.text
    assert "do not intend to cause any of the harms referred to in paragraphs (1)(a) and (b)" in sub5.text
    
    # Verify historical notes
    assert len(section.historical_notes) == 3
    assert section.historical_notes[0].text == "R.S., 1985, c. C-46, s. 52"
    
    # Verify amendment notes
    amendment1 = section.historical_notes[1]
    assert amendment1.text == "2019, c. 25, s. 6"
    if hasattr(amendment1, 'amendment_details'):
        assert "The portion of subsection 52(1) of the Act before paragraph (a) is replaced" in amendment1.amendment_details.text
    
    amendment2 = section.historical_notes[2]
    assert amendment2.text == "2024, c. 16, s. 60"
    if hasattr(amendment2, 'amendment_details'):
        assert "Section 52 of the Act is amended by adding the following after subsection (4)" in amendment2.amendment_details.text

def test_parse_section_with_subsection_indented_definitions(parser_with_soup):
    """Test parsing a section with subsections containing indented definitions"""
    parser, soup, example = parser_with_soup('test_parse_section_with_subsection_indented_definitions')
    section_elem = soup.find('ul', class_='Section')
    
    # Parse the section
    section = parser._parse_section(section_elem)
    
    # Verify base section properties
    assert section.marginal_note.text == "Counterfeiting stamp, etc."
    assert section.number == "376"
    assert section.id == "122374"
    
    # Verify subsections
    assert len(section.subsections) == 3
    
    # Check first subsection (1)
    sub1 = section.subsections[0]
    assert sub1.number == "(1)"
    assert sub1.id == "122376"
    assert "Every person is guilty of an indictable offence" in sub1.text
    
    # Verify paragraphs in subsection (1)
    paragraphs = sub1.list_items
    assert len(paragraphs) == 3
    assert paragraphs[0].id == "122377"
    assert "fraudulently uses, mutilates" in paragraphs[0].text
    
    # Check second subsection (2)
    sub2 = section.subsections[1]
    assert sub2.number == "(2)"
    assert sub2.id == "122382"
    assert sub2.marginal_note.text == "Counterfeiting mark"
    
    # Check third subsection (3) with definitions
    sub3 = section.subsections[2]
    assert sub3.number == "(3)"
    assert sub3.id == "122389"
    assert sub3.marginal_note.text == "Definitions"
    
    # Verify definitions
    definitions = sub3.definitions
    assert len(definitions) == 2
    
    # Check "mark" definition
    mark_def = definitions[0]
    assert mark_def.term == "mark"
    assert "means a mark, brand, seal" in mark_def.definition_text
    assert mark_def.french_term == "marque"
    
    # Check "stamp" definition
    stamp_def = definitions[1]
    assert stamp_def.term == "stamp"
    assert "means an impressed or adhesive stamp" in stamp_def.definition_text
    assert stamp_def.french_term == "timbre"
    
    # Detailed testing of subsection (1) list items
    sub1 = section.subsections[0]
    list_items = sub1.list_items
    
    # Test first item (a)
    assert list_items[0].label == "(a)"
    assert list_items[0].id == "122377"
    assert "fraudulently uses, mutilates, affixes, removes or counterfeits a stamp or part thereof" in list_items[0].text
    
    # Test second item (b) and its subitems
    assert list_items[1].label == "(b)"
    assert list_items[1].id == "122378"
    assert "knowingly and without lawful excuse has in their possession" in list_items[1].text
    
    # Test (b)'s subitems
    subitems = list_items[1].subitems
    assert len(subitems) == 2
    assert subitems[0].label == "(i)"
    assert subitems[0].id == "122379"
    assert "a counterfeit stamp or a stamp that has been fraudulently mutilated" in subitems[0].text
    assert subitems[1].label == "(ii)"
    assert subitems[1].id == "122380"
    assert "anything bearing a stamp of which a part has been fraudulently erased, removed or concealed" in subitems[1].text
    
    # Test third item (c)
    assert list_items[2].label == "(c)"
    assert list_items[2].id == "122381"
    assert "without lawful excuse makes or knowingly has in their possession a die or instrument" in list_items[2].text

def test_parse_section_with_cross_references(parser_with_soup):
    """Test parsing of cross-references"""
    parser, soup, example = parser_with_soup('test_parse_section_with_cross_references')
    
    # Find the cross-reference element in subsection (2)
    cross_ref_elem = soup.find('cite', class_='XRefExternalAct')
    
    # Parse the cross-reference
    cross_ref = parser._parse_cross_reference(cross_ref_elem)
    
    # Verify the cross-reference
    assert cross_ref.is_external == True
    assert cross_ref.text == "Aeronautics Act"
    assert cross_ref.external_url == "https://laws-lois.justice.gc.ca/eng/acts/A-2"

def test_parser_error_handling():
    """Test parser behavior with malformed input"""
    parser = CriminalCodeParser()
    
    # Test with empty/invalid HTML
    empty_soup = BeautifulSoup("", 'html.parser')
    result = parser.parse_html("")
    assert result is None
    
    # Test with missing required attributes
    malformed_html = """
        <p class="Section">
            <span class="sectionLabel">1</span>
        </p>
    """
    soup = BeautifulSoup(malformed_html, 'html.parser')
    section = parser._parse_section(soup.find('p'))
    assert section is None

@pytest.mark.parametrize("section_number,expected_format", [
    ("1", True),
    ("1.1", True),
    ("1.a", False),
    ("a1", False),
])
def test_section_number_validation(section_number, expected_format):
    """Test section number format validation"""
    parser = CriminalCodeParser()
    assert bool(parser.section_number_pattern.match(section_number)) == expected_format

