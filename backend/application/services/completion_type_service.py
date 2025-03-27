from domain.repositories.completion_type_repository import CompletionTypeRepository
import traceback
import sys

class CompletionTypeService:
    """Service for completion type operations."""
    
    def __init__(self):
        self.repository = CompletionTypeRepository()
    
    def get_all_completion_types(self):
        """Get all completion types."""
        try:
            completion_types = self.repository.get_all()
            print(f"Completion type service retrieved {len(completion_types)} completion types")
            return completion_types
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in completion type service get_all_completion_types at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            # Return empty list instead of failing
            return []
    
    def get_completion_types_by_template(self, template_id):
        """Get completion types for a specific template."""
        try:
            completion_types = self.repository.get_by_template_id(template_id)
            print(f"Retrieved {len(completion_types)} completion types for template {template_id}")
            return completion_types
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in completion type service get_completion_types_by_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
    
    def create_completion_type(self, completion_type_data):
        """Create a new completion type."""
        try:
            # Validate input data
            if not completion_type_data or not isinstance(completion_type_data, dict):
                raise ValueError("Invalid completion type data format")
            
            if 'name' not in completion_type_data or not completion_type_data['name']:
                raise ValueError("Completion type name is required")
            
            # Handle empty template_id string
            if 'template_id' in completion_type_data and completion_type_data['template_id'] == '':
                completion_type_data['template_id'] = None
                
            # Ensure description exists even if it's None
            if 'description' not in completion_type_data:
                completion_type_data['description'] = None
                
            # Create the completion type
            completion_type = self.repository.create(completion_type_data)
            print(f"Created completion type: {completion_type['name']} with ID {completion_type['id']}")
            if completion_type.get('template_id'):
                print(f"  Associated with template ID: {completion_type['template_id']}")
                
            return completion_type
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in completion type service create_completion_type at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def update_completion_type(self, completion_type_id, completion_type_data):
        """Update a completion type."""
        try:
            # Validate input data
            if not completion_type_data or not isinstance(completion_type_data, dict):
                raise ValueError("Invalid completion type data format")
            
            if 'name' not in completion_type_data or not completion_type_data['name']:
                raise ValueError("Completion type name is required")
            
            # Handle empty template_id string
            if 'template_id' in completion_type_data and completion_type_data['template_id'] == '':
                completion_type_data['template_id'] = None
                
            # Ensure description exists even if it's None
            if 'description' not in completion_type_data:
                completion_type_data['description'] = None
                
            # Update the completion type
            completion_type = self.repository.update(completion_type_id, completion_type_data)
            
            if completion_type:
                print(f"Updated completion type: {completion_type['name']} with ID {completion_type['id']}")
                if completion_type.get('template_id'):
                    print(f"  Associated with template ID: {completion_type['template_id']}")
            else:
                print(f"Completion type with ID {completion_type_id} not found for update")
                
            return completion_type
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in completion type service update_completion_type at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def associate_with_template(self, completion_type_id, template_id):
        """Associate a completion type with a template."""
        try:
            result = self.repository.associate_with_template(completion_type_id, template_id)
            if result:
                print(f"Associated completion type {completion_type_id} with template {template_id}")
            else:
                print(f"Failed to associate completion type {completion_type_id} with template {template_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in completion type service associate_with_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def remove_template_association(self, completion_type_id):
        """Remove the template association from a completion type."""
        try:
            result = self.repository.remove_template_association(completion_type_id)
            if result:
                print(f"Removed template association from completion type {completion_type_id}")
            else:
                print(f"Failed to remove template association from completion type {completion_type_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in completion type service remove_template_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise