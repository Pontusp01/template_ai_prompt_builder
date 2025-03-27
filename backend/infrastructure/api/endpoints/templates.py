from flask import jsonify, request
import traceback
import sys

def register_template_routes(app, template_service):
    """Register template-related routes with the Flask app."""
    
    # Templates main routes
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
    
    # Template completion type routes
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