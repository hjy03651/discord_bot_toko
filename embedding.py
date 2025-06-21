import discord


def pagination(query, result):
    page_size = 10
    embeds = []
    for start in range(0, len(result), page_size):
        chunk = result[start : start + page_size]
        embed = discord.Embed(
            title=f"{query}에 대한 검색 결과 ({start + 1}–{min(start + page_size, len(result))}/{len(result)})",
            color=0x23A55A,
        )
        for book_id, book_title, book_num, book_location, book_rentable in chunk:
            embed.add_field(
                name=f"[{book_id}] {book_title} {book_num}권",
                value=f"책장: {book_location} ({book_rentable})",
                inline=False,
            )
        embeds.append(embed)
    return embeds


def get_embed(desc, error=False, title=None):
    color = 0x2B2D30
    if error and title is None:
        title = "오류가 발생했습니다."
        color = 0xDB5060
    elif error:
        color = 0xDB5060
    elif title and len(title) >= 5 and title[:5] == "호박 재배":
        color = 0xDB810B
    elif title in ("호박(?) 재배", "호...호 불면은"):
        color = 0x77B255
    elif title == "벌레 재배":
        color = 0x844823
    else:
        color = 0x23A55A  # default

    return discord.Embed(title=title, description=desc, color=color)
