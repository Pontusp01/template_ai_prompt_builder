from flask import jsonify, request
import traceback
import sys

def register_category_routes(app, category_service):
    """Register category-related routes with the Flask app."""
    
    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        try:
            print("GET /api/categories: Fetching categories")
            
            categories = category_service.get_all_categories()
            
            print(f"GET /api/categories: Retrieved {len(categories)} categories")
            
            return jsonify(categories)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting categories at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve categories', 'details': str(e)}), 500
    
    @app.route('/api/templates/<template_id>/categories', methods=['GET'])
    def get_categories_by_template(template_id):
        try:
            print(f"GET /api/templates/{template_id}/categories: Fetching categories for template")
            categories = category_service.get_categories_by_template(template_id)
            print(f"GET /api/templates/{template_id}/categories: Retrieved {len(categories)} categories")
            return jsonify(categories)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting categories for template {template_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve categories', 'details':str(e)}), 500

    @app.route('/api/categories', methods=['POST'])
    def create_category():
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            print(f"POST /api/categories: Creating category with data: {data}")
            
            category = category_service.create_category(data)
            
            print(f"POST /api/categories: Category created with ID {category.get('id', 'unknown')}")
            
            return jsonify(category), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error creating category at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to create category', 'details': str(e)}), 500
    
    @app.route('/api/categories/<category_id>', methods=['GET'])
    def get_category(category_id):
        try:
            category = category_service.get_category_by_id(category_id)
            
            if category:
                return jsonify(category)
            return jsonify({'error': 'Category not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting category {category_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve category', 'details': str(e)}), 500
    
    @app.route('/api/categories/<category_id>', methods=['PUT'])
    def update_category(category_id):
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            print(f"PUT /api/categories/{category_id}: Received data: {data}")
            print(f"Category ID type: {type(category_id)}")
            
            # If this is a template association request
            if 'template_id' in data and len(data) == 1:
                template_id = data['template_id']
                print(f"PUT /api/categories/{category_id}: Associating with template {template_id} (Type: {type(template_id)})")
                
                # VIKTIGT: Hantera tom sträng som NULL-värde
                if template_id == '':
                    print(f"Empty template_id detected, will set to NULL")
                    # Anropa remove_template_association istället för associate_with_template
                    success = category_service.remove_template_association(category_id)
                    if success:
                        return jsonify({'message': 'Template association removed successfully'})
                    return jsonify({'error': 'Failed to remove template association'}), 400
                else:
                    try:
                        # Testa om template_id kan konverteras till integer
                        int(template_id)
                        success = category_service.associate_with_template(category_id, template_id)
                        if success:
                            return jsonify({'message': 'Template associated successfully'})
                        return jsonify({'error': 'Failed to associate template'}), 400
                    except ValueError:
                        return jsonify({'error': 'Invalid template ID format'}), 400
            
            # Regular update  
            category = category_service.update_category(category_id, data)
            
            if category:
                print(f"PUT /api/categories/{category_id}: Updated")
                return jsonify(category)
            return jsonify({'error': 'Category not found'}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating category {category_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update category', 'details': str(e)}), 500
        
    @app.route('/api/categories/<category_id>', methods=['DELETE'])
    def delete_category(category_id):
        try:
            success = category_service.delete_category(category_id)
            if success:
                return jsonify({'message': 'Category deleted successfully'})
            return jsonify({'error': 'Category not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error deleting category {category_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to delete category', 'details': str(e)}), 500