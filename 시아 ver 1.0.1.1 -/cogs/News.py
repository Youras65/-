import discord
import asyncio
from urllib.request import urlopen, Request
import urllib
import urllib.request
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

class News(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="뉴스") 
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def adwuhi(self, ctx):
        temp = 0
        u = requests.get("https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100")
        t = u.content
        bus = BeautifulSoup(t, "html.parser")
        babo = bus.find("ul", {"class": "type06_headline"})
        hi = babo.find_all("li")
        embed = discord.Embed(title="오늘 최신 뉴스를 가지고 왔어요.", description="")
        for item in hi:
            if temp == 3:
                break
            title = item.find("dt", "").find("a").text.strip("\n\t")
            cuty = item.find("span", {"class": "lede"}).text
            sim = item.find("span", {"class": "writing"}).text
            embed.add_field(name=title, value=cuty+ "\n"+sim + "\n_____________________", inline=False)
            embed.set_footer(text="이 뉴스는 1분마다 새로고침 돼요!\n이 뉴스들의 출처는 네이버 뉴스 에요!")
            temp+=1
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(News(client))