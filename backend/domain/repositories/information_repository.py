from infrastructure.database.connection import get_db_connection
import traceback
import sys

class InformationRepository:
    """Repository for information operations."""
    
    def get_all(self):
        """Get all information items."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id, i.name, i.label, i.description, i.created_at, i.template_id, i.comments,
                    t.title as template_title  
                FROM information i
                LEFT JOIN templates t ON i.template_id = t.id
            """)
            
            information_items = []
            rows = cursor.fetchall()
            
            print(f"Query returned {len(rows)} rows")
            if rows and len(rows) > 0:
                print(f"First row type: {type(rows[0])}")
                if hasattr(rows[0], 'keys'):
                    print(f"Row keys: {list(rows[0].keys())}")
            
            for row in rows:
                if hasattr(row, 'keys'):
                    item = {
                        'id': row['id'],
                        'name': row['name'],
                        'label': row['label'],
                        'description': row['description'],
                        'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                        'template_id': row['template_id'],
                        'comments': row['comments'],
                        'template': None
                    }
                    
                    if row['template_id'] is not None:
                        item['template'] = {
                            'id': row['template_id'],
                            'title': row['template_title']
                        }
                else:
                    item = {
                        'id': row[0],
                        'name': row[1],
                        'label': row[2],
                        'description': row[3],
                        'created_at': row[4].isoformat() if hasattr(row[4], 'isoformat') else row[4],
                        'template_id': row[5],
                        'comments': row[6],
                        'template': None
                    }
                    
                    if row[5] is not None:
                        item['template'] = {
                            'id': row[5],
                            'title': row[7]
                        }
                
                information_items.append(item)
            
            return information_items
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information repository get_all at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def create(self, information_data):
        """Create a new information item."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if 'template_id' in information_data and information_data['template_id']:
                cursor.execute("""
                    INSERT INTO information (name, label, description, template_id, comments)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, name, label, description, created_at, template_id, comments
                """, (
                    information_data['name'],
                    information_data.get('label'),
                    information_data.get('description'),
                    information_data['template_id'],
                    information_data.get('comments', False)
                ))
            else:
                cursor.execute("""
                    INSERT INTO information (name, label, description, comments)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, name, label, description, created_at, template_id, comments
                """, (
                    information_data['name'],
                    information_data.get('label'),
                    information_data.get('description'),
                    information_data.get('comments', False)
                ))
            
            row = cursor.fetchone()
            
            if hasattr(row, 'keys'):
                item = {
                    'id': row['id'],
                    'name': row['name'],
                    'label': row['label'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'template_id': row['template_id'],
                    'comments': row['comments']
                }
            else:
                item = {
                    'id': row[0],
                    'name': row[1],
                    'label': row[2],
                    'description': row[3],
                    'created_at': row[4].isoformat() if hasattr(row[4], 'isoformat') else row[4],
                    'template_id': row[5],
                    'comments': row[6]
                }
            
            conn.commit()
            return item
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information repository create at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update(self, information_id, information_data):
        """Update an information item."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if 'template_id' in information_data:
                cursor.execute("""
                    UPDATE information
                    SET name = %s, label = %s, description = %s, template_id = %s, comments = %s
                    WHERE id = %s
                    RETURNING id, name, label, description, created_at, template_id, comments
                """, (
                    information_data['name'],
                    information_data.get('label'),
                    information_data.get('description'),
                    information_data['template_id'],
                    information_data.get('comments', False),
                    information_id
                ))
            else:
                cursor.execute("""
                    UPDATE information
                    SET name = %s, label = %s, description = %s, comments = %s
                    WHERE id = %s
                    RETURNING id, name, label, description, created_at, template_id, comments
                """, (
                    information_data['name'],
                    information_data.get('label'),
                    information_data.get('description'),
                    information_data.get('comments', False),
                    information_id
                ))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            if hasattr(row, 'keys'):
                item = {
                    'id': row['id'],
                    'name': row['name'],
                    'label': row['label'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'template_id': row['template_id'],
                    'comments': row['comments']
                }
            else:
                item = {
                    'id': row[0],
                    'name': row[1],
                    'label': row[2],
                    'description': row[3],
                    'created_at': row[4].isoformat() if hasattr(row[4], 'isoformat') else row[4],
                    'template_id': row[5],
                    'comments': row[6]
                }
            
            conn.commit()
            return item
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information repository update at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def associate_with_template(self, information_id, template_id):
        """Associate an information item with a template."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Skriv ut detaljer för felsökning
            print(f"[REPO] Associating information {information_id} with template {template_id}")
            print(f"[REPO] Information ID type: {type(information_id)}, Template ID type: {type(template_id)}")
            
            # Testa att först hämta informationen för att säkerställa att det existerar
            cursor.execute("SELECT id FROM information WHERE id = %s", (information_id,))
            info_exists = cursor.fetchone()
            print(f"[REPO] Information exists check: {info_exists}")
            
            # Om template_id inte är None, verifiera att mallen existerar
            if template_id is not None:
                cursor.execute("SELECT id FROM templates WHERE id = %s", (template_id,))
                template_exists = cursor.fetchone()
                print(f"[REPO] Template exists check: {template_exists}")
                if not template_exists:
                    print(f"[REPO] WARNING: Template with ID {template_id} does not exist!")
            
            # Kör uppdateringen
            cursor.execute("""
                UPDATE information
                SET template_id = %s
                WHERE id = %s
                RETURNING id
            """, (template_id, information_id))
            
            row = cursor.fetchone()
            success = row is not None
            
            # Skriv ut resultat för felsökning
            print(f"[REPO] Association query result: {row}")
            if not success:
                print(f"[REPO] WARNING: Update succeeded but no rows were returned!")
                # Kontrollera om någon rad uppdaterades, även om RETURNING inte gav resultat
                affected_rows = cursor.rowcount
                print(f"[REPO] Affected rows: {affected_rows}")
                success = affected_rows > 0
            
            conn.commit()
            return success
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information repository associate_with_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def remove_template_association(self, information_id):
        """Remove the template association from an information item."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE information
                SET template_id = NULL
                WHERE id = %s
                RETURNING id
            """, (information_id,))
            
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
            print(f"Error in information repository remove_template_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete(self, information_id):
        """Delete an information item."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM information
                WHERE id = %s
                RETURNING id
            """, (information_id,))
            
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
            print(f"Error in information repository delete at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_by_template_id(self, template_id):
        """Get information items by template ID."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, label, description, created_at, template_id, comments
                FROM information
                WHERE template_id = %s
            """, (template_id,))
            
            information_items = []
            rows = cursor.fetchall()
            
            for row in rows:
                if hasattr(row, 'keys'):
                    item = {
                        'id': row['id'],
                        'name': row['name'],
                        'label': row['label'],
                        'description': row['description'],
                        'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                        'template_id': row['template_id'],
                        'comments': row['comments']
                    }
                else:
                    item = {
                        'id': row[0],
                        'name': row[1],
                        'label': row[2],
                        'description': row[3],
                        'created_at': row[4].isoformat() if hasattr(row[4], 'isoformat') else row[4],
                        'template_id': row[5],
                        'comments': row[6]
                    }
                
                information_items.append(item)
            
            return information_items
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information repository get_by_template_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_by_id(self, information_id):
        """Get an information item by ID."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT i.id, i.name, i.label, i.description, i.created_at, i.template_id, i.comments,
                    t.title as template_title
                FROM information i
                LEFT JOIN templates t ON i.template_id = t.id
                WHERE i.id = %s
            """, (information_id,))
            
            row = cursor.fetchone()
            
            if not row:
                return None
                
            if hasattr(row, 'keys'):
                item = {
                    'id': row['id'],
                    'name': row['name'],
                    'label': row['label'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'template_id': row['template_id'],
                    'comments': row['comments'],
                    'template': None
                }
                
                if row['template_id'] is not None:
                    item['template'] = {
                        'id': row['template_id'],
                        'title': row['template_title']
                    }
            else:
                item = {
                    'id': row[0],
                    'name': row[1],
                    'label': row[2],
                    'description': row[3],
                    'created_at': row[4].isoformat() if hasattr(row[4], 'isoformat') else row[4],
                    'template_id': row[5],
                    'comments': row[6],
                    'template': None
                }
                
                if row[5] is not None:
                    item['template'] = {
                        'id': row[5],
                        'title': row[7]
                    }
            
            return item
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in information repository get_by_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return None
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()