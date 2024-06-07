import discord
from discord.ext import commands, tasks
import os
import uuid

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
    reminder_id = str(uuid.uuid4())
    
    if user_id not in reminders:
        reminders[user_id] = {}

    reminders[user_id][reminder_id] = reminder
    reminder_message = f'{ctx.author.mention}, your reminder has been set. Your Reminder ID is: `{reminder_id}`'
    await ctx.send(reminder_message)

@bot.command(name='cancelreminder', help='Cancel a reminder by ID. Usage: !cancelreminder <reminder_id>')
async def cancelreminder(ctx, reminder_id: str):
    user_id = ctx.author.id
    if user_id in reminders and reminder_id in reminders[user_id]:
        del reminders[user_id][reminder_id]
        if not reminders[user_id]:  # Clean up if no reminders left
            del reminders[user_id]
        await ctx.send(f'{ctx.author.mention}, your reminder with ID `{reminder_id}` has been canceled.')
    else:
        await ctx.send(f'{ctx.author.mention}, no reminder found with ID `{reminder_id}`.')

@tasks.loop(hours=24)
async def reminder_loop():
    for user_id, user_reminders in reminders.items():
        for reminder_id, reminder in user_reminders.items():
            user = bot.get_user(user_id)
            if user:
                reminder_message = f'Here is your daily reminder: {reminder}\nReminder ID: `{reminder_id}`'
                await user.send(f'{user.mention}, {reminder_message}')

@reminder_loop.before_loop
async def before_reminder_loop():
    await bot.wait_until_ready()

# Run the bot
bot.run(DISCORD_TOKEN)
