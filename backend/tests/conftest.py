import pytest
from app import create_app
import re
from pathlib import Path
from bs4 import BeautifulSoup
from app.scraper.parser import CriminalCodeParser

@pytest.fixture
def app():
    """Create and configure a test Flask app"""
    app = create_app(testing=True)
    return app

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

def load_examples_from_md():
    """Load and parse examples from parsing_examples.md"""
    project_root = Path(__file__).parent.parent
    file_path = project_root / "src" / "app" / "scraper" / "parsing_examples.md"
    
    print(f"\nReading from: {file_path}")
    with open(file_path, 'r') as f:
        content = f.read()
    
    print(f"Content length: {len(content)} characters")
    examples = {}
    
    # Split content into sections
    sections = re.split(r'(?=##\s*\d+(?:\.\d+)*\s+[^\n]+)', content)[1:]
    
    print(f"\nFound {len(sections)} sections:")
    for section in sections:
        # Extract section title
        title_match = re.match(r'##\s*\d+(?:\.\d+)*\s+(.*?)(?:\n|$)', section)
        if title_match:
            name = title_match.group(1).strip()
            print(f"- {name}")
            
            # Find HTML example
            example_match = re.search(r'### Example:\s*\n(.*?)(?=###|\Z)', section, re.DOTALL)
            if example_match:
                html = example_match.group(1).strip()
                print(f"  Found HTML example ({len(html)} chars)")
                
                # Find components
                components_match = re.search(r'### Components:\s*\n(.*?)(?=##|\Z)', section, re.DOTALL)
                if components_match:
                    components = components_match.group(1).strip()
                    print(f"  Found components ({len(components)} chars)")
                    
                    # Parse components into dictionary
                    component_dict = {}
                    current_key = None
                    current_list = []
                    
                    for line in components.split('\n'):
                        line = line.strip()
                        if not line:
                            continue
                            
                        if line.startswith('- '):
                            # Save previous key-value pair if exists
                            if current_key and current_list:
                                component_dict[current_key] = '\n'.join(current_list)
                                current_list = []
                            
                            # Start new key-value pair
                            if ':' in line[2:]:
                                current_key, value = line[2:].split(':', 1)
                                current_key = current_key.strip()
                                current_list = [value.strip()]
                        elif line.startswith('  -') and current_key:
                            # This is a nested value
                            current_list.append(line)
                    
                    # Don't forget to save the last key-value pair
                    if current_key and current_list:
                        component_dict[current_key] = '\n'.join(current_list)
                    
                    # Store example
                    examples[name] = {
                        'html': html,
                        'components': component_dict
                    }
                    print(f"  Stored example for '{name}'")
    
    return examples

@pytest.fixture(scope="session")
def example_sections():
    """Fixture that provides access to parsed examples"""
    return load_examples_from_md()

# Mapping between test cases and example names
TEST_CASE_MAPPING = {
    'test_parse_part': 'Part',
    'test_parse_section': 'Section',                   
    'test_parse_section_with_list': 'Section with List',             
    'test_parse_section_with_inline_definitions': 'Section with Inline Definitions',         
    'test_parse_section_with_indented_definitions': 'Section with Indented Definitions',
    'test_parse_section_with_continued_text': 'Section with Continued Text',
    'test_parse_section_with_subsections': 'Section with Subsections',
    'test_parse_section_with_subsection_lists': 'Section with Subsections with Lists',
    'test_parse_section_with_subsection_inline_definitions': 'Section with Subsections with Inline Definitions',
    'test_parse_section_with_subsection_indented_definitions': 'Section with Subsections with Indented Definitions',     
    'test_parse_section_with_cross_references': 'Section with Cross References',   

}

@pytest.fixture
def get_example():
    def _get_example(test_name, examples):
        example_name = TEST_CASE_MAPPING.get(test_name)
        if not example_name:
            raise ValueError(f"No example mapping found for test {test_name}")
        return examples[example_name]  
    return _get_example

@pytest.fixture
def parser_with_soup(example_sections, get_example):
    """Creates a parser and soup for a specific test example"""
    def _create_parser_and_soup(test_name):
        example = get_example(test_name, example_sections)
        parser = CriminalCodeParser()
        soup = BeautifulSoup(example['html'], 'html.parser')
        return parser, soup, example
    return _create_parser_and_soup