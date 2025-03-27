from flask import Blueprint, jsonify, request, current_app
from application.services.template_service import TemplateService
from application.services.department_service import DepartmentService
from application.services.color_service import ColorService
from application.services.completion_type_service import CompletionTypeService
import traceback
import sys

def register_routes(app):
    """Register all routes with the Flask app."""
    
    # Create services
    template_service = TemplateService()
    department_service = DepartmentService()
    color_service = ColorService()
    completion_type_service = CompletionTypeService()
    
    # Templates routes
    @app.route('/api/templates', methods=['GET'])
    def get_templates():
        try:
            templates = template_service.get_all_templates()
            return jsonify(templates)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting templates at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve templates', 'details': str(e)}), 500
    
    @app.route('/api/templates/<template_id>', methods=['GET'])
    def get_template(template_id):
        try:
            template = template_service.get_template_by_id(template_id)
            if template:
                return jsonify(template)
            return jsonify({'error': 'Template not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting template {template_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve template', 'details': str(e)}), 500
    
    @app.route('/api/templates', methods=['POST'])
    def create_template():
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            print(f"POST /api/templates: Creating template with data: {data}")
            
            template = template_service.create_template(data)
            return jsonify(template), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error creating template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to create template', 'details': str(e)}), 500
    
    @app.route('/api/templates/<template_id>', methods=['PUT'])
    def update_template(template_id):
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
                
            print(f"PUT /api/templates/{template_id}: Updating template with data: {data}")
            
            template = template_service.update_template(template_id, data)
            if template:
                return jsonify(template)
            return jsonify({'error': 'Template not found'}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating template {template_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update template', 'details': str(e)}), 500
    
    @app.route('/api/templates/<template_id>', methods=['DELETE'])
    def delete_template(template_id):
        try:
            success = template_service.delete_template(template_id)
            if success:
                return jsonify({'message': 'Template deleted'})
            return jsonify({'error': 'Template not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error deleting template {template_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to delete template', 'details': str(e)}), 500
    
    # Template color routes
    @app.route('/api/templates/<template_id>/color', methods=['PUT'])
    def update_template_color(template_id):
        try:
            data = request.json
            if not data or 'color_id' not in data:
                return jsonify({'error': 'No color_id provided'}), 400
            
            print(f"PUT /api/templates/{template_id}/color: Updating color to {data['color_id']}")
            
            success = template_service.update_template_color(template_id, data['color_id'])
            if success:
                return jsonify({'message': f'Template {template_id} color updated to {data["color_id"]}'})
            return jsonify({'error': 'Failed to update template color'}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating template {template_id} color at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update template color', 'details': str(e)}), 500
    
    @app.route('/api/templates/<template_id>/color', methods=['DELETE'])
    def remove_template_color(template_id):
        try:
            success = template_service.remove_template_color(template_id)
            if success:
                return jsonify({'message': f'Color removed from template {template_id}'})
            return jsonify({'error': 'Failed to remove color from template'}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error removing color from template {template_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to remove color from template', 'details': str(e)}), 500
    
    # Template completion type association routes
    @app.route('/api/templates/<template_id>/completion-types/<completion_type_id>', methods=['PUT'])
    def associate_completion_type(template_id, completion_type_id):
        try:
            success = template_service.associate_completion_type(template_id, completion_type_id)
            if success:
                return jsonify({'message': f'Completion type {completion_type_id} associated with template {template_id}'})
            return jsonify({'error': 'Failed to associate completion type with template'}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error associating completion type {completion_type_id} with template {template_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to associate completion type with template', 'details': str(e)}), 500
    
    @app.route('/api/templates/<template_id>/completion-types/<completion_type_id>', methods=['DELETE'])
    def remove_completion_type_association(template_id, completion_type_id):
        try:
            success = template_service.remove_completion_type_association(template_id, completion_type_id)
            if success:
                return jsonify({'message': f'Completion type {completion_type_id} association removed from template {template_id}'})
            return jsonify({'error': 'Failed to remove completion type association from template'}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error removing completion type {completion_type_id} association from template {template_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to remove completion type association from template', 'details': str(e)}), 500
    
    @app.route('/api/templates/<template_id>/completion-types', methods=['PUT'])
    def update_template_completion_types(template_id):
        try:
            data = request.json
            if not data or 'completion_type_ids' not in data:
                return jsonify({'error': 'No completion_type_ids provided'}), 400
            
            success = template_service.update_template_completion_types(template_id, data['completion_type_ids'])
            if success:
                return jsonify({'message': f'Template {template_id} completion types updated'})
            return jsonify({'error': 'Failed to update template completion types'}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating template {template_id} completion types at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update template completion types', 'details': str(e)}), 500
    
    # Departments routes
    @app.route('/api/departments', methods=['GET'])
    def get_departments():
        try:
            # Add logging before making service call
            print("GET /api/departments: Fetching departments")
            
            departments = department_service.get_all_departments()
            
            # Add logging after service call
            print(f"GET /api/departments: Retrieved {len(departments)} departments")
            
            return jsonify(departments)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting departments at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve departments', 'details': str(e)}), 500
    
    @app.route('/api/departments', methods=['POST'])
    def create_department():
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Add logging for debugging
            print(f"POST /api/departments: Creating department with data: {data}")
            
            department = department_service.create_department(data)
            
            print(f"POST /api/departments: Department created with ID {department.get('id', 'unknown')}")
            
            return jsonify(department), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error creating department at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to create department', 'details': str(e)}), 500
    
    # Colors routes
    @app.route('/api/colors', methods=['GET'])
    def get_colors():
        try:
            print("GET /api/colors: Fetching colors")
            colors = color_service.get_all_colors()
            print(f"GET /api/colors: Retrieved {len(colors)} colors")
            return jsonify(colors)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting colors at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve colors', 'details': str(e)}), 500
    
    @app.route('/api/colors', methods=['POST'])
    def create_color():
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Enhanced debug logging
            print(f"POST /api/colors: Received data: {data}")
            
            color = color_service.create_color(data)
            print(f"POST /api/colors: Created color with ID {color.get('id', 'unknown')} and hex_value {color.get('hex_value', 'unknown')}")
            
            return jsonify(color), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error creating color at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to create color', 'details': str(e)}), 500
    
    @app.route('/api/colors/<color_id>', methods=['GET'])
    def get_color(color_id):
        try:
            # Get a single color
            colors = color_service.get_all_colors()
            color = next((c for c in colors if str(c['id']) == str(color_id)), None)
            
            if color:
                return jsonify(color)
            return jsonify({'error': 'Color not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting color {color_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve color', 'details': str(e)}), 500
    
    @app.route('/api/colors/<color_id>', methods=['PUT'])
    def update_color(color_id):
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Enhanced debug logging
            print(f"PUT /api/colors/{color_id}: Received data: {data}")
            
            color = color_service.update_color(color_id, data)
            
            if color:
                print(f"PUT /api/colors/{color_id}: Updated color with hex_value {color.get('hex_value', 'unknown')}")
                return jsonify(color)
            return jsonify({'error': 'Color not found'}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating color {color_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update color', 'details': str(e)}), 500
    
    @app.route('/api/colors/<color_id>', methods=['DELETE'])
    def delete_color(color_id):
        try:
            success = color_service.delete_color(color_id)
            
            if success:
                return jsonify({'message': 'Color deleted'})
            return jsonify({'error': 'Color not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error deleting color {color_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to delete color', 'details': str(e)}), 500
    
    # Completion types routes
    @app.route('/api/completion-types', methods=['GET'])
    def get_completion_types():
        try:
            print("GET /api/completion-types: Fetching completion types")
            completion_types = completion_type_service.get_all_completion_types()
            print(f"GET /api/completion-types: Retrieved {len(completion_types)} completion types")
            return jsonify(completion_types)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting completion types at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve completion types', 'details':str(e)}), 500
    
    @app.route('/api/completion-types', methods=['POST'])
    def create_completion_type():
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Enhanced debug logging
            print(f"POST /api/completion-types: Received data: {data}")
            
            completion_type = completion_type_service.create_completion_type(data)
            print(f"POST /api/completion-types: Created completion type with ID {completion_type.get('id', 'unknown')}")
            
            return jsonify(completion_type), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error creating completion type at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to create completion type', 'details': str(e)}), 500
    
    @app.route('/api/completion-types/<completion_type_id>', methods=['GET'])
    def get_completion_type(completion_type_id):
        try:
            # Get a single completion type
            completion_types = completion_type_service.get_all_completion_types()
            completion_type = next((ct for ct in completion_types if str(ct['id']) == str(completion_type_id)), None)
            
            if completion_type:
                return jsonify(completion_type)
            return jsonify({'error': 'Completion type not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting completion type {completion_type_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve completion type', 'details': str(e)}), 500
    
    @app.route('/api/completion-types/<completion_type_id>', methods=['PUT'])
    def update_completion_type(completion_type_id):
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Enhanced debug logging
            print(f"PUT /api/completion-types/{completion_type_id}: Received data: {data}")
            
            completion_type = completion_type_service.update_completion_type(completion_type_id, data)
            
            if completion_type:
                print(f"PUT /api/completion-types/{completion_type_id}: Updated completion type")
                return jsonify(completion_type)
            return jsonify({'error': 'Completion type not found'}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating completion type {completion_type_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update completion type', 'details': str(e)}), 500
    
    @app.route('/api/completion-types/<completion_type_id>', methods=['DELETE'])
    def delete_completion_type(completion_type_id):
        try:
            # Implementera delete_completion_type om du behöver ta bort completion types
            # OBS: Denna funktion behöver läggas till i CompletionTypeService
            return jsonify({'error': 'Not implemented yet'}), 501
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error deleting completion type {completion_type_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to delete completion type', 'details': str(e)}), 500
    
    @app.route('/api/templates/<template_id>/completion-types', methods=['GET'])
    def get_template_completion_types(template_id):
        try:
            # Hämta template och returnera dess completion types
            template = template_service.get_template_by_id(template_id)
            if not template:
                return jsonify({'error': 'Template not found'}), 404
                
            if 'completion_types' in template:
                return jsonify(template['completion_types'])
            else:
                return jsonify([])
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting completion types for template {template_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve completion types for template', 'details': str(e)}), 500
    
    # Debug/status endpoint
    @app.route('/api/debug/db-status', methods=['GET'])
    def check_db_status():
        try:
            from infrastructure.database.connection import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if we can connect to the database
            cursor.execute("SELECT 1")
            db_connect = cursor.fetchone() is not None
            
            # Check which tables exist
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = [row[0] if isinstance(row, tuple) else row['table_name'] for row in cursor.fetchall()]
            
            # Check column structure of templates table
            template_columns = []
            if 'templates' in tables:
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'templates'
                """)
                template_columns = [
                    {'name': row[0] if isinstance(row, tuple) else row['column_name'], 
                     'type': row[1] if isinstance(row, tuple) else row['data_type']}
                    for row in cursor.fetchall()
                ]
            
            # Check column structure of colors table
            color_columns = []
            if 'colors' in tables:
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'colors'
                """)
                color_columns = [
                    {'name': row[0] if isinstance(row, tuple) else row['column_name'], 
                     'type': row[1] if isinstance(row, tuple) else row['data_type']}
                    for row in cursor.fetchall()
                ]
            
            # Check column structure of completion_types table
            completion_type_columns = []
            if 'completion_types' in tables:
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'completion_types'
                """)
                completion_type_columns = [
                    {'name': row[0] if isinstance(row, tuple) else row['column_name'], 
                     'type': row[1] if isinstance(row, tuple) else row['data_type']}
                    for row in cursor.fetchall()
                ]
            
            cursor.close()
            conn.close()
            
            return jsonify({
                'database_connected': db_connect,
                'tables': tables,
                'template_columns': template_columns,
                'color_columns': color_columns,
                'completion_type_columns': completion_type_columns
            })
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error checking database status at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to check database status', 'details': str(e)}), 500
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'ok',
            'version': '1.0.0',
            'timestamp': import_module('datetime').datetime.now().isoformat()
        })
    
    # Import utility for health check
    import_module = __import__