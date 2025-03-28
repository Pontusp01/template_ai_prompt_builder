from domain.repositories.category_repository import CategoryRepository
import traceback
import sys

class CategoryService:
    """Service for category operations."""
    
    def __init__(self):
        self.repository = CategoryRepository()
    
    def get_all_categories(self):
        """Get all categories."""
        try:
            categories = self.repository.get_all()
            print(f"Category service retrieved {len(categories)} categories")
            return categories
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in category service get_all_categories at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
    
    def get_categories_by_template(self, template_id):
        """Get categories for a specific template."""
        try:
            categories = self.repository.get_by_template_id(template_id)
            print(f"Retrieved {len(categories)} categories for template {template_id}")
            return categories
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in category service get_categories_by_template at {fname}:{line}: {e}")
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
            print(f"Error in category service get_category_by_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return None
    
    def create_category(self, category_data):
        """Create a new category."""
        try:
            if not category_data or not isinstance(category_data, dict):
                raise ValueError("Invalid category data format")
                
            if 'name' not in category_data or not category_data['name']:
                raise ValueError("Category name is required")
                
            if 'description' not in category_data:
                category_data['description'] = None
                  
            if 'template_id' in category_data and category_data['template_id'] == '':
                category_data['template_id'] = None
                
            category = self.repository.create(category_data)
            print(f"Created category: {category['name']} with ID {category['id']}")
            if category.get('template_id'):
                print(f"  Associated with template ID: {category['template_id']}")
                
            return category
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in category service create_category at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def update_category(self, category_id, category_data):
        """Update a category."""
        try:
            if not category_data or not isinstance(category_data, dict):
                raise ValueError("Invalid category data format")
                
            if 'name' not in category_data or not category_data['name']:
                raise ValueError("Category name is required")
                
            if 'description' not in category_data:
                category_data['description'] = None
                
            if 'template_id' in category_data and category_data['template_id'] == '':
                category_data['template_id'] = None
                
            category = self.repository.update(category_id, category_data)
            
            if category:
                print(f"Updated category with ID {category['id']}")
                if category.get('template_id'):
                    print(f"  Associated with template ID: {category['template_id']}")
            else:
                print(f"Category with ID {category_id} not found for update")
                
            return category
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in category service update_category at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise

    def associate_with_template(self, category_id, template_id):
        """Associate a category with a template."""
        try:
            # Säkerställ att category_id är en sträng om det behövs
            category_id_str = str(category_id)
            
            # Om template_id inte är None, konvertera till integer
            # Detta är kritiskt för PostgreSQL som kräver rätt typ
            template_id_converted = int(template_id) if template_id is not None else None
            
            print(f"BEFORE CONVERSION - category_id: {category_id} ({type(category_id)}), template_id: {template_id} ({type(template_id)})")
            print(f"AFTER CONVERSION - category_id: {category_id_str} ({type(category_id_str)}), template_id: {template_id_converted} ({type(template_id_converted)})")
            
            result = self.repository.associate_with_template(category_id_str, template_id_converted)
            if result:
                print(f"Associated category {category_id} with template {template_id}")
            else:
                print(f"Failed to associate category {category_id} with template {template_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in category service associate_with_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise

    def remove_template_association(self, category_id):
        """Remove the template association from a category."""
        try:
            result = self.repository.remove_template_association(category_id)
            if result:
                print(f"Removed template association from category {category_id}")
            else:
                print(f"Failed to remove template association from category {category_id}")
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in category service remove_template_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def delete_category(self, category_id):
        """Delete a category."""
        try:
            success = self.repository.delete(category_id)
            if success:
                print(f"Deleted category with ID {category_id}")
            else:
                print(f"Category with ID {category_id} not found for deletion")
            return success
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in category service delete_category at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise