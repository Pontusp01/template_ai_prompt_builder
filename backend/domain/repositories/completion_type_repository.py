from infrastructure.database.connection import get_db_connection
import traceback
import sys

class CompletionTypeRepository:
    """Repository for completion type operations."""
    
    def get_all(self):
        """Get all completion types."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Ändrad query för att hämta template-information
            cursor.execute("""
                SELECT ct.id, ct.name, ct.description, ct.created_at, ct.template_id, 
                    t.title as template_title
                FROM completion_types ct
                LEFT JOIN templates t ON ct.template_id = t.id
            """)
            
            completion_types = []
            rows = cursor.fetchall()
            
            # Debug: Print what we're getting from the database
            print(f"Completion type query returned {len(rows)} rows")
            if rows and len(rows) > 0:
                print(f"First row type: {type(rows[0])}")
                if hasattr(rows[0], 'keys'):
                    print(f"Row keys: {list(rows[0].keys())}")
            
            for row in rows:
                # If using RealDictCursor, row is dict-like
                if hasattr(row, 'keys'):
                    completion_type = {
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                        'template_id': row['template_id'],
                        'template': None
                    }
                    
                    # Lägg till template-information om det finns
                    if row['template_id'] is not None:
                        completion_type['template'] = {
                            'id': row['template_id'],
                            'title': row['template_title']
                        }
                # Fallback to index-based access
                else:
                    completion_type = {
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                        'template_id': row[4],
                        'template': None
                    }
                    
                    # Lägg till template-information om det finns
                    if row[4] is not None:
                        completion_type['template'] = {
                            'id': row[4],
                            'title': row[5]
                        }
                
                completion_types.append(completion_type)
            
            return completion_types
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in completion type repository get_all at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            # Return empty list on error instead of crashing
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_by_template_id(self, template_id):
        """Get completion types by template ID."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, description, created_at, template_id 
                FROM completion_types 
                WHERE template_id = %s
            """, (template_id,))
            
            completion_types = []
            rows = cursor.fetchall()
            
            for row in rows:
                # If using RealDictCursor, row is dict-like
                if hasattr(row, 'keys'):
                    completion_type = {
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                        'template_id': row['template_id']
                    }
                # Fallback to index-based access
                else:
                    completion_type = {
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                        'template_id': row[4]
                    }
                
                completion_types.append(completion_type)
            
            return completion_types
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in completion type repository get_by_template_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            # Return empty list on error instead of crashing
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def create(self, completion_type_data):
        """Create a new completion type."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if template_id exists in the data
            if 'template_id' in completion_type_data and completion_type_data['template_id']:
                cursor.execute("""
                    INSERT INTO completion_types (name, description, template_id)
                    VALUES (%s, %s, %s)
                    RETURNING id, name, description, created_at, template_id
                """, (
                    completion_type_data['name'],
                    completion_type_data.get('description'),
                    completion_type_data['template_id']
                ))
            else:
                cursor.execute("""
                    INSERT INTO completion_types (name, description)
                    VALUES (%s, %s)
                    RETURNING id, name, description, created_at, template_id
                """, (
                    completion_type_data['name'],
                    completion_type_data.get('description')
                ))
            
            row = cursor.fetchone()
            
            # If using RealDictCursor, row is dict-like
            if hasattr(row, 'keys'):
                completion_type = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'template_id': row['template_id']
                }
            # Fallback to index-based access
            else:
                completion_type = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                    'template_id': row[4]
                }
            
            conn.commit()
            return completion_type
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in completion type repository create at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def update(self, completion_type_id, completion_type_data):
        """Update a completion type."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if template_id should be updated
            if 'template_id' in completion_type_data:
                cursor.execute("""
                    UPDATE completion_types
                    SET name = %s, description = %s, template_id = %s
                    WHERE id = %s
                    RETURNING id, name, description, created_at, template_id
                """, (
                    completion_type_data['name'],
                    completion_type_data.get('description'),
                    completion_type_data['template_id'],
                    completion_type_id
                ))
            else:
                cursor.execute("""
                    UPDATE completion_types
                    SET name = %s, description = %s
                    WHERE id = %s
                    RETURNING id, name, description, created_at, template_id
                """, (
                    completion_type_data['name'],
                    completion_type_data.get('description'),
                    completion_type_id
                ))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # If using RealDictCursor, row is dict-like
            if hasattr(row, 'keys'):
                completion_type = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'template_id': row['template_id']
                }
            # Fallback to index-based access
            else:
                completion_type = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                    'template_id': row[4]
                }
            
            conn.commit()
            return completion_type
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in completion type repository update at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def associate_with_template(self, completion_type_id, template_id):
        """Associate a completion type with a template."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE completion_types
                SET template_id = %s
                WHERE id = %s
                RETURNING id
            """, (template_id, completion_type_id))
            
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
            print(f"Error in completion type repository associate_with_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_by_id(self, completion_type_id):
        """Get a completion type by ID."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT ct.id, ct.name, ct.description, ct.created_at, ct.template_id,
                    t.title as template_title
                FROM completion_types ct
                LEFT JOIN templates t ON ct.template_id = t.id
                WHERE ct.id = %s
            """, (completion_type_id,))
            
            row = cursor.fetchone()
            
            if not row:
                return None
                
            # If using RealDictCursor, row is dict-like
            if hasattr(row, 'keys'):
                completion_type = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'template_id': row['template_id'],
                    'template': None
                }
                
                # Lägg till template-information om det finns
                if row['template_id'] is not None:
                    completion_type['template'] = {
                        'id': row['template_id'],
                        'title': row['template_title']
                    }
            # Fallback to index-based access
            else:
                completion_type = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                    'template_id': row[4],
                    'template': None
                }
                
                # Lägg till template-information om det finns
                if row[4] is not None:
                    completion_type['template'] = {
                        'id': row[4],
                        'title': row[5]
                    }
            
            return completion_type
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in completion type repository get_by_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return None
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def remove_template_association(self, completion_type_id):
        """Remove the template association from a completion type."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE completion_types
                SET template_id = NULL
                WHERE id = %s
                RETURNING id
            """, (completion_type_id,))
            
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
            print(f"Error in completion type repository remove_template_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def delete(self, completion_type_id):
        """Delete a completion type."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Först kontrollera om denna completion type används av några templates
            cursor.execute("""
                SELECT id, title FROM templates 
                WHERE completion_type_id = %s
            """, (completion_type_id,))
            
            templates = cursor.fetchall()
            if templates:
                template_ids = []
                if hasattr(templates[0], 'keys'):
                    template_ids = [row['id'] for row in templates]
                    template_titles = [row['title'] for row in templates]
                else:
                    template_ids = [row[0] for row in templates]
                    template_titles = [row[1] for row in templates]
                    
                print(f"Warning: Cannot delete completion type {completion_type_id} because it is used by templates: {template_titles}")
                return False
            
            # Om det inte finns några referenser, fortsätt med borttagningen
            cursor.execute("""
                DELETE FROM completion_types
                WHERE id = %s
                RETURNING id
            """, (completion_type_id,))
            
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
            print(f"Error in completion type repository delete at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()