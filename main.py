import discord
from gd import GD
import os

# Main command function
async def userinfo_command(ctx, username):
    try:
        # Get user info using gdpy
        user_info = GD().get_user(username)

        # Create an embed with user info
        embed = discord.Embed(
            title=f'User Info for {username}',
            color=0x0099ff,
        )
        embed.add_field(name='Username', value=user_info.name, inline=True)
        embed.add_field(name='Stars', value=user_info.stars, inline=True)
        embed.add_field(name='Diamonds', value=user_info.diamonds, inline=True)
        embed.add_field(name='Coins', value=user_info.coins, inline=True)
        embed.add_field(name='User Coins', value=user_info.user_coins, inline=True)
        embed.add_field(name='Demons', value=user_info.demons, inline=True)
        embed.set_footer(text='Geometry Dash User Info', icon_url='https://www.boomlings.com/database/icon.png')

        await ctx.send(embed=embed)
    except Exception as e:
        print(f"Exception in userinfo_command: {e}")
        await ctx.send('An error occurred while fetching the user info.')

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
        username = message.content.split(' ', 1)[1]
        await userinfo_command(message.channel, username)

client.run(TOKEN)
