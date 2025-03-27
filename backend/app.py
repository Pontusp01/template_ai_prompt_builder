import os
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from infrastructure.database.connection import get_db_connection, test_connection
from infrastructure.api.routes import register_routes
from infrastructure.config.config import load_config

def create_app():
    # Create Flask application
    app = Flask(__name__)
    
    # Load configuration
    config = load_config()
    app.config.update(config)
    
    # Allow these origins for CORS
    allowed_origins = [
        'https://intelligent-prompt-builder.lovable.app',
        'https://lovable.dev/projects/678a6a36-8a47-4cec-a4c8-b451ad325b06',
        'https://preview--intelligent-prompt-builder.lovable.app/',
        'https://intelligent-prompt-builder',
        'http://localhost:3000',
        'https://localhost:3000',
        'http://127.0.0.1:3000',
        'https://127.0.0.1:3000',
        'http://192.168.33.63:3000',
        'https://192.168.33.63:3000'
    ]
    
    # Enable CORS with proper configuration
    CORS(app, 
         origins=allowed_origins,
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "Origin"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Register routes
    register_routes(app)
    
    # Add status endpoint with special CORS handling
    @app.route('/api/status', methods=['GET', 'OPTIONS'])
    def status():
        # For OPTIONS request, return 200 OK with proper headers
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
            return response
        
        # For GET request
        try:
            connection_status = test_connection()
            return jsonify({
                'status': 'ok',
                'database_connected': connection_status,
                'env': app.config.get('ENV', 'not set')
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e),
                'database_connected': False,
                'env': app.config.get('ENV', 'not set')
            }), 500
    
    # Add a catch-all route for CORS preflight checks
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin in allowed_origins:
            response.headers.add('Access-Control-Allow-Origin', origin)
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    
    # Certifikatsökväg
    cert_path = "C:\\Dev\\cert"
    cert_file = os.path.join(cert_path, "cert.pem")
    key_file = os.path.join(cert_path, "key.pem")
    
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print(f"Found SSL certificates, running with HTTPS on port {port}")
        app.run(
            host='0.0.0.0', 
            port=port, 
            ssl_context=(cert_file, key_file), 
            debug=True
        )
    else:
        print(f"No SSL certificates found at {cert_path}, running with HTTP on port {port}")
        print("To enable HTTPS, create cert.pem and key.pem in the specified directory.")
        app.run(host='0.0.0.0', port=port, debug=True)