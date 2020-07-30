from discord import Game, Embed
from discord.ext import commands

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')
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

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = Embed(color= 0x3de4ba)
    embed.set_author(name = '¯•.¸¸.•´´¯•.¸¸.•´´¯•.¸¸.•´´¯☛​̳𝘽​̳𝙚​̳𝙚​̳𝙢​̳𝙤​̳ ​̳𝘾​̳𝙤​̳𝙢​̳𝙢​̳𝙖​̳𝙣​̳𝙙​̳𝙨 ̳☚¯´´•.¸¸.•¯´´•.¸¸.•¯´´•.¸¸.•¯')
    embed.add_field(name = '$ping', value='Returns pong and bot latency!', inline="True")
    embed.add_field(name = '$help', value='Sends this message to your DMs!', inline="True")
    embed.add_field(name = '$play [x]', value='Plays song of your choice!', inline="True")
    embed.add_field(name = '$pause', value='Pauses and resumes music!', inline="True")
    embed.add_field(name = '$skip', value='Skips current song playing!', inline="True")
    embed.add_field(name = '$remove [x]', value='Removes # of songs from queue!', inline="True")
    embed.add_field(name = '$lyrics [artist] [song]', value='Sends the lyrics of requested song!', inline="True")
    embed.add_field(name = '$clear [x]', value='Clears # of messages from chat!', inline="True")
    embed.add_field(name = '$mute [user] [time]', value='Mutes user for a certain time!', inline="True")
    embed.add_field(name = '$kick [user] [reason]', value='Kicks user from the server!', inline="True")
    embed.add_field(name = '$ban [user] [reason]', value='Bans user from the server!', inline="True")
    embed.add_field(name = '$unban [user]', value='Unbans user from the server!', inline="True")
    embed.add_field(name = '$roll [x]', value='Rolls a dice!', inline="True")
    embed.add_field(name = '$coin [heads or tails]', value='Flips a coin!', inline="True")
    embed.add_field(name = '$levels', value='Checks the level leaderboard!', inline="True")



    await author.send(embed=embed)
    await ctx.send(embed= Embed(description= 'Check your DMs!', color= 0x3de4ba))

@bot.command(brief='$ping')
async def ping(ctx):
    await ctx.send(embed= Embed(description= f'Pong, {round(bot.latency * 1000)}ms!', color= 0x3de4ba))

bot.run("YourTokenHere", bot=True, reconnect=True)
