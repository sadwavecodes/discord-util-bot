import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

@slash.slash(name="reqbutton", description="Create a button to submit level information")
async def reqbutton(ctx: SlashContext):
    # Creating button
    button = create_button(style=ButtonStyle.blue, label="Submit Level Information", custom_id="submit_info")

    # Creating action row and sending the button
    action_row = create_actionrow(button)
    await ctx.send("Click the button to submit level information:", components=[action_row])

@slash.slash(name="channelselect", description="Select a channel to send level information")
async def channelselect(ctx: SlashContext):
    # Get list of all channels
    channels = [channel.name for channel in ctx.guild.channels]

    # Send list of channels
    await ctx.send("Select the channel to send level information:", options=channels)

@bot.event
async def on_component(ctx):
    # Check if the button was clicked
    if ctx.component_id == "submit_info":
        await ctx.send("Button clicked!")

bot.run(os.getenv("DISCORD_TOKEN"))
