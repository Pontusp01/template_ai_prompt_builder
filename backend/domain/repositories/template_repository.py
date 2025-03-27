from infrastructure.database.connection import get_db_connection
import traceback
import sys

class TemplateRepository:
    """Repository for template operations."""
    
    def get_all(self):
        """Get all templates."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Uppdaterad query för att hämta templates med departments och colors
            cursor.execute("""
                SELECT t.id, t.title, t.content, t.created_at, t.updated_at, 
                       d.id as department_id, d.name as department_name,
                       c.id as color_id, c.name as color_name, c.hex_value, c.description as color_description
                FROM templates t
                LEFT JOIN departments d ON t.department_id = d.id
                LEFT JOIN colors c ON t.color_id = c.id
            """)
            
            templates = []
            rows = cursor.fetchall()
            
            # Debug: Print what we're getting from the database
            print(f"Template query returned {len(rows)} rows")
            
            # Skapa templates från resultatet
            for row in rows:
                # If using RealDictCursor, row is dict-like
                if hasattr(row, 'keys'):
                    template = {
                        'id': row['id'],
                        'title': row['title'],
                        'content': row['content'],
                        'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                        'updated_at': row['updated_at'].isoformat() if hasattr(row['updated_at'], 'isoformat') else row['updated_at'],
                        'department': {
                            'id': row['department_id'],
                            'name': row['department_name']
                        } if row['department_id'] else None,
                        'color': {
                            'id': row['color_id'],
                            'name': row['color_name'],
                            'hex_value': row['hex_value'],
                            'description': row['color_description']
                        } if row['color_id'] else None,
                        'completion_types': []
                    }
                # Fallback to index-based access for tuple-like rows
                else:
                    template = {
                        'id': row[0],
                        'title': row[1],
                        'content': row[2],
                        'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                        'updated_at': row[4].isoformat() if hasattr(row[4], 'isoformat') else row[4],
                        'department': {
                            'id': row[5],
                            'name': row[6]
                        } if row[5] else None,
                        'color': {
                            'id': row[7],
                            'name': row[8],
                            'hex_value': row[9],
                            'description': row[10]
                        } if row[7] else None,
                        'completion_types': []
                    }
                
                templates.append(template)
                
            # Se om completion_types har template_id kolumnen
            try:
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'completion_types' AND column_name = 'template_id'
                """)
                
                has_template_id = cursor.fetchone() is not None
                
                if has_template_id:
                    # Skapa en dictionary av templates för snabb lookup
                    templates_dict = {t['id']: t for t in templates}
                    
                    # Hämta alla completion types för alla templates på en gång
                    template_ids = list(templates_dict.keys())
                    if template_ids:
                        placeholders = ', '.join(['%s'] * len(template_ids))
                        
                        cursor.execute(f"""
                            SELECT id, name, description, template_id
                            FROM completion_types
                            WHERE template_id IN ({placeholders})
                        """, template_ids)
                        
                        completion_type_rows = cursor.fetchall()
                        
                        # Lägg till completion types till rätt template
                        for ct_row in completion_type_rows:
                            if hasattr(ct_row, 'keys'):
                                template_id = ct_row['template_id']
                                completion_type = {
                                    'id': ct_row['id'],
                                    'name': ct_row['name'],
                                    'description': ct_row['description']
                                }
                            else:
                                template_id = ct_row[3]
                                completion_type = {
                                    'id': ct_row[0],
                                    'name': ct_row[1],
                                    'description': ct_row[2]
                                }
                            
                            if template_id in templates_dict:
                                templates_dict[template_id]['completion_types'].append(completion_type)
            except Exception as e:
                print(f"Warning: Could not retrieve completion types for templates: {e}")
            
            return templates
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template repository get_all at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            # Return empty list on error instead of crashing
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_by_id(self, template_id):
        """Get template by ID."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Uppdaterad query för att hämta template med department och color
            cursor.execute("""
                SELECT t.id, t.title, t.content, t.created_at, t.updated_at, 
                       d.id as department_id, d.name as department_name,
                       c.id as color_id, c.name as color_name, c.hex_value, c.description as color_description
                FROM templates t
                LEFT JOIN departments d ON t.department_id = d.id
                LEFT JOIN colors c ON t.color_id = c.id
                WHERE t.id = %s
            """, (template_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # If using RealDictCursor, row is dict-like
            if hasattr(row, 'keys'):
                template = {
                    'id': row['id'],
                    'title': row['title'],
                    'content': row['content'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'updated_at': row['updated_at'].isoformat() if hasattr(row['updated_at'], 'isoformat') else row['updated_at'],
                    'department': {
                        'id': row['department_id'],
                        'name': row['department_name']
                    } if row['department_id'] else None,
                    'color': {
                        'id': row['color_id'],
                        'name': row['color_name'],
                        'hex_value': row['hex_value'],
                        'description': row['color_description']
                    } if row['color_id'] else None,
                    'completion_types': []
                }
            # Fallback to index-based access
            else:
                template = {
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                    'updated_at': row[4].isoformat() if hasattr(row[4], 'isoformat') else row[4],
                    'department': {
                        'id': row[5],
                        'name': row[6]
                    } if row[5] else None,
                    'color': {
                        'id': row[7],
                        'name': row[8],
                        'hex_value': row[9],
                        'description': row[10]
                    } if row[7] else None,
                    'completion_types': []
                }
            
            # Se om completion_types har template_id kolumnen
            try:
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'completion_types' AND column_name = 'template_id'
                """)
                
                has_template_id = cursor.fetchone() is not None
                
                if has_template_id:
                    # Hämta completion types för denna template
                    cursor.execute("""
                        SELECT id, name, description
                        FROM completion_types
                        WHERE template_id = %s
                    """, (template_id,))
                    
                    completion_type_rows = cursor.fetchall()
                    
                    # Lägg till completion types till template
                    for ct_row in completion_type_rows:
                        if hasattr(ct_row, 'keys'):
                            completion_type = {
                                'id': ct_row['id'],
                                'name': ct_row['name'],
                                'description': ct_row['description']
                            }
                        else:
                            completion_type = {
                                'id': ct_row[0],
                                'name': ct_row[1],
                                'description': ct_row[2]
                            }
                        
                        template['completion_types'].append(completion_type)
            except Exception as e:
                print(f"Warning: Could not retrieve completion types for template {template_id}: {e}")
            
            return template
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template repository get_by_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return None
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def create(self, template_data):
        """Create a new template."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Ta med både department_id och color_id om de finns
            query_parts = ["title", "content"]
            values = [template_data['title'], template_data['content']]
            placeholders = ["%s", "%s"]
            
            if template_data.get('department_id'):
                query_parts.append("department_id")
                values.append(template_data['department_id'])
                placeholders.append("%s")
                
            if template_data.get('color_id'):
                query_parts.append("color_id")
                values.append(template_data['color_id'])
                placeholders.append("%s")
            
            # Bygg query dynamiskt baserat på vilka fält som ska ingå
            query = f"""
                INSERT INTO templates ({', '.join(query_parts)})
                VALUES ({', '.join(placeholders)})
                RETURNING id, title, content, created_at, updated_at, department_id, color_id
            """
            
            cursor.execute(query, values)
            row = cursor.fetchone()
            
            # If using RealDictCursor, row is dict-like
            if hasattr(row, 'keys'):
                template = {
                    'id': row['id'],
                    'title': row['title'],
                    'content': row['content'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'updated_at': row['updated_at'].isoformat() if hasattr(row['updated_at'], 'isoformat') else row['updated_at'],
                    'department_id': row['department_id'],
                    'color_id': row['color_id'],
                    'completion_types': []
                }
            # Fallback to index-based access
            else:
                template = {
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                    'updated_at': row[4].isoformat() if hasattr(row[4], 'isoformat') else row[4],
                    'department_id': row[5],
                    'color_id': row[6],
                    'completion_types': []
                }
            
            # Se om completion_types har template_id kolumnen
            try:
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'completion_types' AND column_name = 'template_id'
                """)
                
                has_template_id = cursor.fetchone() is not None
                
                if has_template_id and 'completion_types' in template_data and template_data['completion_types']:
                    for ct_id in template_data['completion_types']:
                        cursor.execute("""
                            UPDATE completion_types
                            SET template_id = %s
                            WHERE id = %s
                        """, (template['id'], ct_id))
            except Exception as e:
                print(f"Warning: Could not associate completion types with template {template['id']}: {e}")
            
            conn.commit()
            return template
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template repository create at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def update(self, template_id, template_data):
        """Update a template."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Bygg uppdateringsfrågan dynamiskt baserat på vilka fält som ska uppdateras
            query_parts = ["title = %s", "content = %s", "updated_at = NOW()"]
            values = [template_data['title'], template_data['content']]
            
            if 'department_id' in template_data:
                query_parts.append("department_id = %s")
                values.append(template_data['department_id'])
                
            if 'color_id' in template_data:
                query_parts.append("color_id = %s")
                values.append(template_data['color_id'])
            
            # Lägg till template_id i values
            values.append(template_id)
            
            # Bygg query
            query = f"""
                UPDATE templates
                SET {', '.join(query_parts)}
                WHERE id = %s
                RETURNING id, title, content, created_at, updated_at, department_id, color_id
            """
            
            cursor.execute(query, values)
            row = cursor.fetchone()
            if not row:
                return None
            
            # If using RealDictCursor, row is dict-like
            if hasattr(row, 'keys'):
                template = {
                    'id': row['id'],
                    'title': row['title'],
                    'content': row['content'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'updated_at': row['updated_at'].isoformat() if hasattr(row['updated_at'], 'isoformat') else row['updated_at'],
                    'department_id': row['department_id'],
                    'color_id': row['color_id'],
                    'completion_types': []
                }
            # Fallback to index-based access
            else:
                template = {
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                    'updated_at': row[4].isoformat() if hasattr(row[4], 'isoformat') else row[4],
                    'department_id': row[5],
                    'color_id': row[6],
                    'completion_types': []
                }
            
            # Se om completion_types har template_id kolumnen
            try:
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'completion_types' AND column_name = 'template_id'
                """)
                
                has_template_id = cursor.fetchone() is not None
                
                if has_template_id and 'completion_types' in template_data:
                    # Rensa befintliga relationer
                    cursor.execute("""
                        UPDATE completion_types
                        SET template_id = NULL
                        WHERE template_id = %s
                    """, (template_id,))
                    
                    # Skapa nya relationer
                    if template_data['completion_types']:
                        for ct_id in template_data['completion_types']:
                            cursor.execute("""
                                UPDATE completion_types
                                SET template_id = %s
                                WHERE id = %s
                            """, (template_id, ct_id))
            except Exception as e:
                print(f"Warning: Could not update completion type associations for template {template_id}: {e}")
            
            conn.commit()
            return template
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in template repository update at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def delete(self, template_id):
        """Delete a template."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Rensa relationer i completion_types om template_id kolumnen finns
            try:
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'completion_types' AND column_name = 'template_id'
                """)
                
                has_template_id = cursor.fetchone() is not None
                
                if has_template_id:
                    cursor.execute("""
                        UPDATE completion_types
                        SET template_id = NULL
                        WHERE template_id = %s
                    """, (template_id,))
            except Exception as e:
                print(f"Warning: Could not clear completion type associations for template {template_id}: {e}")
            
            # Ta bort template
            cursor.execute("DELETE FROM templates WHERE id = %s RETURNING id", (template_id,))
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
            print(f"Error in template repository delete at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def update_color(self, template_id, color_id):
        """Update a template's color."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Uppdatera template med ny color_id
            if color_id:
                cursor.execute("""
                    UPDATE templates
                    SET color_id = %s
                    WHERE id = %s
                    RETURNING id
                """, (color_id, template_id))
            else:
                # Om color_id är None/null, ta bort färgassociationen
                cursor.execute("""
                    UPDATE templates
                    SET color_id = NULL
                    WHERE id = %s
                    RETURNING id
                """, (template_id,))
            
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
            print(f"Error in template repository update_color at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def remove_color(self, template_id):
        """Remove a template's color association."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Sätt color_id till NULL
            cursor.execute("""
                UPDATE templates
                SET color_id = NULL
                WHERE id = %s
                RETURNING id
            """, (template_id,))
            
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
            print(f"Error in template repository remove_color at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def associate_completion_type(self, template_id, completion_type_id):
        """Associate a completion type with a template."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Kontrollera om completion_types har template_id kolumnen
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'completion_types' AND column_name = 'template_id'
            """)
            
            has_template_id = cursor.fetchone() is not None
            
            if not has_template_id:
                print(f"Warning: completion_types table does not have template_id column")
                return False
            
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
            print(f"Error in template repository associate_completion_type at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def remove_completion_type_association(self, template_id, completion_type_id):
        """Remove the association between a template and a completion type."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Kontrollera om completion_types har template_id kolumnen
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'completion_types' AND column_name = 'template_id'
            """)
            
            has_template_id = cursor.fetchone() is not None
            
            if not has_template_id:
                print(f"Warning: completion_types table does not have template_id column")
                return False
            
            cursor.execute("""
                UPDATE completion_types
                SET template_id = NULL
                WHERE template_id = %s AND id = %s
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
            print(f"Error in template repository remove_completion_type_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()