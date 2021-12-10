import discord
import json
import os
from discord.ext import commands, tasks
import random
from itertools import cycle
import sys



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
bot = commands.Bot(command_prefix = get_prefix)

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
        

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        
    prefixes.pop(str(guild.id))
    
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)
        
@bot.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        
    prefixes[str(ctx.guild.id)] = prefix
    
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)
        
    await ctx.send(f'Prefix changed to: `{prefix}`')
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Please Note My Prefix Is `{get_prefix}` In This Server!',delete_after=5.0) 
        
    # elif isinstance((error, commands.CommandNotFound) and (ctx.channel, discord.channel.DMChannel)):
    #     await ctx.author.send('Please Note My Prefix Is `nn.` in DMs!',delete_after=5.0)
    else:
        pass   
    
# @bot.command(pass_context=True)
# async def getguild(ctx):
#     id = int(ctx.message.guild.id)
#     await ctx.send(f'Your Server ID:    {id}')
    
    
# with open('prefixes.json', 'r') as json_file:
#    data = json.load(json_file)
   
# print("Type", type(data))
# print("\nID:" data[id])



# Looping Status    
status =['Spreading Kindness', 
                'Staying Hydrated', 
                'Cutely Moderating', 
                'Munching On Midnight Snacks', 
                'Taking A Breather', 
                'Dozing Away To Sleep', 
                'Siping My Morning Coffee', 
                "Setting A Reminder To Remind Me I'm A Cutie", 
                "Persevering Through My Difficulties",
                "Vibin' With My Music",
                "Flying In My Dreams",
                "Sending Good Vibes and Wishes",
                "Showing Coot Eyes To Grab Attention"]    
@tasks.loop(seconds = 5)
async def change_status():
    await bot.change_presence(activity = discord.Game(random.choice(status)))

# Loading Cogs    
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

# Unloading Cogs    
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    
@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

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

# Clear Error Message Not Right Perms
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("I'm Sorry I Don't Think You Have The Right Permissions To Use This Command! Please Make Sure You Have The `Manage Permissions` Enabled To Run This Command!")


# def is_it_me(ctx):
#     return ctx.author.id == 800091221652799500
    
# @bot.command()
# @commands.check(is_it_me)
# async def example(ctx):
#     await ctx.send(f'hi i am {ctx.author}')
        
# Kick Command     
@bot.command()
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)

# Kick Error MEssage    
@kick.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please Specify Who You Would Like To Kick! + reason (optional)')

# Ban Command    
@bot.command()
async def ban(ctx, member : commands.MemberConverter, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'Banned {member.mention}') 

# Ban Error Message
@ban.error    
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please Specify Who You Would Like To Ban! + reason (optional)')


@bot.command(aliases = ['hello','hey'])
async def hi(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):   
        await ctx.author.send('hallo!!', delete_after=10.0)


        
# # Soft Ban Command    
# @bot.command()
# async def softban(ctx, member : commands.MemberConverter, *, reason = None):
#     await member.ban(reason = reason)
#     await ctx.send(f'Banned {member.mention}') 

# # Soft Ban Error Message
# @softban.error    
# async def clear_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('Please Specify Who You Would Like To Ban! + reason (optional)')

# Unban Command    
@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
# Unban Error Message    
@unban.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please Specify Who You Would Like To Unban! + reason (optional)')

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

