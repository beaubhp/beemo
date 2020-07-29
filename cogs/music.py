from discord import Embed, FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get

from youtube_dl import YoutubeDL
from asyncio import run_coroutine_threadsafe

import re
import requests
from bs4 import BeautifulSoup

class Music(commands.Cog, name='Music'):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.message = {}

    @staticmethod
    def parse_duration(duration):
        result = []
        m, s = divmod(duration, 60)
        h, m = divmod(m, 60)
        return f'{h:d}:{m:02d}:{s:02d}'

    @staticmethod
    def search(author, arg):
        with YoutubeDL(Music.YDL_OPTIONS) as ydl:
            try: requests.get(arg)
            except: info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            else: info = ydl.extract_info(arg, download=False)

        embed = (Embed(description=f"[{info['title']}]({info['webpage_url']})", color=0x3de4ba)
                .add_field(name='Duration', value=Music.parse_duration(info['duration']))
                .add_field(name='Requested by', value=author)
                .add_field(name='Uploader', value=f"[{info['uploader']}]({info['channel_url']})")
                .set_thumbnail(url=info['thumbnail']))

        return {'embed': embed, 'source': info['formats'][0]['url'], 'title': info['title']}

    async def edit_message(self, ctx):
        embed = self.song_queue[ctx.guild][0]['embed']
        content = "\n".join([f"({self.song_queue[ctx.guild].index(i)}) {i['title']}" for i in self.song_queue[ctx.guild][1:]]) if len(self.song_queue[ctx.guild]) > 1 else "No song queued"
        embed.set_field_at(index=3, name="File d'attente :", value=content, inline=False)
        await self.message[ctx.guild].edit(embed=embed)

    def play_next(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if len(self.song_queue[ctx.guild]) > 1:
            del self.song_queue[ctx.guild][0]
            run_coroutine_threadsafe(self.edit_message(ctx), self.bot.loop)
            voice.play(FFmpegPCMAudio(self.song_queue[ctx.guild][0]['source'], **Music.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
            voice.is_playing()
        else:
            run_coroutine_threadsafe(voice.disconnect(), self.bot.loop)
            run_coroutine_threadsafe(self.message[ctx.guild].delete(), self.bot.loop)

    @commands.command(aliases=['p'], brief='$play [url/words]')
    async def play(self, ctx, *, video: str):
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        song = Music.search(ctx.author.mention, video)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()     

        if not voice.is_playing():
            self.song_queue[ctx.guild] = [song]
            self.message[ctx.guild] = await ctx.send(embed=song['embed'])
            await ctx.message.delete()
            voice.play(FFmpegPCMAudio(song['source'], **Music.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
            voice.is_playing()
        else:
            self.song_queue[ctx.guild].append(song)
            await self.edit_message(ctx)

    @commands.command(brief='$pause')
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await ctx.message.delete()
            if voice.is_playing():
                await ctx.send('Music paused!', delete_after=10.0)
                voice.pause()
            else:
                await ctx.send('Music resumed!', delete_after=10.0)
                voice.resume()

    @commands.command(aliases=['pass'], brief='$skip')
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await ctx.message.delete()
            await ctx.send('Music skipped!', delete_after=10.0)
            voice.stop()

    @commands.command(brief='$remove')
    async def remove(self, ctx, *, num: int):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            del self.song_queue[ctx.guild][num]
            await ctx.message.delete()
            await self.edit_message(ctx)
    
    @commands.command(brief='$lyrics [artist] [song]')
    async def lyrics(self, ctx, song: str):
        message = ctx.message.content
        song = message.replace("$lyrics", "")
        url = self.generateUrl(song)
        html = self.getHtml(url)
        lyrics = self.extractLyrics(html)
        for msg in self.extractLyrics(html):
            await ctx.send(embed= Embed(description= msg, color= 0x3de4ba))
    
    def generateUrl(self,artist):
        host = "https://genius.com/"
        urlWords = [w.lower() for w in artist.split()] + ["lyrics"]
        urlWords[0] = urlWords[0].title()
        return host+"-".join(urlWords)
    
    def getHtml(self,url):
        req = requests.get(url=url)
        return BeautifulSoup(req.content, 'html.parser')
    
    def extractLyrics(self,html):
        htmlString = str(html.find_all("div", "lyrics")[0])
        htmlString, _ = re.subn("</a>","", htmlString)
        htmlString, _= re.subn("<a[^>]*>","", htmlString)
        htmlString, _= re.subn("<p>","", htmlString)
        htmlString, _= re.subn("<!--sse-->","", htmlString)
        htmlString, _= re.subn("<br/>","", htmlString)
        htmlString, _= re.subn("<div class=\"lyrics\">","", htmlString)
        htmlString, _= re.subn("</p>","", htmlString)
        htmlString, _= re.subn("<!--/sse-->","", htmlString)
        htmlString, _= re.subn("</div>","", htmlString)
        htmlString, _= re.subn("<i>","*", htmlString)
        htmlString, _= re.subn("</i>","*", htmlString)
        htmlString, _= re.subn("<b>","**", htmlString)
        htmlString, _= re.subn("</b>","**", htmlString)
        htmlString, _= re.subn("&amp;","&", htmlString)
        htmlString, _= re.subn("&lt;","<", htmlString)
        htmlString, _= re.subn("&gt;",">", htmlString)
        n = 2000
        return [htmlString[i:i+n] for i in range(0, len(htmlString), n)]


def setup(bot):
    bot.add_cog(Music(bot))
