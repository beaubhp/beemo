from discord import Game
from discord.ext import commands

bot = commands.Bot(command_prefix='$')
initial_extensions = [
    'cogs.admin',
    'cogs.music',
    'cogs.intro',
    'cogs.diceroll',
    'cogs.levelling',
]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}')
    await bot.change_presence(activity=Game(name='$help | made by bahburs'))
    print(f'Bimo is ready!')

@bot.command(brief='$ping')
async def ping(ctx):
    await ctx.send(f'Pong, {round(bot.latency * 1000)}ms!')

bot.run("NzM3NDgwNTY3MzE0MTg2MzAw.Xx9-TA.HusoBZ8Z_SQbP8To7kZRmC66p4o", bot=True, reconnect=True)
