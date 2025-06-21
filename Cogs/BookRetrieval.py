# Import modules ===============================================
import discord
import embedding as e

from discord import app_commands
from discord.ext import commands
from DBtoolBook import ManageBook


# URL & lists =================================================
book = ManageBook()
url = "https://img.freepik.com/premium-photo/discord-logo-icon-vector-illustration_895118-9640.jpg"
category_list = [
    app_commands.Choice(name="만화", value="만화"),
    app_commands.Choice(name="소설", value="소설"),
    app_commands.Choice(name="작법서", value="작법서"),
    app_commands.Choice(name="일러북", value="일러북"),
    app_commands.Choice(name="설정집", value="설정집"),
    app_commands.Choice(name="잡지", value="잡지"),
    app_commands.Choice(name="악보", value="악보"),
]
language_list = [
    app_commands.Choice(name="한국어", value="kor"),
    app_commands.Choice(name="일본어", value="jpn"),
    app_commands.Choice(name="영어", value="eng"),
    app_commands.Choice(name="중국어", value="chn"),
    app_commands.Choice(name="기타", value="etc"),
]
change_list = [
    app_commands.Choice(name="도서명", value="title"),
    app_commands.Choice(name="별명1", value="byname1"),
    app_commands.Choice(name="별명2", value="byname2"),
    app_commands.Choice(name="위치", value="location"),
    app_commands.Choice(name="카테고리", value="category"),
    app_commands.Choice(name="언어", value="language"),
]


