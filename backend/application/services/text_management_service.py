from domain.repositories.text_management_repository import TextManagementRepository
import traceback
import sys

class TextManagementService:
    def __init__(self):
        self.repository = TextManagementRepository()
    
    def get_all_variables(self):
        """Get all text variables."""
        try:
            variables = self.repository.get_all_variables()
            print(f"Retrieved {len(variables)} variables")
            return variables
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in text management service get_all_variables at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
    
    def get_variable_by_id(self, variable_id):
        """Get a variable by ID."""
        try:
            variable = self.repository.get_variable_by_id(variable_id)
            return variable
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in text management service get_variable_by_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return None
    
    def create_variable(self, variable_data):
        """Create a new variable."""
        try:
            # Validera data
            if not variable_data or not isinstance(variable_data, dict):
                raise ValueError("Invalid variable data format")
            
            if 'namn' not in variable_data or not variable_data['namn']:
                raise ValueError("Variable name (namn) is required")
            
            # Säkerställ att alla nödvändiga fält finns
            if 'beskrivning' not in variable_data:
                variable_data['beskrivning'] = ''
                
            if 'variabel_namn' not in variable_data:
                variable_data['variabel_namn'] = f"${variable_data['namn']}$"
                
            if 'comments' not in variable_data:
                variable_data['comments'] = False
            
            variable = self.repository.create_variable(variable_data)
            print(f"Created variable: {variable['namn']} with ID {variable['id']}")
            return variable
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in text management service create_variable at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def update_variable(self, variable_id, variable_data):
        """Update a variable."""
        try:
            # Validera data
            if not variable_data or not isinstance(variable_data, dict):
                raise ValueError("Invalid variable data format")
            
            if 'namn' not in variable_data or not variable_data['namn']:
                raise ValueError("Variable name (namn) is required")
            
            # Säkerställ att alla nödvändiga fält finns
            if 'beskrivning' not in variable_data:
                variable_data['beskrivning'] = ''
                
            if 'variabel_namn' not in variable_data:
                variable_data['variabel_namn'] = f"${variable_data['namn']}$"
                
            if 'comments' not in variable_data:
                variable_data['comments'] = False
            
            variable = self.repository.update_variable(variable_id, variable_data)
            
            if variable:
                print(f"Updated variable with ID {variable['id']}")
            else:
                print(f"Variable with ID {variable_id} not found for update")
                
            return variable
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in text management service update_variable at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def delete_variable(self, variable_id):
        """Delete a variable."""
        try:
            success = self.repository.delete_variable(variable_id)
            if success:
                print(f"Deleted variable with ID {variable_id}")
            else:
                print(f"Variable with ID {variable_id} not found for deletion")
            return success
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in text management service delete_variable at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
    def update_variable_comments(self, variable_id, comments_status):
        """Update comments status for a variable."""
        try:
            # Hämta befintlig variabel
            existing_variable = self.repository.get_variable_by_id(variable_id)
            if not existing_variable:
                print(f"Variable with ID {variable_id} not found for comments update")
                return None
            
            # Uppdatera endast comments-fältet
            update_data = {
                'namn': existing_variable['namn'],
                'beskrivning': existing_variable.get('beskrivning', ''),
                'variabel_namn': existing_variable.get('variabel_namn', ''),
                'comments': comments_status
            }
            
            variable = self.repository.update_variable(variable_id, update_data)
            
            if variable:
                print(f"Updated comments status for variable with ID {variable['id']} to {comments_status}")
            
            return variable
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in text management service update_variable_comments at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise