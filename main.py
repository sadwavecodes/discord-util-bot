import discord
from gd import GDClient
import os

# Main command function
async def userinfo_command(channel, user_input):
    try:
        # Initialize GDClient
        gd_client = GDClient()

        # Fetch user info based on user input
        user_info = gd_client.get_user(user_input)

        # Create an embed with user info
        embed = discord.Embed(
            title=f'User Info for {user_input}',
            color=0x0099ff,
        )
        embed.add_field(name='Username', value=user_info.name, inline=True)
        embed.add_field(name='Stars', value=user_info.stars, inline=True)
        embed.add_field(name='Diamonds', value=user_info.diamonds, inline=True)
        embed.add_field(name='Coins', value=user_info.coins, inline=True)
        embed.add_field(name='User Coins', value=user_info.user_coins, inline=True)
        embed.add_field(name='Demons', value=user_info.demons, inline=True)
        embed.set_footer(text='Geometry Dash User Info', icon_url='https://www.boomlings.com/database/icon.png')

        await channel.send(embed=embed)
    except Exception as e:
        print(f"Exception in userinfo_command: {e}")
        await channel.send('An error occurred while fetching the user info.')

TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content.startswith('!userinfo'):
        # Split the message to get the command and the user input
        command, user_input = message.content.split(' ', 1)

        # Check if user input is provided
        if not user_input:
            await message.channel.send('Please provide a username or user ID.')
            return

        # Fetch user info based on user input
        await userinfo_command(message.channel, user_input)

client.run(TOKEN)
