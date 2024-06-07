import discord
import aiohttp
import os

# Function to fetch data from a URL
async def fetch_data(url, payload=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers) as response:
                if response.status != 200:
                    raise ValueError(f'Failed to fetch data. Status: {response.status}')
                return await response.text()
    except Exception as e:
        print(f"Exception while fetching data: {e}")
        raise

# Function to parse user info from response data
def parse_user_info(data):
    fields = data.split(':')
    if len(fields) < 18:
        raise ValueError(f"Unexpected data format: {data}")
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
        search_url = 'https://www.boomlings.com/database/getGJUsers20.php'
        payload = {'str': username}
        print(f"Fetching data from: {search_url} with payload: {payload}")
        search_data = await fetch_data(search_url, payload=payload)
        print(f"Search data received: {search_data}")

        # Check if the user exists
        if '|NoGDAccount' in search_data:
            await ctx.send('User not found.')
            return

        # Extract the account ID from the search data
        account_id = search_data.split(':')[1]
        print(f"Account ID found: {account_id}")

        # Step 2: Get the user info using the account ID
        user_info_url = 'https://www.boomlings.com/database/getGJUserInfo20.php'
        payload = {'targetAccountID': account_id}
        print(f"Fetching user info from: {user_info_url} with payload: {payload}")
        user_info_data = await fetch_data(user_info_url, payload=payload)
        print(f"User info data received: {user_info_data}")
        
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
