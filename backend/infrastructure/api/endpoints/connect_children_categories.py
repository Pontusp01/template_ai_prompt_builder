from flask import jsonify, request
import traceback
import sys

def register_connect_children_categories_routes(app, connect_children_category_service):
    """Register children categories-related routes with the Flask app."""
    
    @app.route('/api/children-categories', methods=['GET'])
    def get_children_categories():
        try:
            print("GET /api/children-categories: Fetching children categories")
            
            categories = connect_children_category_service.get_all_categories()
            
            print(f"GET /api/children-categories: Retrieved {len(categories)} categories")
            
            return jsonify(categories)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting children categories at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve children categories', 'details': str(e)}), 500
    
    @app.route('/api/completion-types/<completion_type_id>/children-categories', methods=['GET'])
    def get_categories_by_completion_type(completion_type_id):
        try:
            print(f"GET /api/completion-types/{completion_type_id}/children-categories: Fetching categories for completion type")
            categories = connect_children_category_service.get_categories_by_completion_type(completion_type_id)
            print(f"GET /api/completion-types/{completion_type_id}/children-categories: Retrieved {len(categories)} categories")
            return jsonify(categories)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting categories for completion type {completion_type_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve children categories', 'details':str(e)}), 500
    
    @app.route('/api/departments/<department_id>/children-categories', methods=['GET'])
    def get_categories_by_department(department_id):
        try:
            print(f"GET /api/departments/{department_id}/children-categories: Fetching categories for department")
            categories = connect_children_category_service.get_categories_by_department(department_id)
            print(f"GET /api/departments/{department_id}/children-categories: Retrieved {len(categories)} categories")
            return jsonify(categories)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting categories for department {department_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve children categories', 'details':str(e)}), 500
            
    @app.route('/api/children-categories', methods=['POST'])
    def create_children_category():
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            print(f"POST /api/children-categories: Creating children category with data: {data}")
            
            category = connect_children_category_service.create_category(data)
            
            print(f"POST /api/children-categories: Children category created with ID {category.get('id', 'unknown')}")
            
            return jsonify(category), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error creating children category at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to create children category', 'details': str(e)}), 500
    
    @app.route('/api/children-categories/<category_id>', methods=['GET'])
    def get_children_category(category_id):
        try:
            category = connect_children_category_service.get_category_by_id(category_id)
            
            if category:
                return jsonify(category)
            return jsonify({'error': 'Children category not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting children category {category_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve children category', 'details': str(e)}), 500
    
    @app.route('/api/children-categories/<category_id>', methods=['PUT'])
    def update_children_category(category_id):
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            print(f"PUT /api/children-categories/{category_id}: Received data: {data}")
            print(f"Category ID type: {type(category_id)}")
            
            # If this is a completion type association request
            if 'completion_type_id' in data and len(data) == 1:
                completion_type_id = data['completion_type_id']
                print(f"PUT /api/children-categories/{category_id}: Associating with completion type {completion_type_id} (Type: {type(completion_type_id)})")
                
                # Handle empty string as NULL value
                if completion_type_id == '':
                    print(f"Empty completion_type_id detected, will set to NULL")
                    # Call remove_completion_type_association instead of associate_with_completion_type
                    success = connect_children_category_service.remove_completion_type_association(category_id)
                    if success:
                        return jsonify({'message': 'Completion type association removed successfully'})
                    return jsonify({'error': 'Failed to remove completion type association'}), 400
                else:
                    try:
                        # Test if completion_type_id can be converted to integer
                        int(completion_type_id)
                        success = connect_children_category_service.associate_with_completion_type(category_id, completion_type_id)
                        if success:
                            return jsonify({'message': 'Completion type associated successfully'})
                        return jsonify({'error': 'Failed to associate completion type'}), 400
                    except ValueError:
                        return jsonify({'error': 'Invalid completion type ID format'}), 400
            
            # If this is a department association request
            if 'department_id' in data and len(data) == 1:
                department_id = data['department_id']
                print(f"PUT /api/children-categories/{category_id}: Associating with department {department_id} (Type: {type(department_id)})")
                
                # Handle empty string as NULL value
                if department_id == '':
                    print(f"Empty department_id detected, will set to NULL")
                    # Call remove_department_association
                    success = connect_children_category_service.remove_department_association(category_id)
                    if success:
                        return jsonify({'message': 'Department association removed successfully'})
                    return jsonify({'error': 'Failed to remove department association'}), 400
                else:
                    try:
                        # Ensure department_id is in the correct format
                        success = connect_children_category_service.associate_with_department(category_id, department_id)
                        if success:
                            return jsonify({'message': 'Department associated successfully'})
                        return jsonify({'error': 'Failed to associate department'}), 400
                    except ValueError:
                        return jsonify({'error': 'Invalid department ID format'}), 400
            
            # Regular update  
            category = connect_children_category_service.update_category(category_id, data)
            
            if category:
                print(f"PUT /api/children-categories/{category_id}: Updated")
                return jsonify(category)
            return jsonify({'error': 'Children category not found'}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating children category {category_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update children category', 'details': str(e)}), 500
        
    @app.route('/api/children-categories/<category_id>', methods=['DELETE'])
    def delete_children_category(category_id):
        try:
            success = connect_children_category_service.delete_category(category_id)
            if success:
                return jsonify({'message': 'Children category deleted successfully'})
            return jsonify({'error': 'Children category not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error deleting children category {category_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to delete children category', 'details': str(e)}), 500