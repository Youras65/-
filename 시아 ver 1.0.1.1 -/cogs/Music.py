import re
import discord
import lavalink
from discord.ext import commands
import inspect, math
from config import BOTID

url_rx = re.compile(r'https?://(?:www\.)?.+')

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):
            bot.lavalink = lavalink.Client(BOTID)
            bot.lavalink.add_node('127.0.0.1', 2333, '123456', 'eu', 'default-node')
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')
        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)
        return guild_check

    async def ensure_voice(self, ctx):
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('재생',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('먼저 음성 채널에 들어가주세요')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('연결되지 않았어요')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                raise commands.CommandInvokeError('연결하기 또는 말하기 권한이 없어요')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('제가 들어있는 음성 채널에 들어와 주세요')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command(name='재생', aliases=['play', 'p', 'ㅔ', 'ㅔㅣ묘'])
    async def 재생(self, ctx, *, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)
        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')
        embed = discord.Embed()#color=self.normal_color)
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            embed.set_image(url=f'https://i.ytimg.com/vi/{track["info"]["identifier"]}/hqdefault.jpg')
            player.add(requester=ctx.author.id, track=track)
        await ctx.send(embed=embed)
        if not player.is_playing:
            await player.play()
        if not player.is_playing:
            await player.play()

    @commands.command()
    async def 깡(self, ctx):
        await self.재생(ctx, query="깡")
        await self.재생(ctx, query="깡 리믹스")
        await self.재생(ctx, query="라 깡")

    @commands.command(name='들어와', aliases=['j', 'join'])
    async def 들어와(self, ctx, channel=None):
        if channel == None:
            channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

    @commands.command(name='나가', aliases=['dc', 'disconnect'])
    async def 나가(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voicechannel!')

        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('*⃣ | Disconnected.')

    @commands.command(name='재생목록', aliases=['q', 'queue'])
    async def 재생목록(self, ctx, page: int = 1):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.queue:
            return await ctx.send('Nothing queued.')
        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)
        start = (page - 1) * items_per_page
        end = start + items_per_page
        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'
        embed = discord.Embed(colour=discord.Color.blurple(),
                              description=f'**{len(player.queue)} tracks**\n\n{queue_list}')
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        await ctx.send(embed=embed)

    @commands.command(name='스킵', aliases=['skip'])
    async def 스킵(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('아무것도 플레이하고 있지 않아요')

        await player.skip()
        await ctx.send('스킵했어요!')

    @commands.command(aliases=['nowplaying','np', 'n'])
    async def 지금곡(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.current:
            return await ctx.send('Nothing playing.')
        position = lavalink.format_time(player.position)
        if player.current.stream:
            duration = '🔴 LIVE'
        else:
            duration = lavalink.format_time(player.current.duration)
        song = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'
        embed = discord.Embed(color=discord.Color.blurple(),
                              title='Now Playing', description=song)
        sans = player.current.uri.split('/')[-1].split('?v=')[-1]
        embed.set_image(url=f'https://i.ytimg.com/vi/{sans}/hqdefault.jpg')
        await ctx.send(embed=embed)

    @commands.command(aliases=['m', 'move', 'ㅡ','seek'])
    async def 시간스킵(self, ctx, *, seconds: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        track_time = player.position + (seconds * 1000)
        await player.seek(track_time)

        await ctx.send(f':hammer_pick: | 시간 스킵: {lavalink.utils.format_time(track_time)}')

    @commands.command(aliases=['loop'])
    async def repeat(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('Nothing playing.')
        player.repeat = not player.repeat
        await ctx.send('🔁 | Repeat ' + ('enabled' if player.repeat else 'disabled'))

    @commands.command(aliases=['vol', 'v', '볼륨'])
    async def volume(self, ctx, volume: int = None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not volume:
            return await ctx.send(f'🔈 | {player.volume}%')
        await player.set_volume(volume) 
        await ctx.send(f'🔈 | Set to {player.volume}%')

def setup(bot):
    bot.add_cog(Music(bot))