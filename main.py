import os
import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Discord bot token
TOKEN = os.getenv('DISCORD_TOKEN')

# Google Sheets credentials
SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
SPREADSHEET_KEY = '1_MGZdYGTN-VzaBrCR-_W-fW8Jk08Pa3QEVTyiPgfr4E'
SHEET_NAME = 'Sheet1'

# Discord channel ID
CHANNEL_ID = 991823635037814855

# Initialize bot
bot = commands.Bot(command_prefix='!')

# Function to handle changes in the Google Sheet
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message_edit(before, after):
    if after.author == bot.user:
        return
    if after.channel.id == CHANNEL_ID:
        cell_value = after.content
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'Edited entry in row B: {cell_value}')

# Run the bot
bot.run(TOKEN)
