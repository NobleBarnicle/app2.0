def test_config(app):
    assert app.config['TESTING'] == True
    assert 'criminalcode_test' in app.config['POSTGRES_URI'] 