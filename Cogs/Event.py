# Import modules ===============================================
import discord
import embedding as e

from discord import app_commands
from discord.ext import commands
from DBtoolEvent import ManageEvents


# URL & lists =================================================
event = ManageEvents()
url = "https://img.freepik.com/premium-photo/discord-logo-icon-vector-illustration_895118-9640.jpg"


# Class =======================================================
class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="event", description="이벤트 참여자를 집계합니다")
    @app_commands.describe(title="이벤트명", number="당첨자 수")
    async def finish_event(
        self, interaction: discord.Interaction, title: str, number: int
    ):
        if interaction.user.avatar is not None:
            avatar = interaction.user.avatar.url
        else:
            avatar = url

        role = discord.utils.get(interaction.user.roles, id=1181080308590858361)
        if role is None:
            embed = e.get_embed(":warning: 명령어 사용 권한이 없습니다.", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        image_count = {}

        channel = interaction.channel
        event.delete_all(title)

        async for message in channel.history(limit=200):
            for attachment in message.attachments:
                if attachment.content_type and "image" in attachment.content_type:
                    display_name = message.author.display_name
                    if display_name in image_count:
                        image_count[display_name] *= 1.4
                    else:
                        image_count[display_name] = 1

            # 결과 출력
        if image_count:
            for name, count in image_count.items():
                event.new_participation(title, name, count)

            winners = event.get_random(title, number)

            ctx = ""
            for win in winners:
                ctx += f"{win}\n"

            embed = e.get_embed(ctx, title="이벤트 당첨 축하드립니다!")
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)

        else:
            embed = e.get_embed(":warning: 이벤트 참여자가 없습니다.", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Event(bot))
