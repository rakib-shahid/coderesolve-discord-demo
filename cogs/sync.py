# sync all commands2
import discord
from discord.ext import commands

class Sync(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Sync command loaded')

    # sync command
    # move into main if possible
    @commands.command()
    async def sync(self, ctx) -> None:
        # check if user ids are me anurag or jubayer
        if (ctx.message.author.id == 235835251052642315):
            # change nickname
            await self.bot.user.edit(username='code resolve demo')
            print("Changed name and status")
            
            # sync commands
            fmt = await ctx.bot.tree.sync()
            commands = len(fmt)
            print("Synced commands")
            user = self.bot.get_user(ctx.message.author.id)
            # send message
            await ctx.send(f'{user.mention} synced {commands} commands')
            print("Replied")
            
async def setup(bot):
    await bot.add_cog(Sync(bot))