from flask import Flask

def create_app(testing=False):
    app = Flask(__name__)
    
    # Basic configuration
    app.config['TESTING'] = testing
    
    # Register routes
    @app.route('/')
    def index():
        return 'Welcome to Criminal Code API'
        
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
        
    return app