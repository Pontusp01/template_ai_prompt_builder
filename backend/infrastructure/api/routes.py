from flask import Blueprint, jsonify, request, current_app
from application.services.template_service import TemplateService
from application.services.department_service import DepartmentService
from application.services.color_service import ColorService
from application.services.completion_type_service import CompletionTypeService
from infrastructure.api.endpoints import (
    register_department_routes,
    register_template_routes,
    register_color_routes,
    register_completion_type_routes,
    register_debug_routes
)

def register_routes(app):
    """Register all routes with the Flask app."""
    
    # Create services
    template_service = TemplateService()
    department_service = DepartmentService()
    color_service = ColorService()
    completion_type_service = CompletionTypeService()
    
    # Register all routes
    register_department_routes(app, department_service)
    register_template_routes(app, template_service)
    register_color_routes(app, color_service)
    register_completion_type_routes(app, completion_type_service)
    register_debug_routes(app)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        import datetime
        return jsonify({
            'status': 'ok',
            'version': '1.0.0',
            'timestamp': datetime.datetime.now().isoformat()
        })