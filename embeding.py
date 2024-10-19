import discord


def get_embed(desc, error=False, title=None):
    if not error:
        # 오류가 아니면; 기본값
        color = 0x23a55a
    elif error and title is None:
        title = '오류가 발생했습니다.'
        color = 0xdb5060

    return discord.Embed(title=title, description=desc, color=color)
