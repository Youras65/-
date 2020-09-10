import discord
import time
import asyncio
from discord.ext import commands

class Timer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is Online.")
    async def status_loop(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=self.messages[0], type=discord.ActivityType.playing))
        self.messages.append(self.messages.pop(0))
        await asyncio.sleep(15)

    @commands.command(name="타이머", help="타이머기능입니다.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def timer(self, ctx, set_time:int):
        msg=await ctx.send(embed=discord.Embed(title=f"{set_time}초 남았어요."))
        for i in range(set_time):
            set_time -= 1
            embed=discord.Embed(title=f"{set_time}초 남았어요.")
            await msg.edit(embed=embed)
            await asyncio.sleep(1)
        embed=discord.Embed(title="땡!")
        await msg.edit(embed=embed, delete_after=5)
        await ctx.send(f"{ctx.author.mention}님 타이머가 끝났어요.")


def setup(client):
    client.add_cog(Timer(client))