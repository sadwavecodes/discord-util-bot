import discord
from discord.ext import commands
import os

# Load the Discord bot token from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize the bot with the command prefix "!"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Import and setup bot commands from utils
from utils import setup_bot
setup_bot(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run the bot
bot.run(DISCORD_TOKEN)
