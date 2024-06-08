import os
import discord
from discord.ext import commands
from help import HelpCommand, setup_help

# Load the Discord bot token from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Setup help command
setup_help(bot)

# Run the bot
bot.run(DISCORD_TOKEN)
