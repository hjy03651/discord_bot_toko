# Import modules ===============================================
import os
import discord
import psycopg2
import embedding

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
        except Exception as err:
            print(f"Failed to initialize database connections: {err}")

    @app_commands.command(name="dbreconnect", description="데이터베이스 재연결")
    async def dbreconnect(self, interaction: discord.Interaction):
        """Reconnect to database using robust reconnection logic"""
        await interaction.response.defer()
        
        success_count = 0
        failed_handlers = []
        
        # Attempt to reconnect each handler
        handlers = [
            ("book", self.book, "ManageBook"),
            ("event", self.event, "ManageEvents"), 
            ("saving", self.saving, "ManageSaving")
        ]
        
        for name, handler, class_name in handlers:
            if handler:
                # Try to reconnect existing handler
                if handler.reconnect():
                    success_count += 1
                    print(f"Successfully reconnected {name} handler")
                else:
                    failed_handlers.append(f"{name} ({class_name})")
                    print(f"Failed to reconnect {name} handler")
            else:
                # Handler doesn't exist, try to create new one
                try:
                    if name == "book":
                        self.book = ManageBook()
                        success_count += 1
                    elif name == "event":
                        self.event = ManageEvents()
                        success_count += 1
                    elif name == "saving":
                        self.saving = ManageSaving()
                        success_count += 1
                    print(f"Successfully created new {name} handler")
                except Exception as err:
                    failed_handlers.append(f"{name} ({class_name})")
                    print(f"Failed to create new {name} handler: {err}")
        
        # Update database instances in other cogs with successfully reconnected handlers
        if success_count > 0:
            for cog_name in ["BookRetrieval", "Sql", "Event", "Saving"]:
                cog = self.bot.get_cog(cog_name)
                if cog:
                    if hasattr(cog, 'book') and self.book and self.book.is_connected():
                        cog.book = self.book
                    if hasattr(cog, 'event') and self.event and self.event.is_connected():
                        cog.event = self.event
                    if hasattr(cog, 'saving') and self.saving and self.saving.is_connected():
                        cog.saving = self.saving
        
        # Create response embed based on results
        if success_count == 3:
            # All handlers reconnected successfully
            embed = embedding.get_embed("✅ 모든 데이터베이스 연결이 성공적으로 재연결되었습니다!", title="재연결 완료")
            embed.add_field(name="재연결된 핸들러", value="📚 ManageBook\n📅 ManageEvents\n💾 ManageSaving", inline=False)
        elif success_count > 0:
            # Partial success
            embed = embedding.get_embed("⚠️ 일부 데이터베이스 연결이 재연결되었습니다", title="부분 재연결")
            embed.add_field(name="성공", value=f"{success_count}/3 핸들러", inline=True)
            if failed_handlers:
                embed.add_field(name="실패", value="\n".join(failed_handlers), inline=True)
        else:
            # Complete failure
            embed = embedding.get_embed("🐱 모든 데이터베이스 재연결이 실패했습니다! 서버 관리자에게 문의하세요", error=True)
            if failed_handlers:
                embed.add_field(name="실패한 핸들러", value="\n".join(failed_handlers), inline=False)
        
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None
        )
        
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(DBreconnection(bot))