import discord
from discord.ext import commands

async def myhelp_command(ctx):
    embed = discord.Embed(title="Help", description="List of available commands:", color=discord.Color.blue())
    embed.add_field(name="!reminder <time> <message>", value="Set a reminder. Time examples: 1s, 1m, 1h, 1d", inline=False)
    embed.add_field(name="!cancelreminder <reminder_id>", value="Cancel a reminder by ID.", inline=False)
    await ctx.send(embed=embed)

def setup_help(bot):
    bot.add_command(commands.Command(myhelp_command, name='myhelp', help='Show this help message.'))