# Class =======================================================
class Paginator(discord.ui.View):
    def __init__(self, embeds: list[discord.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.current = 0

        self.previous_button: discord.ui.Button = self.children[0]  # « 이전
        self.next_button: discord.ui.Button = self.children[1]  # 다음 »

        self._update_button_states()

    def _update_button_states(self):
        # 첫 페이지면 이전 비활성화, 마지막 페이지면 다음 비활성화
        self.previous_button.disabled = self.current == 0
        self.next_button.disabled = self.current == len(self.embeds) - 1

    @discord.ui.button(label="« 이전", style=discord.ButtonStyle.grey)
    async def previous(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.current > 0:
            self.current -= 1
            self._update_button_states()
            await interaction.response.edit_message(
                embed=self.embeds[self.current], view=self
            )
        else:
            button.disabled = True

    @discord.ui.button(label="다음 »", style=discord.ButtonStyle.grey)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current < len(self.embeds) - 1:
            self.current += 1
            self._update_button_states()
            await interaction.response.edit_message(
                embed=self.embeds[self.current], view=self
            )


class BookRetrieval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="목록", description="도서 리스트를 표시합니다")
    @app_commands.describe(title="도서명", series="권 수")
    async def search_books(
        self, interaction: discord.Interaction, title: str, series: str = None
    ):
        # Exception
        if interaction.user.avatar is not None:
            avatar = interaction.user.avatar.url
        else:
            avatar = url

        if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
            embed = e.get_embed(
                ":warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!", True
            )
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return
        if title.lower() in ("none", "test", "temp"):
            embed = e.get_embed(":warning: 검색이 불가능한 검색어입니다!", True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        # Retrieval
        hits = book.read_book_data(title, series)

        if hits and series is None:
            results = []
            for books in hits:
                db_id, db_loc, db_name, db_num, db_rent = books
                # book_id = book.find_book_id(db_name, db_num)
                if db_rent:
                    rentable = "대출 가능"
                else:
                    rentable = "대출 불가"
                results.append([db_id, db_name.strip(), db_num, db_loc, rentable])

            embeds = e.pagination(title, results)

            view = Paginator(embeds)
            await interaction.response.send_message(embed=embeds[0], view=view)

        elif title is not None and not hits:
            embed = e.get_embed("검색 결과가 없습니다 :sob:", error=True)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="책장", description="특정 책장의 도서를 검색합니다")
    @app_commands.describe(bookshelf="책장명")
    async def search_bookshelf(self, interaction: discord.Interaction, bookshelf: str):
        # Exception
        if interaction.user.avatar is not None:
            avatar = interaction.user.avatar.url
        else:
            avatar = url

        if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
            embed = e.get_embed(
                ":warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!", True
            )
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return
        if len(bookshelf) not in (3, 4) or "-" not in bookshelf:
            embed = e.get_embed(":warning: 책장명의 형식의 다릅니다!", True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        # Retrieval
        hits = book.get_location(bookshelf)

        if hits:
            results = []
            for books in hits:
                db_id, db_loc, db_name, db_num, db_rent = books
                if db_rent:
                    rentable = "대출 가능"
                else:
                    rentable = "대출 불가"
                results.append([db_id, db_name.strip(), db_num, db_loc, rentable])

            embeds = e.pagination(bookshelf, results)

            view = Paginator(embeds)
            await interaction.response.send_message(embed=embeds[0], view=view)

        elif bookshelf is not None and not hits:
            embed = e.get_embed("검색 결과가 없습니다 :sob:", error=True)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="대출", description="도서를 대출합니다")
    @app_commands.describe(book_id="도서 아이디")
    async def rent_book(self, interaction: discord.Interaction, book_id: str):
        # Exception
        if interaction.user.avatar is not None:
            avatar = interaction.user.avatar.url
        else:
            avatar = url

        if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
            embed = e.get_embed(
                ":warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!", error=True
            )
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        # Rent
        try:
            rentable = book.find_book_rentable(book_id)
            if rentable:
                student_name = interaction.user.display_name[3:6]
                book.rent_book(student_name, book_id)

                title, series = book.get_info_by_id(book_id)[0]
                if float(series).is_integer():
                    series = int(series)
                else:
                    series = round(float(series), 1)

                embed = e.get_embed(
                    f"[{book_id}] {title} {series}권을 대출하였습니다.",
                    title="성공적으로 대출되었습니다!",
                )
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)
            else:
                embed = e.get_embed("현재 대출이 불가능한 도서입니다 :sob:", error=True)
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)
        except ValueError:
            embed = e.get_embed("도서 아이디가 잘못됐습니다 :sob:", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
        except IndexError:
            embed = e.get_embed("도서 아이디가 잘못됐습니다 :sob:", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="대출목록", description="자신의 대출 현황을 출력합니다")
    async def get_rent_list(self, interaction: discord.Interaction):
        # Exception
        if interaction.user.avatar is not None:
            avatar = interaction.user.avatar.url
        else:
            avatar = url

        if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
            embed = e.get_embed(
                ":warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!", error=True
            )
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        # Retrieval
        name = interaction.user.display_name[3:6]
        rent_list = book.get_rent_list(name)

        if not rent_list:
            embed = e.get_embed(
                "대출 중인 도서가 없습니다!",
                title=f"{interaction.user.display_name} 님의 대출 목록입니다.",
            )
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
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

        embed = e.get_embed(
            context, title=f"{interaction.user.display_name} 님의 대출 목록입니다."
        )
        embed.set_author(name=interaction.user.display_name, icon_url=avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rent", description="대신 대출을 해줍니다")
    @app_commands.describe(name="name", book_id="id")
    async def rent_book_outer(
        self, interaction: discord.Interaction, name: discord.Member, book_id: str
    ):
        try:
            if interaction.user.avatar is not None:
                avatar = interaction.user.avatar.url
            else:
                avatar = url
                
            if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
                embed = e.get_embed(
                    ":warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!",
                    error=True,
                )
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)
                return

            role = discord.utils.get(interaction.user.roles, id=1181080308590858361)
            if role is None:
                embed = e.get_embed(
                    ":warning: 명령어 사용 권한이 없습니다.", error=True
                )
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)
                return

            if name is None:
                embed = e.get_embed(
                    f"{name}이라는 멤버는 존재하지 않습니다 :sob:", error=True
                )
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)
                return

            rentable = book.find_book_rentable(book_id)
            if rentable:
                book.rent_book(name.display_name[3:6], book_id)

                title, series = book.get_info_by_id(book_id)[0]
                if float(series).is_integer():
                    series = int(series)
                else:
                    series = round(float(series), 1)

                embed = e.get_embed(
                    f"[{book_id}] {title} {series}권을 대출하였습니다.",
                    title="성공적으로 대출되었습니다!",
                )
                embed.set_author(
                    name=name.display_name, icon_url=name.display_avatar.url
                )
                await interaction.response.send_message(embed=embed)
            else:
                embed = e.get_embed("현재 대출이 불가능한 도서입니다 :sob:", error=True)
                embed.set_author(
                    name=name.display_name, icon_url=name.display_avatar.url
                )
                await interaction.response.send_message(embed=embed)
        except ValueError:
            embed = e.get_embed("도서 아이디가 잘못됐습니다 :sob:", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="반납", description="도서를 반납합니다")
    @app_commands.describe(book_id="도서 아이디")
    async def return_book(self, interaction: discord.Interaction, book_id: str):
        # Exception
        if interaction.user.avatar is not None:
            avatar = interaction.user.avatar.url
        else:
            avatar = url

        if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
            embed = e.get_embed(
                ":warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!", error=True
            )
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        # Return
        try:
            rentable = book.find_book_rentable(book_id)
            if not rentable:
                student_num = interaction.user.display_name[3:6]
                book.rent_book(student_num, book_id, True)

                title, series = book.get_info_by_id(book_id)[0]
                if float(series).is_integer():
                    series = int(series)
                else:
                    series = round(float(series), 1)

                embed = e.get_embed(
                    f"[{book_id}] {title} {series}권을 반납하였습니다.",
                    title="성공적으로 반납되었습니다!",
                )
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)
            else:
                embed = e.get_embed(
                    "대출 처리가 되지 않은 도서입니다 :sob:", error=True
                )
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)
        except ValueError:
            embed = e.get_embed("도서 아이디가 잘못됐습니다 :sob:", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
        except IndexError:
            embed = e.get_embed("도서 아이디가 잘못됐습니다 :sob:", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="추가", description="도서를 추가합니다")
    @app_commands.describe(
        title="도서명",
        series="권 수",
        byname1="별칭1",
        byname2="별칭2",
        location="책장 번호",
        category="도서 분류",
        language="언어",
    )
    @app_commands.choices(category=category_list, language=language_list)
    async def add_book(
        self,
        interaction: discord.Interaction,
        title: str,
        series: str,
        location: str,
        category: app_commands.Choice[str],
        language: app_commands.Choice[str],
        byname1: str = None,
        byname2: str = None,
    ):
        # Exception
        if interaction.user.avatar is not None:
            avatar = interaction.user.avatar.url
        else:
            avatar = url

        if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
            embed = e.get_embed(
                ":warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!", error=True
            )
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        role = discord.utils.get(interaction.user.roles, id=1181080308590858361)
        if role is None:
            embed = e.get_embed(":warning: 명령어 사용 권한이 없습니다.", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        if len(title) > 100:
            embed = e.get_embed(":warning: 도서명이 너무 깁니다!", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        elif len(location) > 5 or "-" not in location:
            embed = e.get_embed(":warning: 책장 번호를 다시 확인해주세요.", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        elif book.is_there_same_book(title, series, category.value, language.value):
            embed = e.get_embed(":warning: 이미 있는 도서입니다.", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        else:
            # Creating
            try:
                if float(series).is_integer():
                    series = int(series)
                else:
                    series = round(float(series), 1)
            except ValueError:
                embed = e.get_embed(":warning: 도서 권 수가 잘못됐습니다!", error=True)
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)
                return
            else:
                if series > 99:
                    embed = e.get_embed(
                        ":warning: 도서 권 수가 잘못됐습니다!", error=True
                    )
                    embed.set_author(
                        name=interaction.user.display_name, icon_url=avatar
                    )
                    await interaction.response.send_message(embed=embed)
                    return

                book.insert_book_data(
                    title,
                    series,
                    byname1,
                    byname2,
                    location,
                    category.value,
                    language.value,
                )
                book_id = book.find_book_id(title, series)
                embed = e.get_embed(
                    f"[{book_id}] {title} {series}권 ({location}) 추가 완료!",
                    title="성공적으로 추가되었습니다!",
                )
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)

    @app_commands.command(name="삭제", description="도서를 삭제합니다")
    @app_commands.describe(book_id="도서 아이디")
    async def delete_book(self, interaction: discord.Interaction, book_id: str):
        # Exception
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

        if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
            embed = e.get_embed(
                ":warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!", error=True
            )
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        # Deletion
        try:
            if book.get_info_by_id(book_id):
                title, series = book.get_info_by_id(book_id)[0]
                book.delete_book_data(book_id)
                embed = e.get_embed(
                    f"[{book_id}] {title} ({series}권)를 삭제하였습니다.",
                    title="성공적으로 삭제되었습니다!",
                )
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)
            else:
                embed = e.get_embed("도서 아이디가 잘못됐습니다 :sob:", error=True)
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)

        except ValueError:
            embed = e.get_embed("도서 아이디가 잘못됐습니다 :sob:", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="수정", description="도서 정보를 수정합니다")
    @app_commands.describe(
        book_id="도서 아이디", change="수정할 부분", to="수정된 데이터"
    )
    @app_commands.choices(change=change_list)
    async def change_book(
        self,
        interaction: discord.Interaction,
        book_id: str,
        change: app_commands.Choice[str],
        to: str,
    ):
        # Exception
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

        if interaction.channel_id not in (1280321483285074047, 1272086876638937130):
            embed = e.get_embed(
                ":warning: 이 커맨드는 도서관 채널에서만 사용 가능합니다!", error=True
            )
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        if not book.get_info_by_id(book_id):
            embed = e.get_embed(":warning: 도서 아이디가 틀렸습니다.", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        if change.value == "title" and book.get_info_by_id(book_id)[0][0] == to:
            embed = e.get_embed(":warning: 변경사항이 없습니다!", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return
        elif change.value in ("title", "byname1", "byname2") and len(to) > 100:
            embed = e.get_embed(":warning: 도서명이 너무 깁니다!", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return
        elif change.value == "location" and (
            len(to) > 4 or "-" not in to or to.upper() != to
        ):
            embed = e.get_embed(":warning: 책장 번호를 다시 확인해주세요.", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return
        elif change.value == "category" and to not in [v.value for v in category_list]:
            embed = e.get_embed(":warning: 카테고리가 유효하지 않습니다!", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return
        elif change.value == "language" and to not in [v.value for v in language_list]:
            embed = e.get_embed(":warning: 언어가 유효하지 않습니다!", error=True)
            embed.set_author(name=interaction.user.display_name, icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            return

        else:
            # Updating
            try:
                title, series = book.get_info_by_id(book_id)[0]
                book.update_book_data(change.value, to, book_id)
                embed = e.get_embed(
                    f"[{book_id}] {title} ({series}권)의 {change.value}가 {to}로 변경되었습니다.",
                    title="성공적으로 추가되었습니다!",
                )
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)

            except IndexError:
                embed = e.get_embed(
                    ":warning: 알 수 없는 오류가 발생했습니다 :sob:", error=True
                )
                embed.set_author(name=interaction.user.display_name, icon_url=avatar)
                await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(BookRetrieval(bot))
