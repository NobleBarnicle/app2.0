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
    