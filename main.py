import os
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
DiscordComponents(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def recentattachments(ctx):
    channel_id = 1245824371394613439
    channel = bot.get_channel(channel_id)
    
    # Get all messages from the last week
    end_time = discord.utils.utcnow()
    start_time = end_time - discord.timedelta(weeks=1)
    recent_messages = await channel.history(limit=None, after=start_time, before=end_time).flatten()
    
    attachments = []
    for message in recent_messages:
        if message.attachments:
            for attachment in message.attachments:
                attachments.append(attachment.url)
    
    if not attachments:
        await ctx.send("No attachments found in the last week.")
        return
    
    embed = discord.Embed(title="Recent Attachments", color=discord.Color.blue())
    embed.set_image(url=attachments[0])  # Display the first attachment initially
    
    if len(attachments) > 1:
        buttons = [
            Button(style=ButtonStyle.blue, label="Previous", custom_id="previous"),
            Button(style=ButtonStyle.blue, label="Next", custom_id="next")
        ]
        
        message = await ctx.send(embed=embed, components=[buttons])
        
        while True:
            button_ctx = await bot.wait_for("button_click", check=lambda b_ctx: b_ctx.message.id == message.id)
            if button_ctx.custom_id == "previous":
                current_index = attachments.index(embed.image.url)
                previous_index = (current_index - 1) % len(attachments)
                embed.set_image(url=attachments[previous_index])
                await button_ctx.edit_origin(embed=embed)
            elif button_ctx.custom_id == "next":
                current_index = attachments.index(embed.image.url)
                next_index = (current_index + 1) % len(attachments)
                embed.set_image(url=attachments[next_index])
                await button_ctx.edit_origin(embed=embed)

bot.run(os.environ.get('DISCORD_TOKEN'))
