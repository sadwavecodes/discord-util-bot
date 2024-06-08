import discord
from discord.ext import commands
import os

# Load the Discord bot token from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize the bot with the command prefix "!"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Import commands from the other modules
from reminders import setup_reminders
from help import setup_help

# Register commands
setup_reminders(bot)
setup_help(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # Register slash commands
    await bot.tree.sync()
    print(f'Synced {len(bot.tree.get_commands())} commands.')

# Run the bot
bot.run(DISCORD_TOKEN)
