#for now this moku does nothing and is infact just the example bot.
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

moku = discord.Client()

'''
-----------------------
        BOT JOIN
-----------------------
'''
@moku.event
async def on_ready():
    # Display Login Status in Console
    print('<---------------------------->')
    print('Logged in as')
    print(moku.user.name)
    print(moku.user.id)
    print('<---------------------------->')
    while True:
        await moku.change_presence(game=discord.Game(name='Combot is my friend.'))
        await asyncio.sleep(15)
        await moku.change_presence(game=discord.Game(name='type ~help for assistance!'))
        await asyncio.sleep(10000)
        await moku.change_presence(game=discord.Game(name='git gud'))
        await asyncio.sleep(30)

'''
--------------------
    Welcome Message
--------------------
'''        

@moku.event        
async def on_member_join(member):
    server = member.server
    moku_fmt = 'Welcome {0.mention} to {1.name}!'
    await moku.send_message(server, moku_fmt.format(member, server))
        
''' 
    ----------------
        Commands
    ----------------	
'''

@moku.event
async def on_message(message):
# prevent bot from replying to itself incase such a condition arises..
    if message.author == moku.user:
        await mokun_message_cleanup(message)
        return

    else:
        if message.content.startswith('~hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await moku.send_message(message.channel, msg)
              
            
            
        if message.content.startswith('~count'):
            counter = 0
            tmp = await moku.send_message(message.channel, 'Calculating messages...')
            async for log in moku.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1
            await moku.edit_message(tmp, 'You have {} messages.'.format(counter))
             
            

        if message.content.startswith('~sleep'):
            await asyncio.sleep(15)
            await moku.send_message(message.channel, 'Done sleeping')
        #delete all messages 
        if message.content.startswith('~delete'):
            mgs = []
            tmp = await moku.send_message(message.channel, 'Clearing messages...')
            await asyncio.sleep(5)
            async for mgs in moku.logs_from(message.channel, limit=100):
                await moku.delete_message(mgs)
        
        
        
            
''' 
    -------------------
        Auto Clean Up
    -------------------	
'''

#delete moku messages.        
async def mokun_message_cleanup(message):
    if message.channel.is_private:
        return
    if message.channel.permissions_for(message.server.me).manage_messages:
        await asyncio.sleep(60)
        await moku.delete_message(message)
    else:
        print("Moku lacks the permissions required to delete user messages.")



moku.run(token)
