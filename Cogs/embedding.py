import discord


def pagination(query, result):
    page_size = 10
    embeds = []
    for start in range(0, len(result), page_size):
        chunk = result[start: start + page_size]
        embed = discord.Embed(
            title=f"{query}에 대한 검색 결과 ({start + 1}–{min(start + page_size, len(result))}/{len(result)})",
            color=0x23a55a
        )
        for book_id, book_title, book_num, book_location, book_rentable in enumerate(chunk, start=start + 1):
            embed.add_field(name=f"[{book_id}] {book_title} {book_num}권",
                            value=f"책장: {book_location} ({book_rentable})", inline=False)
        embeds.append(embed)


def get_embed(desc, error=False, title=None):
    color = 0x2b2d30
    if error and title is None:
        title = '오류가 발생했습니다.'
        color = 0xdb5060
    elif title[:5] == '호박 재배':
        color = 0xdb810b
    elif title in ('호박(?) 재배', '호...호 불면은'):
        color = 0x77b255
    elif title == '벌레 재배':
        color = 0x844823
    elif not error:
        color = 0x23a55a  # default

    return discord.Embed(title=title, description=desc, color=color)
