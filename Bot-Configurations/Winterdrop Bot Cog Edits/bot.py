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

            

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in mapping[cog]]}')
    
    async def send_cog_help(self, cog):
        await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in cog.get_commands()]}')
    
    async def send_group_help(self, group):
        
        await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')
    
    async def send_command_help(self, command):
        await self.get_destination().send(command.name)


def get_prefix(bot, message):
    try:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            return prefixes[str(message.guild.id)]
        
    except KeyError: # if the guild's prefix cannot be found in 'prefixes.json'
        with open('prefixes.json', 'r') as k:
            prefixes = json.load(k)
        prefixes[str(message.guild.id)] = 'nn.'

        with open('prefixes.json', 'w') as j:
            json.dump(prefixes, j, indent = 4)

        with open('prefixes.json', 'r') as t:
            prefixes = json.load(t)
            return prefixes[str(message.guild.id)]
        
    except: # I added this when I started getting dm error messages
        return 'nn.' # This will return "nn." as a prefix.default prefix.
    
def get_embedcolor(bot, message):
    try:
        with open('defaultcolors.json', 'r') as f:
            defaultcolors = json.load(f)
            return defaultcolors[str(message.guild.id)]
        
    except KeyError: # if the guild's prefix cannot be found in 'prefixes.json'
        with open('defaultcolors.json', 'r') as k:
            defaultcolors = json.load(k)
        defaultcolors[str(message.guild.id)] = 88, 101, 242

        with open('defaultcolors.json', 'w') as j:
            json.dump(defaultcolors, j, indent = 4)

        with open('defaultcolors.json', 'r') as t:
            defaultcolors = json.load(t)
            return defaultcolors[str(message.guild.id)]
        
    except: # I added this when I started getting dm error messages
        return 'nn.' # This will return "nn." as a prefix.default prefix.

bot = commands.Bot(command_prefix = get_prefix, default_embed_color = get_embedcolor, help_command = commands.MinimalHelpCommand())
# bot.remove_command('help')

def is_it_owner(ctx):
    return ctx.author.id == 800091221652799500

filtered_words = ["angy"]
@bot.event
async def on_message(ctx):
    for word in filtered_words:
        if word in ctx.content:
            await ctx.delete()
            await ctx.channel.send(f'{ctx.author.mention} Message Deleted', delete_after=5.0)
    await bot.process_commands(ctx)
    
    mention = f'<@!{bot.user.id}>'
    if mention in ctx.content:
        id = str(ctx.guild.id)
        print(id)
        with open('prefixes.json') as myfile:
            data = json.load(myfile)
            for n in data.keys():
                if n == id:
                    prefix = data[n]
                    # print(prefix)
        await ctx.channel.send(f"WHY YOU PING ME T^T Forgot my prefix is : {prefix}")
    
    
            
@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.do_not_disturb)
    change_status.start()
    
    print("Bot Is Ready!")
    
@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        
    prefixes[str(guild.id)] = 'nn.' 
    
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)
        
    with open('defaultcolors.json', 'r') as f:
        defaultcolors = json.load(f)
        
    defaultcolors[str(guild.id)] = 88, 101, 242
    
    with open('defaultcolors.json', 'w') as f:
        json.dump(defaultcolors, f, indent = 4)
        

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        
    prefixes.pop(str(guild.id))
    
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)
    
    
        
    with open('defaultcolors.json', 'r') as f:
       defaultcolors = json.load(f)
        
    defaultcolors.pop(str(guild.id))
    
    with open('defaultcolors.json', 'w') as f:
        json.dump(defaultcolors, f, indent = 4)
        
    
        
@bot.command()
async def changeprefix(ctx, prefix):
    
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        
    prefixes[str(ctx.guild.id)] = prefix
    
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)
        
    await ctx.send(f'Prefix successfully changed to: `{prefix}`')
        
    
    
@bot.command()
async def setdefaultcolor(ctx, hex):
    if hex.startswith('#'):
        hex = hex.replace('#', '')
        rgb =  tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        with open('defaultcolors.json', 'r') as f:
            defaultcolors = json.load(f)
        
        defaultcolors[str(ctx.guild.id)] = rgb
    
        with open('defaultcolors.json', 'w') as f:
            json.dump(defaultcolors, f, indent = 4)
        
        await ctx.send(f'Embed Color Successfully Changed to: #`{hex}`')
    else:
        await ctx.send(f'{ctx.author.mention} Incorrect Usage!')
    

    
    
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send('Invalid Command!')

# Looping Status    
status =['nn.help']    
@tasks.loop(seconds = 5)
async def change_status():
    await bot.change_presence(activity = discord.Game(random.choice(status)))

# Loading Cogs    
@bot.command()
@commands.check(is_it_owner)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    


# Unloading Cogs    
@bot.command()
@commands.check(is_it_owner)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    
@bot.command()
@commands.check(is_it_owner)
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    
@reload.error
async def reload_cog_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please Specify The Cog That You Would Like To Reload')



# Clear 'x' # of Messages  Command
@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount + 1)
    

# Clear Error Message    
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please Specify The Amount Of Message You Would Like To Remove!')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("I'm Sorry I Don't Think You Have The Right Permissions To Use This Command! Please Make Sure You Have The `Manage Permissions` Enabled To Run This Command!")
# Clear Error Message Not Right Perms

@bot.command()
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(
        title = member.name, 
        description = member.mention,
        color = discord.Colour.green())
    embed.add_field(name = "ID" , value = member.id, inline=True)
    await ctx.send(embed = embed)
    
