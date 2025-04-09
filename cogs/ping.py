import discord
from discord.ext import commands
from discord import app_commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ping command loaded")

    @app_commands.command(name="ping", description="test2!")  # this is a slash command
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.defer()
        # real command logic goes
        if interaction.user != self.bot.user:
            await interaction.followup.send("Pong!")


async def setup(bot):
    await bot.add_cog(Ping(bot))
