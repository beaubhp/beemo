from discord import Member, User, Embed, File
from discord.ext import commands

class Intro(commands.Cog, name = "Intro"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        channel = None
        if (message.author == (self.bot.user or message.author.bot)):
            return
        if message.content == "Hello!":
            channel = self.bot.get_channel(message.channel.id)
            await message.channel.send(embed= Embed(description= f'Hello {message.author.mention} how are you?', color= 0x3de4ba))
        if self.isMessageSplitable(message.content):
            channel = self.bot.get_channel(message.channel.id)
            messageid = message.content.split()[2:]
            if message.content.split()[2] == "a":
                messageid = message.content.split()[3:]
            embed = Embed(description = f" Hello " + " ".join(messageid) + ". I am Beemo!", color = 0x3de4ba)
            embed.set_image(url = 'https://github.com/Bahburs/bimo-discord-bot-with-music-etc/blob/master/images/bimo.png?raw=true')
            await message.channel.send(embed = embed)
            
    
    def isMessageSplitable(self,message):
        isLong = len(message.split()) > 2 
        correctFormat = message.split()[0] == "I" and message.split()[1] == "am"
        return isLong and correctFormat

def setup(bot):
    bot.add_cog(Intro(bot))
