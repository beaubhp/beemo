import discord
import json
from discord.ext import commands
import os

class Levelling(commands.Cog, name = "Levelling"):
    def __init__(self, bot):
        self.bot = bot
    
    os.chdir(r'C:\Users\mrhyt\Desktop\Projects\Python Applications\Bimo Bot')
 
    @commands.Cog.listener("on_message")
    async def on_message(self, message):
        if message.author.bot == False:
            with open('json/users.json', 'r') as f:
                users = json.load(f)
    
    
            await self.update_data(users, message.author)
            await self.add_experience(users, message.author, 5)
            await self.level_up(users, message.author, message)
    
    
            with open('json/users.json', 'w') as f:
                json.dump(users, f)
    
    
    async def update_data(self, users, user):
        if not f'{user.mention}' in users:
            users[f'{user.mention}'] = {}
            users[f'{user.mention}']['experience'] = 0
            users[f'{user.mention}']['level'] = 1
    
    
    async def add_experience(self, users, user, exp):
        users[f'{user.mention}']['experience'] += exp
    
    async def level_up(self, users, user, message):
        experience = users[f'{user.mention}']['experience']
        lvl_start = users[f'{user.mention}']['level']
        lvl_end = int(experience ** (1/4))
        if lvl_start < lvl_end:
            await message.channel.send(embed= discord.Embed(description= f'{user.mention} has reached level {lvl_end}!', color= 0x3de4ba))
            users[f'{user.mention}']['level'] = lvl_end
    
    @commands.command(brief='$levels')
    async def levels(self, ctx):
        f = open('json/users.json')
        await ctx.send(embed = discord.Embed(description= f.read(), color= 0x3de4ba))


def setup(bot):
    bot.add_cog(Levelling(bot))
