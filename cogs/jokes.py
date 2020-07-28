from discord import Member, User, Embed, File
from discord.ext import commands

class Jokes(commands.Cog, name = "Jokes"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        channel = None
        if (str(message.channel) != "beau") or (message.author == (self.bot.user or message.author.bot)):
            return
        if message.content == "Hello!":
            channel = self.bot.get_channel(message.channel.id)
            await channel.send("Hello {0} how are you?".format(message.author))
        if self.isMessageSplitable(message.content):
            channel = self.bot.get_channel(message.channel.id)
            messageid = message.content.split()[2:]
            if message.content.split()[2] == "a":
                messageid = message.content.split()[3:]
            await channel.send("Hello " + " ".join(messageid) + ". I am Bimo!")
            await channel.send(file=File('Bimo Bot/images/bimo.gif')) 
    
    def isMessageSplitable(self,message):
        isLong = len(message.split()) > 2 
        correctFormat = message.split()[0] == "I" and message.split()[1] == "am"
        return isLong and correctFormat

def setup(bot):
    bot.add_cog(Jokes(bot))
