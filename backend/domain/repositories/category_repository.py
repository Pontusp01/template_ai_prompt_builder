from infrastructure.database.connection import get_db_connection
import traceback
import sys

class CategoryRepository:
    """Repository for category operations."""
    
    def get_all(self):
        """Get all categories."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, c.name, c.description, c.created_at, c.template_id,
                    t.title as template_title  
                FROM categories c
                LEFT JOIN templates t ON c.template_id = t.id
            """)
            
            categories = []
            rows = cursor.fetchall()
            
            print(f"Query returned {len(rows)} rows")
            if rows and len(rows) > 0:
                print(f"First row type: {type(rows[0])}")
                if hasattr(rows[0], 'keys'):
                    print(f"Row keys: {list(rows[0].keys())}")
            
            for row in rows:
                if hasattr(row, 'keys'):
                    category = {
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                        'template_id': row['template_id'],
                        'template': None
                    }
                    
                    if row['template_id'] is not None:
                        category['template'] = {
                            'id': row['template_id'],
                            'title': row['template_title']
                        }
                else:
                    category = {
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                        'template_id': row[4],
                        'template': None
                    }
                    
                    if row[4] is not None:
                        category['template'] = {
                            'id': row[4],
                            'title': row[5]
                        }
                
                categories.append(category)
            
            return categories
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in category repository get_all at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def create(self, category_data):
        """Create a new category."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if 'template_id' in category_data and category_data['template_id']:
                cursor.execute("""
                    INSERT INTO categories (name, description, template_id)
                    VALUES (%s, %s, %s)
                    RETURNING id, name, description, created_at, template_id
                """, (
                    category_data['name'],
                    category_data.get('description'),
                    category_data['template_id']
                ))
            else:
                cursor.execute("""
                    INSERT INTO categories (name, description)
                    VALUES (%s, %s)
                    RETURNING id, name, description, created_at, template_id
                """, (
                    category_data['name'],
                    category_data.get('description')
                ))
            
            row = cursor.fetchone()
            
            if hasattr(row, 'keys'):
                category = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'template_id': row['template_id']
                }
            else:
                category = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                    'template_id': row[4]
                }
            
            conn.commit()
            return category
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in category repository create at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update(self, category_id, category_data):
        """Update a category."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if 'template_id' in category_data:
                cursor.execute("""
                    UPDATE categories
                    SET name = %s, description = %s, template_id = %s
                    WHERE id = %s
                    RETURNING id, name, description, created_at, template_id
                """, (
                    category_data['name'],
                    category_data.get('description'),
                    category_data['template_id'],
                    category_id
                ))
            else:
                cursor.execute("""
                    UPDATE categories
                    SET name = %s, description = %s
                    WHERE id = %s
                    RETURNING id, name, description, created_at, template_id
                """, (
                    category_data['name'],
                    category_data.get('description'),
                    category_id
                ))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            if hasattr(row, 'keys'):
                category = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'template_id': row['template_id']
                }
            else:
                category = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                    'template_id': row[4]
                }
            
            conn.commit()
            return category
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in category repository update at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def associate_with_template(self, category_id, template_id):
        """Associate a category with a template."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Skriv ut detaljer för felsökning
            print(f"[REPO] Associating category {category_id} with template {template_id}")
            print(f"[REPO] Category ID type: {type(category_id)}, Template ID type: {type(template_id)}")
            
            # Testa att först hämta kategorin för att säkerställa att det existerar
            cursor.execute("SELECT id FROM categories WHERE id = %s", (category_id,))
            cat_exists = cursor.fetchone()
            print(f"[REPO] Category exists check: {cat_exists}")
            
            # Om template_id inte är None, verifiera att mallen existerar
            if template_id is not None:
                cursor.execute("SELECT id FROM templates WHERE id = %s", (template_id,))
                template_exists = cursor.fetchone()
                print(f"[REPO] Template exists check: {template_exists}")
                if not template_exists:
                    print(f"[REPO] WARNING: Template with ID {template_id} does not exist!")
            
            # Kör uppdateringen
            cursor.execute("""
                UPDATE categories
                SET template_id = %s
                WHERE id = %s
                RETURNING id
            """, (template_id, category_id))
            
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
            print(f"Error in category repository associate_with_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def remove_template_association(self, category_id):
        """Remove the template association from a category."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE categories
                SET template_id = NULL
                WHERE id = %s
                RETURNING id
            """, (category_id,))
            
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
            print(f"Error in category repository remove_template_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete(self, category_id):
        """Delete a category."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM categories
                WHERE id = %s
                RETURNING id
            """, (category_id,))
            
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
            print(f"Error in category repository delete at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_by_template_id(self, template_id):
        """Get categories by template ID."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, description, created_at, template_id 
                FROM categories
                WHERE template_id = %s
            """, (template_id,))
            
            categories = []
            rows = cursor.fetchall()
            
            for row in rows:
                if hasattr(row, 'keys'):
                    category = {
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                        'template_id': row['template_id']
                    }
                else:
                    category = {
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                        'template_id': row[4]
                    }
                
                categories.append(category)
            
            return categories
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in category repository get_by_template_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_by_id(self, category_id):
        """Get a category by ID."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.id, c.name, c.description, c.created_at, c.template_id,
                    t.title as template_title
                FROM categories c
                LEFT JOIN templates t ON c.template_id = t.id
                WHERE c.id = %s
            """, (category_id,))
            
            row = cursor.fetchone()
            
            if not row:
                return None
                
            if hasattr(row, 'keys'):
                category = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'template_id': row['template_id'],
                    'template': None
                }
                
                if row['template_id'] is not None:
                    category['template'] = {
                        'id': row['template_id'],
                        'title': row['template_title']
                    }
            else:
                category = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                    'template_id': row[4],
                    'template': None
                }
                
                if row[4] is not None:
                    category['template'] = {
                        'id': row[4],
                        'title': row[5]
                    }
            
            return category
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in category repository get_by_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return None
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()