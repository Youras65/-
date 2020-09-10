import discord
import asyncio
from discord.ext import commands

async def emojicheck(emoji,ctx: commands.Context, message: discord.Message) -> bool:
    def _check(reaction, user):
        return reaction.message.id == message.id and user == ctx.author
    try:
        reaction, _ = await ctx.bot.wait_for("reaction_add", check=_check, timeout=60.0)
        return reaction.emoji == emoji
    except asyncio.TimeoutError:
        return False

def get_emoji(bot,emoji):
    for i in bot.emojis:
        if i.name == emoji:
            return i