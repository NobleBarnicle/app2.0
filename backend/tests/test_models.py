import pytest
from datetime import datetime
from app.scraper.models import (
    CriminalCode, Part, Section, Subsection,
    Definition, HistoricalNote, CrossReference,
    MarginalNote, ListItem
)

def test_criminal_code_structure():
    # Create a complex structure
    section1 = Section(
        id="sec-1",
        number="1",
        marginal_note=MarginalNote(text="First Section"),
        text="Main text",
        subsections=[
            Subsection(id="sub-1", number="(1)", text="First subsection")
        ],
        definitions=[],
        historical_notes=[
            HistoricalNote(text="R.S., 1985, c. C-46, s. 1")
        ],
        cross_references=[],
        list_items=[]
    )
    
    section2 = Section(
        id="sec-2",
        number="2",
        marginal_note=MarginalNote(text="Second Section"),
        text="Another section",
        subsections=[],
        definitions=[],
        historical_notes=[],
        cross_references=[
            CrossReference(text="See section 1", target_section="1")
        ],
        list_items=[]
    )
    
    part = Part(
        id="part-1",
        number="I",
        title="First Part",
        subheading="General",
        sections=[section1, section2]
    )
    
    code = CriminalCode(
        title="Criminal Code",
        parts=[part],
        last_updated=datetime.now(),
        last_amended=datetime.now()
    )
    
    # Test structure
    assert len(code.parts) == 1
    assert len(code.parts[0].sections) == 2
    assert code.parts[0].sections[0].subsections[0].number == "(1)"
    assert code.parts[0].sections[1].cross_references[0].target_section == "1"
    
    # Print example structure
    print("\nCriminal Code Structure Example:")
    print(f"Title: {code.title}")
    print(f"Part {code.parts[0].number}: {code.parts[0].title}")
    for section in code.parts[0].sections:
        print(f"  Section {section.number}: {section.marginal_note.text}")
        if section.subsections:
            print(f"    Subsection {section.subsections[0].number}: {section.subsections[0].text}")
        if section.cross_references:
            print(f"    Cross Reference: {section.cross_references[0].text}")

def test_get_section_by_number():
    # Create a test structure with section 35
    section = Section(
        id="test-35",
        number="35",
        marginal_note=None,
        text="Test section",
        subsections=[],
        definitions=[],
        historical_notes=[],
        cross_references=[],
        list_items=[]
    )
    
    part = Part(
        id="part-1",
        number="I",
        title="Test Part",
        subheading=None,
        sections=[section]
    )
    
    code = CriminalCode(
        title="Criminal Code",
        parts=[part],
        last_updated=datetime.now(),
        last_amended=datetime.now()
    )
    
    # Test section lookup
    found_section = code.get_section_by_number("35")
    assert found_section is not None
    assert found_section.number == "35"
    
    # Test non-existent section
    assert code.get_section_by_number("999") is None

def test_list_item_behavior():
    # Test auto-initialization of subitems
    item = ListItem(
        id="test-1",
        label="(a)",
        text="Test text"
        # intentionally not providing subitems or parent_id
    )
    assert item.subitems == []  # Should be initialized as empty list
    
    # Test adding subitems
    subitem = ListItem(
        id="sub-1",
        label="(i)",
        text="Subitem text",
        parent_id="test-1"
    )
    item.subitems.append(subitem)
    
    # Verify relationships
    assert len(item.subitems) == 1
    assert item.subitems[0].parent_id == item.id
    
    # Test nested structure integrity
    sub_subitem = ListItem(
        id="sub-sub-1",
        label="(A)",
        text="Sub-subitem text",
        parent_id="sub-1"
    )
    subitem.subitems.append(sub_subitem)
    
    # Verify multi-level nesting
    assert len(item.subitems[0].subitems) == 1
    assert item.subitems[0].subitems[0].parent_id == subitem.id

def test_section_with_nested_definitions():
    definition = Definition(
        term="vehicle",
        definition_text="means any of the following:",
        french_term="véhicule",
        nested_items=[
            ListItem(
                id="def-1-a",
                label="(a)",
                text="automobile",
                subitems=[
                    ListItem(
                        id="def-1-a-i",
                        label="(i)",
                        text="passenger vehicle",
                        parent_id="def-1-a"
                    )
                ]
            ),
            ListItem(
                id="def-1-b",
                label="(b)",
                text="motorcycle"
            )
        ]
    )
    
    section = Section(
        id="test-1",
        number="1",
        marginal_note=MarginalNote(text="Definitions"),
        text="In this section,",
        subsections=[],
        definitions=[definition],
        historical_notes=[],
        cross_references=[],
        list_items=[]
    )
    
    # Test structure
    assert len(section.definitions) == 1
    assert len(section.definitions[0].nested_items) == 2
    assert len(section.definitions[0].nested_items[0].subitems) == 1
    
    # Print example structure
    print("\nDefinition Structure Example:")
    print(f"Term: {definition.term} ({definition.french_term})")
    print(f"Text: {definition.definition_text}")
    for item in definition.nested_items:
        print(f"  {item.label} {item.text}")
        for subitem in item.subitems:
            print(f"    {subitem.label} {subitem.text}")

def test_subsection_with_continued_text():
    subsection = Subsection(
        id="sub-1",
        number="(1)",
        text="Initial text",
        continued_text="Continued text"
    )
    
    assert subsection.text == "Initial text"
    assert subsection.continued_text == "Continued text"

