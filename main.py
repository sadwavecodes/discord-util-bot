import discord
from discord.ext import commands
import os
import uuid
import asyncio
from datetime import datetime, timedelta
from discord_slash import SlashCommand

# Load the Discord bot token from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize the bot with the command prefix "/"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Dictionary to store reminders
reminders = {}

# Create a SlashCommand instance
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Define a slash command for setting a reminder
@slash.slash(name='reminder', description='Set a reminder.')
async def reminder(ctx, time: str, *, reminder_text: str):
    user_id = ctx.author.id

    # Parse time argument
    multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}.get(time[-1])
    if multiplier is None:
        await ctx.send('Invalid time format. Please use s (seconds), m (minutes), h (hours), or d (days).')
        return
    
    try:
        duration = int(time[:-1]) * multiplier
    except ValueError:
        await ctx.send('Invalid time format. Please enter a valid number for the duration.')
        return
    
    if duration < 1 or duration > 604800:  # Check if duration is within 1 second to 7 days
        await ctx.send('Please choose a time between 1 second and 7 days.')
        return
    
    reminder_id = str(uuid.uuid4())
    if reminder_id in reminders:
        await ctx.send('A reminder with the same ID is already set.')
        return

    await ctx.send(f'Your reminder has been set. Reminder ID: `{reminder_id}`')

    # Schedule the reminder
    reminder_time = datetime.now() + timedelta(seconds=duration)
    reminders[reminder_id] = {"user_id": user_id, "reminder_text": reminder_text, "time": reminder_time}
    await asyncio.sleep(duration)
    if reminder_id in reminders:
        user = await bot.fetch_user(reminders[reminder_id]["user_id"])
        if user:
            await user.send(f'**Reminder:** *{reminder_text}*\nSet at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            print(f'Reminder sent to {user} at {reminder_time}.')
        del reminders[reminder_id]

# Define a slash command for canceling a reminder
@slash.slash(name='cancelreminder', description='Cancel a reminder by ID.')
async def cancelreminder(ctx, reminder_id: str):
    if reminder_id in reminders:
        del reminders[reminder_id]
        await ctx.send(f'Your reminder with ID `{reminder_id}` has been canceled.')
    else:
        await ctx.send(f'No reminder found with ID `{reminder_id}`.')

# Run the bot
bot.run(DISCORD_TOKEN)
