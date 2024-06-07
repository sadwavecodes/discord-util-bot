import os
import discord
from discord_slash import SlashCommand, SlashContext

intents = discord.Intents.default()
intents.messages = True

bot = discord.Client(intents=intents)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@slash.slash(name="recentmodsend", description="Displays the last 5 messages with pictures from a specific channel")
async def recentmodsend(ctx: SlashContext):
    channel_id = 1245824371394613439
    channel = bot.get_channel(channel_id)
    
    recent_messages = await channel.history(limit=5).flatten()
    embed = discord.Embed(title="Recent Messages", color=discord.Color.blue())
    
    for message in recent_messages:
        embed.add_field(name=f"Message by {message.author}", value=message.content, inline=False)
        if message.attachments:
            embed.set_image(url=message.attachments[0].url)
    
    await ctx.send(embed=embed)

bot.run(os.environ.get('DISCORD_TOKEN'))
