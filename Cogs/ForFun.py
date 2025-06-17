# Import modules ===============================================
import random
import urllib.request  # for url

import discord
import requests  # for url also
from discord import app_commands
from discord.ext import commands

import embedding as e

# URL & lists =================================================
url = "https://img.freepik.com/premium-photo/discord-logo-icon-vector-illustration_895118-9640.jpg"
used_words = []


# Functions ===================================================
def get_next_word_from_api(last_letter):
    # TODO: Define words_api and api_url or get from environment
    # params = {
    #     "key": words_api,
    #     "q": last_letter,
    #     "req_type": "json",
    #     "advanced": "y",
    #     "method": "start",
    #     "type1": "word",
    #     "pos": [1, 2],
    #     "num": 100,
    # }

    # response = requests.get(api_url, params=params)
    return None  # Temporary return until API is configured

    if response.status_code != 200:
        return None

    data = response.json()

    if "channel" in data and "item" in data["channel"]:
        words = [
            item["word"].replace("-", "")
            for item in data["channel"]["item"]
            if item["word"] not in used_words and len(item["word"]) > 1
        ]
        return random.choice(words) if words else None

    return None


def has_final_consonant(char):
    code = ord(char) - 0xAC00
    final_consonant = code % 28
    return final_consonant != 0


def first_consonant_change(char):
    code = ord(char) - 0xAC00
    initial = code // 588  # 초성 추출
    medial = (code % 588) // 28  # 중성 추출
    final = code % 28  # 종성 추출

    medial_law_targets = {6, 9, 12, 13, 18, 20}  # 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅣ', 'ㅖ'

    if initial == 2 and medial in medial_law_targets:
        # 'ㄴ' -> 'ㅇ'
        initial = 11
    elif initial == 5:
        if medial in medial_law_targets:
            # 'ㄹ' -> 'ㅇ'
            initial = 11
        else:
            # 'ㄹ' -> 'ㄴ'
            initial = 2

    # 새 유니코드 값 계산
    new_code = initial * 588 + medial * 28 + final + 0xAC00
    return chr(new_code)


# TODO: Uncomment when openai is properly imported and configured
# async def get_gpt_response(prompt):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4",  # GPT-4 모델 사용
#             messages=[{"role": "user", "content": prompt}],
#         )
#         return response["choices"][0]["message"]["content"]
#     except Exception as e:
#         return f"에러 발생: {str(e)}"


