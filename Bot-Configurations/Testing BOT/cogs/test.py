import discord
from discord.ext import commands
from discord.ext.commands.converter import MemberConverter
from discord.ext.commands.errors import MissingRequiredArgument

class Test(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    
    # Commands    
    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        await ctx.send(f"{ctx.author.mention} hugs {member.mention}")
        
    @hug.error
    async def hug_error(self, ctx, error):
        
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("This Member Isn't In This Server")
        await ctx.send("There was an error") 

def setup(client):
    client.add_cog(Test(client))