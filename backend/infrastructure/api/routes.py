from flask import Blueprint, jsonify, request, current_app
from application.services.template_service import TemplateService
from application.services.department_service import DepartmentService
from application.services.color_service import ColorService
from application.services.completion_type_service import CompletionTypeService
from application.services.text_management_service import TextManagementService
from application.services.connect_children_categories_service import ConnectChildrenCategoryService

from infrastructure.api.endpoints import (
    register_department_routes,
    register_template_routes,
    register_color_routes,
    register_completion_type_routes,
    register_text_management_routes,
    register_debug_routes,
    register_connect_children_categories_routes
)

def register_routes(app):
    """Register all routes with the Flask app."""
    
    # Create services
    template_service = TemplateService()
    department_service = DepartmentService()
    color_service = ColorService()
    completion_type_service = CompletionTypeService()
    text_management_service = TextManagementService()
    connect_children_category_service = ConnectChildrenCategoryService()
    
    # Register all routes
    register_department_routes(app, department_service)
    register_template_routes(app, template_service)
    register_color_routes(app, color_service)
    register_completion_type_routes(app, completion_type_service)
    register_text_management_routes(app, text_management_service)
    register_connect_children_categories_routes(app, connect_children_category_service)
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