from flask import Flask
from flask_cors import CORS

def create_app(config_class=None):
    app = Flask(__name__)
    
    if config_class:
        app.config.from_object(config_class)
    
    CORS(app)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}
    
    return app 