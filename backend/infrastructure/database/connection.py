import psycopg2
from psycopg2.extras import RealDictCursor
from infrastructure.config.config import load_config
import traceback
import sys

def get_db_connection():
    """Get a database connection."""
    config = load_config()
    
    try:
        # For Supabase, the username might contain a dot which is part of the format
        # We don't need to sanitize this as it's expected
        conn = psycopg2.connect(
            host=config['DB_HOST'],
            port=config['DB_PORT'],
            dbname=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            cursor_factory=RealDictCursor
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        # Show detailed error information
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = traceback.extract_tb(exc_tb)[-1][0]
        line = traceback.extract_tb(exc_tb)[-1][1]
        print(f"Connection error in {fname} at line {line}: {e}")
        
        # Try an alternative connection approach - sometimes Supabase requires a connection string
        try:
            print("Trying alternative connection method...")
            conn_string = f"postgresql://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}"
            conn = psycopg2.connect(conn_string, cursor_factory=RealDictCursor)
            conn.autocommit = True
            print("Alternative connection method successful!")
            return conn
        except Exception as e2:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Second attempt failed in {fname} at line {line}: {e2}")
            
            # One more attempt with URL-encoded password
            try:
                import urllib.parse
                print("Trying with URL-encoded password...")
                encoded_password = urllib.parse.quote_plus(config['DB_PASSWORD'])
                encoded_user = urllib.parse.quote_plus(config['DB_USER'])
                conn_string = f"postgresql://{encoded_user}:{encoded_password}@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}"
                conn = psycopg2.connect(conn_string, cursor_factory=RealDictCursor)
                conn.autocommit = True
                print("URL-encoded connection successful!")
                return conn
            except Exception as e3:
                print(f"Third attempt failed: {e3}")
                raise e3

def test_connection():
    """Test the database connection."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 as test')
        result = cursor.fetchone()
        print(f"Connection test successful: {result}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = traceback.extract_tb(exc_tb)[-1][0]
        line = traceback.extract_tb(exc_tb)[-1][1]
        print(f"Database connection error in {fname} at line {line}: {e}")
        print(f"Stacktrace: {traceback.format_exc()}")
        return False
