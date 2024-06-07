import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from discord_components import DiscordComponents, Button, ButtonStyle

bot = commands.Bot(command_prefix='!')
slash = SlashCommand(bot)
DiscordComponents(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@slash.slash(name="button", description="Creates a button")
async def button(ctx: SlashContext):
    # Create a button
    button = Button(style=ButtonStyle.green, label="Open Modal", custom_id="open_modal")

    # Send a message with the button
    await ctx.send(content="Click the button to open the modal", components=[button])

@bot.event
async def on_button_click(interaction):
    if interaction.custom_id == "open_modal":
        # Open a modal
        action_row = manage_components.create_actionrow(
            manage_components.create_button(
                style=ButtonStyle.green, label="Submit", custom_id="submit_button"
            )
        )
        await interaction.send(content="Please fill out the form", components=[action_row])

@bot.event
async def on_dropdown(interaction):
    if interaction.custom_id == "channel_dropdown":
        channel_id = interaction.values[0]  # Get the selected channel ID
        channel = bot.get_channel(int(channel_id))
        # Save the selected channel for embedding level information

@slash.slash(name="channelset", description="Set the channel for embedding level information")
async def channelset(ctx: SlashContext):
    # Get all the channels in the guild
    channels = ctx.guild.channels
    # Create a dropdown with channel options
    dropdown = manage_components.create_select(
        options=[
            manage_components.create_select_option(channel.name, str(channel.id))
            for channel in channels
        ],
        placeholder="Select a channel",
        custom_id="channel_dropdown",
    )
    await ctx.send(content="Select a channel", components=[manage_components.create_actionrow(dropdown)])

@bot.event
async def on_select_option(interaction):
    await interaction.respond(type=7)

bot.run(os.getenv('DISCORD_TOKEN'))
