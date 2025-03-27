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
            # Additional logging for debugging
            print(f"Department service retrieved {len(departments)} departments")
            return departments
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department service get_all_departments at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            # Return empty list instead of failing
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
            # Validate input data
            if not department_data or not isinstance(department_data, dict):
                raise ValueError("Invalid department data format")
                
            if 'name' not in department_data or not department_data['name']:
                raise ValueError("Department name is required")
                
            # Ensure description exists even if it's None
            if 'description' not in department_data:
                department_data['description'] = None
                
            # Create the department
            department = self.repository.create(department_data)
            print(f"Created department: {department['name']} with ID {department['id']}")
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
            # Validate input data
            if not department_data or not isinstance(department_data, dict):
                raise ValueError("Invalid department data format")
                
            if 'name' not in department_data or not department_data['name']:
                raise ValueError("Department name is required")
                
            # Ensure description exists even if it's None
            if 'description' not in department_data:
                department_data['description'] = None
                
            # Update the department
            department = self.repository.update(department_id, department_data)
            
            if department:
                print(f"Updated department with ID {department['id']}")
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