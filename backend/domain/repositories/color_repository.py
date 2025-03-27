from infrastructure.database.connection import get_db_connection
import traceback
import sys

class ColorRepository:
    """Repository for color operations."""
    
    def get_all(self):
        """Get all colors."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, name, hex_value, description, created_at FROM colors")
            
            colors = []
            rows = cursor.fetchall()
            
            # Debug: Print what we're getting from the database
            print(f"Color query returned {len(rows)} rows")
            if rows and len(rows) > 0:
                print(f"First row type: {type(rows[0])}")
                if hasattr(rows[0], 'keys'):
                    print(f"Row keys: {list(rows[0].keys())}")
            
            for row in rows:
                # If using RealDictCursor, row is dict-like
                if hasattr(row, 'keys'):
                    color = {
                        'id': row['id'],
                        'name': row['name'],
                        'hex_value': row['hex_value'],
                        'description': row['description'],
                        'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at']
                    }
                # Fallback to index-based access
                else:
                    color = {
                        'id': row[0],
                        'name': row[1],
                        'hex_value': row[2],
                        'description': row[3],
                        'created_at': row[4].isoformat() if hasattr(row[4], 'isoformat') else row[4]
                    }
                
                colors.append(color)
            
            return colors
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in color repository get_all at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            # Return empty list on error instead of crashing
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def create(self, color_data):
        """Create a new color."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Använd exakt de hex_value som kommer från frontend
            print(f"Creating color with hex_value: {color_data['hex_value']}")
            
            cursor.execute("""
                INSERT INTO colors (name, hex_value, description)
                VALUES (%s, %s, %s)
                RETURNING id, name, hex_value, description, created_at
            """, (color_data['name'], color_data['hex_value'], color_data.get('description')))
            
            row = cursor.fetchone()
            
            # Debug output för att verifiera att färgen sparades korrekt
            if hasattr(row, 'keys'):
                print(f"Color saved with hex_value: {row['hex_value']}")
            else:
                print(f"Color saved with hex_value: {row[2]}")
            
            # If using RealDictCursor, row is dict-like
            if hasattr(row, 'keys'):
                color = {
                    'id': row['id'],
                    'name': row['name'],
                    'hex_value': row['hex_value'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at']
                }
            # Fallback to index-based access
            else:
                color = {
                    'id': row[0],
                    'name': row[1],
                    'hex_value': row[2],
                    'description': row[3],
                    'created_at': row[4].isoformat() if hasattr(row[4], 'isoformat') else row[4]
                }
            
            conn.commit()
            return color
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in color repository create at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    def update(self, color_id, color_data):
        """Update an existing color."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Uppdatera en befintlig färg
            print(f"Updating color ID {color_id} with hex_value: {color_data['hex_value']}")
            
            cursor.execute("""
                UPDATE colors
                SET name = %s, hex_value = %s, description = %s
                WHERE id = %s
                RETURNING id, name, hex_value, description, created_at
            """, (color_data['name'], color_data['hex_value'], color_data.get('description'), color_id))
            
            row = cursor.fetchone()
            if not row:
                return None
                
            # Debug output för att verifiera att färgen uppdaterades korrekt
            if hasattr(row, 'keys'):
                print(f"Color updated with hex_value: {row['hex_value']}")
            else:
                print(f"Color updated with hex_value: {row[2]}")
            
            # If using RealDictCursor, row is dict-like
            if hasattr(row, 'keys'):
                color = {
                    'id': row['id'],
                    'name': row['name'],
                    'hex_value': row['hex_value'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at']
                }
            # Fallback to index-based access
            else:
                color = {
                    'id': row[0],
                    'name': row[1],
                    'hex_value': row[2],
                    'description': row[3],
                    'created_at': row[4].isoformat() if hasattr(row[4], 'isoformat') else row[4]
                }
            
            conn.commit()
            return color
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in color repository update at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    def delete(self, color_id):
        """Delete a color."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM colors WHERE id = %s RETURNING id", (color_id,))
            row = cursor.fetchone()
            success = row is not None
            
            conn.commit()
            return success
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in color repository delete at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()