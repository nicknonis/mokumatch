#for now this bot does nothing and is infact just the example bot.
import discord
import asyncio
import random 
import logging
from discord.ext import commands

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='log', encoding='utf-8', mode='w')
log.addHandler(handler)

# Get token from local dir text file
tokenFile = open("token", 'r')
token = tokenFile.read()
tokenFile.close()



'''
-----------------------
        BOT JOIN
-----------------------
'''
sudo_list = ['329513316835655680','329513060614012928'] #mod and admin user groups
region_list = ['NA', 'EU', 'AUS', 'ASIA','SEA']

prefix = '~' #can swap to array to allow more prefixes...
description = "Moku the lobby and matchmaking bot"
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None)


@bot.event
async def on_ready():
    # Display Login Status in Console
    print('<---------------------------->')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('<---------------------------->')
    while True:
        await bot.change_presence(game=discord.Game(name='Combot is my friend.'))
        await asyncio.sleep(15)
        await bot.change_presence(game=discord.Game(name='type ~help for assistance!'))
        await asyncio.sleep(10000)
        await bot.change_presence(game=discord.Game(name='git gud'))
        await asyncio.sleep(30)


'''
--------------------
    Welcome Message
--------------------
'''        

@bot.event        
async def on_member_join(member):
    server = member.server
    bot_fmt = 'Welcome {0.mention} to {1.name}! I am Moku, type ~help to get help.'
    await bot.send_message(server, bot_fmt.format(member, server))



'''
    ---------------------
            HELP Func
    ---------------------
'''    
@asyncio.coroutine
def _default_help_command(ctx, *commands : str):
    """Shows this message."""
    bot = ctx.bot
    destination = ctx.message.author if bot.pm_help else ctx.message.channel

    def repl(obj):
        return _mentions_transforms.get(obj.group(0), '')

    # help by itself just lists commands.
    if len(commands) == 0:
        pages = bot.formatter.format_help_for(ctx, bot)
    elif len(commands) == 1:
        name = _mention_pattern.sub(repl, commands[0])
        command = None
        if name in bot.cogs:
            command = bot.cogs[name]
        else:
            command = bot.commands.get(name)
            if command is None:
                yield from bot.send_message(destination, bot.command_not_found.format(name))
                return

        pages = bot.formatter.format_help_for(ctx, command)
    else:
        name = _mention_pattern.sub(repl, commands[0])
        command = bot.commands.get(name)
        if command is None:
            yield from bot.send_message(destination, bot.command_not_found.format(name))
            return
''' 
    ----------------
        Commands
    ----------------	
'''


@bot.event
async def on_message(message):
# prevent bot from replying to itself incase such a condition arises..
    if message.author.bot:
        # check if sent by self
        if message.author.id == bot.user.id:
            await botn_message_cleanup(message)
            return
        

    if message.content.startswith(prefix): 
        #for quick and simple functions with dynamic prefix. makes it easier to maintain.
        fntMsg = message.content                    
        fntMsg = fntMsg.replace(prefix, "") 
          
            

    await bot.process_commands(message) 

@bot.command(pass_context=True)    
@commands.has_permissions(administrator=True)
async def sleep(ctx):
    """Puts moku to sleep for 15 seconds. [Admin Only]"""
    await asyncio.sleep(15)
    await bot.send_message(ctx.message.channel, 'Done sleeping')
    
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx):
    """Delete last 100 messages[Admin Only]"""
    mgs = []
    tmp = await bot.send_message(ctx.message.channel, 'Clearing messages...')
    await asyncio.sleep(5)
    async for mgs in bot.logs_from(ctx.message.channel, limit=100):
        await bot.delete_message(mgs)       
    
    
@bot.command(pass_context=True)
async def hello(ctx):
    """Moku will greet you."""
    msg = 'Hello {0.author.mention}'.format(ctx.message)
    await bot.send_message(ctx.message.channel, msg)        
    
@bot.command(pass_context=True)
async def count(ctx):
    """Counts messages sent."""
    counter = 0
    tmp = await bot.send_message(ctx.message.channel,'Calculating messages...')
    async for log in bot.logs_from(ctx.message.channel, limit=100):
        if log.author == ctx.message.author:
            counter += 1
        await bot.edit_message(tmp, 'You have {} messages.'.format(counter)) 

''' 
    ---------------------------------
        REGION/ROLE ASSIGNMENT 
     ---------------------------------
'''
            
            #can be swapped and used as role manager instead.
            
@bot.command(pass_context=True)       
async def region(ctx):  
    """Assigns a region to requester. [ex: ~region NA]""" 
    member = ctx.message.author
    region = ctx.message.content[8:].upper()
    role_exists = False
    user_has_role = False
    for role in ctx.message.server.roles:
        if role.name == region:
            role_exists = True
            actual_role = role
            break
    if not role_exists:
            await bot.send_message(ctx.message.channel, ("Region does not exist.\nAvailable regions are {0}.".format(region_list)).strip('[]'))
            return
    if role_exists:
        # Replace the region
        for role in member.roles:  
            if role.name in region_list:  
                user_has_role = True
                try:
                    await bot.remove_roles(ctx.message.author, role)
                    await bot.add_roles(member, actual_role)
                    await bot.send_message(ctx.message.channel, "Region changed for user to {0}.".format(region))
                    return
                except discord.Forbidden:
                    await bot.send_message(ctx.message.channel, "bot lacks the permissions to do that...")
                    return    
        if not user_has_role:  # user doesnt have the role yet
            try:
                await bot.add_roles(member, actual_role)
                await bot.send_message(ctx.message.channel, "Region for user set to {0}.".format(region))
            except discord.Forbidden:
                await bot.send_message(ctx.message.channel, "bot lacks the permissions to do that...")
                            
@bot.command(pass_context=True)       
async def rmregion(ctx):  
    """Removes region from requester. [ex: ~region NA]""" 
    member = ctx.message.author    
    for role in member.roles:  # Replace existing region
        if role.name in region_list:  
            try:
                await bot.remove_roles(member, role)
                await bot.send_message(ctx.message.channel, "Region removed from user successfully.")
                return
            except discord.Forbidden:
                await bot.send_message(ctx.message.channel, "bot lacks the permissions to do that...")
                return    
      
      


''' 
    -------------------
        Auto Clean Up
    -------------------	
'''

#delete bot messages.        
async def botn_message_cleanup(message):
    if message.channel.is_private:
        return
    if message.channel.permissions_for(message.server.me).manage_messages:
        await asyncio.sleep(60)
        await bot.delete_message(message)
    else:
        print("bot lacks the permissions required to delete user messages.")


        
        
bot.run(token)
