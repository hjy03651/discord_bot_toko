# Import modules ===============================================
import discord
import asyncio  # for ascyn functions
import embedding as e

from discord import app_commands
from discord.ext import commands
from DBtoolSaving import ManageSaving
from datetime import datetime


# URL & lists =================================================
saving = ManageSaving()
url = "https://img.freepik.com/premium-photo/discord-logo-icon-vector-illustration_895118-9640.jpg"


# Class =======================================================
class Saving(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="보관", description="물품을 보관합니다")
    @app_commands.describe(name="물품 보관자", goods="굿즈 종류")
    async def keep_goods(
        self, interaction: discord.Interaction, name: discord.Member, goods: str
    ):
        if interaction.user.avatar is not None and name.avatar is not None:
            avatar = interaction.user.avatar.url
            member_avatar = name.display_avatar.url
        else:
            avatar = url
            member_avatar = url

        if interaction.channel_id not in (1279810905009426474, 1272086876638937130):
            embed = e.get_embed(
                ":warning: 이 커맨드는 특정 채널에서만 사용 가능합니다!", error=True
            )
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        else:
            now = datetime.now()
            formatted_date = now.strftime("%y/%m/%d %H:%M")

            if name is None:
                embed = e.get_embed(
                    f"{name}이라는 멤버는 존재하지 않습니다 :sob:", error=True
                )
                embed.set_author(name=name.display_name, icon_url=member_avatar)
                await interaction.response.send_message(embed=embed)
                return

            context = f">>> {name.mention}님의 물품을 {formatted_date}에 정상적으로 보관처리 했습니다!\n"
            context += "짐이 철수되지 않았을 경우, 6일 후에 DM을 보내드리겠습니다."
            embed = e.get_embed(context, title="짐 보관이 시작되었습니다.")
            embed.set_author(name=name.display_name, icon_url=member_avatar)
            await interaction.response.send_message(embed=embed)

            saving.store_goods(name.display_name, goods, formatted_date)

            await asyncio.sleep(6 * 24 * 60 * 60)
            if saving.get_storage(name.display_name) is not None:
                await name.send(
                    f"> {name.mention}님의 물품 보관 시간이 1일 남았습니다."
                )

    @app_commands.command(name="회수", description="물품을 회수합니다")
    @app_commands.describe(name="물품 보관자")
    async def return_goods(
        self, interaction: discord.Interaction, name: discord.Member
    ):
        if interaction.user.avatar is not None and name.avatar is not None:
            avatar = interaction.user.avatar.url
            member_avatar = name.display_avatar.url
        else:
            avatar = url
            member_avatar = url

        role = discord.utils.get(interaction.user.roles, id=1181080308590858361)
        if role is None:
            embed = e.get_embed(":warning: 명령어 사용 권한이 없습니다.", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        if interaction.channel_id not in (1279810905009426474, 1272086876638937130):
            embed = e.get_embed(
                "이 커맨드는 특정 채널에서만 사용 가능합니다!", error=True
            )
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        now = datetime.now()
        formatted_date = now.strftime("%y/%m/%d %H:%M")

        context = f">>> {name.mention}님의 물품이 {formatted_date}에 보관 리스트에서 정상적으로 삭제됐습니다!\n"
        embed = e.get_embed(context, title="짐 보관이 종료되었습니다.")
        embed.set_author(name=name.display_name, icon_url=avatar)
        await interaction.response.send_message(embed=embed)

        saving.move_out_goods(name.display_name)


async def setup(bot: commands.Bot):
    await bot.add_cog(Saving(bot))
