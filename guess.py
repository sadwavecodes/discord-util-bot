import random
import discord
from discord.ext import commands

random_number = None

def reset_random_number():
    global random_number
    random_number = random.randint(1, 100)

async def guess_command(ctx, number: int):
    global random_number
    if number == random_number:
        embed = discord.Embed(title="Guessing Game", description="Congratulations! You guessed the correct number!", color=discord.Color.green())
        reset_random_number()  # Generate a new number for the next game
    else:
        embed = discord.Embed(title="Guessing Game", description="Sorry, you guessed wrong. Try again!", color=discord.Color.red())
    await ctx.send(embed=embed)
