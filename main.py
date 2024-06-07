from discord.ext import commands
import discord
import gd
import os

bot = commands.Bot(command_prefix="> ")
client = gd.Client()

@bot.event
async def on_ready() -> None:
    bot.client = client
    activity = discord.Activity(type=discord.ActivityType.playing, name="Geometry Dash")
    await bot.change_presence(activity=activity, status=discord.Status.online)

@bot.command(name="daily")
async def get_daily(ctx: commands.Context) -> None:
    try:
        daily = await bot.client.get_daily()

    except gd.MissingAccess:
        return await ctx.send(
            embed=discord.Embed(
                description="Failed to get a daily level.",
                title="Error Occurred", color=0xde3e35)
        )

    embed = (
        discord.Embed(color=0x7289da).set_author(name="Current Daily")
        .add_field(name="Name", value=daily.name)
        .add_field(name="Difficulty", value=f"{daily.stars} ({daily.difficulty.title})")
        .add_field(name="ID", value=f"{daily.id}")
        .set_footer(text=f"Creator: {daily.creator.name}")
    )

    await ctx.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
