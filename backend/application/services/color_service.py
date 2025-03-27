from domain.repositories.color_repository import ColorRepository
import traceback
import sys

class ColorService:
    """Service for color operations."""
    
    def __init__(self):
        self.repository = ColorRepository()
    
    def get_all_colors(self):
        """Get all colors."""
        try:
            colors = self.repository.get_all()
            print(f"Color service retrieved {len(colors)} colors")
            return colors
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in color service get_all_colors at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            # Return empty list instead of failing
            return []
    
    def create_color(self, color_data):
        """Create a new color."""
        try:
            # Validate input data
            if not color_data or not isinstance(color_data, dict):
                raise ValueError("Invalid color data format")
            
            if 'name' not in color_data or not color_data['name']:
                raise ValueError("Color name is required")
                
            if 'hex_value' not in color_data or not color_data['hex_value']:
                raise ValueError("Color hex value is required")
                
            # Skapa logposter för att felsöka
            print(f"Color data before save: {color_data}")
            
            # Se till att hexkoden är i rätt format (om det behövs)
            if color_data['hex_value'] and not color_data['hex_value'].startswith('#'):
                print(f"Adding # prefix to hex value: {color_data['hex_value']}")
                color_data['hex_value'] = f"#{color_data['hex_value']}"
                
            # Ensure description exists even if it's None
            if 'description' not in color_data:
                color_data['description'] = None
                
            # Create the color
            color = self.repository.create(color_data)
            print(f"Created color: {color['name']} with ID {color['id']} and hex_value {color['hex_value']}")
            return color
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in color service create_color at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
    def update_color(self, color_id, color_data):
        """Update a color."""
        try:
            # Validate input data
            if not color_data or not isinstance(color_data, dict):
                raise ValueError("Invalid color data format")
            
            if 'name' not in color_data or not color_data['name']:
                raise ValueError("Color name is required")
                
            if 'hex_value' not in color_data or not color_data['hex_value']:
                raise ValueError("Color hex value is required")
            
            # Se till att hexkoden är i rätt format (om det behövs)
            if color_data['hex_value'] and not color_data['hex_value'].startswith('#'):
                print(f"Adding # prefix to hex value: {color_data['hex_value']}")
                color_data['hex_value'] = f"#{color_data['hex_value']}"
                
            # Ensure description exists even if it's None
            if 'description' not in color_data:
                color_data['description'] = None
                
            # Update the color
            color = self.repository.update(color_id, color_data)
            
            if color:
                print(f"Updated color: {color['name']} with ID {color['id']} and hex_value {color['hex_value']}")
            else:
                print(f"Color with ID {color_id} not found for update")
                
            return color
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in color service update_color at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
    def delete_color(self, color_id):
        """Delete a color."""
        try:
            success = self.repository.delete(color_id)
            
            if success:
                print(f"Deleted color with ID {color_id}")
            else:
                print(f"Color with ID {color_id} not found for deletion")
                
            return success
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in color service delete_color at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise