import os
from dotenv import load_dotenv
import socket

def load_config():
    """Load configuration from environment variables."""
    load_dotenv()
    
    # Get values with fallbacks
    host = os.getenv('DB_HOST', 'db.oatxqwsmylwagybwqmjg.supabase.co')
    
    # Try DNS lookup for the hostname
    if not host.replace('.', '').isdigit() and '.' in host:
        try:
            print(f"Trying to resolve hostname {host}...")
            ip_address = socket.gethostbyname(host)
            print(f"Hostname {host} resolved to IP address {ip_address}")
        except socket.gaierror as dns_error:
            print(f"DNS error: Could not find host {host}. {dns_error}")
    
    port = os.getenv('DB_PORT', '5432')
    dbname = os.getenv('DB_NAME', 'postgres')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', 'KqM51oyYzDzVDJES')
    env = os.getenv('ENV', 'development')
    
    # Print debug info
    print(f"DB_HOST: {host}")
    print(f"DB_PORT: {port}")
    print(f"DB_NAME: {dbname}")
    print(f"DB_USER: {user}")
    # Do not print password for security reasons
    print(f"ENV: {env}")
    
    # Store connection string parts separately
    config = {
        'DB_HOST': host,
        'DB_PORT': port,
        'DB_NAME': dbname,
        'DB_USER': user,
        'DB_PASSWORD': password,
        'ENV': env,
    }
    
    return config
