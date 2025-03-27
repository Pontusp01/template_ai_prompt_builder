from flask import jsonify
import traceback
import sys

def register_debug_routes(app):
    """Register debug-related routes with the Flask app."""
    
    @app.route('/api/debug/db-status', methods=['GET'])
    def check_db_status():
        try:
            from infrastructure.database.connection import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if we can connect to the database
            cursor.execute("SELECT 1")
            db_connect = cursor.fetchone() is not None
            
            # Check which tables exist
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = [row[0] if isinstance(row, tuple) else row['table_name'] for row in cursor.fetchall()]
            
            # Check column structure of templates table
            template_columns = []
            if 'templates' in tables:
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'templates'
                """)
                template_columns = [
                    {'name': row[0] if isinstance(row, tuple) else row['column_name'], 
                     'type': row[1] if isinstance(row, tuple) else row['data_type']}
                    for row in cursor.fetchall()
                ]
            
            # Check column structure of colors table
            color_columns = []
            if 'colors' in tables:
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'colors'
                """)
                color_columns = [
                    {'name': row[0] if isinstance(row, tuple) else row['column_name'], 
                     'type': row[1] if isinstance(row, tuple) else row['data_type']}
                    for row in cursor.fetchall()
                ]
            
            # Check column structure of completion_types table
            completion_type_columns = []
            if 'completion_types' in tables:
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'completion_types'
                """)
                completion_type_columns = [
                    {'name': row[0] if isinstance(row, tuple) else row['column_name'], 
                     'type': row[1] if isinstance(row, tuple) else row['data_type']}
                    for row in cursor.fetchall()
                ]
            
            cursor.close()
            conn.close()
            
            return jsonify({
                'database_connected': db_connect,
                'tables': tables,
                'template_columns': template_columns,
                'color_columns': color_columns,
                'completion_type_columns': completion_type_columns
            })
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error checking database status at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to check database status', 'details': str(e)}), 500