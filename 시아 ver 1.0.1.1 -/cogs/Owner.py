import discord
from discord.ext import commands
from config import OWNERS
from config import EXTENSIONS

def is_owner():
    async def predicate(ctx):
        return ctx.author.id in OWNERS
    return commands.check(predicate)

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        if isinstance(e, commands.CommandNotFound):
            cmdstart = ctx.message.content[3:]
            await ctx.message.add_reaction('🤔')
            await ctx.send(f'[ {cmdstart} ] (은)는 없는 커맨드네요')
        elif isinstance(e, commands.CommandInvokeError):
            await ctx.message.add_reaction('⚠')
            await ctx.send(f'[ {ctx.message.content} ] 에서 오류 발생!\n```{e.original}```')
        else:
            await ctx.message.add_reaction('⚠')
            await ctx.send(f'[ {ctx.message.content} ] 에서 오류 발생!\n```{e}```')

    @commands.command(name = 'reload', aliases = ['리로드','r'])
    @is_owner()
    async def 리로드(self, ctx, c=None):
        if c == None:
            try:
                for i in EXTENSIONS :
                    self.client.reload_extension (i)
                await ctx.send(f"모든 모듈을 리로드했어요.")
            except Exception as a:
                await ctx.send(f"리로드에 실패했어요. [{a}]")
        else:
            try:
                self.client.reload_extension(c)
                await ctx.send(f"{c} 모듈을 리로드했어요.")
            except Exception as a:
                await ctx.send(f"{c} 모듈 리로드에 실패했어요. [{a}]")

def setup(client):
    client.add_cog(Owner(client))