from logging import ERROR, error
from sys import prefix
from typing import Mapping
import discord
import json
import os
from discord import client
from discord.colour import Color
from discord.ext import commands, tasks
import random
from itertools import cycle
from discord.utils import get
import asyncio
from PIL import ImageColor

class Moderation(commands.Cog):
    
    def __init__(self, bot):
        self.client = bot
    
    
    # Commands    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')
        

        
        
    @commands.command()
    async def echo(self, ctx, arg):
        await ctx.send(arg)

    @echo.error
    async def echo_error(self, ctx, error):
        await ctx.send("There was an error")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("MIssing Required Argument")
        else:
            raise error
        

def setup(bot):
    bot.add_cog(Moderation(bot))