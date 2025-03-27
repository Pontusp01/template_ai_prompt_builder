from infrastructure.database.connection import get_db_connection

class TextManagementRepository:
    def get_all_variables(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM variables")
        variables = cursor.fetchall()
        cursor.close()
        conn.close()
        return variables

    def get_variable_by_id(self, variable_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM variables WHERE id = %s", (variable_id,))
        variable = cursor.fetchone()
        cursor.close()
        conn.close()
        return variable

    def create_variable(self, variable_data):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO variables (namn, beskrivning, exempel_varde) VALUES (%s, %s, %s) RETURNING *", 
                       (variable_data['namn'], variable_data['beskrivning'], variable_data['exempel_varde']))
        variable = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return variable

    def update_variable(self, variable_id, variable_data):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE variables SET namn = %s, beskrivning = %s, exempel_varde = %s WHERE id = %s RETURNING *", 
                       (variable_data['namn'], variable_data['beskrivning'], variable_data['exempel_varde'], variable_id))
        variable = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return variable

    def delete_variable(self, variable_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM variables WHERE id = %s RETURNING *", (variable_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        return deleted