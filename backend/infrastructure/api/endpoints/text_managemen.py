# infrastructure/api/endpoints/text_management.py
from flask import jsonify, request
import traceback
import sys

def register_text_management_routes(app, text_management_service):
    """Register text management-related routes with the Flask app."""
    
    @app.route('/api/text/variables', methods=['GET'])
    def get_variables():
        try:
            print("GET /api/text/variables: Fetching variables")
            variables = text_management_service.get_all_variables()
            print(f"GET /api/text/variables: Retrieved {len(variables)} variables")
            return jsonify(variables)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting variables at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve variables', 'details': str(e)}), 500

    @app.route('/api/text/variables', methods=['POST'])
    def create_variable():
        try:
            variable_data = request.json
            if not variable_data:
                return jsonify({'error': 'No data provided'}), 400
            
            print(f"POST /api/text/variables: Creating variable with data: {variable_data}")
            
            variable = text_management_service.create_variable(variable_data)
            
            print(f"POST /api/text/variables: Variable created with ID {variable.get('id', 'unknown')}")
            
            return jsonify(variable), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error creating variable at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to create variable', 'details': str(e)}), 500

    @app.route('/api/text/variables/<int:variable_id>', methods=['GET'])
    def get_variable(variable_id):
        try:
            print(f"GET /api/text/variables/{variable_id}: Fetching variable")
            
            variable = text_management_service.get_variable_by_id(variable_id)
            
            if variable:
                print(f"GET /api/text/variables/{variable_id}: Retrieved variable {variable.get('namn', '')}")
                return jsonify(variable)
                
            print(f"GET /api/text/variables/{variable_id}: Variable not found")
            return jsonify({'error': 'Variable not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting variable {variable_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve variable', 'details': str(e)}), 500

    @app.route('/api/text/variables/<int:variable_id>', methods=['PUT'])
    def update_variable(variable_id):
        try:
            variable_data = request.json
            if not variable_data:
                return jsonify({'error': 'No data provided'}), 400
            
            print(f"PUT /api/text/variables/{variable_id}: Updating variable with data: {variable_data}")
            
            updated_variable = text_management_service.update_variable(variable_id, variable_data)
            
            if updated_variable:
                print(f"PUT /api/text/variables/{variable_id}: Variable updated")
                return jsonify(updated_variable)
                
            print(f"PUT /api/text/variables/{variable_id}: Variable not found")
            return jsonify({'error': 'Variable not found'}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating variable {variable_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update variable', 'details': str(e)}), 500

    @app.route('/api/text/variables/<int:variable_id>/comments', methods=['PUT'])
    def update_variable_comments(variable_id):
        try:
            data = request.json
            if not isinstance(data, dict) or 'comments' not in data:
                return jsonify({'error': 'Missing comments field in request data'}), 400
                
            print(f"PUT /api/text/variables/{variable_id}/comments: Setting comments to {data['comments']}")
            
            updated_variable = text_management_service.update_variable_comments(variable_id, data['comments'])
            
            if updated_variable:
                print(f"PUT /api/text/variables/{variable_id}/comments: Comments status updated to {data['comments']}")
                return jsonify({'message': 'Comments status updated successfully', 'variable': updated_variable})
                
            return jsonify({'error': 'Variable not found'}), 404
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating variable comments {variable_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update comments status', 'details': str(e)}), 500

    @app.route('/api/text/variables/<int:variable_id>', methods=['DELETE'])
    def delete_variable(variable_id):
        try:
            print(f"DELETE /api/text/variables/{variable_id}: Deleting variable")
            
            deleted = text_management_service.delete_variable(variable_id)
            
            if deleted:
                print(f"DELETE /api/text/variables/{variable_id}: Variable deleted")
                return '', 204
                
            print(f"DELETE /api/text/variables/{variable_id}: Variable not found")
            return jsonify({'error': 'Variable not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error deleting variable {variable_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to delete variable', 'details': str(e)}), 500