from flask import jsonify, request
import traceback
import sys

def register_department_routes(app, department_service):
    """Register department-related routes with the Flask app."""
    
    @app.route('/api/departments', methods=['GET'])
    def get_departments():
        try:
            print("GET /api/departments: Fetching departments")
            
            departments = department_service.get_all_departments()
            
            print(f"GET /api/departments: Retrieved {len(departments)} departments")
            
            return jsonify(departments)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting departments at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve departments', 'details': str(e)}), 500
    
    @app.route('/api/templates/<template_id>/departments', methods=['GET'])
    def get_departments_by_template(template_id):
        try:
            print(f"GET /api/templates/{template_id}/departments: Fetching departments for template")
            departments = department_service.get_departments_by_template(template_id)
            print(f"GET /api/templates/{template_id}/departments: Retrieved {len(departments)} departments")
            return jsonify(departments)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting departments for template {template_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve departments', 'details':str(e)}), 500

    @app.route('/api/departments', methods=['POST'])
    def create_department():
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
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
    
    @app.route('/api/departments/<department_id>', methods=['GET'])
    def get_department(department_id):
        try:
            department = department_service.get_department_by_id(department_id)
            
            if department:
                return jsonify(department)
            return jsonify({'error': 'Department not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting department {department_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve department', 'details': str(e)}), 500
    
    # Uppdatering till routes.py - update_department
    @app.route('/api/departments/<department_id>', methods=['PUT'])
    def update_department(department_id):
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            print(f"PUT /api/departments/{department_id}: Received data: {data}")
            print(f"Department ID type: {type(department_id)}")
            
            # If this is a template association request
            if 'template_id' in data and len(data) == 1:
                template_id = data['template_id']
                print(f"PUT /api/departments/{department_id}: Associating with template {template_id} (Type: {type(template_id)})")
                
                # VIKTIGT: Hantera tom sträng som NULL-värde
                if template_id == '':
                    print(f"Empty template_id detected, will set to NULL")
                    # Anropa remove_template_association istället för associate_with_template
                    success = department_service.remove_template_association(department_id)
                    if success:
                        return jsonify({'message': 'Template association removed successfully'})
                    return jsonify({'error': 'Failed to remove template association'}), 400
                else:
                    try:
                        # Testa om template_id kan konverteras till integer
                        int(template_id)
                        success = department_service.associate_with_template(department_id, template_id)
                        if success:
                            return jsonify({'message': 'Template associated successfully'})
                        return jsonify({'error': 'Failed to associate template'}), 400
                    except ValueError:
                        return jsonify({'error': 'Invalid template ID format'}), 400
            
            # Regular update  
            department = department_service.update_department(department_id, data)
            
            if department:
                print(f"PUT /api/departments/{department_id}: Updated")
                return jsonify(department)
            return jsonify({'error': 'Department not found'}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating department {department_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update department', 'details': str(e)}), 500
        
    @app.route('/api/departments/<department_id>', methods=['DELETE'])
    def delete_department(department_id):
        try:
            success = department_service.delete_department(department_id)
            if success:
                return jsonify({'message': 'Department deleted successfully'})
            return jsonify({'error': 'Department not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error deleting department {department_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to delete department', 'details': str(e)}), 500