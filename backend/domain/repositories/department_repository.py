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
            cursor.execute("SELECT id, name, description, created_at FROM departments")
            
            departments = []
            rows = cursor.fetchall()
            
            # Debug: Print what we're getting from the database
            print(f"Query returned {len(rows)} rows")
            if rows and len(rows) > 0:
                print(f"First row type: {type(rows[0])}")
                print(f"First row content: {rows[0]}")
                print(f"First row keys: {rows[0].keys() if hasattr(rows[0], 'keys') else 'No keys method'}")
            
            # Process rows based on type
            for row in rows:
                # If using RealDictCursor (as in your connection.py), rows are dict-like
                if hasattr(row, 'keys'):
                    department = {
                        'id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at']
                    }
                # Fallback to index-based access for tuple-like rows
                else:
                    department = {
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3]
                    }
                
                departments.append(department)
            
            return departments
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in department repository get_all at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            # Return empty list instead of crashing
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
                SELECT id, name, description, created_at
                FROM departments 
                WHERE id = %s
            """, (department_id,))
            
            row = cursor.fetchone()
            
            if not row:
                return None
                
            # If using RealDictCursor, row is dict-like
            if hasattr(row, 'keys'):
                department = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at']
                }
            # Fallback to index-based access
            else:
                department = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3]
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
                conn.close()
    
    def create(self, department_data):
        """Create a new department."""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO departments (name, description)
                VALUES (%s, %s)
                RETURNING id, name, description, created_at
            """, (department_data['name'], department_data.get('description')))
            
            row = cursor.fetchone()
            
            # Handle the return value based on cursor type
            if row is None:
                raise ValueError("No data returned from department insert")
            
            # If using RealDictCursor, row is dict-like
            if hasattr(row, 'keys'):
                department = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at']
                }
            # Fallback to index-based access
            else:
                department = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3]
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
            
            cursor.execute("""
                UPDATE departments
                SET name = %s, description = %s
                WHERE id = %s
                RETURNING id, name, description, created_at
            """, (
                department_data['name'],
                department_data.get('description'),
                department_id
            ))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # If using RealDictCursor, row is dict-like
            if hasattr(row, 'keys'):
                department = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else row['created_at']
                }
            # Fallback to index-based access
            else:
                department = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3]
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