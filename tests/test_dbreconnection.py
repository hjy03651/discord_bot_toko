import unittest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
from discord.ext import commands
import psycopg2

from Cogs.DBreconnection import DBreconnection


class TestDBreconnection(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.bot = Mock(spec=commands.Bot)
        self.bot.get_cog = Mock(return_value=None)
        
    @patch('Cogs.DBreconnection.ManageBook')
    @patch('Cogs.DBreconnection.ManageEvents')
    @patch('Cogs.DBreconnection.ManageSaving')
    def test_init_connections_success(self, mock_saving, mock_event, mock_book):
        """Test successful initialization of database connections"""
        # Create cog instance
        cog = DBreconnection(self.bot)
        
        # Verify all connections were initialized
        mock_book.assert_called_once()
        mock_event.assert_called_once()
        mock_saving.assert_called_once()
        
        self.assertIsNotNone(cog.book)
        self.assertIsNotNone(cog.event)
        self.assertIsNotNone(cog.saving)
    
    @patch('Cogs.DBreconnection.ManageBook', side_effect=Exception("Connection failed"))
    @patch('Cogs.DBreconnection.ManageEvents')
    @patch('Cogs.DBreconnection.ManageSaving')
    @patch('builtins.print')
    def test_init_connections_failure(self, mock_print, mock_saving, mock_event, mock_book):
        """Test handling of failed database connection during init"""
        # Create cog instance
        cog = DBreconnection(self.bot)
        
        # Verify error was printed
        mock_print.assert_called_with("Failed to initialize database connections: Connection failed")
        
    @patch('Cogs.DBreconnection.psycopg2.connect')
    @patch('Cogs.DBreconnection.ManageBook')
    @patch('Cogs.DBreconnection.ManageEvents')
    @patch('Cogs.DBreconnection.ManageSaving')
    @patch('Cogs.DBreconnection.load_dotenv')
    @patch('Cogs.DBreconnection.os.getenv')
    async def test_dbreconnect_success(self, mock_getenv, mock_load_dotenv, 
                                       mock_saving, mock_event, mock_book, mock_connect):
        """Test successful database reconnection"""
        # Setup environment variables
        mock_getenv.side_effect = lambda key: {
            "DB_HOST": "localhost",
            "DB_NAME": "testdb",
            "DB_USER": "testuser",
            "DB_PASSWORD": "testpass",
            "DB_PORT": "5432"
        }.get(key)
        
        # Setup mock connection
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        
        # Create cog and setup existing connections
        cog = DBreconnection(self.bot)
        cog.book = Mock()
        cog.event = Mock()
        cog.saving = Mock()
        
        # Setup mock interaction
        interaction = AsyncMock(spec=discord.Interaction)
        interaction.user = Mock()
        interaction.user.display_name = "TestUser"
        interaction.user.avatar = Mock()
        interaction.user.avatar.url = "http://example.com/avatar.png"
        
        # Mock embed creation
        with patch('Cogs.DBreconnection.e.get_embed') as mock_embed:
            mock_embed_obj = Mock()
            mock_embed.return_value = mock_embed_obj
            
            # Execute command
            await cog.dbreconnect(interaction)
            
            # Verify connection attempt
            mock_connect.assert_called_once_with(
                host="localhost",
                dbname="testdb",
                user="testuser",
                password="testpass",
                port="5432"
            )
            
            # Verify success message
            mock_embed.assert_called_with("✅ 데이터베이스 재연결 성공!", title="재연결 완료")
            interaction.followup.send.assert_called_once_with(embed=mock_embed_obj)
    
    @patch('Cogs.DBreconnection.psycopg2.connect', side_effect=psycopg2.OperationalError("Connection refused"))
    @patch('Cogs.DBreconnection.load_dotenv')
    @patch('Cogs.DBreconnection.os.getenv')
    async def test_dbreconnect_operational_error(self, mock_getenv, mock_load_dotenv, mock_connect):
        """Test database reconnection with operational error"""
        # Setup environment variables
        mock_getenv.side_effect = lambda key: {
            "DB_HOST": "localhost",
            "DB_NAME": "testdb",
            "DB_USER": "testuser",
            "DB_PASSWORD": "testpass",
            "DB_PORT": "5432"
        }.get(key)
        
        # Create cog
        cog = DBreconnection(self.bot)
        
        # Setup mock interaction
        interaction = AsyncMock(spec=discord.Interaction)
        interaction.user = Mock()
        interaction.user.display_name = "TestUser"
        interaction.user.avatar = None  # Test without avatar
        
        # Mock embed creation
        with patch('Cogs.DBreconnection.e.get_embed') as mock_embed:
            mock_embed_obj = Mock()
            mock_embed_obj.add_field = Mock()
            mock_embed.return_value = mock_embed_obj
            
            # Execute command
            await cog.dbreconnect(interaction)
            
            # Verify error message
            mock_embed.assert_called_with("🐱 재연결 실패! 서버 관리자에게 문의하세요", error=True)
            mock_embed_obj.add_field.assert_called_once()
            interaction.followup.send.assert_called_once_with(embed=mock_embed_obj)
    
    @patch('Cogs.DBreconnection.psycopg2.connect')
    @patch('Cogs.DBreconnection.ManageBook')
    @patch('Cogs.DBreconnection.ManageEvents')
    @patch('Cogs.DBreconnection.ManageSaving')
    @patch('Cogs.DBreconnection.load_dotenv')
    @patch('Cogs.DBreconnection.os.getenv')
    async def test_dbreconnect_updates_other_cogs(self, mock_getenv, mock_load_dotenv,
                                                  mock_saving, mock_event, mock_book, mock_connect):
        """Test that reconnection updates database instances in other cogs"""
        # Setup environment variables
        mock_getenv.side_effect = lambda key: {
            "DB_HOST": "localhost",
            "DB_NAME": "testdb",
            "DB_USER": "testuser",
            "DB_PASSWORD": "testpass",
            "DB_PORT": "5432"
        }.get(key)
        
        # Setup mock connection
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        
        # Create cog
        cog = DBreconnection(self.bot)
        
        # Setup mock cogs with database attributes
        mock_book_cog = Mock()
        mock_book_cog.book = None
        mock_sql_cog = Mock()
        mock_sql_cog.book = None
        
        self.bot.get_cog.side_effect = lambda name: {
            "BookRetrieval": mock_book_cog,
            "Sql": mock_sql_cog
        }.get(name)
        
        # Setup mock interaction
        interaction = AsyncMock(spec=discord.Interaction)
        interaction.user = Mock()
        interaction.user.display_name = "TestUser"
        interaction.user.avatar = Mock()
        interaction.user.avatar.url = "http://example.com/avatar.png"
        
        # Mock embed creation
        with patch('Cogs.DBreconnection.e.get_embed') as mock_embed:
            mock_embed.return_value = Mock()
            
            # Execute command
            await cog.dbreconnect(interaction)
            
            # Verify other cogs were updated
            self.assertIsNotNone(mock_book_cog.book)
            self.assertIsNotNone(mock_sql_cog.book)


if __name__ == '__main__':
    unittest.main()