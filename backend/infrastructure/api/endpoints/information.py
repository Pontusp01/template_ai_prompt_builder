from flask import jsonify, request
import traceback
import sys

def register_information_routes(app, information_service):
    """Register information-related routes with the Flask app."""
    
    @app.route('/api/information', methods=['GET'])
    def get_information():
        try:
            print("GET /api/information: Fetching information items")
            
            information_items = information_service.get_all_information()
            
            print(f"GET /api/information: Retrieved {len(information_items)} information items")
            
            return jsonify(information_items)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting information at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve information items', 'details': str(e)}), 500
    
    @app.route('/api/templates/<template_id>/information', methods=['GET'])
    def get_information_by_template(template_id):
        try:
            print(f"GET /api/templates/{template_id}/information: Fetching information items for template")
            information_items = information_service.get_information_by_template(template_id)
            print(f"GET /api/templates/{template_id}/information: Retrieved {len(information_items)} information items")
            return jsonify(information_items)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting information for template {template_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve information items', 'details':str(e)}), 500

    @app.route('/api/information', methods=['POST'])
    def create_information():
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            print(f"POST /api/information: Creating information item with data: {data}")
            
            information = information_service.create_information(data)
            
            print(f"POST /api/information: Information item created with ID {information.get('id', 'unknown')}")
            
            return jsonify(information), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error creating information at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to create information item', 'details': str(e)}), 500
    
    @app.route('/api/information/<information_id>', methods=['GET'])
    def get_information_item(information_id):
        try:
            information = information_service.get_information_by_id(information_id)
            
            if information:
                return jsonify(information)
            return jsonify({'error': 'Information item not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting information {information_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve information item', 'details': str(e)}), 500
    
    @app.route('/api/information/<information_id>', methods=['PUT'])
    def update_information(information_id):
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            print(f"PUT /api/information/{information_id}: Received data: {data}")
            print(f"Information ID type: {type(information_id)}")
            
            # If this is a template association request
            if 'template_id' in data and len(data) == 1:
                template_id = data['template_id']
                print(f"PUT /api/information/{information_id}: Associating with template {template_id} (Type: {type(template_id)})")
                
                # VIKTIGT: Hantera tom sträng som NULL-värde
                if template_id == '':
                    print(f"Empty template_id detected, will set to NULL")
                    # Anropa remove_template_association istället för associate_with_template
                    success = information_service.remove_template_association(information_id)
                    if success:
                        return jsonify({'message': 'Template association removed successfully'})
                    return jsonify({'error': 'Failed to remove template association'}), 400
                else:
                    try:
                        # Testa om template_id kan konverteras till integer
                        int(template_id)
                        success = information_service.associate_with_template(information_id, template_id)
                        if success:
                            return jsonify({'message': 'Template associated successfully'})
                        return jsonify({'error': 'Failed to associate template'}), 400
                    except ValueError:
                        return jsonify({'error': 'Invalid template ID format'}), 400
            
            # Regular update  
            information = information_service.update_information(information_id, data)
            
            if information:
                print(f"PUT /api/information/{information_id}: Updated")
                return jsonify(information)
            return jsonify({'error': 'Information item not found'}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating information {information_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update information item', 'details': str(e)}), 500
        
    @app.route('/api/information/<information_id>/comments', methods=['PUT'])
    def update_information_comments(information_id):
        try:
            data = request.json
            if not isinstance(data, dict) or 'comments' not in data:
                return jsonify({'error': 'Missing comments field in request data'}), 400
                
            print(f"PUT /api/information/{information_id}/comments: Setting comments to {data['comments']}")
            
            # Hämta existerande information
            info = information_service.get_information_by_id(information_id)
            if not info:
                return jsonify({'error': 'Information item not found'}), 404
                
            # Uppdatera endast comments-fältet
            update_data = {
                'name': info['name'],
                'label': info.get('label'),
                'description': info.get('description'),
                'template_id': info.get('template_id'),
                'comments': data['comments']
            }
            
            information = information_service.update_information(information_id, update_data)
            
            if information:
                return jsonify({'message': 'Comments status updated successfully', 'information': information})
            return jsonify({'error': 'Failed to update comments status'}), 500
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating information comments {information_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update comments status', 'details': str(e)}), 500
        
    @app.route('/api/information/<information_id>', methods=['DELETE'])
    def delete_information(information_id):
        try:
            success = information_service.delete_information(information_id)
            if success:
                return jsonify({'message': 'Information item deleted successfully'})
            return jsonify({'error': 'Information item not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error deleting information {information_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to delete information item', 'details': str(e)}), 500