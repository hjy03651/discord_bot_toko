# Import modules ===============================================
import discord
import asyncio  # for ascyn functions
import psycopg2  # for connecting psql
import embedding as e

from discord import app_commands
from discord.ext import commands
from DBtoolBook import ManageBook


# URL & lists =================================================
book = ManageBook()
url = 'https://img.freepik.com/premium-photo/discord-logo-icon-vector-illustration_895118-9640.jpg'


# Class =======================================================
class Sql(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sql", description="봇 오류시")
    @app_commands.describe(command="지정 커맨드", sql="sql문")
    @app_commands.choices(command=[
        app_commands.Choice(name="select", value="select"),
        app_commands.Choice(name="insert", value="insert"),
        app_commands.Choice(name="update", value="update"),
        app_commands.Choice(name="delete", value="delete")
    ])
    async def write_sql(self, interaction: discord.Interaction, command: app_commands.Choice[str], sql: str):
        role = discord.utils.get(interaction.user.roles, id=1181080308590858361)
        if role is None:
            embed = e.get_embed(':warning: 명령어 사용 권한이 없습니다.', error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        try:
            get = book.get_sql(command.value, sql)
            if command.value != 'select':
                context = 'return None'
                embed = e.get_embed(context, title='sql문이 실행됐습니다.')
                embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)
            elif command.value == 'select' and get is not None:
                context = f'실행: /sql {command.value} {sql}'
                for n, items in enumerate(get):
                    if n > 15:
                        break
                    context += f'\n\n{items} \n'

                embed = e.get_embed(context, title='sql문이 실행됐습니다.')
                embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)
            else:
                embed = e.get_embed(':warning: 반환값이 없습니다.', error=True)
                embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)
            book.restart()
        except psycopg2.errors.UndefinedColumn:
            embed = e.get_embed(':warning: 반환값이 없습니다.', error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            book.restart()
            return
        except (psycopg2.errors.SyntaxError,
                discord.app_commands.errors.CommandInvokeError,
                psycopg2.errors.InvalidColumnReference):
            embed = e.get_embed(':warning: 구문오류!', error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            book.restart()
            return
        except InFailedSqlTransaction:
            embed = e.get_embed(':warning: 반환값이 없습니다.', error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            book.restart()
            return

    @app_commands.command(name="restart", description="데베 오류시")
    async def restart_db(self, interaction: discord.Interaction):
        book.restart()

        context = '짠 ✨'
        embed = e.get_embed(context, title='데이터베이스가 재시작됐습니다.')
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Sql(bot))
