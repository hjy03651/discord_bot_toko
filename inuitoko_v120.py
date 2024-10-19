# Import modules ===============================================
import discord
import sys
import time
import asyncio
import urllib.request
import random
import embeding as e

from datetime import datetime
from discord import app_commands
from discord.ext import commands
from dbtool_book import ManageBook
from dbtool_events import ManageEvents
from PIL import Image


# Intents (for bot) ===========================================
intents = discord.Intents.default()
intents.message_content = True  # 메세지 읽기/보내기 권한
intents.voice_states = True  # 음성채팅 감지 권한
intents.guilds = True  # 서버 연결 권한
intents.members = True  # 멤버 열람 권한

bot = commands.Bot(command_prefix='!!', intents=intents)


# Class =======================================================
book = ManageBook()
event = ManageEvents()


# Events ======================================================
@bot.event
async def on_ready():
    """
    to log in to server.
    :return: None
    """
    print(f'Logged in as {bot.user}')
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands.")


@bot.event
async def on_voice_state_update(member, before, after):
    """
    to give or delete role from a member who were in voice chat.
    :param member: get member list
    :param before: get before channel
    :param after: get after channel
    :return: None
    """
    role_name = "temp"
    guild = member.guild

    # find role from server
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        role = await guild.create_role(name=role_name)

    # enter
    if after.channel is not None and before.channel is None:
        await member.add_roles(role)
        print(f"Assigned role '{role_name}' to {member.display_name}")

    # exit
    elif before.channel is not None and after.channel is None:
        await bot.get_command('clear')(before)
        await member.remove_roles(role)
        print(f"Removed role '{role_name}' from {member.display_name}")


@bot.event
async def on_message(msg):
    """
    to send a message.
    :param msg: message
    :return: None
    """
    if msg.author.bot:
        return None

    if msg.channel.id == 1279810905009426474:
        # 기증-승인채널
        recent_messages[msg.channel.id] = msg

    await bot.process_commands(msg)


# Bot Command =================================================
@bot.tree.command(name="help", description="커맨드를 알아보아요")
async def help_command(interaction: discord.Interaction):
    context = "__<대출 관련>__\n"
    context += "`/목록 <키워드>`: 도서를 검색합니다.\n"
    context += "`/목록 <도서명> <권수>`: 특정 권수의 도서를 검색합니다. 도서는 제목이 일치해야 합니다.\n"
    context += "`/대출 <도서아이디>`: 원하는 도서를 대출합니다.\n"
    context += "`/반납 <도서아이디>`: 대출한 도서를 반납합니다.\n"
    context += "`/대출목록`: 본인이 대출한 도서 목록을 출력합니다.\n"

    context += "\n"
    context += "__<기타>__\n"
    context += "`/하빵 <닉네임>`: 하이빵가루!\n"
    context += "`/이누이 <숫자>`: 실행해보시면 압니다. 숫자는 2~10 사이의 자연수!\n"
    context += "`/떠올려`: 두근거림을 떠올리는 거야!\n"
    context += "`/어쩔티비 <닉네임>`: 어쩔티비~ 저쩔냉장고~\n"
    context += "`/아오 <닉네임>`: 화를 내요\n"
    context += "`/포메`: 화난 포메를 출력합니다.\n"

    embed = e.get_embed(context, title='이누이 봇의 커맨드를 알아보아요')
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
    await interaction.response.send_message(embed=embed)


# > for fun
@bot.tree.command(name="하빵", description="인사를 해보아요")
@app_commands.describe(member='보낼 멤버')
async def hi_bread(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"{member.mention} 하이빵가루 :bread:")


@bot.command()
async def 이누이(ctx, text=None):
    if text is None:
        await ctx.channel.send(f'{ctx.author.mention} 이누이 기여워 <a:InuiWaveYay:1272086403135832125>')
    elif text == "과제해줘":
        await ctx.channel.send(f'{ctx.author.mention} 챗GPT쨩이 더 똑똑해요 <a:InuiWaveYay:1272086403135832125>')
    elif text == "삼누삼":
        await ctx.channel.send(f'{ctx.author.mention} 사누사 오누오 <a:InuiWaveYay:1272086403135832125>')
    elif text == "삼오라버니":
        await ctx.channel.send(f'{ctx.author.mention} 건좀 <a:InuiWaveYay:1272086403135832125>')
    elif text == "생일":
        await ctx.channel.send(f'{ctx.author.mention} 9월 9일 <a:InuiWaveYay:1272086403135832125>')


