from flask import jsonify, request
import traceback
import sys

def register_completion_type_routes(app, completion_type_service):
    """Register completion type-related routes with the Flask app."""
    
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
            
            # Debug logging
            print(f"POST /api/completion-types: Received data: {data}") 
            
            completion_type = completion_type_service.create_completion_type(data)
            print(f"POST /api/completion-types: Created with ID {completion_type.get('id', 'unknown')}")
            
            return jsonify(completion_type), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error creating completion type at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to create', 'details': str(e)}), 500
    
    @app.route('/api/completion-types/<completion_type_id>', methods=['GET'])
    def get_completion_type(completion_type_id):
        try:
            completion_type = completion_type_service.get_completion_type_by_id(completion_type_id)
            
            if completion_type:
                return jsonify(completion_type)
            return jsonify({'error': 'Completion type not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]  
            print(f"Error getting {completion_type_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve', 'details': str(e)}), 500
    
    @app.route('/api/completion-types/<completion_type_id>', methods=['PUT'])
    def update_completion_type(completion_type_id):
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            print(f"PUT /api/completion-types/{completion_type_id}: Received data: {data}")
            
            # If this is a template association request
            if 'template_id' in data and len(data) == 1:
                print(f"PUT /api/completion-types/{completion_type_id}: Associating with template {data['template_id']}")
                success = completion_type_service.associate_with_template(completion_type_id, data['template_id'])
                
                if success:
                    return jsonify({'message': 'Template associated successfully'})
                return jsonify({'error': 'Failed to associate template'}), 400
            
            # Regular update
            if 'name' in data and not data['name'].strip():
                return jsonify({'error': 'Completion type name is required'}), 400
                        
            completion_type = completion_type_service.update_completion_type(completion_type_id, data)
            
            if completion_type:
                print(f"PUT /api/{completion_type_id}: Updated")
                return jsonify(completion_type)
            return jsonify({'error': 'Completion type not found'}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0] 
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating {completion_type_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update', 'details': str(e)}), 500
    
    @app.route('/api/completion-types/<completion_type_id>', methods=['DELETE'])
    def delete_completion_type(completion_type_id):
        try:
            success = completion_type_service.delete_completion_type(completion_type_id)
            if success:
                return jsonify({'message': 'Completion type deleted'})  
            return jsonify({'error': 'Completion type not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error deleting {completion_type_id} at {fname}:{line}: {e}") 
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to delete', 'details': str(e)}), 500