# Class =======================================================
class ForFun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="커맨드를 알아보아요")
    async def help_command(self, interaction: discord.Interaction):
        if interaction.user.avatar is not None:
            avatar = interaction.user.avatar.url
        else:
            avatar = url

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

        embed = e.get_embed(context, title="이누이 봇의 커맨드를 알아보아요")
        embed.set_author(name=interaction.user.display_name, icon_url=avatar)
        await interaction.response.send_message(embed=embed)

    # > for fun
    @app_commands.command(name="하빵", description="인사를 해보아요")
    async def hi_bread(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"{member.mention} 하이빵가루 :bread:")

    @app_commands.command(name="튀김", description="히히튀김이다")
    @app_commands.describe(number="보낼 숫자")
    async def fry(self, interaction: discord.Interaction, number: int):
        if number > 100:
            await interaction.response.send_message(
                f"{interaction.user.mention} 숫자가 너무 커요 :sob:"
            )
            return
        elif number < -100:
            await interaction.response.send_message(
                f"{interaction.user.mention} 숫자가 너무 작아요 :sob:"
            )
            return

        fry = "튀김" * abs(number) + " 🍤"
        if number < 0:
            fry = fry[::-1]
        await interaction.response.send_message(fry)

    @app_commands.command(name="누구냐", description="바보가 되어 보아요")
    @app_commands.describe(member="보낼 멤버")
    async def who_ru(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(
            f"{member.mention} 넌 누구냐 !!!! :gun:"
        )

    @app_commands.command(name="떠올려", description="두근두근")
    async def dokidoki(self, interaction: discord.Interaction):
        urllib.request.urlretrieve("https://buly.kr/31RhHua", "dokidoki.png")
        image = discord.File("images/dokidoki.png", filename="dokidoki.png")

        embed = discord.Embed(
            title="두근거림을", description="떠올리는 거야!", color=0x4788B6
        )
        embed.set_image(url="attachment://dokidoki.png")

        await interaction.response.send_message(embed=embed, file=image)

    @app_commands.command(name="카구야", description="펑")
    async def houraisan_kaguya(self, interaction: discord.Interaction):
        urllib.request.urlretrieve(
            "https://media1.tenor.com/m/fV1krxBGQWAAAAAd/kaguya-houraisan-kaguya-houraisan-exploding.gif",
            "kaguya.gif",
        )
        image = discord.File("images/kaguya.gif", filename="kaguya.gif")

        embed = discord.Embed(title="", description="", color=0x4788B6)
        embed.set_image(url="attachment://kaguya.gif")

        await interaction.response.send_message(embed=embed, file=image)

    @app_commands.command(name="이누이", description="뇌절")
    @app_commands.describe(number="어디까지?")
    async def say_inui(self, interaction: discord.Interaction, number: int):
        if number > 100:
            await interaction.response.send_message(
                f"{interaction.user.mention} 숫자가 너무 커요 :sob:"
            )
            return
        elif number < 2:
            await interaction.response.send_message(
                f"{interaction.user.mention} 숫자가 너무 작아요 :sob:"
            )
            return

        num_to_kor = "일이삼사오육칠팔구"
        context = [interaction.user.mention]
        for i in range(2, number + 1):
            flag = ""
            if i == 100:
                flag = "백"
            elif (i // 10) > 1:
                flag = num_to_kor[(i // 10) - 1] + "십"
            elif i >= 10:
                flag = "십"

            num = num_to_kor[i % 10 - 1] if i % 10 != 0 else ""
            context.append(flag + num + "누" + flag + num)
        context.append("<a:InuiWaveYay:1272086403135832125>")

        await interaction.response.send_message(" ".join(context))

    @app_commands.command(name="에엥", description="갈고리 살인마")
    @app_commands.describe(num="보낼 개수")
    async def eng(self, interaction: discord.Interaction, num: int):
        if abs(num) > 1000:
            await interaction.response.send_message(
                f"{interaction.user.mention} 범위를 넘어갔어요! :sob:"
            )
            return

        if num == 0:
            await interaction.response.send_message("!")
        elif num < 0:
            await interaction.response.send_message("¿" * abs(num))
        else:
            await interaction.response.send_message("?" * num)

    @app_commands.command(name="어쩔티비", description="시비를 걸어요")
    @app_commands.describe(member="보낼 멤버")
    async def assertive(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(
            f"{member.mention} 저쩔냉장고 <a:InuiWaveYay:1272086403135832125>"
        )

    @app_commands.command(name="포메", description="빡친 포메는 기엽습니다")
    async def pome(self, interaction: discord.Interaction):
        urls = [
            "https://postfiles.pstatic.net/MjAyNDA5MTlfODYg/MDAxNzI2Njc3MTY2NDQy.29hM_mlUx0M9lfEu9Zj6nX6gwtIZn3AUk8mF_F7cDAwg.LYIzM6sXVRO2ppqI2NdyTqqN2jadX21teRYI-ZtmwCIg.JPEG/2.jpg?type=w3840",
            "https://postfiles.pstatic.net/MjAyNDA5MTlfMTUy/MDAxNzI2Njc3MTY2NDQy.hb8jqlWJHZYMIWdlWO2s0h5CRjG710DPa2wQ1afFTUUg.zknjU_GJ1IKDaHtu8PZ3MISoTP3uZTS5sdr90kE1lfsg.JPEG/3.jpg?type=w3840",
            "https://postfiles.pstatic.net/MjAyNDA5MTlfMjk3/MDAxNzI2Njc3MTY2NDQy.W1yDrdwaP6WNQRQtQFJDMpJxDGh13sfHDngQlLPYkxsg.GLV4dn1_J9JwAOAmSxp-4M6NoUbXROG3G3UPE8VnyF4g.JPEG/1.jpg?type=w3840",
            "https://postfiles.pstatic.net/MjAyNDA5MTlfMjI3/MDAxNzI2Njc3MTY2NDY3.dK_2NJAku_6ZWP2iOH7Y4bAgtUizgy_Xqh0LzKUC61Ig.gb2t4IhJZgNVZMpaNMDSy4-rTTNXcMaIWWFHYCEa7w8g.JPEG/0.jpg?type=w3840",
            "https://postfiles.pstatic.net/MjAyNDA5MjFfMTU1/MDAxNzI2OTA3MjkzMTYy.GZIbs6qd73oXXM0iYBF7JQDwS96kUTzJblW6GBdmRhEg.ZX_yniLCpBLATokatCqtsTjEO0gm0ydffL9OEMoxVvIg.JPEG/4.jpg?type=w3840",
            "https://postfiles.pstatic.net/MjAyNDA5MjFfMjI5/MDAxNzI2OTA3MjkzMTYy.WdEoaHEfMDcdVfeEUs_V8Z9a1WZC3ESra1MksDlZcCIg.rdSaho_zHlQMx6kNmC-sQhjuY2s6fRX9V-zDTJuCkyUg.JPEG/5.jpg?type=w3840",
            "https://postfiles.pstatic.net/MjAyNDA5MjFfMjIy/MDAxNzI2OTA3MjkzMTY0.PjznS4W3dBo7u_dVgqLif_1ayhw2HJyyhXE27S4N2dQg.PCvFyyjjyMcIONOu1JcKpLpQAjE-B1JCsW9K8UdOvkQg.JPEG/6.jpg?type=w3840",
        ]
        urllib.request.urlretrieve(random.choice(urls), "pome.png")
        image = discord.File("images/pome.png", filename="pome.png")

        embed = discord.Embed(color=0x4788B6)
        embed.set_image(url="attachment://pome.png")

        await interaction.response.send_message(embed=embed, file=image)

    @app_commands.command(name="아오", description="아오;;;")
    @app_commands.describe(member="보낼 멤버")
    async def aoh(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(
            f"{member.mention} 아오~ 아카~ 무라사키~ <a:InuiWaveYay:1272086403135832125>"
        )

    @app_commands.command(name="gpt", description="gpt4o")
    @app_commands.describe(prompt="v. 유발하다")
    async def gpt(self, interaction: discord.Interaction, prompt: str):
        if not prompt:
            await interaction.response.send_message("프롬프트를 입력해주세요!")
            return

        await interaction.response.send_message("답변 생성 중...")
        response = await get_gpt_response(prompt)
        await interaction.followup.send(response)

    @app_commands.command(name="끝말잇기", description="듐바륨")
    async def shiritori(self, interaction: discord.Interaction, word: str):
        global used_words

        if word.lower() == "q":
            used_words.clear()
            await interaction.response.send_message(
                "초기화됐습니다! 먼저 시작하세여 <a:InuiWaveYay:1272086403135832125>"
            )
            return
        elif word in used_words:
            tag1 = "은" if has_final_consonant(word[0]) else "는"
            await interaction.response.send_message(
                f"'{word}'{tag1} 이미 쓴 단어라구요 <a:InuiWaveYay:1272086403135832125>"
            )
            return
        elif len(used_words) > 0 and used_words[-1][-1] != word[0]:
            tag1 = "이" if has_final_consonant(word[0]) else "가"
            tag2 = "으로" if has_final_consonant(used_words[-1][-1]) else "로"
            await interaction.response.send_message(
                f"'{word[0]}'{tag1} 아니라 {used_words[-1][-1]}{tag2} 끝냈거든요 !"
            )
            return
        elif len(word) == 1:
            await interaction.response.send_message(
                f"'{word}'는 한글자거든요 <a:InuiWaveYay:1272086403135832125>"
            )
            return

        used_words.append(word)
        last_letter = word[-1]
        next_word = get_next_word_from_api(last_letter)

        if next_word:
            used_words.append(next_word)
            await interaction.response.send_message(f"{word} -> {next_word}!")
        else:
            await interaction.response.send_message(f"{last_letter}... 너무해!!")
            used_words.clear()


async def setup(bot: commands.Bot):
    await bot.add_cog(ForFun(bot))
