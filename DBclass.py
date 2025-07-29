import os

import psycopg2
from dotenv import load_dotenv


class Databases:
    def __init__(self):
        load_dotenv()
        self.db = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
        )
        self.cursor = self.db.cursor()

    def close(self):
        """Safely close database connections"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
        except Exception as e:
            print(f"Warning: Error closing cursor: {e}")
        
        try:
            if hasattr(self, 'db') and self.db:
                self.db.close()
        except Exception as e:
            print(f"Warning: Error closing database connection: {e}")
    
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
        """Reconnect to the database with a new connection"""
        # Store old connections
        old_db = getattr(self, 'db', None)
        old_cursor = getattr(self, 'cursor', None)
        
        try:
            # Create new connections
            load_dotenv()
            new_db = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT"),
            )
            new_cursor = new_db.cursor()
            
            # Test the new connection with a simple query
            new_cursor.execute("SELECT 1")
            new_cursor.fetchone()
            
            # If we reach here, the new connection is working
            # Close old connections safely
            if old_cursor:
                try:
                    old_cursor.close()
                except:
                    pass
            if old_db:
                try:
                    old_db.close()
                except:
                    pass
            
            # Replace with new connections
            self.db = new_db
            self.cursor = new_cursor
            
            return True
            
        except Exception as e:
            # If reconnection fails, keep the old connections if they exist
            print(f"Database reconnection failed: {e}")
            
            # Clean up failed new connections
            try:
                if 'new_cursor' in locals():
                    new_cursor.close()
            except:
                pass
            try:
                if 'new_db' in locals():
                    new_db.close()
            except:
                pass
            
            return False
    
    def is_connected(self):
        """Check if the database connection is still alive"""
        try:
            if not hasattr(self, 'db') or not self.db:
                return False
            if self.db.closed:
                return False
            # Test with a simple query
            self.cursor.execute("SELECT 1")
            self.cursor.fetchone()
            return True
        except:
            return False
