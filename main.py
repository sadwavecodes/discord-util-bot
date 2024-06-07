import discord
from discord.ext import commands, tasks
import os

# Load the Discord bot token from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize the bot with the command prefix "!"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store reminders
reminders = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # Start the reminder loop
    reminder_loop.start()

@bot.command(name='remind', help='Set a daily reminder. Usage: !remind <message>')
async def remind(ctx, *, reminder: str):
    user_id = ctx.author.id
    reminders[user_id] = reminder
    await ctx.send(f'{ctx.author.mention}, I will remind you daily to: {reminder}')

@tasks.loop(hours=24)
async def reminder_loop():
    for user_id, reminder in reminders.items():
        user = bot.get_user(user_id)
        if user:
            await user.send(f'{user.mention}, here is your daily reminder: {reminder}')

@reminder_loop.before_loop
async def before_reminder_loop():
    await bot.wait_until_ready()

# Run the bot
bot.run(DISCORD_TOKEN)