def server_embed_color(server_id):
    with open('defaultcolors.json') as myfile:
        data = json.load(myfile)
        for n in data.keys():
            if n == server_id:
                #r, g, b = data[n][0], data[n][1], data[n][2]
                rgb = data[n]
                return rgb
            
def get_server_prefix(server_id):
    with open('prefixes.json') as prefixfile:
        prefixes = json.load(prefixfile)
        for p in prefixes.keys():
            if p == server_id:
                prefix = str(prefixes[p])
                return prefix
    
@bot.command()
async def wynhelp(ctx):
    
    id = str(ctx.message.guild.id)
    rgb = server_embed_color(id)
    server_prefix = get_server_prefix(id)
                
    await ctx.send("Read The Embed Below If You Need Some Help!")
    embed = discord.Embed(title = "Winterdrop Help!", description = "", color = discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2]))
    embed.add_field(name = "Command List", value = "Here are all commands", inline = False)
    embed.add_field(name = f"{server_prefix}setdefaultcolor", value = "Set The Default Color Of Your Embeds For Your Server!", inline = True)
    embed.add_field(name = f"{server_prefix}mute <@member> [duration] [reason (optional)]", value = "Mutes A Member For A Specific Duration", inline = True)
    embed.add_field(name = "#clear (number)", value = "Clears the number of messages given by the user. If number is not entered, deletes the most recent message. \nAliases = c \nPermissions = Manage Messages", inline = True)
    embed.add_field(name = "#kick (mention)", value = "Kicks the member mentioned. \nAliases: k \n Permissions: Kick Members", inline = True)
    embed.add_field(name = "#ban (mention)", value = "Bans the member mentioned. \nAliases: b \n Permissions: Ban Members", inline = True)
    embed.add_field(name = "#unban (username with tag)", value = "Unbans the member specified. \nAliases: ub \n Permissions: Ban Members", inline = True)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)
    

    
# @bot.command()
# @commands.check(is_it_owner)
# async def example(ctx):
#     await ctx.send(f'hi i am {ctx.author}')

# Kick Command     
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : commands.MemberConverter, *, reason = None):
   
    await member.kick(reason = reason)
    await member.send(f"You have been kicked from {ctx.message.guild.name}")
    await ctx.send(f'Kicked {member.mention}') 

# Kick Error Message    
@kick.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please Specify Who You Would Like To Kick! + reason (optional)')

# Ban Command    
@bot.command()
async def ban(ctx, member : commands.MemberConverter, *, reason = None):
    await member.ban(reason = reason)
    try:
        await member.send(f"You have been banned from {ctx.message.guild.name}")
    except:
       await ctx.send(f'Banned {member.mention}') 
    
    

# Ban Error Message
@ban.error    
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please Specify Who You Would Like To Ban! + reason (optional)')
        


######################### DM TRYOUT!!
# @bot.command()
# async def dm_command(ctx):
#     if isinstance(ctx.channel, discord.channel.DMChannel):   
#         await ctx.author.send('hallo!!')
        
# Soft Ban Command    
class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]
        
        if amount.isdigit() and unit in ['s', 'm', 'h','d', 'mo']:
            return (int(amount), unit)
        
        raise commands.BadArgument(message = "Not A Valid Duration")

@bot.command()
async def softban(ctx, member : commands.MemberConverter, duration: DurationConverter, *, reason = None):
    
    multiplier = {'s' : 1, 'm' : 60, 'h': 3600, 'd' : 86400, 'w' : 604800, 'mo' : 2628288}
    amount, unit = duration
    
    await member.ban(reason = reason)
    await ctx.guild.ban(member)
    await ctx.send(f'Banned {member.mention} for {amount}{unit}.') 
    await asyncio.sleep(amount * multiplier[unit])
    await ctx.guild.unban(member)
# Soft Ban Error Message
# @softban.error    
# async def clear_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('Please Specify Who You Would Like To Ban! + reason (optional)')

# Unban Command    
@bot.command()
async def unban(ctx, *, member : commands.MemberConverter):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
    await ctx.send(f"{member} wasn't found.")
# Unban Error Message    
@unban.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please Specify Who You Would Like To Unban! + reason (optional)')

# Mute Command
@bot.command(pass_context = True)
@commands.has_permissions(manage_roles = True)
async def mute(ctx, member : commands.MemberConverter, duration: DurationConverter, *, reason):
    multiplier = {'s' : 1, 'm' : 60, 'h': 3600, 'd' : 86400, 'w' : 604800, 'mo' : 2628288}
    amount, unit = duration

    muted_role = ctx.guild.get_role(907977642937024512)
    await member.add_roles(muted_role)
    await ctx.send(f'Muted {member.mention} For {amount}{unit} Because {reason}')
    await asyncio.sleep(amount * multiplier[unit])
    await member.remove_roles(muted_role)
    
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(f"{ctx.author.mention} I'm afraid that member doesn't exist")
        
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} I don't think you have the right permissions. :c")

# Get Server ID    
@bot.command(pass_context=True)
async def getguild(ctx):
    id = int(ctx.message.guild.id)
    await ctx.send(f'Your Server ID:    {id}')
    
# 8ball Function    
@bot.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt',
                 'Yes - definitely.',
                 'You may rely on it.',
                 'As I see it, yes',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 "Don't count on it.",
                 'My reply is no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")
    
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


    
bot.run('OTA1MjU3OTAyMTU4MjYyMzEz.YYHdHg.kNvx-VfOxuDRhLeYdrwZQkjLDjk')

