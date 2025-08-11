import mysql.connector
from mysql.connector import pooling
import os

# Connection pool settings
dbconfig = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "reservation_service_db")
}

# Create connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="analytics_pool",
    pool_size=5,
    pool_reset_session=True,
    **dbconfig
)

def get_db_connection():
    """
    Get a pooled DB connection.
    Always close() it after using (or use with-statement).
    """
    return connection_pool.get_connection()
