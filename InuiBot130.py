# Import modules ===============================================
import discord
import asyncio
import sys
import os
import requests
import time

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime


# Intents (for bot) ===========================================
intents = discord.Intents.default()
intents.message_content = True  # 메세지 읽기/보내기 권한
intents.messages = True
intents.voice_states = True  # 음성채팅 감지 권한
intents.guilds = True  # 서버 연결 권한
intents.members = True  # 멤버 열람 권한

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
app_id = os.getenv("DISCORD_APPID")

bot = commands.Bot(command_prefix='$', intents=intents, application_id=app_id)

first_ready = True

"""channel_list = ['VC-1', 'VC-2', 'VC-3', 'VC-CONF', 'VC-W1', 'VC-W2', 'VC-st', 'VC-bed', 'VC-hehe']
channel_id = []
for i in channel_list:
    channel_id.append(os.getenv(i))

    channels = {os.getenv("VC-1"): "VC-1",
                os.getenv("VC-2"): "VC-2",
                os.getenv("VC-3"): "VC-3",
                os.getenv("VC-CONF"): "VC-conf",
                os.getenv("VC-W1"): "VC-w1",
                os.getenv("VC-W2"): "VC-w2",
                os.getenv("VC-ST"): "VC-st",
                os.getenv("VC-BED"): "VC-bed",
                os.getenv("VC-HEHE"): "VC-hehe"
                }
"""  # 일단 나중에 생각해보기


async def load_extensions():
    for filename in 'BookRetrieval Event ForFun Saving Sql'.split():
        await bot.load_extension(f"Cogs.{filename}")


@bot.event
async def setup_hook():
    await load_extensions()
    await bot.tree.sync()


@bot.event
async def on_ready():
    global first_ready

    if not first_ready:
        return
    first_ready = False

    print(f"\n[READY] 봇 로그인 완료: {bot.user} (ID: {bot.user.id})")
    print(f"[READY] 총 {len(bot.tree.get_commands())}개의 슬래시 커맨드를 로드했습니다.")


@bot.event
async def on_voice_state_update(member, before, after):
    """
    to give or delete role from a member who were in voice chat.
    :param member: get member list
    :param before: get before channel
    :param after: get after channel
    :return: None
    """
    channels = {1272081235338068040: "VC-1",
                1272081519632060436: "VC-2",
                1272081537499926591: "VC-3",
                1272081866752659489: "VC-conf",
                1272082585798971442: "VC-w1",
                1272243777989382214: "VC-w2",
                1272082611656982539: "VC-st",
                1272082622981345361: "VC-bed",
                1346093416345505792: "VC-hehe"
                }
    guild = member.guild

    now = datetime.now()
    date = now.strftime("%y/%m/%d %H:%M")

    # enter
    if before.channel is not None and after.channel is None:
        before_role = discord.utils.get(guild.roles, name=channels[before.channel.id])
        if channels[before.channel.id] != "VC-hehe":
            await bot.get_command('clear')(before)
        await member.remove_roles(before_role)
        print(f"Removed role '{channels[before.channel.id]}' from {member.display_name} at {date}")

    elif after.channel.id in list(channels.keys()):
        after_role = discord.utils.get(guild.roles, name=channels[after.channel.id])
        await member.add_roles(after_role)

        if before.channel is None:
            print(f"Assigned role '{channels[after.channel.id]}' to {member.display_name} at {date}")
        elif before.channel != after.channel:
            before_role = discord.utils.get(guild.roles, name=channels[before.channel.id])
            if channels[before.channel.id] != "VC-hehe":
                await bot.get_command('clear')(before)
            await member.remove_roles(before_role)
            print(f"Changed role '{channels[after.channel.id]}' to {member.display_name} at {date}")


@bot.command()
@commands.is_owner()
async def clear(ctx):
    await ctx.channel.purge(limit=sys.maxsize)


@bot.command()
@commands.is_owner()
async def reload(ctx, extension: str):
    try:
        if extension == 'help':
            files = 'BookRetrieval Event ForFun Saving Sql'.split()
            context = '\n'.join(['## 현재 Cogs 리스트'] + [f'> {cog}' for cog in files])
            await ctx.send(context)
        else:
            now = datetime.now()
            date = now.strftime("%y/%m/%d %H:%M")

            await bot.reload_extension(f'Cogs.{extension}')
            await ctx.send(f'{extension} Cog reloaded!')
            await bot.tree.sync()
            print(f'{extension} cog reloaded at {date}')
    except Exception as e:
        await ctx.send(f'err: {e}')


bot.run(token)
