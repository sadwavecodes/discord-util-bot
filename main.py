import discord
import aiohttp
import os

# Function to fetch data from a URL
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            if response.status != 200:
                raise ValueError('Failed to fetch data')
            return await response.text()

# Function to parse user info from response data
def parse_user_info(data):
    fields = data.split(':')
    return {
        'username': fields[1],
        'stars': fields[3],
        'diamonds': fields[13],
        'coins': fields[5],
        'user_coins': fields[7],
        'demons': fields[17]
    }

# Main command function
async def userinfo_command(ctx, username):
    try:
        # Step 1: Get the account ID using the username
        search_url = f'https://www.boomlings.com/database/getGJUsers20.php?str={username}'
        search_data = await fetch_data(search_url)
        account_id = search_data.split(':')[0]

        if not account_id:
            await ctx.send('User not found.')
            return

        # Step 2: Get the user info using the account ID
        user_info_url = f'https://www.boomlings.com/database/getGJUserInfo20.php?targetAccountID={account_id}'
        user_info_data = await fetch_data(user_info_url)
        user_info = parse_user_info(user_info_data)

        # Create an embed with user info
        embed = discord.Embed(
            title=f'User Info for {username}',
            color=0x0099ff,
        )
        embed.add_field(name='Username', value=user_info['username'], inline=True)
        embed.add_field(name='Stars', value=user_info['stars'], inline=True)
        embed.add_field(name='Diamonds', value=user_info['diamonds'], inline=True)
        embed.add_field(name='Coins', value=user_info['coins'], inline=True)
        embed.add_field(name='User Coins', value=user_info['user_coins'], inline=True)
        embed.add_field(name='Demons', value=user_info['demons'], inline=True)
        embed.set_footer(text='Geometry Dash User Info', icon_url='https://www.boomlings.com/database/icon.png')

        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        await ctx.send('An error occurred while fetching the user info.')

# Replace '<your_bot_token>' with your actual bot token
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content.startswith('!userinfo'):
        username = message.content.split(' ', 1)[1]
        await userinfo_command(message.channel, username)

client.run(TOKEN)
