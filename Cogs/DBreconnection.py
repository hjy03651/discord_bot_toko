# Import modules ===============================================
import os
import discord
import psycopg2
import embedding as e

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from DBclass import Databases
from DBtoolBook import ManageBook
from DBtoolEvent import ManageEvents
from DBtoolSaving import ManageSaving


# Class =======================================================
class DBreconnection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.book = None
        self.event = None
        self.saving = None
        self._init_connections()

    def _init_connections(self):
        """Initialize database connections"""
        try:
            self.book = ManageBook()
            self.event = ManageEvents()
            self.saving = ManageSaving()
        except Exception as e:
            print(f"Failed to initialize database connections: {e}")

    @app_commands.command(name="dbreconnect", description="데이터베이스 재연결")
    async def dbreconnect(self, interaction: discord.Interaction):
        """Reconnect to database"""
        await interaction.response.defer()
        
        success = True
        error_msg = ""
        
        try:
            # Close existing connections if they exist
            if self.book:
                try:
                    self.book.__del__()
                except:
                    pass
            if self.event:
                try:
                    self.event.__del__()
                except:
                    pass
            if self.saving:
                try:
                    self.saving.__del__()
                except:
                    pass
            
            # Try to reconnect
            load_dotenv()
            test_conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT"),
            )
            test_conn.close()
            
            # If test connection successful, reinitialize all connections
            self.book = ManageBook()
            self.event = ManageEvents()
            self.saving = ManageSaving()
            
            # Update global book instance in other cogs if they exist
            for cog_name in ["BookRetrieval", "Sql", "Event", "Saving"]:
                cog = self.bot.get_cog(cog_name)
                if cog and hasattr(cog, 'book'):
                    cog.book = self.book
                if cog and hasattr(cog, 'event'):
                    cog.event = self.event
                if cog and hasattr(cog, 'saving'):
                    cog.saving = self.saving
            
        except psycopg2.OperationalError as err:
            success = False
            error_msg = f"Database connection failed: {str(err)}"
        except Exception as err:
            success = False
            error_msg = f"Unexpected error: {str(err)}"
        
        if success:
            embed = e.get_embed("✅ 데이터베이스 재연결 성공!", title="재연결 완료")
            embed.set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.avatar.url if interaction.user.avatar else None
            )
        else:
            embed = e.get_embed(f"🐱 재연결 실패! 서버 관리자에게 문의하세요", error=True)
            embed.add_field(name="오류 내용", value=error_msg[:1024], inline=False)
            embed.set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.avatar.url if interaction.user.avatar else None
            )
        
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(DBreconnection(bot))