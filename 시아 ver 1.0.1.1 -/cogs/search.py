import discord
import asyncio
from urllib.request import urlopen, Request
import urllib
import urllib.request
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

class search(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="블로그검색")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _search_blog(ctx, *, search_query):
        temp = 0
        url_base = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="
        url = url_base + urllib.parse.quote(search_query)
        title = ["", "", ""] 
        link = ["", "", ""] 
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
        result = soup.find_all('a', "sh_blog_title _sp_each_url _sp_each_title")
        embed = discord.Embed(title="검색 결과", description=" ", color=0x00ff56)
        for n in result:
            if temp == 3: 
                break
            title[temp] = n.get("title")
            link[temp] = n.get("href")
            embed.add_field(name=title[temp], value=link[temp], inline=False)
            temp+=1
        embed.set_footer(text="검색 완료!")
        
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(search(client))
