from logging import ERROR, error
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


def get_prefix(bot, message):
    try:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
            return prefixes[str(message.guild.id)]

    except KeyError:  # if the guild's prefix cannot be found in 'prefixes.json'
        with open("prefixes.json", "r") as k:
            prefixes = json.load(k)
        prefixes[str(message.guild.id)] = "nn."

        with open("prefixes.json", "w") as j:
            json.dump(prefixes, j, indent=4)

        with open("prefixes.json", "r") as t:
            prefixes = json.load(t)
            return prefixes[str(message.guild.id)]

    except:  # I added this when I started getting dm error messages
        return "nn."  # This will return "nn." as a prefix.default prefix.


bot = commands.Bot(
    command_prefix=get_prefix, help_command=commands.MinimalHelpCommand()
)

filtered_words = ["angy"]


@bot.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()
            await msg.channel.send(
                f"{msg.author.mention} Message Deleted", delete_after=5.0
            )
    await bot.process_commands(msg)


@bot.event
async def on_ready():

    print("Bot Is Ready!")


filtered_words = ["angy", "kayb"]


@bot.event
async def on_message(msg):
    for word in filtered_words:
        if str(word.lower()) in msg.content:
            await msg.delete()
            await msg.channel.send(
                f"{msg.author.mention} Message Deleted", delete_after=5.0
            )
    await bot.process_commands(msg)


@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "nn."

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.command()
async def changeprefix(ctx, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f"Prefix changed to: `{prefix}`")


@bot.on_error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "Specify What Prefix You'd Like With `changeprefix <prefix you'd like it to be changed to'>`"
        )


bot.run("OTA1MjU3OTAyMTU4MjYyMzEz.YYHdHg.kNvx-VfOxuDRhLeYdrwZQkjLDjk")
