from discord import Member, User, Embed
from discord.ext import commands
from asyncio import sleep

class Admin(commands.Cog, name = "Admin"):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def mute_handler(ctx, member, messages=False):
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(member, send_messages=messages)

    @commands.command(aliases=['purge'], brief='$clear [x]')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, x: int):
        await ctx.channel.purge(limit=x+1)

    @commands.command(brief='$mute [member] [reason]')
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: Member, time: str, *, reason: str = None):
        units = {"s": [1, 'seconds'], "m": [60, 'minutes'], "h": [3600, 'hours']}
        duration = int(time[:-1]) * units[time[-1]][0]
        time = f"{time[:-1]} {units[time[-1]][1]}"
        await self.mute_handler(ctx, member)
        embed = Embed(color=0x3de4ba, description=f'{ctx.author.mention} muted {member} for {time}!')
        await ctx.send(embed=embed)
        await sleep(duration)
        await self.mute_handler(ctx, member, True)
        embed = Embed(color=0x3de4ba, description=f'{member.mention} has been unmuted!')
        await ctx.send(embed=embed)

    @commands.command(brief='$kick [member] [reason]')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason: str = None):
        embed = Embed(description=f'{ctx.author.mention} kicked **{member}**!')
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

    @commands.command(brief='$ban [member] [reason]')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, *, reason: str = None):
        embed = Embed(description=f'{ctx.author.mention} banned **{member}**!')
        await member.ban(reason=reason)
        await ctx.send(embed=embed)

    @commands.command(brief='$unban [member] [reason]')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: str, *, reason: str = None):
        ban_list = await ctx.guild.bans()
        if not ban_list:
            embed = Embed(title="Something went wrong:", description="No users banned!", color=0x3de4ba)
            await ctx.send(embed=embed); return
        for entry in ban_list:
            if member.lower() in entry.user.name.lower():
                embed = Embed(description=f'{ctx.author.mention} unbanned **{entry.user.mention}**!')
                await ctx.guild.unban(entry.user, reason=reason)
                await ctx.send(embed=embed); return
        embed = Embed(title="Something went wrong:", description="No matching banned users!", color=0x3de4ba)
        await ctx.send(embed=embed); return

    
def setup(bot):
    bot.add_cog(Admin(bot))
