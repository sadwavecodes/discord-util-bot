import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.slash_command()
async def recentmodsend(ctx):
    channel_id = 1245824371394613439
    channel = bot.get_channel(channel_id)
    
    recent_messages = await channel.history(limit=5).flatten()
    embed = discord.Embed(title="Recent Messages", color=discord.Color.blue())
    
    for message in recent_messages:
        embed.add_field(name=f"Message by {message.author}", value=message.content, inline=False)
        if message.attachments:
            embed.set_image(url=message.attachments[0].url)
    
    await ctx.send(embed=embed)

bot.run('DISCORD_TOKEN')
