from infrastructure.database.connection import get_db_connection
import traceback
import sys

class DepartmentRepository:
    """Repository for department operations."""
    
    def get_all(self):
        """Get all departments."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.id, d.name, d.description, d.created_at, d.template_id,
                    t.title as template_title  
                FROM departments d
                LEFT JOIN templates t ON d.template_id = t.id
            """)
            
            departments = []
            rows = cursor.fetchall()
            
            print(f"Query returned {len(rows)} rows")
            if rows and len(rows) > 0:
                print(f"First row type: {type(rows[0])}")
                if hasattr(rows[0], 'keys'):
                    print(f"Row keys: {list(rows[0].keys())}")
            
            for row in rows:
                if hasattr(row, 'keys'):
                    department = {
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                        'template_id': row['template_id'],
                        'template': None
                    }
                    
                    if row['template_id'] is not None:
                        department['template'] = {
                            'id': row['template_id'],
                            'title': row['template_title']
                        }
                else:
                    department = {
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                        'template_id': row[4],
                        'template': None
                    }
                    
                    if row[4] is not None:
                        department['template'] = {
                            'id': row[4],
                            'title': row[5]
                        }
                
                departments.append(department)
            
            return departments
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department repository get_all at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def create(self, department_data):
        """Create a new department."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if 'template_id' in department_data and department_data['template_id']:
                cursor.execute("""
                    INSERT INTO departments (name, description, template_id)
                    VALUES (%s, %s, %s)
                    RETURNING id, name, description, created_at, template_id
                """, (
                    department_data['name'],
                    department_data.get('description'),
                    department_data['template_id']
                ))
            else:
                cursor.execute("""
                    INSERT INTO departments (name, description)
                    VALUES (%s, %s)
                    RETURNING id, name, description, created_at, template_id
                """, (
                    department_data['name'],
                    department_data.get('description')
                ))
            
            row = cursor.fetchone()
            
            if hasattr(row, 'keys'):
                department = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'template_id': row['template_id']
                }
            else:
                department = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                    'template_id': row[4]
                }
            
            conn.commit()
            return department
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department repository create at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update(self, department_id, department_data):
        """Update a department."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if 'template_id' in department_data:
                cursor.execute("""
                    UPDATE departments
                    SET name = %s, description = %s, template_id = %s
                    WHERE id = %s
                    RETURNING id, name, description, created_at, template_id
                """, (
                    department_data['name'],
                    department_data.get('description'),
                    department_data['template_id'],
                    department_id
                ))
            else:
                cursor.execute("""
                    UPDATE departments
                    SET name = %s, description = %s
                    WHERE id = %s
                    RETURNING id, name, description, created_at, template_id
                """, (
                    department_data['name'],
                    department_data.get('description'),
                    department_id
                ))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            if hasattr(row, 'keys'):
                department = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'template_id': row['template_id']
                }
            else:
                department = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                    'template_id': row[4]
                }
            
            conn.commit()
            return department
            
        except Exception as e:
            if conn:
                conn.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department repository update at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def associate_with_template(self, department_id, template_id):
        """Associate a department with a template."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Skriv ut detaljer för felsökning
            print(f"[REPO] Associating department {department_id} with template {template_id}")
            print(f"[REPO] Department ID type: {type(department_id)}, Template ID type: {type(template_id)}")
            
            # Testa att först hämta departmentet för att säkerställa att det existerar
            cursor.execute("SELECT id FROM departments WHERE id = %s", (department_id,))
            dept_exists = cursor.fetchone()
            print(f"[REPO] Department exists check: {dept_exists}")
            
            # Om template_id inte är None, verifiera att mallen existerar
            if template_id is not None:
                cursor.execute("SELECT id FROM templates WHERE id = %s", (template_id,))
                template_exists = cursor.fetchone()
                print(f"[REPO] Template exists check: {template_exists}")
                if not template_exists:
                    print(f"[REPO] WARNING: Template with ID {template_id} does not exist!")
            
            # Kör uppdateringen
            cursor.execute("""
                UPDATE departments
                SET template_id = %s
                WHERE id = %s
                RETURNING id
            """, (template_id, department_id))
            
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
            print(f"Error in department repository associate_with_template at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def remove_template_association(self, department_id):
        """Remove the template association from a department."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE departments
                SET template_id = NULL
                WHERE id = %s
                RETURNING id
            """, (department_id,))
            
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
            print(f"Error in department repository remove_template_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete(self, department_id):
        """Delete a department."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM departments
                WHERE id = %s
                RETURNING id
            """, (department_id,))
            
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
            print(f"Error in department repository delete at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_by_template_id(self, template_id):
        """Get departments by template ID."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, description, created_at, template_id 
                FROM departments
                WHERE template_id = %s
            """, (template_id,))
            
            departments = []
            rows = cursor.fetchall()
            
            for row in rows:
                if hasattr(row, 'keys'):
                    department = {
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                        'template_id': row['template_id']
                    }
                else:
                    department = {
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                        'template_id': row[4]
                    }
                
                departments.append(department)
            
            return departments
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department repository get_by_template_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_by_id(self, department_id):
        """Get a department by ID."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT d.id, d.name, d.description, d.created_at, d.template_id,
                    t.title as template_title
                FROM departments d
                LEFT JOIN templates t ON d.template_id = t.id
                WHERE d.id = %s
            """, (department_id,))
            
            row = cursor.fetchone()
            
            if not row:
                return None
                
            if hasattr(row, 'keys'):
                department = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at'],
                    'template_id': row['template_id'],
                    'template': None
                }
                
                if row['template_id'] is not None:
                    department['template'] = {
                        'id': row['template_id'],
                        'title': row['template_title']
                    }
            else:
                department = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3],
                    'template_id': row[4],
                    'template': None
                }
                
                if row[4] is not None:
                    department['template'] = {
                        'id': row[4],
                        'title': row[5]
                    }
            
            return department
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department repository get_by_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return None
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close