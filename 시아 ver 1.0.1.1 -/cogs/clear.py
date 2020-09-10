import discord
import asyncio
from urllib.request import urlopen, Request
import urllib
import urllib.request
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

class clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def 지워(self, ctx, amount : int):
        try:
            await ctx.channel.purge(limit=amount + 1)
        except:
            await ctx.send("지울 메시지의 개수를 적어주세요.")
        

def setup(client):
    client.add_cog(clear(client))