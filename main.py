import os
import discord
from discord.ext import commands

# Load the Discord bot token from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load reminders
from reminders import reminder, cancelreminder

# Load utilities
from utils import setup_bot

@bot.command(description="Help for commands") # this decorator makes a slash command
async def help(ctx): # a slash command will be created with the name "ping"
        embed = discord.Embed(title="Help", description="List of available commands:", color=discord.Color.blue())
        embed.add_field(name="!reminder <time> <message>", value="Set a reminder. Time examples: 1s, 1m, 1h, 1d", inline=False)
        embed.add_field(name="!cancelreminder <reminder_id>", value="Cancel a reminder by ID.", inline=False)
        await ctx.send(embed=embed)


# Run the bot
setup_bot(bot)
bot.run(DISCORD_TOKEN)
