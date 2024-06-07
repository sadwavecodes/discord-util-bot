import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, InputText
import os

# Define the modal
class LevelIDModal(Modal):
    def __init__(self):
        super().__init__(title="Enter Level ID")
        self.add_item(InputText(label="Level ID"))

    async def on_submit(self, interaction: discord.Interaction):
        level_id = self.children[0].value
        await interaction.response.send_message(f"Level ID entered: {level_id}", ephemeral=True)

# Define the button
class LevelIDButton(Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.primary, label="Enter Level ID")

    async def callback(self, interaction: discord.Interaction):
        modal = LevelIDModal()
        await interaction.response.send_modal(modal)

# Define the view that contains the button
class MyView(View):
    def __init__(self):
        super().__init__()
        self.add_item(LevelIDButton())

# Initialize the bot
bot = commands.Bot(command_prefix="!")

@bot.command()
async def open_modal(ctx):
    view = MyView()
    await ctx.send("Click the button to enter the Level ID.", view=view)

# Replace with your actual bot token from the environment variables
bot.run(os.getenv("DISCORD_TOKEN"))
