from discord import Embed
from discord.ext import commands
import random


class Diceroll(commands.Cog, name = "Diceroll"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='$coin [heads/tails]')
    async def coin(self, ctx, arg):
        if arg.lower() == 'heads' or arg.lower() == 'tails':
            piece = random.choice(['heads', 'tails'])
            if arg.lower() in piece:
                await ctx.send(embed= Embed(description= f'{piece.title()}. You won!', color= 0x3de4ba))
            else:
                await ctx.send(embed= Embed(description= f'{piece.title()}. You lost!', color= 0x3de4ba))
        else:
            await ctx.send(embed= Embed(description= 'You must input either "heads" or "tails"!', color= 0x3de4ba))      

    @commands.command(brief='$roll [x]')
    async def roll(self, ctx, arg):
        try:
            float(arg)
        except:
            await ctx.send(embed= Embed(description= 'You must input an integer!', color= 0x3de4ba))
        else:
            number = random.randint(1, int(arg))
            await ctx.send(embed= Embed(description= f'You rolled a {number}!', color= 0x3de4ba))

def setup(bot):
    bot.add_cog(Diceroll(bot))
