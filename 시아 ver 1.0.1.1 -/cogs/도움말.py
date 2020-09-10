import discord
import asyncio
import random
from urllib.request import urlopen, Request
import urllib
import urllib.request
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

class 도움말(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="도움말")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def 도움말(self, ctx):
        embed=discord.Embed(title="시아 사용법", description="올바른 사용법(기능)을 알려드려요!", color=0xff752e)
        embed.add_field(name="접두사는", value="```시아야 에요!```", inline=False)
        embed.add_field(name="명령어를 작성할땐", value="**```시아야 (명령어)```** 이렇게 작성해 주세요!", inline=False)
        embed.add_field(name="**정보**", value="```뉴스```", inline=False)
        embed.add_field(name="**기능**", value="```타이머 (초) 지워 (지울 수)```", inline=False)
        embed.add_field(name="**음악**", value="```재생 (음악 이름 또는 링크)\n재생목록\n시간스킵 (int)\n볼륨 (0~100)```", inline=False)
        embed.add_field(name="**미니 게임**", value="```동전던지기```", inline=False)
        embed.set_footer(text="Developed by 너라s#8331\nSpecial Thanks to STORM, PLRS\n나중에 더 많은 기능으로 찾아뵐게요!\nver. 1.1.0.1")
        
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(도움말(client))