import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
@bot.command(description="Sends the bot's latency.") 
    async def help(ctx)
        embed = discord.Embed(title="Help", description="List of available commands:", color=discord.Color.blue())
        embed.add_field(name="!reminder <time> <message>", value="Set a reminder. Time examples: 1s, 1m, 1h, 1d", inline=False)
        embed.add_field(name="!cancelreminder <reminder_id>", value="Cancel a reminder by ID.", inline=False)
        await ctx.send(embed=embed)

async def setup_help(bot):
    help = HelpCommand()
    bot.add_command(help_command)
