from discord import Game
from discord.ext import commands

bot = commands.Bot(command_prefix='$')
initial_extensions = [
    'cogs.admin',
    'cogs.music',
]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}')
    await bot.change_presence(activity=Game(name='$help | made by bahburs'))
    print(f'Bimo is ready!')

bot.run('BotTokenHere', bot=True, reconnect=True)
