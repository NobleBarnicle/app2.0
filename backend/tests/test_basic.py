import pytest
from app import create_app
from app.scraper.models import CriminalCode, Part, Section
from datetime import datetime

def test_app_creation():
    """Test basic app creation and configuration"""
    app = create_app()
    assert app is not None
    assert app.config['TESTING'] is False
    
    # Test with testing config
    app = create_app(testing=True)
    assert app.config['TESTING'] is True

def test_basic_model_instantiation():
    """Test that our core models can be instantiated with minimal data"""
    # Test CriminalCode
    code = CriminalCode(
        title="Test Code",
        parts=[],
        last_updated=datetime.now(),
        last_amended=datetime.now()
    )
    assert code.title == "Test Code"
    assert len(code.parts) == 0

    # Test Part
    part = Part(
        id="test-part",
        number="I",
        title="Test Part",
        subheading=None,
        sections=[]
    )
    assert part.id == "test-part"
    assert part.sections == []

    # Test Section
    section = Section(
        id="test-section",
        number="1",
        text="Test content",
        marginal_note=None,
        subsections=[],
        definitions=[],
        historical_notes=[],
        cross_references=[],
        list_items=[]
    )
    assert section.id == "test-section"
    assert section.text == "Test content"

def test_basic_routes(client):
    """Test that core routes return expected status codes"""
    response = client.get('/')
    assert response.status_code == 200
    
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' in response.data

def test_basic_error_handling(client):
    """Test basic error handling"""
    response = client.get('/nonexistent-route')
    assert response.status_code == 404
    
def test_pytest_working():
    """Basic test to verify pytest is working"""
    assert True

def test_app_fixture(app):
    """Test that app fixture creates Flask app correctly"""
    assert app is not None
    assert app.config['TESTING'] is True

def test_example_loading(example_sections, get_example):
    """Test that example loading system works"""
    # Verify we can load examples
    assert example_sections is not None
    assert len(example_sections) > 0
    
    # Verify we can get a specific example
    base_section = get_example('test_parse_base_section', example_sections)
    assert base_section is not None
    assert 'html' in base_section
    assert 'components' in base_section
    
    # Verify example contains expected data
    assert 'Marginal Note' in base_section['components']
    assert 'Section ID' in base_section['components']
    