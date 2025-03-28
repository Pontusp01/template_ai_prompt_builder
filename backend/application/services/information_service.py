from domain.repositories.information_repository import InformationRepository
import traceback
import sys

class InformationService:
    """Service for information operations."""
    
    def __init__(self):
        self.repository = InformationRepository()
    
    def get_all_information(self):
        """Get all information items."""
        try:
            information_items = self.repository.get_all()
            print(f"Information service retrieved {len(information_items)} items")
            return information_items
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information service get_all_information at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
    
    def get_information_by_template(self, template_id):
        """Get information items for a specific template."""
        try:
            information_items = self.repository.get_by_template_id(template_id)
            print(f"Retrieved {len(information_items)} information items for template {template_id}")
            return information_items
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information service get_information_by_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []

    def get_information_by_id(self, information_id):
        """Get an information item by ID."""
        try:
            information = self.repository.get_by_id(information_id)
            return information
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information service get_information_by_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return None
    
    def create_information(self, information_data):
        """Create a new information item."""
        try:
            if not information_data or not isinstance(information_data, dict):
                raise ValueError("Invalid information data format")
                
            if 'name' not in information_data or not information_data['name']:
                raise ValueError("Information name is required")
                
            if 'description' not in information_data:
                information_data['description'] = None
                
            if 'label' not in information_data:
                information_data['label'] = None
                  
            if 'template_id' in information_data and information_data['template_id'] == '':
                information_data['template_id'] = None
                
            if 'comments' not in information_data:
                information_data['comments'] = False
                
            information = self.repository.create(information_data)
            print(f"Created information item: {information['name']} with ID {information['id']}")
            if information.get('template_id'):
                print(f"  Associated with template ID: {information['template_id']}")
                
            return information
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information service create_information at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def update_information(self, information_id, information_data):
        """Update an information item."""
        try:
            if not information_data or not isinstance(information_data, dict):
                raise ValueError("Invalid information data format")
                
            if 'name' not in information_data or not information_data['name']:
                raise ValueError("Information name is required")
                
            if 'description' not in information_data:
                information_data['description'] = None
                
            if 'label' not in information_data:
                information_data['label'] = None
                
            if 'template_id' in information_data and information_data['template_id'] == '':
                information_data['template_id'] = None
                
            if 'comments' not in information_data:
                information_data['comments'] = False
                
            information = self.repository.update(information_id, information_data)
            
            if information:
                print(f"Updated information item with ID {information['id']}")
                if information.get('template_id'):
                    print(f"  Associated with template ID: {information['template_id']}")
            else:
                print(f"Information item with ID {information_id} not found for update")
                
            return information
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information service update_information at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise

    def associate_with_template(self, information_id, template_id):
        """Associate an information item with a template."""
        try:
            # Säkerställ att information_id är en sträng om det behövs
            information_id_str = str(information_id)
            
            # Om template_id inte är None, konvertera till integer
            # Detta är kritiskt för PostgreSQL som kräver rätt typ
            template_id_converted = int(template_id) if template_id is not None else None
            
            print(f"BEFORE CONVERSION - information_id: {information_id} ({type(information_id)}), template_id: {template_id} ({type(template_id)})")
            print(f"AFTER CONVERSION - information_id: {information_id_str} ({type(information_id_str)}), template_id: {template_id_converted} ({type(template_id_converted)})")
            
            result = self.repository.associate_with_template(information_id_str, template_id_converted)
            if result:
                print(f"Associated information item {information_id} with template {template_id}")
            else:
                print(f"Failed to associate information item {information_id} with template {template_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information service associate_with_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise

    def remove_template_association(self, information_id):
        """Remove the template association from an information item."""
        try:
            result = self.repository.remove_template_association(information_id)
            if result:
                print(f"Removed template association from information item {information_id}")
            else:
                print(f"Failed to remove template association from information item {information_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information service remove_template_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def delete_information(self, information_id):
        """Delete an information item."""
        try:
            success = self.repository.delete(information_id)
            if success:
                print(f"Deleted information item with ID {information_id}")
            else:
                print(f"Information item with ID {information_id} not found for deletion")
            return success
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information service delete_information at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise