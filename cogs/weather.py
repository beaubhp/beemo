from discord import Embed
from discord.ext import commands

from requests import get 
from datetime import datetime

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='$weather [city]')
    async def weather(self, ctx,  *, city):
        data = get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID=fb9df86d9c484eba8a69269cfb0beac9").json()
        cleared_data = {
            'Location:': data['name'],
            'Weather:': f"{data['weather'][0]['main']} - {data['weather'][0]['description']}",
            'Temperature:': f"{int((float(data['main']['temp']) * 1.8) + 32)}°F",
            'Feels like:': f"{int((float(data['main']['feels_like']) * 1.8) + 32)}°F",
            'Sunset:': datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
            'Sunrise:': datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
        }
        embed = Embed(title=f"Weather in: {cleared_data['Location:']}", color=0x3de4ba)
        for key, value in cleared_data.items():
            embed.add_field(name=key, value=value, inline="True")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Weather(bot))
