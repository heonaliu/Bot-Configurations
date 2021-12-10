import discord
from discord.ext import commands
from discord.ext.commands import bot

class Test(commands.Cog):
    
    def __init__(self,bot):
       self.bot = bot
       
    @commands.command()
    async def nogroup(self,ctx):
        await ctx.send('This command is not in a group.')
        
    @commands.group(invoke_without_command = True)
    async def group(self,ctx):
        await ctx.send('This is a group')
        
    @group.command()
    async def test(self, ctx):
         await ctx.send('This is a subcommand within the group.')
         
def setup(bot):
    bot.add_cog(Test(bot))