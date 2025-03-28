from infrastructure.database.connection import get_db_connection
import traceback
import sys

class TextManagementRepository:
    def get_all_variables(self):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, namn, beskrivning, variabel_namn, comments FROM category_variabels")
            variables = cursor.fetchall()
            
            # Konvertera databasresultat till JSON-vänligt format
            result = []
            for var in variables:
                if hasattr(var, 'keys'):
                    # Om vi använder RealDictCursor
                    variable = {
                        'id': var['id'],
                        'namn': var['namn'],
                        'beskrivning': var['beskrivning'],
                        'variabel_namn': var['variabel_namn'],
                        'comments': var['comments']
                    }
                else:
                    # Använder reguljär cursor
                    variable = {
                        'id': var[0],
                        'namn': var[1],
                        'beskrivning': var[2],
                        'variabel_namn': var[3],
                        'comments': var[4]
                    }
                result.append(variable)
                
            return result
        except Exception as e:
            print(f"Error getting variables: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_variable_by_id(self, variable_id):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, namn, beskrivning, variabel_namn, comments FROM category_variabels WHERE id = %s", (variable_id,))
            var = cursor.fetchone()
            
            if not var:
                return None
                
            # Konvertera till JSON-vänligt format
            if hasattr(var, 'keys'):
                # Om vi använder RealDictCursor
                variable = {
                    'id': var['id'],
                    'namn': var['namn'],
                    'beskrivning': var['beskrivning'],
                    'variabel_namn': var['variabel_namn'],
                    'comments': var['comments']
                }
            else:
                # Använder reguljär cursor
                variable = {
                    'id': var[0],
                    'namn': var[1],
                    'beskrivning': var[2],
                    'variabel_namn': var[3],
                    'comments': var[4]
                }
                
            return variable
        except Exception as e:
            print(f"Error getting variable {variable_id}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def create_variable(self, variable_data):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO category_variabels (namn, beskrivning, variabel_namn, comments) VALUES (%s, %s, %s, %s) RETURNING id, namn, beskrivning, variabel_namn, comments",
                (
                    variable_data.get('namn', ''),
                    variable_data.get('beskrivning', ''),
                    variable_data.get('variabel_namn', ''),
                    variable_data.get('comments', False)
                )
            )
            
            var = cursor.fetchone()
            
            # Konvertera till JSON-vänligt format
            if hasattr(var, 'keys'):
                # Om vi använder RealDictCursor
                variable = {
                    'id': var['id'],
                    'namn': var['namn'],
                    'beskrivning': var['beskrivning'],
                    'variabel_namn': var['variabel_namn'],
                    'comments': var['comments']
                }
            else:
                # Använder reguljär cursor
                variable = {
                    'id': var[0],
                    'namn': var[1],
                    'beskrivning': var[2],
                    'variabel_namn': var[3],
                    'comments': var[4]
                }
            
            conn.commit()
            return variable
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error creating variable: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def update_variable(self, variable_id, variable_data):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE category_variabels SET namn = %s, beskrivning = %s, variabel_namn = %s, comments = %s WHERE id = %s RETURNING id, namn, beskrivning, variabel_namn, comments",
                (
                    variable_data.get('namn', ''),
                    variable_data.get('beskrivning', ''),
                    variable_data.get('variabel_namn', ''),
                    variable_data.get('comments', False),
                    variable_id
                )
            )
            
            var = cursor.fetchone()
            
            if not var:
                return None
                
            # Konvertera till JSON-vänligt format
            if hasattr(var, 'keys'):
                # Om vi använder RealDictCursor
                variable = {
                    'id': var['id'],
                    'namn': var['namn'],
                    'beskrivning': var['beskrivning'],
                    'variabel_namn': var['variabel_namn'],
                    'comments': var['comments']
                }
            else:
                # Använder reguljär cursor
                variable = {
                    'id': var[0],
                    'namn': var[1],
                    'beskrivning': var[2],
                    'variabel_namn': var[3],
                    'comments': var[4]
                }
            
            conn.commit()
            return variable
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error updating variable {variable_id}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def delete_variable(self, variable_id):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM category_variabels WHERE id = %s", (variable_id,))
            deleted = cursor.rowcount > 0
            
            conn.commit()
            return deleted
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error deleting variable {variable_id}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()