import discord
import asyncio
from urllib.request import urlopen, Request
import urllib
import urllib.request
import requests
import time
from bs4 import BeautifulSoup
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="핑")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ping(self, ctx):
        latency = self.client.latency
        await ctx.send(str(round(latency * 1000)) + "ms")




def setup(client):
    client.add_cog(ping(client))