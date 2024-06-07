import discord
from discord.ext import commands
from discord.ui import View, Button

class LevelIDButton(Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.secondary, label="Enter Level ID")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.message.channel.send("Please enter the Level ID.")

class MyView(View):
    def __init__(self):
        super().__init__()
        self.add_item(LevelIDButton())

bot = commands.Bot(command_prefix="!")

@bot.command()
async def open_modal(ctx):
    view = MyView()
    await ctx.send("Click the button to enter the Level ID.", view=view)

bot.run("MTIzOTkwMzM1NTQ0NzU0MTgzMg.GdQTpo.B4WuJD0yYfF8Tf1R8tTM7Kt24bUOg0GEwD8tds")
