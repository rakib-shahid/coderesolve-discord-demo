import discord
import os
from dotenv import load_dotenv
import asyncio
from discord.ext import commands

load_dotenv()

# basic bot setup
########################################
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="cr$", intents=intents)
########################################


# On Ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def load():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")


async def main():
    await load()

    ########################################
    # START BOT
    await bot.start(os.getenv("TOKEN"))
    ########################################


asyncio.run(main())
