import pytest
from app import create_app
import re
from pathlib import Path

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
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Dictionary to store examples by their type/name
    examples = {}
    
    # Find all example sections using regex
    sections = re.split(r'###\s+\d+\.\d+\s+', content)
    
    for section in sections[1:]:  # Skip first empty section
        # Get section name from first line
        name = section.split('\n')[0].strip()
        
        # Find HTML example between the Example: and Components: markers
        example_match = re.search(r'#### Example:\n(.*?)#### Components:', 
                                section, re.DOTALL)
        if example_match:
            html = example_match.group(1).strip()
            
        # Find expected components
        components_match = re.search(r'#### Components:\n(.*?)(?=###|\Z)', 
                                   section, re.DOTALL)
        if components_match:
            components = components_match.group(1).strip()
            
            # Parse components into a dictionary
            component_dict = {}
            for line in components.split('\n'):
                if line.startswith('- '):
                    key, value = line[2:].split(':', 1)
                    component_dict[key.strip()] = value.strip()
            
        examples[name] = {
            'html': html,
            'components': component_dict
        }
    
    return examples

@pytest.fixture(scope="session")
def example_sections():
    """Fixture that provides access to parsed examples"""
    return load_examples_from_md()

# Mapping between test cases and example names
TEST_CASE_MAPPING = {
    'test_parse_base_section': 'Base Case Section',
    'test_parse_section_with_list': 'Section with List',
    'test_parse_section_with_inline_definitions': 'Section with Inline Definitions',
    'test_parse_section_with_indented_definitions': 'Section with Indented Definitions',
    'test_parse_section_with_subsections': 'Section with Subsections',
    'test_parse_section_with_continued_text': 'Section with Continued Text'
}

@pytest.fixture
def get_example():
    """Fixture that returns a function to get example by test name"""
    def _get_example(test_name, examples):
        example_name = TEST_CASE_MAPPING.get(test_name)
        if not example_name:
            raise ValueError(f"No example mapping found for test {test_name}")
        return examples[example_name]
    return _get_example