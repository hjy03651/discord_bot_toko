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

    @app_commands.command(name="dbreconnect", description="데이터베이스 강력 재연결")
    async def dbreconnect(self, interaction: discord.Interaction):
        """Force complete database reconnection with full cleanup and re-initialization"""
        await interaction.response.defer()

        embed = embedding.get_embed(
            "🔄 강력한 데이터베이스 재연결을 시작합니다...",
            title="강력 재연결 진행 중",
        )
        await interaction.followup.send(embed=embed)

        success_count = 0
        failed_handlers = []
        reconnection_details = []

        # Phase 1: Complete cleanup of all existing connections
        print("Phase 1: Cleaning up all existing database connections...")
        handlers_info = [
            ("book", "ManageBook", ManageBook),
            ("event", "ManageEvents", ManageEvents), 
            ("saving", "ManageSaving", ManageSaving),
        ]

        for name, class_name, handler_class in handlers_info:
            try:
                # Force close existing handler
                current_handler = getattr(self, name, None)
                if current_handler:
                    if hasattr(current_handler, 'close'):
                        current_handler.close()
                    if hasattr(current_handler, 'db') and current_handler.db:
                        try:
                            current_handler.db.close()
                        except:
                            pass
                    if hasattr(current_handler, 'cursor') and current_handler.cursor:
                        try:
                            current_handler.cursor.close()
                        except:
                            pass
                    del current_handler
                
                # Reset the attribute
                setattr(self, name, None)
                reconnection_details.append(f"✅ {class_name} 기존 연결 정리 완료")
                print(f"Cleaned up existing {name} handler")
                
            except Exception as e:
                reconnection_details.append(f"⚠️ {class_name} 정리 중 경고: {str(e)[:50]}...")
                print(f"Warning during {name} cleanup: {e}")

        # Phase 2: Wait and reload environment
        print("Phase 2: Reloading environment and waiting...")
        import time
        time.sleep(2)  # Give time for connections to fully close
        
        # Force reload environment variables
        load_dotenv(override=True)
        reconnection_details.append("🔄 환경 변수 재로드 완료")

        # Phase 3: Create completely new handlers with retries
        print("Phase 3: Creating new database handlers...")
        for name, class_name, handler_class in handlers_info:
            max_retries = 3
            retry_delay = 1
            
            for attempt in range(max_retries):
                try:
                    print(f"Creating new {name} handler (attempt {attempt + 1}/{max_retries})")
                    
                    # Create completely new handler instance
                    new_handler = handler_class()
                    
                    # Test the connection immediately
                    if hasattr(new_handler, 'is_connected') and new_handler.is_connected():
                        setattr(self, name, new_handler)
                        success_count += 1
                        reconnection_details.append(f"✅ {class_name} 새로운 연결 생성 성공")
                        print(f"Successfully created new {name} handler")
                        break
                    else:
                        # Connection test failed, clean up and retry
                        if hasattr(new_handler, 'close'):
                            new_handler.close()
                        del new_handler
                        
                        if attempt < max_retries - 1:
                            reconnection_details.append(f"⚠️ {class_name} 연결 테스트 실패, 재시도 중...")
                            time.sleep(retry_delay)
                            retry_delay *= 2
                        else:
                            raise Exception("Connection test failed after creation")
                            
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed for {name}: {e}")
                    if attempt == max_retries - 1:
                        failed_handlers.append(f"{name} ({class_name})")
                        reconnection_details.append(f"❌ {class_name} 연결 실패: {str(e)[:50]}...")
                    elif attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2

        # Phase 4: Update all other cogs with new handlers
        print("Phase 4: Updating other cogs with new handlers...")
        if success_count > 0:
            updated_cogs = []
            for cog_name in ["BookRetrieval", "Sql", "Event", "Saving"]:
                cog = self.bot.get_cog(cog_name)
                if cog:
                    updates_made = False
                    if hasattr(cog, "book") and self.book and self.book.is_connected():
                        cog.book = self.book
                        updates_made = True
                    if hasattr(cog, "event") and self.event and self.event.is_connected():
                        cog.event = self.event
                        updates_made = True
                    if hasattr(cog, "saving") and self.saving and self.saving.is_connected():
                        cog.saving = self.saving
                        updates_made = True
                    
                    if updates_made:
                        updated_cogs.append(cog_name)
            
            if updated_cogs:
                reconnection_details.append(f"🔄 업데이트된 Cogs: {', '.join(updated_cogs)}")

        # Create final response embed
        if success_count == 3:
            embed = embedding.get_embed(
                "✅ 강력 재연결이 완전히 성공했습니다!",
                title="재연결 완료",
            )
            embed.add_field(
                name="재연결된 핸들러 (3/3)",
                value="📚 ManageBook\n📅 ManageEvents\n💾 ManageSaving",
                inline=False,
            )
        elif success_count > 0:
            embed = embedding.get_embed(
                f"⚠️ 부분 재연결 성공 ({success_count}/3)",
                title="부분 재연결",
            )
            if failed_handlers:
                embed.add_field(
                    name="실패한 핸들러", 
                    value="\n".join([f"❌ {h}" for h in failed_handlers]), 
                    inline=False
                )
        else:
            embed = embedding.get_embed(
                "❌ 강력 재연결이 모두 실패했습니다. 네트워크나 DB 서버 상태를 확인해주세요.",
                error=True,
            )

        # Add detailed process information
        if reconnection_details:
            details_text = "\n".join(reconnection_details[-10:])  # Show last 10 details
            embed.add_field(
                name="재연결 과정",
                value=details_text,
                inline=False,
            )

        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None,
        )

        await interaction.edit_original_response(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(DBreconnection(bot))
