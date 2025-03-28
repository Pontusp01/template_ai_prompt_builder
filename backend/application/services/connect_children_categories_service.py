from domain.repositories.connect_children_categories_repository import ConnectChildrenCategoryRepository
import traceback
import sys

class ConnectChildrenCategoryService:
    """Service for children categories operations."""
    
    def __init__(self):
        self.repository = ConnectChildrenCategoryRepository()
    
    def get_all_categories(self):
        """Get all children categories."""
        try:
            categories = self.repository.get_all()
            print(f"Children category service retrieved {len(categories)} categories")
            return categories
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in children category service get_all_categories at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
    
    def get_categories_by_completion_type(self, completion_type_id):
        """Get children categories for a specific completion type."""
        try:
            categories = self.repository.get_by_completion_type_id(completion_type_id)
            print(f"Retrieved {len(categories)} categories for completion type {completion_type_id}")
            return categories
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in children category service get_categories_by_completion_type at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []

    def get_categories_by_department(self, department_id):
        """Get children categories for a specific department."""
        try:
            categories = self.repository.get_by_department_id(department_id)
            print(f"Retrieved {len(categories)} categories for department {department_id}")
            return categories
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in children category service get_categories_by_department at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []

    def get_category_by_id(self, category_id):
        """Get a category by ID."""
        try:
            category = self.repository.get_by_id(category_id)
            return category
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in children category service get_category_by_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return None
    
    def create_category(self, category_data):
        """Create a new children category."""
        try:
            if not category_data or not isinstance(category_data, dict):
                raise ValueError("Invalid category data format")
                
            if 'name' not in category_data or not category_data['name']:
                raise ValueError("Category name is required")
                
            if 'description' not in category_data:
                category_data['description'] = None
                  
            if 'completion_type_id' in category_data and category_data['completion_type_id'] == '':
                category_data['completion_type_id'] = None
                
            if 'department_id' in category_data and category_data['department_id'] == '':
                category_data['department_id'] = None
                
            category = self.repository.create(category_data)
            print(f"Created children category: {category['name']} with ID {category['id']}")
            
            if category.get('completion_type_id'):
                print(f"  Associated with completion type ID: {category['completion_type_id']}")
                
            if category.get('department_id'):
                print(f"  Associated with department ID: {category['department_id']}")
                
            return category
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in children category service create_category at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def update_category(self, category_id, category_data):
        """Update a children category."""
        try:
            if not category_data or not isinstance(category_data, dict):
                raise ValueError("Invalid category data format")
                
            if 'name' not in category_data or not category_data['name']:
                raise ValueError("Category name is required")
                
            if 'description' not in category_data:
                category_data['description'] = None
                
            if 'completion_type_id' in category_data and category_data['completion_type_id'] == '':
                category_data['completion_type_id'] = None
                
            if 'department_id' in category_data and category_data['department_id'] == '':
                category_data['department_id'] = None
                
            category = self.repository.update(category_id, category_data)
            
            if category:
                print(f"Updated children category with ID {category['id']}")
                
                if category.get('completion_type_id'):
                    print(f"  Associated with completion type ID: {category['completion_type_id']}")
                    
                if category.get('department_id'):
                    print(f"  Associated with department ID: {category['department_id']}")
            else:
                print(f"Children category with ID {category_id} not found for update")
                
            return category
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in children category service update_category at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise

    def associate_with_completion_type(self, category_id, completion_type_id):
        """Associate a children category with a completion type."""
        try:
            # Ensure category_id is a string if needed
            category_id_str = str(category_id)
            
            # If completion_type_id is not None, convert to integer
            # This is critical for PostgreSQL which requires correct types
            completion_type_id_converted = int(completion_type_id) if completion_type_id is not None else None
            
            print(f"BEFORE CONVERSION - category_id: {category_id} ({type(category_id)}), completion_type_id: {completion_type_id} ({type(completion_type_id)})")
            print(f"AFTER CONVERSION - category_id: {category_id_str} ({type(category_id_str)}), completion_type_id: {completion_type_id_converted} ({type(completion_type_id_converted)})")
            
            result = self.repository.associate_with_completion_type(category_id_str, completion_type_id_converted)
            if result:
                print(f"Associated children category {category_id} with completion type {completion_type_id}")
            else:
                print(f"Failed to associate children category {category_id} with completion type {completion_type_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in children category service associate_with_completion_type at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise

    def associate_with_department(self, category_id, department_id):
        """Associate a children category with a department."""
        try:
            # Ensure category_id is a string if needed
            category_id_str = str(category_id)
            
            # If department_id is not None, ensure it's in the correct format
            # This is critical for PostgreSQL which requires correct types
            department_id_converted = str(department_id) if department_id is not None else None
            
            print(f"BEFORE CONVERSION - category_id: {category_id} ({type(category_id)}), department_id: {department_id} ({type(department_id)})")
            print(f"AFTER CONVERSION - category_id: {category_id_str} ({type(category_id_str)}), department_id: {department_id_converted} ({type(department_id_converted)})")
            
            result = self.repository.associate_with_department(category_id_str, department_id_converted)
            if result:
                print(f"Associated children category {category_id} with department {department_id}")
            else:
                print(f"Failed to associate children category {category_id} with department {department_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in children category service associate_with_department at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise

    def remove_completion_type_association(self, category_id):
        """Remove the completion type association from a children category."""
        try:
            result = self.repository.remove_completion_type_association(category_id)
            if result:
                print(f"Removed completion type association from children category {category_id}")
            else:
                print(f"Failed to remove completion type association from children category {category_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in children category service remove_completion_type_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def remove_department_association(self, category_id):
        """Remove the department association from a children category."""
        try:
            result = self.repository.remove_department_association(category_id)
            if result:
                print(f"Removed department association from children category {category_id}")
            else:
                print(f"Failed to remove department association from children category {category_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in children category service remove_department_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def delete_category(self, category_id):
        """Delete a children category."""
        try:
            success = self.repository.delete(category_id)
            if success:
                print(f"Deleted children category with ID {category_id}")
            else:
                print(f"Children category with ID {category_id} not found for deletion")
            return success
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in children category service delete_category at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise