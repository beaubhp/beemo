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
                await ctx.send(f'{piece.title()}! You won.')
            else:
                await ctx.send(f'{piece.title()}! You lost.')
        else:
            await ctx.send('You must input either "heads" or "tails"!')         

    @commands.command(aliases=['r'], brief='$roll [x]')
    async def roll(self, ctx, arg):
        try:
            float(arg)
        except:
            await ctx.send('You must input an integer!')
        else:
            number = random.randint(1, int(arg))
            await ctx.send(f'You rolled a {number}!')

def setup(bot):
    bot.add_cog(Diceroll(bot))