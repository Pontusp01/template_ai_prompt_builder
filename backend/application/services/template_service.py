from domain.repositories.template_repository import TemplateRepository
import traceback
import sys

class TemplateService:
    """Service for template operations."""
    
    def __init__(self):
        self.repository = TemplateRepository()
    
    def get_all_templates(self):
        """Get all templates."""
        try:
            templates = self.repository.get_all()
            print(f"Template service retrieved {len(templates)} templates")
            return templates
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template service get_all_templates at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            # Return empty list instead of failing
            return []
    
    def get_template_by_id(self, template_id):
        """Get template by ID."""
        try:
            template = self.repository.get_by_id(template_id)
            return template
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template service get_template_by_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return None
    
    def create_template(self, template_data):
        """Create a new template."""
        try:
            # Validate input data
            if not template_data or not isinstance(template_data, dict):
                raise ValueError("Invalid template data format")
            
            if 'title' not in template_data or not template_data['title']:
                raise ValueError("Template title is required")
                
            if 'content' not in template_data or not template_data['content']:
                raise ValueError("Template content is required")
            
            # Handle empty values for department_id and color_id
            if 'department_id' in template_data and (template_data['department_id'] == '' or template_data['department_id'] == 'null'):
                template_data['department_id'] = None
                
            if 'color_id' in template_data and (template_data['color_id'] == '' or template_data['color_id'] == 'null'):
                template_data['color_id'] = None
                
            # Create the template
            template = self.repository.create(template_data)
            print(f"Created template: {template['title']} with ID {template['id']}")
            
            # Log color_id if it was set
            if template.get('color_id'):
                print(f"  Template has color_id: {template['color_id']}")
                
            return template
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template service create_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def update_template(self, template_id, template_data):
        """Update a template."""
        try:
            # Validate input data
            if not template_data or not isinstance(template_data, dict):
                raise ValueError("Invalid template data format")
            
            if 'title' not in template_data or not template_data['title']:
                raise ValueError("Template title is required")
                
            if 'content' not in template_data or not template_data['content']:
                raise ValueError("Template content is required")
            
            # Handle empty values for department_id and color_id
            if 'department_id' in template_data and (template_data['department_id'] == '' or template_data['department_id'] == 'null'):
                template_data['department_id'] = None
                
            if 'color_id' in template_data and (template_data['color_id'] == '' or template_data['color_id'] == 'null'):
                template_data['color_id'] = None
                
            # Update the template
            template = self.repository.update(template_id, template_data)
            if template:
                print(f"Updated template with ID {template['id']}")
                if 'color_id' in template_data:
                    print(f"  Updated color_id to: {template_data['color_id']}")
            else:
                print(f"Template with ID {template_id} not found for update")
                
            return template
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template service update_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def delete_template(self, template_id):
        """Delete a template."""
        try:
            success = self.repository.delete(template_id)
            if success:
                print(f"Deleted template with ID {template_id}")
            else:
                print(f"Template with ID {template_id} not found for deletion")
            return success
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template service delete_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def update_template_color(self, template_id, color_id):
        """Update a template's color."""
        try:
            # Handle empty color_id
            if color_id == '' or color_id == 'null':
                color_id = None
                
            success = self.repository.update_color(template_id, color_id)
            if success:
                print(f"Updated template {template_id} color to {color_id if color_id else 'None'}")
            else:
                print(f"Failed to update template {template_id} color")
                
            return success
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template service update_template_color at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def remove_template_color(self, template_id):
        """Remove a template's color association."""
        try:
            success = self.repository.remove_color(template_id)
            if success:
                print(f"Removed color from template {template_id}")
            else:
                print(f"Failed to remove color from template {template_id}")
                
            return success
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template service remove_template_color at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def associate_completion_type(self, template_id, completion_type_id):
        """Associate a completion type with a template."""
        try:
            result = self.repository.associate_completion_type(template_id, completion_type_id)
            if result:
                print(f"Associated completion type {completion_type_id} with template {template_id}")
            else:
                print(f"Failed to associate completion type {completion_type_id} with template {template_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template service associate_completion_type at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def remove_completion_type_association(self, template_id, completion_type_id):
        """Remove the association between a template and a completion type."""
        try:
            result = self.repository.remove_completion_type_association(template_id, completion_type_id)
            if result:
                print(f"Removed association between completion type {completion_type_id} and template {template_id}")
            else:
                print(f"Failed to remove association between completion type {completion_type_id} and template {template_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template service remove_completion_type_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def update_template_completion_types(self, template_id, completion_type_ids):
        """Update all completion type associations for a template."""
        try:
            # First, check if the template exists
            template = self.repository.get_by_id(template_id)
            if not template:
                print(f"Template with ID {template_id} not found")
                return False
            
            # Create update data with bare minimum fields
            update_data = {
                'title': template['title'],
                'content': template['content'],
                'completion_types': completion_type_ids
            }
            
            # Add department_id if it exists in template
            if template.get('department') and template['department'].get('id'):
                update_data['department_id'] = template['department']['id']
            
            # Add color_id if it exists in template
            if template.get('color') and template['color'].get('id'):
                update_data['color_id'] = template['color']['id']
            
            # Update the template
            updated_template = self.repository.update(template_id, update_data)
            return updated_template is not None
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template service update_template_completion_types at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise