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

# Load slash commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

# Initialize slash commands
slash = SlashCommand(bot, sync_commands=True)

# Register the ping slash command
@slash.slash(
    name="ping",
    description="Sends the bot's latency.",
)
async def ping(ctx):
    await ctx.send(f"Pong! Latency is {int(bot.latency * 1000)}ms")

# Run the bot
setup_bot(bot)
bot.run(DISCORD_TOKEN)
