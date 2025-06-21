"""Tests for DBclass.py module."""
import pytest
from unittest.mock import MagicMock, patch, call
import os
from DBclass import Databases


class TestDatabases:
    """Test cases for Databases class."""

    @patch('DBclass.psycopg2.connect')
    @patch('DBclass.load_dotenv')
    @patch.dict(os.environ, {
        'DB_HOST': 'test_host',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_pass',
        'DB_PORT': '5432'
    })
    def test_init_connection(self, mock_load_dotenv, mock_connect):
        """Test database connection initialization."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        db = Databases()
        
        mock_load_dotenv.assert_called_once()
        mock_connect.assert_called_once_with(
            host='test_host',
            dbname='test_db',
            user='test_user',
            password='test_pass',
            port='5432'
        )
        assert db.db == mock_connection
        assert db.cursor == mock_cursor

    @patch('DBclass.psycopg2.connect')
    @patch('DBclass.load_dotenv')
    def test_execute_with_args(self, mock_load_dotenv, mock_connect):
        """Test execute method with arguments."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('result1',), ('result2',)]
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        db = Databases()
        query = "SELECT * FROM table WHERE id = %s"
        args = (1,)
        
        result = db.execute(query, args)
        
        mock_cursor.execute.assert_called_once_with(query, args)
        mock_cursor.fetchall.assert_called_once()
        assert result == [('result1',), ('result2',)]

    @patch('DBclass.psycopg2.connect')
    @patch('DBclass.load_dotenv')
    def test_execute_without_args(self, mock_load_dotenv, mock_connect):
        """Test execute method without arguments."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('result1',), ('result2',)]
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        db = Databases()
        query = "SELECT * FROM table"
        
        result = db.execute(query)
        
        mock_cursor.execute.assert_called_once_with(query, {})
        mock_cursor.fetchall.assert_called_once()
        assert result == [('result1',), ('result2',)]

    @patch('DBclass.psycopg2.connect')
    @patch('DBclass.load_dotenv')
    def test_commit(self, mock_load_dotenv, mock_connect):
        """Test commit method."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        db = Databases()
        db.commit()
        
        mock_cursor.commit.assert_called_once()

    @patch('DBclass.psycopg2.connect')
    @patch('DBclass.load_dotenv')
    def test_del_closes_connections(self, mock_load_dotenv, mock_connect):
        """Test that __del__ closes database connections."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        db = Databases()
        db.__del__()
        
        mock_connection.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('DBclass.psycopg2.connect')
    @patch('DBclass.load_dotenv')
    def test_connection_error_handling(self, mock_load_dotenv, mock_connect):
        """Test handling of connection errors."""
        mock_connect.side_effect = Exception("Connection failed")
        
        with pytest.raises(Exception) as exc_info:
            db = Databases()
        
        assert str(exc_info.value) == "Connection failed"