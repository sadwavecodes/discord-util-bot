import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from utils import setup_bot
from help import help

# Load the Discord bot token from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize the bot with the command prefix "!"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot)

# Setup commands
setup_bot(bot)
help(bot)

# Run the bot
bot.run(DISCORD_TOKEN)
