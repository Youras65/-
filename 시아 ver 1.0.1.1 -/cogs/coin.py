import discord
import asyncio
import random
from urllib.request import urlopen, Request
import urllib
import urllib.request
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

class coin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="동전던지기")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coin(self, ctx):
        randomlist = ["*(데구르르르)*...앞면이 나왔어요!", "*(데구르르르)*...뒷면이 나왔어요!","*(데구르르르)*...옆면이 나왔어요..?"]
        ran = random.randint(0, len(randomlist)-1)
        await ctx.send(randomlist[ran])


def setup(client):
    client.add_cog(coin(client))