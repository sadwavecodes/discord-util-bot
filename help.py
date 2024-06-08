import discord
from discord.ext import commands

def setup_help(bot):
    @bot.slash_command(name='help', description='Show all available commands')
    async def help(ctx):
        embed = discord.Embed(title="Help", description="List of available commands", color=0x00ff00)
        embed.add_field(name="!ping", value="Ping the bot to check if it's online", inline=False)
        embed.add_field(name="!reminder", value="Set a reminder. Usage: !reminder <time> <message>", inline=False)
        embed.add_field(name="!cancelreminder", value="Cancel a reminder by ID. Usage: !cancelreminder <reminder_id>", inline=False)

        await ctx.send(embed=embed)
