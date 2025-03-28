from domain.repositories.department_repository import DepartmentRepository
import traceback
import sys

class DepartmentService:
    """Service for department operations."""
    
    def __init__(self):
        self.repository = DepartmentRepository()
    
    def get_all_departments(self):
        """Get all departments."""
        try:
            departments = self.repository.get_all()
            print(f"Department service retrieved {len(departments)} departments")
            return departments
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department service get_all_departments at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
    
    def get_departments_by_template(self, template_id):
        """Get departments for a specific template."""
        try:
            departments = self.repository.get_by_template_id(template_id)
            print(f"Retrieved {len(departments)} departments for template {template_id}")
            return departments
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department service get_departments_by_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []

    def get_department_by_id(self, department_id):
        """Get a department by ID."""
        try:
            department = self.repository.get_by_id(department_id)
            return department
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department service get_department_by_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return None
    
    def create_department(self, department_data):
        """Create a new department."""
        try:
            if not department_data or not isinstance(department_data, dict):
                raise ValueError("Invalid department data format")
                
            if 'name' not in department_data or not department_data['name']:
                raise ValueError("Department name is required")
                
            if 'description' not in department_data:
                department_data['description'] = None
                  
            if 'template_id' in department_data and department_data['template_id'] == '':
                department_data['template_id'] = None
                
            department = self.repository.create(department_data)
            print(f"Created department: {department['name']} with ID {department['id']}")
            if department.get('template_id'):
                print(f"  Associated with template ID: {department['template_id']}")
                
            return department
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department service create_department at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def update_department(self, department_id, department_data):
        """Update a department."""
        try:
            if not department_data or not isinstance(department_data, dict):
                raise ValueError("Invalid department data format")
                
            if 'name' not in department_data or not department_data['name']:
                raise ValueError("Department name is required")
                
            if 'description' not in department_data:
                department_data['description'] = None
                
            if 'template_id' in department_data and department_data['template_id'] == '':
                department_data['template_id'] = None
                
            department = self.repository.update(department_id, department_data)
            
            if department:
                print(f"Updated department with ID {department['id']}")
                if department.get('template_id'):
                    print(f"  Associated with template ID: {department['template_id']}")
            else:
                print(f"Department with ID {department_id} not found for update")
                
            return department
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department service update_department at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise

    def associate_with_template(self, department_id, template_id):
        """Associate a department with a template."""
        try:
            # Säkerställ att department_id är en sträng om det behövs
            department_id_str = str(department_id)
            
            # Om template_id inte är None, konvertera till integer
            # Detta är kritiskt för PostgreSQL som kräver rätt typ
            template_id_converted = int(template_id) if template_id is not None else None
            
            print(f"BEFORE CONVERSION - department_id: {department_id} ({type(department_id)}), template_id: {template_id} ({type(template_id)})")
            print(f"AFTER CONVERSION - department_id: {department_id_str} ({type(department_id_str)}), template_id: {template_id_converted} ({type(template_id_converted)})")
            
            result = self.repository.associate_with_template(department_id_str, template_id_converted)
            if result:
                print(f"Associated department {department_id} with template {template_id}")
            else:
                print(f"Failed to associate department {department_id} with template {template_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department service associate_with_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise

    def remove_template_association(self, department_id):
        """Remove the template association from a department."""
        try:
            result = self.repository.remove_template_association(department_id)
            if result:
                print(f"Removed template association from department {department_id}")
            else:
                print(f"Failed to remove template association from department {department_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department service remove_template_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def delete_department(self, department_id):
        """Delete a department."""
        try:
            success = self.repository.delete(department_id)
            if success:
                print(f"Deleted department with ID {department_id}")
            else:
                print(f"Department with ID {department_id} not found for deletion")
            return success
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department service delete_department at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise