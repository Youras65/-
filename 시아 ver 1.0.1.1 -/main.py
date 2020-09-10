import discord, os
from discord.ext import commands
from config import TOKEN

client = commands.Bot(command_prefix="시아야 ")

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)