@bot.tree.command(name="떠올려", description="두근두근")
async def dokidoki(interaction: discord.Interaction):
    urllib.request.urlretrieve("https://buly.kr/31RhHua", "dokidoki.png")
    image = discord.File("dokidoki.png", filename="dokidoki.png")

    embed = discord.Embed(title="두근거림을", description="떠올리는 거야!", color=0x4788b6)
    embed.set_image(url="attachment://dokidoki.png")

    await interaction.response.send_message(embed=embed, file=image)


@bot.tree.command(name="이누이", description="뇌절")
@app_commands.describe(number="어디까지?")
async def say_inui(interaction: discord.Interaction, number: int):
    if number > 100:
        await interaction.response.send_message(f"{interaction.user.mention} 숫자가 너무 커요 :sob:")
        return
    elif number < 2:
        await interaction.response.send_message(f"{interaction.user.mention} 숫자가 너무 작아요 :sob:")
        return

    num_to_kor = '일이삼사오육칠팔구'
    context = [interaction.user.mention]
    for i in range(2, number + 1):
        flag = ''
        if i == 100:
            flag = '백'
        elif (i // 10) > 1:
            flag = num_to_kor[(i // 10) - 1] + '십'
        elif i >= 10:
            flag = '십'

        num = num_to_kor[i % 10 - 1] if i % 10 != 0 else ''
        context.append(flag + num + '누' + flag + num)
    context.append('<a:InuiWaveYay:1272086403135832125>')

    await interaction.response.send_message(' '.join(context))


@bot.tree.command(name="어쩔티비", description="시비를 걸어요")
@app_commands.describe(member='보낼 멤버')
async def assertive(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"{member.mention} 저쩔냉장고 <a:InuiWaveYay:1272086403135832125>")


@bot.tree.command(name="포메", description="빡친 포메는 기엽습니다")
async def pome(interaction: discord.Interaction):
    urls = ['https://buly.kr/9iEWuT2', 'https://buly.kr/FWRXHOa', 'https://buly.kr/HHb75YY', 'https://buly.kr/HSVs4NL',
            'https://buly.kr/4QloRrJ', 'https://buly.kr/6Mq9EqV', 'https://buly.kr/DPSSTTt']
    urllib.request.urlretrieve(random.choice(urls), "pome.png")
    image = discord.File("pome.png", filename="pome.png")

    embed = discord.Embed(color=0x4788b6)
    embed.set_image(url="attachment://pome.png")

    await interaction.response.send_message(embed=embed, file=image)


@bot.tree.command(name="아오", description="아오;;;")
@app_commands.describe(member='보낼 멤버')
async def aoh(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f'{member.mention} 아오~ 아카~ 무라사키~ <a:InuiWaveYay:1272086403135832125>')


@bot.command()
async def clear(ctx):
    await ctx.channel.purge(limit=sys.maxsize)


# > for books
@bot.tree.command(name="목록", description="도서 리스트를 표시합니다")
@app_commands.describe(title="도서명", series="권 수")
async def search_books(interaction: discord.Interaction, title: str, series: str = None):
    if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
        embed = e.get_embed(':warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!', True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return
    if title.lower() == 'none':
        embed = e.get_embed(':warning: 검색이 불가능한 검색어입니다!', True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    hits = book.read_book_data(title, series)

    if hits and series is None:
        context = ">>> "
        count = 1
        for books in hits:
            if count == 16:
                break

            db_loc, db_name, db_num, db_rent = books
            book_id = book.find_book_id(db_name, db_num)
            if db_rent:
                rentable = '대출 가능'
            else:
                rentable = '대출 불가'
            context += f'[{book_id}] {db_name} {db_num}권 : {db_loc} ({rentable})\n'
            count += 1

        embed = e.get_embed(context, title=f'{title}에 대한 상위 15개 검색 결과입니다.')
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=embed)

    elif hits and series is not None:
        context = ">>> "
        for books in hits:
            db_loc, db_name, db_num, db_rent = books
            book_id = book.find_book_id(db_name, db_num)
            if db_rent:
                rentable = '대출 가능'
            else:
                rentable = '대출 불가'
            context += f'[{book_id}] {db_name} {db_num}권 - {db_loc} ({rentable})\n'

        embed = e.get_embed(context, title=f'{title} {series}에 대한 검색 결과입니다.')
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    elif title is not None and not hits:
        embed = e.get_embed('검색 결과가 없습니다 :sob:', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)


@bot.tree.command(name="대출", description="도서를 대출합니다")
@app_commands.describe(book_id="도서 아이디")
async def rent_book(interaction: discord.Interaction, book_id: str):
    if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
        embed = e.get_embed(':warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    try:
        rentable = book.find_book_rentable(book_id)
        if rentable:
            student_name = interaction.user.display_name[3:]
            book.rent_book(student_name, book_id)

            title, series = book.get_info_by_id(book_id)[0]
            if float(series).is_integer():
                series = int(series)
            else:
                series = round(float(series), 1)

            embed = e.get_embed(f'[{book_id}] {title} {series}권을 대출하였습니다.', title='성공적으로 대출되었습니다!')
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = e.get_embed('현재 대출이 불가능한 도서입니다 :sob:', error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
    except ValueError:
        embed = e.get_embed('도서 아이디가 잘못됐습니다 :sob:', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
    except IndexError:
        embed = e.get_embed('도서 아이디가 잘못됐습니다 :sob:', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)


@bot.tree.command(name="대출목록", description="자신의 대출 현황을 출력합니다")
async def get_rent_list(interaction: discord.Interaction):
    if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
        embed = e.get_embed(':warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    name = interaction.user.display_name[3:]
    rent_list = book.get_rent_list(name)

    if not rent_list:
        embed = e.get_embed('대출 중인 도서가 없습니다!', title=f'{interaction.user.display_name} 님의 대출 목록입니다.')
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    context = ">>> "
    for rent_info in rent_list:
        book_id = rent_info[1]
        title, series = book.get_info_by_id(book_id)[0]
        if float(series).is_integer():
            series = int(series)
        else:
            series = round(float(series), 1)

        context += f"[{book_id}] {title} {series}권\n"

    embed = e.get_embed(context, title=f'{interaction.user.display_name} 님의 대출 목록입니다.')
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="rent", description="rent a book")
@app_commands.describe(name='name', book_id="id")
async def rent_book_outer(interaction: discord.Interaction, name: discord.Member, book_id: str):
    try:
        if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
            embed = e.get_embed(':warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!', error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            return

        role = discord.utils.get(interaction.user.roles, id=1181080308590858361)
        if role is None:
            embed = e.get_embed(':warning: 명령어 사용 권한이 없습니다.', error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            return

        if name is None:
            embed = e.get_embed(f'{name}이라는 멤버는 존재하지 않습니다 :sob:', error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            return

        rentable = book.find_book_rentable(book_id)
        if rentable:
            book.rent_book(name.display_name[3:], book_id)

            title, series = book.get_info_by_id(book_id)[0]
            if float(series).is_integer():
                series = int(series)
            else:
                series = round(float(series), 1)

            embed = e.get_embed(f'[{book_id}] {title} {series}권을 대출하였습니다.', title='성공적으로 대출되었습니다!')
            embed.set_author(name=name.display_name, icon_url=name.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = e.get_embed('현재 대출이 불가능한 도서입니다 :sob:', error=True)
            embed.set_author(name=name.display_name, icon_url=name.display_avatar.url)
            await interaction.response.send_message(embed=embed)
    except ValueError:
        embed = e.get_embed('도서 아이디가 잘못됐습니다 :sob:', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)


@bot.tree.command(name="반납", description="도서를 반납합니다")
@app_commands.describe(book_id="도서 아이디")
async def return_book(interaction: discord.Interaction, book_id: str):
    if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
        embed = e.get_embed(':warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    try:
        rentable = book.find_book_rentable(book_id)
        if not rentable:
            student_num = interaction.user.display_name[3:]
            book.rent_book(student_num, book_id, True)

            title, series = book.get_info_by_id(book_id)[0]
            if float(series).is_integer():
                series = int(series)
            else:
                series = round(float(series), 1)

            embed = e.get_embed(f'[{book_id}] {title} {series}권을 반납하였습니다.', title='성공적으로 반납되었습니다!')
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = e.get_embed('대출 처리가 되지 않은 도서입니다 :sob:', error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
    except ValueError:
        embed = e.get_embed('도서 아이디가 잘못됐습니다 :sob:', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
    except IndexError:
        embed = e.get_embed('도서 아이디가 잘못됐습니다 :sob:', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)


@bot.tree.command(name="추가", description="도서를 추가합니다")
@app_commands.describe(title="도서명", series="권 수", byname1="별칭1", byname2="별칭2",
                       location="책장 번호", category="도서 분류", language="언어")
async def add_book(interaction: discord.Interaction, title: str, series: str,
                   location: str, category: str, language: str, byname1: str = None, byname2: str = None):
    if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
        embed = e.get_embed(':warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    role = discord.utils.get(interaction.user.roles, id=1181080308590858361)
    if role is None:
        embed = e.get_embed(f':warning: 명령어 사용 권한이 없습니다.', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    if len(title) > 100:
        embed = e.get_embed(':warning: 도서명이 너무 깁니다!', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    elif len(location) > 4 or '-' not in location:
        embed = e.get_embed(':warning: 책장 번호를 다시 확인해주세요.', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    elif len(category) > 5 or category not in ['만화', '소설', '작법서', '일러북', '잡지']:
        embed = e.get_embed(':warning: 도서 분류가 잘못됐습니다.', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        embed.set_footer(text="가능한 도서 분류는 '만화', '소설', '작법서', '일러북', '잡지' 입니다.")
        await interaction.response.send_message(embed=embed)
        return

    elif len(language) > 3 or language not in ['kor', 'eng', 'jpn', 'chn']:
        embed = e.get_embed(':warning: 도서 언어가 잘못됐습니다.', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        embed.set_footer(text="가능한 언어는 'kor', 'eng', 'jpn', 'chn' 입니다.")
        await interaction.response.send_message(embed=embed)
        return

    elif book.is_there_same_book(title, series, category, language):
        embed = e.get_embed(':warning: 이미 있는 도서입니다.', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    else:
        try:
            if float(series).is_integer():
                series = int(series)
            else:
                series = round(float(series), 1)
        except ValueError:
            embed = e.get_embed(':warning: 도서 권 수가 잘못됐습니다!', error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            return
        else:
            if series > 99:
                embed = e.get_embed(':warning: 도서 권 수가 잘못됐습니다!', error=True)
                embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)
                return

            book.insert_book_data(title, series, byname1, byname2, location, category, language)
            book_id = book.find_book_id(title, series)
            embed = e.get_embed(f'[{book_id}] {title} {series}권 ({location}) 추가 완료!',
                                title='성공적으로 추가되었습니다!')
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)


@bot.tree.command(name="삭제", description="도서를 삭제합니다")
@app_commands.describe(book_id="도서 아이디")
async def delete_book(interaction: discord.Interaction, book_id: str):
    role = discord.utils.get(interaction.user.roles, id=1181080308590858361)
    if role is None:
        embed = e.get_embed(':warning: 명령어 사용 권한이 없습니다.', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
        embed = e.get_embed(':warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    try:
        if book.get_info_by_id(book_id):
            book.delete_book_data(book_id)
            embed = e.get_embed(f'도서 {book_id}를 삭제하였습니다.', title='성공적으로 삭제되었습니다!')
            embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = e.get_embed('도서 아이디가 잘못됐습니다 :sob:', error=True)
            embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            await interaction.response.send_message(embed=embed)

    except ValueError:
        embed = e.get_embed('도서 아이디가 잘못됐습니다 :sob:', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)


@bot.tree.command(name="수정", description="도서 정보를 수정합니다")
@app_commands.describe(book_id="도서 아이디", change='수정할 부분', to='수정된 데이터')
async def change_book(interaction: discord.Interaction, book_id: str, change: str, to: str):
    role = discord.utils.get(interaction.user.roles, id=1181080308590858361)
    if role is None:
        embed = e.get_embed(':warning: 명령어 사용 권한이 없습니다.', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
        embed = e.get_embed(':warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    if not book.get_info_by_id(book_id):
        embed = e.get_embed(':warning: 도서 아이디가 틀렸습니다.', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    elif change not in ['byname1', 'byname2', 'location', 'category', 'language']:
        embed = e.get_embed(':warning: 수정하고자 하는 카테고리가 틀렸습니다.', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        embed.set_footer(text="가능한 카테고리는 byname1, byname2, location, category, language입니다.")
        await interaction.response.send_message(embed=embed)
        return

    # to는 너무 복잡해서 다음 업데이트에 추가
    else:
        try:
            book.update_book_data(change, to, book_id)
            embed = e.get_embed(f'[{book_id}]의 {change}가 {to}로 변경되었습니다.', title='성공적으로 추가되었습니다!')
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)

        except IndexError:
            embed = e.get_embed(':warning: 알 수 없는 오류가 발생했습니다 :sob:', error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)


# 기증 관련
@bot.tree.command(name="보관", description="물품을 보관합니다")
@app_commands.describe(name="물품 보관자", goods="굿즈 종류")
async def keep_goods(interaction: discord.Interaction, name: str, goods: str):
    if interaction.channel_id not in (1279810905009426474, 1272086876638937130):
        embed = e.get_embed(':warning: 이 커맨드는 특정 채널에서만 사용 가능합니다!', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    else:
        now = datetime.now()
        formatted_date = now.strftime("%y/%m/%d %H:%M")

        guild = interaction.guild
        member = discord.utils.find(lambda m: m.name == name or m.display_name == name, guild.members)

        if member is None:
            embed = e.get_embed(f'{name}이라는 멤버는 존재하지 않습니다 :sob:', error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            return

        context = f">>> {member.mention}님의 물품을 {formatted_date}에 정상적으로 보관처리 했습니다!\n"
        context += f"짐이 철수되지 않았을 경우, 6일 후에 DM을 보내드리겠습니다."
        embed = e.get_embed(context, title='짐 보관이 시작되었습니다.')
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        await interaction.response.send_message(embed=embed)

        book.store_goods(member.display_name, goods, formatted_date)

        await asyncio.sleep(6 * 24 * 60 * 60)
        if book.get_storage(name) is not None:
            await member.send(f"> {member.mention}님의 물품 보관 시간이 1일 남았습니다.")


"""@bot.command()
async def get_id(ctx, *, username: str):
    # 서버의 모든 멤버를 검색
    member = await discord.utils.find(lambda m: m.display_name == username, ctx.guild.fetch_members(limit=None))

    if member:
        return member
    else:
        await ctx.send("이름이 잘못되었습니다.")"""


@bot.tree.command(name="회수", description="물품을 회수합니다")
@app_commands.describe(name="물품 보관자")
async def return_goods(interaction: discord.Interaction, name: str):
    role = discord.utils.get(interaction.user.roles, id=1181080308590858361)
    if role is None:
        embed = e.get_embed(':warning: 명령어 사용 권한이 없습니다.', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    if interaction.channel_id not in (1279810905009426474, 1272086876638937130):
        embed = e.get_embed(f'이 커맨드는 특정 채널에서만 사용 가능합니다!', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        return

    now = datetime.now()
    formatted_date = now.strftime("%y/%m/%d %H:%M")

    guild = interaction.guild
    member = discord.utils.find(lambda m: m.name == name or m.display_name == name, guild.members)

    context = f">>> {member.mention}님의 물품이 {formatted_date}에 보관 리스트에서 정상적으로 삭제됐습니다!\n"
    embed = e.get_embed(context, title='짐 보관이 종료되었습니다.')
    embed.set_author(name=member.display_name, icon_url=member.avatar.url)
    await interaction.response.send_message(embed=embed)

    book.move_out_goods(name)


# for events ======================================================================================
@bot.tree.command(name="event", description="이벤트 참여자를 집계합니다")
@app_commands.describe(title="이벤트명", number="당첨자 수")
async def finish_event(interaction: discord.Interaction, title: str, number: int):
    role = discord.utils.get(interaction.user.roles, id=1181080308590858361)
    if role is None:
        embed = e.get_embed(':warning: 명령어 사용 권한이 없습니다.', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
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
                    image_count[display_name] *= 1.2
                else:
                    image_count[display_name] = 1

        # 결과 출력
    if image_count:
        for name, count in image_count.items():
            event.new_participation(title, name, count)

        winners = event.get_random(title, number)

        ctx = ''
        for win in winners:
            ctx += f'{win}\n'

        embed = e.get_embed(ctx, title='이벤트 당첨 축하드립니다!')
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    else:
        embed = e.get_embed(':warning: 이벤트 참여자가 없습니다.', error=True)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)


token = 'shrouded by the op'
bot.run(token)
