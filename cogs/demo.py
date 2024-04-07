import discord
from discord.ext import commands
from discord import app_commands

class Demo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Demo command loaded')
    
    @app_commands.command(name='demo', description='test!') # this is a slash command
    async def demo(self, interaction:discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send('Hello! This is a test!')

async def setup(bot):
    await bot.add_cog(Demo(bot))