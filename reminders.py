import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

# Dictionary to store reminders
reminders = {}
reminder_counter = 0

async def schedule_reminder(bot, reminder_id, duration):
    await asyncio.sleep(duration)
    if reminder_id in reminders:
        reminder_info = reminders.pop(reminder_id)
        user = await bot.fetch_user(reminder_info["user_id"])
        if user:
            await user.send(f'**Reminder:** *{reminder_info["reminder_text"]}*\nSet at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            print(f'Reminder sent to {user} at {datetime.now()}.')

async def reminder(ctx, time: str, *, reminder_text: str):
    global reminder_counter
    user_id = ctx.author.id

    print(f'Creating reminder for user: {user_id}, time: {time}, text: {reminder_text}')

    # Parse time argument
    multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}.get(time[-1])
    if multiplier is None:
        await ctx.send(f'{ctx.author.mention}, invalid time format. Please use s (seconds), m (minutes), h (hours), or d (days).')
        print('Invalid time format received')
        return
    
    try:
        duration = int(time[:-1]) * multiplier
    except ValueError:
        await ctx.send(f'{ctx.author.mention}, invalid time format. Please enter a valid number for the duration.')
        print('Invalid number for duration')
        return
    
    if duration < 1 or duration > 604800:  # Check if duration is within 1 second to 7 days
        await ctx.send(f'{ctx.author.mention}, please choose a time between 1 second and 7 days.')
        print('Duration out of allowed range')
        return
    
    reminder_id = reminder_counter
    reminder_counter += 1

    reminders[reminder_id] = {"user_id": user_id, "reminder_text": reminder_text}

    await ctx.send(f'{ctx.author.mention}, your reminder has been set. Reminder ID: **{reminder_id}**')

    print(f'Reminder ID {reminder_id} set for user {user_id}, will trigger in {duration} seconds.')

    # Schedule the reminder
    await asyncio.create_task(schedule_reminder(ctx.bot, reminder_id, duration))

async def cancelreminder(ctx, reminder_id: int):
    if reminder_id in reminders:
        reminders.pop(reminder_id)
        await ctx.send(f'{ctx.author.mention}, your reminder with ID **{reminder_id}** has been canceled.')
        print(f'Reminder ID {reminder_id} canceled.')
    else:
        await ctx.send(f'{ctx.author.mention}, no reminder found with ID **{reminder_id}**.')
        print(f'No reminder found with ID {reminder_id}.')
