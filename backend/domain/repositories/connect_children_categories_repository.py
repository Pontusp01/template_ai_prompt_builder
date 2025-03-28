from infrastructure.database.connection import get_db_connection
import psycopg2
import psycopg2.extras
import traceback
import sys
import uuid
import datetime

class ConnectChildrenCategoryRepository:
    """Repository for connecting children categories operations."""
    
    def get_all(self):
        """Get all children category connections."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = """
                SELECT cc.id, cc.name, cc.description, cc.created_at, 
                       cc.completion_type_id, cc.department_id
                FROM connect_children_categories cc
                ORDER BY cc.name
            """
            
            cursor.execute(query)
            
            connect_children_categories = []
            for row in cursor.fetchall():
                connect_children_categories.append({
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                    'completion_type_id': row['completion_type_id'],
                    'department_id': row['department_id']
                })
            
            cursor.close()
            connection.close()
            
            return connect_children_categories
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in repository get_all at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def get_by_id(self, category_id):
        """Get a children category by ID."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = """
                SELECT cc.id, cc.name, cc.description, cc.created_at, 
                       cc.completion_type_id, cc.department_id  
                FROM connect_children_categories cc
                WHERE cc.id = %s
            """
            
            cursor.execute(query, (category_id,))
            
            row = cursor.fetchone()
            if row:
                category = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                    'completion_type_id': row['completion_type_id'],
                    'department_id': row['department_id']
                }
            else:
                category = None
            
            cursor.close()
            connection.close()
            
            return category
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in repository get_by_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def get_by_completion_type_id(self, completion_type_id):
        """Get children categories by completion type ID."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = """
                SELECT cc.id, cc.name, cc.description, cc.created_at, 
                       cc.completion_type_id, cc.department_id
                FROM connect_children_categories cc
                WHERE cc.completion_type_id = %s
                ORDER BY cc.name
            """
            
            cursor.execute(query, (completion_type_id,))
            
            categories = []
            for row in cursor.fetchall():
                categories.append({
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                    'completion_type_id': row['completion_type_id'],
                    'department_id': row['department_id']
                })
            
            cursor.close()
            connection.close()
            
            return categories
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in repository get_by_completion_type_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise

    def get_by_department_id(self, department_id):
        """Get children categories by department ID."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = """
                SELECT cc.id, cc.name, cc.description, cc.created_at, 
                       cc.completion_type_id, cc.department_id
                FROM connect_children_categories cc
                WHERE cc.department_id = %s
                ORDER BY cc.name
            """
            
            cursor.execute(query, (department_id,))
            
            categories = []
            for row in cursor.fetchall():
                categories.append({
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                    'completion_type_id': row['completion_type_id'],
                    'department_id': row['department_id']
                })
            
            cursor.close()
            connection.close()
            
            return categories
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in repository get_by_department_id at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def create(self, category_data):
        """Create a new children category."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            # Generate a new UUID if not provided
            if 'id' not in category_data or not category_data['id']:
                category_data['id'] = str(uuid.uuid4())
                
            # Set created_at to current time if not provided
            if 'created_at' not in category_data or not category_data['created_at']:
                category_data['created_at'] = datetime.datetime.now()
            
            query = """
                INSERT INTO connect_children_categories (
                    id, name, description, created_at, completion_type_id, department_id
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, name, description, created_at, completion_type_id, department_id
            """
            
            cursor.execute(query, (
                category_data['id'],
                category_data['name'],
                category_data.get('description'),
                category_data['created_at'],
                category_data.get('completion_type_id'),
                category_data.get('department_id')
            ))
            
            row = cursor.fetchone()
            category = {
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                'completion_type_id': row['completion_type_id'],
                'department_id': row['department_id']
            }
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return category
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in repository create at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def update(self, category_id, category_data):
        """Update a children category."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            # First check if the category exists
            check_query = "SELECT id FROM connect_children_categories WHERE id = %s"
            cursor.execute(check_query, (category_id,))
            
            if cursor.fetchone() is None:
                cursor.close()
                connection.close()
                return None
            
            # Update the category
            query = """
                UPDATE connect_children_categories
                SET name = %s,
                    description = %s,
                    completion_type_id = %s,
                    department_id = %s
                WHERE id = %s
                RETURNING id, name, description, created_at, completion_type_id, department_id
            """
            
            cursor.execute(query, (
                category_data['name'],
                category_data.get('description'),
                category_data.get('completion_type_id'),
                category_data.get('department_id'),
                category_id
            ))
            
            row = cursor.fetchone()
            category = {
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                'completion_type_id': row['completion_type_id'],
                'department_id': row['department_id']
            }
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return category
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in repository update at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def associate_with_completion_type(self, category_id, completion_type_id):
        """Associate a children category with a completion type."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            query = """
                UPDATE connect_children_categories
                SET completion_type_id = %s
                WHERE id = %s
                RETURNING id
            """
            
            cursor.execute(query, (completion_type_id, category_id))
            
            result = cursor.fetchone() is not None
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in repository associate_with_completion_type at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def associate_with_department(self, category_id, department_id):
        """Associate a children category with a department."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            query = """
                UPDATE connect_children_categories
                SET department_id = %s
                WHERE id = %s
                RETURNING id
            """
            
            cursor.execute(query, (department_id, category_id))
            
            result = cursor.fetchone() is not None
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in repository associate_with_department at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def remove_completion_type_association(self, category_id):
        """Remove the completion type association from a children category."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            query = """
                UPDATE connect_children_categories
                SET completion_type_id = NULL
                WHERE id = %s
                RETURNING id
            """
            
            cursor.execute(query, (category_id,))
            
            result = cursor.fetchone() is not None
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in repository remove_completion_type_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def remove_department_association(self, category_id):
        """Remove the department association from a children category."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            query = """
                UPDATE connect_children_categories
                SET department_id = NULL
                WHERE id = %s
                RETURNING id
            """
            
            cursor.execute(query, (category_id,))
            
            result = cursor.fetchone() is not None
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in repository remove_department_association at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise
    
    def delete(self, category_id):
        """Delete a children category."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            query = "DELETE FROM connect_children_categories WHERE id = %s RETURNING id"
            
            cursor.execute(query, (category_id,))
            
            result = cursor.fetchone() is not None
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return result
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error in repository delete at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            raise