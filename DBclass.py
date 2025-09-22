import os
import time
import threading

import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv


class Databases:
    _connection_pool = None
    _pool_lock = threading.Lock()
    
    def __init__(self):
        load_dotenv()
        self._ensure_connection_pool()
        self._get_connection()
    
    def _ensure_connection_pool(self):
        """Ensure connection pool exists with proper configuration for external RDS"""
        with self._pool_lock:
            if self._connection_pool is None:
                try:
                    self._connection_pool = psycopg2.pool.ThreadedConnectionPool(
                        minconn=1,
                        maxconn=10,
                        host=os.getenv("DB_HOST"),
                        dbname=os.getenv("DB_NAME"),
                        user=os.getenv("DB_USER"),
                        password=os.getenv("DB_PASSWORD"),
                        port=os.getenv("DB_PORT"),
                        # RDS-optimized connection settings
                        connect_timeout=30,
                        keepalives_idle=300,
                        keepalives_interval=30,
                        keepalives_count=3,
                        tcp_user_timeout=60000
                    )
                    print("Database connection pool created successfully")
                except Exception as e:
                    print(f"Failed to create connection pool: {e}")
                    raise
    
    def _get_connection(self):
        """Get connection from pool with retry logic"""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                self.db = self._connection_pool.getconn()
                if self.db:
                    self.cursor = self.db.cursor()
                    # Test connection
                    self.cursor.execute("SELECT 1")
                    self.cursor.fetchone()
                    print(f"Successfully obtained database connection (attempt {attempt + 1})")
                    return
            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if self.db:
                    try:
                        self._connection_pool.putconn(self.db)
                    except:
                        pass
                    self.db = None
                    self.cursor = None
                
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    raise Exception(f"Failed to get database connection after {max_retries} attempts")

    def close(self):
        """Return connection to pool instead of closing"""
        try:
            if hasattr(self, "cursor") and self.cursor:
                self.cursor.close()
                self.cursor = None
        except Exception as e:
            print(f"Warning: Error closing cursor: {e}")

        try:
            if hasattr(self, "db") and self.db and self._connection_pool:
                self._connection_pool.putconn(self.db)
                self.db = None
        except Exception as e:
            print(f"Warning: Error returning connection to pool: {e}")
    
    @classmethod
    def close_all_connections(cls):
        """Close entire connection pool"""
        with cls._pool_lock:
            if cls._connection_pool:
                try:
                    cls._connection_pool.closeall()
                    cls._connection_pool = None
                    print("All database connections closed")
                except Exception as e:
                    print(f"Error closing connection pool: {e}")

    def __del__(self):
        self.close()

    def execute(self, query, args=None):
        if args is None:
            args = {}
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()

    def reconnect(self):
        """Robust reconnection with pool refresh"""
        print("Starting robust database reconnection...")
        
        # Clean up current connection
        self.close()
        
        # Force reload environment variables
        load_dotenv(override=True)
        
        # Reset connection pool to force fresh connections
        with self._pool_lock:
            if self._connection_pool:
                try:
                    self._connection_pool.closeall()
                    self._connection_pool = None
                    print("Existing connection pool closed")
                except Exception as e:
                    print(f"Error closing existing pool: {e}")
        
        # Wait a moment for connections to fully close
        time.sleep(2)
        
        try:
            # Recreate connection pool and get new connection
            self._ensure_connection_pool()
            self._get_connection()
            
            # Additional connection test
            self.cursor.execute("SELECT current_timestamp, version()")
            result = self.cursor.fetchone()
            print(f"Reconnection successful. Server time: {result[0]}")
            
            return True
            
        except Exception as e:
            print(f"Database reconnection failed: {e}")
            return False

    def is_connected(self):
        """Check if the database connection is still alive"""
        try:
            if not hasattr(self, "db") or not self.db:
                return False
            if self.db.closed:
                return False
            if not hasattr(self, "cursor") or not self.cursor:
                return False
            
            # Test with a simple query with timeout
            self.cursor.execute("SELECT 1")
            result = self.cursor.fetchone()
            return result is not None
            
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def execute_with_retry(self, query, args=None, max_retries=3):
        """Execute query with automatic retry on connection failure"""
        for attempt in range(max_retries):
            try:
                if not self.is_connected():
                    print(f"Connection lost, attempting reconnection (attempt {attempt + 1})")
                    if not self.reconnect():
                        continue
                
                return self.execute(query, args)
                
            except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                print(f"Database error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    if not self.reconnect():
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                else:
                    raise
            except Exception as e:
                print(f"Unexpected error: {e}")
                raise
        
        raise Exception(f"Failed to execute query after {max_retries} attempts")
