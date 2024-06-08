import discord
from datetime import datetime, timedelta
import asyncio

# Dictionary to store reminders
reminders = {}
reminder_counter = 1

async def reminder(ctx, time: str, *, reminder_text: str):
    global reminder_counter
    user_id = ctx.author.id

    # Parse time argument
    multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}.get(time[-1])
    if multiplier is None:
        await ctx.send(f'{ctx.author.mention}, invalid time format. Please use s (seconds), m (minutes), h (hours), or d (days).')
        return
    
    try:
        duration = int(time[:-1]) * multiplier
    except ValueError:
        await ctx.send(f'{ctx.author.mention}, invalid time format. Please enter a valid number for the duration.')
        return
    
    if duration < 1 or duration > 604800:  # Check if duration is within 1 second to 7 days
        await ctx.send(f'{ctx.author.mention}, please choose a time between 1 second and 7 days.')
        return
    
    reminder_id = reminder_counter
    reminder_counter += 1

    await ctx.send(f'{ctx.author.mention}, your reminder has been set. Reminder ID: `{reminder_id}`')

    # Schedule the reminder
    reminder_time = datetime.now() + timedelta(seconds=duration)
    reminders[reminder_id] = {"user_id": user_id, "reminder_text": reminder_text, "time": reminder_time}
    await asyncio.sleep(duration)
    if reminder_id in reminders:
        user = await ctx.bot.fetch_user(reminders[reminder_id]["user_id"])
        if user:
            await user.send(f'**Reminder:** *{reminder_text}*\nSet at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            print(f'Reminder sent to {user} at {reminder_time}.')
        del reminders[reminder_id]

async def cancelreminder(ctx, reminder_id: int):
    if reminder_id in reminders:
        del reminders[reminder_id]
        await ctx.send(f'{ctx.author.mention}, your reminder with ID `{reminder_id}` has been canceled.')
    else:
        await ctx.send(f'{ctx.author.mention}, no reminder found with ID `{reminder_id}`.')
